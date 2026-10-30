"""Download NASA POWER daily data for the pilot provinces and save a clean CSV.

Usage:
    python src/fetch_power.py            # baseline 2000-2025 (skips files already downloaded)
    python src/fetch_power.py --force    # re-download the baseline
    python src/fetch_power.py --current  # 2026-01-01 up to today (always re-downloads)

Outputs:
    data/raw/power/<province>.json            raw API response (baseline)
    data/raw/power/current/<province>.json    raw API response (current season)
    data/processed/power_daily.csv            tidy daily table (baseline)
    data/processed/power_daily_current.csv    tidy daily table (current season)
    data/processed/power_metadata*.json       request URLs, API version, missing-value counts

Data source: NASA POWER (https://power.larc.nasa.gov/), Agroclimatology (AG) community.
Partly generated with AI assistance (Claude Code); reviewed by the team.
"""

import argparse
import json
import sys
import time
from datetime import date, datetime, timezone

import pandas as pd
import requests

from config import (
    BASELINE_END,
    BASELINE_START,
    CURRENT_START,
    PARAMETERS,
    POWER_COMMUNITY,
    POWER_URL,
    PROCESSED_DIR,
    PROVINCES,
    RAW_CURRENT_DIR,
    RAW_DIR,
)

TIMEOUT_S = 60
MAX_RETRIES = 4  # waits 2, 4, 8, 16 s between attempts
PAUSE_BETWEEN_CALLS_S = 2
RETRYABLE_STATUS = {429, 500, 502, 503, 504}


class FetchError(Exception):
    pass


def build_params(province, start, end):
    return {
        "parameters": ",".join(PARAMETERS),
        "community": POWER_COMMUNITY,
        "longitude": province["lon"],
        "latitude": province["lat"],
        "start": start,
        "end": end,
        "format": "JSON",
    }


def request_with_retries(params):
    """GET the POWER API, retrying on network errors, 429 and 5xx."""
    for attempt in range(MAX_RETRIES + 1):
        try:
            resp = requests.get(POWER_URL, params=params, timeout=TIMEOUT_S)
        except requests.RequestException as e:
            problem = f"network error: {e}"
        else:
            if resp.status_code == 200:
                return resp.json()
            if resp.status_code not in RETRYABLE_STATUS:
                # Bad request (wrong parameter, date, coordinates): retrying won't help.
                raise FetchError(f"HTTP {resp.status_code}: {resp.text[:500]}")
            problem = f"HTTP {resp.status_code}"

        if attempt == MAX_RETRIES:
            raise FetchError(f"gave up after {MAX_RETRIES + 1} attempts ({problem})")
        wait = 2 ** (attempt + 1)
        print(f"    {problem}; retrying in {wait}s...")
        time.sleep(wait)


def validate(data, start, end):
    """Check the response has every parameter and one value per requested day."""
    values = data.get("properties", {}).get("parameter", {})
    missing = [p for p in PARAMETERS if p not in values]
    if missing:
        raise FetchError(f"response is missing parameters {missing}; messages: {data.get('messages')}")

    expected_days = len(pd.date_range(start, end, freq="D"))
    for p in PARAMETERS:
        if len(values[p]) != expected_days:
            raise FetchError(f"{p} has {len(values[p])} days, expected {expected_days}")


def fetch_province(province, start, end, out_dir, force):
    """Download one province to out_dir/<slug>.json. Returns the request URL."""
    out_path = out_dir / f"{province['slug']}.json"
    params = build_params(province, start, end)
    url = requests.Request("GET", POWER_URL, params=params).prepare().url

    if out_path.exists() and not force:
        print(f"  {province['name_en']}: already downloaded, skipping (use --force to refresh)")
        return url

    print(f"  {province['name_en']}: downloading {start}-{end}...")
    data = request_with_retries(params)
    validate(data, start, end)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(data), encoding="utf-8")
    return url


def raw_to_frame(province, data):
    """Turn one raw POWER response into a tidy DataFrame, with fill values as NaN."""
    fill_value = data["header"].get("fill_value", -999)
    values = data["properties"]["parameter"]

    df = pd.DataFrame({PARAMETERS[p]: values[p] for p in PARAMETERS})
    df.index = pd.to_datetime(df.index, format="%Y%m%d")
    # Leave gaps as NaN: filling rain with 0 would create fake dry spells.
    df = df.mask(df == fill_value)

    df.insert(0, "lon", province["lon"])
    df.insert(0, "lat", province["lat"])
    df.insert(0, "province", province["slug"])
    df.index.name = "date"
    return df.reset_index()


