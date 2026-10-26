# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# "Planet Fitness: $15 a month, $220M profit" — energetic young narrator
LINES = [
    ("i1", "How does Planet Fitness charge just fifteen dollars a month... and still make over two hundred million dollars?", 1.08, 0.25, +1.0, 1.4, ["fifteen", "million"], "q"),
    ("i2", "The answer is kind of genius. And it involves you!", 1.06, 0.30, +1.4, 1.45, ["genius.", "you!"], None),
    ("a1", "Secret one: make it so cheap, cancelling feels pointless.", 1.06, 0.20, +1.0, 1.45, ["one:", "pointless."], None),
    ("a2", "Fifteen bucks a month. Plus a forty-nine dollar yearly fee.", 1.06, 0.35, +0.8, 1.45, ["bucks", "yearly"], None),
    ("b1", "Secret two: pack in the members. Almost twenty-one million of them!", 1.06, 0.25, +1.0, 1.45, ["pack", "twenty-one"], None),
    ("b2", "But under three thousand clubs. That's over seven thousand members per gym!", 1.06, 0.25, +0.8, 1.45, ["three", "seven"], None),
    ("b3", "If they all showed up on the same day? Total chaos!", 1.06, 0.40, +1.0, 1.5, ["same", "chaos!"], None),
    ("c1", "Secret three: they know lots of people won't come. It's right there in their annual report.", 1.06, 0.25, +1.0, 1.45, ["three:", "report."], None),
    ("c2", "A portion of our member base does not regularly use our clubs.", 1.02, 0.40, 0.0, 1.4, ["portion", "regularly"], "low"),
    ("d1", "And it's not just them. Berkeley economists studied people paying over seventy dollars a month for the gym.", 1.08, 0.20, +1.0, 1.45, ["Berkeley", "seventy"], None),
    ("d2", "They went under five times a month. So every visit cost them over seventeen dollars!", 1.06, 0.20, +0.8, 1.45, ["five", "seventeen"], None),
    ("d3", "When a ten dollar pass was right there.", 1.06, 0.25, +0.6, 1.45, ["ten", "there."], None),
    ("d4", "Eighty percent would have saved money just paying per visit!", 1.06, 0.40, +1.0, 1.5, ["Eighty", "saved"], "low"),
    ("f1", "Last year, Planet Fitness made one point three billion in revenue, and two hundred twenty million in profit.", 1.08, 0.35, +1.0, 1.45, ["billion", "twenty"], None),
    ("e1", "So the cheap gym isn't really selling workouts. It's selling the plan to work out!", 1.04, 0.35, +0.6, 1.45, ["workouts.", "plan"], None),
    ("e2", "Send this to the friend who pays for a gym they never go to!", 1.06, 0.0, +1.0, 1.45, ["friend", "never"], None),
]
