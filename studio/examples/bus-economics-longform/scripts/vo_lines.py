# (id, text, speed, pause_after, base_semitones, range_expand, stressed_words, ending)
# OopsMyBusiness LONG-FORM 16:9 (15 Nov 2026): "The Economics of Owning a Bus Business" — US + Europe version, idea from the owner's reference
# (Hindi bus-business case study). Vintage-comic editorial look, American narrator, no music. Target 8-10 min.
# Facts (2+ sources each unless noted):
#  ABA Foundation 2025 Motorcoach Census: 49,543 US motorcoaches, 1,769 US companies (buses.org news + census PDF)
#  new coach price: Metro Mag 2017 "around $500,000 to $550,000"; Metro Mag (Indian Trails) "$600,000 per bus"; financing 5-7 years (Metro 2017)
#  charter: Starr Tours guide $115-195/hr, $1,600-2,500/day; Fash.com $100-190/hr, $1,000-1,800/day
#  Germany limited long-distance buses to protect rail until 2013 (The Local 2014; Wikipedia); Flix: 3 childhood friends, partners own buses +
#   employ drivers, Flix does brand/booking/routes/marketing, "like Uber" (Sifted); keeps ~25% (Bus & Motorcoach News citing reports) / 25-30%
#   (Productmint); bought Greyhound Oct 2021 (FirstGroup RNS 21 Oct 2021; Route One); 2023: 81M passengers, >EUR 2bn revenue, adj. EBITDA
#   EUR 104M = 5.2% margin (Route One; Bus & Coach Buyer)
#  diesel: EIA $6.127/gal (10 Nov 2026, via FleetOwner) / AAA $6.157; coach ~6 mpg example (Citizen Daily Post 6.1 avg; 6-9 cruising)
#  BLS OOH: median bus driver (transit + intercity) $59,050 (May 2025); P endorsement required
#  ABAF/Metro Feb 2023: 21.4% gap between drivers needed and employed
#  FMCSA: $5,000,000 insurance for 16+ passenger vehicles; interstate operating authority
#  NHTSA final rule (2013): seat belts on new motorcoaches built from Nov 2016 (transportation.gov; STN)
#  EU Reg 561/2006: 9 h daily driving (10 h twice a week), 45-min break after 4.5 h; tachograph (legislation.gov.uk; europa.eu)
SERIES = "OOPS ECONOMICS"; PART = 0; EP = 1
CBVOICES = {}
LINES = [
    # --- hook
    ("h1", "Right now, somewhere on a highway, about fifty people are asleep on a night bus.", 0.97, 0.15, +0.6, 1.45, ['highway,', 'asleep'], None),
    ("h2", "Headphones on, seats back. Nobody is thinking about money.", 0.97, 0.2, +0.6, 1.45, ['Nobody', 'money.'], None),
    ("h3", "Except one person. The owner.", 0.97, 0.3, +0.8, 1.5, ['one', 'owner.'], 'low'),
    ("h4", "Because that bus can cost more than a house, and every mile eats cash.", 0.97, 0.2, +0.8, 1.45, ['house,', 'cash.'], None),
    ("h5", "So is owning buses actually a good business?", 0.97, 0.25, +0.8, 1.5, ['actually', 'business?'], None),
    ("h6", "Today we do the math.", 0.97, 0.1, +0.8, 1.5, ['math.'], None),
    ("h6b", "What a bus costs, how it earns, and where the money leaks.", 0.97, 0.2, +0.8, 1.45, ['costs,', 'leaks.'], None),
    ("h7", "And why Europe's top long-distance bus brand grew without owning buses.", 0.97, 0.35, +0.8, 1.5, ['top', 'without'], None),
    # --- 1. the machine
    ("a1", "Let's start with the machine itself.", 0.97, 0.15, +0.8, 1.5, ['machine'], None),
    ("a2", "A full-size intercity coach, the kind with fifty-plus seats, is not cheap.", 0.97, 0.2, +0.6, 1.45, ['fifty-plus', 'cheap.'], None),
    ("a3", "Brand new, you're looking at more than half a million dollars.", 0.97, 0.2, +0.8, 1.5, ['new,', 'half'], None),
    ("a4", "One American operator paid about six hundred thousand per bus.", 0.97, 0.25, +0.6, 1.45, ['six', 'per'], None),
    ("a5", "Most owners don't pay cash. They finance it, often over five to seven years.", 0.97, 0.2, +0.6, 1.45, ["don't", 'finance'], None),
    ("a6", "So before a single passenger climbs on, there's a big payment due every month.", 0.97, 0.25, +0.8, 1.45, ['single', 'every'], None),
    ("a7", "Used coaches cost far less. That's how many small operators get started.", 0.97, 0.2, +0.6, 1.45, ['Used', 'small'], None),
    ("a8", "And there are more of these out there than you'd think.", 0.97, 0.1, +0.6, 1.45, ['more', 'think.'], None),
    ("a8b", "Nearly fifty thousand motorcoaches, in the US alone.", 0.97, 0.15, +0.8, 1.5, ['fifty', 'alone.'], None),
    ("a9", "And fewer than two thousand companies run all of them.", 0.97, 0.2, +0.6, 1.45, ['fewer', 'companies.'], None),
    ("a10", "So this isn't one giant's game. Most bus companies run fewer than ten coaches.", 0.97, 0.3, +0.8, 1.45, ["isn't", 'ten'], 'low'),
    # --- 2. how a bus makes money
    ("b1", "Now the fun part. How does a bus actually make money?", 0.97, 0.2, +0.8, 1.5, ['fun', 'money?'], None),
    ("b2", "There are three main ways, and each one carries a very different risk.", 0.97, 0.25, +0.8, 1.45, ['three', 'risk.'], None),
    ("b3", "Way number one. Charter.", 0.97, 0.15, +1.0, 1.5, ['one.', 'Charter.'], None),
    ("b4", "A school trip, a wedding, or a company retreat rents the whole bus.", 0.97, 0.2, +0.6, 1.45, ['wedding,', 'whole'], None),
    ("b5", "Pricing guides put a full-size coach at a hundred-plus dollars an hour.", 0.97, 0.2, +0.6, 1.45, ['hundred', 'hour.'], None),
    ("b6", "A full day can easily run past a thousand dollars.", 0.97, 0.2, +0.8, 1.5, ['day', 'thousand'], None),
    ("b7", "The upside? The customer pays for the whole bus, full or empty.", 0.97, 0.2, +0.8, 1.5, ['upside?', 'empty.'], None),
    ("b8", "The catch? You have to keep finding the next customer, every single week.", 0.97, 0.3, +0.8, 1.45, ['catch?', 'next'], None),
    ("b9", "Way number two. Your own scheduled route.", 0.97, 0.15, +1.0, 1.5, ['two.', 'route.'], None),
    ("b10", "You pick two cities, set a timetable, and sell seats one by one.", 0.97, 0.2, +0.6, 1.45, ['timetable,', 'seats'], None),
    ("b11", "When the bus is full, it's great money.", 0.97, 0.15, +0.8, 1.5, ['full,', 'great'], None),
    ("b12", "When it's half empty, you still pay for the whole trip.", 0.97, 0.15, +0.6, 1.45, ['half', 'whole'], None),
    ("b12b", "Fuel doesn't care who's on board.", 0.97, 0.3, +0.8, 1.5, ["doesn't", 'board.'], None),
    ("b13", "Way number three. Contracts.", 0.97, 0.15, +1.0, 1.5, ['three.', 'Contracts.'], None),
    ("b14", "A university shuttle, an airport run, or a company moving its workers every day.", 0.97, 0.2, +0.6, 1.45, ['university', 'workers'], None),
    ("b15", "Often you're paid for the bus's time, full or not.", 0.97, 0.2, +0.8, 1.45, ['hour', 'not.'], None),
    ("b16", "Less upside per trip, but much less risk. That's the steady money.", 0.97, 0.3, +0.8, 1.45, ['less', 'steady'], 'low'),
    # --- 3. the Flix twist
    ("c1", "And then there's a fourth way. Let someone else sell your seats.", 0.97, 0.25, +0.8, 1.5, ['fourth', 'else'], None),
    ("c2", "To see how that works, we need to take a little trip to Germany.", 0.97, 0.15, +0.8, 1.5, ['Germany.'], None),
    ("c3", "Until twenty thirteen, the country limited long-distance buses to protect its railway.", 0.97, 0.2, +0.6, 1.45, ['limited', 'railway.'], None),
    ("c4", "When that rule changed, three childhood friends were ready. Their first buses ran within weeks.", 0.97, 0.2, +0.8, 1.45, ['friends', 'weeks.'], None),
    ("c4b", "And they weren't alone. Within a year, the number of intercity bus routes nearly tripled.", 0.97, 0.2, +0.6, 1.45, ['alone.', 'tripled.'], None),
    ("c4c", "Prices crashed. Some bus fares were about half the train price.", 0.97, 0.2, +0.8, 1.45, ['crashed.', 'half'], None),
    ("c4d", "In a few years, one startup bought or merged with its biggest rivals.", 0.97, 0.3, +0.8, 1.5, ['one', 'rivals.'], None),
    ("c5", "Their company was called FlixBus, and here's the twist that made it work.", 0.97, 0.1, +0.8, 1.5, ['FlixBus,', 'twist'], None),
    ("c5b", "They barely owned any buses.", 0.97, 0.25, +0.8, 1.5, ['barely', 'buses.'], None),
    ("c6", "Local bus companies own the coaches and employ the drivers.", 0.97, 0.15, +0.6, 1.45, ['own', 'drivers.'], None),
    ("c7", "Flix plans the routes, sets the prices, runs the app, and sells the tickets.", 0.97, 0.2, +0.8, 1.45, ['routes,', 'tickets.'], None),
    ("c8", "Then it keeps a cut of each ticket. Reports put it around a quarter.", 0.97, 0.25, +0.8, 1.45, ['cut', 'quarter.'], None),
    ("c9", "Think of it like Uber, but for intercity buses.", 0.97, 0.3, +0.8, 1.5, ['Uber,', 'buses.'], None),
    ("c10", "For the bus owner, that means selling seats without running their own marketing.", 0.97, 0.2, +0.6, 1.45, ['selling', 'marketing.'], None),
    ("c11", "For Flix, it means growing fast without buying whole fleets.", 0.97, 0.25, +0.8, 1.45, ['fast', 'fleets.'], None),
    ("c12", "In twenty twenty-one, Flix even bought Greyhound, the famous American bus line.", 0.97, 0.25, +0.8, 1.5, ['Greyhound,', 'American'], None),
    ("c12b", "That deal brought in about thirteen hundred Greyhound vehicles.", 0.97, 0.15, +0.6, 1.45, ['thirteen', 'vehicles.'], None),
    ("c12c", "So the company that grew without owning buses suddenly owned a fleet.", 0.97, 0.25, +0.8, 1.45, ['suddenly', 'fleet.'], None),
    ("c13", "In twenty twenty-three, it carried about eighty-one million passengers.", 0.97, 0.15, +0.6, 1.45, ['eighty-one', 'passengers.'], None),
    ("c14", "Revenue passed two billion euros.", 0.97, 0.2, +0.8, 1.5, ['two', 'euros.'], None),
    ("c15", "Now the part people miss. Its adjusted profit margin was only about five percent.", 0.97, 0.2, +0.8, 1.45, ['miss.', 'five'], None),
    ("c16", "And that's before interest, taxes, and buses slowly wearing out.", 0.97, 0.2, +0.6, 1.45, ['before', 'wearing'], None),
    ("c17", "Even the giant of the industry lives on thin margins.", 0.97, 0.35, +0.8, 1.45, ['giant', 'thin'], 'low'),
    # --- 4. where the money goes
    ("d1", "So let's follow the money on one long trip, and see where it goes.", 0.97, 0.2, +0.8, 1.45, ['follow', 'goes.'], None),
    ("d2", "Bill number one is fuel. The one that never stops.", 0.97, 0.2, +0.8, 1.5, ['fuel.', 'never'], None),
    ("d3", "Say your coach gets around six miles per gallon on the highway.", 0.97, 0.15, +0.6, 1.45, ['six', 'highway.'], None),
    ("d4", "A five-hundred-mile run burns more than eighty gallons of diesel.", 0.97, 0.2, +0.6, 1.45, ['eighty', 'diesel.'], None),
    ("d5", "And right now, US diesel averages over six dollars a gallon.", 0.97, 0.2, +0.6, 1.45, ['six', 'gallon.'], None),
    ("d6", "Do the math. That's around five hundred dollars of fuel, one way.", 0.97, 0.3, +0.8, 1.5, ['five', 'one'], None),
    ("d7", "Bill number two. The driver.", 0.97, 0.15, +1.0, 1.5, ['two.', 'driver.'], None),
    ("d8", "The typical US transit and intercity bus driver earns about fifty-nine thousand a year.", 0.97, 0.2, +0.6, 1.45, ['fifty-nine', 'year.'], None),
    ("d9", "And good drivers have been hard to find.", 0.97, 0.15, +0.8, 1.5, ['hard'], None),
    ("d10", "One recent industry survey found about one in five needed drivers missing.", 0.97, 0.25, +0.6, 1.45, ['one', 'missing.'], None),
    ("d11", "Bill number three. Insurance.", 0.97, 0.15, +1.0, 1.5, ['three.', 'Insurance.'], None),
    ("d12", "Run a bus built for sixteen or more, and the feds demand big insurance.", 0.97, 0.15, +0.6, 1.45, ['sixteen', 'serious'], None),
    ("d13", "At least five million dollars of liability.", 0.97, 0.25, +0.8, 1.5, ['five', 'liability.'], None),
    ("d14", "Then come tires, brakes, repairs, a place to park it, and the loan payment.", 0.97, 0.2, +0.6, 1.45, ['tires,', 'loan.'], None),
    ("m1", "Let's put it together with a rough, made-up example. Easy numbers.", 0.97, 0.2, +0.8, 1.45, ['made-up', 'Easy'], None),
    ("m2", "Fifty seats, forty dollars a ticket, every seat sold.", 0.97, 0.15, +0.6, 1.45, ['Fifty', 'every'], None),
    ("m3", "That's two thousand dollars for the trip.", 0.97, 0.2, +0.8, 1.5, ['two', 'trip.'], None),
    ("m4", "If a booking platform keeps a quarter, you're down to fifteen hundred.", 0.97, 0.2, +0.6, 1.45, ['quarter,', 'fifteen'], None),
    ("m5", "Take out about five hundred for fuel, and maybe a few hundred for the driver.", 0.97, 0.2, +0.6, 1.45, ['five', 'driver.'], None),
    ("m6", "You're left with roughly seven hundred, before the loan, insurance, and repairs.", 0.97, 0.25, +0.8, 1.45, ['seven', 'before'], None),
    ("m7", "Not bad. Now picture the exact same trip, with only half the seats sold.", 0.97, 0.2, +0.8, 1.5, ['bad.', 'half'], None),
    ("m8", "The fuel and the driver cost you exactly the same as before. Profit? Basically gone.", 0.97, 0.3, +0.8, 1.45, ['exactly', 'gone.'], None),
    ("m9", "That's the whole business in one sentence. Empty seats are where the money disappears.", 0.97, 0.35, +0.8, 1.45, ['whole', 'Empty'], 'low'),
    ("d15", "And here's the scary part. A bus sitting in the yard still costs money.", 0.97, 0.2, +0.8, 1.45, ['scary', 'still'], None),
    ("d16", "The loan, the insurance, and the parking keep running, even when it earns nothing.", 0.97, 0.25, +0.6, 1.45, ['keep', 'nothing.'], None),
    ("d17", "So owners obsess over one thing. Keep the bus moving, and the seats full.", 0.97, 0.35, +0.8, 1.45, ['moving,', 'full.'], 'low'),
    # --- 5. the rules
    ("e1", "Now, the paperwork. You can't just buy a bus and start driving.", 0.97, 0.2, +0.8, 1.45, ['paperwork.', "can't"], None),
    ("e2", "In the US, you need federal operating authority to carry passengers across state lines.", 0.97, 0.2, +0.6, 1.45, ['state', 'authority.'], None),
    ("e3", "Every driver needs a commercial license with a passenger endorsement.", 0.97, 0.2, +0.6, 1.45, ['commercial', 'passenger'], None),
    ("e4", "And since late twenty sixteen, new motorcoaches have had to come with seat belts.", 0.97, 0.25, +0.6, 1.45, ['new', 'belts.'], None),
    ("e5", "Europe has its own rulebook.", 0.97, 0.15, +0.8, 1.5, ['Europe', 'own'], None),
    ("e6", "A coach driver can usually drive nine hours a day.", 0.97, 0.15, +0.6, 1.45, ['nine', 'day.'], None),
    ("e7", "After four and a half hours behind the wheel, they need a break. Forty-five minutes.", 0.97, 0.2, +0.8, 1.45, ['break.', 'Forty-five'], None),
    ("e8", "And a little box called a tachograph records all of it.", 0.97, 0.25, +0.8, 1.45, ['tachograph', 'all'], None),
    ("e9", "These rules cost owners time and money. They also keep passengers safe.", 0.97, 0.3, +0.6, 1.45, ['cost', 'safe.'], 'low'),
    # --- 6. the verdict
    ("f1", "So, is owning buses a good business?", 0.97, 0.25, +0.8, 1.5, ['good', 'business?'], None),
    ("f2", "The upside? People always need to travel, and one bus moves a lot of them.", 0.97, 0.2, +0.8, 1.45, ['upside?', 'travel,'], None),
    ("f3", "For a lot of trips, a coach ticket costs less than flying or driving alone.", 0.97, 0.25, +0.6, 1.45, ['less', 'alone.'], None),
    ("f4", "The catch? Big money up front, thin margins, and one empty month really hurts.", 0.97, 0.2, +0.8, 1.45, ['catch?', 'hurts.'], None),
    ("f5", "And when too many buses chase one route, fares can drop fast.", 0.97, 0.25, +0.6, 1.45, ['too', 'fast.'], None),
    ("f6", "Honestly? The winners aren't always the ones with the most buses.", 0.97, 0.2, +0.8, 1.5, ['Honestly?', 'most'], None),
    ("f7", "They're the ones who keep every bus busy.", 0.97, 0.35, +0.8, 1.5, ['every', 'busy.'], 'low'),
    # --- 7. how you'd start
    ("g1", "So if you wanted in, how would you start? Three moves.", 0.97, 0.2, +0.8, 1.5, ['start?', 'Three'], None),
    ("g2", "One. Start with one good used coach, not a shiny new fleet.", 0.97, 0.2, +0.8, 1.45, ['used', 'shiny'], None),
    ("g3", "Two. Lock in contracts first. Steady hours are what pay the loan.", 0.97, 0.2, +0.8, 1.45, ['contracts', 'loan.'], None),
    ("g4", "Three. Plug into a booking network instead of building your own app.", 0.97, 0.2, +0.8, 1.45, ['network', 'own'], None),
    ("g5", "And know your cost per mile before you sign anything.", 0.97, 0.3, +0.8, 1.45, ['cost', 'anything.'], 'low'),
    # --- ending
    ("z1", "So next time you're half asleep on a night bus, think about the owner.", 0.97, 0.2, +0.6, 1.45, ['night', 'owner.'], None),
    ("z2", "While you're dreaming, they're doing math.", 0.97, 0.35, +0.8, 1.5, ['dreaming,', 'math.'], 'low'),
    ("z3", "Send this to the friend who keeps saying, I should just buy a bus.", 1.0, 0.2, +1.0, 1.45, ['friend', 'bus.'], None),
    ("z4", "Tell me in the comments. Would you rather own the buses, or the app?", 1.0, 0.0, +1.0, 1.45, ['buses,', 'app?'], None),
]
