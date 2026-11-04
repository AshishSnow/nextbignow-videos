# Storyboard — HOW IT WORKS · EP 2 · Why your credit score doesn't know your salary. Look: LINE-ART CAST + CLEAN (STORY.md 2b). Hero = orange tie = you; lender = `lady` navy jacket (generic, role chip LENDER). FICO, Experian as plain text only: no logos, no real report layouts, no card brands.
**New vs EP 1 (inauthentic-content guard):** one big pie that fills slice by slice through the whole video (`score_pie`; the biggest slice lands fourth, the catch last), a month strip for the statement trick (`cycle_el`), a report with a circled error (`report_el`), a car on a lot (`car_el`), gauge needle (`gauge_el`). Score idea: lo-fi hip-hop (new genre), a soft tick on each slice. No Oops beat. No charts of real people, no debt shame; the hero never looks foolish, the system is what's surprising.
**Placement notes (lab sheet `lab/story_kit/storyboard_hiw_ep1_ep2.jpg`):** score_pie centre (540, 1120), r 330, top caption stays clear above y 700; hero stands bottom left at scale 0.8 on pie shots, or leaves. mini_card at top-left. Two `say()` in one row play in turn. End card: `choice_card(..., y=1120)`. i3 stamps on a white plate or at size ≥ 60: at size 44 they vanish on the green set. `phone_el` still carries old restaurant-chat text: use `phone2_el("AnnualCreditReport.com", "FREE REPORT")` in t1.

