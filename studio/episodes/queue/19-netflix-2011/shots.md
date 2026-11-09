# shots — HOW THEY GOT SO BIG · EP 3* (whiteboard; one drawn idea per row; renumber the EP at build)
Look: `nbnkit/board.py`, reference `examples/southwest-turn` (BIG on the whiteboard, `topline` "MOVE n OF 2") + `examples/dropship-30day`
(`relabel()` + `stepmap()`). Held object: ONE red envelope (`envelope_m`, text "DVD") that becomes a screen (`tv_m`) by the end — the company's
whole story in one prop. Mini map: `stepmap(c, 2, active, done)` under the pill = the two moves (price split, Qwikster).
Props written 9 Nov (R&D): `disc_m` (DVD disc), `tv_m` (screen + play triangle) — lab sheet `lab/story_kit/props_9nov.jpg`. `envelope_m` draws a plain outline: hatch it red (`hatch(..., RD)`) at build so it reads as *the* red envelope. Existing: `envelope_m`, `mailbox_m`, `tag_m`, `quote_m`,
`arrow_m`, `cross`, `stamp_m`, `heads_m`, `laptop_m`, `calendar_m`, `gov_m` not needed.
Opening move (frame 0 already drawn, STORY §2b): a red `envelope_m` "DVD" half out of a `mailbox_m`; above it a big red "−800,000" already written,
a small arrow from the envelope to a faint dashed `tv_m` outline; the envelope rocks, pen hovers over a "?" — nothing starts blank.
Music: 2011-ish indie pop on uke + glock, dips under the "Oops."; SFX: marker squeak, paper envelope slide (rows 1, 16), cash-register "ding" (row 4),
record scratch (row 9, the Oops), stock-ticker blips (row 12), eraser wipes.
Safety: no Netflix logo, wordmark, red-and-black trade dress or fonts (plain handwritten "NETFLIX"; the envelope is a generic red envelope);
no Twitter/X logo (an "@" speech bubble, "NAME TAKEN"); the handle owner is never shown, named or described. Hastings appears only as a quote card
"REED HASTINGS, NETFLIX CEO · BLOG, 18 SEP 2011" — the hero (NBN stick rig, orange scarf) plays the seat, never his likeness. Members figure =
"MEMBERS IN THE US" (the letter's domestic count). No investment angle: the share drop is a 2011 event, no ticker symbol, no advice.

| Row | Line(s) | Drawing (what the pen draws while the voice says it) | Caption (small / BIG) | Chip / SFX |
|---|---|---|---|---|
| 1 | i1 | frame 0 as above; the "−800,000" gets a red underline; a tiny calendar strip JUL–SEP 2011 is drawn under it | "netflix once lost" / 800,000 MEMBERS | US MEMBERS, END JUN → END SEP 2011 · NETFLIX Q3 2011 LETTER |
| 2 | i2 | the arrow from the envelope to the screen gets two red marks on it: a price tag `tag_m` "$" and a blank name sticker "???"; slow zoom → toward the sticker | "it did that to" / ITSELF | — |
| 3 | i3 | eraser wipe; hero at a desk with a plain sign NETFLIX (handwritten) and "2011"; a stack of red envelopes; coins flow from the stack to the desk | "you're running it" / 2011 | — |
| 4 | i4 | the dashed `tv_m` outline on the right of the board; an arrow from the envelopes to it; `stepmap(2)` appears under the pill with two empty boxes; a red "?" on the arrow | "two moves to get there" / FAST | — |
| 5 | a1 | pill "MOVE 1 OF 2"; one plan card "STREAMING + 1 DVD" is torn in two with a zig-zag marker line | "july" / SPLIT THE PLAN | NETFLIX PRESS RELEASE, 12 JUL 2011 |
| 6 | a2 | the whole card gets a tag `tag_m` "$9.99 / MONTH"; a red envelope + a small play triangle pop onto the card → "1 DVD + STREAMING" | "before" / $9.99 | OLD PLAN: UNLIMITED STREAMING + 1 DVD AT A TIME (TNW, 12 JUL 2011) |
| 7 | a3 | the two halves get their own tags "$7.99" + "$7.99"; the pen draws a "+" and "= $15.98"; a red "+60%" arrow climbs off the tag (ding) | "want both?" / $15.98 | NEW PRICE FOR EXISTING MEMBERS FROM 1 SEP 2011 |
| 8 | a4 | three small stick heads (`heads_m`) with angry eyebrows pop up beside the tags; `stepmap` ticks box 1; box 2 blinks | "and move two" / HASN'T HAPPENED | — |
| 9 | b1 | pill "MOVE 2 OF 2"; `quote_m` card: "I messed up. I owe everyone an explanation." — REED HASTINGS, NETFLIX CEO, BLOG, 18 SEP 2011; the hero (in the seat) rubs his neck | "september" / I MESSED UP | QUOTE: HASTINGS BLOG POST, 18 SEP 2011 (AS REPRINTED BY BUZZFEED / HOME MEDIA MAGAZINE) |
| 10 | b2 | the red envelope slides away from the screen; a wall is drawn between them; the envelope side gets its own little laptop page (`laptop_m`) and its own bill | "the dvd side gets" / ITS OWN NAME | — |
| 11 | b3 | the blank name sticker from row 2 is filled in: big handwritten QWIKSTER on the envelope (`relabel()` style rub + rewrite) | "the new name" / QWIKSTER | — |
| 12 | b4 | a plain "@" speech bubble drawn on the right: "@QWIKSTER" with a red stamp `stamp_m` "TAKEN" | "on twitter, that name was" / TAKEN | NBC NEWS, SEP 2011: THE @QWIKSTER ACCOUNT ALREADY BELONGED TO SOMEONE ELSE |
| 13 | b5 | **Oops beat** (`oops_beat`, the hero's reaction, once): the hero turns to camera, hand on forehead; red "OOPS." stamp; record scratch | — / OOPS. | — |
| 14 | b6 | `calendar_m` flips from 18 SEP to 10 OCT, pen writes "22 DAYS"; the QWIKSTER sticker is crossed out (`cross`); the wall is erased so the envelope sits with the screen again | "in other words" / NO QWIKSTER | NETFLIX BLOG, 10 OCT 2011: "DVDS WILL BE STAYING AT NETFLIX.COM" (VIA ENGADGET / CONSUMERIST) |
| 15 | c1 | the $15.98 tag from row 7 is still there, circled; a clipboard "THE COUNT" slides in | "but the price split" / STAYS | — |
| 16 | c2 | the "−800,000" from frame 0 is redrawn big under the clipboard; the stick heads leave the board one by one (envelope slide SFX) | "gone by september" / −800,000 | US MEMBERS 24.59M → 23.79M · Q3 2011 SHAREHOLDER LETTER (8-K, 24 OCT 2011) |
| 17 | c3 | a hand-drawn line chart falls off a cliff; pen writes "−35%" and "IN ONE DAY" (ticker blips) | "the next day, shares fell" / 35% | CNN MONEY, 25 OCT 2011 · 2011 EVENT, NOT INVESTMENT ADVICE |
| 18 | c4 | the hero looks at the falling line, then at the camera, one eyebrow up; the $15.98 tag gets a small eraser hovering over it, then the eraser is pulled away | "honestly?" / SCRAP THE PRICE TOO? | — |
| 19 | d1 | `quote_m`: "What we misjudged was how quickly to move there." — NETFLIX Q3 2011 LETTER TO SHAREHOLDERS; then zoom → out: the arrow from the envelope to the screen is redrawn solid | "instead" / HOW QUICKLY | Q3 2011 SHAREHOLDER LETTER, 24 OCT 2011 |
| 20 | d2 | two words on the arrow: "WHERE ✓" (green tick) and "HOW FAST ✗" (red); the arrow keeps going to the screen | "not where" / HOW FAST | — |
| 21 | d3 | `tv_m` drawn solid at last, play triangle hatched red; pen writes "300M+" above it, "END OF 2024" under | "paid members" / 300 MILLION+ | NETFLIX Q4 2024 LETTER (21 JAN 2025): 301.6M · IT STOPPED REPORTING THE COUNT IN 2025 |
| 22 | d4 | the red envelope drops into the `mailbox_m` one last time; a `disc_m` beside it; pen writes "LAST ONES: 29 SEP 2023" and "5 BILLION+ DISCS" | "the red envelopes" / LAST ONES OUT | NETFLIX (SARANDOS), 18 APR 2023 · DISC COUNT: CBS LA / THEWRAP, 2023 |
| 23 | t1 | eraser wipe; one new price tag `tag_m` with a speech bubble "WHY?" drawn *before* the tag; pen writes "SAY WHY FIRST" | "raising a price?" / SAY WHY FIRST | LETTER: "OUR LACK OF EXPLANATION ABOUT THE RISING COST…" |
| 24 | z1, z2 | KEEP and SPLIT pills under a small `disc_m`, each circled in turn; "SAVE THIS" underlined; the envelope still rocking in the mailbox | "split off what pays the bills?" / KEEP OR SPLIT? → SAVE THIS | COMMENT ONE WORD · EDUCATION ONLY |
