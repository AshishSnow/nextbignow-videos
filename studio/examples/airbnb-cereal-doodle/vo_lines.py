# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# REAL CASE STUDY · How $40 cereal saved Airbnb — 13 Nov 2026, DOODLE look. Owner: "without real case study is boring ... script weak ...
# more research ... feel like human". One protagonist arc (broke founders -> rent -> debt -> rejection -> cereal -> YC -> the photo fix -> lesson),
# told like talking to a friend; small human details (baseball-card binder of maxed cards, hot glue, "cockroaches").
# Characters: the AIR MATTRESS narrates its own cameo (usa_young); the CEREAL BOX (usa_boss). Founders drawn as plain stick doodles with name tapes
# (no likeness). Cereal boxes are generic "ELECTION CEREAL" doodles — no candidate faces, no politics.
# Facts:
#  Penguin (The Airbnb Story, Leigh Gallagher): Oct 2007 design conference in SF, hotel rates high, rent due; air mattresses; site "AirBed &
#   Breakfast", airbeds at $80 each; three guests booked within days.
#  Product Habits: >$20k credit card debt; ~500 boxes of each cereal, ~1,000 total, $40 a box, ~$30k; Paul Graham invested $20k, YC winter 2009;
#   they rented a camera and shot NY listing photos themselves; revenue across the city doubled.
#  Microsoft BizSpark blog (2013): "a baseball card collecting binder of maxed out credit cards"; $40 cereal during the election.
#  Business Insider: boxes made with a hot glue gun; Chesky says the YC interview went poorly, a co-founder handed Graham a box of cereal;
#   Chesky: "He said we were cockroaches and that's why he funded us."
#  CNBC 18 Apr 2023: Graham via Chesky: "If you can convince people to pay $40 for $4 boxes of cereal, maybe, just maybe, you can convince
#   strangers..."; investors rejected them; market cap ~$75B (2023) -> "worth tens of billions".
#  Fresh-eyes review 13 Nov applied (helped save, investor after investor, a few days, shared binder, YC invested, Graham's NY advice).
#  Quartz: rejection emails incl. "the market doesn't seem big enough"; seed ask $150k at $1.5M valuation.
#  First Round Review: revenue flatlined at $200 per week; photos "were not great photos. People were using their camera phones";
#   Graham suggested flying to NY and upgrading photos; a week later weekly revenue doubled to $400; Gebbia: "permission to do things that don't scale".
SERIES = "HOW IT WORKS"; PART = 0; EP = 1
CBVOICES = {"a5": "usa_young", "a5b": "usa_young", "b7": "usa_boss", "c6": "usa_young"}
LINES = [
    ("i1", "Would you pay forty dollars for a box of cereal?", 0.98, 0.25, +0.8, 1.5, ['forty', 'cereal?'], None),
    ("i2", "Back in two thousand eight, people actually did. And that weird cereal helped save Airbnb.", 0.98, 0.3, +0.6, 1.45, ['actually', 'save'], None),
    ("i3", "You're broke, you're drowning in credit card debt, and investor after investor says no. Here's how they got out, in four strange moves.", 0.98, 0.3, +0.8, 1.5, ['broke,', 'four', 'strange'], None),
    ("a1", "First move. San Francisco, two thousand seven.", 0.97, 0.2, +1.0, 1.5, ['First'], None),
    ("a2", "Brian Chesky and Joe Gebbia can't make rent.", 0.97, 0.2, +0.6, 1.45, ["can't", 'rent.'], None),
    ("a3", "A huge design conference is coming to town, and the hotels are charging crazy prices. So guess what they decide to rent out?", 0.97, 0.25, +0.8, 1.45, ['huge', 'crazy', 'guess'], None),
    ("a4", "They blow up three air mattresses on the living room floor, and rent them out. Eighty bucks a night, breakfast included.", 0.97, 0.25, +0.8, 1.5, ['air', 'Eighty'], None),
    ("a5", "Yep. That's me. The very first Airbnb wasn't a house.", 1.0, 0.15, +1.2, 1.5, ['me.', 'house.'], None),
    ("a5b", "It was an air mattress.", 1.0, 0.25, +1.2, 1.5, ['mattress.'], None),
    ("a6", "Three strangers booked. For a few days, it actually worked.", 0.97, 0.3, +0.6, 1.45, ['Three', 'worked.'], 'low'),
    ("b1", "Now it gets ugly.", 0.97, 0.2, +1.0, 1.5, ['ugly.'], None),
    ("b2", "Investors kept passing. One rejection said the market just didn't seem big enough.", 0.97, 0.25, +0.6, 1.45, ['passing.', 'big'], None),
    ("b3", "By then, they owed over twenty thousand dollars on credit cards.", 0.97, 0.25, +0.6, 1.45, ['twenty'], None),
    ("b4", "Their maxed-out cards filled a baseball card binder. That's how many there were.", 0.97, 0.3, +0.8, 1.45, ['binder.', 'many'], None),
    ("b5", "So what do you do when you're that broke? Move number two.", 0.97, 0.15, +0.8, 1.5, ['broke?', 'two.'], None),
    ("b5b", "Something ridiculous. It was election season, so they made their own cereal.", 0.97, 0.25, +0.8, 1.5, ['ridiculous.', 'cereal.'], None),
    ("b6", "Election-themed boxes, glued together by hand, sold for forty bucks each.", 0.97, 0.25, +0.8, 1.45, ['hand,', 'forty'], None),
    ("b7", "I'm cheap cereal in a forty dollar box. Don't ask questions.", 0.97, 0.25, +0.2, 1.35, ['cheap', "Don't"], None),
    ("b8", "Did it work? They sold about a thousand boxes. That brought in around thirty thousand dollars, and kept the company alive.", 0.97, 0.3, +0.6, 1.45, ['thousand', 'alive.'], None),
    ("c1", "Move number three happened in an interview that went wrong.", 0.97, 0.2, +1.0, 1.5, ['three', 'wrong.'], None),
    ("c2", "They pitched Paul Graham at Y Combinator, and Chesky says it went badly.", 0.97, 0.25, +0.6, 1.45, ['Paul', 'badly.'], None),
    ("c3", "So one of them handed him a box of cereal.", 0.97, 0.3, +0.8, 1.45, ['cereal.'], None),
    ("c4", "His point, as Chesky tells it? If people pay forty bucks for cheap cereal, maybe they'll sleep in strangers' homes too.", 0.97, 0.25, +0.6, 1.45, ['forty', 'strangers\''], None),
    ("c5", "He called them cockroaches. They just wouldn't die. So Y Combinator invested twenty thousand dollars.", 0.97, 0.3, +0.8, 1.5, ['cockroaches.', 'die.', 'twenty'], None),
    ("c6", "Cockroaches? Wow, rude. But honestly, kind of fair.", 1.0, 0.25, +1.2, 1.5, ['rude.', 'fair.'], None),
    ("d1", "And the last move? The fix nobody expected.", 0.97, 0.2, +1.0, 1.5, ['last', 'nobody'], None),
    ("d2", "Even after all that, the site was stuck at about two hundred dollars a week.", 0.97, 0.25, +0.6, 1.45, ['stuck', 'hundred'], None),
    ("d3", "Then someone looked closely at their New York listings. The photos were terrible.", 0.97, 0.25, +0.8, 1.45, ['closely', 'terrible.'], None),
    ("d4", "Graham's advice? Go fix it yourselves. So they flew to New York, rented a real camera, and shot the photos.", 0.97, 0.25, +0.8, 1.45, ['yourselves.', 'flew'], None),
    ("d5", "One week later, their weekly revenue had doubled.", 0.97, 0.25, +1.0, 1.5, ['doubled.'], None),
    ("d6", "Today, Airbnb is worth tens of billions of dollars.", 0.97, 0.3, +0.8, 1.45, ['tens', 'billions'], None),
    ("t1", "No new app, no ad campaign, nothing fancy. Just better photos, done by hand.", 0.97, 0.3, +0.8, 1.45, ['photos,', 'hand.'], None),
    ("t2", "Paul Graham even wrote a famous essay about this idea. Do things that don't scale.", 0.97, 0.3, +0.8, 1.5, ["don't", 'scale.'], None),
    ("e1", "Stuck right now? Try it next time. Do one thing by hand that big companies won't.", 0.97, 0.3, +0.8, 1.45, ['hand', "won't."], 'low'),
    ("z1", "Send this to the friend who has a stuck side hustle.", 1.0, 0.2, +1.0, 1.45, ['friend', 'stuck'], None),
    ("z2", "Which startup story should I break down next? Comment below.", 1.0, 0.0, +1.0, 1.45, ['next?', 'Comment'], None),
]
