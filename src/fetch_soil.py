"""Download topsoil properties for each province point from ISRIC SoilGrids.

Usage:
    python src/fetch_soil.py            # skips provinces already downloaded
    python src/fetch_soil.py --force    # re-download

Outputs:
    data/raw/soil/<province>.json    raw API response
    data/processed/soil.csv          one row per province: clay, sand, silt-free texture class,
                                     organic carbon and pH, averaged over 0-30 cm

Data source: ISRIC SoilGrids 2.0 (CC-BY 4.0), https://soilgrids.org/
SoilGrids is a 250 m global model, not a field survey: treat values as a regional guide.
Partly generated with AI assistance (Claude Code); reviewed by the team.
"""

import argparse
import json
import sys
import time

import pandas as pd
import requests

from config import PROCESSED_DIR, PROVINCES, ROOT

URL = "https://rest.isric.org/soilgrids/v2.0/properties/query"
PROPERTIES = ["clay", "sand", "soc", "phh2o"]
DEPTHS = {"0-5cm": 5, "5-15cm": 10, "15-30cm": 15}  # label -> thickness, for a depth-weighted mean
RAW_DIR = ROOT / "data" / "raw" / "soil"
OUT = PROCESSED_DIR / "soil.csv"
PAUSE_S = 13  # SoilGrids allows about 5 requests a minute
MAX_RETRIES = 4


def fetch(province):
    params = [("lon", province["lon"]), ("lat", province["lat"]), ("value", "mean")]
    params += [("property", p) for p in PROPERTIES] + [("depth", d) for d in DEPTHS]
    for attempt in range(MAX_RETRIES + 1):
        try:
            resp = requests.get(URL, params=params, timeout=90)
            if resp.status_code == 200:
                return resp.json()
            problem = f"HTTP {resp.status_code}"
        except requests.RequestException as e:
            problem = f"network error: {e}"
        if attempt == MAX_RETRIES:
            raise RuntimeError(f"gave up after {MAX_RETRIES + 1} attempts ({problem})")
        wait = 15 * (attempt + 1)
        print(f"    {problem}; retrying in {wait}s...")
        time.sleep(wait)


def summarise(data):
    """Depth-weighted 0-30 cm mean of each property, in normal units (%, g/kg, pH)."""
    out = {}
    for layer in data["properties"]["layers"]:
        factor = layer["unit_measure"]["d_factor"]
        values = [(d["values"]["mean"], DEPTHS[d["label"]]) for d in layer["depths"] if d["values"]["mean"] is not None]
        if not values:
            out[layer["name"]] = None
            continue
        out[layer["name"]] = sum(v * w for v, w in values) / sum(w for _, w in values) / factor
    return out


def texture(clay, sand):
    """Very simple texture group: enough to tell sandy from clayey soils."""
    if clay is None or sand is None:
        return None
    if sand >= 60:
        return "sandy"
    if clay >= 35:
        return "clayey"
    return "loamy"


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    failures, fetched = [], 0
    for p in PROVINCES:
        path = RAW_DIR / f"{p['slug']}.json"
        if path.exists() and not args.force:
            continue
        if fetched:
            time.sleep(PAUSE_S)
        print(f"  {p['name_en']}: downloading...")
        try:
            path.write_text(json.dumps(fetch(p)), encoding="utf-8")
            fetched += 1
        except RuntimeError as e:
            failures.append(p["name_en"])
            print(f"  {p['name_en']}: FAILED - {e}")

    rows = []
    for p in PROVINCES:
        path = RAW_DIR / f"{p['slug']}.json"
        if not path.exists():
            continue
        s = summarise(json.loads(path.read_text(encoding="utf-8")))
        rows.append(
            {
                "province": p["slug"],
                "clay_pct": round(s["clay"], 1) if s["clay"] is not None else None,
                "sand_pct": round(s["sand"], 1) if s["sand"] is not None else None,
                "soc_g_kg": round(s["soc"], 1) if s["soc"] is not None else None,
                "ph": round(s["phh2o"], 1) if s["phh2o"] is not None else None,
                "texture": texture(s["clay"], s["sand"]),
            }
        )
    df = pd.DataFrame(rows)
    df.to_csv(OUT, index=False)
    print(f"\nWrote {len(df)} provinces to {OUT.relative_to(ROOT)}")
    print(df.to_string(index=False))
    if failures:
        print(f"\nFailed: {', '.join(failures)}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
