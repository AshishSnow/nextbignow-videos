# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# TREND + REAL CASE STUDY + HOW TO START — "$900 and a parking lot" (Dave's Hot Chicken) — written 21 Nov 2026 (R&D writers' room),
# DOODLE format, SHORTS LENGTH (target 55-75 s), no music (SFX only), chunked subtitles, big title cover on frame 0.
# Trend: US chicken chains +5.3 % sales in 2025 vs ~3 % for all restaurants; slowing from 9.1 % in 2024 (Technomic via NRN 4 May 2026 +
# Restaurant Business Top 500 2026).
# Story: 2017, an East Hollywood parking lot; Dave Kopushyan (cooked in Michelin-starred kitchens; "I don't even like chicken"), Arman
# Oganesyan, Tommy Rubenyan (+ Gary later) pool ~$900 for a fryer + heat lamp + borrowed tables; no permits at first (LAist quote + Fortune);
# first night $40 from four meals; lines around the block; first store 2018; heat levels up to 'Reaper' with a signed waiver; 2019 Bill
# Phelps group + franchising; Jun 2025 Roark majority stake at a reported ~$1B (terms undisclosed). Catch: chicken growth slowing.
# Moves: county temporary food / community-event permit (LA County); trademark clearance search (USPTO); franchise buyers get the FDD
# >= 14 days before signing (FTC). Every number + quote: SOURCES.md.
# Character: TENDER (one line, attitude only) — generic chicken tender with a sweat drop, NO Dave's logo/box/colors, no founder likeness.
SERIES = "HOW THEY GOT SO BIG"; PART = 0; EP = 0   # build run takes the next free number
CBVOICES = {"c3": "usa_young"}
LINES = [
    ('i1', "You've got nine hundred dollars and some friends. Want to open a restaurant?", 0.97, 0.25, +0.8, 1.45, ['nine', 'restaurant?'], None),
    ('i2', 'One crew did, in a parking lot. Three moves at the end.', 0.97, 0.3, +0.8, 1.45, ['crew', 'parking'], 'low'),
    ('a1', "Chicken's hot, too. Technomic says chicken chains grew about five percent.", 0.97, 0.25, +0.8, 1.45, ['hot,', 'five'], None),
    ('a2', 'Big chains overall? About three.', 0.97, 0.3, +0.8, 1.45, ['overall?', 'three.'], 'low'),
    ('b1', 'Los Angeles, twenty seventeen. Dave Kopushyan had cooked in Michelin-starred kitchens.', 0.97, 0.25, +0.8, 1.45, ['seventeen.', 'Michelin-starred'], None),
    ('b2', 'Odd part? A friend recalls Dave saying, "I don\'t even like chicken."', 0.97, 0.25, +0.8, 1.45, ['Odd', 'chicken."'], None),
    ('b3', 'The friends pool nine hundred bucks.', 0.97, 0.25, +0.8, 1.45, ['pool', 'nine'], None),
    ('b4', 'A fryer, a heat lamp, and tables from their parents.', 0.97, 0.3, +0.8, 1.45, ['fryer,', 'parents.'], 'low'),
    ('b5', "No permits either, so don't copy that part.", 0.97, 0.25, +0.8, 1.45, ['permits', 'copy'], None),
    ('c1', 'Opening night: forty dollars. Four meals, all to friends.', 0.97, 0.3, +0.8, 1.45, ['forty', 'Four'], 'low'),
    ('c2', 'The surprising move? One item only: a hot chicken plate.', 0.97, 0.25, +0.8, 1.45, ['One', 'plate.'], None),
    ('c3', 'Hottest level today? Sign a waiver first.', 1.0, 0.3, +1.2, 1.5, ['Hottest', 'waiver'], 'low'),
    ('d1', 'Did it work? Soon the line wraps around the block.', 0.97, 0.25, +0.8, 1.45, ['work?', 'block.'], None),
    ('d2', 'A real store opens the next year. Franchises follow.', 0.97, 0.3, +0.8, 1.45, ['store', 'Franchises'], 'low'),
    ('e1', 'In twenty twenty-five, Roark buys a majority stake.', 0.97, 0.25, +0.8, 1.45, ['Roark', 'majority'], None),
    ('e2', "The deal's value? Pretty close to a billion, says its CEO.", 0.97, 0.6, +0.8, 1.45, ['Pretty', 'billion,'], 'low'),
    ('e3', "The catch? Chicken's growth is cooling down.", 0.97, 0.3, +0.8, 1.45, ['catch?', 'cooling.'], 'low'),
    ('m1', 'Your moves. One: even a pop-up needs a local health permit.', 0.97, 0.25, +0.8, 1.45, ['pop-up', 'local'], None),
    ('m2', 'Two: search the name before you paint the sign.', 0.97, 0.25, +0.8, 1.45, ['search', 'sign.'], None),
    ('m3', 'Three: buying a franchise? Read its disclosure papers, due two weeks before you sign.', 0.97, 0.25, +0.8, 1.45, ['Read', 'two'], None),
    ('f1', "Not bad for a chef who didn't even like chicken.", 1.0, 0.5, +0.8, 1.45, ['bad', 'chicken.'], 'low'),
    ('z1', 'Send this to the friend who orders the hottest level.', 1.0, 0.25, +0.8, 1.45, ['friend', 'hottest'], None),
    ('z2', 'Mild, or Reaper? Tell me in the comments.', 1.0, 0.0, +0.8, 1.45, ['Mild,', 'Reaper?'], None),
]
