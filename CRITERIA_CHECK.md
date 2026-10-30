# Field Shift KH: criteria check and hackathon plan

Checked on 30 Oct 2026 against the Phnom Penh orientation slides (24.10), the official challenge statement
(https://www.spaceappschallenge.org/2026/challenges/adapting-farms-with-nasa-data/) and the Participant FAQs.
Written with AI assistance (Claude Code).

---

## Update (30 Oct): what has been built since this check

The team reports the Local Lead has cleared pre-event work (keep that in writing and mention it in the submission).
Since then, the main gaps from section 3 are closed in the prototype:

- **≥ 3 rotation strategies incl. the current one:** bare dry season (current), rice → mungbean,
  rice → maize/vegetables, green manure → rice (`src/rotations.py`).
- **NASA evidence per strategy:** each one is tested against every year 2000–2025 with POWER rain, root-zone
  soil wetness and max temperature; the page shows "worked in X of 26 years" plus a year-by-year strip.
- **Local soil information:** ISRIC SoilGrids texture, organic carbon and pH per province (`src/fetch_soil.py`);
  texture changes how much soil water a crop can use, and acidic or low-carbon soils add notes.
- **Farmer priorities and constraints:** sliders (better soil, more income, save water, less work),
  rice harvest timing, and an irrigation switch re-rank the options live; the map can colour provinces by best option.
- **Why / evidence / benefits / gaps / risks** on every option, plus a reminder to check with local experts.
- **Bare-field months** shown for the current rotation.
- **AI metadata:** `<meta name="ai-disclosure">` added to `docs/index.html`.

Still open: demo slides or video, submission text, mentor check of the crop assumptions, optional second NASA dataset
(SMAP or MODIS NDVI) and a POWER vs GPM validation.

---

## 1. Rule risk: read this first

The official site and FAQ both say:

> "Teams are not allowed to begin working on the challenges prior to the hackathon."

Everything in this repo (data pipeline, analysis, map) was built before the event (commits from 30 Oct),
and the repo is public. Judges or organisers could see this as pre-event work on the challenge.

**What to do (team decision):**
1. **Ask the Local Lead (Voneat Pen, penvoneat@gmail.com) before 14 Nov** what preparation is allowed:
   pre-downloading NASA data? a starter map template? The orientation slides encourage practising a
   baseline map before the event, but with NASA FIRMS (a different dataset and topic), not on the challenge itself.
2. Until you get an answer, **stop adding challenge features.** Learning the tools and reading NASA data docs is fine.
3. Safest path if the answer is "no pre-work": treat this repo as **practice**. On 14 Nov, start a fresh repo and
   rebuild during the event, reusing only what the Local Lead allows (for example the download script as a generic tool).
   Making this repo private until then is also worth considering.
4. Whatever you reuse, say so openly in the submission's "Project Details".

---

## 2. Submission checklist (slide 28 + submission form)

| Requirement | Status now | Notes |
|---|---|---|
| Team registered for the same local event (Phnom Penh), all members on the Members tab | ❓ Check | Shortlist deadline was 28 Oct; teams announced 1 Nov |
| Project addresses a 2026 challenge | ⚠️ Partly | Statement is about **crop-rotation strategies**, see section 3 |
| At least one NASA dataset or resource used | ✅ | NASA POWER (listed in the challenge text) |
| Working prototype / demonstrable output | ✅ (pre-event) | Live map on GitHub Pages; see rule risk |
| Project link: public, no password/login/permission | ✅ | GitHub Pages + public repo |
| Demo: ≤ 7 slides (title + intro count) **or** ≤ 30 s video, public link, no login | ❌ To do | Needed for Global Awards; outline in section 6 |
| Summary (50–200 words) | ❌ To do | Draft in section 7 |
| Project Details (what/how, benefits, impact, tools, creativity, factors considered) | ❌ To do | Outline in section 7 |
| Use of AI: list how AI was used | ⚠️ Partly | Code headers, README, metadata JSON and page footer say so; write the form text (section 7) |
| AI content must not use or modify NASA logos, flags or mission identifiers | ✅ | None used; keep it that way in slides/video |
| AI images/videos carry a **visible watermark** saying AI-generated | — | Applies if the demo video or slide images are AI-made |
| Code and data acknowledge AI in **text and metadata** | ⚠️ Partly | Add a `<meta>` AI-disclosure tag to `docs/index.html` |
| NASA Data list (name + full URL) | ✅ Draft | Section 7 |
| Space Agency Partner & Other Data list (incl. open-source code, fonts, tiles) | ✅ Draft | Section 7 |
| Submit before **Sun 15 Nov, 11:59 PM** Phnom Penh time; press "Submit for Judging" | ❌ | Saving ≠ submitting. No edits after the deadline |

---

## 3. Fit with the challenge statement (Relevance)

The statement asks for a decision-support tool that combines NASA Earth observations with **local soil information,
crop characteristics and farmer priorities**, so farmers can **explore crop-rotation strategies** that improve
soil health and adapt to changing conditions. It suggests comparing **at least three rotations, including the
current one**, and for each explaining *why it was suggested, the evidence, the benefits, information gaps,
and risks that need local review*.

| Challenge asks for | What we have | Gap |
|---|---|---|
| NASA Earth observations (POWER, SMAP, GPM, MODIS, Landsat, ECOSTRESS, GRACE, SRTM…) | NASA POWER rain, temperature, root-zone soil wetness, 2000–2026 | Add 1–2 more (SMAP soil moisture, MODIS NDVI or GPM) to strengthen "Best Use of Data" |
| Seasons when current crops are vulnerable | Monsoon onset, dry-spell and flood alerts for wet-season rice | ✅ Strong; keep as the "current rotation" view |
| Times when fields are typically bare | Not shown | Dry season after rice harvest (≈ Dec–Apr) is the obvious bare period |
| **Compare ≥ 3 rotation strategies incl. the existing one** | ❌ | Core missing piece: see section 5 |
| Local soil information | ❌ | e.g. ISRIC SoilGrids (texture, organic carbon, pH) per province |
| Crop characteristics (water use, duration, N-fixing, heat tolerance) | ❌ | Small crop table, checked with mentors |
| Farmer priorities / constraints (water, income, soil, labour) | ❌ | Sliders or toggles that re-rank strategies |
| Explain why / evidence / benefits / gaps / risks per strategy | ❌ | One card per strategy |
| Supports, does not replace, farmer judgment | ✅ | Disclaimer is on the page; repeat it per strategy |
| Farmer-friendly (limited technical skills) | ✅ | Khmer/English, traffic lights, plain language |
| Explain terms (soil-moisture anomaly, evapotranspiration, NDVI) | ⚠️ | Add short "What does this mean?" tooltips |

---

## 4. Judging criteria and awards

Local and global judging use **Impact, Creativity, Validity, Relevance, Presentation**.

| Criterion | Where we stand | What would raise it |
|---|---|---|
| **Relevance** | Weakest: we answer "when to plant rice", not "which rotation" | Add the rotation comparison (section 5) |
| **Validity** | Good: transparent rules, 26-year back-test, 2015–16 flagged as late-monsoon years | Compare one province's POWER rain with GPM IMERG or a published source; show uncertainty and limitations on the page |
| **Impact** | Good story (rain-fed rice, smallholders, Khmer UI) | Income angle from Sovannpangna: what a dry-season mungbean crop or an avoided failed transplanting is worth per hectare |
| **Creativity** | Map-to-advice link, bilingual, back-test view | Priority sliders that re-rank rotations live; "what if the monsoon is 3 weeks late" scenario |
| **Presentation** | Clean UI; no deck/video yet | 7-slide deck or 30 s video with live demo screenshots (section 6) |

Awards that fit best: **Local Impact**, **Best Use of Data**, **Galactic Impact**, **Best Use of Storytelling**.

---

## 5. Plan for the two days (only once the hackathon starts)

**Goal:** turn the planting-alert map into a rotation explorer for Cambodian rice farms.

Rotations to compare per province. These are starting ideas: confirm crops, durations and claims with mentors.
1. **Current: wet-season rice → bare dry season** (baseline, uses the existing alerts)
2. **Rice → mungbean** (short legume after harvest; fixes nitrogen; uses leftover soil moisture)
3. **Rice → maize or vegetables** (income; needs more water or irrigation)
4. **Rice + green manure / cover crop** (e.g. sesbania; organic matter, less erosion; no direct income)

NASA indicators per province (POWER already gives most of these):
- Residual root-zone moisture after harvest (GWETROOT, Nov–Jan) → can a second crop establish?
- Dry-season rain and its variability (PRECTOTCORR, Dec–Apr) → water risk for each crop
- Heat-stress days (T2M_MAX above a crop's limit, Mar–May) → risk for flowering
- Optional: SMAP soil moisture to cross-check GWETROOT; MODIS NDVI to show bare-field months

Scoring: for each rotation, rule-based scores for *water need vs available*, *heat risk*, *soil benefit*, *income potential*;
farmer priority sliders (save water / more income / better soil / less labour) weight the scores.
Each rotation card shows: why suggested · NASA evidence · benefits · information gaps · risks needing local review.

| Who | Day 1 (Sat 14 Nov, 11:00–18:00) | Day 2 (Sun 15 Nov, 09:15–16:00) |
|---|---|---|
| Sieng Phalsithykun (data) | Dry-season indicators from POWER; optional SMAP/MODIS | Validation: POWER vs GPM for 1–2 provinces |
| Ouk Sovannreach (logic) | Crop table + rotation scoring rules (with mentor at 10:30) | Tune thresholds; edge cases |
| Kim Engsomony (frontend) | Rotation comparison cards + priority sliders | Khmer labels, term explanations, polish |
| Youn Visal (integration) | Wire scores into page; deploy on Pages | Testing on phones; final deploy; submission form |
| Hak Sovannpangna (analysis) | Back-test summary for the pitch | Income impact numbers; demo video or slides |

Check-in at 16:30 on Day 1: map shows rotation scores for all provinces from real data.
Day 2 by 14:00: feature freeze; 14:00–16:00 demo, slides and the submission form. Submit well before 11:59 PM.

---

## 6. Demo outline (≤ 7 slides including title and intro)

1. Title: Field Shift KH (team, challenge name). No NASA logo.
2. Problem: rain-fed rice, shifting monsoon, bare dry-season fields, soil decline.
3. Solution: map → province → planting alerts + rotation options ranked by your priorities.
4. Live demo screenshots: one province, priorities changed, rotation ranking changes.
5. NASA data + validity: POWER (+ SMAP/GPM), 26-year back-test, limitations.
6. Impact: farmers and extension officers, income example, Khmer-first design.
7. Next steps: validate with farmers and agronomists, SMS for basic phones, field-level data.

If you make a video instead: ≤ 30 s, and add a visible "AI-generated" watermark if any part is AI-made.

---

## 7. Draft submission text (update after the hackathon)

**Project name:** Field Shift KH

**Summary (draft, ~120 words; finish once the rotation feature exists):**
Field Shift KH is a bilingual (Khmer/English) decision-support map that helps Cambodian rice farmers and extension
officers adapt to shifting rainfall. For every province it turns 26 years of NASA POWER data into a season check
(rain and soil moisture vs normal), a planting window based on the detected monsoon onset, and dry-spell and flood
alerts. It then compares crop-rotation options for the dry season, from leaving fields bare to growing mungbean,
maize or a green-manure cover crop, ranked by the farmer's own priorities: saving water, earning income or building
soil health. Each option explains the NASA evidence, benefits, gaps and risks. A back-test shows the rules would have
flagged the 2015–16 late monsoon. The tool supports, not replaces, local expertise.

**Project details (outline):** what it does and how · benefits and intended impact · tools (Python, pandas, Folium/Leaflet,
Shapely, JavaScript, GitHub Pages) · what makes it creative · factors considered (grid resolution, rule thresholds,
Khmer wording, offline/low-bandwidth use) · what was prepared before the event, if anything (be open about it).

**Use of AI (draft):** Claude Code (Anthropic) was used to help write and debug the Python data pipeline, analysis
rules and the web page code, and to draft documentation. All AI-assisted files say so in their header and in the
page footer and data metadata. The team reviewed and tested all code and chose the rules and thresholds.
No NASA branding was generated or modified by AI. [Add any AI images/video here, with watermark.]

**NASA Data:**
- NASA POWER (Prediction Of Worldwide Energy Resources) daily API, Agroclimatology community: https://power.larc.nasa.gov/
- [Add if used] SMAP soil moisture: https://smap.jpl.nasa.gov/
- [Add if used] GPM IMERG precipitation: https://gpm.nasa.gov/data/imerg
- [Add if used] MODIS vegetation indices: https://modis.gsfc.nasa.gov/data/dataprod/mod13.php

**Space Agency Partner & Other Data / resources:**
- geoBoundaries gbOpen KHM ADM1 (OpenStreetMap, ODbL 1.0): https://www.geoboundaries.org/
- Esri World Light Gray Canvas base map: https://www.arcgis.com/home/item.html?id=8b3d38c0819547faa83f7b7aca80bd76
- Folium: https://python-visualization.github.io/folium/ · Leaflet: https://leafletjs.com/
- pandas: https://pandas.pydata.org/ · Shapely: https://shapely.readthedocs.io/ · requests: https://requests.readthedocs.io/
- Noto Sans / Noto Sans Khmer (Google Fonts): https://fonts.google.com/noto/specimen/Noto+Sans+Khmer
- [Add if used] ISRIC SoilGrids: https://soilgrids.org/
