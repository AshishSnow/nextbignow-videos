# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# YOUR MOVE · EP 1 · PART 2 — the court case (type A, POV; build ~24 h after Part 1 in the same IST slot; STORY.md §3)
# Facts (../SOURCES-pepsi-jet.md; re-verify — esp. 'jet not in the catalog' and the Statute of Frauds point in the opinion text): Leonard sued; PepsiCo asked the court for a declaratory judgment that it owed no
# jet; Judge Kimba Wood (S.D.N.Y.), 5 Aug 1999, summary judgment for PepsiCo: the ad was not an offer; "no objective person
# could reasonably have concluded that the commercial actually offered consumers a Harrier jet"; the scenario was an
# "exaggerated adolescent fantasy"; Pentagon: the jet would not be sold to civilians without demilitarization; 2nd Circuit
# affirmed (210 F.3d 88, 2000); Pepsi later listed the jet at 700,000,000 points with "Just Kidding"; Netflix docuseries
# "Pepsi, Where's My Jet?" (Nov 2022) — optional on-screen fact only. Never say Pepsi "lied" or "settled"; never call Leonard a scammer.
# Never claim "most of you said …" unless Part 1 comment counts are real (STORY.md §3).
SERIES = "YOUR MOVE"; PART = 2; EP = 1
LINES = [
    ("i1", "Part two. You mailed Pepsi a check for a jet. Will a judge make them deliver?", 1.02, 0.40, +1.0, 1.45, ["two.", "judge", "deliver?"], "q"),
    ("i2", "Quick recap: you raised seven hundred thousand dollars. The jet is worth over twenty million.", 1.04, 0.35, +0.8, 1.45, ["hundred", "twenty"], "low"),
    ("a1", "Here's what really happened. You don't drop it. You sue.", 1.02, 0.35, +0.8, 1.5, ["really", "sue.:dn"], "low"),
    ("a2", "But Pepsi moves too. Its lawyers ask a court to rule that it owes you nothing.", 1.04, 0.35, +0.8, 1.45, ["too.", "nothing.:dn"], "low"),
    ("a3", "Three questions will decide who wins.", 1.02, 0.40, +0.8, 1.45, ["Three", "wins.:dn"], "low"),
    ("b1", "Question one. Was the ad a real offer?", 1.02, 0.30, +1.0, 1.45, ["one.", "offer?"], "q"),
    ("b2", "Usually, an ad isn't a promise. It's an invitation to come and buy.", 1.02, 0.30, +0.8, 1.45, ["isn't", "invitation"], "low"),
    ("b3", "And the jet isn't even in the prize catalog.", 1.02, 0.40, +0.8, 1.45, ["even", "catalog.:dn"], "low"),
    ("c1", "Question two. Would a normal person believe it?", 1.02, 0.30, +1.0, 1.45, ["two.", "believe"], "q"),
    ("c2", "The judge watches the ad. A teen flies a fighter jet to school.", 1.02, 0.30, +0.8, 1.45, ["judge", "school.:dn"], "low"),
    ("c3", "She calls it an exaggerated adolescent fantasy.", 1.0, 0.40, +0.6, 1.5, ["exaggerated", "fantasy.:dn"], "low"),
    ("d1", "Question three. Where's the signed contract?", 1.02, 0.30, +1.0, 1.45, ["three.", "signed"], None),
    ("d2", "A deal this big needs one in writing. There isn't one.", 1.02, 0.35, +0.8, 1.45, ["writing.", "isn't"], "low"),
    ("d3", "August, nineteen ninety nine. The ruling: no objective person could think that ad offered a real jet.", 1.0, 0.40, +0.6, 1.5, ["August,", "objective"], "low"),
    ("d4", "You appeal. You lose again. No jet.", 1.0, 0.45, +0.6, 1.5, ["appeal.", "again.", "jet.:dn"], "low"),
    ("d5", "And even if you won, the Pentagon said that jet isn't sold to civilians unless it's demilitarized.", 1.04, 0.40, +0.8, 1.45, ["Pentagon", "civilians"], "low"),
    ("t1", "But Pepsi changed the ad: seven hundred million points… and the words just kidding.", 1.02, 0.40, +0.8, 1.5, ["changed", "seven", "kidding."], "low"),
    ("t2", "Oops.", 0.98, 0.50, +0.4, 1.5, ["Oops."], "low"),
    ("e1", "The takeaway? Price every joke like someone will pay it.", 1.02, 0.35, +0.8, 1.45, ["takeaway?", "joke", "pay"], "low"),
    ("e2", "Was the judge right? Comment FAIR or ROBBED.", 1.02, 0.35, +1.0, 1.45, ["right?", "FAIR", "ROBBED."], None),
    ("e3", "Send this to the friend who'd mail that check.", 1.06, 0.0, +1.0, 1.45, ["friend", "check."], None),
]
