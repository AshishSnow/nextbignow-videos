# shots — HOW IT WORKS · EP 7 (whiteboard; one drawn idea per row; renumber the EP at build)
Look: `nbnkit/board.py`, reference `examples/credit-board` + `examples/cash-rewards` (copy its anim_shots.py: `rs`/`topline`/pill, colour `spot()` per row, then swap the rows).
Held object: ONE plane (`plane_m`, 10 windows = the seats) with a live counter under the pill: `tally(c, v, label="TICKETS SOLD", fmt="{:.0f}")`
running 100 → 110 in the first 1.6 s (frame-0 move; the pill's label reads "EXAMPLE": no source says airlines oversell by 10 %), then the extra red stick passengers (`extra=`) queue beside the plane. The `stepmap(c, 3, …)`
mini map carries the three things (1 empty seats · 2 volunteers · 3 the law), colour spots coded BLUE / ORANGE / RED by thing.
Props written 12 Nov (R&D): `plane_m`, `boardpass_m`, `gatedesk_m` (+ existing `tally`, `stepmap`, `spot`, `cash_m`, `coin_m`, `stamp_m`,
`clock_m`, `grid100_m`, `gov_m`, `memo_m`, `heads_m`). Lab sheet: `lab/story_kit/props_12nov.jpg`.
Opening move (frame 0 already drawn, STORY §2b): `boardpass_m` (seat 12C) big in the centre with a red `stamp_m` "BUMPED" already landing,
a fare tag "$300" beside it and "× 4 ?" being written by the pen; the plane small behind, windows all hatched — nothing starts blank.
Music: bright airport-lounge swing on uke + vibraphone (new genre for the channel); SFX: marker squeak, "ding-dong" gate chime (row 2), cash
register (row 7), stamp (row 9), eraser wipes between things.
Safety: no airline logos, liveries or colours (plain "AIRLINE"; the plane is a generic outline; flight "OB 261" is made up); Delta named in
plain text only on the memo card (an AP report, past tense, a positive fact); no airline ranked or blamed; DOT numbers say "reporting
airlines"; education only, not legal advice; the $400 in row 15 is a hypothetical ("SAY THEY OFFER…").

| Row | Line(s) | Drawing (what the pen draws while the voice says it) | Caption (small / BIG) | Chip / SFX |
|---|---|---|---|---|
| 1 | i1 | frame 0 as above; "× 4 ?" finishes and is circled; a stack of four $300 tags fans out under the pass | "bumped in America?" / 4× YOUR FARE | EDUCATION ONLY · NOT LEGAL ADVICE · US RULES, INVOLUNTARY BUMPS |
| 2 | i2 | eraser wipe; hero (NBN stick rig) holding the pass at a `gatedesk_m` "GATE 12"; the desk's bubble pops "VOLUNTEERS?" (chime) | "you're at the gate" / FULL FLIGHT | — |
| 3 | i3 | `plane_m` big (10 windows hatched = full); the tally under the pill ticks TICKETS SOLD 100 → 110 (EXAMPLE); two red stick passengers queue at the steps | "more tickets than seats" / ON PURPOSE | MADE-UP NUMBERS |
| 4 | i4 | `stepmap(3)` draws on under the pill; three numbered boxes, the 3rd gets a small gavel and "US LAW" | "three things" / THE LAST ONE PAYS | — |
| 5 | a1 | thing 1 active (blue spot); ONE of the ten windows goes empty (hatch rubbed out), a dashed stick figure walks away from the plane | "why sell a seat twice?" / NO-SHOWS | — |
| 6 | a2 | `grid100_m`-style 10×10 bookings grid; one row of ten fades to dashed outlines; pen writes ≈ 1 IN 10 | "no-shows can average" / ~1 IN 10 | GAO-20-191 (DEC 2019), CITING ACADEMIC LITERATURE: "ABOUT 10 PERCENT OF FINAL PRE-DEPARTURE BOOKINGS" |
| 7 | a3 | the empty window gets a red "$0"; then an extra ticket stub slides in beside the plane, the tally ticks to 110 | "empty seats earn nothing" / SELL EXTRA | — |
| 8 | b1, b2 | thing 2 active (orange spot); every window hatched + the extra passengers pop in at the steps → the gate desk bubble pops "VOLUNTEERS FIRST" → a blank cheque slides in with "NO LEGAL LIMIT" on the amount line | "volunteers first" / NO LEGAL LIMIT | 14 CFR 250.2b (VOLUNTEERS FIRST) · 250.5(g) (CARRIERS MAY PAY MORE) |
| 9 | b3, b4 | "HOW HIGH?" pops by the cheque → `memo_m` slides in, labelled "DELTA MEMO · 2017" → two lines written on it: "GATE AGENTS: UP TO $2,000" and "SUPERVISORS: UP TO $9,950" (the second circled, register SFX) | "one airline's memo, 2017" / $9,950 | ASSOCIATED PRESS VIA CBS MIAMI, 14 APR 2017 (INTERNAL MEMO) |
| 10 | c1, c2 | thing 3 active (red spot); nobody's hand goes up; the pass gets a `stamp_m` "BUMPED"; a `clock_m` appears next to it with "NEW FLIGHT LANDS…" and "MINIMUM" over the cheque | "US law sets the minimum" / BUMPED | — |
| 11 | c3 | the clock's hand sweeps 0 → 1 h; a zero drawn in the window | "lands within an hour" / $0 | 14 CFR 250.5(a) |
| 12 | c4, c5 | the hand sweeps to 2 h; a bar "2× FARE" draws on; a lid line "MAX $1,075" caps it | "1–2 h late, US flights" / 2× FARE | 14 CFR 250.5 (CAPS SINCE 22 JAN 2025: $1,075 / $2,150) |
| 13 | c6, c7 | the hand passes 2 h; the bar doubles to "4× FARE"; lid "MAX $2,150" | "over 2 hours" / 4× FARE | INTERNATIONAL FROM THE US: 1–4 H = 2×, 4 H+ = 4× |
| 14 | c8 | `cash_m` and a cheque slide in under the bar (cash register SFX) | "owed as" / CASH OR CHECK | 14 CFR 250.8 (CASH OR AN IMMEDIATELY NEGOTIABLE CHECK) |
| 15 | e1, e2 | eraser wipe; two plain boxes EU and UK; under EU a distance line short / medium / long with €250 · €400 · €600 written on in turn; under UK "TOP £520" | "EU, by distance: up to" / €600 | YOUR EUROPE (EU REG. 261/2004), MOD. 21 SEP 2026 · UK CAA: £220 / £350 / £520 |
| 16 | d1, d2 | eraser wipe; a long row of tiny `heads_m` people, one red among them, the pen writes "1 IN 36,000" | "bumped against their will" / 1 IN 36,000 | DOT AIR TRAVEL CONSUMER REPORT, FEB 2026: 2025, REPORTING AIRLINES, 24,596 OF 891M PASSENGERS |
| 17 | d3 | twelve green stick people with a hand up appear beside the one red one; "×12" written | "volunteers" / 12× MORE | SAME REPORT: 290,413 VOLUNTARY |
| 18 | d4 | hero at the gate tilts his head toward the desk, one ear cupped; a little "$?" over him | "honestly?" / HEAR THE OFFER | — |
| 19 | t1 | the hero's hand half up, two sticky notes pop on the desk "THE OFFER?" and "LANDS WHEN?" | "before you raise your hand" / ASK 2 THINGS | — |
| 20 | z1, z2 | under the plane: CASH and SEAT pills, each circled in turn; "SAVE THIS" underlined; a "SAY: $400 + FLY TOMORROW" note; the tally still ticking 110 | "they offer you $400" / CASH OR SEAT? → SAVE THIS | COMMENT ONE WORD · EDUCATION ONLY |
