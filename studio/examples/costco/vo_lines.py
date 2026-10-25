# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# energetic young narrator: faster, tighter pauses, lifted register; "w:dn" = drop low + stretched
LINES = [
    ("i1", "Do you know Costco sells a hot dog and a soda for just a dollar fifty?", 1.06, 0.22, +1.0, 1.4, ["know", "hot", "dollar"], "q"),
    ("i2", "And that price hasn't changed in forty years!", 1.06, 0.30, +1.6, 1.45, ["hasn't", "forty"], None),
    ("i3", "So how does Costco make billions?", 1.06, 0.18, +0.8, 1.4, ["billions?"], "q"),
    ("i4", "Here are four secrets… and the last one is pure genius.", 1.06, 0.40, +0.6, 1.45, ["four", "genius."], None),
    ("a1", "Secret one. The hot dog loses money… on purpose.", 1.06, 0.25, +1.0, 1.45, ["one.", "loses", "purpose.:dn"], "low"),
    ("a2", "When the CEO wanted to raise the price, the founder told him… if you raise the price of the hot dog, I will kill you!", 1.08, 0.30, +0.6, 1.45, ["raise", "kill"], None),
    ("a3", "Because that cheap hot dog makes you trust every other price in the store.", 1.06, 0.40, 0.0, 1.4, ["trust", "every"], "low"),
    ("b1", "Secret two. The four ninety-nine chicken.", 1.06, 0.20, +1.0, 1.45, ["two.", "chicken."], None),
    ("b2", "Costco sells over a hundred and fifty million of them a year.", 1.06, 0.20, +0.6, 1.45, ["hundred", "million"], None),
    ("b3", "And it's way at the back of the store… so you walk past everything else to get it.", 1.06, 0.40, 0.0, 1.4, ["back", "everything"], "low"),
    ("c1", "Secret three. Costco caps its markups.", 1.06, 0.20, +1.0, 1.45, ["three.", "caps"], None),
    ("c2", "Around fourteen percent on brands, fifteen on its own stuff. So you always feel like you're getting a deal.", 1.08, 0.40, 0.0, 1.4, ["fourteen", "fifteen", "deal."], "low"),
    ("d1", "And secret four, the genius one.", 1.04, 0.20, +0.6, 1.45, ["four,", "genius"], None),
    ("d2", "Costco's real product isn't in the store… it's this card.", 1.04, 0.30, -0.6, 1.4, ["isn't", "card."], "low"),
    ("d3", "Last year, membership fees brought in almost six billion dollars. That's about half of Costco's operating profit!", 1.06, 0.25, +0.6, 1.45, ["six", "half"], None),
    ("d4", "And about nine out of ten members renew every year.", 1.06, 0.40, 0.0, 1.4, ["nine", "ten"], "low"),
    ("e1", "So that dollar fifty hot dog isn't really food. It's an ad… for the card.", 1.04, 0.35, 0.0, 1.4, ["isn't", "ad…", "card."], "low"),
    ("e2", "Send this to the friend who basically lives at Costco!", 1.06, 0.0, +1.0, 1.45, ["lives"], None),
]
