# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# HOW TO START · EP 3 — "How to start a food truck in New York City" (four steps + the permit line). Written by the R&D writers' room 2 Nov 2026.
# Facts: SOURCES.md. Verified 2 Nov 2026 on the NYC Health Department page + its 13 Mar 2026 release (cap by law, 2,200 supervisory
# license applications a year from 1 Jul 2026 for 5 years, offered to the 2022 waiting lists, daily commissary return, ~5,800 permits,
# no waiting list for the personal vendor license). Checked 1 Nov 2026 by the sourcing run (re-verify at build): fees, DOI 2009, Queens
# Daily Eagle 2025 reported rental prices, Square truck prices. Never promise income; NYC-only (said in i2 + frame-1 card).
# Vendors who rent permits are told as people squeezed by a cap, never as villains; the 2009 DOI case is told as "charged".
# Build run 2 Nov 21:30 UTC: all sources re-read (SOURCES.md): e6 now = DOI headline (six arrests), e7 'at least', new t2 = Restricted Area permit (NYC Health: no waiting list; private property).
# Fresh-eyes review 2 Nov: "not ready" → 9 must-fixes applied (see SOURCES.md). BUILD GATE: re-open the ⚠ sources before rendering.
SERIES = "HOW TO START"; PART = 0; EP = 3
LINES = [
    ("i1", "Why would a New York food vendor pay thousands to rent a two-hundred-dollar permit?", 1.02, 0.40, +1.0, 1.45, ["thousands", "permit?"], None),
    ("i2", "You're in New York City, and you want to sell tacos from a truck.", 1.02, 0.25, +0.8, 1.45, ["New", "tacos"], "low"),
    ("i3", "Get the order wrong, and your truck can't legally serve anyone. So here's the plan in four steps.", 1.02, 0.25, +0.8, 1.45, ["legally", "four"], "low"),
    ("a1", "Step one is you, not the truck.", 1.0, 0.30, +1.0, 1.45, ["you,", "truck.:dn"], "low"),
    ("a2", "Anyone working on a truck needs a mobile food vendor license, and must pass a food safety course.", 1.02, 0.30, +0.8, 1.45, ["license,", "course.:dn"], "low"),
    ("a3", "Good news: there's no waiting list for this one.", 1.02, 0.40, +0.8, 1.45, ["no", "one.:dn"], "low"),
    ("b1", "Step two. Find your commissary.", 1.0, 0.30, +1.0, 1.45, ["two.", "commissary.:dn"], "low"),
    ("b2", "That's the base where your truck is stored, cleaned and serviced.", 1.02, 0.30, +0.8, 1.45, ["stored,", "serviced.:dn"], "low"),
    ("b3", "The rule: the truck goes back there at least once every day.", 1.02, 0.40, +0.8, 1.45, ["back", "day.:dn"], "low"),
    ("c1", "Step three. Price the truck, but don't buy it yet.", 1.0, 0.30, +1.0, 1.45, ["Price", "yet.:dn"], "low"),
    ("c2", "A used one often costs tens of thousands of dollars.", 1.02, 0.30, +0.8, 1.45, ["used", "thousands"], "low"),
    ("c3", "Because step four decides if it ever rolls.", 1.02, 0.40, +0.8, 1.45, ["four", "rolls.:dn"], "low"),
    ("e1", "Step four. The truck permit.", 1.0, 0.30, +1.0, 1.45, ["four.", "permit.:dn"], "low"),
    ("e2", "The truck needs its own permit. And the number of permits is capped by law.", 1.0, 0.30, +0.6, 1.5, ["own", "capped"], "low"),
    ("e3", "The city is still working through waiting lists from twenty twenty-two.", 1.0, 0.35, +0.6, 1.5, ["still", "twenty-two.:dn"], "low"),
    ("e4", "So some vendors quietly rent a permit from a holder, outside the official system.", 1.02, 0.30, +0.6, 1.5, ["rent", "outside"], "low"),
    ("e5", "Vendors told reporters they paid up to twenty-five thousand dollars.", 1.0, 0.30, +0.6, 1.5, ["twenty-five", "thousand"], "low"),
    ("e6", "That's risky. A city undercover probe of black-market permits once led to six arrests.", 1.0, 0.40, +0.6, 1.5, ["risky.", "six"], "low"),
    ("e7", "But since July, the city offers at least twenty-two hundred license applications a year.", 1.04, 0.30, +0.8, 1.45, ["since", "twenty-two"], "low"),
    ("t1", "The twist? They only go to those lists. Not on one? Try working a truck first.", 1.04, 0.25, +0.8, 1.45, ["twist?", "first.:dn"], "low"),
    ("t2", "Or stay on private property. That permit has no waiting list.", 1.04, 0.25, +0.8, 1.45, ["private", "no"], "low"),
    ("z1", "Save this before you start. Still New York? Comment: STAY or MOVE?", 1.04, 0.25, +1.0, 1.45, ["Save", "MOVE?"], None),
    ("z2", "Send this to the friend who wants a truck.", 1.06, 0.0, +1.0, 1.45, ["friend", "truck."], None),
]
