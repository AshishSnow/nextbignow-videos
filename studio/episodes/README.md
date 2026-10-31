# The writers' room — episode queue

Scripts are written ahead, checked (`tools/story_check.py`: 7/7 R-gates + all S-gates) and reviewed by a fresh pair of eyes
before anyone renders (STORY.md §8). The R&D task keeps **≥ 3 REVIEWED** episodes here; the episode task builds the top one.

Folder per episode: `queue/NN-slug/` with `vo_lines.py` (SERIES / PART / EP + LINES), `shots.md` (storyboard: one row per line)
and a `SOURCES-*.md` (every number and quote with link + date). After posting: move the folder to `done/` and fill the row below.

Status: DRAFT → REVIEWED → BUILDING → BUILT (post time IST). A two-part Part 2 is due in the **same IST slot one day after
Part 1**: the episode task builds it on the second run after Part 1 was built. If Part 1 was never posted, Part 2 waits.

## Series counters
- YOUR MOVE: EP 1 (Pepsi jet, two parts), EP 2 (nickel Coke, queued)
- SPOT THE TRICK: #1 (IKEA maze, queued; next: #2)
- WHO REALLY OWNS IT: — (next: #1; the glasses video, built 28 Oct in the old format, counts as the format's origin)

## Queue (top = next to build)
| # | Folder | Series · EP · Part | Topic | Type | Status | Notes |
|---|---|---|---|---|---|---|
| 1 | queue/01-pepsi-jet-p1 | YOUR MOVE · EP 1 · Part 1 | Could you buy a fighter jet with Pepsi points? (Leonard v. PepsiCo, 1996) | A | REVIEWED (31 Oct: story_check 7/7 + 6/6; independent review "ready after must-fixes" → all applied) | Pilot of the new format. ~90 s. Assets ready in the story kit: jumpjet_el, crt_tv_el, catalog_el, coupon_el, mailbox_el, sets bedroom90s/schoolyard. Cliffhanger: Pepsi returns the cheque with coupons, then takes YOU to court → "Comment FIGHT or FOLD" + "Part two tomorrow". Storyboard frames: lab render 31 Oct (story kit). |
| 2 | queue/01-pepsi-jet-p2 | YOUR MOVE · EP 1 · Part 2 | The court case: was the ad a real offer? | A | REVIEWED (31 Oct, same review) | Build on the 2nd run after Part 1; same IST slot +1 day. Courtroom set + `set_front` for the judge behind the bench (story kit). Twist: even a win = a jet you couldn't fly. Ends "Comment JOKE or DEAL". |
| 3 | queue/03-ikea-maze | SPOT THE TRICK · #1 | Why does IKEA hide the way out? (the maze, the bins, the food, the IKEA effect) | E | REVIEWED (31 Oct R&D run: story_check 7/7 + 6/6; independent fresh-eyes review "ready after must-fixes" → all 7 must-fixes + 9 should-fixes applied, see SOURCES.md) | ~125 s est. Four tricks, strongest last ("follows you home" = the IKEA effect, Norton/Mochon/Ariely 2012); twist = IKEA's no-maze stores closed (Fortune 2023). New sets/props needed: maze_store, market_hall, store_cafe, bin_el, flatpack_el, shortcut_door_el (shots.md). No yellow bag / blue-yellow trade dress. Check "IKEA" in ASR read-back. Ends "Save this… comment which trick got you" + pills MAZE·BINS / FOOD·SHELF. |
| 4 | queue/04-nickel-coke | YOUR MOVE · EP 2 | Why would a soda boss ask the President for a brand-new coin? (Coke = 5¢ 1886–1959) | B | REVIEWED (31 Oct R&D run: story_check 7/7 + 6/6; independent fresh-eyes review "ready after must-fixes" → all 7 must-fixes + should-fixes applied, see SOURCES.md) | ~120 s est., single part. Seat = the Coca-Cola boss, 1950; three traps (ads / bottlers / nickel-only machines), decision 1953 (7½¢ coin), Treasury says no, twist = the empty-ninth-bottle memo. Choice DIME / COIN. The Levy & Young 2004 PDF was blocked here — build run should re-try it; no Coke trade dress; President/Treasury = generic cast. New sets/props: office1950, soda_fountain, oval_office, bottle_el, vending_el, billboard_el, ghost coin (shots.md). |

## Built
(none yet in the new format)
