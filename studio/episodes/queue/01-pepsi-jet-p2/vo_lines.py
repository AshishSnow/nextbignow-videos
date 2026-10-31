# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# YOUR MOVE · EP 1 · PART 2 — the court case (type A, POV; build ~24 h after Part 1 in the same IST slot; STORY.md §3)
# Fresh-eyes review 31 Oct applied: PepsiCo filed first (S.D.N.Y., 18 Jul 1996), Leonard sued in Florida (~6 Aug 1996, moved to NY);
# 700M + 'Just Kidding' version ran when the ad went national in 1996 (judge: a move to head off lawsuits, not an admission —
# never present it as a confession); Statute of Frauds = sale of goods >= $500 needs a writing signed by the party charged.
# Pentagon spokesman Kenneth Bacon: without weapons, 'not one he could fly' (Mental Floss). Facts: Leonard sued; PepsiCo asked the court for a declaratory judgment that it owed no
# jet; Judge Kimba Wood (S.D.N.Y.), 5 Aug 1999, summary judgment for PepsiCo: the ad was not an offer; "no objective person
# could reasonably have concluded that the commercial actually offered consumers a Harrier jet"; the scenario was an
# "exaggerated adolescent fantasy"; Pentagon: the jet would not be sold to civilians without demilitarization; 2nd Circuit
# affirmed (210 F.3d 88, 2000); Pepsi later listed the jet at 700,000,000 points with "Just Kidding"; Netflix docuseries
# "Pepsi, Where's My Jet?" (Nov 2022) — optional on-screen fact only. Never say Pepsi "lied" or "settled"; never call Leonard a scammer.
# Never claim "most of you said …" unless Part 1 comment counts are real (STORY.md §3).
SERIES = "YOUR MOVE"; PART = 2; EP = 1
LINES = [
    ("i1", "You mailed Pepsi a check for a fighter jet. Will a judge make them deliver?", 1.02, 0.40, +1.0, 1.45, ["check", "judge", "deliver?"], "q"),
    ("i2", "Part two. Their ad priced the jet at seven million points. Points cost ten cents. So you paid seven hundred thousand.", 1.04, 0.35, +0.8, 1.45, ["seven", "ten", "hundred"], "low"),
    ("a1", "Here's what really happened. Pepsi moves first.", 1.02, 0.30, +0.8, 1.5, ["really", "first.:dn"], "low"),
    ("a2", "Its lawyers ask a New York court to rule that it owes you nothing. So you sue back.", 1.04, 0.35, +0.8, 1.45, ["nothing.", "back.:dn"], "low"),
    ("a4", "But watch the ad. Pepsi changes the jet's price to seven hundred million points… plus the words: just kidding.", 1.02, 0.40, +0.8, 1.5, ["watch", "seven", "kidding."], "low"),
    ("a5", "Oops.", 0.98, 0.45, +0.4, 1.5, ["Oops."], "low"),
    ("a6", "Not an admission, the judge later says. Just a way to head off more lawsuits.", 1.02, 0.40, +0.8, 1.45, ["admission,", "lawsuits.:dn"], "low"),
    ("a3", "So three questions will decide who wins.", 1.02, 0.40, +0.8, 1.45, ["three", "wins.:dn"], "low"),
    ("b1", "Question one. Was the ad a real offer?", 1.02, 0.30, +1.0, 1.45, ["one.", "offer?"], "q"),
    ("b2", "Usually, an ad isn't an offer. It invites you to make one, and the company can say no.", 1.02, 0.30, +0.8, 1.45, ["isn't", "no.:dn"], "low"),
    ("b3", "And the small print you read? The jet isn't even in the prize catalog.", 1.02, 0.40, +0.8, 1.45, ["small", "catalog.:dn"], "low"),
    ("c1", "Question two. Would a normal person believe it?", 1.02, 0.30, +1.0, 1.45, ["two.", "believe"], "q"),
    ("c2", "The judge watches the ad. A teen flies a fighter jet to school.", 1.02, 0.30, +0.8, 1.45, ["judge", "school.:dn"], "low"),
    ("c3", "She calls flying a jet to school an exaggerated adolescent fantasy.", 1.0, 0.40, +0.6, 1.5, ["exaggerated", "fantasy.:dn"], "low"),
    ("d1", "Question three. Did Pepsi ever sign anything?", 1.02, 0.30, +1.0, 1.45, ["three.", "sign"], "q"),
    ("d2", "A sale over five hundred dollars needs a written deal, signed by the side you're suing. Pepsi signed nothing.", 1.04, 0.35, +0.8, 1.45, ["written", "nothing."], "low"),
    ("d3", "August, nineteen ninety nine. The ruling: no objective person could think that ad offered a real jet.", 1.0, 0.40, +0.6, 1.5, ["August,", "objective"], "low"),
    ("d4", "You appeal. You lose again.", 1.0, 0.45, +0.6, 1.5, ["appeal.", "again.:dn"], "low"),
    ("t1", "And even if you'd won? The Pentagon said you couldn't fly it home.", 1.02, 0.40, +0.8, 1.5, ["won?", "fly"], "low"),
    ("e1", "So price every joke like someone will pay it.", 1.02, 0.35, +0.8, 1.45, ["joke", "pay"], "low"),
    ("e2", "Was that ad a joke, or a deal? Comment JOKE or DEAL.", 1.02, 0.35, +1.0, 1.45, ["joke,", "deal?", "JOKE"], None),
    ("e3", "Send this to the friend who'd mail that check.", 1.06, 0.0, +1.0, 1.45, ["friend", "check."], None),
]
