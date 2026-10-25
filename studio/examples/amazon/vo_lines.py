# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# "Amazon's real money machine is AWS" — energetic young narrator; "w:dn" = drop low + stretched
LINES = [
    ("i1", "Do you think Amazon makes its money… by selling you stuff?", 1.06, 0.25, +1.0, 1.4, ["think", "selling"], "q"),
    ("i2", "Nope! Most of its profit comes from something you've never even seen.", 1.06, 0.30, +1.6, 1.45, ["Nope!", "never"], None),
    ("i3", "Let's follow the money.", 1.04, 0.45, -0.4, 1.4, ["follow", "money.:dn"], "low"),
    ("a1", "First, the shopping side. From April to June, it brought in over one hundred fifty billion dollars.", 1.08, 0.20, +1.0, 1.45, ["shopping", "fifty"], None),
    ("a2", "But the profit? Only about eleven billion.", 1.06, 0.20, +0.6, 1.45, ["profit?", "eleven"], None),
    ("a3", "That's less than seven cents on every dollar.", 1.04, 0.40, 0.0, 1.4, ["seven", "dollar.:dn"], "low"),
    ("b1", "Now the secret. Amazon Web Services.", 1.06, 0.20, +1.0, 1.45, ["secret.", "Web"], None),
    ("b2", "Amazon rents out giant warehouses full of computers… to other companies, over the internet.", 1.06, 0.25, +0.6, 1.45, ["rents", "computers…", "other"], None),
    ("b3", "In those same three months, that made forty-two billion in sales… and over sixteen billion in profit!", 1.08, 0.20, +1.2, 1.5, ["forty-two", "sixteen"], None),
    ("b4", "That's almost forty cents on every dollar.", 1.04, 0.40, 0.0, 1.4, ["forty", "dollar.:dn"], "low"),
    ("c1", "Here's the twist.", 1.04, 0.20, +1.0, 1.45, ["twist."], None),
    ("c2", "The cloud is only about one fifth of Amazon's sales…", 1.06, 0.15, +0.4, 1.4, ["only", "fifth"], None),
    ("c3", "but it brings in six out of every ten dollars of profit!", 1.06, 0.40, +1.2, 1.5, ["six", "ten"], None),
    ("d1", "And there's a second secret. Ads! Those sponsored products when you search?", 1.06, 0.20, +1.0, 1.45, ["second", "Ads!", "sponsored"], "q"),
    ("d2", "Almost twenty billion dollars in ad sales, in three months.", 1.06, 0.40, +0.6, 1.45, ["twenty", "three"], None),
    ("e1", "So the store brings you in… but the cloud pays the bills.", 1.04, 0.35, 0.0, 1.4, ["store", "cloud", "bills.:dn"], "low"),
    ("e2", "Send this to the friend who thinks Amazon is just a shop!", 1.06, 0.0, +1.0, 1.45, ["thinks", "shop!"], None),
]
