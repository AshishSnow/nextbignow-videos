# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# FreshNestHub 19 — "Why do cut apples turn brown?" (cutting breaks the apple's cells; an enzyme, polyphenol oxidase (PPO), that was kept
# apart from the apple's polyphenols meets them + oxygen from the air and turns them into brown MELANINS — the same family of pigment
# that colours human skin, hair and eyes (UW-Madison 2008, R. Hartel; Science News Explores / Science Buddies 2025; Britannica; Scientific
# American, L. McLandsborough: PPO + oxygen + phenolic compounds, 'not unique to apples', used on purpose in tea, coffee, cocoa).
# Believed to be a plant defence against pests and pathogens (UW-Madison). Browning is harmless, the fruit only loses its crisp texture
# (University of Illinois Extension 2020; SN Explores: 'does not make the food harmful to eat'). Fixes: lemon / other acidic juice — the
# lower pH makes PPO less active (Sci Am) and the vitamin C does more than the acid (Illinois: citric acid alone is not a good substitute
# for ascorbic acid; Penn State: lemon juice / citric acid less effective than ascorbic acid; Illinois: 3 tbsp lemon juice in 1 quart
# water, soak 3-5 min); honey water (UNL: 2 tbsp honey in 1 cup water; Illinois honey dip); cold slows the enzyme (SN Explores:
# enzymes stop working when too cold or too warm); heat destroys it (Sci Am: 4-5 min blanching nearly eliminates PPO; Penn State:
# cooking apples before sauce destroys the enzymes). Same reaction in avocados and potatoes (UW-Madison), bananas (SN Explores), and
# used on purpose for tea, coffee and cocoa (Sci Am), raisins, prunes and cider colour (UW-Madison). The Arctic apple: Okanagan
# Specialty Fruits switched the PPO gene off by gene silencing, two varieties approved by the USDA in 2015 (Medill Reports, Feb 2015;
# SN Explores: 'modified so that it no longer produces the PPO enzyme').)
# SCRIPT upgrade (ep 19): a GUESS beat ('Quick guess...') that asks the viewer to predict before the answer (prediction = attention +
# comments), a tan metaphor paid off twice (hook + 'same family'), a three-rule fix map (starve / slow / switch off) so every fix has a
# reason, two re-hooks (the guess at ~40 %, 'on purpose' at ~70 %), a joke per 30 s, and no filler openers.
# VOICE upgrade (ep 19): COMIC-TIMING PAUSES — pause_after is set per beat instead of a flat 0.4: 0.55 s after a joke / reveal / the guess
# (let it land), 0.25 s before a continuation ('And...'), 0.3-0.4 for plain explanation. Registers per beat kept from ep 17 (asides -0.6 st
# + 0.95, reveals +1.2, explanations +0.4) and drop-stress ':dn' from ep 18 on deadpan payoffs.
LINES = [
    ("i1", "Do you know a cut apple goes brown for the same reason you get a tan?", 0.98, 0.35, +1.0, 1.45, ["brown", "tan?"], "q"),
    ("i2", "Yeah. That brown on the slice is melanin, the same stuff that colours your skin, your hair, your eyes.", 1.04, 0.40, +0.8, 1.5, ["melanin,", "same"], None),
    ("i3", "Stick around for the dip that keeps a lunchbox apple white till lunchtime.", 1.06, 0.35, +0.6, 1.5, ["dip", "lunchtime."], None),
    ("a1", "So, an apple. Inside, millions of tiny cells, like little rooms with walls.", 1.09, 0.28, +0.4, 1.45, ["millions", "rooms"], "low"),
    ("a2", "In every room, two things are kept apart. In one corner, an enzyme called PPO: a tiny machine with one job.", 1.09, 0.28, +0.4, 1.45, ["apart.", "machine"], "low"),
    ("a3", "In the other corner, polyphenols. The apple's own flavour chemicals. Fine, as long as the two never meet.", 1.08, 0.30, +0.4, 1.45, ["polyphenols.", "never"], "low"),
    ("b1", "Then you cut it. The knife smashes through thousands of walls at once. And PPO meets the polyphenols.", 1.07, 0.25, +0.6, 1.5, ["smashes", "meets"], "low"),
    ("b2", "And then the third guest comes in from the air, and that guest is oxygen.", 1.04, 0.35, +0.8, 1.5, ["third", "oxygen."], "low"),
    ("b3", "PPO grabs the oxygen and the polyphenols and mashes them together. At first the result is colourless.", 1.09, 0.25, +0.4, 1.45, ["mashes", "colourless."], "low"),
    ("b4", "Then those bits clump into bigger and bigger blobs. And the blobs are brown. That's melanin.", 1.04, 0.40, +0.8, 1.5, ["clump", "melanin.:dn"], "low"),
    ("c1", "Same family of pigment your skin makes in the sun. The apple just does it a lot faster.", 1.04, 0.40, +0.6, 1.5, ["Same", "faster."], "low"),
    ("c2", "Why would an apple do that? Scientists think it's a defence against bugs and germs getting in at the cut.", 1.08, 0.30, +0.4, 1.45, ["defence", "cut."], "low"),
    ("c3", "Quick guess, then: is the brown bit actually going bad?", 1.01, 0.40, +0.6, 1.5, ["guess,", "bad?"], "q"),
    ("c4", "Nope. It's harmless. Same apple, same taste. It just goes a bit soft and looks sad.", 1.07, 0.40, -0.6, 1.4, ["Nope.", "sad.:dn"], "low"),
    ("d1", "Okay, the fixes. Every trick does one of three things: keeps oxygen out, slows the enzyme, or switches it off.", 1.08, 0.28, +0.6, 1.45, ["three", "switches"], "low"),
    ("d2", "Lemon juice, the classic. The acid makes PPO sluggish, and the vitamin C helps even more. A few minutes in there, done.", 1.08, 0.30, +0.4, 1.45, ["sluggish,", "minutes"], "low"),
    ("d3", "No lemon? Honey water. Two spoons of honey in a cup of water, dunk the slices. The sugar coat keeps oxygen off.", 1.09, 0.30, +0.4, 1.45, ["Honey", "coat"], "low"),
    ("d4", "Cold slows the enzyme, so the fridge buys you time. Heat switches it off for good: cooked apples never go brown.", 1.09, 0.40, +0.4, 1.45, ["Cold", "Heat"], "low"),
    ("e1", "Now the part nobody expects. Some foods go brown on purpose.", 1.04, 0.30, +1.0, 1.5, ["nobody", "purpose.:dn"], "low"),
    ("e2", "Black tea gets its colour from this exact reaction, done on purpose. Coffee and cocoa too.", 1.08, 0.28, +0.4, 1.45, ["Black", "purpose."], "low"),
    ("e3", "Avocados, bananas, potatoes: same enzyme, same trick. That grey top layer on your guacamole? Melanin.", 1.07, 0.40, +0.6, 1.5, ["same", "Melanin.:dn"], "low"),
    ("f1", "And one apple can't do it at all: the Arctic apple. Scientists switched off its PPO gene, so it stays white when you cut it.", 1.08, 0.25, +0.6, 1.5, ["can't", "white"], "low"),
    ("f2", "Approved in the US back in twenty fifteen. The apple that never blushes.", 1.01, 0.40, -0.6, 1.4, ["fifteen.", "blushes.:dn"], "low"),
    ("g1", "Quick recap: the cut opens the rooms, the enzyme meets oxygen, and that makes brown melanin. Lemon, honey or cold slow it, heat stops it. And brown is fine to eat.", 1.08, 0.30, +0.6, 1.45, ["rooms,", "fine"], "low"),
    ("g2", "Send this to the friend who throws away brown apple slices!", 1.04, 0.00, +1.2, 1.5, ["friend", "brown"], None),
]
