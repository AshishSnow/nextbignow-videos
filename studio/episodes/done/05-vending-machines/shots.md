# Storyboard — HOW TO START · EP 2 · Vending machine business. Look: COLOURFUL STICK CAST (anim_stick.py): hero = orange beginner,
mentor = `girl2` (purple, runs a small vending route — the expert voice of the steps), seller = `exec` re-coloured grey `{"base": "exec", "col": (150, 152, 160)}`
(a generic "DEAL SELLER", never a real company), the fake reference = `oldman` holding a phone with music notes (the "singer"), the spot owner = `lady`.
**New in this episode (inauthentic-content guard, BRAND.md §2):** first "consumer-protection" story inside a how-to; the singer reveal as the
hook payoff; the four-step plan (steps 1–3 practical, step 4 = the deal to be careful with). US-only rules (said in i2 and on the frame-1 card). Music: **funk / clavinet groove** (new genre for the channel), coin-drop SFX on every STEP card.
No Oops beat (no company blunder of our own story; the FTC cases are told as what the FTC said). No real seller names on screen.
**Assets:** `vending_el(w, fill=1.0, glow=1.0, broken=None, era=None)` — **WRITTEN 1 Nov (R&D run, `template/scripts/anim_props4.py`; lab frames `lab/story_kit/storyboard_vending_ep2.py`, 0.3–0.7 s/frame; smoke test passes).** Lab-frame notes: (1) i1 — `phone_el()` held by the seller renders phone-sized-huge and shows an old chat ("who orders the steak?"): use `bubble_el("BEST DEAL EVER!")` + a small music note instead, or `phone2_el("CALL MY REFERENCE", "♪")` at w≈220; (2) `vending_el(640)` at y 1300 + caption `say("A SINGER?", y=1000)` reads well, card top-left clear of UI zones; (3) CU c3 at w 820 fills the frame, the red dot on BILLS is small — add a `stamp_el` or ring pulse on it. Original spec: — a generic glass-front snack machine (coil rows of coloured snack packs,
`fill` 0..1 empties the coils, keypad, coin slot + bill reader panel on the right, pickup flap; `broken="cooler"|"coins"|"bills"` greys that
part and flashes a red dot). **The nickel-Coke board (04) also lists `vending_el` in its build brief — write it once, both episodes use it.**
Reuse: sets `airport` (busy spot), `office` (empty hallway / break room), `street`, `store`; props `form_el(title=…)`, `shield_el`, `tag_el`, `stamp_el`,
`phone_el`, `bubble_el`, `check_el`, `cash_el`, `coin_el`, `calendar_el`, `sign_el`; HUD `cold_open`, `series_badge`, `hud_rule`, `quote_card`, `choice_card`, `say`.
Keep `say()` captions ≤ ~22 characters and clear of heads (y ≤ 1050 or ≥ 1450 when characters stand at 1650–1880).

