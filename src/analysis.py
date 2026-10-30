"""Turn NASA POWER daily data into season status, planting window, risk alerts, tips and
crop-rotation tests.

Usage:
    python src/analysis.py    # reads data/processed/power_daily*.csv (+ soil.csv), writes data/processed/summary.json

Rotation options and their assumptions live in src/rotations.py.

All rules are simple, transparent thresholds (no trained model). They are starting
assumptions to validate with mentors and agronomic sources; tune them in RULES below.

Partly generated with AI assistance (Claude Code); reviewed by the team.
"""

import json

import pandas as pd

from config import PROCESSED_DIR, PROVINCES
from rotations import HEAT_BAD_DAYS, ROTATIONS, SOIL_WATER_PER_TENTH_MM

RULES = {
    "dry_day_mm": 1.0,  # a day with less rain than this counts as dry
    "onset_earliest": "04-01",  # onset search starts on this day each year
    "onset_3day_mm": 20.0,  # 3-day rain needed to call onset
    "onset_no_dry_spell_days": 7,  # ...and no dry spell this long in the next 30 days
    "onset_late_days": 14,  # onset this many days after the normal date = late
    "planting_window_days": 21,  # recommended sowing/transplanting window after onset
    "wet_season": ("05-01", "10-31"),
    "dry_spell_yellow": 7,
    "dry_spell_red": 10,
    "rain_anomaly_yellow": 20,  # % below/above normal
    "rain_anomaly_red": 40,
    "flood_yellow_pct": 95,  # 3-day rain above this percentile of the wet-season normal
    "flood_red_pct": 99,
    "recent_days": 30,  # window for "right now" checks (soil moisture, flood)
}

LEVELS = ["green", "yellow", "red"]


def load():
    base = pd.read_csv(PROCESSED_DIR / "power_daily.csv", parse_dates=["date"])
    cur = pd.read_csv(PROCESSED_DIR / "power_daily_current.csv", parse_dates=["date"])
    return pd.concat([base, cur], ignore_index=True)


def worst(*levels):
    return max(levels, key=LEVELS.index)


def run_lengths(dry):
    """For a boolean Series, the length of the dry run each day belongs to (0 on wet days)."""
    groups = (dry != dry.shift()).cumsum()
    return dry.groupby(groups).transform("size") * dry


def longest_dry_spell(rain):
    if rain.empty:
        return 0
    return int(run_lengths(rain < RULES["dry_day_mm"]).max())


def monsoon_onset(rain, year):
    """First day from 1 April with 3-day rain >= 20 mm and no 7-day dry spell in the next 30 days."""
    season = rain[f"{year}-{RULES['onset_earliest']}" : f"{year}-12-31"]
    rain3 = season.rolling(3).sum()
    for day in rain3[rain3 >= RULES["onset_3day_mm"]].index:
        next30 = rain[day + pd.Timedelta(days=1) : day + pd.Timedelta(days=30)]
        if len(next30) < 30:
            return None  # not enough data yet to confirm
        if longest_dry_spell(next30) < RULES["onset_no_dry_spell_days"]:
            return day
    return None


def wet_season(rain, year):
    start, end = RULES["wet_season"]
    return rain[f"{year}-{start}" : f"{year}-{end}"]


