# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# "One company behind your glasses, the shop and your eye insurance" (type C, hidden giant) — roadmap: four doors, the 4th is the sneakiest.
# Sources (verified 28 Oct 2026):
#   FY2025 revenue EUR 28,491m, 17,750 stores at 31 Dec 2025: EssilorLuxottica FY2025 press release (Feb 2026), Modaes / FashionUnited (Feb 2026)
#   19,709 stores at 30 Sep 2026 (15,695 corporate + 4,014 franchise/licence); retail banners Sunglass Hut, LensCrafters, Target Optical;
#     lens brands Varilux, Transitions; Ray-Ban, Oakley; Ray-Ban Meta: EssilorLuxottica Q3 2026 revenue release (21 Oct 2026), FashionUnited 21 Oct 2026
#   House brands Ray-Ban, Oakley, Persol, Oliver Peoples: EssilorLuxottica brand pages / Wikipedia (Luxottica)
#   Licences: Chanel, Prada, Miu Miu (EssilorLuxottica releases 2026); Prada 10-yr renewal (AOP Jan 2025, FashionUnited Dec 2024);
#     Armani 15-yr renewal (FashionUnited Sep 2022); Michael Kors renewal (FashionUnited Feb 2024); Versace renewal (WWD)
#   Essilor + Luxottica combined as EssilorLuxottica on 1 Oct 2018 (EU approval Mar 2018): Wikipedia (Luxottica), company history
#   Oakley: Luxottica bought Sunglass Hut in Apr 2001; told Oakley in early Aug 2001 that Sunglass Hut would order only about one-sixth of what
#     Oakley expected; Sunglass Hut = 19% of Oakley sales; shares -35% on 2 Aug 2001 (Forbes 3 Aug 2001 'Oakley Sees Red'; FundingUniverse;
#     OCBJ 20 Jun 2007: cut, Oakley sued, settled late 2001); Luxottica bought Oakley for $2.1bn, announced Jun 2007, closed Nov 2007 (OCBJ, mr-mag, Wikipedia)
#   EyeMed (US vision benefits) parent = EssilorLuxottica, 68M+ members (EyeMed, Oct 2022); Luxottica owns EyeMed (Wikipedia, Luxottica)
#   Meta bought nearly 3% of EssilorLuxottica (~EUR 3bn), Jul 2025: Reuters via TechCentral 10 Jul 2025, Benzinga / Luxury Tribune
#   FTC Eyeglass Rule: prescriber must give you a copy of your prescription immediately after the exam, at no extra charge (FTC consumer alert, Jun 2024)
LINES = [
    ("i1", "How can your sunglasses, the shop, and your eye insurance all be one company?", 1.04, 0.40, +1.0, 1.45, ["sunglasses,", "one"], None),
    ("i2", "It's one giant eyewear company. And most people have never even heard its name.", 1.04, 0.35, +0.6, 1.45, ["giant", "never"], "low"),
    ("i3", "It owns four doors to your eyes. And the fourth door is the sneakiest one of all.", 1.04, 0.45, +0.8, 1.3, ["four", "sneakiest"], "low"),
    ("a1", "Door one. The frame on your face.", 1.02, 0.30, +1.0, 1.45, ["one.", "frame"], "low"),
    ("a2", "Ray-Ban. Oakley. Persol. Oliver Peoples. All owned by this one company.", 1.04, 0.30, +0.8, 1.45, ["Ray-Ban.", "one"], "low"),
    ("a3", "And the designer glasses? Chanel, Prada, Armani, Versace, Michael Kors.", 1.04, 0.25, +0.8, 1.45, ["designer", "Chanel,"], None),
    ("a4", "It makes those frames too, under licence from the fashion houses.", 1.04, 0.35, +0.6, 1.45, ["those", "licence"], "low"),
    ("a5", "So that wall of rival brands in the store? Many of them lead back to one place.", 1.04, 0.40, +0.6, 1.5, ["rival", "one"], "low"),
    ("b1", "Door two. The lens you look through.", 1.02, 0.30, +1.0, 1.45, ["two.", "lens"], "low"),
    ("b2", "In twenty eighteen, the frame giant joined forces with a lens giant, the company behind Transitions lenses.", 1.04, 0.25, +0.8, 1.45, ["lens", "giant"], None),
    ("b3", "So now the frame and the lens inside it can come from the very same company.", 1.04, 0.40, +0.6, 1.45, ["frame", "same"], "low"),
    ("c1", "Door three. The shop where you buy them.", 1.02, 0.30, +1.0, 1.45, ["three.", "shop"], "low"),
    ("c2", "The Sunglass Hut stores. Lens Crafters. Target Optical. All the same owner.", 1.04, 0.30, +0.8, 1.45, ["Sunglass", "owner.:dn"], "low"),
    ("c3", "By this September, it had almost twenty thousand stores around the world.", 1.04, 0.40, +0.6, 1.45, ["twenty", "world.:dn"], "low"),
    ("c4", "And owning the shops is real power. Just ask Oakley.", 1.02, 0.45, +0.8, 1.5, ["power.", "Oakley.:dn"], "low"),
    ("s1", "Back in two thousand one, Oakley was a rival of the frame giant, not part of the family.", 1.04, 0.25, +0.8, 1.45, ["rival,", "family."], None),
    ("s2", "That spring, the frame giant bought Sunglass Hut, one of the biggest sellers of Oakley glasses.", 1.04, 0.30, +0.8, 1.45, ["bought", "biggest"], "low"),
    ("s3", "So guess what happened next? Sunglass Hut planned to order far fewer Oakleys.", 1.04, 0.30, +0.6, 1.45, ["fewer"], "low"),
    ("s4", "In a single day, Oakley's stock fell thirty five percent.", 1.02, 0.45, +0.6, 1.5, ["single", "thirty"], "low"),
    ("s5", "Six years later, the frame giant bought Oakley. For two point one billion dollars.", 1.02, 0.55, +0.8, 1.5, ["bought", "billion"], "low"),
    ("d1", "Door four. The sneaky one. Your eye insurance.", 1.02, 0.35, +1.0, 1.5, ["four.", "insurance.:dn"], "low"),
    ("d2", "In America, a vision plan called EyeMed helps pay for glasses for tens of millions of people.", 1.04, 0.25, +0.8, 1.45, ["EyeMed", "millions"], None),
    ("d3", "And its parent company? The same one.", 1.02, 0.45, +0.8, 1.5, ["parent", "same"], "low"),
    ("d4", "And even the future runs through it. Meta makes its smart glasses with Ray-Ban, and bought about three percent of the company.", 1.04, 0.45, +0.6, 1.45, ["future", "three"], "low"),
    ("t1", "So one company can be the frame, the lens, the shop, and the plan that pays.", 1.02, 0.40, +0.8, 1.5, ["one", "pays.:dn"], "low"),
    ("e0", "Here's your move. In the US, you get a free copy of your prescription after an eye test.", 1.04, 0.30, +0.8, 1.45, ["move.", "free"], "low"),
    ("e1", "Take it anywhere and compare prices. That wall of choices might be one company.", 1.02, 0.35, +0.8, 1.45, ["choices", "one"], "low"),
    ("e2", "Send this to the friend who just paid way too much for glasses!", 1.06, 0.0, +1.0, 1.45, ["friend", "too"], None),
]
