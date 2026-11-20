# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# FreshNestHub 57 — "Does cracking your knuckles cause arthritis?" (35-50 s rule; ONE takeaway: no - the pop is a gas pocket snapping open in the
# joint fluid when the bones are pulled apart, and a doctor who cracked one hand for fifty years found arthritis in neither).
# Facts (verified 20 Nov 2026):
# - Cleveland Clinic Health Essentials 'Is cracking your knuckles bad for you?' (Dr Wesley Baker, DO, 21 Sep 2026): 'No, popping your knuckles won't cause
#   arthritis'; gas in the synovial fluid; a 2015 study: the sound 'might actually be from the formation of a gas-filled cavity rather than from bubbles
#   popping'; see a provider if you notice swelling or crooked fingers; cracking should not hurt.
# - Harvard Health 'Does knuckle cracking cause arthritis?': 'probably won't raise your risk for arthritis' (several studies).
# - Kawchuk et al., PLoS ONE 2015 (PMC4398549; Univ. of Alberta release 15 Apr 2015): real-time MRI of a finger being pulled: cracking = 'cavity
#   inception rather than collapse of a pre-existing bubble'; refractory phase 'approximately 20 minutes' (Roston & Haines 1947).
# - Cedars-Sinai 'Ask a Doc' (Dr Robert Klapper, 2018): 'It does not lead to arthritis'; ~20 minutes before the same knuckle can crack again;
#   pain, swelling or limited motion = signs of damage.
# - Unger D., Arthritis & Rheumatism 1998 (via Scientific American, S. Mirsky, Dec 2009): left hand cracked at least twice a day for 50 years, right hand
#   as the control: 'no arthritis in either hand, and no apparent differences'; Ig Nobel Medicine 2009 (The Tech, 2 Oct 2009). One person = anecdote.
LINES = [
    ("i1", "Do you know if cracking your knuckles can actually give you arthritis?", 0.97, 0.25, +1.0, 1.55, ["arthritis?"], "q"),
    ("i2", "Your naanee says yes. Doctors at Harvard say... no.", 1.0, 0.35, +0.8, 1.55, ["no.:dn"], "low"),
    ("a1", "So what's that pop? Every knuckle sits in a tiny bag of slippery fluid.", 1.0, 0.1, +1.0, 1.55, ["pop?"], "low"),
    ("a2", "Pull the bones apart, and a tiny gas pocket snaps open, like a suction cup coming off glass.", 1.02, 0.3, +0.6, 1.5, ["snaps"], "low"),
    ("a3", "Scientists actually filmed it happening inside an MRI scanner.", 1.0, 0.3, +0.6, 1.5, ["filmed"], "low"),
    ("b1", "That's also why the same knuckle won't pop again for about twenty minutes.", 1.02, 0.35, +0.4, 1.5, ["twenty"], "low"),
    ("b2", "One doctor even tested it on himself. He cracked just one hand for fifty years, never the other.", 1.0, 0.3, +1.0, 1.55, ["one", "never"], "low"),
    ("b3", "And his result? Not a trace of arthritis in either hand.", 0.98, 0.35, +1.2, 1.6, ["either"], "low"),
    ("c1", "But if a knuckle ever hurts or swells up, show it to a doctor.", 1.0, 0.3, -0.3, 1.35, ["doctor.:dn"], "low"),
    ("c2", "Send this to the friend who cracks his knuckles all day.", 1.02, 0.0, +0.8, 1.45, ["day.:dn"], "low"),
]
