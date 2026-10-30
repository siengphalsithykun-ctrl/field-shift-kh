"""Build the bilingual (Khmer/English) Folium map from data/processed/summary.json.

Usage:
    python src/build_map.py    # writes docs/index.html (served by GitHub Pages)

Khmer text is a draft: have a native speaker check it before the pitch.
Partly generated with AI assistance (Claude Code); reviewed by the team.
"""

import json
from datetime import date

import folium

from config import PROCESSED_DIR, ROOT

OUT = ROOT / "docs" / "index.html"

COLORS = {"green": "#2e7d32", "yellow": "#f2a900", "red": "#c62828"}
LEVEL_TEXT = {
    "green": ("Normal", "ធម្មតា"),
    "yellow": ("Watch", "ប្រុងប្រយ័ត្ន"),
    "red": ("Warning", "ព្រមាន"),
}
MONTHS_EN = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
MONTHS_KM = "មករា កុម្ភៈ មីនា មេសា ឧសភា មិថុនា កក្កដា សីហា កញ្ញា តុលា វិច្ឆិកា ធ្នូ".split()

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


def bi(en, km):
    """Text in both languages; the page's language switch shows one of them."""
    return f'<span class="en">{en}</span><span class="km">{km}</span>'


def chip(level):
    en, km = LEVEL_TEXT[level]
    text = "#1d2329" if level == "yellow" else "#fff"
    return f'<span class="chip" style="background:{COLORS[level]};color:{text}">{bi(en, km)}</span>'


def fmt_date(iso):
    if iso is None:
        return bi("not yet", "មិនទាន់")
    d = date.fromisoformat(iso)
    return bi(f"{d.day} {MONTHS_EN[d.month - 1]}", f"{d.day} {MONTHS_KM[d.month - 1]}")


def fmt_month_day(md):
    m, d = (int(x) for x in md.split("-"))
    return bi(f"{d} {MONTHS_EN[m - 1]}", f"{d} {MONTHS_KM[m - 1]}")


def monthly_chart(monthly, level):
    """Small inline SVG: normal monthly rain (grey) vs this year (status colour)."""
    w, h, pad = 300, 96, 14
    top = max(max(m["normal_mm"], m["this_year_mm"] or 0) for m in monthly) or 1
    slot = (w - 4) / 12
    bars = []
    for i, m in enumerate(monthly):
        x = 2 + i * slot
        nh = (h - pad) * m["normal_mm"] / top
        bars.append(f'<rect x="{x + 2:.1f}" y="{h - pad - nh:.1f}" width="{slot / 2 - 2:.1f}" height="{nh:.1f}" fill="#b8bec6"/>')
        if m["this_year_mm"] is not None:
            th = (h - pad) * m["this_year_mm"] / top
            opacity = 0.45 if m["partial"] else 1
            bars.append(
                f'<rect x="{x + slot / 2:.1f}" y="{h - pad - th:.1f}" width="{slot / 2 - 2:.1f}" '
                f'height="{th:.1f}" fill="{COLORS[level]}" opacity="{opacity}"/>'
            )
        bars.append(f'<text x="{x + slot / 2:.1f}" y="{h - 2}" text-anchor="middle">{MONTHS_EN[i][0]}</text>')
    return f'<svg viewBox="0 0 {w} {h}" class="chart" role="img" aria-label="Monthly rainfall">{"".join(bars)}</svg>'


