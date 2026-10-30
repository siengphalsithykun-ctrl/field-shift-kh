"""Crop-rotation options compared for each province, and how NASA data tests them.

Every number here is a starting assumption for a hackathon prototype. Check crop durations, water
needs, heat limits and the 0-1 benefit scores with mentors and agronomists before trusting them.

How a rotation is tested against the climate (in analysis.py, for every year 2000-2025):
  - water: rain in the crop's growing window + water left in the soil at sowing >= the crop's water need
           (soil water = how much wetter than 0.5 the root zone is (NASA POWER GWETROOT) x how much water
           the soil can hold, which depends on texture from SoilGrids: clay holds more than sand)
  - heat:  fewer than HEAT_BAD_DAYS days above the crop's heat limit (NASA POWER T2M_MAX) in the window
"Reliability" = share of past years where both held. The web page then ranks rotations by
reliability x how well the rotation's benefits match the farmer's priorities.

Partly generated with AI assistance (Claude Code); reviewed by the team.
"""

# Root-zone water the soil can give a crop per 0.1 of wetness above 0.5 (mm), by texture group.
SOIL_WATER_PER_TENTH_MM = {"clayey": 60, "loamy": 45, "sandy": 25}
HEAT_BAD_DAYS = 5

# A dry-season crop is sown right after the rice harvest, so its sowing date depends on when the
# farmer harvests (short-duration rice is harvested earlier). The page lets the farmer pick one.
DRY_SEASON_STARTS = {"early": "10-25", "mid": "11-15", "late": "12-05"}
HARVEST_LABELS = {
    "early": ("Late Oct", "ចុងខែតុលា"),
    "mid": ("Mid Nov", "ពាក់កណ្ដាលខែវិច្ឆិកា"),
    "late": ("Early Dec", "ដើមខែធ្នូ"),
}

