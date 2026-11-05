# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# FreshNestHub 24 — "Does the viral iodine test catch fake puneer?" Facts (verified 5 Nov 2026):
# - Test steps: boil a little sample in water, cool, add 2-3 drops tincture of iodine, blue = starch (FSSAI guidance via Hyderabad Mail 30 Oct 2024, Food Safety Helpline). Iodine goes brown -> blue-black/purple with starch; milk stays unchanged; do NOT eat tested food (WebExhibits Causes of Color).
# - Why blue: amylose coils into a helix, iodine 'gets stuck in the coils', forced into a line (WebExhibits; UBB 2022 on Pesek et al., Molecules 2022).
# - It 'only detects starch' (Business Today 6 Aug 2026); 'fails to detect ... vegetable oils'; positive 'doesn't automatically confirm' fake; cross-contamination from fried coatings, gravy thickeners (Daily Excelsior 18 May 2025).
# - Paneer: heat + acid coagulation of casein 'entrapping' other constituents, whey drained, pressed (A. Jana, Technology of Paneer, INFLIBNET; NIFTEM). ~52 % water, 25-27 % fat (NIFTEM table, R.P. Aneja et al.). Standard: only milk + milk solids, no vegetable oils (Civilsdaily 25 Sep 2026); moisture <= 70 %, fat >= 50 % of dry matter.
# - Analogue puneer: milk fat replaced by vegetable oils/fats, starch may be added; 'legal if sold with the right label' ('Is analogue puneer illegal? No.', Business Today 6 Aug 2026); cost 50-60 % lower, 'legal, non-toxic' if labelled, Maharashtra menu declaration, FSSAI no national ban (Telangana Today 12 Jun 2026). Loose sale carries no label; lab needed to separate fats (Civilsdaily).
# - Buffalo milk puneer 'firm and rubbery body'; coagulating hotter than 70 C = 'hard and dry' (Jana). Hot-water test: Business Today vs Onmanorama describe different outcomes.
# - 'No home test ... confirm with certainty' (Business Today); FSSAI: not conclusive (Onmanorama 4 Sep 2026). Ask: dairy or analogue (Business Today).
# - Draft: FSSAI proposed barring non-dairy analogues from the word puneer, 'a proposed draft and not a final rule', 60 days (Business Today 24 Sep 2026; Civilsdaily).
LINES = [
    ("i1", "Do you know the viral blue test for fake puneer can pass a fake?", 1.00, 0.25, +1.0, 1.45, ["pass"], "q"),
    ("i2", "You've seen the video. One drop of iodine, it turns blue, and everybody screams fake.", 1.05, 0.25, +0.4, 1.45, ["blue,", "fake.:dn"], "low"),
    ("i3", "It's a real test. It just isn't testing what you think it's testing.", 1.04, 0.4, -0.3, 1.4, ["real", "think"], "low"),
    ("a1", "Start with the real stuff. Puneer is just hot milk and something sour.", 1.04, 0.25, +0.4, 1.45, ["sour.:dn"], "low"),
    ("a2", "The sour makes the milk protein clump together, and those clumps catch the fat, like a net catching fish.", 1.07, 0.1, +0.4, 1.45, ["clump", "net"], "low"),
    ("a3", "Drain off the watery part, press it, and that's your block.", 1.06, 0.1, +0.4, 1.45, ["block.:dn"], "low"),
    ("a4", "India's food rules say it can only come from milk. No vegetable oil.", 1.04, 0.4, +0.4, 1.4, ["only", "oil.:dn"], "low"),
    ("b1", "But milk's expensive, and vegetable oil isn't.", 1.04, 0.25, -0.3, 1.4, ["expensive,"], "low"),
    ("b2", "So there's a lookalike called analogue puneer. Out goes the milk fat, in goes vegetable oil, maybe some starch, and it can cost about half.", 1.09, 0.3, +0.4, 1.45, ["analogue", "half.:dn"], "low"),
    ("b3", "And the surprise is that it's legal, as long as the label says what it is.", 1.04, 0.1, +0.8, 1.45, ["legal,", "label"], "low"),
    ("b4", "The trouble is your plate. A puneer tikka doesn't come with a label.", 1.03, 0.45, -0.3, 1.4, ["plate.", "label.:dn"], "low"),
    ("c1", "So where does the blue come from?", 1.0, 0.25, +0.8, 1.5, ["blue"], "q"),
    ("c2", "Starch has a long chain in it that coils up like a spring. Iodine gets stuck inside that coil, in a straight line.", 1.07, 0.1, +0.4, 1.45, ["spring.", "stuck"], "low"),
    ("c3", "Lined up like that, it soaks up light differently, and you see blue black.", 1.05, 0.1, +0.4, 1.45, ["blue"], "low"),
    ("c4", "Milk's got no starch, so iodine in milk just stays brown.", 1.03, 0.35, +0.4, 1.45, ["brown.:dn"], "low"),
    ("c5", "Think of iodine as a guard with one photo on the wall. Starch. Anybody else walks right in.", 1.04, 0.4, -0.3, 1.4, ["one", "Starch."], "low"),
    ("d1", "Quick guess, then. A lookalike block, made with vegetable oil and no starch. What colour does it go?", 1.04, 0.7, +0.6, 1.45, ["guess,", "colour"], "q"),
    ("d2", "Brown. It passes.", 1.0, 0.3, -0.3, 1.35, ["passes.:dn"], "low"),
    ("d3", "The oil's invisible to the guard, and so is anything else that isn't starch.", 1.05, 0.3, +0.4, 1.45, ["invisible"], "low"),
    ("d4", "It can go wrong the other way too. Real puneer that's touched a fried coating or a thick gravy can pick up starch, and turn blue.", 1.08, 0.35, +0.4, 1.45, ["other", "blue.:dn"], "low"),
    ("d5", "So it's not a fake detector. It's a starch detector.", 1.0, 0.45, +0.8, 1.5, ["fake", "starch"], "low"),
    ("e1", "What about the other tricks, like if it's rubbery, it's fake?", 1.03, 0.2, +0.8, 1.5, ["rubbery,"], "q"),
    ("e2", "Puneer from buffalo milk is naturally firm and rubbery.", 1.08, 0.3, +0.4, 1.45, ["buffalo", "rubbery,"], "low"),
    ("e4", "There's no home test that can settle it. Telling one fat from another takes a lab.", 1.05, 0.45, -0.3, 1.4, ["no", "lab.:dn"], "low"),
    ("f1", "So what can you do before Diwali dinner? Three easy things.", 1.03, 0.25, +0.8, 1.5, ["Three"], "low"),
    ("f2", "On a packet, read the label. If it says analogue, it isn't milk puneer.", 1.05, 0.25, +0.4, 1.45, ["label.", "analogue,"], "low"),
    ("f3", "Eating out, just ask. Dairy or analogue? Maharashtra already makes restaurants say so on the menu.", 1.06, 0.25, +0.4, 1.45, ["ask.", "menu.:dn"], "low"),
    ("f4", "And if the price looks too good, ask why.", 1.02, 0.35, -0.3, 1.4, ["why.:dn"], "low"),
    ("f5", "Still want to try the drop? Boil a little in water, cool it, and add a few drops. Just don't eat that piece. Iodine isn't food.", 1.07, 0.4, +0.4, 1.4, ["cool", "food.:dn"], "low"),
    ("f6", "In September, the regulator proposed taking the word puneer off these lookalikes. It's still only a draft.", 1.07, 0.45, +0.4, 1.45, ["word", "draft.:dn"], "low"),
    ("g1", "So remember. Blue means starch. And no blue doesn't mean real.", 1.0, 0.3, +0.6, 1.45, ["starch.", "real.:dn"], "low"),
    ("g2", "Now send this to the friend who sent you that video.", 1.03, 0.0, +0.8, 1.45, ["friend"], "low"),
]
