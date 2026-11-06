# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# FreshNestHub 25 — "Can you test ghee at home?" Facts (verified 6 Nov 2026):
# - Home checks 'cannot establish purity or identify adulterants. Only laboratory testing can confirm' (Karmactive 26 Oct 2026); most ghee adulteration 'almost impossible to detect without advanced laboratory equipment', Ramaprasad T R, CFTRI (Deccan Herald, Bengaluru experts).
# - Water test + palm test as usually told: float = pure; 'melts and slides = pure' (The Better India 3 Jul 2024). Pure: 'graininess remains perceptible' (Arya, ICT, Deccan Herald). Floating: every kitchen oil floats on water (everyday physics, our reasoning).
# - Palm olein melting point 26.3 C; market vanaspati 37.2 C (Nadeem et al., J Food Sci Technol 2014, PMC4375235). No source for whole palm oil, so the line says 'the runny part of palm oil'.
# - Junagadh, 26 Oct 2026 (DeshGujarat): SOG police, 500 kg, 'allegedly made using soybean oil, castor oil, artificial flavours and chemicals', 'sold as pure Gir cow ghee', essence bottles, three tin-sealing machines, 1,000 sealing foils, counterfeit labels, tins 'did not carry expiry dates or batch numbers'; lab report pending -> 'police say'.
# - Fakes: vegetable oils, palm, cottonseed (Hazra et al., Indian J Dairy Sci 2020), hydrogenated oils + animal body fat (Ahmed et al., JAVAR 2020), vanaspati, palm, soybean (Kauser et al. 2022).
# - Smell + colour: flavour varies by region and feed (CFTRI, Deccan Herald); cow ghee yellow = beta-carotene, 'buffalo ghee is usually white' (Deccan Herald); FSSAI table has a coal-tar dye test for ghee (CSE newsletter Dec 2012).
# - Iodine: blue = mashed potato / sweet potato / starch (FSSAI table via CSE; Better India).
# - Acid + sugar: crimson = vanaspati/margarine, 'specific for sesame oil which is compulsorily added' (FSSAI table via CSE); 'hydrogenated vegetable oils or vanaspati having no added sesame oil ... can escape detection' (Kumar, Lal, Seth, Indian J Anim Sci 2019). Whether the sesame rule stands in 2026: unverified -> no present-tense legal claim beyond 'food rules'.
# - Fridge: teaspoon, couple of hours: pure 'uniform, grainy', palm oil 'clear separation between the liquid and solid parts' (S. Arya, ICT, Deccan Herald); 'Pure ghee will solidify evenly. If it forms layers...may be mixed with other fats' (Indian Express via FSSAI Media Compendium, 5 Jul 2025).
# - Grain varies: ten commercial ghees 1-40 % grain at 29 C for 24 h (Rachana et al., Int J Dairy Technol 2013); fast cooling = smooth (Milkio, Two Brothers: vendor pages, 2 of them).
# - Butyric: C4:0 2.43 % in ghee, 0.00 in palm oil; fatty acid analysis detects palm oil 'to the tune of 5 %'; 'in such a way that cannot be detected by simple fat constant analysis' (Hazra et al. 2020).
# - Buy: seal, maker, FSSAI licence, avoid unsealed tins, report via Food Safety Connect (Karmactive); licence + trusted sources, ad without licence details was the trigger (FoodTechNetwork 20 Jun 2026, FSSAI raid 17 Jun: lab found vegetable oils).
LINES = [
    ("i1", "Do you know the palm test for ghee can't catch palm oil?", 1.00, 0.25, +1.0, 1.45, ["palm", "oil?"], "q"),
    ("i2", "You've seen it. A little on your hand, it melts, it slides, everybody nods. Pure.", 1.06, 0.3, +0.4, 1.45, ["slides,", "Pure.:dn"], "low"),
    ("i3", "So let's put these home tests on trial. Only one's worth your time.", 1.05, 0.45, +0.4, 1.45, ["trial.", "one's"], "low"),
    ("a1", "First, the real thing. Ghee is butter, cooked until the water's gone.", 1.06, 0.25, +0.8, 1.45, ["butter,"], "low"),
    ("a2", "The fake's built from cheaper fats, like palm oil and vanuspatee.", 1.06, 0.1, +0.4, 1.45, ["cheaper"], "low"),
    ("a3", "Last month in Joonagurh, police say they found soybean oil and bottles of essence, in tins sold as pure cow ghee.", 1.09, 0.45, -0.3, 1.35, ["essence,", "pure"], "low"),
    ("b1", "Test one, water. If it floats, it's pure.", 1.05, 0.25, +0.8, 1.45, ["water.", "floats,"], "low"),
    ("b2", "Sure, and so does every oil in your kitchen.", 1.0, 0.4, -0.3, 1.4, ["every", "kitchen.:dn"], "low"),
    ("c1", "Test two, your palm. Your hand's warm, so ghee melts.", 1.05, 0.2, +0.8, 1.45, ["palm."], "low"),
    ("c2", "But palm olein, the runny part of palm oil, melts at about twenty six degrees. So it slides too.", 1.08, 0.3, +0.4, 1.45, ["twenty", "too.:dn"], "low"),
    ("c3", "And one guide says pure ghee slides, another says it stays grainy. Which is it?", 1.05, 0.45, -0.3, 1.45, ["slides,", "grainy."], "q"),
    ("d1", "Test three, smell. It's nutty, so it's real?", 1.02, 0.2, +0.8, 1.45, ["smell.", "real?"], "q"),
    ("d2", "Nice. Remember those bottles of essence?", 1.03, 0.4, -0.3, 1.4, ["essence?:dn"], "low"),
    ("e1", "Test four, colour. Yellow's good, white's bad?", 1.02, 0.2, +0.8, 1.45, ["colour."], "q"),
    ("e2", "Buffalo ghee is naturally white, and yellow can come out of a bottle.", 1.07, 0.45, +0.4, 1.4, ["white,", "bottle.:dn"], "low"),
    ("f1", "Four tests, no winners. Bring in the chemistry.", 1.03, 0.25, +1.0, 1.45, ["no", "chemistry.:dn"], "low"),
    ("f2", "Iodine's the guard from my puneer video, with one photo. He only knows starch.", 1.07, 0.3, +0.4, 1.45, ["one", "starch.:dn"], "low"),
    ("f3", "The acid test's on the official list. It turns crimson if there's vanuspatee.", 1.07, 0.1, +0.4, 1.45, ["crimson"], "low"),
    ("f4", "Clever, but it's really spotting sesame oil, which food rules add to vanuspatee as a tag. No tag, and it can slip through.", 1.09, 0.3, +0.4, 1.45, ["sesame", "through.:dn"], "low"),
    ("f5", "And that's strong acid, so please, not in your kitchen.", 1.04, 0.45, -0.3, 1.35, ["strong", "kitchen.:dn"], "low"),
    ("g1", "Which leaves the fridge. And this is the one.", 1.02, 0.25, +1.0, 1.5, ["fridge.", "one.:dn"], "low"),
    ("g2", "A teaspoon, a couple of hours. Pure ghee sets evenly, into little grains all through.", 1.06, 0.1, +0.4, 1.45, ["evenly,"], "low"),
    ("g3", "Mix in palm oil, and the solid and the liquid split apart.", 1.05, 0.35, +0.4, 1.45, ["split"], "low"),
    ("g4", "It's a clue, not a verdict. Ghee that's cooled fast can come out smooth.", 1.05, 0.25, +0.4, 1.4, ["clue,", "smooth.:dn"], "low"),
    ("g5", "So layers, be suspicious. No layers? Still not proof.", 1.04, 0.45, -0.3, 1.4, ["suspicious.", "proof.:dn"], "low"),
    ("h1", "Why so hard? Some sellers blend it so even simple lab numbers miss it.", 1.07, 0.25, +0.8, 1.45, ["hard?", "lab"], "low"),
    ("h2", "But milk fat has a tiny fat palm oil doesn't, called butyric acid. About two and a half per cent in ghee, zero in palm oil.", 1.09, 0.1, +0.4, 1.45, ["tiny", "zero"], "low"),
    ("h3", "A lab can count it, and catch palm oil down to about five per cent. Your hand can't count.", 1.06, 0.45, +0.4, 1.4, ["count", "can't"], "low"),
    ("k1", "So before Diwali, check the tin, not your hand.", 1.02, 0.25, +1.0, 1.5, ["tin,", "hand.:dn"], "low"),
    ("k2", "Look for the licence number, the maker, a batch number and an expiry date. Those Joonagurh tins had no batch number and no expiry.", 1.09, 0.25, +0.4, 1.45, ["licence", "no"], "low"),
    ("k3", "And a seal isn't proof. That raid found sealing machines.", 1.04, 0.25, -0.3, 1.4, ["seal", "machines.:dn"], "low"),
    ("k4", "Buy from a shop you trust, and if the price looks too good, ask why.", 1.05, 0.45, +0.4, 1.4, ["trust,", "why.:dn"], "low"),
    ("l1", "So remember. Fridge for a clue, lab for the truth, label before you pay.", 1.0, 0.35, +0.8, 1.45, ["clue,", "truth,", "pay.:dn"], "low"),
    ("l2", "Send this to whoever's rubbing ghee on their hand right now.", 1.03, 0.0, +0.8, 1.45, ["hand"], "low"),
]
