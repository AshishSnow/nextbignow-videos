# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# FreshNestHub 34 — "Why does spicy food make your nose run?" (first episode under the 11 Nov rule: 35-50 s, payoff before 60 %, loop ending)
# Facts (verified 12 Nov 2026):
# - Cleveland Clinic, 'Gustatory rhinitis' (updated 16 Jan 2026): 'heat or spices activate the trigeminal nerve in the mucous membranes of your nose',
#   the nose makes mucus; capsaicin = 'a chemical that makes them taste spicy'; triggers incl. chili peppers, heated foods such as soup, curry; 'isn't an
#   allergic reaction'; comes on while eating, 'goes away quickly after you're done eating'; 'more common as you get older'; see a provider if bothersome
#   or 'happening all the time'.
# - Cleveland Clinic Health Essentials, 'Runny nose when eating' (2022): 'your nose will stop running a few minutes after you're done eating';
#   nonallergic rhinitis; 'isn't serious'.
# - UCLA Health 'Ask the Doctors' (28 Oct 2026): 'a nerve reflex', 'unlike an allergy', hot (temperature) foods trigger it too, 'not a risk to health'.
# - BBC Science Focus (L. Villazon) via HuffPost UK: capsaicin 'triggers the nerve receptors that normally detect heat, and your nose is fooled into
#   producing extra mucus'; no tissue damage.
LINES = [
    ("i1", "Do you know why your nose runs when you eat spicy food?", 1.0, 0.25, +1.0, 1.55, ["runs", "spicy"], "q"),
    ("i2", "It's not a cold, and it's not an allergy either.", 1.02, 0.25, +0.4, 1.45, ["cold,", "allergy"], "low"),
    ("a1", "Chillies have capsaicin, the stuff that makes them taste hot.", 1.02, 0.1, +0.8, 1.5, ["capsaicin,"], "low"),
    ("a2", "And inside your nose, there's a nerve that senses heat.", 1.0, 0.25, +0.4, 1.45, ["heat.:dn"], "low"),
    ("a3", "Capsaicin trips that same nerve, so your nose thinks it's on fire.", 1.0, 0.3, +1.2, 1.6, ["same", "fire."], "low"),
    ("a4", "So it opens the taps. Mucus, coming right up.", 1.0, 0.35, +0.4, 1.45, ["taps.", "up.:dn"], "low"),
    ("b1", "There's no real fire, it's just a false alarm.", 0.98, 0.35, -0.3, 1.4, ["false"], "low"),
    ("b2", "It even has a name, gustatory rhinitis. Big name, runny nose.", 1.0, 0.3, +0.8, 1.5, ["Big", "runny"], "low"),
    ("b3", "Hot soup can set it off too.", 1.02, 0.25, +0.4, 1.45, ["soup"], "low"),
    ("b4", "It stops a few minutes after you finish eating, and if it bugs you all the time, see a doctor.", 1.04, 0.35, -0.3, 1.35, ["stops", "doctor.:dn"], "low"),
    ("c1", "Send this to the friend who needs a tissue at every chaat stall.", 1.02, 0.0, +0.8, 1.45, ["tissue"], "low"),
]
