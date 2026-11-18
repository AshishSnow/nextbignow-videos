# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# TREND + REAL CASE STUDY + HOW TO START — "Would you pay $70 for one bottle of hot sauce?" (Huy Fong Sriracha) — queue/31 (R&D 17 Nov),
# rebuilt 19 Nov 2026 (episode run): DOODLE format, SHORTS LENGTH (target 55-75 s), no music (SFX only), chunked subtitles, big title cover.
# UPGRADE this run: line 1 = "Would you pay $X for ___?" everyday-price hook (Airbnb / Black Friday / Stanley pattern) taken from the story's
# chaos moment (~$70 for a 28 oz bottle on eBay, 2023), then flash back; c5 closes the loop on the same $70 (callback), e1 answers i2 (no ads).
# Story shape (SCRIPT_FEEL): no ads -> so the bottle does the selling -> did it work? 20M bottles -> BUT one farm -> court -> weather -> $70.
# Every number + quote: SOURCES.md. Character: SAUCE BOTTLE (one line) — generic red squeeze bottle, white cap, NO rooster, NO green cap, NO label art.
SERIES = "HOW THEY GOT SO BIG"; PART = 0; EP = 0
CBVOICES = {"b5": "usa_young"}
LINES = [
    ('i1', 'Would you pay seventy dollars for one bottle of hot sauce?', 0.97, 0.25, +0.8, 1.45, ['seventy', 'hot'], None),
    ('i2', "That's what eBay sellers asked in twenty twenty-three.", 0.97, 0.3, +0.8, 1.45, ['eBay', 'twenty-three.'], None),
    ('i3', 'You want to bottle your own? Three moves at the end.', 0.97, 0.3, +0.8, 1.45, ['own?', 'Three'], 'low'),
    ('a1', 'One menu tracker says spicy food is on ninety-five percent of American menus.', 0.97, 0.25, +0.8, 1.45, ['spicy', 'ninety-five'], None),
    ('b1', 'Rewind. David Tran flees Vietnam on a freighter called Huy Fong.', 0.97, 0.25, +0.8, 1.45, ['Vietnam', 'freighter'], None),
    ('b2', 'In Los Angeles, he names his sauce company after that ship.', 0.97, 0.2, +0.8, 1.45, ['Angeles,', 'ship.'], None),
    ('b3', 'He delivers it himself, in a blue van.', 0.97, 0.25, +0.8, 1.45, ['himself,', 'blue'], None),
    ('b4', 'His ad budget? Not a dime.', 0.97, 0.25, +0.8, 1.45, ['budget?', 'dime.'], None),
    ('b5', "Ads? Sweetie, I'm the ad.", 1.0, 0.25, +1.2, 1.5, ["I'm", 'ad.'], None),
    ('b7', 'So, did it work?', 0.95, 0.3, +0.6, 1.4, ['work?'], 'low'),
    ('b8', 'Bloomberg reported it sold twenty million bottles in one year.', 0.97, 0.6, +0.8, 1.45, ['twenty', 'million'], None),
    ('c1', 'But for almost thirty years, most of its peppers come from one farm.', 0.97, 0.25, +0.8, 1.45, ['one', 'farm.'], None),
    ('c2', 'After a split, the two end up in court.', 0.97, 0.2, +0.8, 1.45, ['split,', 'court.'], None),
    ('c3', 'A jury awards the farm over twenty-three million dollars from Huy Fong.', 0.97, 0.25, +0.8, 1.45, ['jury', 'twenty-three'], None),
    ('c4', 'Later, Huy Fong says bad weather hurt its chilies.', 0.97, 0.25, +0.8, 1.45, ['weather', 'chilies.'], None),
    ('c5', 'The result? Bottles get scarce, and one hits seventy dollars online.', 0.97, 0.35, +0.8, 1.45, ['scarce,', 'seventy'], 'low'),
    ('m1', 'Your moves. One: hot sauce usually counts as an acidified food.', 0.97, 0.2, +0.8, 1.45, ['One:', 'acidified'], None),
    ('m1b', "Some states won't let you sell it from a home kitchen. Check yours.", 0.97, 0.25, +0.8, 1.45, ['sell', 'yours.'], None),
    ('m2', 'Two: who signs off on your recipe? A process authority.', 0.97, 0.25, +0.8, 1.45, ['Two:', 'authority.'], None),
    ('m3', 'Three: never lean on one farm. Try a backup supplier.', 0.97, 0.3, +0.8, 1.45, ['Three:', 'backup'], None),
    ('e1', 'Honestly? Seventy bucks, for a sauce that never paid for an ad.', 1.0, 0.3, +0.8, 1.45, ['Seventy', 'never'], 'low'),
    ('z1', 'Send this to the friend who puts hot sauce on everything.', 1.0, 0.25, +0.8, 1.45, ['friend', 'everything.'], None),
    ('z2', 'Mild, or extra hot? Tell me in the comments.', 1.0, 0.0, +0.8, 1.45, ['Mild,', 'hot?'], None),
]
