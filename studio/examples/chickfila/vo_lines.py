# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# "Chick-fil-A is closed every Sunday and still wins" — energetic young narrator; "w:dn" = drop low + stretched
LINES = [
    ("i1", "Why is Chick-fil-A closed every single Sunday… and still beating almost everyone?", 1.06, 0.25, +1.0, 1.4, ["closed", "Sunday…", "beating"], "q"),
    ("i2", "One day a week, the doors stay locked. And they make more anyway!", 1.06, 0.30, +1.4, 1.45, ["locked.", "more"], None),
    ("a1", "First, the size. Last year, Chick-fil-A sold almost twenty-four billion dollars of food in America.", 1.08, 0.20, +1.0, 1.45, ["size.", "twenty-four"], None),
    ("a2", "That's the number three chain in the country. Only McDonald's and Starbucks sell more.", 1.06, 0.40, +0.4, 1.45, ["three", "Only"], "low"),
    ("b1", "But here's the crazy part. McDonald's has almost fourteen thousand restaurants here.", 1.06, 0.20, +1.0, 1.45, ["crazy", "fourteen"], None),
    ("b2", "Chick-fil-A? About three thousand three hundred.", 1.06, 0.25, +0.6, 1.45, ["About", "three"], None),
    ("b3", "So each one has to work way harder. And it does!", 1.06, 0.40, +0.8, 1.45, ["harder.", "does!"], None),
    ("c1", "An average McDonald's sells about four million dollars a year.", 1.06, 0.20, +0.6, 1.45, ["average", "four"], None),
    ("c2", "An average Chick-fil-A? About seven and a half million. In six days a week!", 1.06, 0.40, +1.2, 1.5, ["seven", "six"], None),
    ("d1", "Now the hidden deal. Want to run one? It costs just ten thousand dollars.", 1.06, 0.20, +1.0, 1.45, ["hidden", "ten"], None),
    ("d2", "But you don't own it. Chick-fil-A keeps the restaurant and the equipment.", 1.06, 0.20, +0.4, 1.45, ["don't", "keeps"], None),
    ("d3", "And reports say it takes fifteen percent of sales… plus half of the profit.", 1.06, 0.40, 0.0, 1.4, ["fifteen", "half"], "low"),
    ("f1", "So why not open on Sundays? The founder closed his first diner on Sundays back in nineteen forty-six, to give workers a day of rest.", 1.08, 0.25, +0.6, 1.45, ["Sundays?", "forty-six", "rest."], None),
    ("f2", "And they never changed it.", 1.04, 0.40, -0.2, 1.4, ["never", "changed"], "low"),
    ("e1", "Closed one day a week… and their busiest restaurant still makes over twenty million dollars a year!", 1.04, 0.35, +0.6, 1.45, ["Closed", "busiest", "twenty"], None),
    ("e2", "Send this to the friend who always craves Chick-fil-A on a Sunday!", 1.06, 0.0, +1.0, 1.45, ["always", "Sunday!"], None),
]
