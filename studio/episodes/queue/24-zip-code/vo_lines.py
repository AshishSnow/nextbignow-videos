# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# HOW IT WORKS · EP 8* (renumber at build: next free HOW IT WORKS number) — "Why the card machine asks for your ZIP code" (topic_bank W16).
# Written by the R&D writers' room 14 Nov 2026 (WRITING.md, whiteboard look). Facts: SOURCES.md (FTC Data Brokers report May 2014 p.24;
# Pineda v. Williams-Sonoma, Cal. S. Ct. 10 Feb 2011; Cal. Civ. Code 1747.08; Tyler v. Michaels Stores, Mass. SJC 11 Mar 2013;
# Flores v. Chevron, Cal. Ct. App. 20 Jun 2013; Apple v. Superior Court, Cal. S. Ct. 4 Feb 2013). Education only, not legal advice.
# No store is named (what the stores did is the shoppers' allegation, never a finding); no data broker named; two states only.
SERIES = "HOW IT WORKS"; PART = 0; EP = 8
LINES = [
    ("i1", "Do you know typing your ZIP at checkout can lead a store to your door?", 0.97, 0.7, +1.0, 1.45, ['ZIP', 'door?'], None),
    ("i2", "You're at the register, card in hand, about to pay. The little screen wants five digits.", 0.97, 0.25, +0.8, 1.45, ['register,', 'five'], 'low'),
    ("i3", "Seems harmless. Lots of people share one.", 0.97, 0.3, +0.8, 1.45, ['harmless.', 'Lots'], 'low'),
    ("i4", "Three things to know before you type it. In two states, the store isn't supposed to ask.", 0.97, 0.35, +0.8, 1.45, ['Three', 'ask.:dn'], 'low'),
    ("a1", "First, the store already knows your name. It's printed on your card.", 0.97, 0.25, +0.8, 1.45, ['name.', 'card.'], 'low'),
    ("a2", "Add a ZIP code, and the list of people you could be gets tiny. How tiny?", 0.97, 0.3, +0.6, 1.45, ['tiny.', 'tiny?'], 'low'),
    ("a3", "In twenty fourteen, America's consumer watchdog studied data brokers. Companies that sell information about people.", 0.97, 0.2, +0.6, 1.45, ['watchdog', 'sell'], 'low'),
    ("a4", "Its report describes a lookup some brokers offered. A store sends in a customer's name and the store's own ZIP code.", 0.97, 0.2, +0.6, 1.45, ['lookup', 'own'], 'low'),
    ("a5", "Back comes that customer's address.", 0.97, 0.3, +0.6, 1.45, ['address.:dn'], 'low'),
    ("a6", "Honestly? The store's ZIP, not even yours. That's the part that gets me.", 0.96, 0.4, +0.8, 1.45, ['Honestly?', 'yours.'], 'low'),
    ("b1", "Second, a California shopper sued.", 0.97, 0.2, +0.8, 1.45, ['California', 'sued.:dn'], 'low'),
    ("b2", "She said a home goods chain asked for her ZIP at the register.", 0.97, 0.15, +0.6, 1.45, ['ZIP', 'register.'], 'low'),
    ("b3", "Her claim: the store's software matched it with her name and found her address.", 0.97, 0.3, +0.6, 1.45, ['software', 'address.:dn'], 'low'),
    ("b4", "The question for the court: is a ZIP code personal information? In twenty eleven, California's top court said yes.", 0.97, 0.2, +0.6, 1.45, ['personal', 'yes.:dn'], 'low'),
    ("b5", "So asking for it during a credit card sale, and writing it down, breaks the state's law.", 0.97, 0.3, +0.6, 1.45, ['credit', 'breaks'], 'low'),
    ("b6", "What can that cost the store? Up to two hundred fifty dollars the first time. Up to a thousand dollars each time after.", 0.97, 0.3, +0.6, 1.45, ['fifty', 'thousand'], 'low'),
    ("b7", "Two years later, Massachusetts' top court said a ZIP code counts there too.", 0.97, 0.35, +0.6, 1.45, ['Massachusetts\'', 'too.:dn'], 'low'),
    ("c1", "Third, where those laws stop.", 0.96, 0.25, +0.8, 1.35, ['Third,', 'stop.:dn'], 'low'),
    ("c2", "They're only about credit cards, so paying cash isn't covered.", 0.97, 0.25, +0.6, 1.45, ['credit', 'cash'], 'low'),
    ("c3", "Want it delivered? California lets the store ask where you live.", 0.97, 0.25, +0.6, 1.45, ['delivered?', 'live.:dn'], 'low'),
    ("c4", "And the gas pump that wants your ZIP? California allows that one, as long as it's only used to stop stolen cards.", 0.97, 0.3, +0.6, 1.45, ['pump', 'stolen'], 'low'),
    ("c5", "Those are two states. Live somewhere else? Look up your state's rules.", 0.97, 0.35, +0.6, 1.45, ['two', 'rules.:dn'], 'low'),
    ("d1", "So yes. A name off a card and five digits can be enough to find a front door.", 0.96, 0.35, +0.8, 1.45, ['yes.', 'door.:dn'], 'low'),
    ("t1", "When the screen asks, ask the cashier what it's for. You're allowed to.", 0.97, 0.35, +0.8, 1.45, ['ask', 'for.'], 'low'),
    ("z1", "Save this. Five digits at the register. Give it, or say no? Tell me in the comments.", 1.0, 0.2, +1.0, 1.45, ['Save', 'Give', 'no?'], None),
    ("z2", "Send this to the friend who types their ZIP without even looking.", 1.0, 0.0, +1.0, 1.45, ['friend', 'looking.'], None),
]
