# shots — HOW THEY GOT SO BIG · EP 6* (whiteboard; one drawn idea per row; renumber the EP at build)
Look: `nbnkit/board.py`, reference `examples/seven-eleven` (BIG on the whiteboard: `stepmap` + `tally` + `relabel`/`ownertag`) and `examples/childminding` (`set_boil`).
Held object: ONE open pizza box (`pizza_m`) centre-low, with a yellow `sticky_m` complaint stuck on the inside of the lid that gets rubbed out and rewritten
(`relabel`) through the story: "LIKE CARDBOARD" → "NEW RECIPE" (row 14) → "ON TV" (row 18) → "+14.3%" (row 21). The pizza itself changes: `sad=True` (pale, flat) until b4, then
`garlic=True` with a red sauce hatch. Mini map: `stepmap(c, 3, active, done)` under the pill = the three moves (LISTEN · FIX · AIR IT).
Live counter: `tally(c, v, label="US SAME-STORE SALES", fmt="{:+.1f}%")` — reads +14.3 % in frame 0, drops to −4.9 % on i4 (label "· 2008"), stays there through
the moves, then climbs to +14.3 % on d2 (the frame-0 move + the middle's re-hook). Colour spots: BLUE (listen) / ORANGE (fix) / RED (air it).
Props written 14 Nov (R&D): `pizza_m` (open box, sad/garlic pizza, optional lid word), `ketchup_m` (plain squeeze bottle) — lab sheet `lab/story_kit/props_14nov.jpg`.
Existing: `tv_m`, `sticky_m`, `relabel`, `stepmap`, `tally`, `spot`, `quote_m`, `heads_m`, `calendar_m`, `chart_drop_m`, `risingline`, `yearcard`, `stamp_m`,
`shopfront_m`, `pin_m`, `say` (no cheese prop: b3 is three written counters).
Opening move (frame 0 already drawn, STORY §2b): a `tv_m` playing, on its screen the pale pizza box with the sticky "LIKE CARDBOARD" already written; the
`tally` reads +14.3 % and pulses; the pen hovers over a red "?" between the TV and the counter — nothing starts blank.
Music: bright uke + upright-bass walking line with a soft brush kit (diner feel, new genre for BIG); dips to near-silence under a3–a5 (the complaints), lifts
on b4 (new recipe); SFX: marker squeak, TV click-on (row 1, 14), oven "ding" (row 10), stamp thump (row 18), eraser wipes.
Safety: no Domino's logo, domino tile, blue/red trade dress or uniforms — the box is plain white with no marks, "DOMINO'S" only as plain handwritten text on
the pill/labels; Patrick Doyle appears only as a quote card "PATRICK DOYLE · PRESIDENT, DOMINO'S USA (IN THE DEC 2009 AD)", never drawn as a likeness —
the hero (NBN stick rig, orange scarf) plays the seat (someone at head office), not Doyle. The complaints are customers' words from the ads (quote cards with
the source), not our verdict on the food. The "Oops." is the hero's reaction to the tape, the company itself aired it. No stock price, no "record for fast food".

