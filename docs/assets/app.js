/* Field Shift KH: interactive province map and side panel.
   Data (province results + shapes) comes from window.FIELD_SHIFT, embedded in index.html by src/build_map.py.
   The base map itself is made by Folium; this file draws the provinces, the map controls and the panel.
   Khmer text is a draft: have a native speaker check it.
   Partly generated with AI assistance (Claude Code); reviewed by the team. */
(function () {
  "use strict";

  const DATA = window.FIELD_SHIFT;

  // ---------------------------------------------------------------- text
  const T = {
    en: {
      tagline: "Rice planting guidance from NASA Earth data",
      seasonLine: "Wet season {year} · data up to {date}",
      green: "Normal",
      yellow: "Watch",
      red: "Warning",
      search: "Search {n} provinces",
      provincesCount: "{n} provinces",
      noMatch: "No province matches your search.",
      sortRisk: "Most at risk",
      sortName: "A–Z",
      sortBy: "Sort",
      clearFilter: "Show all",
      back: "All provinces",
      prev: "Previous province",
      next: "Next province",
      colourBy: "Colour map by",
      mStatus: "Status",
      mRain: "Rain",
      mOnset: "Monsoon",
      mDry: "Dry spell",
      legendRain: "Rain since 1 May vs normal",
      legendOnset: "Monsoon onset vs normal",
      legendDry: "Longest dry spell this season",
      legendStatus: "Overall status",
      onTime: "On time",
      notYet: "Not confirmed",
      daysLate: "{n} days late",
      daysEarly: "{n} days early",
      daysLateShort: "{n}d late",
      daysUnit: "{n} days",
      seasonCheck: "Season",
      planting: "Planting",
      risks: "Risks",
      history: "History",
      kpiRain: "Rain vs normal",
      kpiOnset: "Monsoon onset",
      kpiDry: "Longest dry spell",
      whatToDo: "What to do",
      rainSince: "Rain since 1 May",
      vsNormal: "{mm} mm · normal {normal} mm",
      soil: "Soil moisture",
      soilSub: "Root zone, last 30 days · normal {normal}%",
      monthlyRain: "Rain per month (mm)",
      normalYears: "Normal 2000–2025",
      monthReadout: "<b>{month}</b>: {year} {mm} mm · normal {normal} mm",
      monthPartial: " (month not finished)",
      notYetMonth: "<b>{month}</b>: normal {normal} mm",
      onset: "Monsoon onset {year}",
      normalOnset: "Normal",
      windowText: "Sow or transplant between <b>{a}</b> and <b>{b}</b>.",
      windowWait: "Wait for steady rain before sowing: the monsoon onset is not confirmed yet.",
      onsetRule: "Onset = first day from 1 April with at least 20 mm of rain in 3 days and no 7-day dry spell in the next 30 days.",
      drySpell: "Dry spell",
      drySpellText: "Longest run of dry days (under 1 mm) this season: <b>{n} days</b>.",
      flood: "Heavy rain / flood",
      floodText: "Heaviest 3-day rain in the last 30 days: <b>{n} mm</b>.",
      historyText: "Each square is a past year. Red years are when these same rules would have warned of a late monsoon.",
      lateYear: "Late monsoon",
      dryYear: "Dry spell 10+ days",
      yearHint: "Tap or hover a year to see it.",
      yearReadout: "<b>{year}</b>: onset {onset} ({delay}) · longest dry spell {dry} days · {rain} mm rain May–Oct",
      issueLate: "Monsoon started late",
      issueNoOnset: "Monsoon onset not confirmed",
      issueDry: "Less rain than normal",
      issueWet: "More rain than normal",
      issueDrySpell: "Dry-spell risk",
      issueFlood: "Heavy-rain risk",
      issueNone: "Conditions close to normal",
      about: "Made by AUPP students for NASA Space Apps Challenge Cambodia 2026 with NASA POWER daily data (2000–2026). Simple rules, not yet checked by agronomists: use together with advice from your local extension officer. Province values come from one ~50 km grid cell. Code partly generated with AI (Claude Code).",
      source: "Data: NASA POWER",
      code: "Source code",
      moreTips: "{n} more",
      mRotation: "Best rotation",
      legendRotation: "Best rotation for your priorities",
      rotations: "Rotations",
      rotIntro: "What should the field do after the rice? Set what matters to you and the options re-rank.",
      yourPriorities: "What matters to you?",
      prioLevels: "Not important|A little|Important|Very important",
      harvest: "When do you harvest your rice?",
      irrigation: "I have water to irrigate (pond, canal or pump)",
      bestMatch: "Best match",
      matchScore: "{n}% match",
      worked: "Would have worked in <b>{ok} of {n}</b> past years ({mode})",
      rainfed: "rain only",
      irrigatedMode: "with irrigation",
      yrOk: "Worked",
      yrDry: "Too dry",
      yrHot: "Too hot",
      evidence: "NASA evidence",
      evSowing: "Sown around {date}, about {days} days in the field.",
      evRain: "Rain while growing: <b>{mm} mm</b> on average; the crop needs about {need} mm.",
      evSoil: "Water left in the soil at sowing: about <b>{mm} mm</b> ({texture} soil).",
      evHeat: "Days hotter than {c}°C: <b>{d}</b> on average.",
      evBare: "Fields here are usually bare in <b>{months}</b> (under 50 mm of rain a month).",
      noBare: "No month here is normally under 50 mm of rain.",
      pros: "Benefits",
      cons: "Risks",
      gaps: "Not in the data yet",
      localSoil: "Local soil (SoilGrids, top 30 cm)",
      soilLine: "{texture} · clay {clay}% · sand {sand}% · organic carbon {soc} g/kg · pH {ph}",
      sandy: "Sandy",
      loamy: "Loamy",
      clayey: "Clayey",
      acidNote: "Acidic soil (pH under 5.5): legumes such as mungbean may need lime. Ask your extension officer.",
      lowCarbonNote: "Low organic carbon: green manure or keeping crop residues would help most.",
      soilMissing: "No soil data for this province yet: loamy soil assumed.",
      reviewNote: "These are options to explore, not instructions. Talk them through with other farmers and your agricultural extension officer before changing what you grow.",
      assumptions: "Crop water needs, heat limits and benefit scores are assumptions to check with agronomists.",
      currentTag: "Now",
    },
    km: {
      tagline: "ការណែនាំដាំស្រូវ ពីទិន្នន័យផែនដីរបស់ NASA",
      seasonLine: "រដូវវស្សា {year} · ទិន្នន័យដល់ {date}",
      green: "ធម្មតា",
      yellow: "ប្រុងប្រយ័ត្ន",
      red: "ព្រមាន",
      search: "ស្វែងរកខេត្ត ({n})",
      provincesCount: "{n} ខេត្ត",
      noMatch: "រកមិនឃើញខេត្តដែលត្រូវនឹងការស្វែងរក។",
      sortRisk: "ហានិភ័យខ្ពស់មុន",
      sortName: "តាមឈ្មោះ",
      sortBy: "តម្រៀប",
      clearFilter: "បង្ហាញទាំងអស់",
      back: "ខេត្តទាំងអស់",
      prev: "ខេត្តមុន",
      next: "ខេត្តបន្ទាប់",
      colourBy: "ពណ៌ផែនទីតាម",
      mStatus: "ស្ថានភាព",
      mRain: "ទឹកភ្លៀង",
      mOnset: "រដូវវស្សា",
      mDry: "រាំងស្ងួត",
      legendRain: "ទឹកភ្លៀងចាប់ពី 1 ឧសភា ធៀបនឹងធម្មតា",
      legendOnset: "ការចាប់ផ្តើមរដូវវស្សា ធៀបនឹងធម្មតា",
      legendDry: "រាំងស្ងួតយូរបំផុតក្នុងរដូវនេះ",
      legendStatus: "ស្ថានភាពទូទៅ",
      onTime: "ទាន់ពេល",
      notYet: "មិនទាន់បញ្ជាក់",
      daysLate: "យឺត {n} ថ្ងៃ",
      daysEarly: "លឿន {n} ថ្ងៃ",
      daysLateShort: "យឺត {n}ថ្ងៃ",
      daysUnit: "{n} ថ្ងៃ",
      seasonCheck: "រដូវ",
      planting: "ការដាំ",
      risks: "ហានិភ័យ",
      history: "ប្រវត្តិ",
      kpiRain: "ភ្លៀងធៀបធម្មតា",
      kpiOnset: "រដូវវស្សាចាប់ផ្តើម",
      kpiDry: "រាំងស្ងួតយូរបំផុត",
      whatToDo: "អ្វីដែលគួរធ្វើ",
      rainSince: "ទឹកភ្លៀងចាប់ពី 1 ឧសភា",
      vsNormal: "{mm} មម · ធម្មតា {normal} មម",
      soil: "សំណើមដី",
      soilSub: "តំបន់ឫស 30 ថ្ងៃចុងក្រោយ · ធម្មតា {normal}%",
      monthlyRain: "ទឹកភ្លៀងប្រចាំខែ (មម)",
      normalYears: "ធម្មតា 2000–2025",
      monthReadout: "<b>{month}</b>៖ {year} {mm} មម · ធម្មតា {normal} មម",
      monthPartial: " (ខែមិនទាន់ចប់)",
      notYetMonth: "<b>{month}</b>៖ ធម្មតា {normal} មម",
      onset: "ការចាប់ផ្តើមរដូវវស្សា {year}",
      normalOnset: "ធម្មតា",
      windowText: "គួរសាបព្រោះ ឬស្ទូង ចន្លោះ <b>{a}</b> ដល់ <b>{b}</b>។",
      windowWait: "រង់ចាំភ្លៀងធ្លាក់ទៀងទាត់សិន មុនសាបព្រោះ៖ មិនទាន់បញ្ជាក់ការចាប់ផ្តើមរដូវវស្សា។",
      onsetRule: "ការចាប់ផ្តើម = ថ្ងៃដំបូងចាប់ពី 1 មេសា ដែលមានភ្លៀងយ៉ាងតិច 20 មម ក្នុង 3 ថ្ងៃ ហើយគ្មានរាំងស្ងួត 7 ថ្ងៃ ក្នុង 30 ថ្ងៃបន្ទាប់។",
      drySpell: "រាំងស្ងួត",
      drySpellText: "រាំងស្ងួតយូរបំផុត (ភ្លៀងក្រោម 1 មម) ក្នុងរដូវនេះ៖ <b>{n} ថ្ងៃ</b>។",
      flood: "ភ្លៀងខ្លាំង / ទឹកជំនន់",
      floodText: "ភ្លៀង 3 ថ្ងៃខ្លាំងបំផុត ក្នុង 30 ថ្ងៃចុងក្រោយ៖ <b>{n} មម</b>។",
      historyText: "ការេនីមួយៗជាឆ្នាំមុនៗ។ ឆ្នាំពណ៌ក្រហម គឺជាឆ្នាំដែលច្បាប់ដដែលនេះនឹងព្រមានពីរដូវវស្សាយឺត។",
      lateYear: "រដូវវស្សាយឺត",
      dryYear: "រាំងស្ងួត 10+ ថ្ងៃ",
      yearHint: "ចុច ឬដាក់កណ្ដុរលើឆ្នាំ ដើម្បីមើល។",
      yearReadout: "<b>{year}</b>៖ ចាប់ផ្តើម {onset} ({delay}) · រាំងស្ងួតយូរបំផុត {dry} ថ្ងៃ · ភ្លៀង {rain} មម ខែឧសភា–តុលា",
      issueLate: "រដូវវស្សាចាប់ផ្តើមយឺត",
      issueNoOnset: "មិនទាន់បញ្ជាក់ការចាប់ផ្តើមរដូវវស្សា",
      issueDry: "ភ្លៀងតិចជាងធម្មតា",
      issueWet: "ភ្លៀងច្រើនជាងធម្មតា",
      issueDrySpell: "ហានិភ័យរាំងស្ងួត",
      issueFlood: "ហានិភ័យភ្លៀងខ្លាំង",
      issueNone: "លក្ខខណ្ឌជិតធម្មតា",
      about: "បង្កើតដោយនិស្សិត AUPP សម្រាប់ NASA Space Apps Challenge Cambodia 2026 ដោយប្រើទិន្នន័យប្រចាំថ្ងៃ NASA POWER (2000–2026)។ ច្បាប់សាមញ្ញ មិនទាន់ត្រួតពិនិត្យដោយអ្នកជំនាញកសិកម្ម៖ សូមប្រើរួមជាមួយដំបូន្មានពីមន្ត្រីផ្សព្វផ្សាយកសិកម្មក្នុងតំបន់។ តម្លៃខេត្តនីមួយៗបានមកពីក្រឡាក្រឡាចត្រង្គប្រហែល 50 គម។ កូដមួយផ្នែកបង្កើតដោយ AI (Claude Code)។",
      source: "ទិន្នន័យ៖ NASA POWER",
      code: "កូដប្រភព",
      moreTips: "{n} ទៀត",
      mRotation: "ការដាំបង្វិល",
      legendRotation: "ការដាំបង្វិលល្អបំផុតតាមអាទិភាពរបស់អ្នក",
      rotations: "ការដាំបង្វិល",
      rotIntro: "តើគួរធ្វើអ្វីជាមួយស្រែក្រោយច្រូតស្រូវ? កំណត់អ្វីដែលសំខាន់សម្រាប់អ្នក ហើយជម្រើសនឹងតម្រៀបឡើងវិញ។",
      yourPriorities: "តើអ្វីសំខាន់សម្រាប់អ្នក?",
      prioLevels: "មិនសំខាន់|បន្តិច|សំខាន់|សំខាន់ណាស់",
      harvest: "តើអ្នកច្រូតស្រូវនៅពេលណា?",
      irrigation: "ខ្ញុំមានទឹកសម្រាប់ស្រោចស្រព (ស្រះ ប្រឡាយ ឬម៉ាស៊ីនបូម)",
      bestMatch: "សមស្របបំផុត",
      matchScore: "សមស្រប {n}%",
      worked: "នឹងដំណើរការបាន <b>{ok} ក្នុងចំណោម {n}</b> ឆ្នាំកន្លងមក ({mode})",
      rainfed: "ពឹងលើទឹកភ្លៀង",
      irrigatedMode: "មានស្រោចស្រព",
      yrOk: "ដំណើរការ",
      yrDry: "ស្ងួតពេក",
      yrHot: "ក្ដៅពេក",
      evidence: "ភស្តុតាងពី NASA",
      evSowing: "សាបព្រោះប្រហែល {date} នៅក្នុងស្រែប្រហែល {days} ថ្ងៃ។",
      evRain: "ទឹកភ្លៀងពេលដំណាំលូតលាស់៖ ជាមធ្យម <b>{mm} មម</b> ដំណាំត្រូវការប្រហែល {need} មម។",
      evSoil: "ទឹកដែលនៅសល់ក្នុងដីពេលសាបព្រោះ៖ ប្រហែល <b>{mm} មម</b> (ដី{texture})។",
      evHeat: "ចំនួនថ្ងៃក្ដៅជាង {c}°C៖ ជាមធ្យម <b>{d}</b> ថ្ងៃ។",
      evBare: "ស្រែនៅទីនេះជាធម្មតាទំនេរនៅខែ <b>{months}</b> (ភ្លៀងតិចជាង 50 មម ក្នុងមួយខែ)។",
      noBare: "គ្មានខែណាដែលជាធម្មតាភ្លៀងតិចជាង 50 មម។",
      pros: "អត្ថប្រយោជន៍",
      cons: "ហានិភ័យ",
      gaps: "មិនទាន់មានក្នុងទិន្នន័យ",
      localSoil: "ដីក្នុងតំបន់ (SoilGrids ស្រទាប់ 30 សម ខាងលើ)",
      soilLine: "{texture} · ដីឥដ្ឋ {clay}% · ខ្សាច់ {sand}% · កាបូនសរីរាង្គ {soc} ក្រ/គក · pH {ph}",
      sandy: "ខ្សាច់",
      loamy: "ល្បាយ",
      clayey: "ឥដ្ឋ",
      acidNote: "ដីជូរ (pH ក្រោម 5.5)៖ ដំណាំសណ្ដែកដូចជាសណ្ដែកបាយ អាចត្រូវការកំបោរ។ សូមសួរមន្ត្រីផ្សព្វផ្សាយកសិកម្ម។",
      lowCarbonNote: "កាបូនសរីរាង្គទាប៖ ជីបៃតង ឬការទុកសំណល់ដំណាំ នឹងជួយបានច្រើនបំផុត។",
      soilMissing: "មិនទាន់មានទិន្នន័យដីសម្រាប់ខេត្តនេះ៖ សន្មតថាជាដីល្បាយ។",
      reviewNote: "ទាំងនេះជាជម្រើសសម្រាប់ពិចារណា មិនមែនជាការណែនាំត្រូវធ្វើតាមទេ។ សូមពិភាក្សាជាមួយកសិករផ្សេងទៀត និងមន្ត្រីផ្សព្វផ្សាយកសិកម្ម មុនពេលផ្លាស់ប្ដូរដំណាំ។",
      assumptions: "តម្រូវការទឹករបស់ដំណាំ កម្រិតកំដៅ និងពិន្ទុអត្ថប្រយោជន៍ គឺជាការសន្មត ដែលត្រូវពិនិត្យជាមួយអ្នកជំនាញកសិកម្ម។",
      currentTag: "បច្ចុប្បន្ន",
    },
  };

  const MONTHS = {
    en: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    km: ["មករា", "កុម្ភៈ", "មីនា", "មេសា", "ឧសភា", "មិថុនា", "កក្កដា", "សីហា", "កញ្ញា", "តុលា", "វិច្ឆិកា", "ធ្នូ"],
  };

  const ICON = {
    green: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>',
    yellow: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" aria-hidden="true"><path d="M12 6v8M12 18.5v.01"/></svg>',
    red: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 4l9 16H3z"/><path d="M12 10v4M12 17.5v.01"/></svg>',
    check: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 12.5l4 4 8-9"/></svg>',
    left: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg>',
    right: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg>',
    search: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="6.5"/><path d="M16 16l4 4"/></svg>',
    logo: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 21V9"/><path d="M12 13c-4 0-6-2.5-6-6 3.5 0 6 2 6 6z"/><path d="M12 10c0-3.5 2.5-6 6-6 0 3.5-2 6-6 6z"/><path d="M5 21h14"/></svg>',
  };

  const LEVELS = ["green", "yellow", "red"];
  const STATUS_COLOR = { green: "#3f9a63", yellow: "#efb52d", red: "#d2493a" };
  const MISSING_COLOR = "#a9b3ae";

  // How each "colour map by" option turns a province into a colour, a legend and a short value.
  const METRICS = {
    status: {
      label: "mStatus",
      legend: "legendStatus",
      value: (p) => p.overall,
      color: (v) => STATUS_COLOR[v],
      format: (v) => t(v),
      keys: () => LEVELS.map((l) => [STATUS_COLOR[l], t(l)]),
    },
    rain: {
      label: "mRain",
      legend: "legendRain",
      value: (p) => p.season_check.rain_anomaly_pct,
      steps: [-40, -20, 20, 40],
      colors: ["#a6611a", "#dfc27d", "#e9ece6", "#80cdc1", "#1a8a7a"],
      format: (v) => signed(v) + "%",
      keys: () => [
        ["#a6611a", "< −40%"],
        ["#dfc27d", "−40 … −20%"],
        ["#e9ece6", "±20%"],
        ["#80cdc1", "+20 … +40%"],
        ["#1a8a7a", "> +40%"],
      ],
    },
    onset: {
      label: "mOnset",
      legend: "legendOnset",
      value: (p) => p.onset.delay_days,
      steps: [4, 15, 31],
      colors: ["#e3ece6", "#fdd49e", "#f4895a", "#c8382a"],
      format: (v) => (v === null ? t("notYet") : v <= 3 ? t("onTime") : t("daysLateShort", { n: v })),
      keys: () => [
        ["#e3ece6", t("onTime")],
        ["#fdd49e", "4–14"],
        ["#f4895a", "15–30"],
        ["#c8382a", "> 30 " + (state.lang === "km" ? "ថ្ងៃ" : "days")],
        [MISSING_COLOR, t("notYet")],
      ],
    },
    dry: {
      label: "mDry",
      legend: "legendDry",
      value: (p) => p.dry_spell.longest_days,
      steps: [7, 10, 15],
      colors: ["#e3ece6", "#fee391", "#f7a13a", "#c8571c"],
      format: (v) => t("daysUnit", { n: v }),
      keys: () => [
        ["#e3ece6", "< 7"],
        ["#fee391", "7–9"],
        ["#f7a13a", "10–14"],
        ["#c8571c", "15+ " + (state.lang === "km" ? "ថ្ងៃ" : "days")],
      ],
    },
    rotation: {
      label: "mRotation",
      legend: "legendRotation",
      value: (p) => bestRotation(p).id,
      color: (v) => ROT_COLOR[v],
      format: (v) => DATA.rotations.find((r) => r.id === v).label[state.lang],
      keys: () => DATA.rotations.map((r) => [ROT_COLOR[r.id], r.label[state.lang]]),
    },
  };
  const ROT_COLOR = { rice_fallow: "#bfae90", rice_mungbean: "#3f9a63", rice_maize: "#e0a526", green_manure_rice: "#2b7f8f" };

  // ---------------------------------------------------------------- state
  const state = {
    lang: stored("fieldshift-lang", "en"),
    metric: "status",
    slug: null,
    tab: "rotations",
    filter: null, // null or a status level
    query: "",
    sort: "risk",
    month: null,
    // Farmer's rotation settings, remembered in this browser.
    farm: loadFarm(),
  };
  const byslug = Object.fromEntries(DATA.provinces.map((p) => [p.slug, p]));
  const panel = document.getElementById("panel");
  let map = null;
  let provinceLayer = null;
  let controls = null;
  let hovered = null;

  // ---------------------------------------------------------------- helpers
  function stored(key, fallback) {
    try {
      return localStorage.getItem(key) || fallback;
    } catch (e) {
      return fallback;
    }
  }

  function store(key, value) {
    try {
      localStorage.setItem(key, value);
    } catch (e) {
      /* private mode: just not remembered */
    }
  }

  function loadFarm() {
    const fallback = { priorities: { soil: 2, income: 2, water: 2, labour: 1 }, harvest: "mid", irrigation: false };
    try {
      const saved = JSON.parse(stored("fieldshift-farm", "null"));
      return saved && saved.priorities ? { ...fallback, ...saved } : fallback;
    } catch (e) {
      return fallback;
    }
  }

  // ---------------------------------------------------------------- rotations
  // Score = how well a rotation's benefits match the farmer's priorities (0-1)
  //       x how often it would have worked in past years with this province's NASA weather (0-1).
  function rotationStats(p, r) {
    const res = p.rotation.rotations[r.id];
    if (!res.tested) return null;
    return res.by_start[state.farm.harvest] || res.by_start.any;
  }

  function rotationScores(p) {
    const w = state.farm.priorities;
    const total = Object.values(w).reduce((a, b) => a + b, 0);
    return DATA.rotations
      .map((r) => {
        const s = rotationStats(p, r);
        const match = total ? Object.keys(w).reduce((sum, k) => sum + w[k] * r.benefits[k], 0) / total : 0.5;
        const reliability = s ? (state.farm.irrigation ? s.reliability_irrigated : s.reliability_rainfed) : 1;
        return { rot: r, stats: s, match, reliability, score: match * reliability };
      })
      .sort((a, b) => b.score - a.score);
  }

  function bestRotation(p) {
    return rotationScores(p)[0].rot;
  }

  function saveFarm() {
    store("fieldshift-farm", JSON.stringify(state.farm));
  }

  function t(key, vars) {
    let s = T[state.lang][key] || T.en[key] || key;
    for (const [k, v] of Object.entries(vars || {})) s = s.split("{" + k + "}").join(v);
    return s;
  }

  function fmtDate(iso) {
    if (!iso) return t("notYet");
    const [, m, d] = iso.split("-").map(Number);
    return `${d} ${MONTHS[state.lang][m - 1]}`;
  }

  function signed(n) {
    return (n > 0 ? "+" : n < 0 ? "−" : "±") + Math.abs(Math.round(n));
  }

  function worst(...levels) {
    return levels.reduce((a, b) => (LEVELS.indexOf(b) > LEVELS.indexOf(a) ? b : a), "green");
  }

  function chip(level) {
    return `<span class="chip chip--${level}">${ICON[level]}${t(level)}</span>`;
  }

  function nameMain(p) {
    return state.lang === "km" ? p.name_km : p.name_en;
  }

  function nameSub(p) {
    return state.lang === "km" ? p.name_en : p.name_km;
  }

  function metricColor(p, metric) {
    const m = METRICS[metric || state.metric];
    const v = m.value(p);
    if (m.color) return m.color(v);
    if (v === null || v === undefined) return MISSING_COLOR;
    return m.colors[m.steps.filter((s) => v >= s).length];
  }

  function metricText(p) {
    return METRICS[state.metric].format(METRICS[state.metric].value(p));
  }

  function issues(p) {
    const out = [];
    if (!p.onset.date) out.push("issueNoOnset");
    else if (p.onset.level === "red") out.push("issueLate");
    if (p.season_check.level !== "green") out.push(p.season_check.rain_anomaly_pct < 0 ? "issueDry" : "issueWet");
    if (p.dry_spell.level !== "green") out.push("issueDrySpell");
    if (p.flood.level !== "green") out.push("issueFlood");
    return out;
  }

  function summary(p) {
    const list = issues(p);
    return list.length ? list.map((k) => t(k)).join(" · ") : t("issueNone");
  }

  function delayText(d) {
    if (d === null) return t("notYet");
    if (Math.abs(d) <= 3) return t("onTime");
    return d > 0 ? t("daysLate", { n: d }) : t("daysEarly", { n: -d });
  }

  function riskScore(p) {
    const sub = [p.onset.level, p.season_check.level, p.dry_spell.level, p.flood.level];
    return LEVELS.indexOf(p.overall) * 100 + sub.reduce((s, l) => s + LEVELS.indexOf(l), 0) * 10 + (p.onset.delay_days || 0) / 10;
  }

  function visibleProvinces() {
    const q = state.query.trim().toLowerCase();
    const list = DATA.provinces.filter(
      (p) =>
        (!state.filter || p.overall === state.filter) &&
        (!q || p.name_en.toLowerCase().includes(q) || p.name_km.includes(q))
    );
    const byName = (a, b) => nameMain(a).localeCompare(nameMain(b));
    return list.sort(state.sort === "risk" ? (a, b) => riskScore(b) - riskScore(a) || byName(a, b) : byName);
  }

  function dayOf(iso) {
    return Date.parse(iso + "T00:00:00Z") / 86400000;
  }

  // ---------------------------------------------------------------- panel: list
  function row(p) {
    return `<li><button class="prow" data-slug="${p.slug}">
      <span class="prow-swatch" style="background:${metricColor(p)}"></span>
      <span class="prow-main">
        <span class="prow-name">${nameMain(p)}<span class="prow-sub">${nameSub(p)}</span></span>
        <span class="prow-sum">${summary(p)}</span>
      </span>
      <span class="prow-val">${state.metric === "status" ? chip(p.overall) : metricText(p)}</span>
    </button></li>`;
  }

  function rowsHtml() {
    const list = visibleProvinces();
    return list.length ? list.map(row).join("") : `<li class="empty">${t("noMatch")}</li>`;
  }

  function listView() {
    const counts = Object.fromEntries(LEVELS.map((l) => [l, DATA.provinces.filter((p) => p.overall === l).length]));
    const overview = ["red", "yellow", "green"]
      .map(
        (l) => `<button class="ov ov--${l}" data-filter="${l}" aria-pressed="${state.filter === l}">
          <span class="ov-num">${counts[l]}</span><span class="ov-label">${ICON[l]}${t(l)}</span>
        </button>`
      )
      .join("");
    return `<div class="overview">${overview}</div>
      <div class="search">${ICON.search}
        <input id="q" type="search" autocomplete="off" placeholder="${t("search", { n: DATA.provinces.length })}"
          aria-label="${t("search", { n: DATA.provinces.length })}" value="${state.query.replace(/"/g, "&quot;")}">
      </div>
      <div class="list-head">
        <span id="count">${t("provincesCount", { n: visibleProvinces().length })}</span>
        <span class="list-tools">
          ${state.filter ? `<button class="link" data-clear>${t("clearFilter")}</button>` : ""}
          <span class="seg seg--small" role="group" aria-label="${t("sortBy")}">
            <button data-sort="risk" aria-pressed="${state.sort === "risk"}">${t("sortRisk")}</button>
            <button data-sort="name" aria-pressed="${state.sort === "name"}">${t("sortName")}</button>
          </span>
        </span>
      </div>
      <ul class="rows" id="rows">${rowsHtml()}</ul>`;
  }

  // ---------------------------------------------------------------- panel: detail
  function kpi(tab, metric, label, value, sub, level) {
    const on = state.tab === tab;
    return `<button class="kpi${on ? " is-on" : ""}" data-kpi="${tab}" data-metric="${metric}">
      <span class="kpi-label">${label}</span>
      <span class="kpi-value" style="--c:${STATUS_COLOR[level]}">${value}</span>
      <span class="kpi-sub">${sub}</span>
    </button>`;
  }

  function rainChart(p) {
    const W = 340, H = 140, left = 28, bottom = 18, top = 6;
    const months = p.monthly;
    const peak = Math.max(...months.map((m) => Math.max(m.normal_mm, m.this_year_mm || 0)));
    const step = peak > 400 ? 200 : peak > 200 ? 100 : 50;
    const max = Math.ceil(peak / step) * step || step;
    const y = (v) => H - bottom - ((H - bottom - top) * v) / max;
    const slot = (W - left) / 12;
    const bw = slot * 0.34;
    let svg = "";
    for (let v = 0; v <= max; v += step) {
      svg += `<line class="grid" x1="${left}" x2="${W}" y1="${y(v)}" y2="${y(v)}"/><text x="${left - 5}" y="${y(v) + 3}" text-anchor="end">${v}</text>`;
    }
    months.forEach((m, i) => {
      const x = left + i * slot + slot / 2;
      svg += `<g class="m${state.month === i ? " is-on" : ""}" data-month="${i}" tabindex="0">
        <rect class="hit" x="${left + i * slot}" y="0" width="${slot}" height="${H - bottom + 2}"/>
        <rect x="${x - bw - 1}" y="${y(m.normal_mm)}" width="${bw}" height="${y(0) - y(m.normal_mm)}" rx="2" fill="var(--rain-normal)"/>
        ${m.this_year_mm === null ? "" : `<rect x="${x + 1}" y="${y(m.this_year_mm)}" width="${bw}" height="${y(0) - y(m.this_year_mm)}" rx="2" fill="var(--rain)" opacity="${m.partial ? 0.45 : 1}"/>`}
        <text x="${x}" y="${H - 4}" text-anchor="middle">${state.lang === "km" ? i + 1 : MONTHS.en[i][0]}</text>
      </g>`;
    });
    return `<svg class="chart" viewBox="0 0 ${W} ${H}" role="img" aria-label="${t("monthlyRain")}">${svg}</svg>`;
  }

  function monthReadout(p, i) {
    const m = p.monthly[i];
    const month = MONTHS[state.lang][i];
    if (m.this_year_mm === null) return t("notYetMonth", { month, normal: Math.round(m.normal_mm) });
    return (
      t("monthReadout", { month, year: DATA.currentYear, mm: Math.round(m.this_year_mm), normal: Math.round(m.normal_mm) }) +
      (m.partial ? t("monthPartial") : "")
    );
  }

  function seasonTab(p) {
    const sc = p.season_check;
    if (state.month === null) state.month = Math.max(0, p.monthly.findIndex((m) => m.partial) - 1);
    return `<div class="stats">
        <div class="stat">
          <div class="stat-label">${t("rainSince")}</div>
          <div class="stat-value">${signed(sc.rain_anomaly_pct)}%</div>
          <div class="stat-sub">${t("vsNormal", { mm: sc.season_rain_mm, normal: sc.normal_season_rain_mm })}</div>
        </div>
        <div class="stat">
          <div class="stat-label">${t("soil")}</div>
          <div class="stat-value">${Math.round(sc.soil_moisture_now * 100)}%</div>
          <div class="stat-sub">${t("soilSub", { normal: Math.round(sc.soil_moisture_normal * 100) })}</div>
        </div>
      </div>
      <div class="sub-head">${t("monthlyRain")}
        <span class="keys"><span class="sw" style="background:var(--rain-normal)"></span>${t("normalYears")}
        <span class="sw" style="background:var(--rain)"></span>${DATA.currentYear}</span></div>
      ${rainChart(p)}
      <p class="readout" id="month-readout">${monthReadout(p, state.month)}</p>`;
  }

  function timeline(p) {
    const year = DATA.currentYear;
    const normal = `${year}-${p.onset.normal_date}`;
    const start = dayOf(`${year}-04-01`);
    const latest = Math.max(dayOf(normal), p.onset.window_end ? dayOf(p.onset.window_end) : 0);
    const endMonth = Math.min(11, Math.max(7, new Date((latest + 20) * 86400000).getUTCMonth() + 1));
    const end = dayOf(`${year}-${String(endMonth + 1).padStart(2, "0")}-01`);
    const pct = (iso) => (100 * (dayOf(iso) - start)) / (end - start);
    let axis = "";
    for (let m = 4; m <= endMonth; m++) {
      axis += `<span style="left:${pct(`${year}-${String(m).padStart(2, "0")}-01`)}%">${MONTHS[state.lang][m - 1]}</span>`;
    }
    let marks = `<div class="tl-mark tl-mark--normal" style="left:${pct(normal)}%"><span>${t("normalOnset")}</span></div>`;
    if (p.onset.date) {
      const a = pct(p.onset.window_start), b = pct(p.onset.window_end);
      marks = `<div class="tl-window" style="left:${a}%;width:${b - a}%"></div>` + marks;
      marks += `<div class="tl-mark tl-mark--this" style="left:${pct(p.onset.date)}%"><span>${year}</span></div>`;
    }
    return `<div class="tl" role="img" aria-label="${t("planting")}"><div class="tl-track">${marks}</div><div class="tl-axis">${axis}</div></div>`;
  }

  function plantingTab(p) {
    const on = p.onset;
    return `<div class="onset">
        <div class="stat-label">${t("onset", { year: DATA.currentYear })}</div>
        <div class="onset-line"><span class="onset-date">${fmtDate(on.date)}</span>
          <span class="onset-delay" style="color:${STATUS_COLOR[on.level]}">${delayText(on.delay_days)}</span></div>
        <div class="stat-sub">${t("normalOnset")}: ${fmtDate(`${DATA.currentYear}-${on.normal_date}`)}</div>
      </div>
      ${timeline(p)}
      <p class="callout">${on.date ? t("windowText", { a: fmtDate(on.window_start), b: fmtDate(on.window_end) }) : t("windowWait")}</p>
      <p class="fine">${t("onsetRule")}</p>`;
  }

  function meter(value, yellowAt, redAt, max, unit) {
    const w = (v) => Math.min(100, (100 * v) / max);
    return `<div class="meter" role="img" aria-label="${value} ${unit}">
        <span class="z z-green" style="width:${w(yellowAt)}%"></span><span class="z z-yellow" style="width:${w(redAt) - w(yellowAt)}%"></span><span class="z z-red" style="width:${100 - w(redAt)}%"></span>
        <span class="meter-pin" style="left:${w(value)}%"></span>
      </div>
      <div class="meter-scale"><span style="left:${w(yellowAt)}%">${yellowAt}</span><span style="left:${w(redAt)}%">${redAt} ${unit}</span></div>`;
  }

  function risksTab(p) {
    const ds = p.dry_spell, fl = p.flood, r = DATA.rules;
    return `<div class="risk">
        <div class="risk-head"><span>${t("drySpell")}</span>${chip(ds.level)}</div>
        <p>${t("drySpellText", { n: ds.longest_days })}</p>
        ${meter(ds.longest_days, r.dry_spell_yellow, r.dry_spell_red, Math.max(15, ds.longest_days + 2), state.lang === "km" ? "ថ្ងៃ" : "days")}
      </div>
      <div class="risk">
        <div class="risk-head"><span>${t("flood")}</span>${chip(fl.level)}</div>
        <p>${t("floodText", { n: fl.recent_max_3day_mm })}</p>
        ${meter(fl.recent_max_3day_mm, fl.p95_3day_mm, fl.p99_3day_mm, Math.max(fl.p99_3day_mm * 1.3, fl.recent_max_3day_mm * 1.1), state.lang === "km" ? "មម" : "mm")}
      </div>`;
  }

  function historyTab(p) {
    const squares = p.backtest
      .map((b, i) => `<button class="yr${b.late_onset ? " yr--late" : ""}${b.dry_spell_alert ? " yr--dry" : ""}" data-year="${i}" aria-label="${b.year}">${String(b.year).slice(2)}</button>`)
      .join("");
    const late = p.backtest.filter((b) => b.late_onset).map((b) => b.year);
    return `<p class="fine">${t("historyText")}</p>
      <div class="years">${squares}</div>
      <div class="keys"><span class="sw" style="background:var(--red)"></span>${t("lateYear")}
        <span class="sw sw--ring"></span>${t("dryYear")}</div>
      <p class="readout" id="year-readout">${t("yearHint")}</p>
      ${late.length ? `<p class="callout">${t("lateYear")}: <b>${late.join(", ")}</b></p>` : ""}`;
  }

  function yearReadout(b) {
    return t("yearReadout", {
      year: b.year,
      onset: fmtDate(b.onset),
      delay: delayText(b.onset_delay_days),
      dry: b.longest_dry_spell_days,
      rain: Math.round(b.season_rain_mm),
    });
  }

  function monthList(months) {
    return months
      .slice()
      .sort((a, b) => ((a + 5) % 12) - ((b + 5) % 12)) // dry season reads Nov → Apr
      .map((m) => MONTHS[state.lang][m - 1])
      .join(", ");
  }

  function yearsStrip(stats) {
    const cells = stats.years
      .map(([year, waterOk, heatOk]) => {
        const ok = (state.farm.irrigation || waterOk) && heatOk;
        const cls = ok ? "ok" : !heatOk ? "hot" : "dry";
        return `<span class="ys ys--${cls}" title="${year}: ${t(ok ? "yrOk" : cls === "hot" ? "yrHot" : "yrDry")}"></span>`;
      })
      .join("");
    return `<div class="ystrip" role="img" aria-label="${stats.years.length}">${cells}</div>
      <div class="keys"><span class="sw ys--ok"></span>${t("yrOk")}<span class="sw ys--dry"></span>${t("yrDry")}<span class="sw ys--hot"></span>${t("yrHot")}</div>`;
  }

  function benefitDots(r) {
    return `<div class="bens">${Object.keys(DATA.priorities)
      .map((k) => {
        const n = Math.round(r.benefits[k] * 4);
        const dots = Array.from({ length: 4 }, (_, i) => `<i class="${i < n ? "on" : ""}"></i>`).join("");
        return `<span class="ben"><span>${DATA.priorities[k][state.lang]}</span><span class="dots">${dots}</span></span>`;
      })
      .join("")}</div>`;
  }

  function rotationCard(p, item, rank) {
    const { rot, stats, match, reliability, score } = item;
    const res = p.rotation.rotations[rot.id];
    const texture = t(p.rotation.soil_texture_used).toLowerCase();
    let evidence;
    if (stats) {
      const ok = Math.round(reliability * stats.years_tested);
      const [m, d] = stats.sow.split("-").map(Number);
      evidence = `<p>${t("worked", { ok, n: stats.years_tested, mode: t(state.farm.irrigation ? "irrigatedMode" : "rainfed") })}</p>
        ${yearsStrip(stats)}
        <ul class="ev">
          <li>${t("evSowing", { date: `${d} ${MONTHS[state.lang][m - 1]}`, days: res.days })}</li>
          <li>${t("evRain", { mm: stats.mean_rain_mm, need: res.water_need_mm })}</li>
          ${stats.mean_soil_water_mm ? `<li>${t("evSoil", { mm: stats.mean_soil_water_mm, texture })}</li>` : ""}
          <li>${t("evHeat", { c: res.heat_limit_c, d: stats.mean_heat_days })}</li>
        </ul>`;
    } else {
      const bare = p.rotation.bare_months;
      evidence = `<ul class="ev"><li>${bare.length ? t("evBare", { months: monthList(bare) }) : t("noBare")}</li></ul>`;
    }
    return `<li class="rot${rank === 0 ? " rot--best" : ""}" style="--rc:${ROT_COLOR[rot.id]}">
      <div class="rot-head">
        <span class="rot-rank">${rank + 1}</span>
        <div class="rot-title"><b>${rot.name[state.lang]}</b>
          ${rank === 0 ? `<span class="tag tag--best">${t("bestMatch")}</span>` : ""}
          ${rot.current ? `<span class="tag">${t("currentTag")}</span>` : ""}</div>
        <span class="rot-score">${Math.round(score * 100)}</span>
      </div>
      <div class="rot-bar"><span style="width:${Math.round(score * 100)}%"></span></div>
      <p class="rot-short">${rot.short[state.lang]}</p>
      <details${rank === 0 ? " open" : ""}>
        <summary>${t("evidence")} · ${t("pros").toLowerCase()} · ${t("cons").toLowerCase()}</summary>
        <div class="rot-body">
          ${evidence}
          ${benefitDots(rot)}
          <dl>
            <dt>${t("pros")}</dt><dd>${rot.pros[state.lang]}</dd>
            <dt>${t("cons")}</dt><dd>${rot.cons[state.lang]}</dd>
            <dt>${t("gaps")}</dt><dd>${rot.gaps[state.lang]}</dd>
          </dl>
          <p class="fine">${t("matchScore", { n: Math.round(match * 100) })}</p>
        </div>
      </details>
    </li>`;
  }

  function rotationList(p) {
    return rotationScores(p).map((item, i) => rotationCard(p, item, i)).join("");
  }

  function soilBox(p) {
    const s = p.rotation.soil;
    if (!s) return `<p class="fine">${t("soilMissing")}</p>`;
    const notes = [];
    if (s.ph !== null && s.ph < 5.5) notes.push(t("acidNote"));
    if (s.soc_g_kg !== null && s.soc_g_kg < 10) notes.push(t("lowCarbonNote"));
    return `<div class="soil"><div class="stat-label">${t("localSoil")}</div>
      <div>${t("soilLine", { texture: t(s.texture), clay: Math.round(s.clay_pct), sand: Math.round(s.sand_pct), soc: s.soc_g_kg, ph: s.ph })}</div>
      ${notes.map((n) => `<p class="fine">${n}</p>`).join("")}</div>`;
  }

  function rotationsTab(p) {
    const levels = t("prioLevels").split("|");
    const sliders = Object.keys(DATA.priorities)
      .map((k) => {
        const v = state.farm.priorities[k];
        return `<label class="prio"><span class="prio-name">${DATA.priorities[k][state.lang]}</span>
          <input type="range" min="0" max="3" step="1" value="${v}" data-prio="${k}" aria-valuetext="${levels[v]}">
          <span class="prio-val" id="prio-${k}">${levels[v]}</span></label>`;
      })
      .join("");
    const harvests = Object.keys(DATA.harvests)
      .map((k) => `<button data-harvest="${k}" aria-pressed="${state.farm.harvest === k}">${DATA.harvests[k][state.lang]}</button>`)
      .join("");
    return `<p class="fine">${t("rotIntro")}</p>
      <div class="farm">
        <div class="sub-head">${t("yourPriorities")}</div>
        ${sliders}
        <div class="sub-head">${t("harvest")}</div>
        <span class="seg seg--wrap" role="group" aria-label="${t("harvest")}">${harvests}</span>
        <label class="switch"><input type="checkbox" data-irrigation ${state.farm.irrigation ? "checked" : ""}><span></span>${t("irrigation")}</label>
      </div>
      <ol class="rots" id="rot-list">${rotationList(p)}</ol>
      ${soilBox(p)}
      <p class="callout callout--warn">${t("reviewNote")}</p>
      <p class="fine">${t("assumptions")}</p>`;
  }

  const TABS = [
    ["rotations", "rotations", rotationsTab],
    ["season", "seasonCheck", seasonTab],
    ["planting", "planting", plantingTab],
    ["risks", "risks", risksTab],
    ["history", "history", historyTab],
  ];

  function detailView(p) {
    const list = visibleProvinces();
    const pos = list.findIndex((x) => x.slug === p.slug);
    const sc = p.season_check;
    const tipItems = p.tips.map((id) => `<li>${ICON.check}<span>${DATA.tips[id][state.lang]}</span></li>`);
    // Show the first two tips; the rest fold away so the rotations stay near the top.
    const tips =
      tipItems.slice(0, 2).join("") +
      (tipItems.length > 2
        ? `<li class="more"><details><summary>${t("moreTips", { n: tipItems.length - 2 })}</summary><ul>${tipItems.slice(2).join("")}</ul></details></li>`
        : "");
    const tabs = TABS.map(
      ([id, label]) => `<button role="tab" id="tab-${id}" aria-selected="${state.tab === id}" aria-controls="tabpanel" data-tab="${id}">${t(label)}</button>`
    ).join("");
    const content = TABS.find(([id]) => id === state.tab)[2](p);
    return `<div class="detail-nav">
        <button class="link back" data-back>${ICON.left}${t("back")}</button>
        ${pos >= 0 && list.length > 1
          ? `<span class="pager"><button data-step="-1" aria-label="${t("prev")}">${ICON.left}</button>
             <span>${pos + 1} / ${list.length}</span>
             <button data-step="1" aria-label="${t("next")}">${ICON.right}</button></span>`
          : ""}
      </div>
      <section class="hero">
        <div class="hero-top">
          <div><h2 class="hero-name">${nameMain(p)}</h2><div class="hero-sub">${nameSub(p)}</div></div>
          ${chip(p.overall)}
        </div>
        <p class="hero-sum">${summary(p)}</p>
      </section>
      <div class="kpis">
        ${kpi("season", "rain", t("kpiRain"), signed(sc.rain_anomaly_pct) + "%", t("rainSince"), sc.level)}
        ${kpi("planting", "onset", t("kpiOnset"), fmtDate(p.onset.date), delayText(p.onset.delay_days), p.onset.level)}
        ${kpi("risks", "dry", t("kpiDry"), t("daysUnit", { n: p.dry_spell.longest_days }), "< 1 mm/day", p.dry_spell.level)}
      </div>
      <section class="todo">
        <h3>${t("whatToDo")}</h3>
        <ul>${tips}</ul>
      </section>
      <div class="tabs" role="tablist">${tabs}</div>
      <div class="tabpanel" id="tabpanel" role="tabpanel" aria-labelledby="tab-${state.tab}">${content}</div>`;
  }

  // ---------------------------------------------------------------- panel: frame
  function header() {
    const lang = (l, label) => `<button data-lang="${l}" lang="${l}" aria-pressed="${state.lang === l}">${label}</button>`;
    return `<header class="top">
        <div class="brand"><span class="brand-mark">${ICON.logo}</span>
          <div><h1>Field Shift KH</h1><p>${t("tagline")}</p></div></div>
        <span class="seg" role="group" aria-label="Language / ភាសា">${lang("en", "EN")}${lang("km", "ខ្មែរ")}</span>
      </header>
      <p class="season-line"><span class="live"></span>${t("seasonLine", { year: DATA.currentYear, date: fmtDate(DATA.lastDataDate) })}</p>`;
  }

  function footer() {
    return `<footer class="about"><p>${t("about")}</p>
      <p><a href="https://power.larc.nasa.gov/" target="_blank" rel="noopener">${t("source")}</a> ·
        <a href="${DATA.repoUrl}" target="_blank" rel="noopener">${t("code")}</a></p></footer>`;
  }

  function render() {
    const p = byslug[state.slug];
    document.documentElement.lang = state.lang;
    document.body.classList.toggle("lang-km", state.lang === "km");
    panel.innerHTML = `<div class="panel-inner">${header()}${p ? detailView(p) : listView()}${footer()}</div>`;
    bindPanel(p);
    renderControls();
    restyle();
  }

  function refreshRows() {
    const rows = document.getElementById("rows");
    if (!rows) return;
    rows.innerHTML = rowsHtml();
    document.getElementById("count").textContent = t("provincesCount", { n: visibleProvinces().length });
    bindRows();
    restyle();
  }

  function bindRows() {
    panel.querySelectorAll("[data-slug]").forEach((b) => {
      b.addEventListener("click", () => select(b.dataset.slug));
      b.addEventListener("mouseenter", () => setHover(b.dataset.slug));
      b.addEventListener("mouseleave", () => setHover(null));
    });
  }

  function bindPanel(p) {
    const on = (sel, ev, fn) => panel.querySelectorAll(sel).forEach((el) => el.addEventListener(ev, (e) => fn(el, e)));
    on("[data-lang]", "click", (el) => {
      state.lang = el.dataset.lang;
      store("fieldshift-lang", state.lang);
      render();
    });
    bindRows();
    on("[data-filter]", "click", (el) => {
      state.filter = state.filter === el.dataset.filter ? null : el.dataset.filter;
      render();
    });
    on("[data-clear]", "click", () => {
      state.filter = null;
      render();
    });
    on("[data-sort]", "click", (el) => {
      state.sort = el.dataset.sort;
      render();
    });
    const q = document.getElementById("q");
    if (q) {
      q.addEventListener("input", () => {
        state.query = q.value;
        refreshRows();
      });
      q.addEventListener("keydown", (e) => {
        const first = visibleProvinces()[0];
        if (e.key === "Enter" && first) select(first.slug);
      });
    }
    if (!p) return;

    on("[data-back]", "click", () => select(null));
    on("[data-step]", "click", (el) => {
      const list = visibleProvinces();
      const i = list.findIndex((x) => x.slug === state.slug);
      select(list[(i + Number(el.dataset.step) + list.length) % list.length].slug);
    });
    on("[data-tab]", "click", (el) => setTab(el.dataset.tab));
    on("[role=tab]", "keydown", (el, e) => {
      if (e.key !== "ArrowRight" && e.key !== "ArrowLeft") return;
      const ids = TABS.map(([id]) => id);
      const next = ids[(ids.indexOf(state.tab) + (e.key === "ArrowRight" ? 1 : ids.length - 1)) % ids.length];
      setTab(next);
      document.getElementById("tab-" + next).focus();
    });
    on("[data-kpi]", "click", (el) => {
      state.metric = el.dataset.metric;
      setTab(el.dataset.kpi);
      renderControls();
      restyle();
    });

    // Rotation settings: update the ranking (and the map, if it shows rotations) without
    // re-rendering the whole panel, so the slider being dragged keeps focus.
    const rotList = document.getElementById("rot-list");
    const farmChanged = () => {
      saveFarm();
      if (rotList) rotList.innerHTML = rotationList(p);
      if (state.metric === "rotation") restyle();
    };
    const levels = t("prioLevels").split("|");
    on("[data-prio]", "input", (el) => {
      state.farm.priorities[el.dataset.prio] = Number(el.value);
      el.setAttribute("aria-valuetext", levels[el.value]);
      document.getElementById("prio-" + el.dataset.prio).textContent = levels[el.value];
      farmChanged();
    });
    on("[data-harvest]", "click", (el) => {
      state.farm.harvest = el.dataset.harvest;
      panel.querySelectorAll("[data-harvest]").forEach((b) => b.setAttribute("aria-pressed", b === el));
      farmChanged();
    });
    on("[data-irrigation]", "change", (el) => {
      state.farm.irrigation = el.checked;
      farmChanged();
    });

    // Interactive readouts: chart months and back-test years.
    const monthOut = document.getElementById("month-readout");
    const showMonth = (el) => {
      state.month = Number(el.dataset.month);
      panel.querySelectorAll(".m").forEach((g) => g.classList.toggle("is-on", g === el));
      monthOut.innerHTML = monthReadout(p, state.month);
    };
    ["mouseenter", "focus", "click"].forEach((ev) => on(".m", ev, showMonth));

    const yearOut = document.getElementById("year-readout");
    const showYear = (el) => {
      panel.querySelectorAll(".yr").forEach((y) => y.classList.toggle("is-on", y === el));
      yearOut.innerHTML = yearReadout(p.backtest[Number(el.dataset.year)]);
    };
    ["mouseenter", "focus", "click"].forEach((ev) => on(".yr", ev, showYear));
  }

  function setTab(tab) {
    const p = byslug[state.slug];
    state.tab = tab;
    const scroll = panel.scrollTop;
    render();
    panel.scrollTop = scroll;
    if (p) document.getElementById("tab-" + tab)?.scrollIntoView({ block: "nearest" });
  }

  function select(slug) {
    const p = byslug[slug];
    state.slug = p ? slug : null;
    state.month = null;
    render();
    panel.scrollTop = 0;
    history.replaceState(null, "", p ? "#" + slug : location.pathname + location.search);
    if (!map) return;
    const layer = p && layerFor(slug);
    if (layer) map.flyToBounds(layer.getBounds(), { padding: [40, 40], maxZoom: 9, duration: 0.6 });
    else map.flyToBounds(DATA.bounds, fitOptions(0.6));
  }

  function fitOptions(duration) {
    // On phones the map controls sit across the top of the map; leave room for them.
    const narrow = window.matchMedia("(max-width: 760px)").matches;
    return { paddingTopLeft: narrow ? [8, 64] : [16, 16], paddingBottomRight: [16, 16], duration, animate: duration > 0 };
  }

  // ---------------------------------------------------------------- map
  function layerFor(slug) {
    let found = null;
    if (provinceLayer) provinceLayer.eachLayer((l) => {
      if (l.feature.properties.slug === slug) found = l;
    });
    return found;
  }

  function styleFor(slug) {
    const p = byslug[slug];
    const selected = slug === state.slug;
    const hot = slug === hovered;
    const faded = (state.filter && p.overall !== state.filter) || (state.slug && !selected);
    return {
      fillColor: metricColor(p),
      fillOpacity: faded ? 0.35 : 0.9,
      color: selected || hot ? "#1b2420" : "#ffffff",
      weight: selected ? 3 : hot ? 2.5 : 1.2,
    };
  }

  function restyle() {
    if (!provinceLayer) return;
    provinceLayer.eachLayer((l) => {
      l.setStyle(styleFor(l.feature.properties.slug));
      // Only the selected shape is raised: raising the hovered one under the mouse breaks mouseout.
      if (l.feature.properties.slug === state.slug) l.bringToFront();
    });
  }

  function setHover(slug) {
    hovered = slug;
    restyle();
    panel.querySelectorAll(".prow").forEach((r) => r.classList.toggle("is-hot", r.dataset.slug === slug));
  }

  function tooltipFor(slug) {
    const p = byslug[slug];
    const m = METRICS[state.metric];
    return `<div class="tip-name">${nameMain(p)} <span>${nameSub(p)}</span></div>
      <div class="tip-row"><span>${t(m.label)}</span><b>${state.metric === "status" ? chip(p.overall) : metricText(p)}</b></div>
      ${state.metric === "status" ? `<div class="tip-sum">${summary(p)}</div>` : ""}`;
  }

  function renderControls() {
    if (!controls) return;
    const m = METRICS[state.metric];
    const buttons = Object.entries(METRICS)
      .map(([id, x]) => `<button data-metric="${id}" aria-pressed="${state.metric === id}">${t(x.label)}</button>`)
      .join("");
    const keys = m.keys().map(([c, label]) => `<span class="lg-item"><span class="sw" style="background:${c}"></span>${label}</span>`).join("");
    controls.innerHTML = `<div class="ctl-label">${t("colourBy")}</div>
      <div class="seg seg--metric" role="group" aria-label="${t("colourBy")}">${buttons}</div>
      <div class="lg-title">${t(m.legend)}</div><div class="lg">${keys}</div>`;
    controls.querySelectorAll("[data-metric]").forEach((b) =>
      b.addEventListener("click", () => {
        state.metric = b.dataset.metric;
        render();
      })
    );
  }

  function initMap() {
    map = Object.values(window).find((v) => window.L && v instanceof L.Map) || null;
    if (!map) return;

    // Fade out everything outside Cambodia with a "world minus Cambodia" polygon.
    const outline = DATA.shapes.features.find((f) => f.properties.slug === "_cambodia");
    const hole = outline.geometry.coordinates[0].map(([lng, lat]) => [lat, lng]);
    map.createPane("mask").style.zIndex = 450;
    L.polygon([[[89, -179], [89, 179], [-89, 179], [-89, -179]], hole], {
      pane: "mask",
      stroke: false,
      fillColor: getComputedStyle(document.body).getPropertyValue("--map-bg").trim() || "#eef1ee",
      fillOpacity: 1,
      interactive: false,
    }).addTo(map);
    L.polygon(hole, { pane: "mask", fill: false, color: "#9aa79f", weight: 1.5, interactive: false }).addTo(map);

    provinceLayer = L.geoJSON(
      { type: "FeatureCollection", features: DATA.shapes.features.filter((f) => byslug[f.properties.slug]) },
      {
        style: (f) => styleFor(f.properties.slug),
        onEachFeature: (f, layer) => {
          const slug = f.properties.slug;
          layer.bindTooltip(() => tooltipFor(slug), { sticky: true, direction: "top", offset: [0, -12], className: "tip" });
          layer.on("mouseover", () => {
            provinceLayer.eachLayer((other) => other !== layer && other.closeTooltip());
            setHover(slug);
          });
          layer.on("mouseout", () => setHover(null));
          layer.on("click", () => select(slug));
        },
      }
    ).addTo(map);

    controls = L.DomUtil.create("div", "map-ctl", map.getContainer());
    L.DomEvent.disableClickPropagation(controls);
    L.DomEvent.disableScrollPropagation(controls);
  }

  // ---------------------------------------------------------------- start
  initMap();
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && state.slug) select(null);
  });
  window.addEventListener("hashchange", () => select(location.hash.slice(1) || null));

  state.slug = byslug[location.hash.slice(1)] ? location.hash.slice(1) : null;
  render();
  if (map) {
    // Folium sized the map before our layout CSS applied; measure again, then fit.
    map.invalidateSize();
    if (state.slug) map.fitBounds(layerFor(state.slug).getBounds(), { padding: [40, 40], maxZoom: 9 });
    else map.flyToBounds(DATA.bounds, fitOptions(0));
  }
})();