def analyse_province(df, current_year):
    df = df.set_index("date").sort_index()
    rain, soil = df["precip_mm"], df["gwetroot"]
    last_day = df.index.max()
    base_years = range(df.index.year.min(), current_year)

    # --- Monsoon onset and planting window ---
    onsets = {y: monsoon_onset(rain, y) for y in list(base_years) + [current_year]}
    base_doys = pd.Series([d.dayofyear for y, d in onsets.items() if d is not None and y != current_year])
    normal_onset_doy = int(base_doys.median())
    normal_onset = pd.Timestamp(current_year, 1, 1) + pd.Timedelta(days=normal_onset_doy - 1)
    onset = onsets[current_year]
    window_days = pd.Timedelta(days=RULES["planting_window_days"])
    if onset is None:
        onset_delay, onset_level = None, "yellow"
    else:
        onset_delay = (onset - normal_onset).days
        onset_level = "red" if onset_delay > RULES["onset_late_days"] else "green"

    # --- Season rainfall vs the same calendar period in past years ---
    start_md = RULES["wet_season"][0]
    end_md = last_day.strftime("%m-%d")
    season_rain = rain[f"{current_year}-{start_md}" : last_day].sum()
    normal_season_rain = pd.Series([rain[f"{y}-{start_md}" : f"{y}-{end_md}"].sum() for y in base_years]).mean()
    rain_anomaly = 100 * (season_rain - normal_season_rain) / normal_season_rain
    rain_level = (
        "red"
        if abs(rain_anomaly) >= RULES["rain_anomaly_red"]
        else "yellow" if abs(rain_anomaly) >= RULES["rain_anomaly_yellow"] else "green"
    )

    # --- Soil moisture, last 30 days vs the same days in past years ---
    recent = pd.Timedelta(days=RULES["recent_days"] - 1)
    soil_now = soil[last_day - recent : last_day].mean()
    soil_normal = pd.Series(
        [soil[last_day.replace(year=y) - recent : last_day.replace(year=y)].mean() for y in base_years]
    ).mean()

    # --- Dry-spell risk: longest dry spell so far this wet season ---
    dry_spell = longest_dry_spell(wet_season(rain, current_year))
    dry_level = (
        "red"
        if dry_spell >= RULES["dry_spell_red"]
        else "yellow" if dry_spell >= RULES["dry_spell_yellow"] else "green"
    )

    # --- Flood risk: biggest 3-day rain in the last 30 days vs wet-season normal ---
    rain3 = rain.rolling(3).sum()
    base_wet3 = pd.concat([wet_season(rain3, y) for y in base_years])
    p_yellow = base_wet3.quantile(RULES["flood_yellow_pct"] / 100)
    p_red = base_wet3.quantile(RULES["flood_red_pct"] / 100)
    recent_max3 = rain3[last_day - recent : last_day].max()
    flood_level = "red" if recent_max3 >= p_red else "yellow" if recent_max3 >= p_yellow else "green"

    # --- Monthly rain this year vs normal (for the pop-up chart) ---
    monthly = rain.resample("MS").sum()
    normal_monthly = monthly[monthly.index.year < current_year].groupby(monthly.index.month[monthly.index.year < current_year]).mean()
    this_year = monthly[monthly.index.year == current_year]
    # Last month is partial: scale isn't fair, so flag it instead of comparing directly.
    monthly_chart = [
        {
            "month": int(m),
            "normal_mm": round(float(normal_monthly[m]), 1),
            "this_year_mm": round(float(this_year[this_year.index.month == m].sum()), 1)
            if m <= last_day.month
            else None,
            "partial": m == last_day.month,
        }
        for m in range(1, 13)
    ]

    # --- Back-test: years the rules would have flagged ---
    backtest = []
    for y in base_years:
        d = onsets[y]
        delay = None if d is None else d.dayofyear - normal_onset_doy
        spell = longest_dry_spell(wet_season(rain, y))
        backtest.append(
            {
                "year": y,
                "onset": None if d is None else d.strftime("%Y-%m-%d"),
                "onset_delay_days": delay,
                "late_onset": delay is None or delay > RULES["onset_late_days"],
                "longest_dry_spell_days": spell,
                "dry_spell_alert": spell >= RULES["dry_spell_red"],
                "season_rain_mm": round(float(wet_season(rain, y).sum()), 0),
            }
        )

    # --- Adaptation tips (ids; build_map.py holds the Khmer/English text) ---
    tips = []
    if onset_level == "red" or onset is None:
        tips += ["delay_transplanting", "short_duration_variety"]
    if dry_level != "green" or (rain_level != "green" and rain_anomaly < 0):
        tips += ["save_water", "short_duration_variety"]
    if flood_level != "green" or (rain_level != "green" and rain_anomaly > 0):
        tips += ["drainage", "raise_seedbed"]
    if not tips:
        tips = ["normal_calendar"]
    tips = list(dict.fromkeys(tips))  # de-duplicate, keep order

    return {
        "last_data_date": last_day.strftime("%Y-%m-%d"),
        "overall": worst(onset_level, rain_level, dry_level, flood_level),
        "onset": {
            "level": onset_level,
            "date": None if onset is None else onset.strftime("%Y-%m-%d"),
            "normal_date": normal_onset.strftime("%m-%d"),
            "delay_days": onset_delay,
            "window_start": None if onset is None else onset.strftime("%Y-%m-%d"),
            "window_end": None if onset is None else (onset + window_days).strftime("%Y-%m-%d"),
        },
        "season_check": {
            "level": rain_level,
            "season_rain_mm": round(float(season_rain), 0),
            "normal_season_rain_mm": round(float(normal_season_rain), 0),
            "rain_anomaly_pct": round(float(rain_anomaly), 0),
            "soil_moisture_now": round(float(soil_now), 2),
            "soil_moisture_normal": round(float(soil_normal), 2),
        },
        "dry_spell": {"level": dry_level, "longest_days": dry_spell},
        "flood": {
            "level": flood_level,
            "recent_max_3day_mm": round(float(recent_max3), 0),
            "p95_3day_mm": round(float(p_yellow), 0),
            "p99_3day_mm": round(float(p_red), 0),
        },
        "tips": tips,
        "monthly": monthly_chart,
        "backtest": backtest,
    }


def load_soil():
    path = PROCESSED_DIR / "soil.csv"
    if not path.exists():
        return {}
    # SoilGrids has no values for some points (e.g. city areas); those provinces fall back to loamy soil.
    soil = pd.read_csv(path).dropna(subset=["texture"])
    return {r["province"]: r for r in soil.to_dict("records")}


