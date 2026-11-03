# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# FreshNestHub 22 — "Why does crispy namkeen go soft once you open the box?" Facts (verified 3 Nov 2026):
# - Fried / crisp snacks are hygroscopic, 'virtually water-free', pull moisture from the air (ScienceABC); crackers absorb ambient moisture (America's Test Kitchen).
# - Water moves from higher to lower water activity until balanced (ScienceABC; Baking Business: 'determines the direction of moisture flow').
#   Crackers aw 0.3, humid air 0.7, bread 0.95 (Globe and Mail, 'Bread turns hard but crackers soften').
# - Crisp = glassy; water = plasticizer -> 'glass to rubbery transition' (van Nieuwenhuijzen, Wageningen thesis 2008, edepot.wur.nl/121959; J Agric Food Chem 2008).
# - Critical aw where chips, popcorn, curls, saltines became unacceptable: 0.35-0.50 (Katz & Labuza 1981, via the WUR thesis; MeterGroup + Aqualab confirm the effect).
# - Burfi aw 0.79, moisture 14.67 % (Badola et al., J Food Sci Technol 2018, PMC6233429).
# - Soft + crisp together: crisp absorbs, soft dries out, same texture (King Arthur Baking 2023 + 2024; Exploratorium Science of Cooking). Namkeen + barfi = the same principle (our inference, said as 'the same thing').
# - Airtight keeps crisp (ScienceABC, Food Republic). Re-crisp: oven 120-150 C 5-10 min, microwave 20-30 s bursts (ScienceABC); ~107 C oven, cool then store (Food Republic); Cosmos (microwave expels moisture).
# - Softness is texture, not safety; rancidity = sharp, paint-like or crayon-like smell (ScienceABC; Baking Business on oxidation).
# VOICE upgrade (ep 22): LINKED LINES. pause_after 0.1 (x PZ 1.6 = 0.16 s with PMIN 0.15) between lines of one thought; thought boundaries keep 0.35-0.5.
LINES = [
    ("i1", "Do you know why crispy namkeen goes soft the second you open the box?", 1.00, 0.28, +1.0, 1.45, ["soft"], "q"),
    ("i2", "It isn't getting old, it's drinking the air in your kitchen.", 1.02, 0.1, +0.4, 1.45, ["drinking"], "low"),
    ("i3", "And that's the exact opposite of your bread, in the same kitchen.", 1.05, 0.4, -0.3, 1.4, ["opposite"], "low"),
    ("a1", "A fresh chakli has been fried until there's almost no water left in it.", 1.06, 0.1, +0.4, 1.45, ["almost"], "low"),
    ("a2", "That's the crunch. It's also the problem, because now it's thirsty.", 1.05, 0.35, +0.4, 1.45, ["thirsty.:dn"], "low"),
    ("a3", "Your kitchen air, though, is full of water. You just can't see it.", 1.05, 0.1, -0.3, 1.4, ["full"], "low"),
    ("a4", "And water has one habit: it moves from where there's more to where there's less, until both sides even out.", 1.08, 0.35, +0.4, 1.45, ["more", "less,"], "low"),
    ("b1", "Food scientists even measure this, on a thirst meter from zero to one. The lower the number, the thirstier it is.", 1.08, 0.3, +0.4, 1.45, ["meter", "thirstier"], "low"),
    ("b2", "A cracker sits around zero point three. Humid air sits around zero point seven.", 1.04, 0.1, +0.6, 1.45, ["three.", "seven.:dn"], "low"),
    ("b3", "So the moment that lid comes off, the water only goes one way.", 1.03, 0.35, +0.8, 1.5, ["one"], "low"),
    ("b4", "Bread's already full of water, so it isn't thirsty. Your namkeen is.", 1.05, 0.45, -0.3, 1.4, ["isn't", "is.:dn"], "low"),
    ("c1", "So why would a tiny bit of water kill the crunch? Picture this.", 1.03, 0.1, +0.8, 1.5, ["kill"], "low"),
    ("c2", "Dry spaghetti snaps. Cooked spaghetti bends. It's the same starch, and the only difference is water.", 1.05, 0.35, +0.6, 1.45, ["snaps.", "bends.", "water.:dn"], "low"),
    ("c3", "Your namkeen's the same. Dry, its starch is brittle, like glass, and scientists really do call that glassy.", 1.07, 0.1, +0.4, 1.45, ["glass,", "glassy.:dn"], "low"),
    ("c4", "A little water slips in between the starch molecules and loosens them up. Now it's rubbery.", 1.07, 0.1, +0.4, 1.45, ["slips", "rubbery.:dn"], "low"),
    ("c5", "And a snack that bends can't snap. No snap, no crunch.", 1.03, 0.45, +0.6, 1.45, ["bends", "crunch.:dn"], "low"),
    ("d1", "And it barely takes anything. In the classic study, chips and crackers got rejected at zero point three five to zero point five.", 1.09, 0.1, +0.4, 1.45, ["barely", "rejected"], "low"),
    ("d2", "A cracker starts at zero point three. That's only a couple of steps away.", 1.04, 0.45, +0.4, 1.45, ["couple"], "low"),
    ("e1", "But the real trap is your Diwali gift box.", 1.02, 0.1, -0.3, 1.4, ["trap"], "low"),
    ("e2", "Crispy namkeen, tucked right next to soft barfi, and barfi sits around zero point eight.", 1.07, 0.3, +0.4, 1.45, ["soft", "eight.:dn"], "low"),
    ("e3", "Bakers know this from cookies: store soft ones with crisp ones, and the crisp go soft while the soft dry out.", 1.08, 0.1, +0.4, 1.45, ["soft", "dry"], "low"),
    ("e4", "Your gift box does the same thing, and a closed lid can't save it.", 1.04, 0.45, -0.3, 1.35, ["same", "can't"], "low"),
    ("f1", "So, three things. Lid on right after you grab a handful, in an airtight jar.", 1.05, 0.3, +0.6, 1.45, ["three", "airtight"], "low"),
    ("f2", "Second, keep the crispy stuff and the soft sweets in separate boxes.", 1.04, 0.3, +0.4, 1.45, ["separate"], "low"),
    ("f3", "And if it's already soft, don't throw it. A few minutes in a low oven, or short bursts in the microwave.", 1.07, 0.1, +0.4, 1.45, ["don't", "few"], "low"),
    ("f4", "The heat drives the water back out. Just let it cool before the lid goes on.", 1.05, 0.45, +0.4, 1.45, ["back", "cool"], "low"),
    ("g1", "One honest catch. Soft is just a texture problem, but if it smells sharp, like paint or crayons, that's the oil going off. No oven fixes that, so bin it.", 1.08, 0.4, -0.3, 1.35, ["just", "paint", "bin"], "low"),
    ("h1", "So remember: lid on, sweets apart, and a little heat if it's gone soft.", 1.03, 0.35, +0.6, 1.45, ["lid", "apart,", "heat"], "low"),
    ("h2", "Send this to the friend who leaves the namkeen open all through Diwali!", 1.04, 0.0, +1.2, 1.5, ["friend", "open"], None),
]
