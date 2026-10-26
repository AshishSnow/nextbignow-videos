# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# "Printer ink costs more than champagne" — energetic young narrator
LINES = [
    ("i1", "Did you know printer ink can cost seven times more than fancy champagne?", 1.06, 0.25, +1.0, 1.4, ["seven", "champagne?"], "q"),
    ("i2", "That's not a mistake. It's the whole plan!", 1.06, 0.30, +1.4, 1.45, ["mistake.", "plan!"], None),
    ("a1", "Step one: sell the printer cheap.", 1.06, 0.20, +1.0, 1.45, ["one:", "cheap."], None),
    ("a2", "You think, wow, what a deal! And you carry it home.", 1.06, 0.35, +0.8, 1.45, ["wow,", "deal!"], None),
    ("b1", "Step two: the ink runs out. So you buy more. And again. And again.", 1.06, 0.35, +1.0, 1.45, ["two:", "more."], None),
    ("c1", "A British consumer group checked one ink set. Almost one pound eighty, for every milliliter.", 1.06, 0.20, +0.8, 1.45, ["checked", "eighty,"], None),
    ("c2", "A bottle of Dom Perignon champagne? Just twenty-four pence a milliliter.", 1.06, 0.20, +0.6, 1.45, ["Perignon", "twenty-four"], None),
    ("c3", "So the ink was over seven times pricier!", 1.06, 0.40, +1.0, 1.5, ["seven", "pricier!"], "low"),
    ("d1", "Step three: the money. Last year, HP sold almost eleven billion dollars of printer supplies.", 1.08, 0.20, +1.0, 1.45, ["money.", "eleven"], None),
    ("d2", "That's about two thirds of everything its printer business sold.", 1.06, 0.25, +0.4, 1.45, ["two", "everything"], None),
    ("d3", "And printing made fifty percent more profit than its computers. With less than half the sales!", 1.06, 0.40, +1.0, 1.5, ["fifty", "half"], None),
    ("f1", "Even HP's boss said it on TV.", 1.04, 0.25, +0.6, 1.45, ["boss", "TV."], None),
    ("f2", "If this customer doesn't print enough, or doesn't use our supplies, it's a bad investment.", 1.02, 0.40, 0.0, 1.4, ["enough,", "bad"], "low"),
    ("e1", "So the printer was never the product. The ink is!", 1.04, 0.35, +0.6, 1.45, ["never", "ink"], None),
    ("e2", "Send this to the friend who just paid for new ink!", 1.06, 0.0, +1.0, 1.45, ["friend", "ink!"], None),
]
