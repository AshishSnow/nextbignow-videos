# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# HOW IT WORKS · "They sold NOTHING for $5" — Cards Against Humanity's Black Friday stunts. 13 Nov 2026, DOODLE look (owner: "write better
# script, better topic, interesting ... learn from natural writing people"). Black Friday 2026 = 27 Nov, so it's timely.
# Writing rules used (studied Kallaway's scripting talks): shock-score facts, question hook where line 1 alone tells the story,
# but/therefore links instead of "and then", varied sentence length, talk-to-one-friend tone, a payoff emotion (amused -> "oh, that's smart").
# OUR OWN script; characters (game box, poop box, empty box, dollar bill) are invented generic doodles. No logos or trade dress.
# Voices: narrator usa_narr; a3/c3 game box & empty box usa_young; b3 dollar bill usa_boss.
# Fresh-eyes review 13 Nov applied (three Black Fridays, online store, 'about', headlines not 'free').
# Facts:
#  Fortune 27 Nov 2016: 2013 "anti-sale" $5 above regular price; 2014 game pulled from the store, replaced with "boxes of bull feces",
#   about 30,000 sold; 2015 "Give Cards Against Humanity $5", nothing in return, more than 11,000 paid; 2016 hole raised $100,000.
#  The Hustle: 2013 sales went up; 2014 $6 box of "literal poop", about 30,000 bought, sold out.
#  UPI 30 Nov 2015: 11,248 paid $5, total $71,145, split among 17 employees (~$4,185 each); purchases incl. an $800 Lord of the Rings
#   longbow and Lasik eye surgery. Covered by UPI, Business Insider, Yahoo, TechCrunch, Fortune etc. ("news sites everywhere").
SERIES = "HOW IT WORKS"; PART = 0; EP = 1
CBVOICES = {"a3": "usa_young", "b3": "usa_boss", "c3": "usa_young"}
LINES = [
    ("i1", "Would you pay five dollars for absolutely nothing?", 0.98, 0.25, +0.8, 1.5, ['five', 'nothing?'], None),
    ("i2", "Over eleven thousand people did. On Black Friday.", 0.98, 0.3, +0.6, 1.45, ['Eleven', 'Black'], None),
    ("i3", "You're running a store on the biggest sale day of the year. Everybody around you is slashing prices.", 0.98, 0.25, +0.8, 1.45, ["You're", 'slashing'], None),
    ("i4", "One card game company did the opposite, year after year. Here are three crazy things it did, each one weirder.", 0.98, 0.3, +0.8, 1.5, ['opposite,', 'crazy', 'weirder.'], None),
    ("a1", "Stunt one. The game was Cards Against Humanity.", 0.97, 0.2, +1.0, 1.5, ['one.'], None),
    ("a2", "Instead of a discount, they raised the price. By five bucks.", 0.97, 0.25, +0.8, 1.5, ['raised', 'five'], None),
    ("a3", "Hold on. We're charging people more, on Black Friday?", 1.0, 0.25, +1.2, 1.5, ['Hold', 'more,'], None),
    ("a4", "Sounds like a terrible idea, right? But sales actually went up.", 0.97, 0.25, +0.6, 1.45, ['terrible', 'up.'], None),
    ("a5", "People weren't really buying a card game at all. They were buying the joke.", 0.97, 0.35, +0.8, 1.45, ["weren't", 'joke.'], 'low'),
    ("b1", "Stunt two. They pulled the game off their online store.", 0.97, 0.2, +1.0, 1.5, ['two.', 'pulled'], None),
    ("b2", "In its place? A six dollar box of actual bull poop.", 0.97, 0.3, +0.8, 1.5, ['six', 'poop.'], None),
    ("b3", "Real poop? Shut up and take my money.", 0.97, 0.25, +0.2, 1.35, ['Real', 'money.'], None),
    ("b4", "About thirty thousand people bought one, and it sold out.", 0.97, 0.3, +0.6, 1.45, ['thirty', 'sold'], None),
    ("c1", "Stunt three, the weirdest one yet.", 0.97, 0.2, +1.0, 1.5, ['three,', 'weirdest'], None),
    ("c2", "Give us five dollars, get nothing back. That was the whole deal.", 0.97, 0.25, +0.8, 1.45, ['nothing', 'whole'], None),
    ("c3", "Hi! I'm the product, and there's absolutely nothing inside me.", 1.0, 0.25, +1.2, 1.5, ['product,', 'nothing'], None),
    ("c4", "The total? About seventy-one thousand dollars. For nothing.", 0.97, 0.3, +0.8, 1.5, ['Seventy-one', 'nothing.'], None),
    ("c5", "And they didn't keep it. They split it between all seventeen employees.", 0.97, 0.2, +0.6, 1.45, ["didn't", 'seventeen'], None),
    ("c6", "One bought a longbow. Another got laser eye surgery.", 0.97, 0.35, +0.8, 1.45, ['longbow.', 'laser'], None),
    ("t1", "Here's the trick. On Black Friday, every single store yells sale.", 0.97, 0.25, +0.8, 1.5, ['trick.', 'every', 'sale.'], None),
    ("t2", "So doing the opposite got them headlines everywhere.", 0.97, 0.3, +0.8, 1.45, ['opposite', 'everywhere.'], None),
    ("d1", "Try it next sale. Don't just yell louder. Do the thing people can't stop talking about.", 0.97, 0.3, +0.8, 1.45, ["Don't", 'talking'], 'low'),
    ("z1", "Send this to the friend who lives for Black Friday.", 1.0, 0.2, +1.0, 1.45, ['friend', 'lives'], None),
    ("z2", "Would you have paid? Comment below.", 1.0, 0.0, +1.0, 1.45, ['paid?', 'Comment'], None),
]
