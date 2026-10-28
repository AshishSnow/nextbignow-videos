# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# "Almost every banana you buy is the same clone" (type B, everyday object) — roadmap: three reasons, the last one already happened.
# Sources (verified 28 Oct 2026):
#   Cavendish ~47% of global banana production: FAO 'Overview of world banana production and trade' (y5102e04), FoodNavigator 9 Aug 2019,
#     Guinness World Records ('most popular banana', 47%); ~99% of bananas exported to developed countries: The Conversation (2016);
#     nearly all internationally traded bananas Cavendish: FAO (y5102e04)
#   sterile, seedless, propagated from suckers / tissue culture = genetically almost identical: The Conversation; Wikipedia Panama disease
#   TR4: soil fungus, enters through roots, blocks the vascular (water) system, no cure / no fungicide saves infected plants, persists in
#     soil for decades: FreshPlaza 12 Feb 2026, Atlas Obscura 2019 (Bioversity's Staver), FAO 3 Sep 2026 ('more than two decades'),
#     Wikipedia (chlamydospores up to 30 years)
#   Colombia ICA confirmation 8 Aug 2019 (La Guajira, national emergency): FoodNavigator, Atlas Obscura, FreshFruitPortal
#   Peru Apr 2021 (Piura, SENASA): IPPC pest report 2021/04, Agraria.pe 12 Apr 2021
#   Venezuela notified IPPC 25 Jan 2023 (Aragua, Carabobo, Cojedes): IPPC
#   Ecuador confirmed 18 Dec 2025 (El Oro), phytosanitary emergency: Vistazo, Portal Fruticola, El Diario (18 Dec 2025), FreshPlaza 12 Feb 2026;
#     second case July 2026 (adjoining farm): FreshFruitPortal 21 Jul 2026; Ecuador = world's largest banana exporter, > 1/4 of traded
#     bananas: FreshPlaza 12 Feb 2026; 377M boxes in 2025: FreshFruitPortal (ACORBANEC)
#   Gros Michel = main export banana until the 1950s; race 1 wiped out plantations in Central America in the 1950s; companies moved to
#     new land (Soluri 2005 via Wikipedia); exporters switched to resistant Cavendish (1950s-60s): Atlas Obscura, FoodNavigator,
#     The Conversation, Ploetz/APS 2005 via Wikipedia; Gros Michel still grown (Central America, Africa): Atlas Obscura
#   QCAV-4 GM Cavendish (TR4-resistant) approved by FSANZ 16 Feb 2024 + OGTR licence; no plans for large-scale growing, 'safety net':
#     AgNavigator 19 Feb 2024
LINES = [
    ("i1", "Why is almost every banana you buy a copy of the exact same plant?", 1.04, 0.40, +1.0, 1.45, ["every", "same"], None),
    ("i2", "That one fact has the whole banana business worried.", 1.04, 0.35, +0.6, 1.45, ["whole", "worried.:dn"], "low"),
    ("i3", "Three reasons why. And the third one has already happened once before.", 1.04, 0.45, +0.8, 1.45, ["Three", "already"], "low"),
    ("a1", "Reason one. Your banana has no seeds.", 1.02, 0.30, +1.0, 1.45, ["one.", "seeds.:dn"], "low"),
    ("a2", "Those tiny black dots inside will never grow a plant.", 1.04, 0.25, +0.8, 1.45, ["never"], None),
    ("a3", "So every new banana plant is grown from a piece of an old one. A clone.", 1.04, 0.40, +0.8, 1.45, ["piece", "clone.:dn"], "low"),
    ("a4", "Almost half of all the bananas grown on Earth are this one type, called Cavendish.", 1.04, 0.25, +0.8, 1.45, ["half", "one"], None),
    ("a5", "And nearly every banana shipped to a supermarket is a Cavendish too.", 1.04, 0.35, +0.8, 1.45, ["nearly", "too.:dn"], "low"),
    ("a6", "Here's the problem. Same genes everywhere. So a disease that can kill one plant can kill them all.", 1.04, 0.45, +0.6, 1.5, ["problem.", "all.:dn"], "low"),
    ("b1", "Reason two. That disease is real.", 1.02, 0.30, +1.0, 1.45, ["two.", "real.:dn"], "low"),
    ("b2", "It's a fungus in the soil, called Tropical Race Four.", 1.04, 0.25, +0.8, 1.45, ["fungus", "Four."], None),
    ("b3", "It sneaks in through the roots and blocks the plant's water pipes, until it wilts and dies.", 1.04, 0.30, +0.8, 1.45, ["roots", "dies.:dn"], "low"),
    ("b4", "There's no cure. No spray can save an infected plant.", 1.02, 0.30, +0.6, 1.5, ["no", "save"], "low"),
    ("b5", "And its spores can wait in the soil for decades.", 1.04, 0.40, +0.6, 1.45, ["wait", "decades.:dn"], "low"),
    ("b6", "Now it's moving through the countries that grow your bananas.", 1.04, 0.30, +0.8, 1.45, ["moving", "your"], None),
    ("b7", "Colombia, twenty nineteen. Peru, twenty twenty one. Venezuela, twenty twenty three.", 1.04, 0.35, +0.8, 1.4, ["Colombia,", "Peru,", "Venezuela,"], None),
    ("b8", "Last December, Ecuador. The biggest banana exporter in the world.", 1.02, 0.30, +0.8, 1.5, ["Ecuador.", "biggest"], "low"),
    ("b9", "And this July, a second farm there.", 1.04, 0.45, +0.6, 1.45, ["second", "there.:dn"], "low"),
    ("c0", "So why not just switch to a different banana? Because we already did that once.", 1.04, 0.40, +0.8, 1.45, ["switch", "once.:dn"], "low"),
    ("c1", "Reason three. It has happened before.", 1.02, 0.35, +1.0, 1.5, ["three.", "before.:dn"], "low"),
    ("c2", "Until the nineteen fifties, the banana in every shop was a different kind.", 1.04, 0.25, +0.8, 1.45, ["fifties,", "different"], None),
    ("c3", "But an older strain of the same fungus hit its farms in Central America.", 1.04, 0.25, +0.8, 1.45, ["older", "same"], None),
    ("c4", "Companies moved to fresh land. The fungus followed them.", 1.02, 0.35, +0.6, 1.5, ["fresh", "followed"], "low"),
    ("c5", "So the industry switched to a banana that fungus couldn't kill. The Cavendish.", 1.04, 0.50, +0.8, 1.45, ["couldn't", "Cavendish.:dn"], "low"),
    ("t1", "Here's the twist. To escape a disease that killed one clone, the world bet everything on another clone.", 1.02, 0.35, +0.8, 1.5, ["twist.", "another"], "low"),
    ("t2", "And the new strain kills that one too.", 1.02, 0.45, +0.6, 1.5, ["kills", "too.:dn"], "low"),
    ("e0", "Bananas won't vanish. But put everything on one bet, and one problem hits everything.", 1.04, 0.35, +0.8, 1.45, ["vanish.", "one"], "low"),
    ("e1", "Next time you peel one, remember: you're eating a copy.", 1.02, 0.35, +0.8, 1.45, ["peel", "copy.:dn"], "low"),
    ("e2", "Send this to the friend who eats a banana every single day!", 1.06, 0.0, +1.0, 1.45, ["friend", "every"], None),
]
