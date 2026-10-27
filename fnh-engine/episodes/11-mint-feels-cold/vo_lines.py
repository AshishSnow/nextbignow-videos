# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# FreshNestHub 11 — "Why mint feels cold" (menthol switches on the TRPM8 cold alarm, makes it jumpy, fools your nose too)
# Twin of ep 09 (spicy = heat alarm). Script upgrade: open loop in the first 5 s ("it even fools your nose") paid off at ~70 %.
# Voice upgrade (ep 11): weakest lines (b2 4.11, b3 4.13, a7 4.23, a6 4.25) rewritten shorter; plain lines 1.02-1.03 for 180+ wpm.
# Also: statements SETTLE ("low" ending) on every explaining statement that closes an idea; questions rise.
LINES = [
    ("i1", "Do you know mint... doesn't make your mouth cold at all?", 0.96, 0.30, +1.0, 1.45, ["mint...", "cold"], "q"),
    ("i2", "Chew mint gum, sip some water, and whoa, it's freezing!", 1.02, 0.40, +1.2, 1.5, ["whoa,", "freezing!"], None),
    ("i3", "But nothing in your mouth got colder. It's a trick!", 0.98, 0.40, +1.0, 1.5, ["nothing", "trick!"], None),
    ("i4", "And later, you'll see it even fools your nose.", 0.97, 0.45, +1.0, 1.5, ["even", "nose."], None),
    ("a1", "Meet the trickster. It's menthol, a chemical in mint leaves.", 1.03, 0.40, +0.8, 1.45, ["menthol,", "mint"], "low"),
    ("a2", "Your tongue is full of tiny nerve endings. They're wires to your brain.", 1.03, 0.40, +0.8, 1.45, ["nerve", "wires"], "low"),
    ("a3", "And on those wires sit little cold alarms.", 0.97, 0.40, +1.0, 1.5, ["cold", "alarms."], None),
    ("a4", "Normally, they only ring when things get cool... below about twenty-five degrees.", 1.03, 0.40, +0.8, 1.45, ["cool...", "twenty-five"], "low"),
    ("a5", "Your mouth is warmer than that. So ice water? Ding! Cold alarm.", 1.02, 0.40, +1.0, 1.5, ["warmer", "Ding!"], None),
    ("a6", "But menthol fits the cold alarm... like a key fits a lock.", 0.98, 0.40, +1.0, 1.5, ["fits", "key"], None),
    ("a7", "Click! The alarm rings. Your nerves tell your brain... it's COLD!", 1.02, 0.45, +1.2, 1.5, ["Click!", "COLD!"], None),
    ("a8", "Your brain believes it. But the temperature didn't change at all.", 0.97, 0.45, +0.8, 1.45, ["believes", "didn't"], "low"),
    ("b1", "So why does water feel like ice after mint?", 0.97, 0.35, +1.0, 1.5, ["ice"], "q"),
    ("b2", "Menthol makes the alarm jumpy. Now it rings even when it's warmer.", 1.03, 0.40, +0.8, 1.45, ["jumpy.", "warmer"], "low"),
    ("b3", "It's already half ringing. So when cool water hits... it screams!", 1.02, 0.40, +1.0, 1.5, ["half", "screams!"], None),
    ("b4", "That's why even a hot drink can feel weirdly cool after mint.", 1.03, 0.45, +0.8, 1.45, ["hot", "cool"], "low"),
    ("c1", "Scientists found this cold alarm in two thousand two.", 1.02, 0.35, +0.8, 1.45, ["found"], "low"),
    ("c2", "Then they tested mice born without it.", 1.02, 0.35, +1.0, 1.5, ["without"], None),
    ("c3", "Those mice hardly reacted to cool temperatures. Their cold alarm was gone!", 1.03, 0.40, +0.8, 1.45, ["hardly", "gone!"], None),
    ("c4", "These discoveries helped win the twenty twenty-one Nobel Prize.", 1.02, 0.40, +1.0, 1.5, ["Nobel"], None),
    ("c5", "Same prize as our spicy video! Chili rings the heat alarm. Mint rings the cold one.", 1.02, 0.45, +1.0, 1.5, ["heat", "cold"], "low"),
    ("d1", "Now, the nose trick I promised.", 0.97, 0.35, +1.0, 1.5, ["nose"], None),
    ("d2", "Scientists gave people with a stuffy cold a menthol candy... or a plain one.", 1.03, 0.40, +0.8, 1.45, ["menthol", "plain"], None),
    ("d3", "Within ten minutes, the menthol group said their nose felt clearer.", 1.03, 0.40, +0.8, 1.45, ["ten", "clearer."], "low"),
    ("d4", "But a machine measured the airflow. It was no better than with plain candy!", 0.98, 0.40, +1.0, 1.5, ["machine", "no"], None),
    ("d5", "Scientists think the cool feeling tells the brain... I can breathe!", 0.97, 0.45, +1.0, 1.5, ["cool", "breathe!"], None),
    ("e1", "So mint doesn't change the temperature. It changes what you feel.", 0.98, 0.45, +0.8, 1.45, ["temperature.", "feel."], "low"),
    ("e2", "Remember: menthol rings your cold alarm, makes it jumpy, and fools your nose.", 0.98, 0.45, +0.8, 1.45, ["rings", "jumpy,", "nose."], "low"),
    ("e3", "Send this to the friend who drinks ice water right after gum!", 0.97, 0.0, +1.2, 1.5, ["friend", "gum!"], None),
]
