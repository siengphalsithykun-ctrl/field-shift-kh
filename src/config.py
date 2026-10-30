"""Shared settings for Field Shift KH (provinces, dates, NASA POWER parameters).

Partly generated with AI assistance (Claude Code); reviewed by the team.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw" / "power"
RAW_CURRENT_DIR = RAW_DIR / "current"
PROCESSED_DIR = ROOT / "data" / "processed"

# All 25 provinces. lat/lon is the point sent to NASA POWER: the province shape's centroid
# (or a point inside the shape if the centroid falls outside), from src/prepare_boundaries.py.
# POWER data is on a ~0.5° grid, so small provinces (Phnom Penh, Kep, Pailin) get the
# value of the grid cell they sit in, shared with neighbouring areas.
PROVINCES = [
    {"slug": "banteay_meanchey", "name_en": "Banteay Meanchey", "name_km": "បន្ទាយមានជ័យ", "lat": 13.71, "lon": 103.01},
    {"slug": "battambang", "name_en": "Battambang", "name_km": "បាត់ដំបង", "lat": 12.98, "lon": 103.10},
    {"slug": "kampong_cham", "name_en": "Kampong Cham", "name_km": "កំពង់ចាម", "lat": 12.13, "lon": 105.27},
    {"slug": "kampong_chhnang", "name_en": "Kampong Chhnang", "name_km": "កំពង់ឆ្នាំង", "lat": 12.17, "lon": 104.56},
    {"slug": "kampong_speu", "name_en": "Kampong Speu", "name_km": "កំពង់ស្ពឺ", "lat": 11.54, "lon": 104.29},
    {"slug": "kampong_thom", "name_en": "Kampong Thom", "name_km": "កំពង់ធំ", "lat": 12.82, "lon": 105.05},
    {"slug": "kampot", "name_en": "Kampot", "name_km": "កំពត", "lat": 10.80, "lon": 104.31},
    {"slug": "kandal", "name_en": "Kandal", "name_km": "កណ្ដាល", "lat": 11.42, "lon": 105.02},
    {"slug": "kep", "name_en": "Kep", "name_km": "កែប", "lat": 10.52, "lon": 104.34},
    {"slug": "koh_kong", "name_en": "Koh Kong", "name_km": "កោះកុង", "lat": 11.51, "lon": 103.41},
    {"slug": "kratie", "name_en": "Kratie", "name_km": "ក្រចេះ", "lat": 12.63, "lon": 106.17},
    {"slug": "mondulkiri", "name_en": "Mondulkiri", "name_km": "មណ្ឌលគិរី", "lat": 12.77, "lon": 106.99},
    {"slug": "oddar_meanchey", "name_en": "Oddar Meanchey", "name_km": "ឧត្ដរមានជ័យ", "lat": 14.17, "lon": 103.79},
    {"slug": "pailin", "name_en": "Pailin", "name_km": "ប៉ៃលិន", "lat": 12.88, "lon": 102.63},
    {"slug": "phnom_penh", "name_en": "Phnom Penh", "name_km": "ភ្នំពេញ", "lat": 11.56, "lon": 104.86},
    {"slug": "preah_sihanouk", "name_en": "Preah Sihanouk", "name_km": "ព្រះសីហនុ", "lat": 10.86, "lon": 103.80},
    {"slug": "preah_vihear", "name_en": "Preah Vihear", "name_km": "ព្រះវិហារ", "lat": 13.80, "lon": 105.01},
    {"slug": "prey_veng", "name_en": "Prey Veng", "name_km": "ព្រៃវែង", "lat": 11.40, "lon": 105.42},
    {"slug": "pursat", "name_en": "Pursat", "name_km": "ពោធិ៍សាត់", "lat": 12.37, "lon": 103.64},
    {"slug": "ratanakiri", "name_en": "Ratanakiri", "name_km": "រតនគិរី", "lat": 13.80, "lon": 107.09},
    {"slug": "siem_reap", "name_en": "Siem Reap", "name_km": "សៀមរាប", "lat": 13.48, "lon": 104.02},
    {"slug": "stung_treng", "name_en": "Stung Treng", "name_km": "ស្ទឹងត្រែង", "lat": 13.81, "lon": 106.18},
    {"slug": "svay_rieng", "name_en": "Svay Rieng", "name_km": "ស្វាយរៀង", "lat": 11.16, "lon": 105.86},
    {"slug": "takeo", "name_en": "Takeo", "name_km": "តាកែវ", "lat": 10.94, "lon": 104.82},
    {"slug": "tbong_khmum", "name_en": "Tbong Khmum", "name_km": "ត្បូងឃ្មុំ", "lat": 11.94, "lon": 105.89},
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
