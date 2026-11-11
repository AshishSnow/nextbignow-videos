# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# FreshNestHub 33 — "Which foods have more vitamin C than an orange?" Facts (verified 11 Nov 2026):
# - Per 100 g, USDA FoodData Central (SR Legacy, raw): orange 53.2 mg, lemon (without peel) 53 mg, papaya 60.9 mg, red sweet pepper 127.7 (128) mg,
#   guava (common) 228.3 mg, hot chili pepper green 242.5 mg (FDC entries via Nutrition Advance 'Top 20 foods high in vitamin C', which links every FDC id;
#   getfoodfacts / nutrientnorms USDA mirrors for 'Peppers, hot chili, green, raw' 170497 and 'Guavas, common, raw' 09139).
#   One guava (55 g) = 125 mg; one medium orange (131 g) = 69.7 mg (same USDA entries).
# - NIH ODS Vitamin C fact sheet (health professional): RDA adults 19+ = men 90 mg, women 75 mg; 'Vitamin C is water soluble and susceptible to heat, so
#   cooking can reduce the vitamin C content of food'; 'may be reduced by prolonged storage and by cooking'; 'Steaming or microwaving may lessen cooking
#   losses'; table: red pepper raw 1/2 cup 95 mg, orange 1 medium 70 mg. Humans can't make vitamin C (ODS: unlike most animals, unable to synthesize it).
# Voice markup (ep 33): "word:up" = CONTINUATION RISE (list intonation: a non-final list item rises across the word, no loudness lift); final item falls.
LINES = [
    ("i1", "Do you know an orange isn't even close to the top for vitamin C?", 1.0, 0.25, +1.0, 1.5, ["close", "C?"], "q"),
    ("i2", "Your body can't make vitamin C, so all of it has to come from food, and everyone thinks orange.", 1.04, 0.25, +0.4, 1.45, ["food,", "orange.:dn"], "low"),
    ("i3", "So let's test it. Six everyday foods, one high jump, and the orange sets the bar.", 1.03, 0.35, +0.8, 1.5, ["jump,", "bar.:dn"], "low"),
    ("a0", "Fair rules first. Every food jumps with the same weight, a hundred grams.", 1.03, 0.25, +0.4, 1.45, ["same"], "low"),
    ("a1", "The orange clears fifty-three milligrams. That's the bar to beat.", 1.0, 0.35, +0.8, 1.5, ["clears", "beat.:dn"], "low"),
    ("a2", "First up, the lemon. It's so sour, it's got to win, right?", 1.0, 0.25, +1.0, 1.55, ["sour,", "right?"], "q"),
    ("a3", "Fifty-three. Exactly the same as the orange. Sour doesn't mean more vitamin C.", 1.0, 0.35, -0.3, 1.4, ["same", "more"], "low"),
    ("b0", "Papaya, sixty-one. Just over the bar. Okay, not bad at all.", 1.02, 0.3, +0.4, 1.45, ["over"], "low"),
    ("b1", "But wait till you see who's next, because it isn't even a fruit.", 0.98, 0.3, +0.8, 1.5, ["next,", "fruit.:dn"], "low"),
    ("b2", "Red capsicum! A hundred and twenty-eight. That's more than double the orange.", 1.0, 0.35, +1.2, 1.6, ["capsicum!", "double"], "low"),
    ("c0", "Then the guava steps up, and it clears two hundred and twenty-eight.", 1.0, 0.25, +0.8, 1.5, ["guava", "clears"], "low"),
    ("c1", "That's more than four times the orange. And one guava weighs about fifty-five grams, so even a single fruit beats a whole orange.", 1.05, 0.3, +0.8, 1.5, ["four", "whole"], "low"),
    ("c2", "So just one guava gives you more vitamin C than most adults need in a whole day.", 1.02, 0.4, +0.4, 1.45, ["day.:dn"], "low"),
    ("d0", "And the gold medal goes to... the green chilli. Two hundred and forty-two!", 0.98, 0.35, +1.2, 1.6, ["chilli.", "gold"], "low"),
    ("d1", "The chilli! But nobody eats a hundred grams of chilli. You eat one or two, just a few grams, so bite for bite, the guava still wins.", 1.05, 0.4, +0.4, 1.45, ["nobody", "guava"], "low"),
    ("e0", "One more twist, and it happens in your kitchen. Vitamin C dissolves in water, and heat breaks it down.", 1.04, 0.25, +0.8, 1.5, ["water,", "heat"], "low"),
    ("e1", "So the longer you boil your vegetables, the more of it ends up in the water, or simply gone.", 1.04, 0.3, +0.4, 1.45, ["longer", "gone.:dn"], "low"),
    ("e2", "Steaming or the microwave loses less. And cut fruit is best eaten fresh, not left sitting for days.", 1.04, 0.35, -0.3, 1.35, ["less.", "fresh,"], "low"),
    ("f0", "So, per hundred grams: orange and lemon, fifty-three, papaya, sixty-one, capsicum, a hundred and twenty-eight, guava, two twenty-eight, and green chilli, two forty-two.", 1.04, 0.35, +0.4, 1.45, ["fifty-three.:up", "sixty-one.:up", "twenty-eight.:up"], "low"),
    ("f1", "Save this for your next trip to the market, and send it to the friend who buys oranges every time they catch a cold.", 1.03, 0.0, +0.8, 1.45, ["Save", "oranges"], "low"),
]
