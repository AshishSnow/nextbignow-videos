# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# "Monopoly was invented to warn against monopolies" (type D, origin twist)
# Sources: Smithsonian (Mary Pilon, Jan 2015): 1904 patent, Landlord's Game, 'Go to Jail' corner, two rule sets (monopolist /
#   anti-monopolist) to show the evils of accumulating wealth at others' expense, Atlantic City Quaker version, Darrow sold to Parker
#   Brothers 1935, Magie sold her patent to Parker Brothers for $500 the same year, 278,000 copies year 1 and 1,750,000+ year 2,
#   Darrow 'fantastically rich', 1940 census: occupation 'maker of games', income '0';
#   Wikipedia / Wikimedia Commons patent file: US 748,626, 5 Jan 1904; NPR (Feb 2015): fewer than 1% of US patents from women,
#   Quakers added local street names, Darrow sold it 'as his own', Anspach (professor, SF State) ~10 years in court;
#   UK IPO blog (Dec 2023): anti-monopolist rules = everyone rewarded when wealth is created, monopolist version proved more popular,
#   Parker Brothers promoted Darrow as sole inventor; Wikipedia Anti-Monopoly: Parker Brothers sued Anspach in 1974, he found Magie's
#   history preparing his defense; Wikipedia Charles Darrow: unemployed salesman, learned the game from a friend.
LINES = [
    ("i1", "Did you know Monopoly was invented to warn against monopolies?", 1.02, 0.40, +1.0, 1.45, ["warn", "monopolies?"], "q"),
    ("i2", "And the woman behind it sold her patent for just five hundred dollars.", 1.02, 0.35, +0.6, 1.45, ["woman", "five"], "low"),
    ("i3", "Here's how her game got flipped.", 1.04, 0.45, +0.8, 1.45, ["flipped.:dn"], "low"),
    ("a1", "Nineteen oh four. A woman named Lizzie gets a patent for a board game.", 1.02, 0.30, +1.0, 1.45, ["four.", "patent"], None),
    ("a3", "Her game has a square board, rent to pay, and a corner that says: go to jail.", 1.04, 0.30, +0.8, 1.45, ["square", "jail.:dn"], "low"),
    ("a4", "She calls it the Landlord's Game. And it has a message.", 1.02, 0.30, +0.8, 1.45, ["Landlord's", "message.:dn"], "low"),
    ("a5", "She wants to show what happens when a few people grab all the wealth, at everyone else's expense.", 1.04, 0.40, +0.8, 1.45, ["few", "everyone"], "low"),
    ("b1", "So she writes two sets of rules.", 1.02, 0.30, +1.0, 1.45, ["two"], "low"),
    ("b2", "In one, you win by crushing everyone else.", 1.04, 0.25, +0.8, 1.45, ["crushing"], "low"),
    ("b3", "In the other, when wealth is created, everyone is rewarded.", 1.04, 0.35, +0.8, 1.45, ["other,", "everyone"], "low"),
    ("b4", "Guess which one people loved?", 1.04, 0.45, +1.0, 1.45, ["Guess", "loved?"], None),
    ("b5", "The crushing one.", 1.0, 0.45, +0.4, 1.5, ["crushing:dn"], "low"),
    ("c1", "And then, the game escaped.", 1.02, 0.35, +1.0, 1.5, ["escaped.:dn"], "low"),
    ("c2", "For decades, people drew their own boards by hand. In Atlantic City, Quakers added their own street names.", 1.04, 0.30, +0.8, 1.45, ["hand.", "street"], None),
    ("c3", "In the nineteen thirties, an out of work salesman named Charles Darrow learned the game from a friend.", 1.04, 0.30, +0.8, 1.45, ["salesman", "friend.:dn"], "low"),
    ("c4", "He made his own board. And in nineteen thirty five, he sold it to Parker Brothers.", 1.04, 0.30, +0.8, 1.45, ["own", "sold"], None),
    ("c5", "Who sold it to the world as Darrow's invention.", 1.02, 0.40, +0.6, 1.5, ["Darrow's", "invention.:dn"], "low"),
    ("c6", "Two hundred seventy eight thousand copies in year one. Over one point seven million in year two.", 1.04, 0.30, +0.8, 1.45, ["seventy", "million"], None),
    ("c7", "Darrow got rich.", 1.0, 0.45, +0.4, 1.5, ["rich.:dn"], "low"),
    ("d1", "And Lizzie? That same year, Parker Brothers bought her patent… for five hundred dollars.", 1.02, 0.45, +0.8, 1.5, ["Lizzie?", "five"], "low"),
    ("d2", "In the nineteen forty census, she listed her job as maker of games.", 1.02, 0.35, +0.8, 1.45, ["census,", "games."], None),
    ("d3", "Her income that year? Zero.", 0.98, 0.55, +0.4, 1.5, ["income?", "Zero.:dn"], "low"),
    ("f1", "Her story only came back in the nineteen seventies.", 1.02, 0.30, +1.0, 1.45, ["only", "seventies.:dn"], "low"),
    ("f2", "A professor made a game called Anti-Monopoly, and Parker Brothers took him to court.", 1.04, 0.30, +0.8, 1.45, ["Anti", "court.:dn"], "low"),
    ("f3", "Digging for his defense, he found her old patent. The fight lasted about ten years.", 1.04, 0.45, +0.8, 1.45, ["found", "ten"], "low"),
    ("t1", "So a game built to warn against monopolies… became the game of winning one.", 1.0, 0.45, +0.8, 1.5, ["warn", "winning"], "low"),
    ("t2", "The takeaway? When you hear a lone genius story, check who came first. Patents are public, and free to search.", 1.02, 0.35, +0.8, 1.45, ["takeaway?", "first.", "free"], "low"),
    ("e1", "Because her game had one message: don't play like this.", 1.0, 0.35, +0.6, 1.5, ["one", "this.:dn"], "low"),
    ("e2", "Send this to the friend who always wins at Monopoly!", 1.06, 0.0, +1.0, 1.45, ["friend", "wins"], None),
]