def process(raw_dir, out_csv, out_meta, urls, trim_trailing_gaps):
    frames, meta_provinces = [], {}
    for province in PROVINCES:
        raw_path = raw_dir / f"{province['slug']}.json"
        if not raw_path.exists():
            continue
        data = json.loads(raw_path.read_text(encoding="utf-8"))
        df = raw_to_frame(province, data)

        if trim_trailing_gaps:
            # The newest days are often not published yet and come back as fill values.
            has_data = df[list(PARAMETERS.values())].notna().any(axis=1)
            df = df.loc[: has_data[has_data].index.max()] if has_data.any() else df.iloc[0:0]

        frames.append(df)
        coords = data.get("geometry", {}).get("coordinates", [])
        meta_provinces[province["slug"]] = {
            "name_en": province["name_en"],
            "name_km": province["name_km"],
            "requested_lat": province["lat"],
            "requested_lon": province["lon"],
            "api_geometry_lon_lat_elev": coords,
            "request_url": urls.get(province["slug"]),
            "first_date": str(df["date"].min().date()) if len(df) else None,
            "last_date": str(df["date"].max().date()) if len(df) else None,
            "missing_values": {col: int(df[col].isna().sum()) for col in PARAMETERS.values()},
        }
        header = data["header"]

    if not frames:
        raise FetchError(f"no raw files found in {raw_dir}")

    all_df = pd.concat(frames, ignore_index=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    all_df.to_csv(out_csv, index=False, date_format="%Y-%m-%d")

    meta = {
        "source": "NASA POWER daily point API, Agroclimatology (AG) community",
        "source_url": "https://power.larc.nasa.gov/",
        "api_version": header.get("api", {}).get("version"),
        "api_sources": header.get("sources"),
        "fetched_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "columns": {col: p for p, col in PARAMETERS.items()},
        "missing_value_handling": "API fill value converted to empty (NaN); no gap filling.",
        "ai_disclosure": "Pipeline code partly generated with AI assistance (Claude Code) and reviewed by the team.",
        "provinces": meta_provinces,
    }
    out_meta.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    return all_df, meta


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--force", action="store_true", help="re-download files that already exist")
    parser.add_argument("--current", action="store_true", help="fetch the current season (2026-01-01 to today)")
    args = parser.parse_args()

    if args.current:
        start, end = CURRENT_START, date.today().strftime("%Y%m%d")
        raw_dir, force, suffix = RAW_CURRENT_DIR, True, "_current"
    else:
        start, end = BASELINE_START, BASELINE_END
        raw_dir, force, suffix = RAW_DIR, args.force, ""

    print(f"NASA POWER {start}-{end} for {len(PROVINCES)} provinces")
    urls, failures = {}, {}
    for i, province in enumerate(PROVINCES):
        if i > 0:
            time.sleep(PAUSE_BETWEEN_CALLS_S)
        try:
            urls[province["slug"]] = fetch_province(province, start, end, raw_dir, force)
        except (FetchError, ValueError) as e:
            failures[province["name_en"]] = str(e)
            print(f"  {province['name_en']}: FAILED - {e}")

    out_csv = PROCESSED_DIR / f"power_daily{suffix}.csv"
    out_meta = PROCESSED_DIR / f"power_metadata{suffix}.json"
    try:
        df, meta = process(raw_dir, out_csv, out_meta, urls, trim_trailing_gaps=args.current)
    except FetchError as e:
        print(f"Processing failed: {e}")
        return 1

    print(f"\nWrote {len(df):,} rows to {out_csv.relative_to(PROCESSED_DIR.parent.parent)}")
    for slug, info in meta["provinces"].items():
        gaps = {k: v for k, v in info["missing_values"].items() if v}
        print(f"  {info['name_en']}: {info['first_date']} to {info['last_date']}, missing: {gaps or 'none'}")

    if failures:
        print(f"\n{len(failures)} province(s) failed: {', '.join(failures)}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
