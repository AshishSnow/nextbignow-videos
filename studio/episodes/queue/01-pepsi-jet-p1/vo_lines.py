# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# YOUR MOVE · EP 1 · PART 1 — "Could you buy a real fighter jet with Pepsi points?" (type A, POV; STORY.md beat sheet)
# Facts (see ../SOURCES-pepsi-jet.md; re-verify before building): Pepsi Stuff catalog — points from Pepsi packs swapped for
# merchandise; ad's last frame "HARRIER FIGHTER 7,000,000 PEPSI POINTS"; catalog rule: at least 15 original points, the rest
# bought at 10 cents each; John Leonard, 21, business student, Seattle; first tried to drink enough Pepsi, couldn't; five
# investors lent him $700,000; order form + 15 points + cheque for $700,008.50 (incl. $10 shipping & handling), March 1996;
# Pepsi wrote back that the jet was "fanciful", included to make the ad humorous and entertaining, apologised, sent free coupons.
# Jet value: say "over twenty million" (sources differ: $23M Seattle Times / judge; $33M-$37M elsewhere).
SERIES = "YOUR MOVE"; PART = 1; EP = 1
LINES = [
    ("i1", "Could you buy a real fighter jet… with Pepsi points?", 1.02, 0.40, +1.0, 1.45, ["fighter", "points?"], "q"),
    ("i2", "It's nineteen ninety six. You're twenty one, a business student in Seattle.", 1.02, 0.30, +0.8, 1.45, ["ninety", "twenty"], "low"),
    ("i3", "And one TV ad just showed a jet worth over twenty million dollars… as a prize.", 1.02, 0.40, +0.8, 1.45, ["jet", "twenty", "prize.:dn"], "low"),
    ("a1", "Pepsi is giving away prizes for points from its packs: T-shirts, jackets, sunglasses.", 1.04, 0.30, +0.8, 1.45, ["prizes", "sunglasses.:dn"], "low"),
    ("a2", "Its last scene? A teenager lands a fighter jet at school.", 1.02, 0.30, +1.0, 1.5, ["last", "jet"], "low"),
    ("a3", "The price, right there on screen: seven million Pepsi points.", 1.0, 0.45, +0.6, 1.5, ["screen:", "million"], "low"),
    ("a4", "You want that jet. But three problems stand in your way.", 1.02, 0.40, +0.8, 1.45, ["want", "three"], "low"),
    ("b1", "Problem one. Seven million points means drinking an ocean of Pepsi.", 1.02, 0.30, +0.8, 1.45, ["one.", "ocean"], "low"),
    ("b2", "So you read the small print.", 1.02, 0.35, +0.8, 1.45, ["small"], "low"),
    ("b3", "You only need fifteen real points. The rest, you can buy. Ten cents each.", 1.02, 0.35, +0.8, 1.45, ["fifteen", "buy.", "Ten"], "low"),
    ("b4", "Seven million points? That's seven hundred thousand dollars.", 1.0, 0.30, +0.8, 1.5, ["points?", "hundred"], "low"),
    ("b5", "For a jet worth more than thirty times that.", 1.0, 0.45, +0.6, 1.5, ["thirty"], "low"),
    ("b6", "Oops, Pepsi.", 0.98, 0.50, +0.4, 1.5, ["Oops,"], "low"),
    ("c1", "Problem two. You don't have seven hundred thousand dollars.", 1.02, 0.30, +0.8, 1.45, ["two.", "don't"], "low"),
    ("c2", "So you pitch five investors. And they lend you all of it.", 1.02, 0.40, +0.8, 1.45, ["five", "all"], "low"),
    ("d1", "Problem three. You actually have to ask.", 1.02, 0.30, +0.8, 1.45, ["three.", "ask.:dn"], "low"),
    ("d2", "You fill in the order form. Fifteen points. Plus a check for seven hundred thousand and eight dollars, fifty cents.", 1.04, 0.30, +0.8, 1.45, ["Fifteen", "eight"], "low"),
    ("d3", "Ten of those dollars are for shipping.", 1.04, 0.35, +0.8, 1.45, ["shipping."], "low"),
    ("d4", "You mail it. And you wait.", 1.0, 0.50, +0.6, 1.5, ["mail", "wait.:dn"], "low"),
    ("t1", "Pepsi replies: the jet was just for fun.", 1.02, 0.35, +1.0, 1.45, ["replies:", "fun.:dn"], "low"),
    ("t2", "Instead of a jet… free Pepsi coupons.", 1.0, 0.45, +0.6, 1.5, ["coupons."], "low"),
    ("e1", "Lesson one: read the small print.", 1.02, 0.35, +0.8, 1.45, ["read", "small"], "low"),
    ("e2", "Your move: sue Pepsi, or drop it? Comment JET or DROP.", 1.02, 0.35, +1.0, 1.45, ["sue", "drop", "JET"], None),
    ("e3", "Part two tomorrow. Send this to the friend who reads every rule.", 1.06, 0.0, +1.0, 1.45, ["two", "every"], None),
]
