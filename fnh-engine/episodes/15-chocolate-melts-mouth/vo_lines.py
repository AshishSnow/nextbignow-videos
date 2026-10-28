# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# FreshNestHub 15 — "Why chocolate melts in your mouth" (cocoa butter can set into six crystal shapes; only shape V is glossy,
# snaps and melts at ~34 C, just under body temperature ~37 C; tempering = melt, cool, warm a little -> wrong crystals melt, V
# survives and seeds the rest; white 'bloom' = fat (warmth, or V slowly turning into VI) or sugar (damp fridge) on the surface,
# safe to eat, just chalky; store cool + dry, not in the fridge; bloomed chocolate is fine for baking)
# Script upgrade (ep 15): an everyday food + a belief flip (white chocolate = mould -> it's bloom, safe), Halloween-timely (candy
# bags), ONE concrete everyday analogy for crystals (same bricks, built six ways), numbers you can feel (34 vs 37 degrees), an
# open loop at 6 s paid at ~70 %, 4 chapters, a practical takeaway (store cool + dry, not the fridge; bake with bloomed bars).
LINES = [
    ("i1", "Do you know chocolate is made to melt... right at the temperature of your mouth?", 0.96, 0.30, +1.0, 1.45, ["melt...", "mouth?"], "q"),
    ("i2", "On the shelf, it snaps. On your tongue, it melts away.", 1.0, 0.40, +1.2, 1.5, ["snaps.", "melts"], None),
    ("i3", "And that white dust on old chocolate? It's not what you think.", 0.98, 0.45, +1.0, 1.5, ["white", "think."], None),
    ("a1", "Here's the secret. The fat in chocolate is called cocoa butter.", 1.02, 0.35, +0.8, 1.45, ["secret.", "butter."], "low"),
    ("a2", "It comes from the cocoa bean. And it has a strange talent.", 1.02, 0.35, +0.8, 1.45, ["bean.", "strange"], "low"),
    ("a3", "When it cools down, it can set into six different crystal shapes.", 1.0, 0.35, +0.8, 1.45, ["six", "crystal"], "low"),
    ("a4", "Same fat. Just stacked in different ways. Like the same bricks, built six different ways.", 1.0, 0.45, +0.8, 1.45, ["stacked", "bricks,"], "low"),
    ("b1", "Shapes one to four are the weak ones. They melt too easily, so the chocolate turns soft and dull.", 1.02, 0.40, +0.8, 1.45, ["weak", "dull."], "low"),
    ("b2", "But shape five is the winner.", 0.97, 0.30, +1.0, 1.5, ["five", "winner."], None),
    ("b3", "It's shiny. It snaps. And it melts at about thirty-four degrees Celsius.", 1.0, 0.35, +1.0, 1.5, ["shiny.", "thirty-four"], None),
    ("b4", "Inside your mouth, it's close to thirty-seven. Just a little warmer.", 1.0, 0.35, +0.8, 1.45, ["thirty-seven.", "warmer."], "low"),
    ("b5", "So it stays solid in the wrapper... and melts the moment it hits your tongue.", 0.98, 0.45, +1.0, 1.5, ["solid", "tongue."], None),
    ("c1", "But here's the catch.", 0.97, 0.30, +1.0, 1.5, ["catch."], None),
    ("c2", "Melt chocolate and just let it cool, and you get a messy mix of all the shapes.", 1.02, 0.40, +0.8, 1.45, ["messy", "all"], "low"),
    ("c3", "So chocolate makers use a trick. It's called tempering.", 1.0, 0.35, +0.8, 1.45, ["trick.", "tempering."], "low"),
    ("c4", "First, they melt it all. Then they cool it down. Then they warm it up, just a little.", 1.02, 0.40, +0.8, 1.45, ["melt", "cool", "warm"], "low"),
    ("c5", "That gentle warm-up melts the weak crystals. But shape five survives.", 1.0, 0.35, +0.8, 1.45, ["weak", "survives."], "low"),
    ("c6", "Those crystals work like seeds. As the chocolate sets, the rest lines up the same way.", 1.0, 0.45, +0.8, 1.45, ["seeds.", "same"], "low"),
    ("d1", "Now, that white dust. Maybe you've seen it in your Halloween candy bag.", 0.98, 0.35, +1.0, 1.5, ["white", "Halloween"], None),
    ("d2", "It's not mould. It's called bloom.", 0.97, 0.35, +1.0, 1.5, ["not", "bloom."], None),
    ("d3", "When chocolate gets warm, some of its fat melts, rises to the surface, and sets again. As a white film.", 1.02, 0.40, +0.8, 1.45, ["rises", "white"], "low"),
    ("d4", "Over months, shape five can also slowly turn into shape six. That can bloom too.", 1.02, 0.40, +0.8, 1.45, ["months,", "six."], "low"),
    ("d5", "And in a damp fridge, water pulls sugar to the surface. It dries into tiny white crystals.", 1.02, 0.40, +0.8, 1.45, ["sugar", "crystals."], "low"),
    ("d6", "Either way, it's still safe to eat. It just feels a bit chalky.", 0.98, 0.45, +1.0, 1.5, ["safe", "chalky."], None),
    ("e1", "So keep your chocolate somewhere cool and dry. Not in the fridge.", 1.0, 0.35, +0.8, 1.45, ["dry.", "fridge."], "low"),
    ("e2", "And if it has already bloomed? Melt it into a cake. Nobody will know.", 1.0, 0.45, +1.0, 1.5, ["bloomed?", "cake."], None),
    ("f1", "Remember: chocolate is built to melt in your mouth. And white bloom is just fat or sugar.", 1.0, 0.40, +0.8, 1.45, ["built", "sugar."], "low"),
    ("f2", "Send this to the friend who throws away chocolate with white spots!", 0.97, 0.0, +1.2, 1.5, ["friend", "white"], None),
]
