# Field Shift KH

A bilingual (Khmer/English) decision-support map for Cambodian rice farmers. It turns NASA Earth data into
planting alerts for the wet-season rice crop and compares **crop-rotation options** for the rest of the year
(bare dry season, mungbean, maize/vegetables, green manure), ranked by the farmer's own priorities.
NASA Space Apps Challenge Cambodia 2026, challenge "Field Shift: Adapting Farms with NASA Data".

Live map: https://siengphalsithykun-ctrl.github.io/field-shift-kh/ (link to one province with `#slug`, e.g. `#takeo`)

## Getting the data

```bash
pip install -r requirements.txt
python src/prepare_boundaries.py     # province shapes -> data/processed/provinces.geojson
python src/fetch_power.py            # 2000-2025 baseline for all 25 provinces (a few minutes)
python src/fetch_power.py --current  # 2026 season up to today
python src/fetch_soil.py             # topsoil texture, organic carbon, pH per province (SoilGrids, ~6 minutes)
```

The 25 provinces, with their Khmer names and the point sent to NASA POWER, are listed in `src/config.py`.
Each point is the province shape's centroid (checked to be inside the province by `prepare_boundaries.py`).

Outputs go to `data/raw/power/` (raw API responses) and `data/processed/power_daily*.csv`.
Missing values from the API (`-999`) are left empty in the CSV; they are not filled in.

## Building the map

```bash
python src/analysis.py   # season check, monsoon onset, dry-spell/flood risk, tips, back-test -> data/processed/summary.json
python src/build_map.py  # web page -> docs/index.html
```

All thresholds are in `RULES` at the top of `src/analysis.py`. They are starting assumptions, not validated agronomic advice.

### How the rotation options are compared

The options and every assumption behind them (growing windows, water needs, heat limits, benefit scores) are in
`src/rotations.py`. For each province and each past year (2000–2025), `analysis.py` checks whether a rotation
would have worked with that year's NASA POWER weather:

- **Water:** rain in the crop's growing window + water left in the root zone at sowing (POWER `GWETROOT`,
  scaled by soil texture from SoilGrids) must reach the crop's water need.
- **Heat:** fewer than 5 days above the crop's heat limit (POWER `T2M_MAX`).

"Reliability" is the share of years where both held. Dry-season crops are tested for three sowing dates
(rice harvested late Oct, mid Nov or early Dec). On the page, the farmer sets four priorities (better soil,
more income, save water, less work), picks a harvest time and says whether they can irrigate. Each option's
score = how well its benefits match those priorities × its reliability. Every option shows the NASA evidence,
benefits, risks, what is not in the data yet, and a reminder to check with local experts.

How the page is put together:
- `src/build_map.py` makes the base map with Folium, locked to Cambodia, and embeds the province results and shapes in `docs/index.html`.
- `docs/assets/app.js` does everything interactive: coloured province shapes (by status, rain, monsoon onset or dry spell),
  hover cards, the province list (status filters, search, sorting) and the province details
  (key numbers, what to do, and tabs for season, planting, risks and back-test history), in English or Khmer.
- `docs/assets/style.css` holds all the styling. Edit these two files directly, then rerun `build_map.py` so the page picks up the new version.

The Khmer text in `src/build_map.py` (tips) and `docs/assets/app.js` (labels) is a draft and needs checking by a native speaker.

## NASA data and other resources used

| Resource | What we use it for | Link |
|---|---|---|
| NASA POWER daily point API (AG community) | Rainfall (`PRECTOTCORR`), temperature (`T2M`, `T2M_MAX`), root-zone soil wetness (`GWETROOT`), 2000 to today | https://power.larc.nasa.gov/ |
| geoBoundaries gbOpen KHM ADM1 (OpenStreetMap, ODbL 1.0) | Province shapes and the Cambodia outline | https://www.geoboundaries.org/ |
| ISRIC SoilGrids 2.0 (CC-BY 4.0) | Topsoil clay, sand, organic carbon and pH per province (0–30 cm) | https://soilgrids.org/ |
| Folium / Leaflet | Interactive map | https://python-visualization.github.io/folium/ |
| Shapely | Simplifying province shapes, centroids | https://shapely.readthedocs.io/ |
| Esri World Light Gray Canvas | Base map tiles | https://www.arcgis.com/home/item.html?id=8b3d38c0819547faa83f7b7aca80bd76 |
| Noto Sans / Noto Sans Khmer (Google Fonts) | English and Khmer text | https://fonts.google.com/noto/specimen/Noto+Sans+Khmer |

Known limitations:
- POWER data is on a coarse grid (about 0.5°), so each province value is for the grid cell around one point,
  not an average over the whole province. Neighbouring small provinces can share a cell (Phnom Penh and Kandal get the same values).
- In the north-eastern highlands (Mondulkiri, Ratanakiri) the onset rule often finds no clear start date,
  so many past years count as "late". The rule was designed for lowland rain-fed rice.
- Rotation results depend on assumed crop water needs, heat limits and benefit scores (`src/rotations.py`).
  Market prices, irrigation access, pests and field drainage are not in the data. SoilGrids is a 250 m model,
  not a field survey. The tool is meant to support, not replace, farmers' and extension officers' judgment.

## AI use disclosure

Parts of this project's code were generated with AI assistance (Claude Code, by Anthropic) and reviewed by the team.
Generated files say so in their header, and `data/processed/power_metadata*.json` records it too.
No NASA logos or branding are used in AI-generated content.
