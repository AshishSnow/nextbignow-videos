# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# FreshNestHub 20 — "Is leftover rice safe? The risky part isn't the reheating." Facts (verified 1 Nov 2026):
# - Uncooked rice can contain spores of Bacillus cereus; the spores can survive cooking (Food Standards Scotland, 'Safe food storage: Rice';
#   McGill OSS 2019 'You're probably storing leftovers wrong (especially if it's rice)'; UF/IFAS FSHN15-06 'Preventing foodborne illness: B. cereus').
# - Left standing warm (McGill: 10-50 C), spores germinate, grow and make a toxin; 'a colony can double in size within 20 minutes if kept at
#   30 C' (McGill). The longer it takes to cool / sits at room temperature, the more likely the toxin (FSS).
# - The emetic toxin is heat-stable up to 121 C; 'reheating foods until they are steaming is not enough to inactivate the emetic toxin' (UF/IFAS);
#   'routine reheating ... will not help to deactivate the toxin' (McGill).
# - Vomiting form: incubation 1-5 h (McGill) / onset about 1-6 h (UF/IFAS); 'most frequently associated with improperly refrigerated starch
#   dishes, such as fried rice' (UF/IFAS).
# - Rules (FSS): chill it as quickly as possible, ideally within 1 hour; don't store longer than 24 hours; steaming hot all the way through;
#   never reheat more than once; cold cooked rice is safe if cooled quickly, kept in the fridge and eaten within 24 h. McGill: cool fast (NHS:
#   within 1 hour), no more than a day, never reheat more than once; fridge below 5 C. Shallow / spread out = cools faster (see e2 sources).
# - Hard fridge rice = starch RETROGRADATION: cooked (gelatinized) starch re-forms a more ordered, crystal-like structure as it cools; amylose
#   recrystallizes fast and turns long-grain rice hard (Indiana Public Media 'A Moment of Science', reviewed by Shujun Wang, PolyU); heat disrupts
#   the ordered structures so much of the softness returns (Restaurant India food-science explainer, Sep 2026).
# SCRIPT upgrade (ep 20): a ONE-SENTENCE TAKEAWAY people can repeat ('cool it in an hour, eat it in a day, heat it once, and heat it hot') built
# as a rhythm-of-four mnemonic, seeded as four rules and paid as the recap; a belief flip in the hook (it's not the reheating, it's the hours
# BEFORE the fridge); a guess beat on the fridge; the 'little pebbles' open loop paid in chapter 3.
# VOICE upgrade (ep 20): a CAUTION register for the warning lines (base -0.3 st, narrower range 1.35): people talk lower and flatter when they
# warn a friend; A/B vs the plain register (+0.4 / 1.45) on the same take.
LINES = [
    ("i1", "Do you know the risky part of leftover rice isn't heating it up again?", 0.99, 0.30, +1.0, 1.45, ["risky", "isn't"], "q"),
    ("i2", "It's the hours it sits in the pot, before it ever gets to the fridge.", 1.03, 0.35, +0.6, 1.45, ["hours", "fridge.:dn"], "low"),
    ("i3", "And yes, we'll get to why it turns into little pebbles in there, too.", 1.07, 0.35, +0.6, 1.5, ["pebbles"], None),
    ("a1", "Okay. Raw rice often carries a tiny stowaway, a germ called Bacillus cereus.", 1.04, 0.28, +0.4, 1.45, ["stowaway,", "germ"], "low"),
    ("a2", "It doesn't travel like a normal germ, though. It hides inside a spore, like a seed wearing armour.", 1.07, 0.28, +0.4, 1.45, ["spore,", "armour."], "low"),
    ("a3", "And boiling can't crack that armour, so after cooking, some spores are still in your pot, fast asleep.", 1.07, 0.35, +0.4, 1.45, ["can't", "asleep.:dn"], "low"),
    ("a4", "On their own, that's fine. Sleeping spores don't hurt anybody.", 1.04, 0.35, -0.6, 1.4, ["fine.", "Sleeping"], "low"),
    ("b1", "The trouble starts when the pot just sits there, warm and damp, for hours. That's exactly what wakes them up.", 1.07, 0.28, +0.4, 1.45, ["sits", "wakes"], "low"),
    ("b2", "They hatch, they eat, they multiply. At around thirty degrees, they can double every twenty minutes.", 1.06, 0.30, +0.8, 1.5, ["multiply.", "twenty"], "low"),
    ("b3", "Two becomes four, four becomes eight, and after a few hours on the stove, that's a crowd.", 1.07, 0.35, +0.6, 1.5, ["eight,", "crowd.:dn"], "low"),
    ("b4", "And while they party, they make a toxin. Basically, a poison.", 1.03, 0.35, +0.8, 1.5, ["toxin.", "poison.:dn"], "low"),
    ("b5", "This is the nasty bit. That toxin shrugs off heat. Microwave the rice till it's steaming, and the toxin is still there.", 1.04, 0.35, -0.3, 1.35, ["shrugs", "still"], "low"),
    ("b6", "So reheating gets the blame, but the damage was done hours earlier, while the pot sat on the stove.", 1.06, 0.30, -0.3, 1.35, ["blame,", "earlier,"], "low"),
    ("b7", "And the result? You could be throwing up within a few hours. Leftover fried rice is the classic case.", 1.04, 0.40, -0.3, 1.35, ["throwing", "classic"], "low"),
    ("c1", "So, quick guess: does the fridge actually kill these germs?", 1.01, 0.40, +0.6, 1.5, ["guess,", "kill"], "q"),
    ("c2", "Nope. Cold just slows them right down. And that's all you need, as long as the rice gets there fast.", 1.06, 0.35, +0.4, 1.45, ["Nope.", "fast.:dn"], "low"),
    ("d1", "Right, those little pebbles. Why does rice go hard in the fridge?", 1.03, 0.30, +0.8, 1.5, ["pebbles.", "hard"], "q"),
    ("d2", "When you cook rice, the starch inside soaks up water and swells. That's what makes it soft and fluffy.", 1.08, 0.28, +0.4, 1.45, ["swells.", "fluffy."], "low"),
    ("d3", "As it cools, the starch chains slowly squeeze back together into neat, tight rows, a bit like crystals.", 1.07, 0.28, +0.4, 1.45, ["squeeze", "crystals."], "low"),
    ("d4", "That has a name, retrogradation. Fancy word, simple idea: the starch is setting again.", 1.04, 0.35, +0.6, 1.5, ["retrogradation.", "setting"], "low"),
    ("d5", "Heat shakes those rows loose, and the rice goes soft again. So hard rice isn't bad rice. It's just cold starch.", 1.07, 0.40, +0.4, 1.45, ["soft", "cold"], "low"),
    ("e1", "The good news? The whole fix fits in four simple rules.", 1.04, 0.30, +0.8, 1.5, ["good", "four"], "low"),
    ("e2", "One, cool it fast and get it in the fridge within an hour. Spread it out in a wide dish and it cools much quicker.", 1.08, 0.28, +0.4, 1.45, ["hour.", "wide"], "low"),
    ("e3", "Two, eat it within a day. Three, reheat it just once. Four, make it steaming hot, all the way through.", 1.06, 0.35, +0.4, 1.45, ["day.", "once.", "steaming"], "low"),
    ("e4", "And if the pot sat out all night? Don't gamble on it. Bin it.", 1.02, 0.40, -0.3, 1.35, ["gamble", "Bin"], "low"),
    ("f1", "Good news for rice salad fans: cold rice is fine, if it got into the fridge fast and it's less than a day old.", 1.07, 0.35, +0.6, 1.5, ["fine,", "day"], "low"),
    ("g1", "So remember it like this: cool it in an hour, eat it in a day, heat it once, and heat it hot.", 1.04, 0.35, +0.6, 1.45, ["hour,", "day,", "hot.:dn"], "low"),
    ("g2", "Send this to the friend who leaves the rice on the stove all night!", 1.04, 0.00, +1.2, 1.5, ["friend", "night!"], None),
]
