# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# FreshNestHub 13 — "Why do onions make you cry?" (a booby trap: two chemicals kept apart in each cell, the knife mixes
# them, enzyme 1 -> unstable acid, enzyme 2 -> tear-factor gas, nerves on the eye, tear glands wash it out; it's a defence
# against bugs; 2002 Japan found enzyme 2, 2008 NZ + Japan switched it off -> no tears; Cornell 2025: sharp knife, slow cuts;
# heat kills the enzyme)
# Script upgrade (ep 13): a CHAIN story (cut -> mix -> acid -> gas -> nerves -> tears) told one link per line, a persistent
# chain map builds up link by link, 5 chapters with re-hooks, open loop (tear-free onion) at 6 s paid at ~70 %,
# two practical takeaways (sharp knife + slow cuts; cooked onions can't do it).
LINES = [
    ("i1", "Do you know an onion makes you cry... on purpose?", 0.96, 0.30, +1.0, 1.45, ["cry...", "purpose?"], "q"),
    ("i2", "It's a trap! And your knife sets it off.", 1.0, 0.40, +1.2, 1.5, ["trap!", "knife"], None),
    ("i3", "Stick around. Scientists even made an onion that can't do it.", 0.98, 0.45, +1.0, 1.5, ["can't"], None),
    ("a1", "Here's the secret. An onion is made of tiny cells.", 1.02, 0.35, +0.8, 1.45, ["secret.", "cells."], "low"),
    ("a2", "Inside each cell, two chemicals are kept in separate rooms.", 1.02, 0.40, +0.8, 1.45, ["two", "separate"], "low"),
    ("a3", "The first one is full of sulfur. Onions pull it from the soil.", 1.02, 0.40, +0.8, 1.45, ["sulfur.", "soil."], "low"),
    ("a4", "The second one is an enzyme.", 1.0, 0.30, +0.8, 1.45, ["enzyme."], "low"),
    ("a5", "An enzyme is a tiny helper. It turns one chemical into another.", 1.02, 0.40, +0.8, 1.45, ["helper.", "another."], "low"),
    ("a6", "As long as they stay apart, nothing happens.", 1.0, 0.45, +0.8, 1.45, ["apart,", "nothing"], "low"),
    ("b1", "But then... you cut it.", 0.97, 0.35, +1.0, 1.5, ["cut"], None),
    ("b2", "The knife breaks the walls, and the two chemicals mix.", 1.02, 0.40, +0.8, 1.45, ["breaks", "mix."], "low"),
    ("b3", "First, the enzyme snips the sulfur stuff into a new acid.", 1.02, 0.40, +0.8, 1.45, ["snips", "acid."], "low"),
    ("b4", "That acid is wobbly. So a second enzyme grabs it...", 1.0, 0.30, +0.8, 1.45, ["wobbly.", "second"], None),
    ("b5", "and turns it into a gas. Scientists call it the tear factor.", 1.0, 0.40, +1.0, 1.5, ["gas.", "tear"], "low"),
    ("b6", "The gas floats up, right into your eyes.", 1.02, 0.35, +0.8, 1.45, ["eyes."], "low"),
    ("b7", "Tiny nerves on the front of your eye feel the sting.", 1.02, 0.35, +0.8, 1.45, ["nerves", "sting."], "low"),
    ("b8", "So your tear glands flood your eyes to wash it out.", 1.0, 0.45, +0.8, 1.45, ["flood", "wash"], "low"),
    ("c1", "But why would an onion do this?", 0.97, 0.30, +1.0, 1.5, ["why"], "q"),
    ("c2", "To protect itself. To an onion, a bug's bite is just like your knife.", 1.0, 0.40, +0.8, 1.45, ["protect", "bite"], "low"),
    ("c3", "So the gas is a defense against insects and germs.", 1.02, 0.45, +0.8, 1.45, ["defense"], "low"),
    ("d1", "Now, the tear-free onion I promised.", 0.97, 0.35, +1.0, 1.5, ["tear-free"], None),
    ("d2", "In two thousand two, scientists in Japan found that second enzyme.", 1.02, 0.40, +0.8, 1.45, ["Japan", "second"], "low"),
    ("d3", "Then scientists in New Zealand and Japan switched its gene off.", 1.02, 0.40, +0.8, 1.45, ["switched", "off."], "low"),
    ("d4", "They crushed those onions... and the tears never came!", 0.98, 0.45, +1.2, 1.5, ["crushed", "never"], None),
    ("e1", "So how do you beat the trap today?", 0.97, 0.30, +1.0, 1.5, ["beat"], "q"),
    ("e2", "Scientists at Cornell filmed onions being cut in super slow motion.", 1.02, 0.40, +0.8, 1.45, ["slow", "motion."], "low"),
    ("e3", "A dull knife squashes more cells. More juice sprays out.", 1.02, 0.40, +0.8, 1.45, ["dull", "juice"], "low"),
    ("e4", "And fast chopping can shoot drops at forty meters a second!", 0.98, 0.40, +1.2, 1.5, ["forty"], None),
    ("e5", "So use a sharp knife, and cut slowly.", 1.0, 0.40, +0.8, 1.45, ["sharp", "slowly."], "low"),
    ("e6", "And cooked onions? Heat breaks the enzyme. The trap can't fire.", 1.0, 0.45, +0.8, 1.45, ["cooked", "can't"], "low"),
    ("f1", "Remember: two chemicals, kept apart. Your knife mixes them. The gas finds your eyes.", 1.0, 0.40, +0.8, 1.45, ["apart.", "eyes."], "low"),
    ("f2", "Send this to the friend who cries every time they cut an onion!", 0.97, 0.0, +1.2, 1.5, ["friend", "cries"], None),
]
