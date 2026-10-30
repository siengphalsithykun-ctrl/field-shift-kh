# Field Shift KH

A bilingual (Khmer/English) map that turns NASA Earth data into rice planting guidance for Cambodian farmers.
NASA Space Apps Challenge Cambodia 2026, challenge "Field Shift: Adapting Farms with NASA Data".

## Getting the data

```bash
pip install -r requirements.txt
python src/fetch_power.py            # 2000-2025 baseline (about 1 minute)
python src/fetch_power.py --current  # 2026 season up to today
```

Outputs go to `data/raw/power/` (raw API responses) and `data/processed/power_daily*.csv`.
Missing values from the API (`-999`) are left empty in the CSV; they are not filled in.

## Building the map

```bash
python src/analysis.py   # season check, monsoon onset, dry-spell/flood risk, tips, back-test -> data/processed/summary.json
python src/build_map.py  # bilingual Folium map -> docs/index.html
```

All thresholds are in `RULES` at the top of `src/analysis.py`. They are starting assumptions, not validated agronomic advice.
The Khmer text in `src/build_map.py` is a draft and needs checking by a native speaker.

## NASA data and other resources used

| Resource | What we use it for | Link |
|---|---|---|
| NASA POWER daily point API (AG community) | Rainfall (`PRECTOTCORR`), temperature (`T2M`, `T2M_MAX`), root-zone soil wetness (`GWETROOT`), 2000 to today | https://power.larc.nasa.gov/ |
| Folium / Leaflet | Interactive map | https://python-visualization.github.io/folium/ |
| OpenStreetMap | Base map tiles | https://www.openstreetmap.org/copyright |
| Noto Sans Khmer (Google Fonts) | Khmer text | https://fonts.google.com/noto/specimen/Noto+Sans+Khmer |

Known limitation: POWER data is on a coarse grid (about 0.5°), so each province value is for the grid cell
around its centroid, not an average over the whole province.

## AI use disclosure

Parts of this project's code were generated with AI assistance (Claude Code, by Anthropic) and reviewed by the team.
Generated files say so in their header, and `data/processed/power_metadata*.json` records it too.
No NASA logos or branding are used in AI-generated content.
