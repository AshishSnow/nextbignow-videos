# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# REAL CASE STUDY · DOODLE look · "The $4,500 video that sold razors by the million" (Dollar Shave Club) — R&D writers' room 15 Nov 2026.
# One arc: pricey razors + a guy with no ad money -> a warehouse of unsold blades -> one cheap, funny video -> the launch breaks everything
# (site down, sold out in six hours, labels thrown over a fence) -> 12k sign-ups in 48 h -> 3.2M members, ~$1B Unilever deal -> lesson.
# Characters: a DOLLAR RAZOR (usa_young) and a snooty PRICEY RAZOR in a locked case (usa_boss) — generic doodles, no real brand, logo or packaging;
# the founder = a plain stick doodle with a name tape (no likeness). The video's profane title is never said or shown: "a launch video".
# Facts + quotes: SOURCES.md (Fortune 10 Mar 2015, WSJ 12 Apr 2012, TechCrunch 6 Mar 2012, Entrepreneur 2012/2017, AP 20 Jul 2016, Fortune 19 Jul 2016).
SERIES = "HOW THEY GOT SO BIG"; PART = 0; EP = 1
CBVOICES = {"a4": "usa_boss", "b4": "usa_young", "d6": "usa_young"}
LINES = [
    ("i1", "Would you bet your new business on a forty-five-hundred-dollar video?", 0.98, 0.25, +0.8, 1.5, ['bet', 'video?'], None),
    ("i2", "One guy did. Four million people watched it in about a month.", 0.98, 0.3, +0.6, 1.45, ['Four', 'month.'], None),
    ("i3", "You've got a warehouse of razor blades, no money for ads, and one shot to get noticed. Four moves got him out.", 0.98, 0.3, +0.8, 1.5, ['no', 'Four'], None),
    ("a1", "First move. The blades.", 0.97, 0.2, +1.0, 1.5, ['blades.'], None),
    ("a2", "Michael Dubin works in marketing and takes improv classes at night. He's not a razor guy.", 0.97, 0.25, +0.6, 1.45, ['improv', 'razor'], None),
    ("a3", "At a party, a friend's father-in-law mentions a warehouse full of razor blades he can't sell. What would you do with them?", 0.97, 0.25, +0.8, 1.45, ['warehouse', "can't"], None),
    ("a4", "And at the store, my kind lives behind locked plastic. Premium, dear.", 0.97, 0.25, +0.2, 1.35, ['locked', 'Premium,'], None),
    ("a5", "Dubin's pitch is simple. Razors are expensive in the store. So mail them, every month, for a dollar plus shipping.", 0.97, 0.25, +0.6, 1.45, ['expensive', 'dollar'], None),
    ("b1", "Move two. Nobody knows who you are, and ads cost a fortune. So how do you get noticed?", 0.97, 0.2, +1.0, 1.5, ['two.', 'noticed?'], None),
    ("b2", "He writes a funny launch video, and he's the star.", 0.97, 0.25, +0.6, 1.45, ['funny', 'star.'], None),
    ("b3", "A friend from his improv class directs it. They shoot it among the crates, in about a day.", 0.97, 0.25, +0.6, 1.45, ['friend', 'day.'], None),
    ("b4", "Yep. One warehouse, one day, one very confident man. And me, the dollar razor.", 1.0, 0.25, +1.2, 1.5, ['confident', 'dollar'], None),
    ("b5", "Total cost? Dubin told Fortune he spent about forty-five hundred dollars on it.", 0.97, 0.3, +0.8, 1.45, ['Total', 'forty-five'], None),
    ("c1", "Move three. On March sixth, twenty twelve, the video goes live.", 0.97, 0.2, +1.0, 1.5, ['three.', 'live.'], None),
    ("c2", "And it breaks everything.", 0.97, 0.25, +0.8, 1.5, ['everything.'], 'low'),
    ("c3", "The site crashes from the traffic.", 0.97, 0.2, +0.6, 1.45, ['crashes'], None),
    ("c4", "Dubin told Fortune they ran out of razors in the first six hours.", 0.97, 0.25, +0.8, 1.45, ['out', 'six'], None),
    ("c5", "The warehouse isn't set up for orders like this. So his team prints thousands of shipping labels at the office.", 0.97, 0.25, +0.6, 1.45, ['thousands', 'labels'], None),
    ("c6", "At night, they toss them over the warehouse fence.", 0.97, 0.3, +0.8, 1.45, ['night,', 'fence.'], 'low'),
    ("c7", "Honestly? That's the best kind of disaster. Too many customers.", 0.97, 0.3, +0.8, 1.45, ['best', 'many'], None),
    ("d1", "Last move. Turn one funny video into a real business. Does it last?", 0.97, 0.2, +1.0, 1.5, ['Last', 'last?'], None),
    ("d2", "The company told The Wall Street Journal about twelve thousand people signed up. In just the first two days.", 0.97, 0.25, +0.8, 1.45, ['twelve', 'two'], None),
    ("d3", "Jump to twenty fifteen. By then the club has over three million members.", 0.97, 0.25, +0.8, 1.45, ['three', 'members.'], None),
    ("d4", "And about a hundred fifty million dollars in sales that year.", 0.97, 0.25, +0.8, 1.45, ['hundred', 'fifty'], None),
    ("d5", "In twenty sixteen, Unilever bought it. The price? Reports put it at about a billion dollars.", 0.97, 0.3, +0.8, 1.5, ['Unilever', 'billion'], None),
    ("d6", "A billion dollars, for a razor that costs a dollar? I'll take it.", 1.0, 0.25, +1.2, 1.5, ['billion', 'take'], None),
    ("t1", "No big ad budget. Just a joke, and a buddy with a camera.", 0.97, 0.3, +0.8, 1.45, ['joke,', 'camera.'], None),
    ("t2", "Try it next time. Can't afford ads? Make the one thing your customers would send to a friend.", 0.97, 0.3, +0.8, 1.45, ["Can't", 'friend.'], 'low'),
    ("z1", "Send this to the friend who still pays too much for razors.", 1.0, 0.2, +1.0, 1.45, ['friend', 'razors.'], None),
    ("z2", "Would you put your own face in your first ad? Tell me in the comments.", 1.0, 0.0, +1.0, 1.45, ['face', 'comments.'], None),
]
