# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# FreshNestHub 18 — "Why does milk boil over but water never does?" (milk is ~90 % water, but its proteins (and fat) are
# surfactants: they sit on the surface of steam bubbles and stop them bursting, so bubbles pile up into foam (Mètode / University of
# Valencia, F. Sapiña; America's Test Kitchen: casein proteins stabilise the bubbles); as the milk heats, water evaporates off the top,
# the proteins + fat concentrate and set into a skin that traps the steam, which lifts the foam over the rim (The Kitchn; The
# Conversation). In water the bubbles burst the moment they reach the surface. Proof: one drop of dish soap makes plain water boil over
# (Mètode). Fixes: America's Test Kitchen found a spoon in the pot and a buttered rim only DELAY it; the only surefire fix is a big wide
# pot (4-quart pan for a pint of milk) because big bubbles pop despite the proteins; moderate heat (The Conversation), stir every few
# minutes to break the skin and let steam out, don't walk away (The Kitchn). Bonus: pasta water boils over because of starch (The Conversation).)
# SCRIPT upgrade (ep 18): the 'person talking' guide again, now with a running metaphor (protein = a JACKET on the bubble) that is
# paid off three times (jacket / no jacket / different jacket), a tested-fixes section with a ranking (what only delays vs what works),
# a kitchen demo people can do tonight (a drop of soap), and a joke on the universal moment (milk waits for the moment you check your phone).
# VOICE upgrade (ep 18): DROP-STRESS ('word:dn') on deadpan payoff words — a grown-up emphasises by dropping the pitch and lengthening
# the word, not by lifting it (A/B vs normal lift-stress on the same take, see improvements.md F). Registers per beat kept from ep 17.
LINES = [
    ("i1", "Do you know why milk boils over, but water never, ever does?", 0.96, 0.30, +1.0, 1.45, ["over,", "ever"], "q"),
    ("i2", "Same stove. Same pot. Water just sits there and bubbles. Milk climbs out like it's got somewhere to be.", 0.98, 0.45, +0.8, 1.5, ["Water", "Milk"], None),
    ("i3", "And the trick most of us use to stop it? It only buys you a few seconds. The one that actually works is coming up.", 0.97, 0.45, +0.6, 1.5, ["seconds,", "works"], None),
    ("a1", "Okay, water first. Steam bubbles rise, they reach the top... and pop. Gone.", 0.98, 0.40, +0.4, 1.45, ["pop.", "Gone.:dn"], "low"),
    ("a2", "Nothing holds them. So the water level never climbs.", 1.0, 0.45, +0.4, 1.45, ["Nothing", "never"], "low"),
    ("b1", "Milk looks like water. It's about ninety percent water. But that last ten percent changes everything.", 0.98, 0.40, +0.6, 1.5, ["ninety", "everything."], "low"),
    ("b2", "There's protein in there, a bit of fat, a bit of sugar. And the proteins love sitting on the edge of a bubble.", 1.03, 0.40, +0.4, 1.45, ["protein", "edge"], "low"),
    ("b3", "So a steam bubble rises through milk, and proteins wrap around it like a jacket. It reaches the top... and it doesn't pop.", 0.98, 0.45, +0.6, 1.5, ["jacket.", "doesn't"], "low"),
    ("b4", "That trick has a name: surfactant. Soap does it too, and that's why soap makes foam.", 1.0, 0.45, +0.4, 1.45, ["name:", "foam."], "low"),
    ("c1", "So the bubbles pile up, one on top of the other. That pile has a name too: foam.", 0.98, 0.40, +0.6, 1.5, ["pile", "foam."], "low"),
    ("c2", "Then it gets worse. As the milk heats, water evaporates off the top, so the proteins and fat up there get thicker.", 1.03, 0.35, +0.4, 1.45, ["worse.", "thicker"], "low"),
    ("c3", "They set into a skin. You've seen it. That wrinkly layer on hot milk.", 0.96, 0.45, -0.6, 1.4, ["skin.:dn", "wrinkly"], "low"),
    ("c4", "And the skin is a lid. The steam can't get out, so it lifts the whole foam up... and up... and over the edge.", 0.98, 0.45, +0.8, 1.5, ["lid.", "over"], None),
    ("c5", "Water can't do that. No proteins, no jacket, no skin, no lid.", 0.98, 0.50, +0.4, 1.45, ["can't", "lid.:dn"], "low"),
    ("d1", "Want proof? A scientist at the University of Valencia suggests this: a drop of dish soap in a pot of water. Then boil it.", 0.98, 0.40, +0.6, 1.5, ["proof?", "drop"], "low"),
    ("d2", "Plain water... now boils over. Same trick, different jacket.", 0.96, 0.50, +1.0, 1.5, ["over.", "different"], None),
    ("e1", "Okay, the fixes. America's Test Kitchen tried the classics.", 0.97, 0.40, +0.6, 1.45, ["fixes.", "classics."], None),
    ("e2", "A spoon left in the pot? Butter on the rim? They only delayed it. The milk still came over.", 1.0, 0.40, +0.4, 1.45, ["delayed:dn", "still"], "low"),
    ("e3", "The one that worked every time: a big, wide pot. Way bigger than feels right. About four litres of pot for half a litre of milk.", 0.98, 0.45, +0.8, 1.5, ["wide", "four"], "low"),
    ("e4", "In a wide pot the bubbles have room to grow big. And big bubbles pop, jacket or no jacket.", 1.02, 0.40, +0.4, 1.45, ["room", "pop,"], "low"),
    ("e5", "Two easy extras: moderate heat, and a stir every few minutes to break the skin and let the steam out.", 1.03, 0.40, +0.4, 1.45, ["moderate", "stir"], "low"),
    ("e6", "And don't walk away. Milk waits for the exact moment you check your phone.", 0.96, 0.50, -0.6, 1.4, ["exact", "phone.:dn"], "low"),
    ("f1", "Bonus: pasta water boils over too. Different jacket, same story. This time it's starch.", 0.98, 0.45, +0.6, 1.5, ["pasta", "starch.:dn"], "low"),
    ("g1", "Quick recap: proteins hold the bubbles, the skin traps the steam, the foam climbs. Wide pot, lower heat, stir.", 1.0, 0.40, +0.6, 1.45, ["bubbles,", "climbs."], "low"),
    ("g2", "Send this to the friend who's lost a pot of chai this week!", 0.97, 0.0, +1.2, 1.5, ["friend", "chai"], None),
]