| Row | Line(s) | Drawing (what the pen draws while the voice says it) | Caption (small / BIG) | Chip / SFX |
|---|---|---|---|---|
| 1 | i1 | frame 0 as above; TV click-on; a speech bubble from the TV pops "LIKE CARDBOARD" in red; the pen circles it | "real customers on TV" / "CARDBOARD" | SLATE (11 JAN 2010) · MEDIAPOST (DEC 2009) |
| 2 | i2 | the pen writes "ON PURPOSE" with an arrow to the TV; the `tally` +14.3 % flashes green | "on purpose" / SALES JUMPED | — |
| 3 | i3 | eraser wipe; `yearcard` "2008"; hero (NBN stick rig, white shirt) at a desk in a plain building labelled "HEAD OFFICE · MICHIGAN"; a `pin_m` on it | "you work at head office" / 2008 | — |
| 4 | i4 | `chart_drop_m` draws a falling line labelled "2008"; the `tally` drops +14.3 → −4.9 % and its label reads "US SAME-STORE SALES · 2008"; the pen writes "≈ −5%" | "this year" / SALES −5% | DOMINO'S 2008 RESULTS (24 FEB 2009): US SAME-STORE SALES (4.9)% · SAME STORES = OPEN BOTH YEARS |
| 5 | i5 | `stepmap(3)` draws on under the pill: LISTEN · FIX · AIR IT; box 3 gets a little red "!?" | "three moves" / THE LAST ONE'S SCARY | — |
| 6 | a1 | move 1 active (blue spot); hero puts on big headphones; the pill reads "MOVE 1 OF 3" | "move one" / LISTEN | — |
| 7 | a2 | a long table of `heads_m` (7 heads, mixed hair colours) around the pale pizza box (`pizza_m`, `sad=True`); speech bubbles start popping, empty | "real customers" / FOCUS GROUPS | DOMINO'S (16 DEC 2009) · AP (11 JAN 2010): FOCUS GROUPS |
| 8 | a3 | one bubble fills: `quote_m` "Domino's pizza crust to me is like cardboard" — A CUSTOMER IN THE ADS; a scrap of cardboard is drawn next to the crust | "the crust" / LIKE CARDBOARD | SLATE, "LIKE CARDBOARD" (11 JAN 2010) |
| 9 | a4 | a second bubble: `quote_m` "The sauce tastes like ketchup." — A CUSTOMER IN THE ADS; `ketchup_m` pops beside the box | "the sauce" / LIKE KETCHUP | SLATE (11 JAN 2010) |
| 10 | a5 | hero turns to camera, sweat drop; `oops_beat` stamp "OOPS." + sting | — / OOPS. | — |
| 11 | b1 | move 2 active (orange spot); the pen circles the pale pizza in green and labels three arrows "CRUST", "SAUCE", "CHEESE" (sticky stays "LIKE CARDBOARD" until row 14) | "move two" / FIX THE PIZZA ITSELF | — |
| 12 | b2 | `calendar_m` flips 24 pages quickly; the pen writes "≈ 2 YEARS" | "Domino's says" / ~2 YEARS OF TESTS | DOMINO'S PRESS RELEASE (16 DEC 2009): "OVER A TWO-YEAR PERIOD" |
| 13 | b3 | three counters write on one by one under the box: "CHEESES: DOZENS" · "SAUCES: 15" · "CRUST SEASONINGS: ~50" (each with a tick); oven ding | "dozens, 15, ~50" / TEST EVERYTHING | DOMINO'S (16 DEC 2009): "DOZENS OF CHEESES, 15 SAUCES, AND NEARLY 50 CRUST SEASONING BLENDS" |
| 14 | b4 | "WHAT WINS?" pops; the pizza redraws: `garlic=True` (green herb ticks on the crust), red sauce hatch, a small tag "+ PROVOLONE" on the cheese; sticky → "NEW RECIPE" | "garlic, sweeter sauce, provolone" / NEW PIZZA | DOMINO'S (16 DEC 2009): GARLIC-SEASONED CRUST · SWEETER, BOLDER SAUCE · MOZZARELLA WITH "A HINT OF PROVOLONE" |
| 15 | c1 | move 3 active (red spot); the hero's knees knock; the pen writes "OLD PIZZA = BAD" on a big card and holds it up to a TV camera drawn in outline | "move three" / SAY IT WAS BAD | — |
| 16 | c2 | `yearcard` "DEC 2009"; the `tv_m` clicks on: inside it the old pale box with the CARDBOARD and KETCHUP bubbles playing → then zoom into the TV as a red "ON AIR" light blinks | "Dec 2009, on TV" / THE COMPLAINTS | MEDIAPOST: TV SPOTS UNVEILED 28 DEC 2009; NEW PIZZA IN STORES 27 DEC |
| 17 | c3 | inside the TV: three little chef figures (white hats) watching a smaller screen, hands on faces; the pen writes "MORTIFIED — SLATE" | "chefs watch the tapes" / MORTIFIED | SLATE (11 JAN 2010): "MORTIFIED DOMINO'S CHEFS" |
| 18 | c4, c5 | the TV zooms; `quote_m`: "There comes a time when you know you've got to make a change." — PATRICK DOYLE · PRESIDENT, DOMINO'S USA (IN THE DEC 2009 AD); sticky → "ON TV" (stamp thump) | "on camera" / MAKE A CHANGE | MEDIAPOST (DEC 2009) |
| 19 | c6 | the hero, pen hovering over a "SIGN OFF?" line on a form, hand shaking (squiggly signature) | "honestly?" / SCARY | — |
| 20 | d1 | eraser wipe; `yearcard` "MAY 2010"; an envelope "FIRST NUMBERS" lands on the desk; the `tally` starts to wobble | "did it work?" / MAY 2010 | — |
| 21 | d2 | `risingline` draws up steeply; the `tally` climbs −4.9 → +14.3 % and its label changes to "US SAME-STORE SALES · JAN–MAR 2010"; the sticky → "+14.3%" (green) | "Jan–Mar 2010, US" / +14.3% | DOMINO'S Q1 2010 RESULTS (4 MAY 2010): "DOMESTIC SAME STORE SALES GREW 14.3%" |
| 22 | d3 | a tiny grey bar "Q1 2009: +1.0%" draws next to the tall green bar | "a year earlier" / +1% | SAME RELEASE, TABLE: Q1 2009 +1.0% |
| 23 | d4 | `quote_m`: "A remarkably better pizza, and our honesty in how we told consumers about it, is paying off" — PATRICK DOYLE, CEO, MAY 2010; two ticks: "BETTER PIZZA" · "HONESTY" | "he credits" / PIZZA + HONESTY | DOMINO'S (4 MAY 2010) · CEO FROM MARCH 2010 (8-K, 5 JAN 2010) |
| 24 | e1 | eraser wipe; a `yearcard` "2025"; a grid of tiny plain boxes draws on (no growth animation from one box — no 2009 store count is sourced); the pen writes "22,000+ STORES" and "90+ MARKETS" | "today" / 22,000+ STORES | DOMINO'S FY2025 RESULTS (23 FEB 2026): 22,142 STORES · "OVER 90 MARKETS" |
| 25 | t1 | a phone with a review bubble "TOO DRY" → the hero writes "YOU'RE RIGHT" under it → a box with a green tick "FIXED: …" | "if they're right" / SAY IT FIRST | — |
| 26 | z1 | end card: SAVE pill; two pills "AIR IT" (green) / "HIDE IT" (red) under the box; "?" pulses | "your product gets slammed" / AIR IT or HIDE IT? | EDUCATION ONLY |
| 27 | z2 | a calendar page "FRIDAY" with a pizza box on it; "SEND THIS" arrow → a friend figure | "send this to" / THE FRIDAY PIZZA FRIEND | — |