| Line | Set / shot | Cast + acting | HUD / props / caption | SFX |
|---|---|---|---|---|
| i1 | `store` WIDE, frame 1: a bright `vending_el(900)` centre, the hero reaching for his wallet; behind him the grey seller holds a phone out to him | hero `brow="sus"`, seller smiling | `cold_open(f, "US", "VENDING MACHINES", "YOU: FIRST-TIME BUYER")` (no extra badge in frame 1); `say("A SINGER?")` y≈1000 from ~0.8 s, clear of the card | coin drop |
| i2 | `street` MID: the hero pushes an empty dolly past an office block, thought bubble with a snack machine | hero dreamy | `series_badge(f, "HOW TO START", "EP 2")` top right | street hum |
| i3 | push in on the machine; a price tag swings down → four step pills appear on the glass | hero `expr="wow"` | `tag_el("$4K–$9K NEW")`; chip "Dealer price lists, 2026"; pills 1–4 | ka-ching, dings |
| i4 | pill #4 turns red and wobbles; coins drain out of the hero's wallet | hero gulps (`sweat=True`) | — | buzzer |
| a1 | `office` corridor, the hero rolls the machine on a dolly, stops at a fork: empty hallway left, crowd noise right | hero looks both ways | `cold_open(f, "STEP 1", "SPOT FIRST", "THEN THE MACHINE")` | coin drop, wheels |
| a2 | shot 1 `office` empty hallway, tumbleweed dust, `vending_el(fill=1.0)` untouched → shot 2 `airport` WIDE, people streaming past; three clock icons (morning / lunch / evening) tick | hero counts on fingers | `say("COUNT PEOPLE")`; tally marks (no number) | clicker ticks |
| a3 | `airport` MID: the spot owner (`lady`) and the hero shake hands; a pie slice slides from the machine to her → a "RENT" envelope as the alternative | lady `mouth=2`, hero nods | `say("A CUT · OR RENT")`; chip "Stripe guide, Aug 2026" | slide whoosh |
| b1 | desk CU, papers drop in a stack | hero cracks knuckles | `cold_open(f, "STEP 2", "PAPERWORK", "RULES VARY BY CITY")` | coin drop, paper thump |
| b2 | `form_el(title="VENDING LICENSE")` gets a stamp → `shield_el(text="INSURED")` wraps the machine | girl2 points, hero thumbs up | `say("CHECK YOUR CITY")` → `say("INSURANCE")` | stamp, shield whoosh |
| c1 | `street` used-machine lot, three machines, one dented; a phone with a music note rings far off (singer tease) | hero kneels to inspect, glances at the ringing | `cold_open(f, "STEP 3", "BUY SMART", "NEW OR USED")` | coin drop, faint ring |
| c2 | price tag flips from $4K–$8K to $3K–$6K (used) | hero `expr="wow"` | `tag_el("$3K–$6K+ USED")`; chip "Dealer price lists, 2026" | tag flip |
| c3 | CU `vending_el` panel: coin slot, bill reader, cooler light up in turn — `check_el` ✓ ✓ ✓ (`broken="bills"` blinks red first) | girl2 taps each part | `hud_rule(f, 3, "TEST BEFORE YOU PAY")` | beep ×3 |
| e1 | `store` evening light: the grey seller fans out photos of "PRIME SPOTS" → push in on the contract, a pen slides toward the hero | seller grinning, hero tempted | `cold_open(f, "STEP 4", "CHECK THE DEAL", "SPOTS INCLUDED?")` | low synth swell |
| e2 | `calendar_el("YEAR", "1998")` flips back; sepia tint over the `store` | — | small chip "FTC, Sep 1998" | page flips backwards |
| e3 | 40 `stamp_el("FTC ACTION")` stamps rain onto a pile of brochures | — | `say("40 ACTIONS")` | stamps ×N, thud |
| e4 | the "prime spot" photo peels away: behind it, the empty `office` hallway | hero `expr="sus"` | `quote_card(f, "misrepresenting the availability of profitable locations", "FTC complaint (alleged), Sep 1998")` | record scratch |
| e5 | sepia drops away (back to today); `form_el(title="DISCLOSURE")` slides in with a list of names; `calendar_el("WAIT", "7 DAYS")` flips | girl2 holds it up | `say("PAST BUYERS")` → `say("7 DAYS")`; chip "FTC Business Opportunity Rule" | page flip |
| t1 | sepia again: the oldman on the phone, speech bubble `bubble_el("BEST DEAL EVER!")` with music notes; split-screen: the grey seller hands him cash | oldman beaming, hero jaw drop | `say("“SINGERS”")`; chip "FTC, Sep 1998" | 3-note jingle, cut off |
| t2 | back to today: the disclosure's list of names; the hero dials one himself | hero determined | `hud_rule(f, 4, "CALL THE LIST YOURSELF")` | dial tone |
| z1 | end card, hero + girl2 beside a full machine | hero points at camera | "SAVE THIS" pill → `choice_card(f, "YOUR FIRST SPOT?", "GYM", "OFFICE")` | whoosh, choice whoosh |
| z2 | end card holds, a snack drops in the machine | girl2 waves | `series_badge` | coin drop |

Source chips: "Dealer price lists, 2026" (on screen; links to vending.com + Stripe in the post — never name a seller on screen), "Stripe guide, Aug 2026",
"FTC, Sep 1998", "FTC complaint (alleged), Sep 1998", "FTC Business Opportunity Rule".
Post: first line "How to start a vending machine business in 4 steps (US) — and the 'singer' trick the FTC warned about." · "How to Start · Ep 2" ·
firstCommentText "Your first spot — gym or office? One word." · pinned reply ready for "how much does one make?": "Earnings vary a lot by spot — we don't quote
income numbers. Ask any seller for the past-buyer list." · YouTube title "How to Start a Vending Machine Business | 4 Steps" ·
hashtags #vendingmachine #vendingbusiness #smallbusinessideas #smallbusiness #howtostart
