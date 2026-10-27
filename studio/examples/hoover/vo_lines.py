# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# "Hoover's free flights" (type A, wild true story) — roadmap: three mistakes, the last one the cruelest.
# Sources (verified 28 Oct 2026):
#   offer: GBP 100+ on Hoover products -> two free return flights to Europe (Aug 1992), US added (New York / Orlando) late 1992:
#     Wikipedia (cites BBC News 13 May 2004), The Hustle, UPI 27 Apr 1993 ('December expansion: New York or Orlando'), Chief Marketer 2005
#   cheapest qualifying vacuum ~GBP 119 (The Hustle, Entrepreneur 2019) = UPI's '$177 vacuum cleaner'; tickets worth ~GBP 600 (BBC via Wikipedia)
#   resale + 80,000 extra appliances in Dec-Jan (sales-promotion professionals' estimate): UPI 27 Apr 1993
#   travel agents: expensive extras, inconvenient airports, undesirable dates; three top executives fired; $30M fund: TIME 12 Apr 1993
#   $30M after-tax charge, Q1 1993 loss: UPI 27 Apr 1993; pressure group of thousands: Inc. (Aug 2023), The Hustle (AP: 4,000+)
#   court cases for years (to 1998): BBC 2004 via Wikipedia; Funding Universe / Intl Directory of Company Histories
#   ~220,000 flew: Marketing Week ('Hoover fails to shake off free flights horror'), Chief Marketer (Oct 2005), Funding Universe
#   GBP 48M cost: Marketing Week (2 Jun 1995), Campaign, Management Today
#   June 1995 sale of European operations for $164.3M cash, after-tax loss $135.4M: Maytag 1995 annual report (SEC 10-K);
#     buyer Candy: BBC2 Ceefax 30 May 1995, Marketing Week 2 Jun 1995, Funding Universe
LINES = [
    ("i1", "What happens when a vacuum company gives away free flights, and everyone says yes?", 1.02, 0.40, +1.0, 1.45, ["free", "everyone"], None),
    ("i2", "Hoover found out. Three bosses fired, and its whole European business sold.", 1.02, 0.35, +0.6, 1.45, ["Three", "sold.:dn"], "low"),
    ("i3", "It took three mistakes. And the last one was the cruelest.", 1.02, 0.45, +0.8, 1.45, ["three", "cruelest.:dn"], "low"),
    ("a1", "Mistake one: the maths.", 1.0, 0.30, +1.0, 1.45, ["one:", "maths.:dn"], "low"),
    ("a2", "Britain, nineteen ninety two. Spend a hundred pounds on Hoover products.", 1.02, 0.25, +0.8, 1.45, ["Britain,", "hundred"], None),
    ("a3", "Get two free return flights to Europe.", 1.02, 0.35, +0.8, 1.45, ["free", "Europe.:dn"], "low"),
    ("a4", "A few months later, they made it bigger. Flights to America.", 1.02, 0.30, +1.0, 1.45, ["bigger.", "America."], None),
    ("a5", "The cheapest vacuum that counted cost about one hundred and nineteen pounds.", 1.02, 0.25, +0.8, 1.45, ["cheapest", "nineteen"], None),
    ("a6", "Two flights across the Atlantic were worth several times that.", 1.02, 0.40, +0.8, 1.45, ["several", "that.:dn"], "low"),
    ("a7", "Hoover wasn't really selling vacuums anymore. It was buying people holidays.", 1.02, 0.45, +0.6, 1.5, ["selling", "holidays.:dn"], "low"),
    ("b1", "Mistake two: customers can do maths too.", 1.0, 0.30, +1.0, 1.45, ["two:", "too.:dn"], "low"),
    ("b2", "People bought vacuums they didn't need, just for the tickets.", 1.02, 0.25, +0.8, 1.45, ["didn't", "tickets."], None),
    ("b4", "In the December and January rush alone, experts estimated eighty thousand extra machines.", 1.02, 0.35, +0.8, 1.45, ["alone,", "eighty"], None),
    ("b5", "Every single buyer was owed two plane tickets. So what would Hoover do?", 1.0, 0.40, +0.6, 1.5, ["owed", "Hoover"], None),
    ("c1", "Mistake three. The cruelest one.", 1.0, 0.40, +0.8, 1.5, ["three.", "cruelest"], "low"),
    ("c2", "The travel agents running the offer made the flights hard to get.", 1.02, 0.25, +0.8, 1.45, ["hard"], None),
    ("c3", "Airports far from home. Dates nobody wanted. Expensive extras.", 1.0, 0.35, +0.8, 1.45, ["far", "nobody", "extras.:dn"], "low"),
    ("c4", "Customers were furious. Thousands joined a pressure group to fight Hoover.", 1.02, 0.30, +0.8, 1.45, ["furious.", "Thousands"], None),
    ("c5", "The court cases dragged on for years.", 1.0, 0.45, +0.6, 1.5, ["years.:dn"], "low"),
    ("d1", "So who paid the bill?", 1.02, 0.40, +1.0, 1.45, ["who", "bill?"], None),
    ("d2", "Hoover's American owner, Maytag, fired three top executives.", 1.02, 0.30, +0.8, 1.45, ["fired", "three"], None),
    ("d3", "It set aside thirty million dollars after tax, just to fly people.", 1.02, 0.30, +0.8, 1.45, ["thirty", "fly"], None),
    ("d4", "In the end, about two hundred and twenty thousand people flew.", 1.02, 0.30, +0.8, 1.45, ["twenty", "flew.:dn"], "low"),
    ("d5", "The trade press put the total cost at forty eight million pounds.", 1.02, 0.40, +0.8, 1.45, ["total", "forty"], "low"),
    ("d6", "The final blow? In nineteen ninety five, Maytag sold Hoover's European business to an Italian rival.", 1.02, 0.30, +0.8, 1.45, ["blow?", "sold", "Italian"], None),
    ("d7", "The loss on that sale? About one hundred thirty five million dollars.", 1.0, 0.55, +0.6, 1.5, ["sale?", "thirty"], "low"),
    ("t1", "Here's the twist. The offer worked perfectly. It sold vacuums. Far too many of them.", 1.0, 0.40, +0.8, 1.5, ["twist.", "perfectly.", "many"], "low"),
    ("t2", "Free gift worth more than what you buy? Read the claim rules first.", 1.02, 0.30, +0.8, 1.45, ["more", "claim"], "low"),
    ("e1", "Running a giveaway? First ask: what happens when everyone says yes?", 1.0, 0.35, +0.8, 1.45, ["giveaway?", "everyone"], None),
    ("e2", "Send this to the friend who never reads the small print!", 1.06, 0.0, +1.0, 1.45, ["friend", "small"], None),
]
