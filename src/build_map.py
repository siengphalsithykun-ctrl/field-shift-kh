"""Build the Field Shift KH web page (docs/index.html) from data/processed/summary.json.

Usage:
    python src/build_map.py    # writes docs/index.html (served by GitHub Pages)

The page has two parts:
  - the base map, built here with Folium and locked to Cambodia
  - everything interactive (coloured province shapes, map controls, side panel), drawn in the
    browser by docs/assets/app.js and styled by docs/assets/style.css, from the province results
    and shapes (data/processed/provinces.geojson) embedded in the page

Khmer text (here and in app.js) is a draft: have a native speaker check it before the pitch.
Partly generated with AI assistance (Claude Code); reviewed by the team.
"""

import hashlib
import json

import folium

from config import PROCESSED_DIR, ROOT
from rotations import HARVEST_LABELS, PRIORITIES, ROTATIONS

DOCS = ROOT / "docs"
OUT = DOCS / "index.html"
ASSETS = ["assets/style.css", "assets/app.js"]
REPO_URL = "https://github.com/siengphalsithykun-ctrl/field-shift-kh"

# Light grey base map without labels, so the coloured provinces stand out (free, no API key).
TILES = "https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}"
TILES_ATTR = "&copy; Esri | Boundaries: geoBoundaries (OSM, ODbL)"
SHAPES = PROCESSED_DIR / "provinces.geojson"
BOUNDS_PAD_DEG = 0.6  # how far past Cambodia's edge the map may be panned

TIPS = {
    "delay_transplanting": (
        "Delay transplanting until rains are steady; keep seedlings in the nursery longer.",
        "ពន្យារពេលស្ទូង រហូតដល់មានភ្លៀងធ្លាក់ទៀងទាត់ ហើយទុកកូនស្រូវក្នុងថ្នាលបន្តិចទៀត។",
    ),
    "short_duration_variety": (
        "Choose a short-duration rice variety so the crop finishes before the rains end.",
        "ជ្រើសរើសពូជស្រូវរយៈពេលខ្លី ដើម្បីឱ្យស្រូវទុំមុនរដូវភ្លៀងចប់។",
    ),
    "save_water": (
        "Store water in ponds or canals and irrigate during dry spells if you can.",
        "ស្តុកទឹកក្នុងស្រះ ឬប្រឡាយ ហើយស្រោចស្រពនៅពេលរាំងស្ងួត បើអាចធ្វើបាន។",
    ),
    "drainage": (
        "Clear field drains and check bunds before heavy rain.",
        "សម្អាតប្រឡាយបង្ហូរទឹក និងពិនិត្យភ្លឺស្រែ មុនពេលភ្លៀងខ្លាំង។",
    ),
    "raise_seedbed": (
        "Keep seedbeds on higher ground to protect them from flooding.",
        "រៀបចំថ្នាលសំណាបនៅលើដីខ្ពស់ ដើម្បីការពារពីទឹកជំនន់។",
    ),
    "normal_calendar": (
        "Conditions are close to normal: follow your usual planting calendar.",
        "លក្ខខណ្ឌជិតធម្មតា៖ អនុវត្តតាមប្រតិទិនដាំដុះធម្មតារបស់អ្នក។",
    ),
}

HEAD = """
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Planting alerts and crop-rotation options for Cambodian rice farmers from NASA Earth data (Khmer/English).">
<meta name="generator" content="Python, Folium; code partly generated with AI assistance (Claude Code, Anthropic)">
<meta name="ai-disclosure" content="Code and data processing partly generated with AI assistance (Claude Code) and reviewed by the team. No AI-generated images, audio or video. No NASA branding used.">
<title>Field Shift KH</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;500;600;700&family=Noto+Sans+Khmer:wght@400;500;600;700&display=swap" rel="stylesheet">
"""


def asset_version():
    """Short hash of the CSS/JS so browsers fetch the new files after a change."""
    h = hashlib.sha1()
    for path in ASSETS:
        h.update((DOCS / path).read_bytes())
    return h.hexdigest()[:8]


def country_bounds(shapes):
    """[[south, west], [north, east]] of the Cambodia outline."""
    outline = next(f for f in shapes["features"] if f["properties"]["slug"] == "_cambodia")
    lons = [x for x, _ in outline["geometry"]["coordinates"][0]]
    lats = [y for _, y in outline["geometry"]["coordinates"][0]]
    return [[min(lats), min(lons)], [max(lats), max(lons)]]


def rotation_for_page(r):
    """A rotation's text (as {"en", "km"}) and benefit scores, for app.js."""
    text = {k: {"en": r[k][0], "km": r[k][1]} for k in ("name", "label", "short", "pros", "cons", "gaps")}
    return {"id": r["id"], "current": r["current"], "benefits": r["benefits"], **text}


def page_data(summary, shapes):
    provinces = list(summary["provinces"].values())
    return {
        "currentYear": summary["current_year"],
        "lastDataDate": min(p["last_data_date"] for p in provinces),
        "rules": summary["rules"],
        "tips": {k: {"en": en, "km": km} for k, (en, km) in TIPS.items()},
        "rotations": [rotation_for_page(r) for r in ROTATIONS],
        "priorities": {k: {"en": en, "km": km} for k, (en, km) in PRIORITIES.items()},
        "harvests": {k: {"en": en, "km": km} for k, (en, km) in HARVEST_LABELS.items()},
        "bounds": country_bounds(shapes),
        "repoUrl": REPO_URL,
        "provinces": provinces,
        "shapes": shapes,
    }


def main():
    summary = json.loads((PROCESSED_DIR / "summary.json").read_text(encoding="utf-8"))
    shapes = json.loads(SHAPES.read_text(encoding="utf-8"))
    (south, west), (north, east) = country_bounds(shapes)

    # Locked to Cambodia: can't pan far past the border or zoom out to the region.
    m = folium.Map(
        tiles=None,
        control_scale=True,
        zoom_snap=0.25,
        min_zoom=6,
        max_zoom=11,
        max_bounds=True,
        min_lat=south - BOUNDS_PAD_DEG,
        max_lat=north + BOUNDS_PAD_DEG,
        min_lon=west - BOUNDS_PAD_DEG,
        max_lon=east + BOUNDS_PAD_DEG,
    )
    folium.TileLayer(TILES, attr=TILES_ATTR, name="Base map", max_zoom=16).add_to(m)
    m.fit_bounds([[south, west], [north, east]])

    version = asset_version()
    root = m.get_root()
    root.header.add_child(folium.Element(HEAD))
    # In the body, not the head: Folium puts Bootstrap's CSS at the end of the head, and ours must load after it.
    root.html.add_child(folium.Element(f'<link rel="stylesheet" href="assets/style.css?v={version}">'))
    # Escape "</" so the JSON can't close the <script> tag early.
    data_json = json.dumps(page_data(summary, shapes), ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    root.html.add_child(folium.Element('<aside id="panel" class="panel"></aside>'))
    root.html.add_child(folium.Element(f"<script>window.FIELD_SHIFT = {data_json};</script>"))
    # defer: runs after the whole page (including Folium's map script) has been parsed.
    root.header.add_child(folium.Element(f'<script src="assets/app.js?v={version}" defer></script>'))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    m.save(OUT)
    print(f"Wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