| Line | Set / shot | Cast + acting | HUD / props / caption | SFX |
|---|---|---|---|---|
| i1 | `carlot` frame 1: `car_el` with `tag_el("YOUR RATE?")` swinging, `gauge_el` above; hero lifts pay slip `form_el("SALARY")`, the gauge bounces it away | hero sus | `mini_card` HOW IT WORKS / YOUR SCORE; `say("IT DOESN'T KNOW")` → `say("YOUR SALARY")`; `series_badge` from 1.5 s | needle tick, swipe |
| i2 | `lenderdesk` MEDIUM: hero sits, `car_el` small in `thought` | hero smirk; lender | chip AGE 24; `say("GOOD JOB")`, `say("WANTS A CAR LOAN")`; US chip | pop |
| i3 | `lenderdesk`: three tags PAY · JOB · AGE stack in a column, each gets crossed out by a small `stamp_el("NOT IN IT")`, one by one | hero wow | `say("NOT IN THE SCORE")`; chip myFICO, Oct 2026 | stamp ×3 |
| i4 | `lenderdesk`: lender holds `form_el("INCOME")`, then the `gauge_el` turns away from it | lender talks; hero nods | `say("LENDERS CAN STILL ASK")`; chip THE SCORE JUST WON'T SEE IT · Experian | pop |
| i5 | `stage` navy: `score_pie` empty dark circle pops; 5 question marks, last one red | hero | `say("5 SLICES")`; chip US FICO SCORE · LENDERS MAY USE OTHER SCORES | ding |
| a1 | `stage` navy: slice 1 wedge sweep in | — | `mini_card` SLICE 1 / NEW CREDIT; `say("10%")` | tick |
| a2 | `stage` navy blur: three `card_el` (no brand) pop fast, `sign_el("RISKIER")` drop | hero sweat | chip SEVERAL ACCOUNTS, SHORT TIME · myFICO | pop ×3 |
| b1 | `stage` navy: pie returns, slice 2 wedge sweep in | — | `mini_card` SLICE 2 / MIX; `say("10% AGAIN")` | tick |
| b2 | `stage` purple: `card_el` + `car_el` small + `home_el` pop; `stamp_el("NOT REQUIRED")` slam | — | `say("NOT ONE OF EACH")`; chip myFICO | stamp |
| c1 | `stage` navy: pie returns, slice 3 sweep in | — | `mini_card` SLICE 3 / LENGTH; `say("15%")` | tick |
| c2 | `stage` teal: `year_strip_el` tiles light up in a row, `tag_el("HELPS")`, then chip | hero | `say("LONGER HELPS")`; chip NOT REQUIRED FOR A GOOD SCORE · myFICO | clicks |
| c3 | `stage` navy: pie with 3 small slices; big dark rest pulse | hero points | `say("BARELY A THIRD")` → `say("WHERE'S THE REST?")` | whoosh |
| d1 | `stage` navy: slice 4 swing in huge orange, pops out (`hl`) | hero wow | `mini_card` SLICE 4 / ON TIME; `say("35%: THE BIGGEST")`; chip THE FIRST THING LENDERS WANT TO KNOW · myFICO | big tick, ding |
| d3 | `lenderdesk`: a few red dots on `calendar_el("ON","TIME")`, then `stamp_el("NOT AUTOMATIC")` slam | hero neutral | `say("LATE CAN LOWER IT")`; chip A FEW AREN'T AN AUTOMATIC SCORE-KILLER · myFICO | stamp |
| e1 | `stage` navy: slice 5 sweep in gold, pie complete, flash | hero leans in | `mini_card` SLICE 5 / OWED; `say("30%")` → `say("THE CATCH")`; chip CARD USE IS PART OF THIS SLICE | tick, sting |
| e2 | `homedesk`: hero at table, `form_el("CARD BILL")`, `stamp_el("PAID IN FULL")` slam | hero smirk | `say("PAID IN FULL")` | stamp |
| e3 | `homedesk`: `cycle_el` strip reveals marker 1 → marker 2 flash (red) | hero looks | `say("REPORTED HERE")`; chip WHEN THE MONTHLY STATEMENT ENDS · Experian | ding, tick |
| e4 | `homedesk`: marker 3 pops after the red one; `tag_el("LOOKS USED")` on marker 2 | hero sweat | `say("USED, EVEN IF PAID")`; chip EVEN WHEN YOU PAY IN FULL · Experian | thud |
| e5 | `homedesk`: a payment coin slides left to before the red marker, tag shrinks | hero smirk | `say("PAY BEFORE IT ENDS")`; chip MAY LOWER WHAT'S REPORTED; chip NOT FINANCIAL ADVICE | pop |
| f1 | `stage` plum: full pie shrinks → flip to `report_el` big, `tag_el("INCOME")` bounces off it | hero | `mini_card` ONE MORE THING / THE REPORT; `say("ALL FROM HERE")`; chip INCOME ISN'T ON IT · Experian | whoosh |
| f1b | `stage` plum: `report_el` tilt, red question mark pop | hero sus | `say("REPORTS CAN BE WRONG")` | thud |
| f2 | `stage` plum: `report_el(err=True)` circled pops, then 5 cast heads, one highlights | hero sus | `say("1 IN 5")`, chip AN ERROR ON AT LEAST ONE REPORT · FTC 2013 | ding |
| f3 | same: `car_el` small, `tag_el("$$")` grows | hero sweat | `say("COULD COST MORE")`; chip 5% OF CONSUMERS, ERRORS THAT COULD COST THEM · FTC | thud |
| t1 | `homedesk`: `phone_el` with typed plain address, zoom in; `report_el` slides out | hero smirk | `say("FREE, EVERY WEEK")`, chip AnnualCreditReport.com; chip OTHER SITES MAY CHARGE; chip WRONG? DISPUTE IT · FTC | ding |
| t2 | `homedesk`: `gauge_el` needle doesn't move while hero reads | hero nods | `say("NO SCORE DROP")`; chip SOFT INQUIRY · myFICO + Experian | pop |
| z1 | end card = frame-1 car lot, full `score_pie` small | hero points | `say("COMMENT ONE WORD")`; `choice_card("SHOULD YOUR SALARY COUNT?","YES","NO",y=1120)` | bell, pop ×2 |
| z2 | end card holds | hero waves | `say("SAVE + SEND")`; `series_badge`; chip TO A CAR BUYER | dings |

Post: first line keyword "How your credit score works: the 5 FICO factors (US, 2026), and why your salary isn't one". firstCommentText "Should your salary count in your credit score: YES or NO?". Say in caption: "30% of your limit" is no magic line (Experian: ideally single digits); US FICO only; other scores and other countries differ; education only, not financial advice; no product recommendations.
