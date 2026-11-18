# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# FreshNestHub 52 — "Does drinking water standing up hurt your knees?" (35-50 s rule; ONE takeaway: water doesn't fall into your knees - the food pipe is a
# MUSCLE that squeezes every sip down in any position, the gut soaks it into the blood, and joint fluid is made from blood, so posture doesn't matter).
# Facts (verified 18 Nov 2026):
# - Medical Dialogues fact check (9/11 Oct 2024, medically reviewed): claim 'False'; Dr Raju Vaishya (orthopaedics, Indraprastha Apollo): drinking 'whether standing
#   or sitting' 'does not change how your body absorbs and utilizes it for joint health'; Dr Anup Khatri: 'no studies or evidence available that prove the connection'.
# - NewsMeter fact check (9 Jun 2023): 'false'; Dr Anurag Sharma (orthopaedic surgeon): 'There is no medical evidence to support such a theory'.
# - NIDDK 'Your digestive system & how it works': 'After you swallow, peristalsis pushes the food down your esophagus into your stomach'; the small intestine
#   'absorb[s] water and the digested nutrients into your bloodstream'; the large intestine moves more water into the bloodstream.
# - Binghamton University / The Conversation (S. Venkatesan, 3 Aug 2026): 'Swallowing does not depend on gravity. People can swallow while lying down, and
#   astronauts clearly eat and drink in orbit.'
# - Cleveland Clinic 'Synovial fluid' (updated 9 Mar 2026): 'Your body makes joint fluid from the plasma in your blood.'
LINES = [
    ("i1", "Do you know if drinking water standing up really hurts your knees?", 0.97, 0.25, +1.0, 1.55, ["knees?"], "q"),
    ("i2", "Your naanee swears it does. Bone doctors say it's a myth.", 1.0, 0.3, +0.8, 1.55, ["myth.:dn"], "low"),
    ("a1", "The idea is, water drunk standing falls straight down and slams into your knees.", 1.02, 0.25, +0.4, 1.5, ["slams"], "low"),
    ("a2", "But your food pipe isn't a slide. It's a muscle, and it squeezes every sip down in a wave.", 1.0, 0.3, +1.2, 1.6, ["muscle,"], "low"),
    ("a3", "Standing, sitting, lying down, it works the same. Astronauts drink with no up at all.", 1.02, 0.3, +0.8, 1.5, ["Astronauts"], "low"),
    ("b1", "And the water never goes near your knees. Your gut soaks it into your blood first.", 1.02, 0.25, +0.8, 1.5, ["blood"], "low"),
    ("b2", "Their slippery joint fluid is made from that blood, so posture doesn't matter.", 1.0, 0.3, +0.4, 1.5, ["matter.:dn"], "low"),
    ("c1", "If your knees really hurt, ask a doctor. Just don't blame the glass.", 1.0, 0.3, -0.3, 1.35, ["glass.:dn"], "low"),
    ("c2", "Send this to whoever yells sit down every time you grab a glass.", 1.02, 0.0, +0.8, 1.45, ["sit"], "low"),
]
