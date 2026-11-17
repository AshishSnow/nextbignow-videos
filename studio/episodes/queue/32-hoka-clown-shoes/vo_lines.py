# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# TREND + REAL CASE STUDY + HOW TO START — "People called them clown shoes. Now: $2.6B a year" (Hoka) — written 17 Nov 2026 (R&D writers' room),
# DOODLE format, SHORTS LENGTH (target 55-75 s, ~190 words), no music (SFX only), chunked subtitles, big title cover on frame 0.
# Trend: running clubs on Strava grew 3.5x in 2025 (Strava Year in Sport, 3 Dec 2025); London Marathon 2026 ballot world record 1,133,813.
# Story: two ex-Salomon Frenchmen (Mermoud + Diard) launch Hoka 2009; oversized sole built for downhill speed, during the barefoot/minimalist craze;
# ultrarunner Karl Meltzer: "People thought they looked like clown shoes, but I didn't care." (Outside, 3 Dec 2013); ultrarunners = first adopters (Diard);
# under $3M sales in 2012; Deckers buys it (minority May 2012, rest Sep 2012, price undisclosed); Hoka FY26 (to Mar 2026) net sales $2.587B.
# Catch: May 2025 slower Hoka growth + pulled guidance → DECK opened down >23 %.
# Moves: weekly run club; permits for big groups (Hudson River Park: 20+ people) + event insurance (Seattle: required for all runs); niche first.
# Every number + quote: SOURCES.md. Character: CHUNKY SHOE (one line) — generic thick-soled sneaker, NO Hoka logo/swoosh shapes/colourways.
SERIES = "HOW THEY GOT SO BIG"; PART = 0; EP = 0   # build run takes the next free number
CBVOICES = {"b4": "usa_young"}
LINES = [
    ('i1', 'Would you wear running shoes people called clown shoes?', 0.97, 0.25, +0.8, 1.45, ['clown'], None),
    ('i2', 'This brand now sells billions of dollars a year.', 0.97, 0.25, +0.8, 1.45, ['billions'], None),
    ('i3', 'You want in on the running boom? Three moves at the end.', 0.97, 0.3, +0.8, 1.45, ['running', 'Three'], 'low'),
    ('a1', "Strava's app saw running clubs grow three and a half times last year.", 0.97, 0.25, +0.8, 1.45, ['clubs', 'half'], None),
    ('b1', 'Rewind to France. Two guys who used to work at Salomon start Hoka.', 0.97, 0.25, +0.8, 1.45, ['France.', 'Hoka.'], None),
    ('b2', 'Their idea? A huge, soft sole, built to fly downhill.', 0.97, 0.25, +0.8, 1.45, ['huge,', 'downhill.'], None),
    ('b3', 'The odd timing? Thin, barefoot-style shoes were the big craze.', 0.97, 0.25, +0.8, 1.45, ['Thin,', 'craze.'], None),
    ('b4', "Clown shoes? I prefer bold.", 1.0, 0.25, +1.2, 1.5, ['bold.'], None),
    ('b5', 'One ultrarunner told Outside magazine: people thought they looked like clown shoes.', 0.97, 0.15, +0.8, 1.45, ['ultrarunner', 'clown'], None),
    ('b6', "But I didn't care.", 0.97, 0.25, +0.8, 1.45, ["didn't"], None),
    ('b7', 'Hoka says ultrarunners were its first fans.', 0.97, 0.3, +0.8, 1.45, ['first'], 'low'),
    ('c1', 'Still tiny in twenty twelve. Under three million dollars in sales.', 0.97, 0.2, +0.8, 1.45, ['tiny', 'three'], None),
    ('c2', 'Then Deckers, the Ugg boots company, buys it, for an undisclosed price.', 0.97, 0.3, +0.8, 1.45, ['buys', 'undisclosed'], None),
    ('c3', 'Did it work? Last fiscal year, Hoka sold about two point six billion dollars.', 0.97, 0.2, +0.8, 1.45, ['work?', 'six'], None),
    ('c4', "That's about seven million dollars. Every single day.", 0.97, 0.3, +0.8, 1.45, ['seven', 'day.'], 'low'),
    ('m1', 'Your moves. One: start a weekly run club, and see who keeps coming back.', 0.97, 0.15, +0.8, 1.45, ['One:', 'back.'], None),
    ('m2', 'Two: going big? Some city parks want a permit and insurance.', 0.97, 0.2, +0.8, 1.45, ['Two:', 'permit'], None),
    ('m3', 'Three: win one hard-core crowd first. Look at Hoka and its ultrarunners.', 0.97, 0.3, +0.8, 1.45, ['Three:', 'ultrarunners.'], None),
    ('e1', 'Clown shoes, they said.', 0.97, 0.15, +0.8, 1.45, ['Clown'], None),
    ('e2', 'Honestly? The clowns got the last laugh.', 1.0, 0.3, +0.8, 1.45, ['last', 'laugh.'], 'low'),
    ('z1', 'Send this to the friend who just joined a run club.', 1.0, 0.25, +0.8, 1.45, ['friend', 'club.'], None),
    ('z2', 'Thick soles, or thin? Tell me in the comments.', 1.0, 0.0, +0.8, 1.45, ['Thick', 'thin?'], None),
]
