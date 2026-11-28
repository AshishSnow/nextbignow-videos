# shots — 39 Jellycat "A chef cooks you a stuffed toy" (DOODLE case study, SHORTS length; reference examples/grillos-pickle-doodle + dsc-video-doodle)
COVER = ("THIS TOY STORE HAS A CHEF", "PLUSH 'MEALS' FROM $75 — WHY?")
Look: LIGHT page (white graph paper, wobbly black ink, yellow highlighter — the Grillo's/Yankee look), chunked torn-strip subtitles
(strip_chunk + chunk_now), NO music — SFX only. Recurring plain "YOU" stick doodle (tape "YOU") from i2. One set per section that
evolves; something new every 1–2 s; red marker on top. Cover: cream page, big black title + yellow swipe; the drawn hero = a diner plate
with a generic round plush (dot eyes, stitched smile — OUR design, not a Jellycat character) under a cloche, a "$75" tag on a toothpick.
Director's brief — the ONE moment: d1→d3, the diner's receipt printer starts spitting a long receipt that becomes a bar chart
(£200M → £450M), then a day-counter flips "≈ £650,000 PROFIT / DAY" (ka-ching). Build to it: c1–c4 the plain toy shelf turns into a
diner, a chip shop and an airline desk, piece by piece.
NEW kit assets: `_fries` character (generic paper cone of plush fries, felt-texture lines, dot eyes — attitude only), `plush_blob()`
(generic round soft toy, our own shape, 3 colour variants), `cloche_plate()` (plate + silver dome that lifts), `fryer_basket()` (can reuse
`fryer()` from 37 if built), `chip_paper()` (newspaper cone wrap), `checkin_desk()` (plain desk + "GATE 1" sign + toy suitcase),
`toy_shelf()` (3-shelf unit of plush_blobs), `lab_flask()` (CPSC test flask + a "CERTIFICATE" paper), `market_stall()` (awning stall).
Existing: char, stamp, tape, store, building, money_stack, checklist, clipboard, bars, register, calendar, stall, receipt.
KIT READY (28 Nov R&D run, `python3 studio/tools/kit_check.py` → 0 missing; lab frame `lab/visuals/kit_28nov/sheet_small.jpg`): `_fries` → `char(c, "fries", …)`; `plush_blob(variant 0–3, col)`; `cloche_plate(lift, price)`; `chip_paper()`; `checkin_desk(sign, kg)` + `suitcase()`; `toy_shelf(fill)`; `lab_flask(cert)`; `market_stall()`; receipt = `receipt_printer(feed, lines)` (the d1 receipt → bar-chart moment); fryer = existing `fryer()`.

| Line | Set (evolves) | Props pop in | Tape / stamp | Red marker | SFX |
|---|---|---|---|---|---|
| **SET 1 — the diner counter + YOU (i1–i3)** | | | | | |
| i1 | a diner counter; a chef doodle (tall hat, tape "CHEF") flips a plush_blob on a griddle like a pancake | cloche_plate slides to the front | tape "NEW YORK · A TOY STORE" | "?" over the cloche | sizzle, flip whoosh |
| i2 | cloche lifts: the plush sits on the plate; a toothpick tag "FROM $75 (2026)"; YOU (tape "YOU") pops up at the counter, wallet out | — | — | circle "$75" | cloche ding, pop |
| i3 | three empty boxes "1 2 3" drop onto the counter's menu board | — | tape "3 MOVES" | tick ×3 | thud ×3 |
| **SET 2 — the plain toy shelf becomes a show (b1–c4)** | | | | | |
| b1 | the diner slides off; a small shop with toy_shelf; two stick doodles (tapes "THOMAS GATACRE", "WILLIAM GATACRE") stock it | plush_blobs ×3 | tape "LONDON · 1999" | arrow "BROTHERS" | pop ×3 |
| b2 | name sign "JELLYCAT" hand-lettered (plain text, NOT their logo); a row of other identical shelves "EVERY TOY BRAND" fades in beside it | — | — | "=" sign between shelves | page rustle |
| c1 | the shelf spins around like a stage flat — its back is a kitchen | — | tape "THE SURPRISING MOVE" | big red X over the word "SHELF" | whoosh, stage clunk |
| c2 | a fryer_basket (display — no oil, no flame) holds plush fish and plush fries; staff doodle wraps them in chip_paper | — | tape "SELFRIDGES · LONDON (2024–)" | circle the fryer | fryer sizzle, paper wrap |
| c3 | the fries character (`_fries`) pops out of the cone, offended, shaking off a salt shaker | — | — | red "!" | boing, salt shake |
| c4 | the kitchen folds into a pretend plane cabin (rows of seats used as shelves, plush in the seats); YOU pays at a checkin_desk, toy suitcase on the scale | — | tape "HARRODS · JELLYCAT AIRLINES (OCT 2025)" | circle "CHECK-IN = CHECKOUT" | ding-dong (PA chime), stamp |
| **SET 3 — the receipt + chart (d1–a2)** | | | | | |
| d1 | **(the moment)** the desk's receipt printer feeds a long receipt that bends into a bar chart: 2023 bar then a much taller 2025 bar | chip "SALES £200M (2023, pgbuzz) → £450M (2025, PA / Business Matters)" | — | arrow "MORE THAN ×2" | printer feed, whoosh up |
| d2 | the tall bar gets its label | tape "2025 (YEAR TO DEC) · £450 MILLION" | — | underline "£450M" | ding |
| d3 | a day-calendar flips; a money_stack grows each flip | counter "≈ £650,000 / DAY" + chip "PRE-TAX PROFIT £240M ÷ 365 (OUR MATH)" | stamp "PROFIT" | circle "/ DAY" | ka-ching, page flips |
| a1 | the chart rolls into a US-flag-coloured bar chart (plain); YOU steps in (the "why now" bridge) — bar "ADULTS 18+" tallest | — | tape "WHY NOW" | circle the adults bar | whoosh |
| a2 | the adult bar grows by a quarter | chip "TOY SALES TO ADULTS 18+ +25% · JAN–JUN 2026 · CIRCANA" | — | red up-arrow "+25%" | boop up |
| **SET 4 — YOU's stall (m1–m3)** | | | | | |
| m1 | YOU at a desk sews a plush_blob with tiny glasses and a mug (desk buddy); a crib doodle in the corner gets crossed out | — | tape "1 · MADE FOR ADULTS (SAY SO)" | X over the crib | sewing tick-tick |
| m2 | a child-sized plush version goes into a lab_flask scene; a "CERTIFICATE" paper prints | chip "KIDS 12 & UNDER: CPSC-ACCEPTED LAB TEST + CHILDREN'S PRODUCT CERTIFICATE + TRACKING LABEL" | tape "2 · KIDS' TOYS = LAB TEST FIRST" | tick on the certificate | bubbling, stamp |
| m3 | YOU's market_stall gets a mini griddle and a chef hat; a small line of doodle people forms | — | tape "3 · SERVE IT, DON'T JUST SELL IT" | ticks on the hat | sizzle, crowd murmur (soft) |
| **SET 1 again — callback (f1–z2)** | | | | | |
| f1 | back at the diner: the cloche from i2; YOU tries a fork on the plush — it bends | — | tape "100% NOT FOOD" | red X over the fork | boing, fork twang |
| f2 | YOU shrugs and points at the plush fries anyway | — | — | heart doodle | pop |
| z1 | phone send arrow flies to a friend doodle in a bed buried in plush_blobs | — | — | — | whoosh |
| z2 | two options: a heart "CUTE" vs a money stack "CRAZY MONEY" | comment bubble | — | "?" between them | pop |
TTS: listen for "Gatacre" (GAT-uh-ker), "Jellycat", "Selfridges", "Harrods", "Circana" (sir-KAH-nuh), "British pounds", "Sweetie, I'm stuffing".
Safety: no Jellycat character designs (no Bashful bunny, no amuseables food faces), no logo, tags, bags or store trade dress — names as
text tapes only; plush = our own generic blobs; founders = plain stick doodles with name tapes (no likeness); no FAO Schwarz / Selfridges /
Harrods logos or shopfronts. No mental-health or therapy framing. Dividend not mentioned (paid to the parent, understood to stay in the
group). Caption: "Education only. One rare outcome, not typical. US toy rules: cpsc.gov."
