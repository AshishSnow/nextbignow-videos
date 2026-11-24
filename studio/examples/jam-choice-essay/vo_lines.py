# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# MIND TRICKS N° 04: jam study. HOOK/BUILD/DELIVER/CLOSE tags in comments. Facts: ../SOURCES.md
SERIES = "OOPS MIND TRICKS"; PART = 0; EP = 44
CBVOICES = {}
LINES = [
    ("h1", "A grocery store put out twenty four jams to taste. Almost nobody bought one.", 0.92, 0.2, +1.0, 1.55, ['twenty', 'nobody'], None),      # HOOK: surprise
    ("h2", "Then they cut it to six. And sales jumped.", 0.92, 0.3, +1.0, 1.55, ['six.', 'jumped.'], None),                                      # HOOK: twist
    ("a1", "It was a real experiment, run by two researchers at a fancy California grocery store.", 0.92, 0.2, +0.9, 1.5, ['real', 'California'], None),  # BUILD: credibility
    ("a2", "The big table pulled in more people. Sixty percent stopped, versus forty percent at the small one.", 0.92, 0.2, +0.9, 1.5, ['more', 'Sixty'], None),  # BUILD: fact
    ("q1", "So the big table won, right?", 0.92, 0.2, +1.0, 1.6, ['won,', 'right?'], None),                                                     # rehook
    ("a3", "Nope. Of the people who stopped, three percent bought from the big table. At the small table? Thirty percent.", 0.92, 0.25, +0.9, 1.55, ['three', 'Thirty'], None),  # DELIVER: key number
    ("a4", "Shoppers were about six times more likely to buy with fewer choices. It's called choice overload.", 0.92, 0.2, +0.9, 1.5, ['six', 'overload.'], None),  # DELIVER: name it
    ("q2", "Does it always work?", 0.92, 0.2, +1.0, 1.55, ['always'], None),                                                                     # rehook (honest)
    ("a5", "No. Later studies found it depends on how hard the choice feels. But if your customers look stuck, that's your clue.", 0.92, 0.25, +0.9, 1.5, ['depends', 'stuck,'], None),  # DELIVER: caveat + use
    ("z1", "So if people can't decide, don't add another flavor. Take one away.", 0.93, 0.0, +1.0, 1.5, ['another', 'away.'], None),             # CLOSE: action
]
