# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# FreshNestHub 23 — "Which Diwali sweet goes bad first?" Facts (verified 4 Nov 2026):
# - THE LIST: FSSAI Guidance Note 14/2020 'Safety and Quality of Traditional Milk Products' (illustrative, 'does not have any force of law'): kalakand room temp, same day; rasgulla, ras malai, sandesh etc: fridge, within 2 days;
#   milk burfi, peda, boondi ladoo etc: within 4 days; kaju katli, besan burfi etc: within 7 days; besan laddoo, chana laddoo, gajjak, chikki etc: within 30 days. Business Today 28 Sep 2020 restates the groups.
# - 'Sweets particularly those with milk products have lesser shelf life (1-4 days) and are more prone to microbial growth' (FSSAI). Khoa: 'favorable medium ... high moisture content and high nutritive value' (Kumar, BVC Patna slides).
# - Moisture: rasgulla 48-54 % (J Ethnic Foods 2021 table), kalakand 26.5 % (Thikare 2020, plain khoa control), burfi 14.67 % + aw 0.79 (Badola 2018, J Food Sci Technol). Besan laddoo: no measured number found -> ingredients only.
# - aw needs: 'Bacteria usually require at least 0.91, and fungi at least 0.7' (Shrivas 2018, J Appl Nat Sci). Burfi: 'surface mould growth is the most common defect' (Badola 2018).
# - No scraping: USDA FSIS Molds on Food: 'you only see part of the mold', roots 'may be very deep', 'invisible bacteria growing along with the mold'; soft / porous foods discard. Sweets aren't named in the chart -> we say 'on soft food'.
# - Fridge: rava burfi in pouches: 9 days at 30 C (visible mould), 35 days at 7 C (ended by texture: dry, hard, sandy), moisture 19.3 -> 16.2 % (Shrivas 2018). Airtight: Kumar slides.
# - Best before on the tray of loose sweets, from 1 Oct 2020; date of manufacture voluntary; depends on local weather (Deccan Herald, Business Today, FSSAI).
# VOICE upgrade (ep 23): LIST RHYTHM: fragments of the same list run linked with a stepping-down base, plus a 3-take line-by-line comp.
LINES = [
    ("i1", "Do you know which sweet in your Diwali box goes bad first?", 1.00, 0.28, +1.0, 1.45, ["first?"], "q"),
    ("i2", "Because one of them's done by tonight, and the one sitting right next to it has got a month.", 1.05, 0.1, +0.4, 1.45, ["tonight,", "month.:dn"], "low"),
    ("i3", "Every sweet in there is like a cracker with its own fuse, and they're all already lit.", 1.04, 0.4, -0.3, 1.4, ["fuse,", "lit.:dn"], "low"),
    ("a1", "I'm not making this up. India's food regulator actually has a list.", 1.05, 0.3, +0.4, 1.45, ["list.:dn"], "low"),
    ("a2", "The shortest fuse is kalaakund. You're meant to eat it the same day.", 1.03, 0.25, +0.6, 1.45, ["kalaakund.", "same"], "low"),
    ("a3", "Rusgoola, rusmalaai, sundaysh, those get two days, and only in the fridge.", 1.03, 0.1, +0.4, 1.45, ["two", "fridge.:dn"], "low"),
    ("a4", "Milk burfee, payda, boondee luddoo, about four days.", 1.02, 0.1, +0.2, 1.45, ["four"], "low"),
    ("a5", "Kaaju kutlee gets a week.", 1.0, 0.1, 0.0, 1.45, ["week.:dn"], "low"),
    ("a6", "And baysun luddoo gets a whole month, in the same box.", 1.0, 0.45, +0.8, 1.5, ["month,"], "low"),
    ("b1", "So how does a luddoo outlive a rusgoola by a month?", 1.0, 0.25, +0.8, 1.5, ["month?"], "q"),
    ("b2", "Mostly, it's water. A rusgoola is about half water, kalaakund about a quarter, and milk burfee around fifteen percent.", 1.08, 0.1, +0.4, 1.45, ["water.", "half"], "low"),
    ("b3", "Baysun luddoo is roasted flour, ghee and sugar. No milk, and hardly any water to begin with.", 1.08, 0.3, +0.4, 1.45, ["hardly"], "low"),
    ("b4", "And germs need water, same as you. Milk's even worse, because it's a full meal for them too.", 1.06, 0.4, -0.3, 1.4, ["water,", "meal"], "low"),
    ("c1", "Scientists score this from zero to one: how much of that water a germ can really use.", 1.07, 0.1, +0.4, 1.45, ["score"], "low"),
    ("c2", "Most bacteria need about zero point nine, but mould gets by on zero point seven.", 1.05, 0.1, +0.6, 1.45, ["nine,", "seven.:dn"], "low"),
    ("c3", "Burfee sits right in between, around zero point eight. Too dry for most bacteria, but not for mould.", 1.06, 0.1, +0.4, 1.45, ["between,", "mould.:dn"], "low"),
    ("c4", "That's why burfee's classic problem is a bit of fuzz on top.", 1.02, 0.35, +0.6, 1.45, ["fuzz"], "low"),
    ("c5", "And please don't just scrape it off. What you can see is only the top.", 1.03, 0.1, -0.3, 1.35, ["scrape", "top.:dn"], "low"),
    ("c6", "On soft food the roots go deeper, and bacteria you can't see can grow with it. The whole piece goes in the bin.", 1.08, 0.45, -0.3, 1.35, ["deeper,", "bin.:dn"], "low"),
    ("d1", "So do you just put everything in the fridge? Nearly.", 1.02, 0.3, +0.8, 1.5, ["everything", "Nearly.:dn"], "low"),
    ("d2", "In one lab test, sealed burfee lasted nine days at thirty degrees, and thirty five in the fridge.", 1.06, 0.3, +0.6, 1.45, ["nine", "thirty"], "low"),
    ("d3", "But it wasn't mould that finished it off in there. It went dry, hard and sandy.", 1.03, 0.1, +0.4, 1.45, ["mould", "sandy.:dn"], "low"),
    ("d4", "That's your rock hard fridge burfee. So keep it airtight, not in the cardboard box.", 1.08, 0.45, +0.4, 1.45, ["rock", "airtight"], "low"),
    ("e1", "Which brings us to the great Diwali re-gift.", 1.0, 0.3, +0.8, 1.5, ["re-gift.:dn"], "low"),
    ("e2", "Your neighbour gives you a box, you pass it to your cousin, and your cousin gives it to your boss.", 1.06, 0.3, +0.6, 1.45, ["cousin,", "boss.:dn"], "low"),
    ("e3", "Nobody's fuse resets. That kalaakund has been dead since Tuesday.", 1.0, 0.45, -0.3, 1.4, ["resets.", "Tuesday.:dn"], "low"),
    ("e4", "At the shop, you can check. Since twenty twenty, loose sweets have to show a best before date on the tray.", 1.07, 0.1, +0.4, 1.45, ["check.", "tray.:dn"], "low"),
    ("e5", "With a gift box, go by the list. It's a guide, and a hot kitchen means less time.", 1.05, 0.45, +0.4, 1.4, ["guide.", "hot"], "low"),
    ("f1", "So here's the order. Milky and soft first, dry and nutty last.", 1.02, 0.3, +0.6, 1.45, ["first,", "last.:dn"], "low"),
    ("f2", "Screenshot this. Kalaakund today, rusgoola by day two, burfee by day four, kaaju by the week, luddoo whenever you like.", 1.05, 0.3, +0.6, 1.45, ["today,", "whenever"], "low"),
    ("f3", "If it smells sour or grows fuzz, bin it, whatever the list says.", 1.03, 0.4, -0.3, 1.35, ["sour", "bin"], "low"),
    ("g1", "Send this to whoever gave you that box, so they know that you know!", 1.03, 0.0, +1.2, 1.5, ["box,", "know!"], None),
]
