# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# "Why movie theaters really make money on popcorn" (AMC FY2025) — energetic young narrator
LINES = [
    ("i1", "Did you know AMC makes almost as much money from popcorn… as from every single movie ticket it sells?", 1.08, 0.25, +1.0, 1.4, ["popcorn…", "ticket"], "q"),
    ("i2", "Sounds crazy. So grab a snack, here's the math!", 1.06, 0.30, +1.4, 1.45, ["crazy.", "math!"], None),
    ("a1", "Step one: the ticket. Last year, the average AMC ticket cost about twelve dollars.", 1.06, 0.20, +1.0, 1.45, ["one:", "twelve"], None),
    ("a2", "But nearly half of that goes straight back to the movie studio!", 1.06, 0.20, +0.8, 1.45, ["half", "studio!"], None),
    ("a3", "So the theater keeps about fifty-two cents of every ticket dollar.", 1.06, 0.35, +0.6, 1.45, ["keeps", "fifty-two"], "low"),
    ("b1", "Step two: the snack bar. Each guest spends about seven dollars and sixty cents on popcorn and drinks.", 1.06, 0.20, +1.0, 1.45, ["two:", "sixty"], None),
    ("b2", "And the food itself? It costs AMC less than twenty cents per dollar.", 1.06, 0.20, +0.8, 1.45, ["itself?", "twenty"], None),
    ("b3", "So about eighty cents of every snack dollar stays with the theater!", 1.06, 0.40, +1.0, 1.5, ["eighty", "stays"], None),
    ("c1", "Step three: add it all up. Snacks are only about a third of AMC's sales.", 1.06, 0.20, +1.0, 1.45, ["three:", "third"], None),
    ("c2", "But after paying for the films and the food, snacks bring in one point three four billion dollars.", 1.08, 0.20, +0.8, 1.45, ["snacks", "billion"], None),
    ("c3", "Tickets? One point three eight billion. Almost a tie!", 1.06, 0.40, +1.0, 1.5, ["Tickets?", "tie!"], None),
    ("d1", "So the movie gets you in the door… and the popcorn pays the bills.", 1.04, 0.35, +0.6, 1.45, ["door…", "bills."], "low"),
    ("f1", "And the twist? Even with all that popcorn, AMC still lost about six hundred thirty million dollars last year!", 1.08, 0.20, +1.0, 1.45, ["twist?", "lost"], None),
    ("f2", "Rent, staff and huge debt payments eat the rest.", 1.04, 0.35, +0.4, 1.4, ["huge", "rest."], "low"),
    ("e1", "So next time you buy the large popcorn… you're the real blockbuster!", 1.04, 0.35, +0.8, 1.45, ["large", "blockbuster!"], None),
    ("e2", "Send this to the friend who always buys the giant popcorn!", 1.06, 0.0, +1.0, 1.45, ["friend", "giant"], None),
]
