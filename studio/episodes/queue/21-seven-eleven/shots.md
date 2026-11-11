# shots — HOW THEY GOT SO BIG · EP 5* (whiteboard; one drawn idea per row; renumber the EP at build)
Look: `nbnkit/board.py`, reference `examples/netflix-2011` (BIG on the whiteboard: `stepmap` + `tally` + `relabel`) and `examples/southwest-turn`.
Held object: ONE little store (`shopfront_m`, label "7-ELEVEN", awning hatched **BLU**, never orange/green/red stripes) with an owner tag under it
that `relabel()`s through the story: DALLAS → (license) TOKYO → DALLAS, CHAPTER 11 → TOKYO 70% → TOKYO 100%. Mini map: `stepmap(c, 3, active, done)`
under the pill = the three moves (license, rebuild, buy). Live counter: `tally(c, v, label="OWNED IN TOKYO", fmt="{:.0f}%")` — reads 100 % in frame 0,
drops to 0 % on i3 (back to 1973), climbs to 70 % on d1 and 100 % on d2 (the frame-0 move + the middle's re-hook).
Props written 11 Nov (R&D): `ice_m` (ice block), `riceball_m` (onigiri), `truck_m` (delivery truck, label + drive offset), `sunglasses_m` (+ red tag),
`manual_m` (binder; open_ swings the cover to an empty page with a red "?") — lab sheet `lab/story_kit/props_11nov.jpg`.
Existing: `shopfront_m`, `relabel`, `stepmap`, `tally`, `quote_m`, `stamp_m`, `calendar_m`, `clock_m`, `coinpile_m`, `chart_drop_m`, `pin_m`, `heads_m`, `cross`,
`arrow_m`, `receipt_m`, `laptop_m`, `tag_m`.
Opening move (frame 0 already drawn, STORY §2b): the store with "7-ELEVEN" on its sign; a dashed arrow from a small pin "DALLAS" (left) to a pin "TOKYO"
(right) with the owner tag "OWNER: TOKYO" already written; `tally` 100 % pulsing; the pen hovers over a red "?" — nothing starts blank.
Music: bright uke + glock with a soft koto-like pluck colour from a1 (no cultural pastiche, no gongs); dips under c4 "Bankruptcy."; SFX: marker squeak,
ice clink (row 5), cash-register "ding" (row 12, first sale), truck horn tap (row 16), stamp thump (row 20), eraser wipes.
Safety: no 7-Eleven logo, wordmark styling, or orange-green-red stripes (plain handwritten "7-ELEVEN" on the sign); no Seven & i / Ito-Yokado logos
(the dove), no Couche-Tard logo; no national flags. Suzuki appears only as a quote card "TOSHIFUMI SUZUKI, WHO LED THE PROJECT · SEVEN & i HOLDINGS"
— the hero (NBN stick rig, orange scarf) plays the seat (an Ito-Yokado planner), never his likeness; John Jefferson Green and the Thompson family are
named in the voice only, never drawn as likenesses. The 1987 buyout is told as what the records say (to stop a hostile takeover), not mocked;
no "Oops" beat (nobody's blunder is on record). IPO: an event, no ticker, no investment angle.

Fresh-eyes review 11 Nov: the counter and row 1 say OWNED IN TOKYO (a company), never 'Japan owns' (no 1990s 'Japan buys America' framing); the koto-like pluck stays subtle.

| Row | Line(s) | Drawing (what the pen draws while the voice says it) | Caption (small / BIG) | Chip / SFX |
|---|---|---|---|---|
| 1 | i1 | frame 0 as above; the pen underlines "OWNER: TOKYO" in red; the dashed arrow DALLAS → TOKYO turns solid | "america's 7-eleven is" / OWNED IN TOKYO | SEVEN & i HOLDINGS (TOKYO): 7-ELEVEN, INC. WHOLLY OWNED SINCE NOV 2005 |
| 2 | i2 | a tiny desk calendar flips page after page beside a phone with "NO REPLY"; the pen writes "1 YEAR+" | "once couldn't get" / A MEETING | — |
| 3 | i3 | eraser wipe of the calendar and phone; `tally` drops 100 → 0 %; pin TOKYO grows; hero at a desk with a sign "ITO-YOKADO · SUPERMARKETS" and "1973" | "you work in tokyo" / 1973 | — |
| 4 | i4 | `stepmap(3)` appears under the pill with three empty boxes; a long dashed arrow from a tiny "MEETING?" note to the store with "OWNER: YOU?" | "three moves to" / OWN IT ALL | — |
| 5 | i5 | pin DALLAS; a `calendar_m` "1927"; `ice_m` drawn next to the store (ice clink) | "where it started" / AN ICE COMPANY | BRITANNICA · HANDBOOK OF TEXAS (TSHA) |
| 6 | i6 | milk bottle, egg box and bread loaf pop one by one onto the ice block | "off the ice dock" / MILK, EGGS, BREAD | IDEA OF EMPLOYEE JOHN JEFFERSON GREEN, 1927 (ENCYCLOPEDIA.COM COMPANY HISTORY) |
| 7 | i7 | `clock_m` with a wedge from 7 to 11; the store sign is rubbed out (`relabel`) "TOTE'M" → "7-ELEVEN"; pen writes "1946" | "named after its hours" / 7 AM TO 11 PM | BRITANNICA: RENAMED 1946 "TO CALL ATTENTION TO THEIR EXTENDED HOURS" |
| 8 | a1 | pill "MOVE 1 OF 3"; `stepmap` box 1 blinks; a license card (`card_m`) with "LICENSE · JAPAN" and an empty signature line | "move one" / GET THE LICENSE | — |
| 9 | a2 | a speech bubble from the DALLAS pin "SOUTHLAND: NOT INTERESTED"; a `calendar_m` flips pages; pen writes "1 YEAR+" | "just to start talks" / 1 YEAR+ | SEVEN & i: SOUTHLAND "HAD NO INTEREST IN ENTERING THE JAPANESE MARKET" |
| 10 | a3 | a row of `heads_m` around the hero, 99 of 100 shaking (red "X" over the row); `quote_m`: "99% of people opposed the idea" — TOSHIFUMI SUZUKI, WHO LED THE PROJECT  then zoom → onto the quote card | "at home?" / 99% SAID NO | QUOTE: SEVEN & i HOLDINGS, SUZUKI MEMORIAL PAGE (2026) |
| 11 | a4 | the hero looks at the one head that said yes, then at the camera, shrugs; pen circles one of the "no" heads and writes "ME" | "honestly?" / I'D SAY NO TOO | — |
| 12 | a5 | the store is redrawn at the TOKYO pin, owner tag `relabel` "DALLAS" → "TOKYO (LICENSE)"; `sunglasses_m` with red tag "FIRST SALE" (ding); "MAY 1974"; `stepmap` ticks box 1 | "the first sale?" / SUNGLASSES | JAPAN TIMES, 17 MAY 2024 · FIRST STORE: TOYOSU, TOKYO |
| 13 | b1 | pill "MOVE 2 OF 3"; a thick `manual_m` "MANUAL" lands; the hero swings the cover open (open_ 0 → 1) | "move two" / FIND THE SECRET | — |
| 14 | b2 | the open binder shows ruled pages and a big red "?" where the secret should be; pen writes "NO SECRET" | "there" / ISN'T ONE | SEVEN & i: THE TEAM "COULD FIND NO 'SECRET'" |
| 15 | b3 | eraser wipe of the binder; a small ledger stays ("ACCOUNTING ✓" in green); pen writes "BUILD IT OURSELVES" across a blank page | "apart from the accounting" / BUILD IT ALL | SEVEN & i: ALL BUT THE ACCOUNTING SYSTEM |
| 16 | b4 | three drawings land one after another: `riceball_m` (1978), `truck_m` "MILK" with several small labels on the box, rolls right → (horn tap), a till with a little screen and a `receipt_m` printing (1983) | "made for your shelves" / RICE BALLS | SEVEN & i: OWN RICE BALLS 1978 · COMBINED DELIVERY 1980 · POS 1983 |
| 17 | b5 | two stacks of tiny store icons grow side by side: TOKYO pin (taller) vs DALLAS pin "US + CANADA"; pen writes "MID-1990s"; `stepmap` ticks box 2 | "by the mid-nineties" / JAPAN HAS MORE | SOUTHLAND 10-K, END 1995: 6,269 IN JAPAN VS 5,986 IN THE US + CANADA |
| 18 | c1 | pill "MOVE 3 OF 3"; camera pans → back to the DALLAS pin; the original store there, the owner tag reads "DALLAS" | "back in dallas" / THE OTHER WAY | — |
| 19 | c2 | `calendar_m` "1987"; a tiny house labelled "FAMILY" pulls the store under its roof; a shadow hand "TAKEOVER BID" bumps off a drawn wall | "to stop a takeover" / GOING PRIVATE | HANDBOOK OF TEXAS (TSHA): BUYOUT TO FEND OFF A HOSTILE TAKEOVER |
| 20 | c3 | a `coinpile_m` grows under the store with a red "$5 BILLION" tag; pen writes "BORROWED" and hatches most of the pile red | "about" / $5 BILLION | AP, 7 MAR 1991: "$5 BILLION" LEVERAGED BUYOUT |
| 21 | c4 | `calendar_m` "OCT 1990"; `stamp_m` "CHAPTER 11" on the owner tag (stamp thump); music drops out → then a small envelope "RESCUE PLAN" already pinned to the tag, from the TOKYO side | "october 1990" / BANKRUPTCY | SOUTHLAND 10-K (SEC): CHAPTER 11, OCT 1990 · AP: A "PREPACKAGED" PLAN, AGREED WITH THE JAPANESE BUYERS IN 1990 |
| 22 | d1 | the TOKYO store's hero walks over the arrow to the DALLAS store; `tally` 0 → 70 %; owner tag `relabel` "DALLAS" → "TOKYO 70%"; a `tag_m` "$430 MILLION" | "march 1991" / 70% FOR $430M | SOUTHLAND 10-K: ~70 % TO ITO-YOKADO + SEVEN-ELEVEN JAPAN, $430M CASH, 5 MAR 1991 |
| 23 | d2 | a small rising line "PROFIT '93" beside the store; `calendar_m` flips 1991 → 2005; `tally` 70 → 100 %; owner tag `relabel` → "TOKYO 100%"; `stepmap` ticks box 3 | "fourteen years later" / ALL OF IT | SEVEN & i: BACK IN PROFIT 1993 · SEVEN-ELEVEN JAPAN TENDER OFFER, 9 NOV 2005 |
| 24 | d3 | the two stacks from row 16b come back, now labelled: TOKYO "≈22,000", DALLAS "US + CANADA ≈12,700"; the icons pop up one at a time | "today, japan has" / ≈22,000 STORES | SEVEN & i CORPORATE OUTLINE 2026: JAPAN 21,927 (FEB 2026) · 7-ELEVEN, INC. US + CANADA 12,712 (DEC 2025) |
| 25 | t1 | eraser wipe; a license card (`card_m`) passed from one stick hand to another, with a magnifier on the partner's notebook "WHAT ARE THEY LEARNING?" | "licensing abroad?" / CHECK WHAT THEY LEARN | OUR TAKEAWAY FROM THIS STORY · EDUCATION ONLY |
| 26 | z1, z2 | LICENSE and KEEP pills under the little store, each circled in turn; "SAVE THIS" underlined; `riceball_m` rocking on the counter | "your idea, abroad?" / LICENSE OR KEEP? → SAVE THIS | COMMENT ONE WORD |
