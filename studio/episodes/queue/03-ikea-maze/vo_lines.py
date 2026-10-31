# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# SPOT THE TRICK · #1 — "Why does IKEA hide the way out?" (type E; STORY.md SPOT THE TRICK beat sheet). You = the shopper.
# Facts (see SOURCES.md; re-verify before building): Inter IKEA FY25 retail sales EUR 44.6bn, 915m store visits (16 Oct 2025);
# UCL lecture by Prof Alan Penn (Jan 2011): listing blurb "deliberately set out to confuse you"; Penn, as reported: "the way to the
# exit is always behind you"; ~60 % of purchases not on the list = Penn's ESTIMATE (say "he estimates"); IKEA Sweden 2011: stores
# offer shortcuts to all departments; "bulla bulla" = IKEA jargon for over-filled bins giving "the impression of volume and, therefore,
# inexpensiveness" (The New Yorker, Oct 2011, via Mental Floss); IKEA history page: restaurant from 1960 — "He realized that hungry
# customers buy less"; IKEA Food EUR 2.15bn turnover, 680m food guests (FY2019, Ingka Feb 2020 — latest official figure); US bistro
# hot dog $1.00 (ikea.com); IKEA effect: Norton, Mochon & Ariely, J. Consumer Psychology 22 (2012): builders bid $0.78 vs $0.48 =
# 63 % premium; completed box $1.46 vs incomplete $0.59; built-then-taken-apart Lego → premium gone; "labor leads to love only when
# labor results in successful completion of tasks". Twist: Ingka retail chief Tolga Öncü, Fortune 1 Sep 2023 — free-path city stores
# (Madrid, Shanghai, Warsaw) were closed; customers: "No, no, no, this is a big shop!"
# Fresh-eyes review 31 Oct applied: no yellow bag (trade dress), "the store says" shortcuts exist, no "Harvard and Duke" (not in
# sources), "sells you the work" → "you do the work" (no evil-company framing), a Beat-it line for Trick 4, takeaway as three verbs,
# chip for the Penn quote = reported line, "shoppers wanted guiding", Trick 3 = "the food", pills MAZE/BINS/FOOD/SHELF.
# ASR: if "IKEA" reads back wrong, say "the flat-pack giant" in VO and keep IKEA on screen only. No logo, no blue/yellow trade dress.
# No "Oops." beat: there is no blunder here — the tricks work (STORY.md §2: keep the beat special).
SERIES = "SPOT THE TRICK"; PART = 0; EP = 1
LINES = [
    ("i1", "Why does IKEA hide the way out?", 1.02, 0.40, +1.0, 1.45, ["IKEA", "out?"], "q"),
    ("i2", "You walk in to buy one lamp. Budget: twenty dollars.", 1.02, 0.35, +0.8, 1.45, ["one", "twenty"], "low"),
    ("i3", "This shop sells nearly forty-five billion euros a year. Four tricks nudge you along the way.", 1.02, 0.30, +0.8, 1.45, ["forty", "Four"], "low"),
    ("i4", "The last one follows you home.", 1.02, 0.45, +0.8, 1.45, ["home.:dn"], "low"),
    ("a1", "Trick one. The path.", 1.0, 0.30, +0.8, 1.45, ["one.", "path."], "low"),
    ("a2", "One path, one direction, but the exit is always behind you.", 1.02, 0.30, +0.8, 1.45, ["direction,", "behind"], "low"),
    ("a3", "A London professor says the layout is built to confuse you, so you pass everything.", 1.02, 0.35, +0.8, 1.45, ["professor", "confuse"], "low"),
    ("a4", "He estimates six in ten things bought here were never on the list.", 1.02, 0.40, +0.8, 1.45, ["six", "never"], "low"),
    ("a5", "Beat it: ask staff for the shortcut doors. The store says they're there.", 1.02, 0.45, +0.6, 1.45, ["shortcut", "says"], "low"),
    ("b1", "Trick two. The bins.", 1.0, 0.30, +0.8, 1.45, ["two.", "bins."], "low"),
    ("b2", "Huge tubs of one cheap thing. Staff even have a name for it: bulla bulla.", 1.02, 0.30, +0.8, 1.45, ["Huge", "bulla"], "low"),
    ("b3", "A mountain of stuff looks like a bargain. So your lamp gets a candle friend.", 1.02, 0.40, +0.6, 1.45, ["bargain.", "candle"], "low"),
    ("b4", "Beat it: a full bin is not a sale. Read the tag.", 1.02, 0.45, +0.6, 1.45, ["not", "tag."], "low"),
    ("c1", "Trick three. The food.", 1.0, 0.30, +0.8, 1.45, ["three.", "food."], "low"),
    ("c2", "Halfway through you're starving, and there's a one-dollar hot dog.", 1.02, 0.30, +0.8, 1.45, ["starving", "one"], "low"),
    ("c3", "The founder added the restaurant in nineteen sixty. His reason: hungry customers buy less.", 1.02, 0.35, +0.8, 1.45, ["sixty.", "less.:dn"], "low"),
    ("c4", "Full, you keep walking. Food alone brought in over two billion euros in a year.", 1.02, 0.40, +0.6, 1.45, ["Full,", "billion"], "low"),
    ("c5", "Beat it: eat first, then shop the list, not the showroom.", 1.02, 0.45, +0.6, 1.45, ["first,", "showroom."], "low"),
    ("d1", "Trick four. The one that follows you home.", 1.0, 0.35, +1.0, 1.5, ["four.", "home."], "low"),
    ("d2", "You build the shelf. It wobbles. You still love it.", 1.02, 0.30, +0.8, 1.45, ["wobbles.", "still"], "low"),
    ("d3", "Researchers tested this with plain boxes.", 1.02, 0.30, +0.8, 1.45, ["tested"], "low"),
    ("d4", "Build a plain box yourself, and you bid sixty-three percent more than someone handed it built.", 1.02, 0.35, +0.8, 1.45, ["sixty", "built."], "low"),
    ("d5", "Finish it, and you overvalue it. Stop halfway? The magic is gone.", 1.02, 0.35, +0.8, 1.45, ["Finish", "gone.:dn"], "low"),
    ("d6", "So you do the work, and you fall for your own work.", 1.0, 0.40, +0.6, 1.5, ["work,", "own"], "low"),
    ("d8", "Beat it: before you keep it, price it like a stranger would.", 1.02, 0.45, +0.6, 1.45, ["stranger"], "low"),
    ("d7", "The twist? IKEA tried stores with no maze.", 1.02, 0.35, +1.0, 1.45, ["twist?", "no"], "low"),
    ("t1", "Shoppers wanted guiding. IKEA closed those stores.", 1.02, 0.45, +0.8, 1.5, ["guiding.", "stores.:dn"], "low"),
    ("k1", "Bring a list. Take the shortcut. Ask what a stranger would pay.", 1.02, 0.35, +0.8, 1.45, ["list.", "stranger"], "low"),
    ("e1", "Save this before your next trip. Comment which trick got you.", 1.02, 0.35, +1.0, 1.45, ["Save", "which"], None),
    ("e2", "Send this to the friend who went in for a lamp.", 1.06, 0.0, +1.0, 1.45, ["lamp."], None),
]
