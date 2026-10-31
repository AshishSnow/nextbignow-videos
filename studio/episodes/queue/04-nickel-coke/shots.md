# Storyboard — YOUR MOVE · EP 2 (The nickel Coke). One row per VO line; a shot changes every 2–3 s inside long lines.
Look: full-frame lit scenes (PLAYBOOK §6); hero = YOU in the boss's seat, 1950: `who={"base": "hero", "outfit": "suit"}` (orange
stays in the tie/pocket square — the face and colour are the IP), 1950s office set. Every frame graded via finish(). Music:
**1950s jukebox rock-and-roll / doo-wop** (new genre for the channel), a soda-fountain "fizz" riser on reveals; no "Oops" sting.
**No Coca-Cola trade dress**: no contour bottle, no script logo, no red disc, no red-and-white pairing — a plain straight green-glass
bottle with a plain cap and a cream "5¢" tag. The b2 vintage poster uses a plain serif, never anything like the script wordmark.
Real people = generic cast with role labels ("THE PRESIDENT", "TREASURY", "BOTTLER") — no likeness, no names in VO, no year on the
frame-1 label (the cold-open card on i2 sets 1950, as the pilot does).
New assets this episode needs (story-kit style, add to `template/anim_story.py`): set `office1950` (wood panelling, rotary phone,
venetian-blind light, a wall map of the US), set `soda_fountain` (chrome counter, stools), set `oval_office` (plain: desk, two flags
without insignia, tall windows), prop `bottle_el` (generic 6.5-oz straight bottle, `tag=` price), prop `vending_el` (1950s chest
cooler with a coin slot, `coin="5¢"`), prop `billboard_el` (roadside sign "5¢ · EVERYWHERE"), `coin_el` exists (anim_props) → add a
`coin_el(text="7½¢", ghost=True)` dashed "imaginary" variant, prop `contract_el` (long scroll with a seal), `memo_el` (typed memo
sheet). Reuse: `numcard_el` (roadmap 1–3), `flapboard` (year jumps), `hud_clock`, `quote_card`, `choice_card`, `cold_open`,
`series_badge`, `pin_el` + a US map for the 6¢/7¢/10¢ spread, `calendar_el`, `bars()`, `gavel_el`, `poster_el`.

