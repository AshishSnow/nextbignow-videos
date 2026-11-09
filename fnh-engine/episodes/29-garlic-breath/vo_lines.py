# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# FreshNestHub 29 — "Why does garlic breath last so long?" Facts (verified 9 Nov 2026):
# - Crushing/chopping: alliin + an enzyme in the garlic cells react 'in a matter of seconds' -> allicin, which 'breaks down into lots of other chemicals, most of them stinky'
#   (BBC Science Focus, Villazon 2016); the enzyme = alliinase, released when garlic is cut or crushed (Discover, Liu 2015).
# - Two sources: the compounds other than AMS come from the mouth (brushing teeth + tongue reduces those) (Discover 2015); 'If there are still tiny particles stuck back there,
#   you will continue to have garlic breath' (Barringer via Popular Science 2016).
# - Allyl methyl sulfide: 'Nearly all of these chemicals are broken down in your stomach and liver, but allyl methyl sulphide is one that survives to be absorbed into the bloodstream
#   intact' and diffuses out through the lungs; brushing 'has only limited effect because the chemical is still in your blood' (Science Focus); AMS 'does not get metabolized in your gut
#   and liver', bloodstream -> lungs, also 'released through pores of the skin' (Discover); absorbed into the bloodstream, vaporises in the lungs, sweat (Popular Science).
# - Duration: 'Twenty-four hours after consuming garlic, you can still smell it' (Sheryl Barringer, Ohio State food science, via Popular Science); 'up to two days' (Science Focus).
# - Ohio State 2016 (Mirondo & Barringer, J Food Sci, doi 10.1111/1750-3841.13439; IFT release via ScienceDaily + Newswise): 3 g garlic chewed 25 s, then water or a food; breath measured
#   by selected ion flow tube mass spectrometry; raw apple + raw lettuce cut the volatiles '50 percent or more compared to the control for the first 30 minutes'; mint leaves 'higher
#   deodorization level'; heated apple / lettuce 'a significant reduction' (less than raw); green tea 'no deodorizing effect'; enzymes in raw foods + phenolic compounds destroy the volatiles.
# - Milk: Hansanugrum & Barringer, J Food Sci 2010: whole milk (fat) better, milk during the meal better than after (Discover 2015; Popular Science: 'milk (especially with the meal)').
LINES = [
    ("i1", "Do you know garlic breath can come from your lungs, not just your mouth?", 1.00, 0.3, +1.0, 1.5, ["lungs,"], "q"),
    ("i2", "That's why you can brush twice, and your friend still backs away the next morning.", 1.04, 0.45, +0.4, 1.45, ["twice,", "morning.:dn"], "low"),
    ("a0", "Start with a whole clove of garlic. Sitting on the counter, it barely smells.", 1.03, 0.25, +0.8, 1.45, ["whole", "barely"], "low"),
    ("a1", "The smell only shows up when you cut it or crush it.", 1.04, 0.25, +0.4, 1.45, ["cut", "crush"], "low"),
    ("a2", "Crushing breaks the cells open, so two things that were kept apart finally meet: a compound and an enzyme.", 1.06, 0.25, +0.4, 1.45, ["apart", "meet:"], "low"),
    ("a3", "In seconds they make allicin, and allicin falls apart into a bunch of smelly sulfur gases.", 1.05, 0.45, +0.8, 1.5, ["seconds", "smelly"], "low"),
    ("b0", "But the part nobody tells you is this: garlic breath comes from two places.", 1.0, 0.3, +1.0, 1.55, ["nobody", "two"], "low"),
    ("b1", "Place one is your mouth. Tiny bits of garlic stuck to your teeth and tongue keep giving off those gases.", 1.06, 0.25, +0.4, 1.45, ["mouth.", "tongue"], "low"),
    ("b2", "Brushing and flossing really do help with that part.", 1.03, 0.4, +0.4, 1.45, ["really"], "low"),
    ("b3", "Place two is sneakier. One gas, called allyl methyl sulfide, doesn't get broken down like the others.", 1.05, 0.25, +0.8, 1.5, ["sneakier."], "low"),
    ("b4", "Your gut and your liver just can't deal with it, so it slips into your blood.", 1.05, 0.1, +0.4, 1.45, ["slips", "blood."], "low"),
    ("b5", "It rides around your whole body, reaches your lungs, and leaves a little with every breath you breathe out.", 1.05, 0.25, +0.4, 1.45, ["lungs,", "every"], "low"),
    ("b6", "And a little of it even leaks out through your sweat, which is a fun thing to know.", 1.03, 0.3, -0.6, 1.4, ["leaks", "fun"], "low"),
    ("b7", "So your mouth can be squeaky clean while your lungs keep doing the talking.", 1.02, 0.45, +1.2, 1.6, ["clean", "talking.:dn"], "low"),
    ("c0", "So how long can a garlic breath actually hang around?", 1.0, 0.25, +1.0, 1.5, ["long"], "q"),
    ("c1", "An Ohio State food scientist says you can still smell it twenty-four hours later. Some sources say up to two days.", 1.06, 0.25, +0.4, 1.45, ["twenty-four", "two"], "low"),
    ("c2", "That's a whole day of meetings, smelling like last night's dinner.", 1.0, 0.45, -0.6, 1.4, ["whole", "dinner.:dn"], "low"),
    ("d0", "So can you actually fight it?", 1.0, 0.3, +1.0, 1.5, ["fight"], "q"),
    ("d1", "Her team tested it. People chewed raw garlic, then ate different foods, and a machine measured their breath.", 1.06, 0.25, +0.4, 1.45, ["tested", "machine"], "low"),
    ("d2", "Raw apple and raw lettuce cut the smelly gases by half or more, for the first thirty minutes.", 1.05, 0.25, +0.8, 1.5, ["half"], "low"),
    ("d3", "Fresh mint leaves did even better. Green tea did nothing at all.", 1.03, 0.3, +0.8, 1.5, ["better.", "nothing"], "low"),
    ("d4", "Cooked apple helped too, but raw won, because raw food brings an enzyme plus plant compounds that break the gases down.", 1.06, 0.25, +0.4, 1.45, ["raw", "down.:dn"], "low"),
    ("d5", "And an older study from the same lab found milk helps too, especially whole milk, and it works better with the meal than after it.", 1.06, 0.45, +0.4, 1.45, ["whole", "with"], "low"),
    ("e0", "So brush for the mouth part, and grab an apple, some lettuce or a few mint leaves for the rest.", 1.04, 0.25, +0.8, 1.5, ["brush", "apple,"], "low"),
    ("e1", "And the part in your lungs? That one mostly just needs time.", 1.0, 0.45, -0.3, 1.35, ["lungs?", "time.:dn"], "low"),
    ("f1", "Garlic's still worth it, by the way. Maybe just not right before a job interview.", 1.02, 0.3, +0.8, 1.5, ["worth", "interview.:dn"], "low"),
    ("f2", "Send this to the friend who had the garlic naan and is standing way too close.", 1.03, 0.0, +0.8, 1.45, ["close.:dn"], "low"),
]
