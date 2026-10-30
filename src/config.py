"""Shared settings for Field Shift KH (pilot provinces, dates, NASA POWER parameters).

Partly generated with AI assistance (Claude Code); reviewed by the team.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw" / "power"
RAW_CURRENT_DIR = RAW_DIR / "current"
PROCESSED_DIR = ROOT / "data" / "processed"

# Approximate province centroids (verify before the event).
PROVINCES = [
    {"slug": "takeo", "name_en": "Takeo", "name_km": "តាកែវ", "lat": 10.99, "lon": 104.78},
    {"slug": "prey_veng", "name_en": "Prey Veng", "name_km": "ព្រៃវែង", "lat": 11.48, "lon": 105.33},
    {"slug": "battambang", "name_en": "Battambang", "name_km": "បាត់ដំបង", "lat": 13.10, "lon": 103.20},
    {"slug": "kampong_thom", "name_en": "Kampong Thom", "name_km": "កំពង់ធំ", "lat": 12.71, "lon": 104.89},
]

# Baseline period used for the 20+ year "normal".
BASELINE_START = "20000101"
BASELINE_END = "20251231"

# Start of the current season data (--current mode fetches up to today).
CURRENT_START = "20260101"

POWER_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"
POWER_COMMUNITY = "AG"

# NASA POWER parameter -> column name in the processed CSV.
PARAMETERS = {
    "PRECTOTCORR": "precip_mm",  # precipitation, mm/day
    "T2M": "t2m_c",  # mean air temperature at 2 m, °C
    "T2M_MAX": "t2m_max_c",  # max air temperature at 2 m, °C
    "GWETROOT": "gwetroot",  # root-zone soil wetness, 0-1
}
