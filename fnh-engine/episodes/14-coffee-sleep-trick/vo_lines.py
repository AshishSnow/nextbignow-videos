# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# FreshNestHub 14 — "Coffee doesn't give you energy" (caffeine is a look-alike of adenosine, the sleepy chemical that piles up
# while you're awake; it plugs the brain's adenosine locks without turning them, so tiredness is hidden, not removed; the pile
# keeps growing and can hit at once when caffeine wears off; half-life 3-5 h -> a 2 pm coffee is ~1/4 there at bedtime; 2013
# sleep study: caffeine 6 h before bed cut sleep by > 1 h and people didn't notice; daily drinkers may grow extra locks; bonus:
# coffee + citrus flowers lace nectar with caffeine and bees remember them 3x better)
# Script upgrade (ep 14): one running metaphor for the whole system (sleepy keys + locks + a fake key), a "loan with interest"
# frame planted at 6 s and paid at the crash (~45 %), a live graph of the day that the viewer watches being drawn, 5 chapters,
# one practical takeaway (last cup earlier) + one share-worthy twist (bees).
LINES = [
    ("i1", "Do you know coffee doesn't give you any energy?", 0.96, 0.30, +1.0, 1.45, ["doesn't", "energy?"], "q"),
    ("i2", "Not one bit. It just hides how tired you are.", 1.0, 0.40, +1.2, 1.5, ["hides", "tired"], None),
    ("i3", "And that tiredness comes back later. With interest.", 0.98, 0.45, +1.0, 1.5, ["back", "interest."], None),
    ("a1", "Here's how it works. All day, your brain cells use energy.", 1.02, 0.35, +0.8, 1.45, ["works.", "energy."], "low"),
    ("a2", "And as they work, a chemical builds up. It's called adenosine.", 1.02, 0.40, +0.8, 1.45, ["builds", "adenosine."], "low"),
    ("a3", "Think of it as sleepy keys. The longer you're awake, the more pile up.", 1.02, 0.40, +0.8, 1.45, ["sleepy", "more"], "low"),
    ("a4", "Your brain cells have tiny locks for those keys.", 1.02, 0.35, +0.8, 1.45, ["locks"], "low"),
    ("a5", "When a sleepy key clicks in, the cell slows down. And you feel tired.", 1.0, 0.40, +0.8, 1.45, ["clicks", "tired."], "low"),
    ("a6", "That's how your body knows it's time to sleep.", 1.0, 0.45, +0.8, 1.45, ["sleep."], "low"),
    ("b1", "Now, let's say you drink a cup of coffee.", 0.98, 0.35, +1.0, 1.5, ["coffee."], None),
    ("b2", "The caffeine travels in your blood, all the way to your brain.", 1.02, 0.35, +0.8, 1.45, ["blood,", "brain."], "low"),
    ("b3", "And here's the trick. Caffeine looks a lot like adenosine.", 1.0, 0.35, +1.0, 1.5, ["trick.", "like"], None),
    ("b4", "So it slips into the same locks... but it can't turn them.", 1.0, 0.35, +0.8, 1.45, ["same", "can't"], "low"),
    ("b5", "It just sits there. A fake key, blocking the way.", 1.0, 0.35, +0.8, 1.45, ["fake", "blocking"], "low"),
    ("b6", "The sleepy keys can't get in. So you feel awake.", 1.02, 0.40, +0.8, 1.45, ["can't", "awake."], "low"),
    ("b7", "But you didn't get new energy. Your tiredness is just hidden.", 0.98, 0.45, +1.0, 1.5, ["new", "hidden."], None),
    ("c1", "But here's the weird part.", 0.97, 0.30, +1.0, 1.5, ["weird"], None),
    ("c2", "The whole time, sleepy keys keep piling up behind the block.", 1.02, 0.40, +0.8, 1.45, ["piling"], "low"),
    ("c3", "When the caffeine wears off, they can rush in all at once.", 1.0, 0.35, +1.0, 1.5, ["rush", "once."], None),
    ("c4", "That's the crash. One food scientist says coffee only lends you that awake feeling.", 1.0, 0.45, +0.8, 1.45, ["crash.", "lends"], "low"),
    ("d1", "So how long does the loan last?", 0.97, 0.30, +1.0, 1.5, ["long"], "q"),
    ("d2", "Your body needs three to five hours to clear just half of it.", 1.02, 0.40, +0.8, 1.45, ["half"], "low"),
    ("d3", "So a coffee at two in the afternoon? About a quarter can still be there at bedtime.", 1.0, 0.40, +0.8, 1.45, ["quarter", "bedtime."], "low"),
    ("d4", "In one sleep study, people took caffeine six hours before bed.", 1.02, 0.35, +0.8, 1.45, ["six"], "low"),
    ("d5", "They lost over an hour of sleep. And they didn't even notice!", 0.98, 0.45, +1.2, 1.5, ["lost", "notice!"], None),
    ("d6", "So if sleep is hard, try having your last cup earlier in the day.", 1.0, 0.45, +0.8, 1.45, ["earlier"], "low"),
    ("e1", "And if you drink it every day?", 0.97, 0.30, +1.0, 1.5, ["every"], "q"),
    ("e2", "Your brain may build extra locks.", 1.0, 0.30, +0.8, 1.45, ["extra"], "low"),
    ("e2b", "So you need more caffeine, just to feel the same.", 1.02, 0.40, +0.8, 1.45, ["more"], "low"),
    ("e3", "Here's a bonus. You're not the only one who's hooked.", 0.98, 0.35, +1.0, 1.5, ["bonus.", "hooked."], None),
    ("e4", "Coffee and lemon flowers put a little caffeine in their nectar.", 1.02, 0.35, +0.8, 1.45, ["caffeine"], "low"),
    ("e5", "Bees that sip it are three times more likely to remember that flower the next day.", 1.0, 0.40, +0.8, 1.45, ["three", "remember"], "low"),
    ("e6", "So the bees keep coming back. Sound familiar?", 0.97, 0.45, +1.0, 1.5, ["back.", "familiar?"], "q"),
    ("f1", "Remember: caffeine doesn't add energy. It blocks the tired signal. And the tiredness waits for you.", 1.0, 0.40, +0.8, 1.45, ["blocks", "waits"], "low"),
    ("f2", "Send this to the friend who drinks coffee at night and can't sleep!", 0.97, 0.0, +1.2, 1.5, ["friend", "night"], None),
]
