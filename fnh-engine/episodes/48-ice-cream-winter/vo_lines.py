# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# FreshNestHub 48 — "Does eating ice cream in winter give you a cold?" (PART 2 of ep 44; 35-50 s rule; ONE takeaway: a cold comes from a virus
# passed between people, not from cold food; and if your throat is already sore, cold ice cream can even soothe it).
# PLACE + STORY: a WINTER WEDDING dessert counter at night (wedding season: ice cream with gulab jamun at every shaadi; the relatives say no).
# Facts (verified 17 Nov 2026):
# - Mayo Clinic News Network, 'Mayo Clinic Q and A: Myths about catching a cold' (10 Feb 2022, Dr Carmen Dargel, Family Medicine):
#   'Colds are caused by viruses'; transmitted 'when people who are sick sneeze, cough or blow their nose'; 'Cold ice cream can soothe a sore throat.'
# - NHS 111 Wales 'Sore throat' (adapted from nhs.uk, updated 3 Feb 2026): sore throats 'usually caused by viruses (like cold or flu)';
#   treat it yourself: 'suck ice cubes, ice lollies or hard sweets' (not for young children: choking). nidirect 'Sore throat' (NI gov, 2024): the same list.
# - Penn Medicine '5 Winter Health Myths' (Dec 2016): 'Dress warmly or you'll get a cold' = fiction; 'It's germs that create illness, not cold weather per se';
#   'we tend to catch more illnesses in the winter because we spend so much time inside with other people.'
# - India TV News (Feb 2026; Dr Suchismitha Rajamanya, Aster Whitefield Hospital): 'Ice cream will not give you a cold. Viruses cause colds, not cold food,
#   cold water or the weather.'; winter crowding 'make[s] it easier for viruses to spread'.
# - VICE (2017; Dr Andi Khomeini Takdir Haruni, Indonesian Doctors Association): 'no direct correlation between consuming ice, or cold drinks, and coughing, colds, or the flu'.
LINES = [
    ("i1", "Do you know if eating ice cream in winter can really give you a cold?", 0.97, 0.25, +1.0, 1.55, ["ice", "cold?"], "q"),
    ("i2", "Ask anyone at home, and it's a big no. Ask a doctor, and it's... fine.", 1.0, 0.3, +0.8, 1.55, ["no.", "fine."], "low"),
    ("a1", "A cold comes from a virus, and there's no virus in your ice cream. It's just cold.", 1.0, 0.3, +1.2, 1.6, ["virus,", "just:dn"], "low"),
    ("a2", "You catch that virus from other people, from a sneeze, a cough, or a germy hand.", 1.03, 0.25, +0.4, 1.45, ["people,"], "low"),
    ("a3", "And winter packs us all indoors, so it hops from person to person.", 1.02, 0.3, +0.8, 1.5, ["indoors,", "hops"], "low"),
    ("b1", "But wait, the cold part might even help you.", 0.98, 0.25, +0.8, 1.5, ["help"], "low"),
    ("b2", "Got a sore throat? Mayo Clinic doctors say cold ice cream can actually soothe it.", 1.0, 0.25, +1.0, 1.55, ["soothe"], "low"),
    ("b3", "The NHS even lists ice lollies for a sore throat.", 1.0, 0.3, +0.4, 1.5, ["lollies"], "low"),
    ("c1", "So enjoy the scoop, and wash your hands instead.", 1.0, 0.3, +0.4, 1.5, ["hands"], "low"),
    ("c2", "Send this to whoever says no ice cream at every winter wedding.", 1.02, 0.0, +0.8, 1.45, ["wedding."], "low"),
]
