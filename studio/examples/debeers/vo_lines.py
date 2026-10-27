# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# "Diamonds aren't as rare as their price: how De Beers sold 'forever'"
# Sources: Al Jazeera (14 Sep 2025): De Beers ~90% of world supply (~1900), CSO stockpiled + controlled release = illusion of scarcity,
#   N.W. Ayer, 'A diamond is forever' (1947), US brides with a diamond ring 10% (1940) -> ~80% (1980), 1980s ads "two months' salary";
#   National Geographic: "eventually owned up to 90 percent"; De Beers / Assouline (Feb 2026): Frances Gerety wrote it in 1947;
#   NPR (2013): Ad Age named it slogan of the century (1999), ad line "How else could two months' salary last forever?";
#   Anglo American full-year 2025 results (Feb 2026): De Beers production 21.7 Mct, underlying EBITDA -$511M, $2.3B impairment;
#   JCK (10 Aug 2026, Edahn Golan index): lab-grown wholesale prices down 96% since 2018;
#   National Jeweler (12 May 2025): Lightbox launched 2018 at $800/carat, being shut down; CNBC Africa (Jul 2026): De Beers up for sale since May 2024.
LINES = [
    ("i1", "Why does a tiny rock cost two months' salary?", 1.02, 0.40, +1.0, 1.45, ["tiny", "two"], None),
    ("i2", "Because one company spent a century making it look rare.", 1.02, 0.35, +0.6, 1.45, ["century", "rare.:dn"], "low"),
    ("i3", "Here's the trick, in three moves.", 1.04, 0.45, +0.8, 1.45, ["three"], "low"),
    ("a1", "Move one. Control the supply.", 1.02, 0.30, +1.0, 1.45, ["one.", "supply."], "low"),
    ("a2", "At its peak, De Beers controlled about ninety percent of the world's diamonds.", 1.04, 0.30, +0.8, 1.45, ["peak,", "ninety"], None),
    ("a3", "It kept the stones locked away, and let them out slowly. Scarcity, on demand.", 1.02, 0.40, +0.6, 1.45, ["locked", "demand.:dn"], "low"),
    ("a4", "Even last year, De Beers dug up about twenty two million carats. Not exactly rare.", 1.04, 0.45, +0.8, 1.45, ["twenty", "rare.:dn"], "low"),
    ("b1", "Move two. Sell a feeling.", 1.02, 0.30, +1.0, 1.45, ["two.", "feeling."], "low"),
    ("b2", "In nineteen forty, only about one bride in ten got a diamond ring.", 1.04, 0.30, +0.8, 1.45, ["only", "ten"], None),
    ("b3", "So De Beers hired an ad agency. And in nineteen forty seven, a young copywriter wrote four words.", 1.04, 0.60, +0.8, 1.45, ["agency.", "four"], None),
    ("b4", "A diamond is forever.", 0.96, 0.45, +0.4, 1.5, ["forever.:dn"], "low"),
    ("b5", "Ad Age later called it the slogan of the century. By nineteen eighty, about eight in ten brides got a diamond.", 1.04, 0.45, +0.8, 1.45, ["century.", "eight"], "low"),
    ("c1", "And move three is the sneakiest. Tell people what to pay.", 1.02, 0.30, +1.0, 1.5, ["sneakiest.", "pay.:dn"], "low"),
    ("c2", "In the nineteen eighties, its ads asked: how can you make two months' salary last forever?", 1.04, 0.35, +0.8, 1.45, ["eighties,", "two"], None),
    ("c3", "A price rule, written by the seller.", 1.02, 0.50, +0.6, 1.5, ["rule,", "seller.:dn"], "low"),
    ("d1", "But now, the trick is breaking.", 1.02, 0.30, +1.0, 1.5, ["now,", "breaking."], "low"),
    ("d2", "Labs can grow real diamonds. Same carbon, same sparkle.", 1.04, 0.30, +0.8, 1.45, ["grow", "sparkle."], None),
    ("d3", "And their wholesale price has fallen about ninety six percent since twenty eighteen.", 1.04, 0.40, +0.8, 1.5, ["fallen", "ninety"], "low"),
    ("d4", "Even De Beers sold lab diamonds, at eight hundred dollars a carat. Then it shut that brand down.", 1.04, 0.35, +0.8, 1.45, ["Even", "eight", "shut"], "low"),
    ("d5", "Last year, De Beers made a core loss of about half a billion dollars. Now its owner is selling it.", 1.04, 0.45, +0.8, 1.5, ["half", "selling"], "low"),
    ("t1", "So here's the takeaway. A price tag tells you what someone wants you to pay. Not what a thing is worth.", 1.02, 0.30, +0.8, 1.45, ["takeaway.", "wants", "worth.:dn"], "low"),
    ("t2", "Before you pay for rare, ask one question. What would it sell for tomorrow?", 1.02, 0.35, +0.8, 1.45, ["rare,", "tomorrow?"], None),
    ("e1", "Because the rarest thing about a diamond… was the story.", 1.0, 0.35, +0.6, 1.5, ["rarest", "story.:dn"], "low"),
    ("e2", "Send this to the friend who's shopping for a ring!", 1.06, 0.0, +1.0, 1.45, ["friend", "ring!"], None),
]
