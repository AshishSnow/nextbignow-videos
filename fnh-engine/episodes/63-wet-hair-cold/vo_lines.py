# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# FreshNestHub 63 — "Can going out with wet hair give you a cold?" (35-50 s rule; ONE takeaway: a cold needs a VIRUS, wet hair has none;
# the honest twist: getting chilled (Cardiff 2005: FEET in ice water, not hair) may help a virus you ALREADY carry take hold).
# Elder-said winter myth (mom at the door with a towel) -> 'No.' at ~6 %, 'half right' at ~30 %, the Cardiff test, the nose vessels, the recap,
# a hand-washing tip, send line = the mom who yells 'dry your hair first'.
# VOICE upgrade (ep 63): CONTRAST AS A MINI QUESTION inside the number line ('With dry feet? Just nine.') vs the flat 'compared to just nine percent
# with dry feet' (A/B on identical other lines).
# Facts (verified 26 Nov 2026):
# - Mayo Clinic News Network 'Can wet hair make you sick?' (2022): 'Sorry, mom, but the short answer is no.' 'it will not give you a cold.'
#   'Viruses transmitted through bodily fluids cause colds'; tips: clean your hands often with soap and water.
# - Cleveland Clinic (Dr M. Goldman, 2021): 'Hair being wet is not the cause for catching a cold.' 'A microorganism, such as a virus, has to be involved.'
# - University Hospitals (Dr B. Behm, 2021): 'colds are caused by viruses, most commonly by rhinoviruses'; 'If the cold virus is already in your body,
#   however, being chilled can cause the onset of symptoms.'; 'wash your hands often'.
# - Cardiff University press release 13 Nov 2005 (Johnson & Eccles, Family Practice 2005; PubMed 16286463): 180 volunteers, half with feet in ice-cold
#   water for 20 minutes; '29% of the chilled volunteers developed cold symptoms over the next 4-5 days compared to only 9% in the control group';
#   chilling 'causes a pronounced constriction of the blood vessels in the nose and shuts off the warm blood that supplies the white cells that fight
#   infection'; 'the dormant infection has taken hold'.
LINES = [
    ("i1", "Do you know if going out with wet hair can give you a cold?", 0.97, 0.1, +1.0, 1.55, ["wet"], "q"),
    ("i2", "Short answer? No. A cold needs a virus, and wet hair doesn't come with one.", 1.0, 0.3, +1.2, 1.6, ["No.", "virus,"], "low"),
    ("a1", "Colds come from other people, through sneezes, coughs, and hands that touch your nose.", 1.03, 0.3, +0.4, 1.5, ["people,"], "low"),
    ("a2", "But wait, your mom might still be half right.", 1.0, 0.3, +1.0, 1.6, ["half"], "low"),
    ("a3", "In two thousand five, scientists put people's feet in ice water for twenty minutes.", 1.03, 0.25, +0.6, 1.5, ["ice"], "low"),
    ("a4", "Over the next few days, twenty-nine percent got cold symptoms. With dry feet? Just nine.", 1.02, 0.3, +0.8, 1.6, ["twenty-nine", "nine.:dn"], "low"),
    ("a5", "Chilling squeezes the blood vessels in your nose, so fewer germ fighters get there, and a virus you already have gets a head start.", 1.05, 0.3, +0.4, 1.5, ["squeezes", "head"], "low"),
    ("c1", "So wet hair can't give you a cold. Chilling might just help one you already caught.", 1.02, 0.3, -0.2, 1.4, ["can't", "already"], "low"),
    ("c2", "Wash your hands, and send this to the mom who yells, dry your hair first!", 1.06, 0.0, +0.8, 1.45, ["first!"], "low"),
]
