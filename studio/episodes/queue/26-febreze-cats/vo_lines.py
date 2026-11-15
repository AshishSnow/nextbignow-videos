# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# REAL CASE STUDY · DOODLE look · "How nine cats saved Febreze" — R&D writers' room 15 Nov 2026 (format of examples/airbnb-cereal-doodle).
# One arc: P&G's smell-killer flops in test markets -> researchers visit homes -> the nine-cat house (people stop smelling their own smells)
# -> the Scottsdale bed-making tape ("minicelebration") -> perfume added, sold as the last step of cleaning -> sales doubled, $230M, $1B brand.
# Characters: the SPRAY BOTTLE (usa_young) and a smug CAT (usa_boss) — generic doodles, no P&G logo/trade dress: the bottle's tape label reads
# "SMELL KILLER". People = plain stick doodles with name tapes (no likeness). The whole insight story is Charles Duhigg's reporting (NYT Magazine
# 16/19 Feb 2012 + The Power of Habit) -> said as his telling. Facts + quotes: SOURCES.md.
SERIES = "HOW THEY GOT SO BIG"; PART = 0; EP = 1
CBVOICES = {"a6": "usa_young", "c7": "usa_boss", "e7": "usa_young"}
LINES = [
    ("i1", "Would you pay for a spray that makes your house smell like nothing?", 0.98, 0.25, +0.8, 1.5, ['pay', 'nothing?'], None),
    ("i2", "Procter and Gamble bet millions of dollars that you would. And at first, it flopped.", 0.98, 0.3, +0.6, 1.45, ['millions', 'flopped.'], None),
    ("i3", "You're on the team selling it, and it's flopping. Nine cats help turn it around. Them, and a busy mom.", 0.98, 0.3, +0.8, 1.5, ['flopping.', 'cats'], None),
    ("a1", "Clue one. The mid nineties.", 0.97, 0.2, +1.0, 1.5, ['Clue'], None),
    ("a2", "The company has a clear, cheap liquid that actually gets rid of bad smells.", 0.97, 0.25, +0.6, 1.45, ['clear,', 'rid'], None),
    ("a3", "In Charles Duhigg's telling, a scientist comes home and his wife notices his clothes don't smell of smoke.", 0.97, 0.25, +0.6, 1.45, ['wife', 'smoke.'], None),
    ("a5", "They call it Febreze, and they test it in Phoenix, Salt Lake City and Boise. What could go wrong?", 0.97, 0.25, +0.8, 1.45, ['Febreze,', 'test'], None),
    ("a6", "Hi, that's me. Cigarette smoke, wet dog, your brother's gym socks? I make them all disappear.", 1.0, 0.25, +1.2, 1.5, ['me.', 'disappear.'], None),
    ("b2", "The first ads? A woman whose jacket smells like a smoky restaurant. Then a dog who lives on the couch.", 0.97, 0.25, +0.6, 1.45, ['jacket', 'couch.'], None),
    ("b3", "Sales start small. Then they get smaller.", 0.97, 0.25, +0.6, 1.45, ['small.', 'smaller.'], 'low'),
    ("b4", "Duhigg puts it bluntly in the New York Times. Febreze was a dud.", 0.97, 0.3, +0.6, 1.45, ['bluntly', 'dud.'], 'low'),
    ("b5", "So the team goes into people's homes to find out why.", 0.97, 0.25, +0.8, 1.45, ['homes', 'why.'], None),
    ("c1", "Clue two. A house outside Phoenix, with nine cats.", 0.97, 0.2, +1.0, 1.5, ['Clue', 'cats.'], None),
    ("c2", "The woman who lives there is a neat freak. But that many cats?", 0.97, 0.25, +0.6, 1.45, ['neat', 'cats?'], None),
    ("c3", "The researchers ask about the cat smell.", 0.97, 0.2, +0.6, 1.45, ['cat', 'smell.'], None),
    ("c4", "And she says, isn't it wonderful? They hardly smell at all.", 0.97, 0.3, +0.8, 1.45, ['wonderful?', 'hardly'], None),
    ("c5", "Why? Live with a smell every day, and your nose stops noticing it.", 0.97, 0.25, +0.6, 1.45, ['every', 'noticing'], None),
    ("c7", "What smell? I smell amazing, thank you very much.", 1.0, 0.25, +0.4, 1.35, ['What', 'amazing.'], None),
    ("c8", "Honestly? That's brutal. The spray works, and the people who need it most can't tell.", 0.97, 0.3, +0.8, 1.45, ['brutal.', 'most'], None),
    ("d1", "Clue three. A bed near Scottsdale, Arizona. What does a bed have to do with it?", 0.97, 0.2, +1.0, 1.5, ['Clue', 'bed'], None),
    ("d2", "The researchers visit a mom of four there, and follow her real cleaning routine.", 0.97, 0.25, +0.6, 1.45, ["mom", "routine."], None),
    ("d3", "She makes the bed. Tightens the corners. Then she sprays the comforter.", 0.97, 0.25, +0.8, 1.45, ['corners.', 'sprays'], None),
    ("d4", "Her words: spraying feels like a little mini celebration when I'm done with a room.", 0.97, 0.3, +0.8, 1.45, ['mini', 'celebration'], None),
    ("d5", "That's the turn. The spray could be the little reward at the end of cleaning.", 0.97, 0.3, +0.8, 1.5, ['turn.', 'reward'], None),
    ("e1", "The fix. What do you do with a spray that smells like nothing? You make it smell like something.", 0.97, 0.2, +1.0, 1.5, ['fix.', 'something.'], None),
    ("e2", "They add more perfume. New ads show open windows and freshly made beds.", 0.97, 0.25, +0.6, 1.45, ['perfume.', 'windows'], None),
    ("e3", "In the summer of nineteen ninety-eight, it comes back as the last step after you clean.", 0.97, 0.25, +0.6, 1.45, ['last', 'clean.'], None),
    ("e4", "Did it work? Duhigg reports that within two months, sales doubled.", 0.97, 0.25, +1.0, 1.5, ['two', 'doubled.'], None),
    ("e5", "A year later, it brought in two hundred thirty million dollars.", 0.97, 0.25, +0.8, 1.45, ['hundred', 'thirty'], None),
    ("e6", "When Duhigg writes about it, Febreze and its spin-offs sell over a billion dollars a year.", 0.97, 0.3, +0.8, 1.45, ['billion'], None),
    ("e7", "Told you. I can make anything disappear, even bad sales.", 1.0, 0.25, +1.2, 1.5, ['Told', 'sales.'], None),
    ("t1", "Same spray, a little more perfume. Mostly, they changed when you use it.", 0.97, 0.3, +0.8, 1.45, ['Mostly,', 'when'], None),
    ("t2", "Try it next time. Don't sell the fix. Tie your product to something people already do, and make it feel like a treat.", 0.97, 0.3, +0.8, 1.45, ['already', 'treat.'], 'low'),
    ("z1", "Send this to the friend who sprays air freshener every time they clean.", 1.0, 0.2, +1.0, 1.45, ['friend', 'clean.'], None),
    ("z2", "What's one smell in your house you've stopped noticing? Tell me in the comments.", 1.0, 0.0, +1.0, 1.45, ['stopped', 'comments.'], None),
]

