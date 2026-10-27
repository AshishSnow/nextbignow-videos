# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# "Your gas station barely makes money on gas" — Casey's Q4 + FY2026 results 8-K (Jun 9 2026), NACS State of the Industry 2025 (Apr 2026),
# Fortune (Aug 29 2026: Casey's = 5th-largest US pizza chain by prepared food & beverage sales, BofA; confirmed by Casey's)
LINES = [
    ("i1", "Do you know your gas station barely makes any money… on gas?", 1.04, 0.35, +1.0, 1.45, ["barely", "gas?"], "q"),
    ("i2", "Casey's, with almost three thousand stations, earns about forty three cents on a gallon.", 1.04, 0.25, +0.6, 1.45, ["forty", "gallon.:dn"], "low"),
    ("a1", "Fill a fifteen gallon tank, and that's about six bucks.", 1.04, 0.40, +0.8, 1.45, ["fifteen", "six"], "low"),
    ("a2", "So where's the real money? Look past the pump.", 1.02, 0.30, +1.0, 1.45, ["real", "past"], None),
    ("a3", "Last year, Casey's sold ten point six billion dollars of gas… and six point three billion inside the store.", 1.06, 0.25, +0.8, 1.45, ["ten", "inside"], None),
    ("a4", "But the store made almost twice the profit.", 1.02, 0.45, +1.0, 1.5, ["store", "twice"], "low"),
    ("b1", "Here's why. On gas, it keeps about fourteen cents of every dollar.", 1.04, 0.2, +0.8, 1.45, ["why.", "fourteen"], "low"),
    ("b2", "Inside the store? Forty two cents.", 1.02, 0.25, +1.0, 1.5, ["store?", "two"], None),
    ("b3", "And on fresh food, like pizza and fountain drinks, about fifty nine cents!", 1.04, 0.40, +1.2, 1.5, ["pizza", "fifty"], None),
    ("c1", "That's how a gas station chain became America's fifth biggest pizza chain.", 1.04, 0.40, +0.8, 1.45, ["fifth", "pizza"], "low"),
    ("c2", "But the sneakiest part? The giant price sign.", 1.02, 0.25, +1.0, 1.5, ["sneakiest", "sign."], None),
    ("c3", "Cheap gas pulls you in. The snacks do the rest.", 1.04, 0.30, +0.8, 1.45, ["in.", "rest.:dn"], "low"),
    ("d1", "Across the whole industry last year, gas was sixty five percent of sales… but under forty percent of the profit.", 1.06, 0.35, +0.8, 1.45, ["whole", "under"], "low"),
    ("d2", "So if you only need gas, pay at the pump. Every step inside is part of the plan.", 1.04, 0.30, +0.8, 1.45, ["only", "pump."], None),
    ("e1", "Your gas station isn't really a gas station. It's a snack shop… with a giant price sign.", 1.02, 0.35, +0.6, 1.45, ["snack", "sign.:dn"], "low"),
    ("e2", "Send this to the friend who never leaves a gas station without snacks!", 1.06, 0.0, +1.0, 1.45, ["friend", "never"], None),
]
