# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# FreshNestHub 71 — "Does vitamin C stop a cold?" (35-50 s rule; ONE takeaway: a daily vitamin C habit does NOT stop most people catching colds; it only
# makes them a bit shorter; the twist: people under extreme physical stress caught half as many).
# Shape: hook -> 'Nope' at ~8 % -> the proof (29 trials, 11,306 people, colds came just as often) -> 'so why does everyone believe it?' -> the ORIGIN
# (1970, a scientist with two Nobel Prizes, a hit book) -> what it really does (a bit shorter; no clear effect once you're sick) -> the twist group -> takeaway
# -> send line = the friend who downs orange juice the second they sneeze.
# VOICE upgrade (ep 71): CASUAL ANSWER WORD A/B: 'Nope.' vs 'No.' in i2 on identical other lines (does the everyday word sound as natural to UTMOS?).
# Facts (verified 27 Nov 2026):
# - Cochrane review CD000980 (Hemila & Chalker, 31 Jan 2013): 'Regular ingestion of vitamin C had no effect on common cold incidence in the ordinary
#   population, based on 29 trial comparisons involving 11,306 participants.' Duration: 'In adults the duration of colds was reduced by 8% ... and in
#   children by 14%'. 'In five trials with 598 participants exposed to short periods of extreme physical stress (including marathon runners and skiers)
#   vitamin C halved the common cold risk' (abstract: 'marathon runners, skiers and soldiers on subarctic exercises', RR 0.48). 'Trials of high doses of
#   vitamin C administered therapeutically, starting after the onset of symptoms, showed no consistent effect on the duration or severity'.
# - NIH ODS vitamin C consumer fact sheet: 'for most people, vitamin C supplements do not reduce the risk of getting the common cold ... might have
#   slightly shorter colds ... Using vitamin C supplements after cold symptoms start does not appear to be helpful.' Food: citrus, peppers, kiwifruit...
# - Popular Science (Chodosh 2017/2021): 'Linus Pauling won two Nobel Prizes'; 'When he published a book on the matter in 1970, Vitamin C and the
#   Common Cold, the American public went crazy for it.'  Wikipedia (the book): 1970, 'a rush of vitamin C sales'; scientists criticised it.
LINES = [
    ("i1", "Do you know if vitamin C can stop a cold?", 0.97, 0.1, +1.0, 1.55, ["stop"], "q"),
    ("i2", "For most people? Nope. Taking it every day won't stop you catching one.", 1.02, 0.3, +1.2, 1.6, ["Nope.", "won't"], "low"),
    ("a1", "Across twenty-nine trials and eleven thousand people, the colds came just as often.", 1.05, 0.3, +0.4, 1.5, ["just"], "low"),
    ("a2", "So why does everyone believe it?", 0.98, 0.1, +1.0, 1.6, ["everyone"], "q"),
    ("a3", "In nineteen seventy, a two-time Nobel winner wrote a book saying it works, and people went crazy for it.", 1.06, 0.3, +0.8, 1.55, ["two-time", "crazy"], "low"),
    ("a4", "What it really does is small: taken daily, your colds end a bit sooner.", 1.04, 0.3, -0.3, 1.4, ["small:", "sooner."], "low"),
    ("a5", "Except for one group: marathon runners, skiers, and soldiers training in the freezing cold. Their colds dropped by half.", 1.05, 0.3, +0.8, 1.6, ["half.:dn"], "low"),
    ("c1", "So eat oranges because they're good food, not a cold shield.", 1.03, 0.3, -0.2, 1.4, ["food,", "shield."], "low"),
    ("c2", "Send this to the friend who downs orange juice the second they sneeze!", 1.06, 0.0, +0.8, 1.45, ["sneeze!"], "low"),
]