def popup_html(p, year):
    on, sc, ds, fl = p["onset"], p["season_check"], p["dry_spell"], p["flood"]

    if on["delay_days"] is None:
        delay = bi("Onset not confirmed yet", "មិនទាន់បញ្ជាក់ការចាប់ផ្តើមរដូវវស្សា")
    elif on["delay_days"] > 0:
        delay = bi(f"{on['delay_days']} days later than normal", f"យឺតជាងធម្មតា {on['delay_days']} ថ្ងៃ")
    else:
        delay = bi(f"{-on['delay_days']} days earlier than normal", f"លឿនជាងធម្មតា {-on['delay_days']} ថ្ងៃ")

    anomaly = sc["rain_anomaly_pct"]
    late_years = [str(b["year"]) for b in p["backtest"] if b["late_onset"]]
    tips = "".join(f"<li>{bi(*TIPS[t])}</li>" for t in p["tips"])

    return f"""
<div class="popup">
  <div class="head">
    <div><b>{p['name_km']}</b> · {p['name_en']}</div>
    {chip(p['overall'])}
  </div>

  <h4>{bi('1. Season check', '១. ពិនិត្យរដូវ')} {chip(sc['level'])}</h4>
  <p>{bi(f"Rain since 1 May: <b>{sc['season_rain_mm']:.0f} mm</b> (normal {sc['normal_season_rain_mm']:.0f} mm, <b>{anomaly:+.0f}%</b>)",
         f"ទឹកភ្លៀងចាប់ពី ១ ឧសភា៖ <b>{sc['season_rain_mm']:.0f} មម</b> (ធម្មតា {sc['normal_season_rain_mm']:.0f} មម, <b>{anomaly:+.0f}%</b>)")}<br>
  {bi(f"Soil moisture (last 30 days): {sc['soil_moisture_now']:.2f} (normal {sc['soil_moisture_normal']:.2f})",
      f"សំណើមដី (៣០ថ្ងៃចុងក្រោយ)៖ {sc['soil_moisture_now']:.2f} (ធម្មតា {sc['soil_moisture_normal']:.2f})")}</p>
  {monthly_chart(p['monthly'], sc['level'])}
  <div class="legend-row"><span class="sw" style="background:#b8bec6"></span>{bi('Normal 2000–2025', 'ធម្មតា ២០០០–២០២៥')}
    <span class="sw" style="background:{COLORS[sc['level']]}"></span>{year}</div>

  <h4>{bi('2. Planting window', '២. ពេលវេលាដាំសមស្រប')} {chip(on['level'])}</h4>
  <p>{bi('Monsoon onset', 'ការចាប់ផ្តើមរដូវវស្សា')}: <b>{fmt_date(on['date'])}</b>
     ({bi('normal', 'ធម្មតា')} {fmt_month_day(on['normal_date'])}) · {delay}<br>
  {bi('Recommended sowing/transplanting', 'ពេលសាបព្រោះ/ស្ទូងដែលណែនាំ')}: <b>{fmt_date(on['window_start'])} – {fmt_date(on['window_end'])}</b></p>

  <h4>{bi('3. Risk alerts', '៣. ការព្រមានហានិភ័យ')}</h4>
  <p>{chip(ds['level'])} {bi(f"Dry spell: longest {ds['longest_days']} dry days in a row this season",
                              f"រាំងស្ងួត៖ យូរបំផុត {ds['longest_days']} ថ្ងៃជាប់គ្នា ក្នុងរដូវនេះ")}<br>
  {chip(fl['level'])} {bi(f"Flood: heaviest 3-day rain in last 30 days {fl['recent_max_3day_mm']:.0f} mm (alert above {fl['p95_3day_mm']:.0f} mm)",
                           f"ទឹកជំនន់៖ ភ្លៀង៣ថ្ងៃខ្លាំងបំផុត ក្នុង៣០ថ្ងៃចុងក្រោយ {fl['recent_max_3day_mm']:.0f} មម (ព្រមានលើស {fl['p95_3day_mm']:.0f} មម)")}</p>

  <h4>{bi('4. What to do', '៤. អ្វីដែលគួរធ្វើ')}</h4>
  <ul>{tips}</ul>

  <p class="small">{bi(f"Back-test: these rules would have flagged a late monsoon in {', '.join(late_years)}.",
                       f"ការសាកល្បងលើអតីតកាល៖ ច្បាប់ទាំងនេះនឹងព្រមានពីរដូវវស្សាយឺតក្នុងឆ្នាំ {', '.join(late_years)}។")}
  {bi(f"Data up to {p['last_data_date']}.", f"ទិន្នន័យដល់ថ្ងៃ {p['last_data_date']}។")}</p>
</div>"""


