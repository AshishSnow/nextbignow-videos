# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# FreshNestHub 28 — "Do you need a detox after Diwali?" Facts (verified 8 Nov 2026):
# - Body already detoxes: 'Your digestive tract, liver, kidneys and skin break down toxins daily and get rid of them through your urine, stool and sweat' (Cleveland Clinic, 2024);
#   liver = 'the human body's primary filtration system, converting toxins into waste products' (Johns Hopkins Medicine); detox products 'cannot improve liver or kidney function' (Sense About Science 2009 via News-Medical).
# - 2009 Sense About Science: '15 products' (News-Medical + CTV); 'manufacturers could not provide research to prove the efficacy'; 'no one we contacted was able to ... give a comprehensive
#   definition of what they meant by detox'; one company 'defined toxins as dirt and oil, which any cleanser can remove' (CTV; brand not named on screen).
# - Liver: lipophilic (fat-soluble) drugs 'are first metabolized in the liver before excretion'; conjugation 'renders the compound ... water-soluble, allowing the compound to be easily excreted';
#   kidneys 'primarily responsible for the excretion' (StatPearls, Drug Metabolism, NCBI 2023) + Hopkins 'converting toxins into waste products'.
# - Kidneys: 'each about the size of a fist' (NIDDK; Cleveland Clinic; NKF); 'about a million filtering units called nephrons' (NIDDK) / 'more than a million' (Cleveland Clinic);
#   'about 150 quarts of blood' a day (NIDDK, = 142 L) / '200 quarts of fluid' (Cleveland Clinic, NKF, = 189 L) -> 'more than 140 litres'; urine '1 to 2 quarts' (NIDDK) / 'about 2 quarts'
#   (Cleveland Clinic, NKF) -> 'a litre or two'; fluid is 'returned to the bloodstream' (NKF).
# - Detox diets: 2015 review 'no compelling research to support the use of detox diets for weight management or eliminating toxins'; 2017 review: initial weight loss, 'tend to lead to weight
#   gain once a person resumes a normal diet' (NCCIH, 2025); Hopkins 'no clinical data'; Cleveland Clinic 'effects aren't likely to last'.
# - Risks: laxatives 'can cause diarrhea ... can lead to dehydration' (NCCIH) + Cleveland Clinic 'gastrointestinal distress'; unpasteurized juices 'can make people sick' (NCCIH) + FDA 2005 warning.
# - What helps: 'eating healthily and getting plenty of sleep is a far better investment' (Sense About Science); balanced diet of vegetables, fruit, whole grains (Cleveland Clinic);
#   alcohol: 'less is always best' (Johns Hopkins); the liver metabolises alcohol (NIAAA Alcohol Alert 35; Alcohol Research review PMC6826796).
# VOICE upgrade (ep 28): TIGHTER PAUSES (owner 7 Nov: 'tighter pauses') -> PZ A/B 1.6 vs 1.35 on identical text; no lone short payoff sentences (ep 27 lesson: 4-word payoffs scored worst),
#   every payoff folded into a full sentence.
LINES = [
    ("i1", "Do you know your body is running a detox right now, while you watch this?", 1.00, 0.3, +1.0, 1.5, ["detox", "now,"], "q"),
    ("i2", "No juice, no special tea, no seven-day plan. It just does it, for free.", 1.05, 0.25, +0.4, 1.45, ["juice,", "free.:dn"], "low"),
    ("i3", "So that green detox drink everyone's posting after Diwali? Your liver is not impressed.", 1.04, 0.45, +1.2, 1.6, ["green", "impressed.:dn"], "low"),
    ("a1", "Back in two thousand and nine, a team of scientists asked detox companies one simple question: which toxins, exactly?", 1.07, 0.3, +0.8, 1.45, ["simple", "exactly?"], "low"),
    ("a2", "They checked fifteen products, and not one company could show proof that theirs worked.", 1.06, 0.25, +0.4, 1.45, ["fifteen", "proof"], "low"),
    ("a3", "And most of them couldn't even tell you what detox actually means.", 1.04, 0.25, +0.4, 1.45, ["tell", "means.:dn"], "low"),
    ("a4", "One said the toxins were dirt and oil, which, to be fair, is exactly what soap is for.", 0.98, 0.45, -0.6, 1.4, ["dirt", "soap"], "low"),
    ("b0", "So who's really doing the cleaning?", 1.0, 0.25, +1.0, 1.5, ["really"], "q"),
    ("b1", "Two organs you've already got, and the first one is your liver. It works like a sorting factory.", 1.06, 0.3, +1.0, 1.55, ["liver.", "factory.:dn"], "low"),
    ("b2", "A lot of the stuff your body wants gone dissolves in fat, not in water, and you can't pee out fat.", 1.07, 0.25, +0.4, 1.45, ["fat,", "pee"], "low"),
    ("b3", "So the liver changes it, one step at a time, into something that dissolves in water.", 1.05, 0.1, +0.4, 1.45, ["changes", "water."], "low"),
    ("b4", "Same junk, new packaging, and now it can actually leave.", 1.0, 0.45, +1.2, 1.6, ["packaging,", "leave.:dn"], "low"),
    ("c0", "And that's where your kidneys take over.", 1.0, 0.2, +1.0, 1.55, ["kidneys"], "low"),
    ("c1", "Each one is about the size of your fist, with around a million tiny filters packed inside.", 1.06, 0.25, +0.4, 1.45, ["fist,", "million"], "low"),
    ("c2", "Every day, they filter more than a hundred and forty litres. That's about seven big water cans.", 1.05, 0.3, +0.8, 1.5, ["hundred", "seven"], "low"),
    ("c3", "And only a litre or two of it ends up as pee. The rest goes straight back into you.", 1.05, 0.3, +0.4, 1.45, ["two", "back"], "low"),
    ("c4", "So the detox is already running, all day, every day, and it doesn't need a subscription.", 1.03, 0.5, -0.6, 1.4, ["running,", "subscription.:dn"], "low"),
    ("d0", "Okay, but what about a three-day juice cleanse?", 1.0, 0.3, +1.0, 1.5, ["juice"], "q"),
    ("d1", "When researchers went through the studies, they found no good proof that detox diets clear out toxins.", 1.07, 0.25, +0.4, 1.45, ["no", "proof"], "low"),
    ("d2", "You might lose a little weight at first, but it tends to come back once you eat normally again.", 1.07, 0.3, +0.4, 1.45, ["back"], "low"),
    ("d3", "And some cleanses aren't harmless. Laxatives can leave you dehydrated.", 1.03, 0.25, -0.3, 1.35, ["harmless.", "dehydrated.:dn"], "low"),
    ("d4", "And juice that isn't pasteurized can carry germs that make you sick.", 1.04, 0.45, -0.3, 1.35, ["germs", "sick.:dn"], "low"),
    ("e0", "So after Diwali, what actually helps your liver and kidneys?", 1.0, 0.3, +1.0, 1.5, ["helps"], "q"),
    ("e1", "The boring stuff. A proper night's sleep, and normal meals with vegetables, fruit and whole grains.", 1.05, 0.25, +0.8, 1.45, ["boring", "sleep,"], "low"),
    ("e2", "And go easy on the alcohol, because your liver has to deal with every single drop.", 1.04, 0.45, -0.3, 1.35, ["easy", "every"], "low"),
    ("f1", "No detox kit needed. You've got a liver and two kidneys working the night shift, and the day shift.", 1.03, 0.3, +0.8, 1.5, ["night", "day"], "low"),
    ("f2", "Send this to whoever just sent you a detox juice recipe.", 1.03, 0.0, +0.8, 1.45, ["recipe.:dn"], "low"),
]
