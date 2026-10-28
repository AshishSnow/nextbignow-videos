# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# FreshNestHub 16 — "Does swallowed gum stay in your stomach for 7 years?" (myth: the gum base can't be digested, but the gut
# doesn't need to digest something to move it: peristalsis squeezes it along, and between meals the 'housekeeping' wave
# (migrating motor complex, every ~1.5-2 h) sweeps leftovers on; out in ~40 h / a day or two, like corn kernels; catch: lots
# of gum often can clump into a blockage (bezoar), mostly in young kids; twist: 5,700-year-old chewed birch pitch -> full genome)
# Script upgrade (ep 16): the breakout pattern (everyday habit + belief flip) in REFUTATION order, a define-on-sight enzyme
# + peristalsis with an everyday analogy (toothpaste tube), a number you can feel (61,000 hours vs 40), a share bonus (why your
# stomach growls), an open loop at 8 s ('gum almost 6,000 years old') paid at ~85 %, 4 chapters, practical tip + safe doctor line.
LINES = [
    ("i1", "Do you know what really happens to gum when you swallow it?", 0.96, 0.30, +1.0, 1.45, ["really", "swallow"], "q"),
    ("i2", "You've probably heard it sits in your stomach for seven years.", 1.0, 0.40, +1.0, 1.5, ["stomach", "seven"], None),
    ("i3", "That's a myth. And stick around, because later you'll meet a piece of gum that's almost six thousand years old.", 0.98, 0.45, +1.0, 1.5, ["myth.", "six"], None),
    ("a1", "First, what is gum actually made of?", 0.97, 0.30, +1.0, 1.5, ["made"], "q"),
    ("a2", "The sugar and the flavour? Your body digests those, like any other food.", 1.0, 0.35, +0.8, 1.45, ["sugar", "digests"], "low"),
    ("a3", "But the chewy part is different. It's called gum base.", 1.0, 0.35, +0.8, 1.45, ["chewy", "base."], "low"),
    ("a4", "It's a mix of rubbery resins and softeners. It's made to stay chewy, not to dissolve.", 1.03, 0.35, +0.8, 1.45, ["rubbery", "dissolve."], "low"),
    ("a5", "And your body has no enzymes that can break it down. Enzymes are tiny helpers that cut food into pieces.", 1.03, 0.40, +0.8, 1.45, ["no", "helpers"], "low"),
    ("a6", "So yes, the chewy part stays in one piece, all the way through.", 0.98, 0.40, +0.8, 1.45, ["one"], "low"),
    ("b1", "So if your body can't break it down, why doesn't it get stuck inside you?", 0.97, 0.30, +1.0, 1.5, ["stuck"], "q"),
    ("b2", "Here's the thing: your gut doesn't have to digest something to move it.", 1.0, 0.35, +0.8, 1.45, ["move"], "low"),
    ("b3", "Your gut is a long tube made of muscle. It squeezes behind the food, and relaxes in front of it.", 1.03, 0.35, +0.8, 1.45, ["muscle.", "squeezes"], "low"),
    ("b4", "That squeeze rolls along like a wave. It's called peristalsis.", 1.0, 0.35, +0.8, 1.45, ["wave.", "peristalsis."], "low"),
    ("b5", "It's like squeezing toothpaste out of a tube.", 1.0, 0.40, +0.8, 1.45, ["toothpaste"], "low"),
    ("b6", "And between meals, a stronger wave sweeps through, about every ninety minutes to two hours.", 1.03, 0.35, +0.8, 1.45, ["stronger", "ninety"], "low"),
    ("b7", "Scientists call it a housekeeping wave. It sweeps leftovers out of your stomach and small intestine.", 1.0, 0.40, +0.8, 1.45, ["housekeeping", "leftovers"], "low"),
    ("b8", "Bonus fact: that same wave is one reason your stomach growls when it's empty.", 0.98, 0.45, +1.0, 1.5, ["growls"], None),
    ("c1", "So where does the gum go? It rides along with everything else.", 1.0, 0.35, +1.0, 1.5, ["go?", "everything"], None),
    ("c2", "Corn kernels and seeds often come out whole too.", 1.03, 0.35, +0.8, 1.45, ["whole"], "low"),
    ("c3", "Experts say swallowed gum leaves your body in about forty hours. A day or two.", 1.0, 0.35, +0.8, 1.45, ["forty"], "low"),
    ("c4", "Seven years would be over sixty thousand hours. The real number? About forty.", 0.98, 0.45, +1.0, 1.5, ["sixty", "forty."], None),
    ("d1", "Now, one honest catch.", 0.97, 0.30, +1.0, 1.5, ["catch."], None),
    ("d2", "Swallowing lots of gum, every single day, is a different story.", 1.0, 0.35, +0.8, 1.45, ["lots", "different"], "low"),
    ("d3", "Doctors have seen it clump into a lump that blocks the gut. Mostly in young kids.", 1.0, 0.35, +0.8, 1.45, ["clump", "kids."], "low"),
    ("d4", "So spit your gum in the bin. And if a child swallowed a lot and gets tummy pain or starts throwing up, see a doctor.", 1.0, 0.45, +0.6, 1.45, ["bin.", "doctor."], "low"),
    ("e1", "Now, remember that ancient gum I promised?", 0.97, 0.30, +1.0, 1.5, ["ancient"], "q"),
    ("e2", "In Denmark, scientists found a chewed lump of birch tar. It's about five thousand seven hundred years old.", 1.0, 0.35, +0.8, 1.45, ["birch", "seven"], "low"),
    ("e3", "From the spit trapped inside it, they read the complete DNA of the woman who chewed it.", 1.0, 0.40, +1.0, 1.5, ["complete", "woman"], None),
    ("e4", "Now that is a piece of gum that really stuck around.", 0.98, 0.45, +1.0, 1.5, ["really", "stuck"], None),
    ("f1", "Remember: your body can't digest gum, but your gut moves it out anyway. In about two days.", 1.0, 0.40, +0.8, 1.45, ["can't", "two"], "low"),
    ("f2", "Send this to the friend who still believes the seven year gum rule!", 0.97, 0.0, +1.2, 1.5, ["friend", "seven"], None),
]
