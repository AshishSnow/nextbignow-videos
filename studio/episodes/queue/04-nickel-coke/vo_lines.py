# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# YOUR MOVE · EP 2 — "Why would a soda boss ask the President for a brand-new coin?" (type B, single part; STORY.md §4 beat sheet).
# You = the boss of Coca-Cola, 1950–53 (Robert Woodruff's seat; the hero plays the role, no likeness, no name needed in VO).
# Facts (see SOURCES.md; re-verify before building): a 6.5-oz Coke cost 5 cents from 1886 (fountain glass; bottling from 1899) until
# 1959 (Levy & Young, JMCB 2004: "nominal price rigidity that lasted more than 70 years"); 1908 ad "5¢. Everywhere."; ~160,000
# billboards by the 1930s; ~1,100 bottlers, only 125 had raised retail prices by 1950; 1899 bottling contract "permanent and
# perpetual" (1920 court record), syrup price fixed (about $1/gal, later 92c), renegotiated 1921 ($1.17 + sugar escalator) — the RETAIL
# price was never a contract term; Fortune Jan 1951: "Coke has been charged with coercing its bottlers to stay at the 80-cent case
# price" (resale-price control cuts both ways); ~400,000 nickel-only Coke vending machines by 1950 (of ~460,000 US machines); next coin
# = a dime = a 100 % jump; Dec 1950 New York "went to 6¢" (Time); 1953: Woodruff asked his friend President Eisenhower for a 7.5-cent
# coin; Eisenhower forwarded it to the Treasury, "who did not like the idea" (Coin World, reporting Levy & Young); 1955 "6¢, 7¢ or even
# 10¢ depending on the area" (Business Week); 1959 the last nickel Coke; the "official blank": every ninth vending bottle empty so the
# average price rises to ~5.6¢ — company memos, never implemented (NPR Planet Money ep. 416). No "Oops." beat: no blunder, a trap.
# Fresh-eyes review 31 Oct applied: chronology (New York 6¢ in Dec 1950 now BEFORE the 1953 ask), "ask" not "beg", price-fixing cuts
# both ways, a dime = ten cents said aloud, the decision posed before the outcome, "Every Coke" (1886 = fountain), the memo idea
# "never leaves the memo", takeaway = check the size, machines "sell your Coke" (bottlers/operators owned them).
# Never say the 1899 contract "froze the price until 1959" (myth); never quote a Woodruff letter (none found); say "in 1953".
# Company name: "Coca-Cola" is fine in VO (common word); no contour bottle, no script logo, no red disc — a plain green-glass bottle + "5¢" tag.
SERIES = "YOUR MOVE"; PART = 0; EP = 2
LINES = [
    ("i1", "Why would a soda boss ask the President… for a brand-new coin?", 1.02, 0.40, +1.0, 1.45, ["President…", "coin?"], "q"),
    ("i2", "It's nineteen fifty. You run Coca-Cola.", 1.02, 0.30, +0.8, 1.45, ["fifty.", "run"], "low"),
    ("i3", "Every Coke costs a nickel. It has since eighteen eighty-six.", 1.02, 0.35, +0.8, 1.45, ["nickel.", "eighty"], "low"),
    ("i4", "Sixty-four years. Two world wars. One price.", 1.0, 0.45, +0.8, 1.5, ["Sixty", "One"], "low"),
    ("a1", "Your costs keep rising, but three traps keep that nickel stuck. The last is the coin in your pocket.", 1.02, 0.45, +0.8, 1.45, ["three", "pocket.:dn"], "low"),
    ("b1", "Trap one. The ads.", 1.0, 0.30, +0.8, 1.45, ["one.", "ads."], "low"),
    ("b2", "For decades your ads said it in two words. Five cents. Everywhere.", 1.02, 0.30, +0.8, 1.45, ["two", "Everywhere."], "low"),
    ("b3", "Raise it, and a hundred and sixty thousand billboards are suddenly wrong.", 1.02, 0.45, +0.8, 1.45, ["hundred", "wrong."], "low"),
    ("c1", "Trap two. The bottlers.", 1.0, 0.30, +0.8, 1.45, ["two.", "bottlers."], "low"),
    ("c2", "You don't set the shop price. Eleven hundred independent bottlers do.", 1.02, 0.30, +0.8, 1.45, ["don't", "Eleven"], "low"),
    ("c3", "Their contract dates from eighteen ninety-nine, and it never expires.", 1.02, 0.30, +0.8, 1.45, ["ninety", "never"], "low"),
    ("c4", "Tell them what to charge, up or down, and regulators may call it price-fixing.", 1.02, 0.35, +0.8, 1.45, ["Tell", "fixing."], "low"),
    ("c5", "And already a hundred and twenty-five of them have broken ranks.", 1.02, 0.45, +0.8, 1.45, ["twenty", "ranks.:dn"], "low"),
    ("d1", "Trap three. Your pocket.", 1.0, 0.30, +0.8, 1.45, ["three.", "pocket."], "low"),
    ("d2", "Four hundred thousand machines sell your Coke, and take only a nickel.", 1.02, 0.30, +0.8, 1.45, ["Four", "only"], "low"),
    ("d3", "But the next coin up is a dime: ten cents. So your smallest rise… is double.", 1.0, 0.45, +0.8, 1.5, ["ten", "double.:dn"], "low"),
    ("d4", "Now New York breaks ranks: six cents a bottle.", 1.02, 0.40, +0.8, 1.45, ["York", "six"], "low"),
    ("d5", "Double the most famous nickel in America? Or gamble on a coin that doesn't exist?", 1.02, 0.45, +0.8, 1.45, ["Double", "exist?"], "low"),
    ("d6", "So in nineteen fifty-three you go to your friend. He runs the country.", 1.02, 0.35, +0.8, 1.45, ["friend.", "country."], "low"),
    ("d7", "Your ask: mint a brand-new coin. Seven and a half cents.", 1.0, 0.50, +0.8, 1.5, ["mint", "half"], "low"),
    ("o1", "He passes it to the Treasury. And the Treasury? Does not like the idea.", 1.02, 0.40, +0.6, 1.45, ["Treasury?", "not"], "low"),
    ("o2", "Without a coin, the nickel breaks town by town. Six cents, seven, a dime.", 1.02, 0.30, +0.8, 1.45, ["town", "dime."], "low"),
    ("o3", "By nineteen fifty-nine, the nickel Coke is gone.", 1.02, 0.45, +0.6, 1.45, ["nine,", "gone.:dn"], "low"),
    ("t1", "One idea never left the memo: every ninth bottle, empty.", 1.02, 0.35, +1.0, 1.45, ["memo:", "empty."], "low"),
    ("t2", "Some people pay twice. Average, five point six cents.", 1.0, 0.45, +0.8, 1.5, ["twice.", "six"], "low"),
    ("k1", "A price that never moves? Check the size.", 1.02, 0.35, +0.8, 1.45, ["never", "size."], "low"),
    ("e1", "Dime or coin? Comment DIME or COIN.", 1.02, 0.35, +1.0, 1.45, ["coin?", "DIME"], None),
    ("e2", "Send this to the friend who moans about prices.", 1.06, 0.0, +1.0, 1.45, ["moans"], None),
]
