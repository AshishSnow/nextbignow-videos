# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# HOW IT WORKS · EP 2 — "Why your credit score doesn't know your salary" (five slices; the last one catches people who pay on time). Written + reviewed by the R&D run 4 Nov 2026.
# Facts: SOURCES.md. Education only: US FICO, no card/loan/repair product advice, no income or score promises.
SERIES = "HOW IT WORKS"; PART = 0; EP = 2
LINES = [
    ("i1", "Your credit score can raise your car loan's cost. So why doesn't it know your salary?", 1.02, 0.35, +1.0, 1.45, ['raise', 'salary?'], None),
    ("i2", "You're twenty-four in the US, with a good job, and you want a car loan.", 1.04, 0.25, +0.8, 1.45, ['twenty-four', 'want'], 'low'),
    ("i3", "But FICO, a major credit score, doesn't count your pay, your job or your age.", 1.04, 0.2, +0.6, 1.45, ["doesn't", 'age.:dn'], 'low'),
    ("i4", "Your lender can still ask your income. The score just won't see it.", 1.04, 0.3, +0.6, 1.45, ['still', 'see'], 'low'),
    ("i5", 'So what does it count? Five slices. And the last one catches people who pay on time.', 1.04, 0.35, +0.8, 1.45, ['Five', 'last', 'time.:dn'], 'low'),
    ("a1", "Slice one. New credit, worth ten percent.", 1.02, 0.15, +0.8, 1.35, ["New", "ten"], "low"),
    ("a2", "Open several accounts in a short time, and you look riskier.", 1.04, 0.25, +0.6, 1.45, ["several", "riskier.:dn"], "low"),
    ("b1", 'Slice two. Your mix of cards and loans. Ten percent again.', 1.04, 0.25, +0.8, 1.45, ['mix', 'again.:dn'], 'low'),
    ("b2", "But FICO says you don't need one of each.", 1.04, 0.25, +0.6, 1.45, ["don't"], 'low'),
    ("c1", "Slice three. How long you've had credit. Fifteen percent.", 1.02, 0.15, +0.8, 1.35, ["long", "Fifteen"], "low"),
    ("c2", "Longer usually helps, but it isn't required.", 1.04, 0.25, +0.6, 1.45, ['helps,', "isn't"], 'low'),
    ("c3", "That's barely a third so far. So where's the rest of the pie?", 1.04, 0.35, +0.8, 1.45, ['barely', 'rest'], None),
    ("d1", "Slice four. Do you pay on time? Thirty-five percent, the biggest slice.", 1.02, 0.20, +0.8, 1.35, ["time?", "biggest"], "low"),
    ("d3", "Late payments can lower it. But FICO says a few aren't an automatic score killer.", 1.04, 0.35, +0.6, 1.45, ['lower', 'automatic'], 'low'),
    ("e1", "Slice five. How much you owe. Thirty percent. And here's the catch.", 1.02, 0.25, +0.8, 1.35, ["owe.", "catch.:dn"], "low"),
    ("e2", "You pay your card in full every month. So you owe nothing, right?", 1.04, 0.25, +0.6, 1.45, ["full", "right?"], None),
    ("e3", 'But card companies usually report your balance when each monthly statement ends. That can be before you pay.', 1.04, 0.2, +0.6, 1.45, ['report', 'before'], 'low'),
    ("e4", 'So Experian says your card can look heavily used, even when you pay in full.', 1.02, 0.2, +0.6, 1.45, ['heavily', 'full.:dn'], 'low'),
    ("e5", 'Paying before the statement ends may lower what gets reported.', 1.02, 0.35, +0.6, 1.45, ['before', 'lower'], 'low'),
    ("f1", "Here's why it doesn't know your salary. All of this comes from your credit report, and income isn't on it.", 1.04, 0.25, +0.8, 1.45, ['why', "isn't"], 'low'),
    ("f1b", 'But reports can be wrong.', 1.02, 0.2, +0.6, 1.45, ['wrong.:dn'], 'low'),
    ("f2", "In a federal study back in twenty thirteen, one in five people found an error.", 1.02, 0.20, +0.6, 1.45, ["federal", "five"], "low"),
    ("f3", "Some of those errors could mean paying more for a loan.", 1.02, 0.35, +0.6, 1.45, ["more"], "low"),
    ("t1", "So check yours. Free, every week, at AnnualCreditReport dot com.", 1.0, 0.25, +0.8, 1.45, ["check", "Free,"], "low"),
    ("t2", "Looking at your own won't lower your score.", 1.02, 0.25, +0.6, 1.45, ["own", "won't"], "low"),
    ("z1", "Save this. Should your salary count? Comment YES or NO.", 1.04, 0.20, +1.0, 1.45, ["Save", "salary", "NO."], None),
    ("z2", "Send this to the friend who's buying a car.", 1.06, 0.0, +1.0, 1.45, ["friend", "car."], None),
]
