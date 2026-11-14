# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# FreshNestHub 36 — "Why do fizzy drinks give you hiccups?" (35-50 s rule; ONE takeaway: the fizz stretches your stomach right under the diaphragm,
# the nerves there trip a reflex: the diaphragm jerks down, the vocal cords slam shut = HIC)
# METAPHOR for the whole video: a BALLOON under a DRUM-SKIN floor (stomach under the diaphragm) + a DOOR that slams (vocal cords).
# Facts (verified 14 Nov 2026):
# - Cleveland Clinic 'Hiccups' (med. reviewed, 17 Apr 2024): repeated spasms of the diaphragm + a 'hic' from the vocal cords closing; the diaphragm pulls
#   down suddenly and sucks in air, the glottis closes; causes incl. carbonated beverages, eating too much / too fast, swallowing air; irritated vagus /
#   phrenic nerves; transient hiccups go away within minutes; call a provider if they last longer than two days; 'experts haven't found a hiccup cure'.
# - Cleveland Clinic Health Essentials (Dr Kayla Rapp, 28 Oct 2025): 'a hiccup is basically a muscle spasm', irritated diaphragm, vocal cords close.
# - The Conversation / Western Sydney University (2023): 'the most common is stretching the stomach from eating a large meal or drinking soft drinks';
#   involuntary diaphragm contractions + sudden vocal-cord closure; < 48 h unconcerning; hiccups seen in healthy fetuses on ultrasound.
# - NHS 'Hiccups' (reviewed 23 Jun 2023): should only last a few minutes; see a GP if longer than 48 hours; fizzy drinks make you swallow air.
# - Live Science 'Why do we hiccup?' (A. P. Taylor, 7 Dec 2019): hiccupping recorded in the womb as early as nine weeks (L. Fabrizi, UCL); why we hiccup
#   is a mystery; theory = practice for breathing.
LINES = [
    ("i1", "Do you know why you get hiccups after a fizzy drink?", 1.0, 0.25, +1.0, 1.55, ["hiccups", "fizzy"], "q"),
    ("i2", "It's not the bubbles tickling your throat. It's your stomach.", 1.0, 0.3, +1.0, 1.6, ["not", "stomach.:dn"], "low"),
    ("a1", "Right under your lungs sits a dome of muscle, your diaphragm. It pulls down every time you breathe in.", 1.03, 0.25, +0.4, 1.45, ["diaphragm."], "low"),
    ("a2", "A fizzy drink fills your stomach with gas, so it stretches fast, like a balloon, right under your diaphragm.", 1.03, 0.3, +0.8, 1.5, ["gas,", "balloon,"], "low"),
    ("a3", "The nerves there get irritated, and your diaphragm jerks down. Air rushes in,", 1.0, 0.1, +0.8, 1.5, ["jerks"], "low"),
    ("a4", "and your vocal cords slam shut, like a door. Hic! That slam is the sound.", 1.0, 0.35, +1.2, 1.6, ["door.", "sound.:dn"], "low"),
    ("b1", "Most hiccups stop in a few minutes. If they last more than two days, see a doctor.", 1.0, 0.3, -0.3, 1.35, ["two"], "low"),
    ("c1", "Weird bonus: you were hiccupping in the womb, before you were even born.", 0.98, 0.3, +0.8, 1.5, ["womb,", "born.:dn"], "low"),
    ("c2", "Send this to the friend on their third fizzy drink at this party.", 1.02, 0.0, +0.8, 1.45, ["third"], "low"),
]
