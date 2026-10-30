"""Prepare Cambodia province shapes for the web map.

Usage:
    python src/prepare_boundaries.py

Reads the geoBoundaries ADM1 file in data/raw/boundaries/ and writes
data/processed/provinces.geojson: one simplified shape per province (with its slug) plus the
country outline used to fade out neighbouring countries. It also prints, for each province,
the point used for the NASA POWER request (the shape's centroid, or a point inside the shape
when the centroid falls outside) so config.py can be checked against it.

Boundaries: geoBoundaries gbOpen KHM ADM1 (OpenStreetMap, ODbL 1.0), https://www.geoboundaries.org/
Partly generated with AI assistance (Claude Code); reviewed by the team.
"""

import json

from shapely.geometry import mapping, shape
from shapely.ops import unary_union

from config import PROCESSED_DIR, PROVINCES, ROOT

RAW = ROOT / "data" / "raw" / "boundaries" / "geoBoundaries-KHM-ADM1_simplified.geojson"
OUT = PROCESSED_DIR / "provinces.geojson"
SIMPLIFY_DEG = 0.004  # about 400 m: plenty for a country-level map, keeps the page small

# geoBoundaries spelling -> our slug, where it isn't just the English name.
NAME_FIXES = {"Bantey Meanchey": "banteay_meanchey", "Ratanakiri Province": "ratanakiri"}


def slug_for(name):
    return NAME_FIXES.get(name, name.lower().replace(" ", "_"))


def rounded(geom, digits=4):
    """Round coordinates to ~10 m to cut the file size."""

    def walk(c):
        return [walk(x) for x in c] if isinstance(c[0], (list, tuple)) else [round(v, digits) for v in c]

    g = mapping(geom)
    return {"type": g["type"], "coordinates": walk(g["coordinates"])}


def main():
    raw = json.loads(RAW.read_text(encoding="utf-8"))
    by_slug = {slug_for(f["properties"]["shapeName"]): shape(f["geometry"]) for f in raw["features"]}

    known = {p["slug"] for p in PROVINCES}
    missing, extra = known - by_slug.keys(), by_slug.keys() - known
    if missing or extra:
        raise SystemExit(f"Names don't match config.py. Missing shapes: {missing}; unknown shapes: {extra}")

    features = []
    print(f"{'province':18} {'lat':>6} {'lon':>7}  config point inside shape?")
    for p in PROVINCES:
        geom = by_slug[p["slug"]].buffer(0)
        point = geom.centroid if geom.contains(geom.centroid) else geom.representative_point()
        inside = geom.contains(shape({"type": "Point", "coordinates": [p["lon"], p["lat"]]}))
        print(f"{p['slug']:18} {point.y:6.2f} {point.x:7.2f}  {'yes' if inside else 'NO'}")
        features.append(
            {
                "type": "Feature",
                "properties": {"slug": p["slug"]},
                "geometry": rounded(geom.simplify(SIMPLIFY_DEG, preserve_topology=True)),
            }
        )

    outline = unary_union(list(by_slug.values())).buffer(0)
    # Keep only the outer edge (drop tiny holes) for the mask around the country.
    polys = getattr(outline, "geoms", [outline])
    outline_rings = [[round(x, 4), round(y, 4)] for x, y in max(polys, key=lambda g: g.area).exterior.coords]
    features.append(
        {
            "type": "Feature",
            "properties": {"slug": "_cambodia"},
            "geometry": rounded(
                shape({"type": "Polygon", "coordinates": [outline_rings]}).simplify(SIMPLIFY_DEG)
            ),
        }
    )

    OUT.write_text(json.dumps({"type": "FeatureCollection", "features": features}), encoding="utf-8")
    print(f"\nWrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