# benefits: 0-1 scores the farmer's priority sliders weight (assumptions to review).
#   soil = improves soil health · income = extra income · water = saves water (1 = uses none)
#   labour = low extra work (1 = no extra work)
ROTATIONS = [
    {
        "id": "rice_fallow",
        "label": ("Bare (current)", "ទុកទំនេរ (បច្ចុប្បន្ន)"),
        "current": True,
        "name": ("Rice → bare dry season (current)", "ស្រូវ → ទុកដីទំនេររដូវប្រាំង (បច្ចុប្បន្ន)"),
        "short": ("Wet-season rice, then the field stays bare until the next rains.",
                  "ដាំស្រូវរដូវវស្សា បន្ទាប់មកទុកដីទំនេររហូតដល់ភ្លៀងបន្ទាប់។"),
        "window": None,
        "benefits": {"soil": 0.1, "income": 0.0, "water": 1.0, "labour": 1.0},
        "pros": ("No extra cost, water or work.", "មិនចំណាយ ទឹក ឬកម្លាំងបន្ថែម។"),
        "cons": ("Bare soil for months: erosion, weeds, nutrients and organic matter lost; no dry-season income.",
                 "ដីទំនេររាប់ខែ៖ សំណឹកដី ស្មៅ បាត់បង់ជីជាតិ និងសារធាតុសរីរាង្គ គ្មានចំណូលរដូវប្រាំង។"),
        "gaps": ("Doesn't account for straw burning or grazing on the stubble.",
                 "មិនបានគិតពីការដុតចំបើង ឬការឱ្យសត្វស៊ីស្មៅលើគល់ស្រូវ។"),
    },
    {
        "id": "rice_mungbean",
        "label": ("Mungbean", "សណ្ដែកបាយ"),
        "current": False,
        "name": ("Rice → mungbean", "ស្រូវ → សណ្ដែកបាយ"),
        "short": ("Sow a short (~70-day) mungbean right after the rice harvest, on the water left in the soil.",
                  "សាបព្រោះសណ្ដែកបាយរយៈពេលខ្លី (~70 ថ្ងៃ) ភ្លាមៗក្រោយច្រូតស្រូវ ដោយប្រើសំណើមដែលនៅសល់ក្នុងដី។"),
        "window": {"starts": DRY_SEASON_STARTS, "days": 70, "water_need_mm": 250, "heat_limit_c": 37, "uses_soil_water": True},
        "benefits": {"soil": 0.8, "income": 0.6, "water": 0.6, "labour": 0.5},
        "pros": ("Legume: fixes nitrogen for the next rice crop; extra income; covers bare soil.",
                 "ដំណាំសណ្ដែក៖ ចាប់អាសូតសម្រាប់ស្រូវបន្ទាប់ ចំណូលបន្ថែម គ្របដណ្ដប់ដីទំនេរ។"),
        "cons": ("Fails if the soil dries out early; needs seed, labour and a market to sell to.",
                 "អាចបរាជ័យបើដីស្ងួតលឿន ត្រូវការគ្រាប់ពូជ កម្លាំង និងទីផ្សារ។"),
        "gaps": ("Field drainage, pests and local mungbean prices are not in the data.",
                 "ការបង្ហូរទឹកក្នុងស្រែ សត្វល្អិត និងតម្លៃសណ្ដែកក្នុងតំបន់ មិនមានក្នុងទិន្នន័យ។"),
    },
    {
        "id": "rice_maize",
        "label": ("Maize / veg", "ពោត / បន្លែ"),
        "current": False,
        "name": ("Rice → maize or vegetables", "ស្រូវ → ពោត ឬបន្លែ"),
        "short": ("A longer (~100-day) cash crop in the dry season. Usually needs a pond, canal or pump.",
                  "ដំណាំលក់យកប្រាក់រយៈពេលវែងជាង (~100 ថ្ងៃ) ក្នុងរដូវប្រាំង។ ជាធម្មតាត្រូវការស្រះ ប្រឡាយ ឬម៉ាស៊ីនបូមទឹក។"),
        "window": {"starts": DRY_SEASON_STARTS, "days": 100, "water_need_mm": 450, "heat_limit_c": 38, "uses_soil_water": True},
        "benefits": {"soil": 0.3, "income": 0.9, "water": 0.1, "labour": 0.2},
        "pros": ("Highest income potential; keeps the field in use.", "សក្ដានុពលចំណូលខ្ពស់បំផុត ប្រើដីបានពេញលេញ។"),
        "cons": ("High water and labour needs; risky without irrigation; can deplete soil if not fertilised.",
                 "ត្រូវការទឹក និងកម្លាំងច្រើន មានហានិភ័យបើគ្មានប្រព័ន្ធស្រោចស្រព អាចធ្វើឱ្យដីខ្សោះបើមិនដាក់ជី។"),
        "gaps": ("Irrigation access, input costs and market prices are not in the data.",
                 "លទ្ធភាពស្រោចស្រព ថ្លៃធាតុចូល និងតម្លៃទីផ្សារ មិនមានក្នុងទិន្នន័យ។"),
    },
    {
        "id": "green_manure_rice",
        "label": ("Green manure", "ជីបៃតង"),
        "current": False,
        "name": ("Green manure → rice", "ជីបៃតង → ស្រូវ"),
        "short": ("Grow a cover crop such as sesbania with the first rains (~50 days), then plough it in before rice.",
                  "ដាំដំណាំគ្រប់ដណ្ដប់ដូចជាស្នោ ពេលភ្លៀងដំបូង (~50 ថ្ងៃ) រួចភ្ជួរលុបមុនដាំស្រូវ។"),
        "window": {"starts": {"any": "04-15"}, "days": 50, "water_need_mm": 200, "heat_limit_c": 40, "uses_soil_water": False},
        "benefits": {"soil": 1.0, "income": 0.1, "water": 0.7, "labour": 0.6},
        "pros": ("Adds organic matter and nitrogen; can cut fertiliser costs for rice.",
                 "បន្ថែមសារធាតុសរីរាង្គ និងអាសូត អាចកាត់បន្ថយថ្លៃជីសម្រាប់ស្រូវ។"),
        "cons": ("No direct income; can delay rice if the monsoon starts late.",
                 "គ្មានចំណូលផ្ទាល់ អាចពន្យារពេលដាំស្រូវ បើរដូវវស្សាចាប់ផ្តើមយឺត។"),
        "gaps": ("Seed availability and how much fertiliser it really saves need local checking.",
                 "លទ្ធភាពរកគ្រាប់ពូជ និងបរិមាណជីដែលសន្សំបានពិតប្រាកដ ត្រូវពិនិត្យក្នុងតំបន់។"),
    },
]

PRIORITIES = {
    "soil": ("Better soil", "ដីល្អជាងមុន"),
    "income": ("More income", "ចំណូលច្រើនជាង"),
    "water": ("Save water", "សន្សំទឹក"),
    "labour": ("Less work", "ការងារតិចជាង"),
}
