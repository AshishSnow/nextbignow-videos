# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# HOW IT WORKS · "Sell me this pen" — 11 Nov 2026. Owner sent a street skit ("hater challenges millionaire to sell a pen") and asked for our
# version with an American accent. OUR OWN script and invented characters (an interviewer and a candidate), not the skit's people or lines.
# Voices: narrator usa_narr, candidate usa_young, interviewer usa_boss (all our own Kokoro American voices -> Chatterbox; synthetic only).
# Facts: "Sell me this pen" — final scene of The Wolf of Wall Street (2013 film); Jordan Belfort quoted in The Globe and Mail (via Yesware,
# "The Best Way to Answer 'Sell Me This Pen'"): "before I'm even going to sell a pen to anybody, I need to know about the person".
# Advice to ask questions first: Yesware; Joel Comm ("If you want to sell the pen, you ask the buyer questions").
SERIES = "HOW IT WORKS"; PART = 0; EP = 1
CBVOICES = {"i1": "usa_boss", "a2": "usa_young", "a3": "usa_boss", "c1": "usa_young", "c2": "usa_boss", "c3": "usa_young",
            "c4": "usa_boss", "c5": "usa_young", "c6": "usa_boss"}
LINES = [
    ("i1", "Can you sell me this pen?", 0.97, 0.3, +0.0, 1.3, ['sell', 'pen?'], None),
    ("i2", "Do you know why this famous sales test costs so many people the job?", 0.98, 0.25, +1.0, 1.5, ['costs', 'job?'], None),
    ("i3", "You're in the interview chair, and one bad answer can lose you the job. The best answer has three steps, and the last one's the smartest.", 0.98, 0.3, +0.8, 1.5, ['chair.', 'three', 'smartest.'], None),
    ("a1", "First, the move most people make.", 0.97, 0.2, +0.8, 1.5, ['most'], None),
    ("a2", "This pen writes super smooth, it never smudges, and it's only three bucks!", 1.0, 0.25, +1.4, 1.6, ['smooth,', 'five'], None),
    ("a3", "I don't need a pen.", 0.97, 0.35, +0.0, 1.3, ['need'], 'low'),
    ("a4", "Game over. He talked about the pen, and nobody asked about the pen.", 0.97, 0.3, +0.8, 1.5, ['over.', 'nobody'], 'low'),
    ("b0", "This line got famous from the movie The Wolf of Wall Street.", 0.97, 0.2, +0.6, 1.45, ['famous', 'Wolf'], None),
    ("b1", "Jordan Belfort, the real broker the movie's based on, put it simply. Before he sells a pen to anybody, he needs to know about the person.", 0.97, 0.25, +0.6, 1.45, ['simply.', 'person.'], None),
    ("b2", "So the pros start with questions. Watch this.", 0.97, 0.3, +1.0, 1.5, ['questions.', 'Watch'], None),
    ("c1", "When did you last use a pen?", 1.0, 0.25, +1.0, 1.5, ['last'], None),
    ("c2", "This morning. I signed a big contract.", 0.97, 0.25, +0.0, 1.3, ['morning.', 'big'], None),
    ("c3", "And what if your pen had died right then?", 1.0, 0.25, +1.2, 1.5, ['died'], None),
    ("c4", "Honestly? That would've been pretty embarrassing.", 0.97, 0.25, +0.2, 1.35, ['Honestly?', 'embarrassing.'], None),
    ("c5", "So you need one that never lets you down. This one's yours for three bucks.", 1.0, 0.25, +1.0, 1.5, ['never', 'yours'], None),
    ("c6", "Okay, you got me. I'll take it, and I might grab a spare for the car.", 0.97, 0.4, +0.2, 1.35, ['got', 'take'], None),
    ("d1", "Same pen, same price. So what changed? He found the need before he pitched.", 0.97, 0.3, +1.0, 1.5, ['Same', 'need', 'before'], None),
    ("d2", "Works in any business. List features, and you're just noise. Find their problem first, and you're the answer.", 0.97, 0.3, +0.8, 1.45, ['noise.', 'answer.'], None),
    ("d3", "Try it next time. Step one, ask questions. Step two, find the need. Step three, sell it back in their own words.", 0.97, 0.3, +0.8, 1.5, ['one,', 'two,', 'three,', 'own'], 'low'),
    ("z1", "Save this. Send this to the friend who always oversells.", 1.0, 0.2, +1.0, 1.45, ['Save', 'oversells.'], None),
    ("z2", "Comment what I should sell you next.", 1.0, 0.0, +1.0, 1.45, ['Comment', 'next.'], None),
]
