# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# FreshNestHub 75 — "Do sweets give you worms?" (35-50 s rule; ONE takeaway: worms don't come from sugar, they come from worm EGGS that travel
# poop -> soil (about 3 weeks) -> hands / unwashed veggies / water -> mouth, and hookworm through bare feet; so wash hands + veggies, wear chappals).
# Shape: an elder-said Indian habit myth (naani: 'too many laddoos = worms') -> 'Nope, myth' at ~10 % -> the egg's journey in 4 steps (define on sight)
# -> the payoff map 'soil, hands, mouth. Sugar isn't on the map' at ~60 % -> the tip -> send line = the naani with the laddoo tin.
# Respellings (Kokoro): laddoos -> luddoos, naani, chappals -> chuppuls (screen text keeps the normal spelling).
# VOICE upgrade (ep 75): TRIAD CADENCE A/B on the payoff a5 + the a3 list: continuation rises (:up) on the non-final items vs none (UPOFF=1).
# Facts (verified 28 Nov 2026):
# - Kokilaben Dhirubhai Ambani Hospital, 'Myth - Eating Sugar causes stomach worms in children': 'That is not true. Intestinal worms are usually
#   contracted due to unhygienic conditions.'
# - WHO fact sheet 'Soil-transmitted helminth infections' (18 Jan 2023): 'transmitted by eggs that are passed in the faeces of infected people'; eggs
#   attached to vegetables 'not carefully cooked, washed or peeled', 'contaminated water sources', children 'who play in the contaminated soil and then put
#   their hands in their mouths without washing them'; 'People become infected with hookworm primarily by walking barefoot on the contaminated soil';
#   'no direct person-to-person transmission ... eggs passed in faeces need about 3 weeks to mature in the soil'; 'do not multiply in the human host'.
# - CDC 'About Soil-transmitted Helminths' (2024): prevention 'Wash your hands before handling food', 'Wash, peel, and cook raw fruits and vegetables',
#   'Wear shoes when walking in soil that may be contaminated'; hookworm 'spreads primarily by walking barefoot on contaminated soil'.
LINES = [
    ("i1", "Do you know if eating too many sweets gives you worms?", 0.97, 0.1, +1.0, 1.55, ["worms?"], "q"),
    ("i2", "Nope. That's a myth. No amount of luddoos can make a worm.", 1.02, 0.3, +1.2, 1.6, ["Nope.", "worm.:dn"], "low"),
    ("a1", "Worms start as tiny eggs, and those eggs come out in an infected person's poop.", 1.04, 0.3, +0.8, 1.5, ["eggs,", "poop."], "low"),
    ("a2", "If there's no toilet, they end up in the soil, where they wait about three weeks to get ready.", 1.05, 0.3, +0.4, 1.5, ["soil,", "three"], "low"),
    ("a3", "Then they hitch a ride on dirty hands, on unwashed veggies, or in dirty water.", 1.05, 0.25, +0.6, 1.5, ["hands,", "water."], "low"),
    ("a4", "And one kind doesn't even need your mouth. It gets in through bare feet.", 1.03, 0.3, +0.8, 1.55, ["mouth.", "bare"], "low"),
    ("a5", "So the real route is soil. Hands. Mouth. Sugar isn't even on the map.", 1.02, 0.3, +1.0, 1.6, ["Mouth.", "map.:dn"], "low"),
    ("c1", "Wash your hands before you eat, wash the veggies, and wear chuppuls outside.", 1.04, 0.3, -0.2, 1.4, ["wash", "chuppuls"], "low"),
    ("c2", "Send this to the naani who hides the luddoo tin to save you from worms!", 1.06, 0.0, +0.8, 1.45, ["hides"], "low"),
]
