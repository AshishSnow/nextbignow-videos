# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# FreshNestHub 60 — "Does spicy food give you stomach ulcers?" (35-50 s rule; ONE takeaway: chilli doesn't cause ulcers - mostly a germ
# (H. pylori) or regular painkillers do; spice can only sting one that's already there). Elder-said myth (the uncle) -> the culprit flip at ~12 %,
# the two causes by ~25 %, the PROOF STORY (1982, stress was blamed; one doctor drank the germ; Nobel 2005), safe tip, send line = the uncle.
# VOICE upgrade (ep 60): the RHETORICAL QUESTION on its own LINKED line ('So how do you prove it?' with a q rise, pause 0.1, then the answer)
# A/B vs the merged statement ('To prove it, one of them drank the germs.').
# Facts (verified 23 Nov 2026):
# - Harvard Health 'Medical myths: does food cause ulcers?' (Apr 2026): 'foods have little or nothing to do with ulcer development'; 'the vast
#   majority of peptic ulcers have one of two causes': 'a bacterial infection (Helicobacter pylori)' and 'NSAIDs, such as ibuprofen or aspirin'.
# - University Hospitals (Dr Abbass, Nov 2025): 'Forget what you've heard about spicy foods causing peptic ulcers'; most common cause 'regular use of
#   NSAIDs'; 'The majority of people with H. pylori never get ulcers'; 'If your upper abdominal pain is recurrent, persistent or it gets worse, it
#   should not be ignored.'
# - Live Science: 'spicy food doesn't cause ulcers, though it can irritate existing ulcers'; the real culprit for most = H. pylori.
# - Nobel Prize press release 2005: Marshall + Warren, 'In 1982 ... stress and lifestyle were considered the major causes of peptic ulcer disease';
#   H. pylori 'colonizes the stomach in about 50% of all humans'. BMJ 2005 (Watts): 'Marshall swallowed a culture of the bacteria, developed gastritis'.
LINES = [
    ("i1", "Do you know if spicy food can give you a stomach ulcer?", 0.97, 0.25, +1.0, 1.55, ["ulcer?"], "q"),
    ("i2", "Every uncle says yes. But the real culprit? It isn't the chilli.", 1.0, 0.35, +0.8, 1.55, ["isn't"], "low"),
    ("a1", "Most ulcers come from a germ called aitch pylori, or from taking painkillers like aspirin a lot.", 1.04, 0.3, +0.6, 1.5, ["germ"], "low"),
    ("a2", "Spicy food can sting an ulcer that's already there. It just can't make one.", 1.0, 0.35, +0.8, 1.55, ["sting", "one.:dn"], "low"),
    ("b1", "Back in nineteen eighty-two, doctors blamed stress. Then two Australian doctors found the germ.", 1.04, 0.3, +0.9, 1.5, ["stress."], "low"),
    ("b2q", "So how do you prove it?", 0.98, 0.1, +1.2, 1.6, ["prove"], "q"),
    ("b2", "One of them drank the germs. On purpose.", 1.0, 0.3, +0.8, 1.55, ["drank", "purpose.:dn"], "low"),
    ("b3", "Days later, his stomach was inflamed. In two thousand five, a Nobel Prize.", 1.0, 0.35, +1.2, 1.6, ["Nobel"], "low"),
    ("c1", "If your upper belly keeps hurting, it's time to see a doctor. Just don't blame the chilli.", 1.02, 0.3, -0.3, 1.35, ["chilli.:dn"], "low"),
    ("c2", "Send this to the uncle who pushes the chilli away at every dinner.", 1.04, 0.0, +0.8, 1.45, ["dinner."], "low"),
]
