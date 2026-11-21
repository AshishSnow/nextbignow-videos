# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# FreshNestHub 58 — "Does reading in dim light ruin your eyes?" (35-50 s rule; ONE takeaway: no lasting damage - dim light only causes
# temporary eye strain; what really changes kids' eyes is too little time outdoors in daylight).
# Shape (SCRIPT_FEEL): macro loop opened in i2 ('the real risk is somewhere else'), micro loops a1 ('why do they ache?') and b1
# ('so where's the real risk?'), but/so turns, the send line calls back to line 2 (the mom).
# Facts (verified 21 Nov 2026):
# - Johns Hopkins Medicine 'Six Children's Eye Health Misconceptions Demystified' (K. Funari OD MPH, E. Min OD, Jun 2026): in dim light 'your eyes must
#   work harder to focus, which can lead to eye strain, headaches, fatigue and blurry vision - but these effects are short term and temporary. They go
#   away once you rest your eyes.' 'There is no evidence that dim light causes permanent damage'; myopia progression = 'the lack of outdoor time and a
#   decrease in reading distance ... and not the dim lighting.'
# - University of Utah Health (Moran Eye Center, G. Hulewsky OD, 2021): 'reading in dim light will not hurt your eyes.'
# - WebMD archive (Dr Richard Gans, Cleveland Clinic Cole Eye Institute): no evidence of long-term harm; reading in insufficient light -> 'short-term
#   drying of eyes because you blink less often'; doesn't damage the structure or function of the eyes.
# - American Academy of Ophthalmology 'Prevent childhood myopia with sunshine and outdoor time' (Dr Noha Ekdawi): 'Nearsightedness happens when the eye
#   grows too long from front to back'; 'at least one to two hours of outdoor time each day'; mechanism 'unclear', one idea = sunlight raises dopamine
#   in the eye, which controls its growth.
# - National Academies (NASEM) myopia report news release, 17 Sep 2024: 'one to two hours outdoors each day for children'; 'unequivocal evidence that
#   increased time outdoors slows excessive eye growth in children and therefore reduces the risk of developing myopia.'
LINES = [
    ("i1", "Do you know if reading in dim light can actually ruin your eyes?", 0.97, 0.25, +1.0, 1.55, ["ruin"], "q"),
    ("i2", "Your mom says yes. But eye doctors say... no. The real risk is hiding somewhere else.", 1.0, 0.35, +0.8, 1.55, ["no."], "low"),
    ("a1", "So why do your eyes ache? In dim light, they have to work extra hard to focus.", 1.0, 0.1, +1.0, 1.55, ["ache?"], "low"),
    ("a2", "And you blink less, so they dry out. That's eye strain, and it goes away once you rest.", 1.02, 0.35, +0.6, 1.5, ["rest.:dn"], "low"),
    ("b1", "So where's the real risk? It's not the dim light. It's too little sunlight.", 0.98, 0.3, +1.2, 1.6, ["sunlight.:dn"], "low"),
    ("b2", "Kids who play outside for one to two hours a day are less likely to become nearsighted.", 1.0, 0.3, +0.8, 1.55, ["outside"], "low"),
    ("b3", "Experts think all that bright daylight helps stop the eyeball from growing too long.", 1.0, 0.35, +0.6, 1.5, ["long."], "low"),
    ("c1", "But if the words still look blurry in good light, it's time to get your eyes checked.", 1.0, 0.3, -0.3, 1.35, ["checked.:dn"], "low"),
    ("c2", "Send this to the mom who still yells, you'll ruin your eyes!", 1.02, 0.0, +0.8, 1.45, ["eyes!"], "low"),
]
