# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# FreshNestHub 21 — "Does the fridge make bread go stale faster?" Facts (verified 2 Nov 2026):
# - Stale is not (just) dry: 'Most of us tend to think that bread stales simply because it begins to dry out, but this is far from what is actually
#   happening' (D. Mercer, Food Science, University of Guelph, IUFoST). Sealed bread still goes hard (Eat Your Books summarising D. Gritzer + H. McGee).
# - Baking: starch absorbs water and gelatinises at ~60-65 C; as the loaf cools, the starch realigns / recrystallises (Guelph; Milling MEA, W. Gatama).
# - The crystals 'lock away the crumb's water ... leaving the crumb hard and dry' (America's Test Kitchen, L. Bomze 2023); it feels dry 'even though
#   almost no water has actually left' (ScienceABC).
# - Fridge: 'refrigeration (0-10 C) actually accelerates amylopectin recrystallization' (Milling MEA); 'bread kept in the refrigerator actually stales more
#   quickly' (Guelph); C. Van Buiten, Colorado State, via TODAY: 'Lower temperatures contribute to faster rates of starch crystallization'.
#   ATK: 'a loaf of rustic bread stales within a day - about twice as fast as it does at room temperature'. ScienceABC / others say up to ~6x -> say 'about
#   twice' + 'some say more'.
# - Freezer: ~ -20 C almost halts recrystallisation (Guelph); 'the freezer slows staling significantly' (ATK); wrap tight, up to 3 months (Federation of Bakers FS18).
# - Toasting / oven: 'add enough energy to start the starch crystals moving ... which will soften the bread' (Guelph); microwave 'melts' crystallised starch
#   (Van Buiten / TODAY). Temporary (Milling MEA); 'unstaled' bread 'would turn hard even faster' second time (ScienceABC).
# - Catch: 'refrigeration can delay mold growth, it can also accelerate staling' (Van Buiten / TODAY); 'don't store bread in the refrigerator (except in extremely
#   hot weather)' (Federation of Bakers); store in bread bin / cool dark dry place (FoB).
# - Toast straight from frozen: 'just pop the frozen slices straight into the toaster' (FoB); slice before freezing, no defrost needed (Food Republic).
# SCRIPT upgrade (ep 21): shorter (no padding: the topic needs ~2:20, not 2:50), a sequel hook to ep 20's pebbles; the WHY of the intuition ('cold slows almost
# everything... starch is the weird one'); a three-way guess; a repeatable three-part rule.
LINES = [
    ("i1", "Do you know your fridge makes bread go stale faster than just leaving it on the counter?", 1.00, 0.30, +1.0, 1.45, ["fridge", "faster"], "q"),
    ("i2", "You think you're protecting that loaf in there, but you're actually aging it.", 1.02, 0.35, +0.4, 1.45, ["aging"], "low"),
    ("i3", "And the strangest part is, stale bread isn't even dry.", 1.03, 0.40, -0.3, 1.4, ["isn't"], "low"),
    ("a1", "Everybody thinks stale means dried out. But seal a loaf up so tight that no water can escape, and it still goes hard.", 1.07, 0.30, +0.4, 1.45, ["dried", "still"], "low"),
    ("a2", "So where did the water go? Nowhere. It's still in there, it's just been locked up.", 1.04, 0.35, +0.6, 1.5, ["Nowhere.:dn", "locked"], "low"),
    ("a3", "And if you saw our leftover rice video, you've already met the culprit. It's starch.", 1.04, 0.35, -0.3, 1.4, ["met", "starch.:dn"], "low"),
    ("b1", "When bread bakes, the starch in the flour soaks up water and swells, and that's what makes the inside so soft.", 1.08, 0.28, +0.4, 1.45, ["swells,", "soft."], "low"),
    ("b2", "But the second that loaf starts cooling down, the starch starts squeezing back together, into neat, tight rows, a bit like crystals.", 1.08, 0.28, +0.4, 1.45, ["squeezing", "crystals."], "low"),
    ("b3", "And those rows trap the water inside them. So it's all still there, but the bread feels dry and hard.", 1.07, 0.35, +0.4, 1.45, ["trap", "hard.:dn"], "low"),
    ("b4", "That's what stale really is. Your bread isn't drying out, it's setting.", 1.04, 0.40, +0.6, 1.45, ["stale", "setting.:dn"], "low"),
    ("c1", "So, quick guess: where does that happen fastest? The counter, the freezer, or the fridge?", 1.02, 0.50, +0.8, 1.5, ["guess:", "fastest?"], "q"),
    ("c2", "Yep, it's the fridge. Those crystals grow fastest when it's cold but not frozen, which is exactly where your fridge sits.", 1.06, 0.30, +0.8, 1.5, ["fridge.", "exactly"], "low"),
    ("c3", "One big test kitchen says a rustic loaf goes stale within a day in there. That's about twice as fast as the counter, and some sources say even more.", 1.09, 0.35, +0.4, 1.45, ["day", "twice"], "low"),
    ("c4", "It feels wrong, because cold slows down almost everything in your kitchen. Germs, mould, milk going off. Starch is the weird one.", 1.06, 0.40, -0.3, 1.4, ["wrong,", "weird"], "low"),
    ("d1", "But go colder, way colder, and it flips. In a freezer, the starch can barely move, so staling almost stops.", 1.06, 0.30, +0.6, 1.45, ["flips.", "stops.:dn"], "low"),
    ("d2", "So on the counter it's slow, in the fridge it's fast, and in the freezer it's nearly paused.", 1.05, 0.40, +0.4, 1.45, ["slow,", "fast,", "paused.:dn"], "low"),
    ("e1", "The good news? Stale bread can come back from the dead.", 1.03, 0.30, +0.8, 1.5, ["good", "back"], "low"),
    ("e2", "Toast it, or warm it in the oven, and the heat shakes those tight rows loose, so the inside goes soft again.", 1.07, 0.30, +0.4, 1.45, ["Toast", "soft"], "low"),
    ("e3", "It's a one-time rescue, though. Once it cools, it goes hard even faster than before, so warm it right before you eat it.", 1.07, 0.35, -0.3, 1.35, ["one-time", "faster"], "low"),
    ("f1", "One honest catch. The fridge really does slow down mould, so if it's brutally hot where you live, it isn't the crime I'm making it sound like.", 1.08, 0.30, -0.3, 1.4, ["mould,", "hot"], "low"),
    ("f2", "But your freezer does that job better. Slice the loaf first, wrap it tight, and freeze it.", 1.06, 0.25, +0.4, 1.45, ["freezer", "Slice"], "low"),
    ("f3", "Then just drop the frozen slices straight in the toaster. No thawing needed.", 1.05, 0.40, +0.6, 1.5, ["straight", "needed.:dn"], "low"),
    ("g1", "So remember it like this: counter for now, freezer for later, and the fridge for literally everything else.", 1.04, 0.35, +0.6, 1.45, ["now,", "later,", "else.:dn"], "low"),
    ("g2", "Send this to the friend who keeps their bread right next to the eggs!", 1.04, 0.00, +1.2, 1.5, ["friend", "eggs!"], None),
]
