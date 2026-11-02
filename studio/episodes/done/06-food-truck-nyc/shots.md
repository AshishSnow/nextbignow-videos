# Storyboard — HOW TO START · EP 3 · Food truck in New York City. Look: LINE-ART CAST (anim_stick.py, STORY.md 2b): hero = orange-tie beginner
(add a white paper cap `{"base": "hero", "style": "cap", "cap": (255, 255, 255)}` from step 2 on — `style` is needed, `cap` alone draws nothing), mentor = `girl` re-coloured `{"base": "girl", "shirt": (0, 150, 140), "hair": (40, 30, 30)}`
(teal apron shirt — a veteran truck owner, the expert voice of the steps), permit holder = `exec` with a grey tie `{"base": "exec", "tie": (150, 152, 160)}`
(a generic "PERMIT HOLDER", never a real person; shown neutral, not villainous), city inspector = `worker` with a navy cap `{"base": "worker", "cap": (30, 50, 110)}`.
**New in this episode (inauthentic-content guard, BRAND.md §2):** first city-specific how-to; the steps are told in the *order you must do them*
(person → base → truck → permit) with the twist that the order matters; first "good news" twist (a rule change that helps the viewer, verified on the
city's own page) instead of a warning; the mystery in the hook (why rent a $200 permit for thousands?) is paid off by the cap in step 4.
Music: **doo-wop street-corner score** (built 2 Nov; boom-bap was already used, PLAYBOOK §7), a truck-horn honk on every STEP card. No Oops beat (no blunder; the
cap is told as a fact of law). NYC-only (said in i2 and on the frame-1 card). No real truck brands, no city seal/logo, no NYC Health logo
(plain text "CITY HEALTH DEPT." chip only).

**BUILD BRIEF: all 3 assets WRITTEN 2 Nov (same R&D run, `template/scripts/anim_props5.py`, in anim.py's exec list; `board_check --strict` PASS, 0 missing;
lab frames `lab/story_kit/storyboard_foodtruck_ep3.py` + `.jpg`, 0.04–0.33 s/frame).** Placement notes from the lab sheet: (1) i1 — captions at y≈620 / 740
(at 560 the first touches the cold-open card), the permit card as its own `comp(permit_el(≥ 360))` above the truck, not held (held = thumbnail-tiny), the
`tag_el` at x ≤ 760 (right rail); (2) cast standing in front of the truck hide the `menu` word — pass `menu=None` when people stand at the window, or place
them by the wheels; (3) end card: `foodtruck_el(640)` at y≈1060 sits clear above `choice_card`; (4) a row of `foodtruck_el(300)` at y 1240–1320 reads as a queue.
Original spec:
- `foodtruck_el(w, open_=True, menu="TACOS", glow=1.0, permit=True)` — a generic step-van food truck side view: boxy body (accent colour param),
  serving window with a pull-up awning (striped), a small menu board, a round headlight + two wheels, a little permit sticker rectangle on the
  door (`permit=False` = empty dashed outline), optional steam puffs from the roof vent. Needs to read at w 260 (queue of trucks) and w 900 (hero shot).
- `commissary` set (register in `_FLOOR`, floor ≈ 1220): a big garage-kitchen — roll-up door, steel prep tables, a wash bay with a hose, ceiling
  lights, two parked trucks' rear ends; cool light. (Fallback if time is short: `market_hall` with `foodtruck_el` parked + a hose — note it in the run log.)
- `permit_el(w, price="$200", stamped=False)` — a small official-looking card (no seal): "MOBILE FOOD VENDING UNIT PERMIT", a number line, price tag
  corner; `stamped=True` adds `stamp_el` "VALID". Can be a thin wrapper over `card_el`/`form_el` if those fit.
Reuse: sets `street` (NYC block), `office` (city office), `store_cafe` (taco moment), `courtroom`-free; props `tag_el`, `form_el`, `calendar_el`, `stamp_el`,
`cash_el`, `coin_el`, `check_el`, `list_el`, `phone_el`, `bubble_el`, `gavel_el`(not used), `sign_el`; HUD `cold_open`, `series_badge`, `hud_rule`,
`choice_card`, `say`. Keep `say()` captions ≤ ~22 characters, clear of heads (y ≤ 1050 or ≥ 1450 when characters stand at 1650–1880).

| Line | Set / shot | Cast + acting | HUD / props / caption | SFX |
|---|---|---|---|---|
| i1 | `street` WIDE, frame 1: a bright `foodtruck_el(900, permit=False)` centre (awning shut), the grey-tie permit holder holds up a tiny `permit_el(260, price="$200")`; beside it a towering `tag_el("$$$$$")` swings down | hero `brow="sus"`, holder neutral | `cold_open(f, "2026", "NEW YORK CITY", "YOU: FIRST-TIME OWNER")`; `series_badge(f, "HOW TO START", "EP 3")` from ~1.5 s; `say("$200 PERMIT")` y≈960 → `say("RENTED FOR $$$$$?")` y≈1060 | truck horn honk |
| i2 | `street` MID: the hero holds a taco up to the skyline → slow push-in; at ~2.5 s the taco "grows" into a thought bubble with the truck and a queue of customers | hero dreamy | `series_badge(f, "HOW TO START", "EP 3")` top right | street hum, sizzle |
| i3 | the thought bubble pops: the truck sits with its awning shut and a `sign_el("NOT ALLOWED TO SERVE")` → four step pills drop in a row | hero `expr="wow"` then `sweat=True` | pills 1–4 (YOU · BASE · TRUCK · PERMIT) | pop, 4 dings |
| a1 | `office` city counter: the hero alone, no truck — he points at himself | hero cheeky | `cold_open(f, "STEP 1", "LICENSE YOU", "NOT THE TRUCK")` | honk, counter bell |
| a2 | `form_el(title="MOBILE FOOD VENDOR LICENSE")` slides across the counter → a `list_el` "FOOD SAFETY COURSE" with a `check_el` | inspector stamps, hero writes | `say("VENDOR LICENSE")` → `say("+ PASS A COURSE")`; `hud_rule(f, 1, "LICENSE YOU FIRST")`; chip "NYC Health Dept., 2026" | stamp, pen scratch |
| a3 | a long empty rope line; the hero walks straight to the front | hero `expr="smirk"` | `say("NO WAITING LIST")` | whoosh, ding |
| b1 | `commissary` WIDE: the roll-up door rises, light floods in | girl (mentor) waves him in | `cold_open(f, "STEP 2", "FIND A BASE", "THE COMMISSARY")` | honk, roll-up door rattle |
| b2 | three quick beats: truck parked (STORED) → hose spray (CLEANED) → wrench on the generator (SERVICED) | mentor points, hero copies | `say("STORED · CLEANED")` → `say("SERVICED")` | hose spray, wrench clank |
| b3 | `calendar_el("EVERY", "DAY")` flips; a dotted route line loops from the `street` back to the commissary door | hero yawns, mentor taps her wrist | `hud_rule(f, 2, "BACK AT LEAST ONCE A DAY")`; chip "NYC Health Dept." | clock tick, honk |
| c1 | `street` used-truck lot: three trucks, one dented; the hero walks past them, hands behind his back, wallet stays in his pocket | hero `brow="sus"` | `cold_open(f, "STEP 3", "PRICE THE TRUCK", "DON'T BUY YET")` | honk |
| c2 | price tag swings down on the dented truck | hero `expr="wow"` | `tag_el("$30K–$100K USED")`; chip "DoorDash guide, Sep 2026" | ka-ching, tag swing |
| c3 | the hero's hand with cash freezes mid-air; pill #4 glows red and wobbles; the truck's wheels spin but it doesn't move | mentor holds up a hand "STOP" | `say("NOT YET")`; `hud_rule(f, 3, "DON'T BUY BEFORE THE CALL")` | record scratch |
| e1 | `office`: a giant `permit_el(700, price="$200")` on the counter | hero leans in | `cold_open(f, "STEP 4", "THE TRUCK PERMIT", "THE HARD ONE")` | honk, low synth swell |
| e2 | a velvet rope clicks shut in front of a short stack of permit cards; a `sign_el("CAPPED BY LAW")` drops | inspector neutral | `say("CAPPED BY LAW")`; chip "NYC Health Dept." | rope click, thud |
| e3 | `calendar_el("LIST", "2022")` flips; a line of tiny `foodtruck_el(260)` trucks stretches off-screen | hero counts the trucks, gives up | `say("2022 LISTS FIRST")` | slow ticking |
| e4 | dim side street: the holder's hand slides a permit card across a table from off-frame (face not shown); the hero looks at it, torn | hero torn | `say("RENT ONE?")` → small `say("OUTSIDE THE SYSTEM")` | low hum |
| e5 | the `tag_el` grows: $200 → "UP TO $25,000" | hero jaw drop | `say("UP TO $25,000")`; chip "Vendors to Queens Daily Eagle, Apr 2025" | ka-ching x3 |
| e6 | `calendar_el("YEAR", "2009")` flip, sepia: a `form_el(title="CHARGES")` lands on a pile of permit cards (no characters on screen — the holder from e4 is never shown next to the charges) | — | small chip "NYC Dept. of Investigation, Jun 2009"; `say("RISKY")` | paper thud |
| e7 | sepia drops away, bright `street`: a door in the rope opens; numbered tickets start printing fast | hero `expr="wow"` | `say("+2,200 A YEAR")` → `say("SUPERVISORY LICENSE")` → `say("FOR 5 YEARS")`; chip "NYC Health Dept., Mar 2026" | printer whirr, ding |
| t1 | the tickets fly to the trucks already in line (labelled "2022 LIST"); the hero checks his pockets — no ticket — shrugs, then puts on an apron and the mentor waves him into the window of her truck | hero sheepish → grin | `say("ON A 2022 LIST?")` → `hud_rule(f, 4, "NO SPOT? WORK ONE FIRST")` | whoosh, sizzle |
| t2 | parked in a `street` private lot: truck open, steam, `sign_el("PRIVATE LOT")` | hero smirks | `say("PRIVATE PROPERTY")`; `tag_el("NO WAITING LIST")`; chip "NYC Health Dept.: Restricted Area permit" | sizzle, ding |
| z1 | end card: hero (paper cap) + mentor beside the open truck, steam from the vent, the skyline behind | hero points at camera | "SAVE THIS" pill → `choice_card(f, "STILL NYC?", "STAY", "MOVE")` | whoosh, choice whoosh |
| z2 | end card holds, a customer queue forms | mentor waves | `series_badge` | horn honk (short) |

Source chips: "NYC Health Dept., 2026" (on screen as plain text, no seal), "DoorDash guide, Sep 2026", "Vendors to Queens Daily Eagle, Apr 2025",
"NYC Dept. of Investigation, Jun 2009", "NYC Health Dept., Mar 2026".
Post: first line "How to start a food truck in New York City in 4 steps (2026) — and why some vendors report renting a $200 permit for thousands." · "How to Start · Ep 3" ·
step list in the caption (vendor license + course · commissary, back daily · truck last · unit permit: capped by law, 2022 waiting lists first; at least 2,200 supervisory license
applications a year from 1 Jul 2026 for 5 years) · "Rules as of Nov 2026, NYC only. Not legal advice, no income promised." ·
firstCommentText "Still New York — STAY or MOVE? And which city would you pick?" · pinned reply ready for "how do I get on the list?": "Check the NYC Health
Department's mobile food vending page for current waiting-list news. There's no waiting list for the personal vendor license." · YouTube title "How to Start a Food Truck in NYC | 4 Steps" ·
hashtags #foodtruck #nycfoodtruck #smallbusinessideas #smallbusiness #howtostart
