# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# FreshNestHub 38 — "Why does your mouth water when you just look at food?" (35-50 s rule; ONE takeaway: your brain gets digestion started
# before the first bite — the spit it sends carries an enzyme that turns starch into sugar, and your stomach starts on acid too)
# METAPHOR for the whole video: a RESTAURANT KITCHEN. Your brain = the head chef who hears 'ORDER!' the moment you see / smell / think of food;
# the spit glands = taps that open; amylase = the prep cook with scissors cutting starch chains into sugar; the stomach = the stove that lights early.
# Facts (verified 15 Nov 2026):
# - Cleveland Clinic 'Saliva' (health library): 'Just thinking about food can make you salivate, especially foods that you think of as particularly
#   delicious.'; 'Your autonomic nervous system (ANS) mainly controls salivation.'; 'about 0.5 to 1.5 liters (2 to 6.3 cups) of saliva a day in most
#   adults'; 'Saliva contains an enzyme called amylase'; more saliva for sour foods; '99% water'.
# - Live Science 'Why do our mouths water?': up to 1.5 quarts a day; 'salivary amylase, breaks down starches'.
# - StatPearls (NCBI NBK557738, Apr 2026) 'Amylase': salivary glands 'initiating starch hydrolysis during mastication'; products 'maltose and residual
#   glucose' / 'simpler sugars'.
# - Aji, Warren & Roura, Chemical Senses 2019 (PubMed abstract): chewing starch 'produced an oral concentration of maltose above the sweet taste
#   threshold'; sweet taste 'after mastication as a result of the maltose generated'; varies by person (sAA activity). NSTA lesson: a cracker starts
#   to taste sweeter (classroom demo).
# - OpenStax Biology 25.4: 'The response to food begins even before food enters the mouth'; the CNS 'prepares the stomach to receive food';
#   'the stomach begins to produce hydrochloric acid'.
# - Feldman & Richardson, Gastroenterology 1986 (PubMed 3940915): 'discussing appetizing food for 30 min (without sight, smell, or taste) increased
#   acid secretion from 4 to 13 mmol/h' (= more than tripled); talking about other topics did not.
LINES = [
    ("i1", "Do you know why your mouth waters when you just look at food?", 1.0, 0.25, +1.0, 1.55, ["waters", "look"], "q"),
    ("i2", "You haven't taken a single bite. But your brain's already placed the order.", 1.0, 0.3, +0.8, 1.55, ["single", "order.:dn"], "low"),
    ("a1", "The sight, the smell, even the thought of food, and your brain tells your spit glands, open up.", 1.03, 0.25, +0.4, 1.45, ["thought", "open"], "low"),
    ("a2", "And that spit isn't just water. It carries an enzyme, amylase, that cuts starch into sugar.", 1.02, 0.3, +1.0, 1.55, ["isn't", "sugar.:dn"], "low"),
    ("a3", "Try it. Chew a plain bit of roti for a while, and it starts tasting a little sweet.", 1.0, 0.35, +0.8, 1.5, ["sweet."], "low"),
    ("b1", "Your stomach gets the memo too, and starts making acid before the food even arrives.", 1.03, 0.25, +0.4, 1.45, ["acid"], "low"),
    ("b2", "In one study, just talking about tasty food for half an hour... more than tripled it.", 1.0, 0.35, +1.2, 1.6, ["talking", "tripled"], "low"),
    ("c1", "So a watering mouth isn't greed. It's your body setting the table.", 0.98, 0.3, +0.4, 1.5, ["greed.", "table.:dn"], "low"),
    ("c2", "Send this to the friend staring into a sweet shop window right now.", 1.02, 0.0, +0.8, 1.45, ["sweet"], "low"),
]
