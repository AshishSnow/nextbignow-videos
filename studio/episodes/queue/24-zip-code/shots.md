# shots — HOW IT WORKS · EP 8* (whiteboard; one drawn idea per row; renumber the EP at build)
Look: `nbnkit/board.py`, reference `examples/cash-rewards` + `examples/childminding` (copy its anim_shots.py: `rs`/`topline`/pill, `set_boil`, colour `spot()` per row, then swap the rows).
Held object: ONE card-terminal screen (`zippad_m`, prompt "ZIP CODE?", five boxes) bottom-left, and ONE little house (`house_m`) top-right; between them
a winding `road_m` that grows through thing 1 (a third on a2, reaching the door on a5 — the broker lookup), turns orange in thing 2 (the court calls the ZIP
personal info) and gets red barriers `cross` in thing 3 (where the two states' laws stop). The road IS the story: five digits → a front door. Mini map: `stepmap(c, 3, active, done)` under the pill = the three things
(1 YOUR NAME · 2 THE COURT · 3 THE LIMITS), colour spots BLUE / ORANGE / RED by thing.
Props written 14 Nov (R&D): `zippad_m` (five boxes; digits typed one by one; `hot=` makes the boxes glow red), `road_m` (dashed road drawn on from a to b),
`gaspump_m` (plain pump, "ZIP?" on its screen). Lab sheet `lab/story_kit/props_14nov.jpg`.
Existing: `terminal_m`, `house_m`, `card_m`, `stepmap`, `spot`, `quote_m`, `court_m`, `gavel_m`, `laptop_m`, `folder_m`, `cash_m`, `truck_m`, `cross`, `stamp_m`,
`magnifier_m`, `heads_m`, `pin_m`, `arrow_m`, `say`.
Opening move (frame 0 already drawn, STORY §2b): `zippad_m` with "9 0 2 1 _" already typed (the 5th box blinking, the pen hovering over it), the dashed road
already running from the pad to the house with a red `pin_m` on the door; a red "?" pulsing over the house — nothing starts blank. The digits are a made-up
example (chip "EXAMPLE ZIP").
Music: bright marimba + pizzicato with a light ticking hi-hat (new genre for HIW; ticking = typing); SFX: keypad beeps on each digit (rows 1–2), marker squeak,
gavel knock (row 13), cash-register "ding" (row 15), eraser wipes between things.
Safety: no store, data broker or card network named or drawn (no logos, no card brand marks — the card says "CARDHOLDER NAME"); what the stores did in both
cases is the shoppers' claim (on screen: "HER CLAIM"), never a finding; the court quotes are on quote cards with the court + year; two states only, credit
cards only, cash/delivery/gas-pump/download carve-outs said aloud; education only, not legal advice (chip row 1 + end card).

| Row | Line(s) | Drawing (what the pen draws while the voice says it) | Caption (small / BIG) | Chip / SFX |
|---|---|---|---|---|
| 1 | i1 | frame 0 as above; the 5th digit "0" types in (beep), the dashed road flashes orange from pad to door, the red pin bounces on the house | "your ZIP at checkout" / → YOUR DOOR? | EXAMPLE ZIP · EDUCATION ONLY · NOT LEGAL ADVICE |
| 2 | i2 | eraser wipe of the road; hero (NBN stick rig) at a `till_m` holding a `card_m`; the `zippad_m` pops up big on the counter, boxes empty, cursor blinking | "at the register" / 5 DIGITS | — |
| 3 | i3 | a row of `heads_m` (9 little heads) all wearing the same "90210" badge; the pen writes "SO WHAT?" with a shrug line | "lots of people share one" / HARMLESS? | — |
| 4 | i4 | `stepmap(3)` draws on under the pill; box 3 gets a tiny red barrier with "2 STATES"; the pad and house slide to their held places, road not drawn yet | "three things" / BEFORE YOU TYPE | — |
| 5 | a1 | thing 1 active (blue spot); the `card_m` zooms in: the pen underlines "CARDHOLDER NAME"; an arrow from the card to the pad | "it's on your card" / YOUR NAME | — |
| 6 | a2 | the `heads_m` row shrinks from 9 to 2 as a `magnifier_m` sweeps over it; the road draws its first third | "add a ZIP code" / HOW SMALL? | — |
| 7 | a3 | `folder_m` labelled "FTC · DATA BROKERS · MAY 2014" drops in; the pen writes "p. 24" on its tab | "a 2014 report" / DATA BROKERS | FTC, "DATA BROKERS: A CALL FOR TRANSPARENCY AND ACCOUNTABILITY" (MAY 2014), P. 24 |
| 8 | a4, a5 | a little shop icon (off the road, top-left) sends an envelope labelled "NAME + STORE'S OWN ZIP" to a box labelled "BROKER · 2014"; a second envelope comes back labelled "ADDRESS" and lands on the house (the road reaches the door) | "name + store's ZIP" / → ADDRESS | FTC (2014): "THE CLIENT PROVIDES A CUSTOMER'S NAME AND A STORE'S ZIP CODE, AND THE DATA BROKER PROVIDES THE CUSTOMER'S ADDRESS" |
| 9 | a6 | the pen circles "STORE'S" on the first envelope twice in red; hero turns to camera, eyebrows up | "not even yours" / THE STORE'S ZIP | — |
| 10 | b1 | thing 2 active (orange spot); eraser wipe; a `court_m` labelled "CALIFORNIA" draws on; a girl figure (stick rig, purple dress) walks up its steps | "a California shopper" / SUED | — |
| 11 | b2 | flashback bubble: the girl at a plain till, the `zippad_m` filling with digits (beeps); label on the shop "HOME GOODS CHAIN" (no name) | "she said the register asked" / HER ZIP | — |
| 12 | b3 | in the bubble: a `laptop_m` titled "MATCH" draws a line from "NAME" + "ZIP" to a little house; a yellow sticker "HER CLAIM" is slapped on the bubble | "her claim" / → HER ADDRESS | PINEDA (CAL. SUPREME COURT, 2011): ALLEGED IN THE COMPLAINT, TAKEN AS TRUE ON APPEAL |
| 13 | b4 | "ZIP = PERSONAL INFO?" pops; `gavel_m` knocks (knock SFX); the pen writes "YES · 2011" on the court's steps | "California's top court" / YES | — |
| 14 | b5 | `quote_m`: "a ZIP code constitutes 'personal identification information'" — CALIFORNIA SUPREME COURT, 2011; the five pad boxes glow red (`zippad_m(..., hot=t)`) | "during a credit card sale" / BREAKS THE LAW | PINEDA, 51 CAL.4TH 524: "REQUESTING AND RECORDING A CARDHOLDER'S ZIP CODE, WITHOUT MORE, VIOLATES THE CREDIT CARD ACT" |
| 15 | b6 | two `cash_m` notes pop by the court: "UP TO $250" (first time), then "UP TO $1,000" (each time after), register ding | "the penalty" / UP TO $1,000 | CAL. CIV. CODE § 1747.08(e): CIVIL PENALTY "NOT TO EXCEED" $250 FIRST, $1,000 EACH LATER VIOLATION |
| 16 | b7 | camera slides right: a second `court_m` "MASSACHUSETTS" draws on beside the first, the pen writes "2013" and a green tick | "Massachusetts too" / 2013 | TYLER, 464 MASS. 492 (MASS. SUPREME JUDICIAL COURT, 11 MAR 2013) |
| 17 | c1 | thing 3 active (red spot); eraser wipe back to the held pad → road → house; three red `cross` barriers wait, undrawn, beside the road | "where it stops" / THE LIMITS | — |
| 18 | c2 | the `card_m` gets a green tick and "CREDIT"; a `cash_m` note slides in and gets a red cross "NOT COVERED" | "credit cards only" / CASH? NO | — |
| 19 | c3 | `truck_m` labelled "DELIVERY" drives along the road to the house (horn tap); the house gets a green tick "OK TO ASK · CALIFORNIA" | "want it delivered?" / OK TO ASK | § 1747.08(c)(4): SHIPPING, DELIVERY, SERVICING, INSTALLATION, SPECIAL ORDERS |
| 20 | c4 | `gaspump_m` draws on beside the road, "ZIP?" on its screen; a small shield with a red-crossed card "STOLEN" pops beside it | "California allows it" / FRAUD CHECK | § 1747.08(c)(3)(B) (ADDED 2011) · FLORES v. CHEVRON (CAL. CT. APP. 2013) |
| 21 | c5 | a small plain outline map: only two pins coloured (CA, MA); the rest of the outline gets a dashed "?" ; the pen writes "YOUR STATE?" | "two states" / LOOK UP YOUR STATE | ALSO NOT COVERED IN CALIFORNIA: DOWNLOADS BOUGHT ONLINE (APPLE v. SUPERIOR COURT, 2013) |
| 22 | d1 | back to frame 0's picture: card name + the five digits → the full orange road → the pin on the door, all lit at once | "so yes" / 5 DIGITS → A DOOR | — |
| 23 | t1 | hero at the till; the pad says "ZIP CODE?"; a cashier figure behind the counter; a blue speech bubble from the hero: "WHAT'S IT FOR?" → then the pen draws a green tick and "YOUR CALL" beside the pad | "when it asks" / ASK WHAT FOR | — |
| 24 | z1 | end card: SAVE pill; two pills "GIVE IT" (green) / "SAY NO" (red) under the pad; "?" pulses → then the two pills swing like a scale, one after the other | "five digits at the register" / GIVE IT or SAY NO? | EDUCATION ONLY · NOT LEGAL ADVICE |
| 25 | z2 | the pad's five boxes fill on their own while the hero looks away (no-look typing); "SEND THIS" arrow → a little friend figure | "send this to" / THE NO-LOOK TYPER | — |
