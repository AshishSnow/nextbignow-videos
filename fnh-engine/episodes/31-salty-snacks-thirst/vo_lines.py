# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# FreshNestHub 31 — "Why do salty snacks make you thirsty?" Facts (verified 10 Nov 2026):
# - Salt is absorbed through the small-intestine wall into the blood, 'making your blood saltier than it was before'; the extra salt outside 'acts like a magnet,
#   pulling water out of the cells'; sensors in the brain's thirst centre 'keep tabs on the saltiness of the blood'; kidneys slow urine and conserve water
#   (Indiana Public Media, A Moment of Science, 16 Sep 2019). Sodium levels in blood rise, water is pulled out of cells, the brain says drink; water moves back into cells
#   (Deccan Herald, 11 Sep 2025).
# - Brain: the OVLT and the subfornical organ 'don't measure water levels but rather the concentration of salt'; 'a change of between 1% and 3% in the blood's water content'
#   is enough to start thirst; the hypothalamus releases vasopressin, 'which tells the kidneys to retain water rather than let it out as urine'; cells 'can swell or shrink';
#   'It takes 30 to 60 minutes for water to enter the bloodstream'; mouth/throat + gut signals 'within a minute' block the thirst neurons (Quanta Magazine, 11 Aug 2025).
# - Sea water: activates the same mouth/throat receptors as ice water but doesn't quench thirst; the gut measures the salt concentration and relays it to the brain;
#   thirst neurons 'go quiet as soon as the thirsty animals took a drink, but then quickly switched back on' with salty water (NHLBI, 30 Mar 2019, Nature 2019).
# - Mice: SFO neurons fire on salt; 'eating, when we drink the most water, triggered the neurons to fire'; they decline 'the second the mice started lapping up water'
#   (STAT, 3 Aug 2016, Zachary Knight / UCSF, Nature 2016).
# - Mars simulation (Rakova et al. + Kitada et al., J Clin Invest 2017; MDC release via EurekAlert + ScienceDaily, 17 Apr 2017): two groups of 10 men in a mock spaceship,
#   105 and 205 days, identical diets except 3 salt levels over weeks; 'a salty diet caused the subjects to drink less'; kidneys conserve water; urea builds up in the kidney
#   and counteracts the water-drawing force of sodium; 'synthesizing urea takes a lot of energy'; 'Higher salt didn't increase their thirst, but it did make them hungrier.'
LINES = [
    ("i1", "Do you know why a bowl of salty chips makes you so thirsty?", 1.0, 0.25, +1.0, 1.5, ["salty", "thirsty?"], "q"),
    ("i2", "And why, in one long space study, eating more salt made people drink less?", 1.02, 0.3, +0.8, 1.5, ["space", "less?"], "q"),
    ("i3", "Less! I know, it sounds backwards.", 0.97, 0.4, -0.6, 1.4, ["backwards.:dn"], "low"),
    ("a0", "Start with the chips. The salt doesn't just sit on your tongue.", 1.03, 0.25, +0.8, 1.45, ["tongue.:dn"], "low"),
    ("a1", "It soaks through your gut wall into your blood, so now your blood is a little saltier than it was.", 1.06, 0.25, +0.4, 1.45, ["blood,", "saltier"], "low"),
    ("a2", "Salt pulls on water like a magnet, so water slides out of your cells to dilute it, and the cells shrink a little.", 1.05, 0.3, +0.4, 1.45, ["magnet,", "shrink"], "low"),
    ("a3", "Your cells don't like that, and something notices. Not your tongue, by the way. Your brain.", 1.02, 0.35, +0.8, 1.5, ["notices.", "brain.:dn"], "low"),
    ("b1", "Deep inside it, there's a tiny spot that checks your blood all day. It doesn't measure water, it measures salt.", 1.07, 0.25, +0.4, 1.45, ["water,", "salt."], "low"),
    ("b2", "It's got a mouthful of a name, the subfornical organ, but think of it as your salt checker.", 1.04, 0.3, +0.4, 1.45, ["checker.:dn"], "low"),
    ("b3", "If your blood's water shifts by just one to three percent, it sounds the alarm.", 1.03, 0.3, +0.8, 1.5, ["three", "alarm."], "low"),
    ("b4", "Two things happen at once. A hormone called vasopressin tells your kidneys, keep the water, don't send it out.", 1.05, 0.25, +0.4, 1.45, ["kidneys,", "keep"], "low"),
    ("b5", "And you get that dry, I need a glass right now feeling. That's thirst.", 1.0, 0.45, +1.0, 1.55, ["now", "thirst.:dn"], "low"),
    ("c0", "So you grab a glass, you drink, and you feel better almost straight away.", 1.02, 0.25, +0.8, 1.45, ["better"], "low"),
    ("c1", "But water takes thirty to sixty minutes to actually reach your blood. So how does your brain know when to stop?", 1.04, 0.3, +1.0, 1.5, ["sixty", "stop?"], "q"),
    ("c2", "It takes a shortcut. Your mouth and throat feel the gulps, your gut checks the salt, and within a minute, thirst switches off.", 1.07, 0.3, +0.4, 1.45, ["shortcut.", "minute"], "low"),
    ("c3", "That's why sea water never works. Your mouth says ahh, your gut tastes the salt, and the thirst comes right back.", 1.05, 0.4, +0.8, 1.5, ["never", "back.:dn"], "low"),
    ("c4", "And in mice, these thirst cells fire while they're still eating, before the blood even changes. The brain sees the salt coming.", 1.06, 0.45, +0.4, 1.45, ["eating,", "coming.:dn"], "low"),
    ("d0", "Okay, so let's go back to that space study.", 1.0, 0.25, +1.0, 1.55, ["space"], "low"),
    ("d1", "Two crews of ten men lived sealed inside a pretend spaceship, on a fake trip to Mars, for up to two hundred and five days.", 1.07, 0.25, +0.4, 1.45, ["Mars,", "two"], "low"),
    ("d2", "Same food every day, only the salt went up and down, a few weeks at a time.", 1.04, 0.3, +0.4, 1.45, ["salt"], "low"),
    ("d3", "And when the salt went up, they didn't drink more. They drank less.", 1.0, 0.4, +1.2, 1.6, ["more.", "less.:dn"], "low"),
    ("d4", "Their kidneys held on to water instead, helped by a waste product called urea, which pulls water back into the body.", 1.06, 0.25, +0.4, 1.45, ["urea", "back"], "low"),
    ("d5", "Making all that urea takes energy. And the crew on the salty food kept saying they were hungry.", 1.03, 0.45, +0.8, 1.5, ["energy.", "hungry.:dn"], "low"),
    ("e0", "So the thirst after chips is real, but it's short. Over weeks, your body plays a longer game, and scientists are still working it out.", 1.04, 0.35, -0.3, 1.35, ["short.", "longer"], "low"),
    ("e1", "Salt into your blood, water out of your cells, your salt checker sounds the alarm, you drink, and your mouth and gut switch it off.", 1.05, 0.35, +0.4, 1.45, ["alarm,", "off.:dn"], "low"),
    ("e2", "Thirsty after a salty snack? Plain water is the fix. Another handful of chips is not.", 1.02, 0.3, +0.8, 1.5, ["water", "not.:dn"], "low"),
    ("e3", "Send this to the friend who finishes the whole packet of chips, then the whole bottle of water.", 1.03, 0.0, +0.8, 1.45, ["whole", "water.:dn"], "low"),
]