PAGE_CSS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Khmer:wght@400;600&display=swap" rel="stylesheet">
<style>
  html, body { font-family: system-ui, -apple-system, "Segoe UI", "Noto Sans Khmer", sans-serif; }
  body:not(.lang-km) .km, body.lang-km .en { display: none; }
  .panel { position: fixed; z-index: 650; /* above markers, below Leaflet pop-ups (700) */ background: #fff; border-radius: 10px;
           box-shadow: 0 2px 10px rgba(0,0,0,.2); padding: 10px 14px; color: #1d2329; }
  .title { top: 12px; left: 56px; max-width: min(420px, calc(100vw - 80px)); }
  .title h1 { font-size: 18px; margin: 0 0 2px; }
  .title p { font-size: 13px; margin: 0; color: #4a5560; }
  .lang { margin-top: 8px; }
  .lang button { border: 1px solid #c9ced4; background: #fff; border-radius: 6px; padding: 3px 10px;
                 cursor: pointer; font: inherit; font-size: 13px; }
  .lang button.on { background: #1d2329; color: #fff; border-color: #1d2329; }
  .legend { bottom: 28px; left: 12px; font-size: 13px; line-height: 1.7; }
  .dot { display: inline-block; width: 12px; height: 12px; border-radius: 50%; margin-right: 6px; vertical-align: -1px; }
  .footer { bottom: 28px; right: 12px; font-size: 11px; max-width: 300px; color: #4a5560; }
  @media (max-width: 600px) { .footer { display: none; } .title { left: 50px; } }
  .popup { font-size: 13px; line-height: 1.45; width: 320px; max-width: 75vw;
           max-height: min(65vh, 480px); overflow-y: auto; padding-right: 4px; }
  .popup .head { display: flex; justify-content: space-between; align-items: center; gap: 8px; font-size: 15px; }
  .popup h4 { margin: 10px 0 3px; font-size: 13px; display: flex; gap: 6px; align-items: center; }
  .popup p { margin: 0; }
  .popup ul { margin: 2px 0; padding-left: 18px; }
  .popup .small { margin-top: 8px; font-size: 11px; color: #5b6670; }
  .chip { border-radius: 10px; padding: 0 8px; font-size: 11px; font-weight: 600; white-space: nowrap; }
  .chart { width: 100%; height: auto; margin-top: 4px; }
  .chart text { font-size: 9px; fill: #5b6670; }
  .legend-row { font-size: 11px; color: #5b6670; }
  .sw { display: inline-block; width: 10px; height: 10px; margin: 0 4px 0 8px; vertical-align: -1px; }
</style>
"""


def page_panels(generated):
    legend = "".join(
        f'<div><span class="dot" style="background:{COLORS[k]}"></span>{bi(*LEVEL_TEXT[k])}</div>' for k in COLORS
    )
    return f"""
<div class="panel title">
  <h1>Field Shift KH</h1>
  <p>{bi('Rice planting guidance from NASA POWER Earth data. Click a province.',
         'ការណែនាំអំពីការដាំស្រូវ ពីទិន្នន័យផែនដី NASA POWER។ ចុចលើខេត្តណាមួយ។')}</p>
  <div class="lang">
    <button id="btn-en" class="on" onclick="setLang('en')">English</button>
    <button id="btn-km" onclick="setLang('km')">ខ្មែរ</button>
  </div>
</div>
<div class="panel legend">{legend}</div>
<div class="panel footer">
  {bi('Data: NASA POWER daily point API (AG), 2000–2026, power.larc.nasa.gov. '
      'Rule-based prototype, not yet validated by agronomists. '
      'Code partly generated with AI (Claude Code).',
      'ទិន្នន័យ៖ NASA POWER (AG) ២០០០–២០២៦, power.larc.nasa.gov។ '
      'គំរូដំបូងផ្អែកលើច្បាប់ មិនទាន់ត្រួតពិនិត្យដោយអ្នកជំនាញកសិកម្ម។ '
      'កូដមួយផ្នែកបង្កើតដោយ AI (Claude Code)។')}
  {bi(f'Built {generated}.', f'បង្កើតថ្ងៃ {generated}។')}
</div>
<script>
  function setLang(l) {{
    document.body.classList.toggle('lang-km', l === 'km');
    document.documentElement.lang = l;
    document.getElementById('btn-en').classList.toggle('on', l === 'en');
    document.getElementById('btn-km').classList.toggle('on', l === 'km');
  }}
  // Hide the title panel while a pop-up is open so it doesn't cover the pop-up.
  window.addEventListener('load', () => {{
    const map = Object.values(window).find(v => v instanceof L.Map);
    const title = document.querySelector('.panel.title');
    map.on('popupopen', () => title.style.display = 'none');
    map.on('popupclose', () => title.style.display = '');
  }});
</script>
"""


def main():
    summary = json.loads((PROCESSED_DIR / "summary.json").read_text(encoding="utf-8"))
    year = summary["current_year"]

    m = folium.Map(location=[12.3, 104.6], zoom_start=7, tiles="OpenStreetMap",control_scale=True)
    m.get_root().header.add_child(folium.Element('<title>Field Shift KH</title>'))
    m.get_root().header.add_child(folium.Element(PAGE_CSS))

    for p in summary["provinces"].values():
        color = COLORS[p["overall"]]
        folium.CircleMarker(
            location=[p["lat"], p["lon"]],
            radius=16,
            color="#fff",
            weight=3,
            fill=True,
            fill_color=color,
            fill_opacity=0.95,
            tooltip=f"{p['name_km']} · {p['name_en']}",
            popup=folium.Popup(popup_html(p, year), max_width=360),
        ).add_to(m)

    m.get_root().html.add_child(folium.Element(page_panels(date.today().isoformat())))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    m.save(OUT)
    print(f"Wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
