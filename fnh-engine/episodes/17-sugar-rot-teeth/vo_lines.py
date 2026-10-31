# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# FreshNestHub 17 — "Does sugar rot your teeth?" (no: bacteria in plaque eat the sugar and make ACID; the acid pulls minerals out of
# the enamel; saliva + fluoride put minerals back, early white spots can heal; each sweet = a 30-60 min acid attack (Temple University
# dentist), so FREQUENCY matters more than amount (Temple, CDA); chewy/gummy sweets stick = longer meal for bacteria, sour sweets bring
# their own acid, chocolate washes away fast (CDA); eat sweets with a meal, water, wait an hour before brushing after sour; brush twice
# a day with fluoride toothpaste (NIDCR, NHS); white/brown patch or pain -> dentist.)
# Script upgrade (ep 17): FIRST script written under the 28 Oct 'person talking' guide: no filler openers, direct address, small jokes
# ('Your spit. Seriously.'), rhythm changes (3-word lines after 15-word ones), an open loop at 6 s (the 'kindest candy') paid at ~75 %,
# a timer you can feel (one sweet = one hour; one sweet an hour = acid all day), Halloween-day timing, practical plan + one safe dentist line.
# VOICE upgrade (ep 17): conversational REGISTERS per beat - confiding/aside lines drop the base pitch (-0.6 st) and slow to 0.95,
# excited reveals lift (+1.2) with a '...' micro-pause before the payoff word, plain explanations sit in the middle (+0.4, 1.0-1.03).
LINES = [
    ("i1", "Do you know sugar doesn't actually rot your teeth?", 0.96, 0.30, +1.0, 1.45, ["actually", "teeth?"], "q"),
    ("i2", "Something else does. And it's living in your mouth right now.", 0.98, 0.45, +0.8, 1.5, ["else", "right"], None),
    ("i3", "Stick around, because the candy that's kindest to your teeth... is probably the one you'd guess is worst.", 0.97, 0.45, +0.6, 1.5, ["kindest", "worst."], None),
    ("a1", "So who's the real culprit? Your teeth wear a thin, sticky film called plaque.", 0.98, 0.35, +0.6, 1.45, ["culprit?", "plaque."], "low"),
    ("a2", "Plaque is basically a tiny city of bacteria.", 1.0, 0.35, +0.4, 1.45, ["city"], "low"),
    ("a3", "They can't chew through your teeth. But they absolutely love sugar.", 0.98, 0.40, +0.6, 1.5, ["can't", "love"], "low"),
    ("a4", "You eat a sweet. They eat the leftovers. And what comes out of them... is acid.", 0.98, 0.40, +0.8, 1.5, ["leftovers.", "acid."], "low"),
    ("a5", "That acid pulls minerals out of your enamel. Enamel is the hard, shiny shell on the outside of each tooth.", 1.03, 0.35, +0.4, 1.45, ["minerals", "shell"], "low"),
    ("a6", "Lose enough minerals, and the shell breaks. That hole has a name: a cavity.", 1.0, 0.45, +0.6, 1.45, ["breaks.", "cavity."], "low"),
    ("b1", "But wait. Your mouth has a rescue team.", 0.96, 0.35, +1.0, 1.5, ["wait.", "rescue"], None),
    ("b2", "It's your spit. No, really.", 0.95, 0.50, -0.6, 1.4, ["spit.", "really."], "low"),
    ("b3", "Saliva washes the acid away, and it carries minerals back into the enamel.", 1.0, 0.35, +0.4, 1.45, ["washes", "back"], "low"),
    ("b4", "So after every attack, your teeth quietly patch themselves up. The fluoride in toothpaste helps them do it.", 1.02, 0.35, +0.4, 1.45, ["patch", "fluoride"], "low"),
    ("b5", "An early cavity, just a white spot, can actually heal. A real hole can't.", 0.98, 0.45, +0.6, 1.5, ["heal.", "can't."], "low"),
    ("c1", "Which brings us to the thing nobody tells you. The timer.", 0.95, 0.40, -0.6, 1.4, ["nobody", "timer."], "low"),
    ("c2", "Every time you eat something sweet, that acid hangs around for about thirty to sixty minutes.", 1.0, 0.35, +0.4, 1.45, ["thirty", "sixty"], "low"),
    ("c3", "One sweet? Half an hour to an hour of acid.", 1.0, 0.35, +0.8, 1.5, ["One", "hour"], "low"),
    ("c4", "Three sweets at once? Still half an hour to an hour.", 1.0, 0.35, +0.8, 1.5, ["Three", "Still"], "low"),
    ("c5", "But one sweet every hour, all afternoon? Your teeth sit in acid the whole day. No time to repair.", 0.98, 0.40, +0.6, 1.5, ["every", "whole"], "low"),
    ("c6", "So it's not how much candy you eat. It's how often. Dentists have been saying this for years.", 0.97, 0.45, +0.8, 1.5, ["much", "often."], "low"),
    ("d1", "Okay. Time for the candy ranking.", 0.96, 0.35, +1.0, 1.5, ["ranking."], None),
    ("d2", "Chewy caramels and gummies stick to your teeth. So the bacteria get a longer meal.", 1.0, 0.35, +0.4, 1.45, ["stick", "longer"], "low"),
    ("d3", "Sour sweets? They bring their own acid along.", 0.98, 0.35, +0.6, 1.5, ["Sour", "own"], "low"),
    ("d4", "And chocolate? It melts and washes off fast. Dentists call it one of the better picks. Told you.", 0.98, 0.45, +0.8, 1.5, ["chocolate?", "better", "Told"], None),
    ("e1", "So, your plan for tonight.", 0.96, 0.35, +0.6, 1.45, ["plan"], "low"),
    ("e2", "Eat your candy in one go, with a meal, when your mouth is full of saliva. Then a glass of water.", 1.02, 0.35, +0.4, 1.45, ["one", "water."], "low"),
    ("e3", "If you had sour stuff, wait an hour before you brush. The acid softens enamel, and you don't want to scrub it.", 1.02, 0.35, +0.4, 1.45, ["hour", "softens"], "low"),
    ("e4", "Brush twice a day with fluoride toothpaste. And if a tooth hurts, or you spot a white or brown patch, see a dentist.", 1.02, 0.45, +0.2, 1.45, ["twice", "dentist."], "low"),
    ("f1", "Quick recap: bacteria eat the sugar, they make acid, your spit repairs the damage, and it's how often that counts.", 1.0, 0.40, +0.6, 1.45, ["acid,", "often"], "low"),
    ("f2", "Send this to the friend who nibbles one sweet every hour!", 0.97, 0.0, +1.2, 1.5, ["friend", "hour!"], None),
]
