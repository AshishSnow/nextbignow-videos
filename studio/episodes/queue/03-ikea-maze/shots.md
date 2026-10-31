# Storyboard — SPOT THE TRICK · #1 (Why does IKEA hide the way out?). One row per VO line; a shot changes every 2–3 s inside long lines.
Look: full-frame lit scenes (PLAYBOOK §6), hero = YOU, the shopper (hoodie, a plain grey tote or wire basket — never the big yellow bag: trade dress).
Every frame graded via finish(). Music: **marching-band / brass oompah** (new genre for the channel — "the route march"), woodblock
clicks on each TRICK chip; no "Oops" sting (no blunder in this episode). **No IKEA logo, no blue-and-yellow trade dress, no product
names**: the store is "the flat-pack giant" on screen (plain white sign "FLAT-PACK STORE"), arrows on the floor are grey, bins are
plain cardboard, the hot dog is a generic hot dog. "IKEA" appears only as plain text in the hook caption and source chips.
New assets this episode needs (write in `template/anim_story.py` style, add to the story kit): set `maze_store` (top-down-ish
showroom path: white floor with grey arrows, room sets left and right, a far EXIT sign always behind the camera), set
`market_hall` (tall shelves + cardboard bins), set `store_cafe` (long canteen tables, serving counter), prop `bin_el` (cardboard tub
piled with one item: candles / cushions / plastic plants), prop `arrow_floor` (floor arrow decal), prop `flatpack_el` (flat box →
assembled wobbly shelf, `built=0..1`), `hotdog_el` exists (anim_props), `tray_el` (meatballs + lingonberry blob), `shortcut_door_el`
(plain grey door with a small "SHORTCUT" sign). Reuse: `door_el`, `numcard_el` (roadmap cards 1–4), `tag_el`, `shelf_el`, `lamp_el`,
`copier_el` (no), `quote_card`, `series_badge`, `choice_card` (use for the save/share end card with "SAVE" / "SEND" pills).

