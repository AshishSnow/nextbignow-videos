# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# TREND + REAL CASE STUDY + HOW TO START — "The hot sauce that never paid for an ad" (Huy Fong Sriracha) — written 17 Nov 2026 (R&D writers' room),
# DOODLE format, SHORTS LENGTH (target 55-75 s, ~180 words), no music (SFX only), chunked subtitles, big title cover on frame 0.
# Trend: spicy food on 95.3 % of US restaurant menus (Datassential, Aug 2025, up from 91.6 % in 2015).
# Story: David Tran leaves Vietnam on the freighter Huy Fong, ends up in Boston, then LA; starts Huy Fong Foods 1980, delivers from a blue van;
# "didn't spend a dime" on ads; "rich man's sauce at a poor man's price"; 20 million bottles in 2012 (Bloomberg). Chaos: pepper grower Underwood
# Ranches (supplier 1988-2017) wins a $23.3M jury verdict (Jul 2019, affirmed 2021); 2022 chili shortage (Huy Fong letter: weather); ~$70 a bottle on eBay (2023).
# Moves: hot sauce = acidified food (21 CFR 114/108); some states ban it from home kitchens (Connecticut names hot sauce); process authority +
# Better Process Control School or a co-packer; a backup supplier.
# Every number + quote: SOURCES.md. Character: SAUCE BOTTLE (one line) — generic squeeze bottle, NO rooster, NO green cap, NO Huy Fong label art.
SERIES = "HOW THEY GOT SO BIG"; PART = 0; EP = 0   # build run takes the next free number
CBVOICES = {"b5": "usa_young"}
LINES = [
    ('i1', 'Can a hot sauce get famous without paying for ads?', 0.97, 0.25, +0.8, 1.45, ['famous', 'ads?'], None),
    ('i2', 'You want to bottle your own? Three moves at the end.', 0.97, 0.3, +0.8, 1.45, ['own?', 'Three'], 'low'),
    ('a1', 'Datassential says spicy food is on ninety-five percent of American restaurant menus.', 0.97, 0.25, +0.8, 1.45, ['spicy', 'ninety-five'], None),
    ('b1', 'David Tran flees Vietnam on a freighter, and ends up in Los Angeles.', 0.97, 0.25, +0.8, 1.45, ['freighter,', 'Angeles.'], None),
    ('b2', 'He delivers his chili sauce from a blue van.', 0.97, 0.25, +0.8, 1.45, ['chili', 'van.'], None),
    ('b3', 'He names the company after that freighter: Huy Fong.', 0.97, 0.25, +0.8, 1.45, ['freighter:', 'Fong.'], None),
    ('b4', 'The surprising move? Not a dime on ads.', 0.97, 0.25, +0.8, 1.45, ['surprising', 'dime'], None),
    ('b5', "Ads? Sweetie, I'm the ad.", 1.0, 0.25, +1.2, 1.5, ["I'm", 'ad.'], None),
    ('b6', "His line: a rich man's sauce at a poor man's price.", 0.97, 0.25, +0.8, 1.45, ['rich', 'poor'], None),
    ('b7', 'Did it work? Huy Fong told Bloomberg: twenty million bottles in a year.', 0.97, 0.3, +0.8, 1.45, ['twenty', 'million'], 'low'),
    ('c1', 'The low point? A fight with its only pepper supplier.', 0.97, 0.25, +0.8, 1.45, ['low', 'only'], None),
    ('c2', 'A jury orders Huy Fong to pay that farm over twenty-three million dollars.', 0.97, 0.25, +0.8, 1.45, ['jury', 'twenty-three'], None),
    ('c3', 'Later, Huy Fong blames bad weather for a chili shortage.', 0.97, 0.25, +0.8, 1.45, ['weather', 'shortage.'], None),
    ('c4', 'One big bottle on eBay? About seventy dollars.', 0.97, 0.3, +0.8, 1.45, ['seventy'], 'low'),
    ('m1', 'Your moves. One: hot sauce usually counts as an acidified food.', 0.97, 0.25, +0.8, 1.45, ['One:', 'acidified'], None),
    ('m1b', "Some states won't let you sell it from a home kitchen. Check yours.", 0.97, 0.25, +0.8, 1.45, ['sell', 'yours.'], None),
    ('m2', 'Two: a process authority must approve your recipe. A co-packer can handle that.', 0.97, 0.25, +0.8, 1.45, ['Two:', 'co-packer.'], None),
    ('m3', 'Three: never rely on one farm. Try two suppliers.', 0.97, 0.25, +0.8, 1.45, ['Three:', 'two'], None),
    ('e1', 'So, famous without paying for ads?', 0.97, 0.25, +0.8, 1.45, ['without'], None),
    ('e2', 'Honestly? It started in a blue van.', 1.0, 0.3, +0.8, 1.45, ['blue', 'van.'], 'low'),
    ('z1', 'Send this to the friend who puts hot sauce on everything.', 1.0, 0.25, +0.8, 1.45, ['friend', 'everything.'], None),
    ('z2', 'Mild, or extra hot? Tell me in the comments.', 1.0, 0.0, +0.8, 1.45, ['Mild,', 'hot?'], None),
]
