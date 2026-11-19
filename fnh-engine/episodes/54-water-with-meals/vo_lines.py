# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# FreshNestHub 54 — "Does drinking water while you eat water down your stomach acid?" (35-50 s rule; ONE takeaway: no - stomach acid is made with
# water anyway, and the stomach has sensors that turn the acid UP when food + water stretch it or the acid gets weaker; just sip, don't chug).
# Facts (verified 19 Nov 2026):
# - Mayo Clinic 'Water after meals: Does it disturb digestion?' (Mayo Clinic Staff, 7 Mar 2025, medical review 14 Feb 2025): 'Water doesn't cause problems
#   with digestion or thin body fluids used in digestion.' 'Water is part of the stomach acid that helps digestion'. Caveats: heart / kidney / liver disease
#   may need to limit water; water with meals can make you feel full faster.
# - Hackensack Meridian Health (30 Nov 2022, Dr Shamila Zawahir, gastroenterologist): the TikTok claim that water 'will dilute your stomach acid and slow down
#   digestion' -> 'there's no scientific evidence that water interferes with digestion in any way'.
# - StatPearls 'Physiology, Stomach' (NCBI Bookshelf NBK535425): gastric content pH ~1.0; 'Gastrin release occurs in response to increased gastric distension,
#   increased gastric pH' ...; 'Gastrin is capable of indirectly and directly increasing HCl production'; D cells switch it off when acidic enough.
# - THIP fact check (8 Mar 2023): 'No... no evidence that drinking water during meals interferes with digestion'; the gut adapts its secretions (1979 study).
# - India TV (20 Feb 2026, Dr Manan Vora): 'Only drinking a very large amount at once may cause temporary bloating or heaviness.'
LINES = [
    ("i1", "Do you know if drinking water while you eat really waters down your stomach acid?", 0.97, 0.25, +1.0, 1.55, ["acid?"], "q"),
    ("i2", "Every family has that one uncle who grabs your glass the second you sit down to eat.", 1.02, 0.3, +0.6, 1.5, [], "low"),
    ("a1", "Funny thing is, your stomach acid is made with water in the first place.", 1.0, 0.35, +1.2, 1.6, ["water"], "low"),
    ("b1", "When food and water stretch your stomach, tiny sensor cells notice.", 1.02, 0.1, +0.8, 1.5, ["notice.:dn"], "low"),
    ("b2", "They send out a signal called gastrin, and your stomach makes more acid.", 1.02, 0.3, +0.4, 1.5, ["more"], "low"),
    ("b3", "Water it down a bit? Same alarm, more acid, and it's back to normal.", 1.0, 0.3, +0.8, 1.55, ["normal.:dn"], "low"),
    ("c1", "That's why the Mayo Clinic says water doesn't thin your digestive juices.", 1.0, 0.3, +0.4, 1.5, ["thin"], "low"),
    ("c2", "Just sip it. Chugging a whole bottle can leave you feeling bloated.", 1.0, 0.3, -0.3, 1.35, ["bloated.:dn"], "low"),
    ("c3", "Send this to the uncle with the glass. Then pour yourself one.", 1.02, 0.0, +0.8, 1.45, ["one.:dn"], "low"),
]
