# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# FreshNestHub 44 — "Does eating curd in winter give you a cold?" (35-50 s rule; ONE takeaway: colds come from viruses passed between people,
# not from cold food; curd is safe in winter — keep the curd, wash your hands).
# METAPHOR for the whole video: a POLICE LINEUP. Curd is the accused every winter; Detective Chubby finds the real culprit (the cold virus) by
# turning the light on a silhouette at the end of the line.
# Facts (verified 16 Nov 2026):
# - Mayo Clinic News Network, 'Mayo Clinic Minute: Can cold weather cause a cold?' (16 Jan 2024, Dr Jesse Bracamonte, family physician):
#   'the cold weather itself doesn't cause the common cold'; a virus in most cases; 'as winter temps dip down, the chances of spreading a
#   respiratory virus go up because more time is spent indoors with others'; 'more likely to be in close proximity to someone who is ill'.
# - BBC Science Focus, 'Cold weather doesn't cause colds. Here's what does' (Dr Nish Manek, GP, Dec 2024): 'the common cold is caused by viruses,
#   such as rhinoviruses, not exposure to chilly conditions'; 'people tend to spend more time indoors creating an environment where viruses can be
#   easily passed on'; dry air may make airways more susceptible.
# - The Week, 'FACT CHECK: Can you fall ill if you have curd during the winter?' (29 Jan 2026; Dr Amit Gupta, Motherhood Hospitals): 'Colds and coughs
#   are not caused by food; they are caused by viruses.'; claim rated: 'Consuming curd in winter does not cause colds or coughs and is safe to eat
#   during colder months.'; 'Curd is a very good probiotic'.
# - The South First, 'Don't eat curd when you have cold — is there any truth to this?' (13 Dec 2023; Dr Gopikrishna G, Sevakshetra Hospital; Dr Sonali
#   Vaid): 'no evidence to suggest that eating curd worsens cold symptoms'; 'Probiotics in yoghurt help maintain a healthy balance of gut flora';
#   'eating curd straight out of the refrigerator may not be a good idea' (-> the one safe tip: let fridge-cold curd sit out a bit).
# - CDC 'About Common Cold' + 'About Rhinoviruses' (Feb 2026): rhinoviruses 'are the most frequent cause of colds'; spread through droplets 'when they cough
#   or sneeze' and 'shaking hands with an infected person and then touching your eyes, nose, or mouth'; CDC respiratory-virus prevention: 'washing your hands regularly'.
# Shipped take = SPD 0.893 (voice.env SPD 0.88 overridden for this episode's take).
LINES = [
    ("i1", "Do you know if eating curd in winter can really give you a cold?", 0.97, 0.25, +1.0, 1.55, ["curd", "cold?"], "q"),
    ("i2", "Every winter, curd gets the blame. But it's the wrong suspect.", 1.0, 0.3, +0.8, 1.55, ["blame.", "wrong"], "low"),
    ("a1", "Colds are caused by viruses, mostly one called rhinovirus, not by cold food.", 1.0, 0.3, +1.2, 1.6, ["viruses,", "food.:dn"], "low"),
    ("a2", "You catch it from other people, from a sneeze, a cough, a hand you just shook.", 1.03, 0.25, +0.4, 1.45, ["people,"], "low"),
    ("a3", "And in winter, we all pack indoors with the windows shut, sharing the same air.", 1.02, 0.3, +0.8, 1.5, ["indoors", "same"], "low"),
    ("b1", "So the curd's innocent. Doctors say it's safe in winter, and its friendly bacteria are good for your gut.", 1.03, 0.25, +1.0, 1.55, ["innocent.", "safe"], "low"),
    ("b2", "If fridge-cold curd bothers your throat, just let it sit out for a bit.", 0.98, 0.3, -0.3, 1.35, ["sit"], "low"),
    ("c1", "So keep eating your curd, and just wash your hands more often.", 1.0, 0.3, +0.4, 1.5, ["hands"], "low"),
    ("c2", "Send this to whoever keeps taking the curd off your plate every winter.", 1.02, 0.0, +0.8, 1.45, ["taking"], "low"),
]
