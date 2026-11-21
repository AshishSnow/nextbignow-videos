# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# TREND + REAL CASE STUDY + HOW TO START — "Nike said no, so he sold pickles from a cart" (Grillo's Pickles) — written 21 Nov 2026
# (R&D writers' room), DOODLE format, SHORTS LENGTH (target 55-75 s), no music (SFX only), chunked subtitles, big title cover on frame 0.
# Trend: pickle-flavored snacks +30 % in a year vs +3.8 % for all snacks (Circana via WSJ 24 Aug 2026 + Fox News 21 Sep 2026 — one
# Circana number, two outlets); Pabst x Grillo's pickle beer (Apr/May 2026) + Smoothie King pickle smoothie (May 2026).
# Story: Travis Grillo, rejected for a Nike shoe-design job; summer 2008 sells his grandfather's ~100-year-old recipe on Boston Common,
# two spears for $1, from a wooden cart; packs them in a produce warehouse; the move: cold, never a shelf jar — "made cold, shipped cold,
# sold cold", a plastic tub that stores put wherever their fridges are (produce, even the meat section); buyers push cheaper garlic/herbs,
# he refuses ("I kept my eye on quality."); ~7,000 stores mid-2019; King's Hawaiian buys it 2021 (terms undisclosed); $54M Indiana plant
# 2026. Moves: FDA acidified-foods rule (21 CFR 114) for shelf-stable jars — refrigerated pickles excluded; cottage food laws differ
# (Texas allows pickles pH <= 4.6, Michigan bans); licensed kitchen + cart/market stall + local permit.
# Every number + quote: SOURCES.md. Character: PICKLE (one line, attitude only) — generic dill spear, NO Grillo's tub art/logo, NO Nike swoosh.
SERIES = "HOW THEY GOT SO BIG"; PART = 0; EP = 0   # build run takes the next free number
CBVOICES = {"b4": "usa_young"}
LINES = [
    ('i1', 'Nike turned down his dream job. Guess what he sold instead?', 0.97, 0.25, +0.8, 1.45, ['Nike', 'instead?'], None),
    ('i2', 'Pickles, from a cart. Your three moves are at the end.', 0.97, 0.3, +0.8, 1.45, ['Pickles,', 'three'], 'low'),
    ('a1', 'You want proof pickles are hot? Pickle chips, beer, even smoothies.', 0.97, 0.25, +0.8, 1.45, ['proof', 'smoothies.'], None),
    ('a2', 'Circana says pickle snacks grew about thirty percent in a year.', 0.97, 0.3, +0.8, 1.45, ['thirty', 'year.'], 'low'),
    ('b1', 'Boston, two thousand eight. Meet Travis Grillo.', 0.97, 0.25, +0.8, 1.45, ['Boston,', 'Grillo.'], None),
    ('b2', "So he grabs grandpa's recipe, about a hundred years old.", 0.97, 0.25, +0.8, 1.45, ["grandpa's", 'hundred'], None),
    ('b3', 'Two spears for a dollar, from a cart on Boston Common.', 0.97, 0.3, +0.8, 1.45, ['Two', 'dollar,'], 'low'),
    ('b4', 'Shelf? Not for me.', 1.0, 0.25, +1.2, 1.5, ['Shelf?', 'Not'], None),
    ('c1', 'The surprising move? Skip the pickle aisle and stay cold.', 0.97, 0.25, +0.8, 1.45, ['aisle', 'cold.'], None),
    ('c2', 'Target puts the tub in produce. Kroger, right by the meat.', 0.97, 0.3, +0.8, 1.45, ['produce.', 'meat.'], 'low'),
    ('d1', "Then buyers push him: use garlic oil, it's cheaper.", 0.97, 0.25, +0.8, 1.45, ['oil,', 'cheaper.'], None),
    ('d2', 'His answer: "I kept my eye on quality." Good call.', 1.0, 0.3, +0.8, 1.45, ['quality."', 'Good'], 'low'),
    ('e1', 'Did it work? Later, about seven thousand stores carry it.', 0.97, 0.25, +0.8, 1.45, ['work?', 'seven'], None),
    ('e2', "Then King's Hawaiian buys it, for a price nobody shared.", 0.97, 0.3, +0.8, 1.45, ['buys', 'nobody'], 'low'),
    ('m1', 'Your moves. One: shelf-stable jars count as acidified foods to the FDA.', 0.97, 0.25, +0.8, 1.45, ['shelf-stable', 'acidified'], None),
    ('m2', 'Register, and file your process before you pack. Fridge pickles skip that.', 0.97, 0.25, +0.8, 1.45, ['file', 'skip'], None),
    ('m3', "Two: a home kitchen? Texas lets you sell pickles from one, Michigan doesn't.", 0.97, 0.25, +0.8, 1.45, ['home', "doesn't."], None),
    ('m4', 'Three: rent a licensed kitchen, then try a cart or a market stall.', 0.97, 0.3, +0.8, 1.45, ['market', 'licensed'], 'low'),
    ('f1', 'And the Nike dream? He later joked he owns a sneaker line.', 0.97, 0.25, +0.8, 1.45, ['Nike', 'sneaker'], None),
    ('f2', "It's got pickles on it.", 1.0, 0.6, +0.8, 1.45, ['pickles'], 'low'),
    ('z1', 'Send this to the friend who puts pickles on everything.', 1.0, 0.25, +0.8, 1.45, ['friend', 'everything.'], None),
    ('z2', 'Pickle chips, or pickle beer? Tell me in the comments.', 1.0, 0.0, +0.8, 1.45, ['chips,', 'beer?'], None),
]