| Line | Set / shot | Cast + acting | HUD / props / caption | SFX / camera |
|---|---|---|---|---|
| i1 "Why does IKEA hide the way out?" | **maze_store WIDE, frame 1**: the hero mid-path, a grey arrow under his feet, room sets both sides, a tiny EXIT sign far *behind* him (reversed) | hero `expr="sus"`, looking back over his shoulder | `series_badge("SPOT THE TRICK", "#1 · THE FLAT-PACK MAZE")`; `say("WHY HIDE THE EXIT?")` | footsteps, slow push-in |
| i2 "You walk in to buy one lamp. Budget: twenty dollars." | store entrance MEDIUM: turnstile, a stack of wire baskets | hero takes a basket, holds a tiny paper list "LAMP" | `cold_open(f, "TODAY", "THE FLAT-PACK STORE", "YOU: SHOPPER, $20")`; `say("$20 · ONE LAMP")` | turnstile click |
| i3 "This shop sells nearly forty-five billion euros a year. Four tricks nudge you along the way." | CU on a cash desk → four `numcard_el` roadmap cards slide in (1–4) | — | `say("€44.6 BILLION A YEAR")` + chip "Source: Inter IKEA, FY25 (Oct 2025)" | cash register ×4 |
| i4 "The last one follows you home." | card 4 flips to "?" and floats off toward a tiny house | hero watches it go | `numcard_el(4, down=True)` | whoosh |
| a1 "Trick one. The path." | maze_store, top-down WIDE: the winding path drawn as one grey line through the whole store | hero = a dot on the line | chip `TRICK #1 · THE PATH` (`hud_rule` style) | woodblock |
| a2 "One path, one direction, but the exit is always behind you." | maze_store MEDIUM: hero walks forward on an `arrow_floor` decal; the EXIT sign slides backwards out of frame | hero turns, confused, `look=(-1,0)` | `say("EXIT: BEHIND YOU")` | reverse whoosh |
| a3 "A London professor says the layout is built to confuse you, so you pass everything." | lecture CU: `oldman` look re-dressed (tweed jacket, no glasses) at a lectern labelled "UCL LECTURE, 2011" | points at a floor plan | `quote_card(f, "The way to the exit is always behind you", "Prof Alan Penn, UCL, as reported by The Local, Jan 2011")` | chalk tap |
| a4 "He estimates six in ten things bought here were never on the list." | hero's trolley from above: 10 items, 6 light up red, 4 green; the paper list says LAMP | hero shrugs | `say("6 IN 10: NOT ON THE LIST")` + chip "Prof Penn's estimate, UCL 2011" | pop ×6 |
| a5 "Beat it: ask staff for the shortcut doors. The store says they're there." | maze_store: a `worker` look (re-dressed: plain grey polo, cap off) opens a grey `shortcut_door_el` in the wall | hero peeks through, `expr="wow"` | `say("BEAT IT:", y≈1180)` + `say("ASK FOR THE SHORTCUT")` (two lines, green; one line shrinks to 46 %) | door creak |
| b1 "Trick two. The bins." | **market_hall** WIDE: three giant cardboard `bin_el` tubs | hero small beside them | chip `TRICK #2 · THE BINS` | woodblock |
| b2 "Huge tubs of one cheap thing. Staff even have a name for it: bulla bulla." | bin CU: hundreds of identical candles piled over the rim | a `worker` whispers behind a hand | `say("BULLA BULLA")` + chip "The New Yorker, Oct 2011" | candle clatter |
| b3 "A mountain of stuff looks like a bargain. So your lamp gets a candle friend." | hero's basket: lamp box + a candle hops in | hero `expr="smirk"` | a plain price tag (no invented price) → the basket | hop + ding |
| b4 "Beat it: a full bin is not a sale. Read the tag." | CU of the bin's price tag; the pile fades to one candle on a plain shelf at the same price | — | `say("BEAT IT: READ THE TAG")` (green) | — |
| c1 "Trick three. The food." | **store_cafe** WIDE: queue, trays, a plain menu board | hero rubs his stomach | chip `TRICK #3 · THE FOOD` | woodblock |
| c2 "Halfway through you're starving, and there's a one-dollar hot dog." | counter CU: `hotdog_el` with a "$1" tag | hero `sweat=True`, eyes on the hot dog | `say("$1 HOT DOG")` + chip "IKEA US bistro menu, 2026" (UK/EU build: localise the price or say "a one-dollar hot dog" with the US chip) | sizzle |
| c3 "The founder added the restaurant in nineteen sixty. His reason: hungry customers buy less." | sepia flashback (`sepia_tone`): 1960 canteen, a `creator` look as the founder (no likeness, label "THE FOUNDER, 1960") | points at the counter | `quote_card(f, "hungry customers buy less", "IKEA company history (ikea.com)")` | old-film flutter |
| c4 "Full, you keep walking. Food alone brought in over two billion euros in a year." | hero with a `tray_el` walks back onto the grey arrow; a meatball-shaped counter rolls up | `expr="happy"` | `say("€2 BILLION+ ON FOOD")` + chip "Ingka Group, FY2019 figure (Feb 2020)" | coins |
| c5 "Beat it: eat first, then shop the list, not the showroom." | hero sets the tray down, pulls out the paper list "LAMP" | determined | `say("BEAT IT:", y≈1180)` + `say("BACK TO THE LIST")` (green) | paper snap |
| d1 "Trick four. The one that follows you home." | **study** set (home): a flat box on the floor | hero kneels with an Allen key | chip `TRICK #4 · FOLLOWS YOU HOME` | woodblock + door close |
| d2 "You build the shelf. It wobbles. You still love it." | `flatpack_el(built=0→1)`: box → wobbly shelf; a heart pops over it | hero `expr="wow"`, hugging the shelf | `say("YOU LOVE IT ANYWAY")` | clacks, wobble creak |
| d3 "Researchers tested this with plain boxes." | lab CU: two identical plain boxes, one built, one pre-built, with bid cards | `inventor` look in a lab coat | chip "Norton, Mochon & Ariely, J. Consumer Psychology 2012" | — |
| d4 "Build a plain box yourself, and you bid sixty-three percent more than someone handed it built." | `bars()` chart: $0.48 vs $0.78 (labels) on a sky scheme | — | `ui_word("BUILDERS PAID", "+63%", …)` | bar rise |
| d5 "Finish it, and you overvalue it. Stop halfway? The magic is gone." | split: a finished box glowing vs a half-built box, grey, heart cracks | hero on the right half, deflated | `say("HALF-BUILT? NO LOVE")` | glass crack |
| d6 "So you do the work, and you fall for your own work." | hero CU (`person_head_at`), the wobbly shelf behind him | `expr="smirk"`, looks at camera | `say("YOUR WORK. YOUR BIAS.")` | — |
| d8 "Beat it: before you keep it, price it like a stranger would." | the hero holds the shelf up to a passing `friend` look, who holds up a small price card | friend shrugs | `say("BEAT IT:", y≈1180)` + `say("A STRANGER'S PRICE")` (green) | ding |
| d7 "The twist? IKEA tried stores with no maze." | city-street set: three small storefronts labelled MADRID · SHANGHAI · WARSAW, open-plan inside | hero peeks in | `say("STORES WITH NO MAZE")` + chip "Fortune, 1 Sep 2023 (Ingka retail chief)" | city ambience |
| t1 "Shoppers wanted guiding. IKEA closed those stores." | the three storefronts get a `closed_sign_el` one by one | hero `expr="wow"` | `quote_card(f, "No, no, no, this is a big shop!", "shoppers, as told by Ingka's retail chief to Fortune, 2023")` | sign thunk ×3 |
| k1 "Bring a list. Take the shortcut. Ask what a stranger would pay." | takeaway card: three pills LIST · SHORTCUT · ASK A STRANGER | hero holds the list up | three `say()` lines stacked (y≈1120/1270/1420): "LIST" · "SHORTCUT" · "ASK A STRANGER" (one line shrinks to 42 %) | ding ×3 |
| e1 "Save this before your next trip. Comment which trick got you." | **end card**: hero centre on the frame-1 path, the four TRICK chips around him | to camera | `choice_card(f, "WHICH TRICK GOT YOU?", "MAZE · BINS", "FOOD · SHELF", y≈1410)` + `series_badge` | choice whoosh |
| e2 "Send this to the friend who went in for a lamp." | end card holds; phone "SEND THIS" | hero points at camera | — | — |

Loop: the last frame dissolves to the hero on the grey arrow with the EXIT sign behind him (frame 1).
Post copy: first line "IKEA hides the exit on purpose. Here's why — plus 3 more tricks you can spot tomorrow." · series line "Spot the Trick · #1" ·
firstCommentText "Which trick gets you every time — MAZE, BINS, FOOD or SHELF?" ·
YouTube title "IKEA Hides the Exit on Purpose | Spot the Trick" (≤ 50 chars → check).
Sponsor slot (BRAND.md §4, when a deal exists): the "Beat it" line of Trick #1 or #4 (a list/budgeting app, 8–15 s), never the hook.
