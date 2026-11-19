# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# TREND + REAL CASE STUDY + HOW TO START — "Too broke for a Christmas gift" (Yankee Candle) — written 19 Nov 2026 (R&D writers' room),
# DOODLE format, SHORTS LENGTH (target 55-75 s, ~190 words), no music (SFX only), chunked subtitles, big title cover on frame 0.
# SEASONAL: post late Nov - mid Dec (holiday candle season).
# Trend: ~35 % of US candle sales happen in the Christmas/holiday season (National Candle Association; NPR 25 Dec 2025 "more than a third").
# Story: Christmas 1969, South Hadley MA, Mike Kittredge, 16, too broke for a present, melts crayons into a candle for his mom; a neighbor
# wants it; he sells it and buys wax for two candles, one for mom, one to sell (company timeline + Greenfield Recorder 26 Jul 2019 + AJC 2019);
# 1973 the crew moves into an old Holyoke paper mill; 1998 sells ~90 % for ~$500M (Recorder + FundingUniverse); Sep 2013 Jarden buys it
# for ~$1.75B (Jarden 8-K + Reuters) — from Madison Dearborn, NOT from Kittredge. Catch: Dec 2025 owner Newell says ~20 Yankee Candle
# stores will close (Scripps 2 Dec 2025 + Daily Hampshire Gazette 8 Jan 2026).
# Moves: lead-cored wicks banned (CPSC, Oct 2003); ASTM F2058 fire-safety label; small batch + state seller's permit; no crayons (clog wicks).
# Every number + quote: SOURCES.md. Character: CANDLE (one line) — generic jar candle, NO Yankee Candle jar shape/label/lid, NO logo.
SERIES = "HOW THEY GOT SO BIG"; PART = 0; EP = 0   # build run takes the next free number
CBVOICES = {"b5": "usa_young"}
LINES = [
    ('i1', "You're sixteen, and too broke to buy Mom a Christmas present. Now what?", 0.97, 0.25, +0.8, 1.45, ['sixteen,', 'broke'], None),
    ('i2', 'One kid melted crayons. Your three moves are at the end.', 0.97, 0.3, +0.8, 1.45, ['crayons.', 'three'], 'low'),
    ('a1', "Here's the timing: about a third of candle sales happen over the holidays.", 0.97, 0.25, +0.8, 1.45, ['third', 'holidays.'], None),
    ('b1', 'Meet Mike Kittredge. Massachusetts, nineteen sixty-nine.', 0.97, 0.25, +0.8, 1.45, ['Kittredge.', 'sixty-nine.'], None),
    ('b2', 'He melts crayons on the stove and pours Mom a candle.', 0.97, 0.25, +0.8, 1.45, ['crayons', 'candle.'], None),
    ('b3', 'Then a neighbor sees it, and she wants it.', 0.97, 0.25, +0.8, 1.45, ['neighbor', 'wants'], None),
    ('b4', "The surprising move? He sells Mom's present.", 0.97, 0.25, +0.8, 1.45, ['sells', 'present.'], None),
    ('b5', 'Relax. Mom still gets a candle.', 1.0, 0.25, +1.2, 1.5, ['Relax.', 'still'], None),
    ('b6', 'That cash buys wax for two. One for Mom, one to sell.', 0.97, 0.3, +0.8, 1.45, ['two.', 'sell.'], 'low'),
    ('b7', "Soon there's a crew, an old mill, and a name: Yankee Candle.", 0.97, 0.25, +0.8, 1.45, ['mill,', 'Yankee'], None),
    ('c1', 'Did it work? He sells most of it in nineteen ninety-eight.', 0.97, 0.25, +0.8, 1.45, ['work?', 'most'], None),
    ('c2', 'The price? About five hundred million dollars.', 0.97, 0.25, +0.8, 1.45, ['five', 'million'], None),
    ('c3', 'Later, a new owner pays one point seven five billion. Not to Mike.', 0.97, 0.25, +0.8, 1.45, ['billion.', 'Mike.'], None),
    ('c4', 'The catch? Owner Newell announced about twenty store closures.', 0.97, 0.3, +0.8, 1.45, ['catch?', 'twenty'], 'low'),
    ('m1', 'Your moves. One: lead-free wicks only, since America banned lead-core wicks.', 0.97, 0.25, +0.8, 1.45, ['lead-free', 'banned'], None),
    ('m2', 'Two: a fire-safety label. Burn within sight, away from kids.', 0.97, 0.25, +0.8, 1.45, ['Two:', 'label.'], None),
    ('m3', "Three: test a small batch at a craft fair. Get a seller's permit.", 0.97, 0.25, +0.8, 1.45, ['small', 'permit.'], None),
    ('m4', 'And skip crayons. Try real candle dye; suppliers say crayons can clog wicks.', 0.97, 0.3, +0.8, 1.45, ['skip', 'clog'], 'low'),
    ('e1', 'So, too broke for a Christmas present?', 0.97, 0.25, +0.8, 1.45, ['broke'], None),
    ('e2', "Funny. That's exactly how this one started.", 1.0, 0.3, +0.8, 1.45, ['exactly', 'started.'], 'low'),
    ('z1', 'Send this to the friend who buys a candle every December.', 1.0, 0.25, +0.8, 1.45, ['friend', 'December.'], None),
    ('z2', 'Pine, or gingerbread? Tell me in the comments.', 1.0, 0.0, +0.8, 1.45, ['Pine,', 'gingerbread?'], None),
]
