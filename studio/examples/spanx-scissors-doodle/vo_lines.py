# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# REAL CASE STUDY · Spanx: $5,000, a pair of scissors and a ladies'-room demo — 14 Nov 2026, DOODLE format (owner: "new video will go in this format").
# Characters: FAX MACHINE (usa_boss), SCISSORS (usa_young). Sara Blakely drawn as a plain doodle person with a name tape (no likeness).
# Shapewear shown only as tan footless stockings on a hanger + white pants — kept tasteful.
# Facts:
#  Entrepreneur (2014): 7 years selling fax machines door to door; cut the feet off tan pantyhose to wear under white pants; $5,000 savings, no
#   retail/manufacturing experience; hosiery makers wouldn't take her seriously by phone, she drove to North Carolina; ~2-3 weeks later a Charlotte
#   manufacturer agreed; bought her own ticket to Dallas for a 10-minute meeting; bathroom demonstration -> order for seven Neiman Marcus stores.
#  Business of Business: every NC hosiery manufacturer turned her down, one called two weeks later; wrote the initial patent application herself,
#   attorney $750 to finalize; invited the buyer into the ladies' room; Oprah "Favorite Things" Nov 2000; $4M first-year sales; Blackstone majority
#   stake 2021 at $1.2B; all 750 employees got $10,000 cash + two first-class plane tickets.
#  How I Built This notes (davidsnotes): kept the idea private for a year; used a book on patents and trademarks; attorney had quoted $5,000, she paid $750;
#   paid people to buy it, moved it near the cash register.
#  Fortune (6 "unhinged" things): paid friends to buy Spanx at Neiman Marcus so it "wouldn't tank"; paid her own flight Atlanta->Dallas, 10 minutes;
#   snuck into stores and moved products to the registers; mailed Oprah a prototype + handwritten note; youngest self-made female billionaire (Forbes 2012).
#  Wikipedia: Danka; $750 patent attorney; Nov 2000 Oprah Favorite Things; $4M first year; Oct 2021 Blackstone at $1.2B; 750 employees, $10,000 + two
#   first-class tickets to any destination.
SERIES = "YOUR MOVE"; PART = 0; EP = 1
CBVOICES = {"a2": "usa_boss", "a5": "usa_young"}
LINES = [
    ("i1", "Why would anyone cut the feet off a pair of pantyhose?", 0.98, 0.25, +0.8, 1.5, ['Why', 'feet'], None),
    ("i2", "Because that one snip turned a fax machine saleswoman into a billionaire.", 0.98, 0.3, +0.6, 1.45, ['snip', 'billionaire.'], None),
    ("i3", "You're betting five grand of savings with no business experience, and you could lose it all.", 0.98, 0.2, +0.8, 1.5, ['betting', 'lose'], None),
    ("i4", "Here's how she won anyway, in five bold moves.", 0.98, 0.3, +0.8, 1.5, ['five', 'bold'], None),
    ("a1", "Meet Sara Blakely. She spent seven years selling fax machines, door to door.", 0.97, 0.2, +0.6, 1.45, ['seven', 'door'], None),
    ("a2", "Seven years with me? Honestly, I'd have quit too.", 0.97, 0.25, +0.2, 1.35, ['Seven', 'quit'], None),
    ("a3", "Getting ready for a party, she wanted to wear white pants, and nothing underneath looked smooth.", 0.97, 0.2, +0.6, 1.45, ['white', 'smooth.'], None),
    ("a4", "So she grabbed a pair of scissors, and cut the feet off her pantyhose.", 0.97, 0.25, +0.8, 1.5, ['scissors,', 'feet'], None),
    ("a5", "Snip, snip. You're welcome.", 1.0, 0.25, +1.2, 1.5, ['Snip,', 'welcome.'], None),
    ("a6", "It worked. And she wondered, why doesn't this exist?", 0.97, 0.3, +0.8, 1.5, ['worked.', 'exist?'], 'low'),
    ("b1", "Move one. She kept it secret for a whole year, and bet her savings on it.", 0.97, 0.2, +1.0, 1.5, ['secret', 'savings'], None),
    ("b2", "Five thousand dollars. That was everything.", 0.97, 0.3, +0.8, 1.5, ['Five', 'everything.'], None),
    ("b3", "But a patent lawyer quoted her about the same amount, just to file the idea.", 0.97, 0.25, +0.6, 1.45, ['same', 'file'], None),
    ("b4", "So, move two. She bought a book on patents, and wrote the application herself.", 0.97, 0.2, +0.8, 1.5, ['two.', 'herself.'], None),
    ("b5", "The lawyer only got seven hundred fifty bucks, to finish it.", 0.97, 0.3, +0.6, 1.45, ['seven', 'finish'], None),
    ("c1", "Move three was about a factory. Every hosiery maker she called brushed her off.", 0.97, 0.2, +1.0, 1.5, ['factory.', 'brushed'], None),
    ("c2", "So she drove to North Carolina and pitched them in person, door to door, like her old job.", 0.97, 0.25, +0.8, 1.45, ['drove', 'person,', 'old'], None),
    ("c3", "Still no. But about two weeks later, one owner called her back. He was in.", 0.97, 0.3, +0.6, 1.5, ['Still', 'in.'], None),
    ("d1", "Move four is the one people still talk about.", 0.97, 0.2, +1.0, 1.5, ['four', 'talk'], None),
    ("d2", "She paid for her own flight to Dallas, for a ten minute meeting with Neiman Marcus.", 0.97, 0.25, +0.6, 1.45, ['own', 'ten'], None),
    ("d3", "The buyer wasn't sold. So Sara walked her into the ladies' room, and showed her the before and after.", 0.97, 0.25, +0.8, 1.45, ["wasn't", "ladies'", 'after.'], None),
    ("d4", "The result? Spanx went into seven stores.", 0.97, 0.3, +0.8, 1.5, ['result?', 'seven'], None),
    ("e1", "The last move? Make sure it actually sells.", 0.97, 0.2, +1.0, 1.5, ['last', 'sells.'], None),
    ("e2", "She even paid her friends to go buy it, so it wouldn't flop.", 0.97, 0.2, +0.8, 1.45, ['friends', 'flop.'], None),
    ("e3", "Some days, she snuck into stores and moved Spanx right next to the cash registers.", 0.97, 0.25, +0.8, 1.5, ['snuck', 'registers.'], None),
    ("e4", "And she mailed Oprah a sample, with a handwritten note.", 0.97, 0.25, +0.6, 1.45, ['Oprah', 'handwritten'], None),
    ("e5", "That November, Oprah named Spanx one of her favorite things.", 0.97, 0.2, +0.8, 1.5, ['November,', 'favorite'], None),
    ("e6", "The first year brought in about four million dollars.", 0.97, 0.3, +0.8, 1.5, ['four'], None),
    ("f1", "And the fax machine saleswoman? Forbes later called her the youngest self-made female billionaire in the world.", 0.97, 0.3, +0.8, 1.5, ['youngest', 'billionaire'], None),
    ("f2", "Years later, an investment firm bought a majority stake. She gave every employee ten thousand dollars.", 0.97, 0.2, +0.6, 1.45, ['every', 'ten'], None),
    ("f3", "Plus two first-class plane tickets, anywhere in the world.", 0.97, 0.35, +0.8, 1.5, ['first-class', 'anywhere'], None),
    ("t1", "Notice the pattern? When nobody answered, she showed up. And she showed it working.", 0.97, 0.3, +0.8, 1.5, ['showed', 'working.'], None),
    ("g1", "Try it next time someone ignores your email. Show up, and let them see it work.", 0.97, 0.3, +0.8, 1.45, ['Show', 'see'], 'low'),
    ("z1", "Send this to the friend who's sitting on a great idea.", 1.0, 0.2, +1.0, 1.45, ['friend', 'great'], None),
    ("z2", "Would you have walked that buyer into the bathroom? Comment YES or NO.", 1.0, 0.0, +1.0, 1.45, ['bathroom?', 'YES'], None),
]
