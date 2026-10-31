# Storyboard — YOUR MOVE · EP 1 · Part 1 (Pepsi jet). One row per VO line; a shot changes every 2–3 s inside long lines.
Look: full-frame lit scenes (PLAYBOOK §6), hero = YOU (hoodie; a 1996 look: `who={"base": "hero", "top": (60, 110, 170)}` denim-blue
hoodie is fine), every frame graded via finish(). Music: 90s alt-rock/funk-lite bed (new genre for the channel), sting on "Oops".
No Pepsi logo, can design or brand colours as trade dress: generic cola cans/packs (silver + green band), a generic jump-jet with no
insignia (grey, two swivel nozzles, bubble canopy). New template assets this episode builds: `jumpjet_el` (lit, `_Fig` style),
`set_view("bedroom90s")` (CRT TV, posters, desk), `set_view("schoolyard")` (brick school, bike rack, flagpole without flag),
`mailbox_el`, `catalog_el`, `coupon_el`, a quote card helper if none exists (`quote_card(f, text, source)`).

| Line | Set / shot | Cast + acting | HUD / props / caption | SFX / camera |
|---|---|---|---|---|
| i1 "Could you buy a real fighter jet… with Pepsi points?" | **schoolyard, dusk**, low angle WIDE: the jump-jet hovering over the bike rack, cola caps raining | hero small at bottom, looking up, `expr="wow"` | frame 1 = the jet already hovering; `part_badge("YOUR MOVE", "EP 1 · THE PEPSI JET")` | jet whine, slow push-in |
| i2 "It's 1996. You're 21, a business student in Seattle." | bedroom90s MEDIUM | hero on bed with textbook, turns to camera | `hud_clock(f, "1996", "SEATTLE", "YOU: STUDENT, 21")` (cold-open card) | clock tick |
| i3 "…a jet worth over twenty million dollars… as a prize." | CRT TV close-up (the ad playing: tiny jet on screen) | hero reflection on the glass, eyebrows up | `say("$20,000,000+ JET")` | TV static pop |
| a1 prizes for points: T-shirts, jackets, sunglasses | TV CU → items pop out of the screen one by one | — | T-shirt / jacket / shades icons with point tags (no numbers needed) | pop pop pop |
| a2 "Its last scene? A teenager lands a fighter jet at school." | schoolyard WIDE (inside the TV frame edge) | a kid look in the cockpit, papers flying | — | jet roar, screen shake |
| a3 "The price… seven million Pepsi points." | TV CU | — | `hud_rule(f, 1, "7,000,000 POINTS = 1 JET")` | rule "ding" |
| a4 "You want that jet. But three problems stand in your way." | bedroom MEDIUM, hero stands up | determined, `look=(1,0)` | three locked padlocks labelled 1 2 3 (roadmap) | lock clicks |
| b1 "Problem one… drinking an ocean of Pepsi." | bedroom WIDE: hero buried in a mountain of generic cans | `sweat=True`, `expr="sad"` | lock 1 pops; `say("PROBLEM 1")` | can avalanche |
| b2 "So you read the small print." | catalog CU (generic "PRIZE CATALOG") | hero leaning in, magnifier | — | page flip |
| b3 "fifteen real points… buy the rest. Ten cents each." | catalog CU, small print highlighted | — | highlight the rule; `say("10¢ PER POINT")` | marker squeak |
| b4 "Seven million points? That's seven hundred thousand dollars." | hero CU (`person_head_at`, parlor-style blur bg) | `expr="smirk"`, calculator in hand | `say("$700,000")` | calculator beeps |
| b5 "For a jet worth more than thirty times that." | split: small $700K bag vs giant jet | — | scale arrow "×30+" | — |
| b6 **"Oops, Pepsi."** (signature beat) | hero turns to camera, CU | smirk | OOPS stamp (`stamp_el("OOPS")`) | **Oops sting** (same every episode) |
| c1 "Problem two. You don't have seven hundred thousand dollars." | hero empties pockets (lint, a coin) | `expr="sad"` | lock 2 | coin tinkle |
| c2 "So you pitch five investors. And they lend you all of it." | **office** two-shot → wide: hero with a flip chart, five `exec`/`creator` looks around a table | investors nod one by one | 5 money bags slide in; `say("5 INVESTORS")` | cash register |
| d1 "Problem three. You actually have to ask." | bedroom desk MEDIUM | nervous | lock 3 | — |
| d2 order form, fifteen points, cheque $700,008.50 | desk top-down: `form_el("PRIZE ORDER FORM")`, 15 tiny points, `cheque_el(...)` with the amount | hero's hands (fg_hand style) | amount readable: $700,008.50 | pen scratch |
| d3 "Ten of those dollars are for shipping." | cheque CU on "$10 S&H" line | — | circle on the $10 | tiny honk (comedy) |
| d4 "You mail it. And you wait." | street at night, mailbox_el, hero drops envelope | — | `hud_clock(f, "MARCH 1996", "SEATTLE", "DAY 1")` → days tick | mail thunk, clock ticking |
| t1 "Pepsi replies: the jet was just for fun." | hero at door with an opened letter, CU | `expr="wow"` → sad | **quote card**: "fanciful … a humorous and entertaining ad" — source chip "Pepsi letter, 1996 (per Seattle Times)" | paper rustle |
| t2 "Instead of a jet… free Pepsi coupons." | coupons flutter down onto the hero | deadpan | coupon_el ×3 | sad trombone (short) |
| e1 "Lesson one: read the small print." | catalog small-print CU | — | `say("READ THE SMALL PRINT")` | — |
| e2 "Your move: sue Pepsi, or drop it? Comment JET or DROP." | **end card**: hero centre, jet left, coupons right | `look=(0,0)` to camera | `hud_choice(f, "YOUR MOVE", "JET  or  DROP", y≈1450)` + badge | choice whoosh |
| e3 "Part two tomorrow. Send this to the friend who reads every rule." | end card holds; "PART 2 TOMORROW" pill | hero points at camera | `part_badge("PART 2", "TOMORROW")` | — |

Loop: the last frame dissolves toward the jet over the schoolyard (frame 1) so a rewatch feels seamless.
Post copy: first line "A 21-year-old tried to buy a fighter jet with Pepsi points." · series line "Your Move · Ep 1 · Part 1" · firstCommentText
"JET or DROP — what would you do?" · YouTube title "He Tried to Buy a Jet With Pepsi Points | Your Move" (≤ 50 chars → shorten if needed).
