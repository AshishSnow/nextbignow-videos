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
]
