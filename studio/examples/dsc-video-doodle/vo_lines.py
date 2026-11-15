# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# TREND + REAL CASE STUDY + HOW TO START — "The $4,500 video" (Dollar Shave Club) — 15 Nov 2026, DOODLE format, no music, chunked subtitles.
# Built from the reviewed queue script episodes/queue/27-dollar-shave-video, rewritten with the owner's 15 Nov reference-reel rules:
# fact hook + viewer's own question; "here's how it works" in 2 tiny steps; the viewer's questions asked out loud one by one; everyday math;
# "The upside? ... The catch? ..."; real quote; kill the myth; callback ending to line 2; 4 moves to start your own launch.
# Characters: DOLLAR RAZOR (usa_young), PRICEY STORE RAZOR (usa_boss) — generic doodles; Dubin = plain stick doodle with a name tape;
# the video's profane title is never said or shown. No DSC/Unilever/Gillette logos or packaging.
# Facts (re-verified 15 Nov 2026):
#  Fortune 10 Mar 2015: "I spent about $4,500 on it."; directed "by a friend of mine who I had studied improv comedy with in New York";
#   "shot it in about eight hours in the original warehouse in Gardena, Calif."; "razors are really expensive in the store."; "The site crashed
#   because of the traffic ... we ran out of inventory in the first six hours."; labels: "we were hurling them over the fence at night".
#  WSJ 12 Apr 2012 (Yahoo republish): "12,000 people signed up in the first 48 hours"; "some four million views"; "$1 a month plus $2 in shipping".
#  Emory Magazine 2018 + Entrepreneur 2017: at a cocktail party a friend's father-in-law had a warehouse full of razor blades; marketing + improv.
#  TechCrunch / Entrepreneur: launch 6 Mar 2012.
#  VentureBeat + Progressive Grocer 2016: Unilever bought it, terms not disclosed, reported ~$1 billion; 3.2 million members.
SERIES = "YOUR MOVE"; PART = 0; EP = 1
CBVOICES = {"a3": "usa_boss", "b4": "usa_young", "c9": "usa_young"}
LINES = [
    ("i1", "Can one cheap, homemade video build a billion-dollar company?", 0.98, 0.25, +0.8, 1.5, ['homemade', 'billion-dollar'], None),
    ("i2", "And could you pull it off too, on a tiny budget?", 0.98, 0.25, +0.8, 1.5, ['you', 'tiny'], None),
    ("i3", "Imagine you're him. Nobody knows your name, and you bet your whole launch on one forty-five-hundred-dollar video.", 0.98, 0.2, +0.6, 1.45, ['Nobody', 'forty-five'], None),
    ("i4", "Here's what happened. Then four moves you can steal for your own launch.", 0.98, 0.3, +0.8, 1.5, ['four', 'steal'], None),
    ("a1", "Meet Michael Dubin. He worked in marketing, and took improv comedy classes at night.", 0.97, 0.2, +0.6, 1.45, ['marketing,', 'improv'], None),
    ("a2", "At a party, a friend's father-in-law told him about a warehouse full of razor blades.", 0.97, 0.25, +0.6, 1.45, ['party,', 'warehouse'], None),
    ("a3", "Meanwhile, I'm the store razor. I'm fancy, I'm locked up, and I'm expensive.", 0.97, 0.25, +0.2, 1.35, ['fancy,', 'expensive.'], None),
    ("a4", "So here's how his idea works. Step one, you sign up online.", 0.97, 0.15, +0.8, 1.5, ['works.', 'online.'], None),
    ("a5", "Step two, fresh blades show up in your mailbox. Every single month.", 0.97, 0.2, +0.8, 1.45, ['mailbox.', 'month.'], None),
    ("a6", "The cheapest plan? A dollar a month, plus two bucks for shipping.", 0.97, 0.2, +0.8, 1.5, ['dollar', 'shipping.'], None),
    ("a7", "So about three bucks. That's less than one fancy coffee.", 0.97, 0.3, +0.6, 1.45, ['three', 'coffee.'], 'low'),
    ("b1", "But how do you get noticed, when ads cost a fortune?", 0.97, 0.2, +1.0, 1.5, ['noticed,', 'fortune?'], None),
    ("b2", "He wrote a funny launch video, and starred in it himself.", 0.97, 0.25, +0.8, 1.5, ['funny', 'himself.'], None),
    ("b3", "A buddy from improv class directed, and they shot the whole thing right there in the warehouse.", 0.97, 0.2, +0.6, 1.45, ['buddy', 'warehouse.'], None),
    ("b3b", "Start to finish, in about eight hours.", 0.97, 0.25, +0.8, 1.5, ['eight'], None),
    ("b4", "One warehouse, one camera, one very confident man. And me.", 1.0, 0.25, +1.2, 1.5, ['confident', 'me.'], None),
    ("b5", "Did it cost a fortune? Dubin told Fortune magazine, I spent about forty-five hundred dollars on it.", 0.97, 0.3, +0.8, 1.45, ['fortune?', 'forty-five'], None),
    ("c1", "On March sixth, twenty twelve, the video went live.", 0.97, 0.2, +1.0, 1.5, ['March', 'live.'], None),
    ("c2", "So, did it work? The website crashed from all the traffic.", 0.97, 0.25, +0.8, 1.5, ['work?', 'crashed'], None),
    ("c3", "The upside? People wanted it, badly. They ran out of razors in six hours.", 0.97, 0.25, +0.8, 1.45, ['upside?', 'six'], None),
    ("c4", "The catch? Now they had to ship every single one of those orders.", 0.97, 0.2, +0.8, 1.45, ['catch?', 'ship'], None),
    ("c5", "So the team printed thousands of shipping labels at the office.", 0.97, 0.2, +0.6, 1.45, ['thousands', 'labels'], None),
    ("c6", "And at night, they threw them over the warehouse fence.", 0.97, 0.3, +0.8, 1.45, ['night,', 'fence.'], 'low'),
    ("c7", "Was it just a fluke? Within days, about twelve thousand people had signed up.", 0.97, 0.25, +0.8, 1.45, ['fluke?', 'twelve'], None),
    ("c8", "Four years later, Unilever bought the company. Reportedly for about a billion dollars.", 0.97, 0.25, +0.8, 1.5, ['Unilever', 'billion'], None),
    ("c8b", "Members by then? Over three million.", 0.97, 0.3, +0.6, 1.45, ['Members', 'three'], None),
    ("c9", "A billion dollars, for a razor that costs a dollar? I'll take it.", 1.0, 0.25, +1.2, 1.5, ['billion', 'take'], None),
    ("t1", "So, did the video need a giant budget? Nope.", 0.97, 0.2, +0.8, 1.5, ['giant', 'Nope.'], None),
    ("t2", "He had a clear idea, a funny friend, and the guts to be on camera.", 0.97, 0.3, +0.8, 1.45, ['clear', 'guts'], None),
    ("s1", "So how could you do this for your own launch? Four moves.", 0.97, 0.2, +0.8, 1.5, ['you', 'Four'], None),
    ("s2", "Move one. Explain your idea in one sentence a ten-year-old gets.", 0.97, 0.2, +0.8, 1.5, ['one.', 'sentence'], None),
    ("s2b", "His was simple. Good blades, a dollar a month.", 0.97, 0.25, +0.8, 1.5, ['simple.', 'dollar'], None),
    ("s3", "Move two. Be the face. You don't need actors, you need your own personality.", 0.97, 0.2, +0.8, 1.45, ['face.', 'personality.'], None),
    ("s4", "Move three. Shoot it cheap, in your real space, with friends who are funny.", 0.97, 0.2, +0.8, 1.45, ['cheap,', 'real'], None),
    ("s5", "And move four, the one everybody forgets. Get ready for it to actually work.", 0.97, 0.25, +0.8, 1.45, ['forgets.', 'work.'], None),
    ("s5b", "Stock up and plan your shipping first, because remember, they sold out in just six hours.", 0.97, 0.3, +0.6, 1.45, ['shipping', 'six'], 'low'),
    ("e1", "So, could you pull it off too? No promises. But a clear idea gives you a real shot.", 0.97, 0.3, +0.8, 1.45, ['promises.', 'clear'], None),
    ("e2", "Try it next time you can't afford ads. Make the thing people send to a friend.", 0.97, 0.3, +0.8, 1.45, ["can't", 'friend.'], 'low'),
    ("z1", "Send this to the friend who still pays way too much for razors.", 1.0, 0.2, +1.0, 1.45, ['friend', 'razors.'], None),
    ("z2", "Would you put your own face in your first ad? Comment YES or NO.", 1.0, 0.0, +1.0, 1.45, ['face', 'YES'], None),
]
