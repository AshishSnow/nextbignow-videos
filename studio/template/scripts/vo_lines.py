# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# energetic young narrator (Bunty-style energy): faster, tight pauses, lifted register; "w:dn" = drop low + stretched
LINES = [
    ("i1", "Do you know Starbucks is sitting on one point seven billion dollars… of your money?", 1.06, 0.25, +1.0, 1.4, ["know", "seven", "your"], "q"),
    ("i2", "That's more than most banks in America have!", 1.06, 0.30, +1.6, 1.45, ["more", "banks"], None),
    ("i3", "Here's how a coffee shop secretly became a bank.", 1.04, 0.45, -0.4, 1.4, ["secretly:dn", "bank."], "low"),
    ("a1", "Step one. You load money into the app… before you even order.", 1.06, 0.20, +1.0, 1.45, ["one.", "before"], None),
    ("a2", "Twenty-five dollars here. Fifty dollars there. Millions of people do it.", 1.08, 0.20, +0.6, 1.45, ["Twenty-five", "Fifty", "Millions"], None),
    ("a3", "So Starbucks gets your cash today… and you get your coffee later.", 1.06, 0.40, 0.0, 1.4, ["today…", "later.:dn"], "low"),
    ("b1", "Step two. It's like a loan… with zero interest.", 1.06, 0.20, +1.0, 1.45, ["two.", "zero"], None),
    ("b2", "A bank has to pay you interest on your money. Starbucks pays you nothing!", 1.06, 0.40, +0.6, 1.45, ["bank", "nothing!"], None),
    ("c1", "Step three. Some of that money is never spent.", 1.06, 0.20, +1.0, 1.45, ["three.", "never"], None),
    ("c2", "Forgotten gift cards. A few dollars left in the app.", 1.04, 0.20, -0.4, 1.4, ["Forgotten", "few"], "low"),
    ("c3", "In one year, that added up to over two hundred million dollars!", 1.06, 0.20, +1.2, 1.5, ["two", "million"], None),
    ("c4", "And Starbucks gets to count it as revenue… no coffee needed.", 1.04, 0.40, 0.0, 1.4, ["revenue…", "no"], "low"),
    ("d1", "Today, about four in ten Starbucks orders in the US are paid with a Starbucks card.", 1.06, 0.40, +0.4, 1.45, ["four", "ten"], None),
    ("e1", "So next time you top up that app, remember… you're not just buying coffee. You're funding a bank.", 1.04, 0.35, 0.0, 1.4, ["remember…", "funding", "bank."], "low"),
    ("e2", "Send this to the friend who lives at Starbucks!", 1.06, 0.0, +1.0, 1.45, ["lives"], None),
]
