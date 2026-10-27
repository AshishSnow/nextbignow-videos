# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# "Your airline's real money machine is your credit card" — Delta Q4/FY2025 results 8-K (Jan 13 2026): Amex remuneration $8.2B (+11%),
# operating income $5.8B; American Airlines Q4/FY2025 results 8-K (Jan 2026): record revenue $54.6B, net income $111M, loyalty liabilities
# $3,725M + $6,839M; American FY2025 10-K: cash payments from co-branded credit card and other partners $6.2B, may change AAdvantage terms
# "at any time and without notice"; United 8-K (Jun 15 2020): MileagePlus valued ~ $21.9B (12x 2019 EBITDA); Kirkland (Jul 2020): $6.8B
# financing secured by MileagePlus.
# Wh-question hook: falls naturally (VOICE.md: only yes/no questions rise) -> ending None, stress on the number.
LINES = [
    ("i1", "Why would a credit card company pay an airline eight billion dollars?", 1.04, 0.35, +1.0, 1.45, ["credit", "eight"], None),
    ("i2", "That's what American Express paid Delta last year.", 1.04, 0.40, +0.6, 1.45, ["American", "Delta:dn"], "low"),
    ("a1", "Now look at Delta's entire profit for the year. Five point eight billion.", 1.04, 0.35, +0.8, 1.45, ["entire", "Five"], "low"),
    ("a2", "The card deal was bigger… than the whole airline's profit.", 1.02, 0.45, +1.0, 1.5, ["bigger…", "whole"], "low"),
    ("a3", "And Delta isn't the only one.", 1.04, 0.25, +0.8, 1.45, ["only"], None),
    ("b1", "American Airlines brought in a record fifty four billion dollars last year.", 1.04, 0.25, +0.8, 1.45, ["record", "fifty"], None),
    ("b2", "It kept just one hundred eleven million as profit.", 1.02, 0.35, +0.6, 1.5, ["just", "million:dn"], "low"),
    ("b3", "But card companies and partners paid it six point two billion dollars.", 1.04, 0.40, +1.0, 1.5, ["paid", "six"], "low"),
    ("c1", "So what are they really paying for? Your miles.", 1.02, 0.30, +1.0, 1.5, ["really", "miles.:dn"], "low"),
    ("c2", "Every time you swipe an airline card, the bank pays the airline. That's where your miles come from.", 1.04, 0.25, +0.8, 1.45, ["swipe", "pays"], None),
    ("c3", "You feel rewarded. The bank gets your spending. And the airline gets paid for a number it adds to your account.", 1.04, 0.40, +0.8, 1.45, ["rewarded.", "number"], "low"),
    ("d1", "But the wildest proof came in twenty twenty.", 1.02, 0.30, +1.0, 1.5, ["wildest", "twenty"], None),
    ("d2", "Planes were parked. So United borrowed six point eight billion dollars, and put up its miles program as security.", 1.04, 0.30, +0.8, 1.45, ["parked.", "miles"], None),
    ("d3", "United itself valued those miles at about twenty two billion dollars.", 1.02, 0.45, +0.8, 1.5, ["itself", "twenty"], "low"),
    ("t1", "Here's the catch for you. The airline decides what a mile is worth, and it can change the rules any time.", 1.04, 0.30, +0.8, 1.45, ["catch", "any"], None),
    ("t2", "American alone is holding about ten and a half billion dollars of miles that people haven't used.", 1.04, 0.35, +0.8, 1.45, ["alone", "ten"], "low"),
    ("t3", "So treat miles like cash that can shrink. Earn them, then use them. Don't hoard them.", 1.02, 0.35, +0.8, 1.45, ["shrink.", "use"], "low"),
    ("e1", "Because to an airline, the most valuable thing you carry isn't your suitcase. It's the card in your wallet.", 1.02, 0.35, +0.6, 1.45, ["suitcase.", "wallet.:dn"], "low"),
    ("e2", "Send this to the friend who's been saving miles for ten years!", 1.06, 0.0, +1.0, 1.45, ["friend", "ten"], None),
]
