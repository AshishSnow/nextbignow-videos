# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# FreshNestHub 35 — "Does sesame have more calcium than milk?" (35-50 s rule; ONE takeaway: on paper yes, in your body much less)
# METAPHOR for the whole video: a BOXING MATCH. Sesame seed vs a glass of milk. On paper = a knockout; then oxalate HANDCUFFS the seed's gloves.
# Facts (verified 13 Nov 2026):
# - USDA National Nutrient Database SR28, calcium list hosted by NIH ODS (ods.od.nih.gov/pubs/usdandb/Calcium-Content.pdf):
#   sesame seeds, whole, dried 1 cup 144 g = 1404 mg (= 975 mg / 100 g); milk, whole 3.25 % 1 cup 244 g = 276 mg (= 113 mg / 100 g) -> 8.6x;
#   sesame seed kernels, toasted (decorticated = hulled) 1 cup 128 g = 168 mg (= 131 mg / 100 g). 1 tbsp whole sesame = 9 g = ~88 mg = 32 % of a 276 mg glass.
# - Healthline 'Sesame seeds' (M. McCulloch RD, med. reviewed K. Rose-Francis RDN, 22 May 2026): 'the calcium is mainly in the hull'; oxalates + phytates
#   'reduce the absorption of these minerals'.
# - J. Food Composition and Analysis 17 (2004) 311-320 'In vitro calcium bioavailability of vegetables, legumes and seeds': white + black sesame had LOW
#   calcium dialysability (2-7 %), high oxalate (680-2620 mg / 100 g), linked to limited calcium bioavailability.
# - Bunseki Kagaku 43(2) 151 (1994) 'Extraction of calcium, oxalate and calcium oxalate crystals from sesame seeds': 800 mg total Ca / 100 g, only ~165 mg
#   estimated as nutrient calcium, the rest bound as calcium oxalate.
# - Ujong & Emelike, Applied Food Research 3 (2023) 100267: 'The testa of the seed contains anti-nutrients like oxalate'.
LINES = [
    ("i1", "Do you know sesame has more calcium than milk?", 1.0, 0.25, +1.0, 1.55, ["more", "milk?"], "q"),
    ("i2", "Per hundred grams, whole sesame seeds have over... eight times more. On paper, that's a knockout.", 1.02, 0.3, +1.0, 1.6, ["eight", "knockout."], "low"),
    ("a1", "But most of that calcium sits in the seed's thin skin, and a lot of it is stuck to something called oxalate.", 1.03, 0.1, +0.4, 1.45, ["skin,", "oxalate."], "low"),
    ("a2", "Oxalate locks onto calcium like handcuffs, so your gut can only pull out a small part of it.", 1.0, 0.35, +0.8, 1.5, ["handcuffs,", "small"], "low"),
    ("b1", "And let's be honest, nobody eats a hundred grams of til. You eat a spoonful.", 0.97, 0.25, -0.6, 1.4, ["nobody", "spoonful.:dn"], "low"),
    ("b2", "That spoonful has about a third of the calcium in one glass of milk.", 1.0, 0.35, +0.8, 1.5, ["third"], "low"),
    ("c1", "So til is a lovely bonus. It just isn't a swap for your milk.", 1.0, 0.3, -0.3, 1.4, ["bonus.", "swap"], "low"),
    ("c2", "Send this to the friend who thinks one til luddoo beats a glass of milk.", 1.02, 0.0, +0.8, 1.45, ["luddoo", "beats"], "low"),
]
