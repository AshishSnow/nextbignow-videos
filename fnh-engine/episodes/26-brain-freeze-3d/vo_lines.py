# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# FreshNestHub 26 — "What happens when you eat ice cream too fast" (brain freeze). Zack D Films-style 3D explainer (owner, 6 Nov).
# Facts (verified 6 Nov 2026):
# - Roof of the mouth goes from warm to much colder; blood vessels there constrict, then relax -> blood flow jumps -> pain signals;
#   leading theory: the trigeminal nerve, referred pain felt in the forehead/temples (Houston Methodist, 'What causes brain freeze', 2020;
#   Science Notes 'Brain freeze (ice cream headache)': vessels constrict then dilate, trigeminal detects, brain reads it as forehead pain).
# - Formal name: cold-stimulus headache (Science Notes); 'a type of headache' (Houston Methodist).
# - Lasts a few seconds to under five minutes (Houston Methodist); usually under a minute (Science Notes).
# - Fix: warm the roof of the mouth — press the tongue against it, sip warm/room-temperature water; prevent by eating slowly (both).
LINES = [
    ("i1", "This is what happens when you eat ice cream way too fast.", 1.0, 0.35, 0, 1.3, ["fast."], "low"),
    ("i2", "One big, greedy bite, and the roof of your mouth goes from warm to freezing in a second.", 1.0, 0.3, 0, 1.3, ["freezing"], "low"),
    ("a1", "Up there are tiny blood vessels. And they panic.", 1.0, 0.25, 0, 1.3, ["panic."], "low"),
    ("a2", "First they squeeze shut. Then they snap wide open, and warm blood comes rushing back in.", 1.0, 0.3, 0, 1.3, ["shut.", "rushing"], "low"),
    ("a3", "Right next to them runs a big nerve, called the trigeminal nerve. And it sends an alarm straight to your brain.", 1.0, 0.3, 0, 1.3, ["alarm"], "low"),
    ("b1", "But your brain gets the address wrong.", 1.0, 0.25, 0, 1.3, ["wrong."], "low"),
    ("b2", "It thinks the pain is coming from your forehead, so that's exactly where you feel it.", 1.0, 0.35, 0, 1.3, ["forehead,"], "low"),
    ("b3", "That's brain freeze. Doctors call it a cold stimulus headache.", 1.0, 0.35, 0, 1.3, ["brain"], "low"),
    ("c1", "It usually fades in seconds. Want it gone faster?", 1.0, 0.25, 0, 1.3, ["faster?"], "q"),
    ("c2", "Press your tongue flat against the roof of your mouth. Its warmth heats the spot back up, and the pain fades away.", 1.0, 0.3, 0, 1.3, ["tongue"], "low"),
    ("c3", "Or, you know. Just eat slower.", 1.0, 0.6, 0, 1.3, ["slower."], "low"),
]
