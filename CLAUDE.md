# Field Shift KH — Project Context

NASA Space Apps Challenge Cambodia 2026 (Phnom Penh local event, Raintree).
Challenge: **Field Shift: Adapting Farms with NASA Data**.
Team: 5 AUPP students. This file gives Claude Code the full project context.

## Problem
Cambodian smallholder rice farmers face unpredictable rainfall: late monsoon onset, mid-season dry spells and floods (Mekong / Tonle Sap). Most rice is rain-fed and planted by traditional calendars, so when the season shifts, seedlings fail and yields and income drop. Free NASA climate data exists but doesn't reach farmers in a usable form.

## Solution
**Field Shift KH**: a bilingual (Khmer/English) interactive map that turns NASA Earth data into planting guidance for rice farmers and extension officers. Clicking a province shows:
1. **Season check**: this season's rainfall and soil moisture vs. the 20-year normal (anomaly).
2. **Planting window**: recommended period based on detected monsoon onset, not a fixed date.
3. **Risk alerts**: dry-spell and flood risk.
4. **Adaptation tips**: e.g., short-duration rice varieties, delayed transplanting.
Traffic-light colours (green/yellow/red) for non-technical users.

**Scope (keep it realistic):** rule-based logic, not a trained AI model. Rice only. A few pilot provinces.

## Tech stack (beginner-friendly, recommended by organisers)
- Python, Google Colab / Jupyter, Pandas
- Folium for the interactive map, exported as a standalone HTML file
- Hosting: GitHub repo + GitHub Pages (must be a public link, no login)

## Data sources
- **NASA POWER API (core, no login):** daily point data, agriculture community.
  Example: `https://power.larc.nasa.gov/api/temporal/daily/point?parameters=PRECTOTCORR,T2M,T2M_MAX,GWETROOT&community=AG&longitude=104.78&latitude=10.99&start=20000101&end=20251231&format=JSON`
  - PRECTOTCORR = precipitation (mm/day), T2M / T2M_MAX = temperature, GWETROOT = root-zone soil wetness (0–1)
- **GPM IMERG** (rainfall, higher resolution) and **SMAP** (soil moisture): optional layers. They need a free NASA Earthdata login. Pre-download before the event.
- **MODIS NDVI via AppEEARS**: optional crop-health layer. Requests can take hours.

Pilot provinces (approximate centroids, verify):
| Province | Lat | Lon |
|---|---|---|
| Takeo | 10.99 | 104.78 |
| Prey Veng | 11.48 | 105.33 |
| Battambang | 13.10 | 103.20 |
| Kampong Thom | 12.71 | 104.89 |

## Logic (starting assumptions; validate with mentors/agronomic sources)
- **Normal:** 20+ year daily/monthly climatology per province. **Anomaly:** current vs. normal (%).
- **Monsoon onset:** first day after 1 April where 3-day cumulative rain ≥ 20 mm AND no dry spell ≥ 7 days (<1 mm/day) in the next 30 days.
- **Dry-spell risk:** ≥ 10 consecutive days < 1 mm during the wet season.
- **Flood risk:** e.g., 3-day rain or monthly rain far above the normal (set threshold, e.g., > 90th percentile).
- **Back-test:** run on a past drought or late-monsoon year to show the tool would have warned farmers (supports "Validity" in judging).

## Suggested repo structure
```
field-shift-kh/
├── data/raw/            # downloaded NASA data
├── data/processed/
├── src/fetch_power.py   # NASA POWER download
├── src/analysis.py      # normals, anomalies, onset, dry spells, flood risk
├── src/build_map.py     # Folium map + bilingual pop-ups -> docs/index.html
├── notebooks/backtest.ipynb
├── docs/index.html      # GitHub Pages output
└── README.md            # list ALL NASA data + AI tool use
```

## Team roles
- **Sieng Phalsithykun**: backend + datasets (NASA data pipeline)
- **Kim Engsomony**: frontend (Folium map, bilingual UI) + datasets
- **Ouk Sovannreach**: backend (onset, planting window, dry-spell logic)
- **Youn Visal**: backend + app development (integration, testing, GitHub deploy)
- **Hak Sovannpangna**: data handling (cleaning, analysis, back-test), fintech background (income impact for pitch)

## Timeline
- **Before event:** pre-download 20+ yrs of POWER data; build a baseline Folium map. Shortlist announced 1 Nov 2026.
- **Day 1, Sat 14 Nov:** 09:00 welcome, 10:30 mentor briefing, **11:00–18:00 hacking** (lunch 12:30, check-in 16:30). Goal: map showing season status and planting window for the pilot provinces from real data.
- **Day 2, Sun 15 Nov:** **09:15–16:00 hacking** (lunch 12:00), **16:00 pitches**, 18:00 awards. Goal: alerts, tips, Khmer labels, back-test, deploy, demo video, pitch.

## Submission requirements
- Must address a 2026 challenge and use ≥ 1 NASA dataset/resource.
- Working prototype, public project link (no password/login).
- Demo: ≤ 7 slides OR ≤ 30-second video, public link.
- List all NASA data and other resources used, with URLs.
- Disclose AI use: code/data must acknowledge AI generation in text and metadata. AI-generated content must not use NASA logos or branding.
- Deadline: Sun 15 Nov, 11:59 PM local time.
- Judging: Impact, Creativity, Validity, Relevance, Presentation.

## Pitch structure
Problem → solution → live demo → NASA data used → back-test (validity) → impact → next steps (validate with farmers/agronomists, more crops, SMS for basic phones).
