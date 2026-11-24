# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# FreshNestHub 61 — "Does sitting too close to the TV ruin your eyes?" (35-50 s rule; ONE takeaway: no lasting damage, only tired / dry eyes;
# the fear began with some 1960s colour TVs that leaked radiation and were recalled; a kid who ALWAYS sits close may be nearsighted = a SIGN,
# not the cause). Elder-said myth (mom) -> 'won't damage them' at ~17 %, the origin story by ~45 %, the sign-not-cause twist, eye check, send line = mom.
# VOICE upgrade (ep 61): the LINKED HOOK — the hook question flows into the first answer line with a 0.1 s link instead of a 0.25 s pause
# (A/B on identical text: UTMOS of i1/i2 + chunk20, and the time to the payoff).
# Facts (verified 24 Nov 2026):
# - AAO 'Can sitting too close to the TV damage your eyes?': 'sitting too close to a TV will not damage your eyes but it may cause eyestrain';
#   'Children can focus at close distance without eyestrain better than adults.'
# - KSDK Verify (Eye Consultants of Atlanta / Paul Vision Institute): it 'will not damage vision in children or adults'; dry, uncomfortable eyes;
#   'blink frequently'; habitually sitting too close 'may signal that an adult or child is nearsighted and may need glasses'.
# - Scientific American (EarthTalk, quoting AAO's Dr Lee Duffner): 'won't cause any physical damage'; 'back in the 1960s General Electric sold some
#   new-fangled color TV sets that emitted excessive amounts of radiation'; recalled and repaired; 'electronic emissions aren't an issue with TVs
#   made any time after 1968'; a child may sit close 'because he or she is nearsighted and undiagnosed' -> 'get his or her eyes tested'.
# - The Star QuickCheck (10 Jun 2026): early-1960s recall of colour sets 'emitting X-ray radiation at levels far above what was considered safe'.
LINES = [
    ("i1", "Do you know if sitting too close to the TV can ruin your eyes?", 0.97, 0.1, +1.0, 1.55, ["ruin"], "q"),
    ("i2", "Every mom has yelled it at least once. Sit back, you'll ruin your eyes!", 1.0, 0.3, +1.4, 1.65, ["back,"], "low"),
    ("i3", "But eye doctors say... it won't damage them.", 1.0, 0.35, +0.8, 1.55, ["won't"], "low"),
    ("a1q", "So where did that fear come from?", 0.98, 0.1, +1.2, 1.6, ["fear"], "q"),
    ("a1", "The nineteen sixties. Some new colour TVs leaked radiation, way above the safe level.", 1.03, 0.3, +0.9, 1.55, ["radiation,"], "low"),
    ("a2", "They got recalled and fixed, and TVs made after nineteen sixty-eight don't have that problem.", 1.04, 0.35, +0.6, 1.5, ["fixed,"], "low"),
    ("b1", "Sitting close today just gives you tired, dry eyes, because you forget to blink.", 1.02, 0.3, +0.4, 1.5, ["blink.:dn"], "low"),
    ("b2", "And kids can actually focus up close better than grown-ups.", 1.02, 0.25, +0.8, 1.55, ["better"], "low"),
    ("b3", "But if your kid always sits close, that could be a sign they're nearsighted. Get their eyes checked.", 1.02, 0.3, -0.3, 1.35, ["sign", "checked.:dn"], "low"),
    ("c1", "Send this to the mom who still yells sit back every time the TV is on.", 1.04, 0.0, +0.8, 1.45, ["back"], "low"),
]
