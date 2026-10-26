# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# "Duolingo gives every lesson away free, yet made over $1B last year — the streak" (Duolingo FY2025 10-K + Q4 FY2025 8-K, Q2 2026 8-K, Duolingo blog Jan 2022)
LINES = [
    ("i1", "Duolingo gives away every single lesson for free… so how did it make over a billion dollars last year?", 1.06, 0.30, +1.0, 1.4, ["free…", "billion"], "q"),
    ("i2", "The secret is one tiny number. Your streak.", 1.02, 0.40, +0.6, 1.45, ["tiny", "streak.:dn"], "low"),
    ("a1", "Every course really is free. You just watch an ad after each lesson.", 1.04, 0.20, +1.0, 1.45, ["free.", "ad"], None),
    ("a2", "But ads bring in less than eight cents of every dollar.", 1.04, 0.30, +0.8, 1.45, ["eight", "dollar.:dn"], "low"),
    ("a3", "The real money? About nine in every hundred monthly users pay.", 1.04, 0.20, +1.0, 1.45, ["money?", "nine"], None),
    ("a4", "By June, that was twelve point seven million subscribers.", 1.04, 0.40, +0.6, 1.45, ["twelve", "subscribers.:dn"], "low"),
    ("b1", "So Duolingo needs you back. Every single day.", 1.02, 0.25, +1.0, 1.45, ["back.", "Every"], None),
    ("b2", "That's what the streak is for. Miss one day… and it drops back to zero.", 1.04, 0.30, +0.8, 1.45, ["streak", "zero.:dn"], "low"),
    ("b3", "On day two, who cares? But on day two hundred, losing it feels like losing money.", 1.04, 0.40, +1.0, 1.5, ["cares?", "hundred,"], None),
    ("c0", "And it works. Wait for this number.", 1.04, 0.30, +1.2, 1.5, ["works.", "number."], None),
    ("c1", "At the end of last year, forty three million people opened it daily on a streak of a week or more.", 1.06, 0.20, +0.8, 1.45, ["forty", "week"], None),
    ("c2", "And about fifteen million were on a streak longer than a whole year!", 1.04, 0.30, +1.2, 1.5, ["fifteen", "year!"], None),
    ("c3", "In one June event, fifteen point four million people revived a broken streak.", 1.06, 0.40, +0.6, 1.45, ["revived", "streak.:dn"], "low"),
    ("d1", "Here's the twist. Every day you come back is another ad… or another nudge to pay.", 1.04, 0.25, +1.0, 1.5, ["twist.", "pay.:dn"], None),
    ("d2", "The streak costs you nothing. Your habit is the whole business.", 1.02, 0.45, +0.6, 1.45, ["nothing.", "habit"], "low"),
    ("d3", "But steal the trick. People who hit a seven day streak were three point six times more likely to finish their course.", 1.06, 0.25, +0.8, 1.45, ["steal", "three"], None),
    ("e1", "So want a habit to stick? Start a streak… and just survive the first seven days.", 1.02, 0.35, +0.6, 1.45, ["stick?", "seven"], None),
    ("e2", "Send this to the friend who has never missed a day on Duolingo!", 1.06, 0.0, +1.0, 1.45, ["friend", "never"], None),
]
