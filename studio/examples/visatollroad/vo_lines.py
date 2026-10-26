# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# "Visa never lends you a dollar, yet keeps about half its revenue as profit" (Visa FY2025 10-K + Q4 FY2025 8-K)
LINES = [
    ("i1", "Did you know Visa never lends you a single dollar… yet it keeps about half of everything it makes as profit?", 1.08, 0.25, +1.0, 1.4, ["never", "half"], "q"),
    ("i2", "No loans. No interest. So what's the trick?", 1.06, 0.30, +1.4, 1.45, ["loans.", "trick?"], None),
    ("a1", "First, Visa doesn't even make your card. Your bank does.", 1.06, 0.20, +1.0, 1.45, ["doesn't", "bank"], None),
    ("a2", "Your bank lends the money, and your bank takes the risk if you don't pay it back.", 1.06, 0.20, +0.8, 1.45, ["lends", "risk"], None),
    ("a3", "Visa just owns the road in the middle.", 1.04, 0.40, 0.0, 1.4, ["road", "middle.:dn"], "low"),
    ("b1", "Think of it like a giant toll road.", 1.06, 0.20, +1.0, 1.45, ["giant", "toll"], None),
    ("b2", "On one side, almost fourteen thousand five hundred banks. On the other, over one hundred seventy five million stores.", 1.08, 0.20, +0.8, 1.45, ["banks.", "million"], None),
    ("b3", "Every time your money drives across… Visa collects a tiny toll.", 1.06, 0.40, +0.6, 1.45, ["across…", "tiny"], "low"),
    ("c1", "Now multiply. Last fiscal year, Visa handled two hundred fifty seven billion transactions!", 1.08, 0.20, +1.0, 1.45, ["multiply.", "billion"], None),
    ("c2", "That's over eight thousand swipes and taps, every single second.", 1.06, 0.20, +1.0, 1.5, ["eight", "second."], None),
    ("c3", "Tiny tolls, times billions… equals forty billion dollars in revenue.", 1.06, 0.40, +0.6, 1.45, ["billions…", "forty"], None),
    ("d1", "And here's the crazy part. About twenty billion of that was pure profit.", 1.06, 0.20, +1.0, 1.5, ["crazy", "profit."], None),
    ("d2", "Half of every dollar! Because running a road is cheap… when you never lend a cent.", 1.06, 0.40, +0.8, 1.45, ["Half", "cent."], "low"),
    ("e1", "So next time you tap your card, remember… you're not borrowing from Visa. You're paying its toll!", 1.04, 0.35, +0.4, 1.45, ["remember…", "toll!"], None),
    ("e2", "Send this to the friend who pays for everything with a card!", 1.06, 0.0, +1.0, 1.45, ["friend", "everything"], None),
]
