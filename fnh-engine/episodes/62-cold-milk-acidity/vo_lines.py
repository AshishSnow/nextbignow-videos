# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# FreshNestHub 62 — "Does cold milk cure acidity?" (35-50 s rule; ONE takeaway: milk calms the burn for a bit, then its protein makes your
# stomach make MORE acid, and full-fat milk loosens the valve -> quick relief, then a comeback; burn > twice a week = see a doctor).
# Elder-said Indian home fix (mom) -> 'calms the burn for a bit' at ~20 %, 'makes MORE acid' at ~42 %, the 1976 test as proof, the valve, the tip,
# send line = whoever keeps cold milk by the bed.
# VOICE upgrade (ep 62): PAYOFF SLOW-DOWN — the payoff line a1 at speed 0.95 with a '...' before 'more' vs 1.0 (A/B on identical other lines).
# Facts (verified 25 Nov 2026):
# - Ippoliti, Maxwell, Isenberg, 'The Effect of Various Forms of Milk on Gastric-Acid Secretion', Annals of Internal Medicine 1976;84(3):286-289:
#   'A significant increase in acid secretion ... was produced by 240 ml of whole, low-fat, and nonfat milk' (duodenal-ulcer patients + normal subjects).
# - AOL / Prevention (Dr Jamie Koufman + RD Lauren O'Connor): milk 'only offers temporary relief for heartburn'; high pH balances acidity;
#   'gastrin also elicits more stomach acid'; 'not enough scientific evidence' as a remedy.
# - Healthline (med. reviewed): 'High fat foods relax the LES muscles, making it easier for the stomach's contents to reflux back up';
#   protein -> gastrin -> 'secretion of stomach acid'.
# - Bon Secours (hospital system): fat 'relaxes the muscles in the esophageal sphincter'; protein 'involved in the secretion of stomach acid';
#   'you may need to see a doctor if you experience it more than twice a week.'
# - Gastroenterology Consultants of San Antonio (2024): 'milk might not be the effective remedy for heartburn it's often thought to be'.
LINES = [
    ("i1", "Do you know if a glass of cold milk can really cure acidity?", 0.97, 0.1, +1.0, 1.55, ["cure"], "q"),
    ("i2", "Your mom swears by it, and for a few minutes, it kind of works.", 1.0, 0.25, +1.2, 1.6, ["swears"], "low"),
    ("i3", "Milk isn't acidic, so it calms the burn for a bit.", 1.02, 0.35, +0.6, 1.5, ["calms"], "low"),
    ("a1", "But then your stomach notices all that protein, and makes more acid to digest it.", 1.0, 0.35, +1.0, 1.6, ["more"], "low"),
    ("a2", "Doctors tested this in nineteen seventy-six. Whole milk, low-fat, even skim. All of them raised the acid.", 1.03, 0.3, +0.6, 1.5, ["skim.", "raised"], "low"),
    ("b1", "And the fat in full-cream milk loosens the little valve that keeps acid down in your stomach.", 1.03, 0.3, +0.4, 1.5, ["loosens"], "low"),
    ("c1", "If the burn shows up more than twice a week, that's a job for a doctor, not for milk.", 1.02, 0.3, -0.3, 1.35, ["doctor,", "milk.:dn"], "low"),
    ("c2", "Send this to whoever keeps a glass of cold milk by the bed for acidity.", 1.04, 0.0, +0.8, 1.45, ["bed"], "low"),
]
