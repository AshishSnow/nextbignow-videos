# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# FreshNestHub 09 — "Spicy food doesn't burn you — it tricks your brain" (capsaicin + heat sensors, milk vs water, birds)
# Voice upgrade (ep 09): per-line speed variety — questions/reveals slower (0.96-0.97), quick facts faster (1.02-1.03),
# explanations 1.0; "..." before payoff words for a breath; lines kept short, contractions (ear-writing).
LINES = [
    ("i1", "Do you know spicy food... doesn't actually burn you?", 0.96, 0.30, +1.0, 1.45, ["spicy", "burn"], "q"),
    ("i2", "Your mouth feels on fire. But nothing is really burning. It's a trick!", 1.0, 0.45, +1.2, 1.5, ["fire.", "nothing", "trick!"], None),
    ("a1", "The trickster is a chemical in chili peppers, called capsaicin.", 1.0, 0.40, +0.8, 1.45, ["chili", "capsaicin."], None),
    ("a2", "Your tongue is packed with tiny nerve endings. Think of them as wires to your brain.", 1.02, 0.40, +0.8, 1.45, ["nerve", "wires"], None),
    ("a3", "And on those nerves sit little heat alarms.", 0.97, 0.40, +1.0, 1.5, ["heat", "alarms."], None),
    ("a4", "Normally, they only go off for painful heat... like a scalding sip of tea.", 1.0, 0.40, +0.8, 1.45, ["painful", "scalding"], None),
    ("a5", "But capsaicin fits those alarms perfectly. Like a key in a lock!", 1.0, 0.40, +1.0, 1.5, ["perfectly.", "key"], None),
    ("a6", "Click! The alarm rings, and your nerves shout to your brain... FIRE!", 1.0, 0.45, +1.2, 1.5, ["Click!", "FIRE!"], None),
    ("a7", "Your brain believes it. So you feel burning... with no real fire at all.", 0.97, 0.45, +0.8, 1.45, ["believes", "no"], "low"),
    ("b1", "Finding these heat alarms was such a big deal, it helped win a Nobel Prize in 2021!", 1.02, 0.45, +1.0, 1.5, ["Nobel", "Prize"], None),
    ("c1", "So how do you put out a fake fire?", 1.0, 0.35, +1.0, 1.5, ["fake", "fire?"], "q"),
    ("c2", "Scientists tested seven drinks on seventy-two people eating spicy sauce.", 1.0, 0.35, +0.8, 1.45, ["seven", "seventy-two"], None),
    ("c3", "Water helped a little. Fizzy drinks did badly. And the winner... milk!", 1.0, 0.45, +1.0, 1.5, ["little.", "badly.", "milk!"], None),
    ("c4", "Even skim milk worked almost as well as whole milk. Scientists think milk's proteins help.", 1.02, 0.45, +0.8, 1.45, ["skim", "proteins"], None),
    ("d1", "Now here's the weirdest part. Birds can't feel the burn at all!", 0.97, 0.40, +1.2, 1.5, ["weirdest", "Birds", "all!"], None),
    ("d2", "They happily eat hot chili peppers, then drop the seeds somewhere new, ready to grow.", 1.03, 0.40, +0.8, 1.45, ["happily", "grow."], None),
    ("d3", "But mice chew the seeds to bits. So the burn keeps them away.", 1.0, 0.40, +0.8, 1.45, ["chew", "away."], None),
    ("d4", "Scientists think that's why chilis are spicy. To pick who eats them!", 0.98, 0.45, +1.0, 1.5, ["spicy.", "pick"], None),
    ("e1", "So remember: spicy is a trick, not a burn. And milk beats water.", 0.98, 0.45, +0.8, 1.45, ["trick,", "milk"], "low"),
    ("e2", "Send this to the friend who chugs water after every spicy bite!", 1.0, 0.0, +1.2, 1.5, ["friend", "water"], None),
]
