# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# REAL CASE STUDY · DOODLE look (rewritten 15 Nov 2026 by the R&D writers' room from the 14 Nov whiteboard script; facts unchanged, SOURCES.md)
# "Domino's put customers on TV calling its pizza cardboard — and sales jumped". Format of examples/airbnb-cereal-doodle (owner 14 Nov).
# One arc: sales falling (2008) -> focus groups: 'like cardboard', 'tastes like ketchup' -> ~2 years remaking the pizza -> the ads air the
# complaints (Dec 2009) -> Jan–Mar 2010 +14.3 % vs +1.0 % -> Doyle credits the pizza and the honesty -> 22,000+ stores -> lesson.
# Characters: the PIZZA (usa_young: sad and pale, then garlic-crust proud) and a grumpy KETCHUP BOTTLE (usa_boss) — generic doodles.
# No Domino's logo, domino tile, blue/red trade dress or uniforms; people = plain stick doodles with name tapes (no likeness of Patrick Doyle).
SERIES = "HOW THEY GOT SO BIG"; PART = 0; EP = 1
CBVOICES = {"a5": "usa_boss", "a6": "usa_young", "d5": "usa_young"}
LINES = [
    ("i1", "Would you put your own customers on TV to say your crust is like cardboard?", 0.98, 0.25, +0.8, 1.5, ['own', 'cardboard?'], None),
    ("i2", "Domino's did. On purpose. And its sales jumped.", 0.98, 0.3, +0.6, 1.45, ['purpose.', 'jumped.'], None),
    ("i3", "Your sales are sliding, your pizza is the joke, and you need people back. Three moves turned it around.", 0.98, 0.3, +0.8, 1.5, ['joke,', 'three'], None),
    ("a1", "Michigan, twenty oh eight.", 0.97, 0.2, +1.0, 1.5, ['Michigan,'], None),
    ("a2", "Domino's American stores are selling about five percent less than the year before.", 0.97, 0.25, +0.6, 1.45, ['less', 'five'], None),
    ("a3", "First move: ask real customers what they think. And they don't hold back.", 0.97, 0.25, +0.6, 1.45, ['real', "don't"], None),
    ("a4", "One says the crust is like cardboard. Another says the sauce tastes like ketchup.", 0.97, 0.25, +0.8, 1.45, ['cardboard.', 'ketchup.'], None),
    ("a5", "Excuse me? Leave me out of this.", 0.97, 0.2, +0.2, 1.35, ['Excuse', 'out'], None),
    ("a6", "Yeah, that's me. The cardboard. Ouch.", 1.0, 0.3, +1.2, 1.5, ['me.', 'Ouch.'], 'low'),
    ("b1", "Most companies would bury those comments. Domino's didn't.", 0.97, 0.2, +1.0, 1.5, ['bury', "didn't."], None),
    ("b2", "Move two. Fix the pizza itself.", 0.97, 0.2, +1.0, 1.5, ['two.', 'itself.'], None),
    ("b3", "Domino's says the testing took about two years.", 0.97, 0.2, +0.6, 1.45, ['two'], None),
    ("b4", "Dozens of cheeses. Fifteen sauces. Nearly fifty seasonings just for the crust.", 0.97, 0.25, +0.6, 1.45, ['Fifteen', 'fifty'], None),
    ("b5", "What wins? Garlic on the crust, a sweeter sauce, and a hint of provolone.", 0.97, 0.3, +0.8, 1.45, ['Garlic', 'provolone'], None),
    ("c1", "And the last move sounds like a terrible idea. Tell everybody the old pizza was bad.", 0.97, 0.2, +1.0, 1.5, ['terrible', 'bad.'], None),
    ("c2", "In December twenty oh nine, the new ads play those complaints right on TV.", 0.97, 0.25, +0.6, 1.45, ['complaints', 'TV.'], None),
    ("c3", "Domino's own chefs watch the feedback on camera. A critic at Slate called them mortified.", 0.97, 0.25, +0.6, 1.45, ['camera.', 'mortified.'], None),
    ("c4", "Then the boss of its American stores speaks. Patrick Doyle.", 0.97, 0.15, +0.6, 1.45, ['boss', 'Doyle.'], None),
    ("c5", "His line: there comes a time when you know you've got to make a change.", 0.97, 0.3, +0.6, 1.45, ['time', 'change.'], None),
    ("c6", "Honestly? I'd have been scared to sign off on that ad.", 0.97, 0.3, +0.8, 1.45, ['Honestly?', 'scared'], None),
    ("d1", "So did it work? In May twenty ten, the first numbers since the new pizza come in.", 0.97, 0.25, +0.8, 1.45, ['work?', 'numbers'], None),
    ("d2", "From January to March, sales at its American stores are up over fourteen percent.", 0.97, 0.25, +0.8, 1.5, ['up', 'fourteen'], None),
    ("d3", "A year earlier, that number was up just one percent.", 0.97, 0.3, +0.6, 1.45, ['just', 'one'], None),
    ("d4", "By then, Doyle runs the whole company. He credits a better pizza, and the honesty.", 0.97, 0.3, +0.6, 1.45, ['better', 'honesty.'], None),
    ("d5", "Garlic crust. Who's cardboard now?", 1.0, 0.25, +1.2, 1.5, ['Garlic', 'now?'], None),
    ("d6", "And today? Domino's counts more than twenty-two thousand stores around the world.", 0.97, 0.3, +0.8, 1.45, ['twenty-two', 'world.'], None),
    ("t1", "They didn't hide the worst thing people said. They used it as the opening line of their comeback.", 0.97, 0.3, +0.8, 1.45, ['worst', 'opening'], None),
    ("t2", "Try it next time. Read your worst reviews. If they're right, fix it, then say so out loud.", 0.97, 0.3, +0.8, 1.45, ['worst', 'loud.'], 'low'),
    ("z1", "Send this to the friend who orders pizza every Friday.", 1.0, 0.2, +1.0, 1.45, ['friend', 'Friday.'], None),
    ("z2", "Your product gets slammed online. Air it, or hide it? Tell me in the comments.", 1.0, 0.0, +1.0, 1.45, ['Air', 'hide'], None),
]