def analyse_rotations(df, soil, current_year):
    """Test each rotation against every past year's NASA POWER weather (see rotations.py)."""
    df = df.set_index("date").sort_index()
    rain, wet, tmax = df["precip_mm"], df["gwetroot"], df["t2m_max_c"]
    years = range(df.index.year.min(), current_year)
    texture = (soil or {}).get("texture") or "loamy"
    per_tenth = SOIL_WATER_PER_TENTH_MM[texture]

    # Months that are normally too dry for a crop without irrigation: when fields usually sit bare.
    monthly = rain.resample("MS").sum()
    normal_monthly = monthly[monthly.index.year < current_year].groupby(monthly.index.month[monthly.index.year < current_year]).mean()
    bare_months = [int(m) for m in normal_monthly.index if normal_monthly[m] < 50]

    results = {}
    for rot in ROTATIONS:
        w = rot["window"]
        if w is None:
            results[rot["id"]] = {"tested": False}
            continue
        by_start = {}
        for key, start_md in w["starts"].items():
            history = []
            for y in years:
                start = pd.Timestamp(f"{y}-{start_md}")
                end = start + pd.Timedelta(days=w["days"] - 1)
                if end > df.index.max():
                    continue
                window_rain = float(rain[start:end].sum())
                sowing_wetness = float(wet[start - pd.Timedelta(days=15) : start - pd.Timedelta(days=1)].mean())
                soil_water = max(0.0, sowing_wetness - 0.5) * 10 * per_tenth if w["uses_soil_water"] else 0.0
                heat_days = int((tmax[start:end] >= w["heat_limit_c"]).sum())
                history.append(
                    {
                        "year": y,
                        "rain_mm": window_rain,
                        "soil_water_mm": soil_water,
                        "heat_days": heat_days,
                        "water_ok": window_rain + soil_water >= w["water_need_mm"],
                        "heat_ok": heat_days < HEAT_BAD_DAYS,
                    }
                )
            h = pd.DataFrame(history)
            by_start[key] = {
                "sow": start_md,
                "years_tested": len(h),
                "reliability_rainfed": round(float((h["water_ok"] & h["heat_ok"]).mean()), 2),
                "reliability_irrigated": round(float(h["heat_ok"].mean()), 2),
                "mean_rain_mm": round(float(h["rain_mm"].mean())),
                "mean_soil_water_mm": round(float(h["soil_water_mm"].mean())),
                "mean_heat_days": round(float(h["heat_days"].mean()), 1),
                # Compact per-year record for the page: [year, water ok, heat ok]
                "years": [[int(r.year), int(r.water_ok), int(r.heat_ok)] for r in h.itertuples()],
            }
        results[rot["id"]] = {
            "tested": True,
            "water_need_mm": w["water_need_mm"],
            "heat_limit_c": w["heat_limit_c"],
            "days": w["days"],
            "by_start": by_start,
        }

    return {
        "soil": None
        if not soil
        else {k: soil[k] for k in ("clay_pct", "sand_pct", "soc_g_kg", "ph", "texture")},
        "soil_texture_used": texture,
        "bare_months": bare_months,
        "rotations": results,
    }


def main():
    df = load()
    soil = load_soil()
    if not soil:
        print("No data/processed/soil.csv yet (run src/fetch_soil.py); assuming loamy soil everywhere.")
    current_year = int(df["date"].dt.year.max())
    summary = {
        "generated_from": "NASA POWER daily point data (https://power.larc.nasa.gov/)",
        "current_year": current_year,
        "rules": RULES,
        "ai_disclosure": "Analysis code partly generated with AI assistance (Claude Code) and reviewed by the team.",
        "provinces": {},
    }
    for p in PROVINCES:
        result = analyse_province(df[df["province"] == p["slug"]], current_year)
        result["rotation"] = analyse_rotations(df[df["province"] == p["slug"]], soil.get(p["slug"]), current_year)
        summary["provinces"][p["slug"]] = {**p, **result}
        late = [b["year"] for b in result["backtest"] if b["late_onset"]]
        print(
            f"{p['name_en']:13} {result['overall']:6} onset {result['onset']['date']} "
            f"(normal {result['onset']['normal_date']}), rain {result['season_check']['rain_anomaly_pct']:+.0f}%, "
            f"dry spell {result['dry_spell']['longest_days']}d, late-onset years: {late}"
        )
        rot = result["rotation"]["rotations"]
        print(
            f"{'':13} soil {result['rotation']['soil_texture_used']:6} rotations (rain-fed reliability): "
            + ", ".join(
                f"{k} " + "/".join(f"{s['reliability_rainfed']:.0%}" for s in v["by_start"].values())
                for k, v in rot.items()
                if v["tested"]
            )
        )

    out = PROCESSED_DIR / "summary.json"
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nWrote {out.relative_to(PROCESSED_DIR.parent.parent)}")


if __name__ == "__main__":
    main()