| Line | Set / shot | Cast + acting | HUD / props / caption | SFX / camera |
|---|---|---|---|---|
| i1 "Why would a soda boss ask the President… for a brand-new coin?" | **oval_office WIDE, frame 1**: the hero in a suit holds up a giant dashed-outline coin "7½¢" to a generic President behind the desk (label "THE PRESIDENT") | hero hopeful, `expr="wow"`; President eyebrows up | `series_badge("YOUR MOVE", "EP 2 · THE NICKEL COKE")`; `say("A BRAND-NEW COIN?")` | coin "ting", slow push-in |
| i2 "It's nineteen fifty. You run Coca-Cola." | **office1950 MEDIUM**: hero at a big desk, rotary phone | turns to camera | `cold_open(f, "1950", "ATLANTA", "YOU: THE SODA BOSS")` | phone ring, clock tick |
| i3 "Every Coke costs a nickel. It has since eighteen eighty-six." | **soda_fountain** CU: a fountain glass (1886, sepia) → `bottle_el(tag="5¢")` (1950, colour), same price tag | an 1880s customer (sepia) → a 1950 customer | `say("5¢ SINCE 1886")` + chip "Levy & Young, J. Money, Credit & Banking, 2004" | cap pop |
| i4 "Sixty-four years. Two world wars. One price." | `flapboard` runs 1886 → 1950 while the 5¢ tag never moves; two plain "WAR" headlines flash past | — | `ui_word("ONE PRICE", "5¢", …)` | flap-flap, two booms |
| a1 "Your costs keep rising, but three traps keep that nickel stuck. The last is the coin in your pocket." | office: a rising `line_chart` (costs) behind three `numcard_el` cards 1–3; card 3 sits on the hero's jacket pocket | hero drums fingers | roadmap cards; `say("3 TRAPS")` | card slaps ×3 |
| b1 "Trap one. The ads." | street set, 1950: a `billboard_el("5¢ · EVERYWHERE")` above a diner | hero looks up | chip `TRAP #1 · THE ADS` | woodblock |
| b2 "For decades your ads said it in two words. Five cents. Everywhere." | `poster_el` vintage ad (plain serif) "5¢. Everywhere." → multiplies into a wall of posters | — | `quote_card(f, "5¢. Everywhere.", "Coca-Cola advertisement, 1908 (Young & Levy)")` | print stamps |
| b3 "Raise it, and a hundred and sixty thousand billboards are suddenly wrong." | highway WIDE: billboards to the horizon; a red "WRONG" stamp slams on each | hero `expr="sad"` | `say("160,000 BILLBOARDS")` + chip "1930s count — Young & Levy, Bar-Ilan WP 2013-06" (hold the chip ≥ 3 s) | stamp ×4, shake |
| c1 "Trap two. The bottlers." | bottling-plant set (conveyor of plain bottles) | a `worker` re-dressed (white shirt, brown apron, label "BOTTLER") | chip `TRAP #2 · THE BOTTLERS` | conveyor clank |
| c2 "You don't set the shop price. Eleven hundred independent bottlers do." | US map: 1,100 tiny bottle pins pop across the states | hero holds an empty price gun | `say("1,100 BOTTLERS SET THE PRICE")` | pops |
| c3 "Their contract dates from eighteen ninety-nine, and it never expires." | `contract_el` unrolls off the desk and out of frame; seal reads "1899"; a calendar page "NO END DATE" | hero tugs the scroll | `say("1899 · NO END DATE")` + chip "US District Court, 1920: 'permanent and perpetual'" | paper roll |
| c4 "Tell them what to charge, up or down, and regulators may call it price-fixing." | office: hero on the phone; a `gavel_el` shadow falls across the desk; two arrows ↑ ↓ both stamped | `expr="sweat"` | `say("PRICE-FIXING?")` + chip "1947 legal memo; Fortune, Jan 1951 (coercion charge) — via Young & Levy" | gavel knock |
| c5 "And already a hundred and twenty-five of them have broken ranks." | US map: 125 of the bottle pins turn red | hero winces | `say("125 OF 1,100 HAVE RAISED IT")` + chip "Young & Levy (by 1950)" | pops |
| d1 "Trap three. Your pocket." | hero CU, pulls one nickel from the pocket | smirk → frown | chip `TRAP #3 · YOUR POCKET` | coin clink |
| d2 "Four hundred thousand machines sell your Coke, and take only a nickel." | WIDE: a grid of `vending_el` coolers to the horizon, each slot stamped "5¢ ONLY" | — | `say("400,000 MACHINES · 5¢ ONLY")` + chip "Levy & Young 2004 / Emory Report 2001" | mechanical hum |
| d3 "But the next coin up is a dime: ten cents. So your smallest rise… is double." | CU coin slot: a dime ("10¢") hovers over the slot; the 5¢ tag flips to 10¢ | hero winces | `ui_word("SMALLEST RISE", "×2", …)` | coin drop, sting |
| d4 "Now New York breaks ranks: six cents a bottle." | US map: a crack runs from New York; pin "NEW YORK · 6¢" | hero watching the map | `pin_el` + chip "TIME, Dec 1950 (via Young & Levy)" | crack |
| d5 "Double the most famous nickel in America? Or gamble on a coin that doesn't exist?" | hero at the desk, two paths drawn on the wall map: DIME / COIN (the coin drawn dashed) | hand on chin, `look=(1,0)` | `hud_rule(f, 1, "ONE COIN = ONE PRICE")` | — |
| d6 "So in nineteen fifty-three you go to your friend. He runs the country." | `flapboard("1953")` → **oval_office** two-shot, hero + President shaking hands | President friendly, label "THE PRESIDENT" | `hud_clock(f, "1953", "WASHINGTON")` | door, footsteps |
| d7 "Your ask: mint a brand-new coin. Seven and a half cents." | CU: hero holds the dashed ghost coin "7½¢" up to the light | hopeful `expr="wow"` | `coin_el("7½¢", ghost=True)`; `say("7½¢")` | coin shimmer |
| o1 "He passes it to the Treasury. And the Treasury? Does not like the idea." | the coin drawing slides down a desk to an `exec` look labelled "TREASURY", who pushes it back | Treasury shakes head | `quote_card(f, "officials, who did not like the idea", "Coin World, 'The Coke coin', reporting Levy & Young 2004")` | paper slide, thud |
| o2 "Without a coin, the nickel breaks town by town. Six cents, seven, a dime." | US map: pins 6¢ / 7¢ / 10¢ pop across states | hero watching | `say("6¢ · 7¢ · 10¢")` + chip "Business Week, 1955 (via Young & Levy)" | pops |
| o3 "By nineteen fifty-nine, the nickel Coke is gone." | `flapboard` 1955 → 1959; the 5¢ tag on the bottle fades out | — | `say("1959: THE NICKEL COKE IS GONE")` | flaps, fade |
| t1 "One idea never left the memo: every ninth bottle, empty." | office night: a `memo_el` under a desk lamp; a `vending_el` row where bottle #9 is see-through | hero reads, eyebrow up | `say("EVERY 9TH BOTTLE: EMPTY")` + chip "company memos, per NPR Planet Money ep. 416 — never used" | lamp click |
| t2 "Some people pay twice. Average, five point six cents." | customer at the cooler gets an empty bottle, drops a second nickel; a calculator shows 5.6¢; a red "NEVER USED" stamp | customer `expr="sus"` | `ui_word("AVERAGE PRICE", "5.6¢", …)` | clink ×2, stamp |
| k1 "A price that never moves? Check the size." | takeaway card: a "$1 menu" sign, a bottle that shrinks while its tag stays | hero points at the bottle size | `say("FIXED PRICE? CHECK THE SIZE")` | ding |
| e1 "Dime or coin? Comment DIME or COIN." | **end card**: hero centre in the 1950 office, a dime left, the ghost coin right | to camera | `choice_card(f, "YOUR MOVE", "DIME", "COIN", y≈1410)` + `series_badge` | choice whoosh |
| e2 "Send this to the friend who moans about prices." | end card holds; phone "SEND THIS" | hero points at camera | — | — |

Loop: the last frame dissolves to the hero holding the ghost coin up to the President (frame 1).
Post copy: first line "A Coke cost 5 cents for 73 years — and the boss asked the President for a 7½-cent coin." · series line
"Your Move · Ep 2" · firstCommentText "DIME or COIN — what would you have done in 1953?" · YouTube title "Coke Cost 5¢ for 73 Years. Why? | Your Move"
(≤ 50 chars → check). Sponsor slot (BRAND.md §4): the takeaway line (a budgeting/price-tracking app, 8–15 s), never the hook.
