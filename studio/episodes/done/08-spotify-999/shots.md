# Storyboard — HOW IT WORKS · EP 1 · Why 999 plays can pay zero. Look: LINE-ART CAST + CLEAN (STORY.md 2b). Hero = orange tie = you, the singer; friend at the end = `girl` teal shirt. Spotify as plain text only: no logo, no green, no app UI lookalike.
**New vs the last 4 how-tos (inauthentic-content guard):** first HOW IT WORKS: one journey through 4 physical gates; coin pot that fills (`pot_el`), a dot grid where YOUR dots stay and everybody's double so the share shrinks on screen (`plays_grid`), a barrier with a live counter stuck at 999 (`gate_el`), then the seat switch (`subscriber` set). Score idea: indie bedroom-pop (new genre), a single note motif that drops out at the gate. No Oops beat (nobody blundered). Numbers in the pot example carry a MADE-UP NUMBERS chip the whole time.
**Placement notes (lab sheet `lab/story_kit/storyboard_hiw_ep1_ep2.jpg`):** gate_el centre x 540, feet on the floor at y≈1440, hero left of it. plays_grid centre y≈1100, w 760; pot_el upper-half label off when it's less than half full. Two `say()` in one row play one after the other (the clean look stacks them at y≈560). End card: `choice_card(..., y=1120)` so the pills clear the heads; props above y 1000. `plays_grid` frames: use a plain `stage` (the `recording` frames sit behind the dots). `phone_el` still carries old restaurant-chat text: use `phone2_el("ONE BAND", "ALL MONTH")` in e1/e2 and `phone2_el("PLAYS", "999")` in t1.

| Line | Set / shot | Cast + acting | HUD / props / caption | SFX |
|---|---|---|---|---|
| i1 | `gatehall` frame 1: big `gate_el(count="999")` closed, red; hero with `mic_el` in front, one `coin_el` bounces off the barrier | hero sweat, look up | `mini_card` HOW IT WORKS / YOUR SONG; `say("999 PLAYS")` → `say("RECORDING PAY: $0")`; chip IN THE PAST 12 MONTHS; `series_badge` from 1.5 s | counter ticks, clunk |
| i2 | `recording` MEDIUM: hero sings at `mic_el`, `notes` float, `tag_el("A TINY PRICE?")` pops | hero smirk | `say("PAID PER PLAY?")` | pop |
| i3 | `recording`: the tag gets `stamp_el("NOPE")` slam | hero wow | chip Spotify Loud & Clear FAQ, Mar 2026; `say("NO SUCH PRICE")` | stamp thud |
| i4 | `gatehall`: pull back, four `gate_el` shrink into line, numbered with 4 `numcard_el` pills POT·SLICE·LINE·MIDDLEMAN; third one flashes red | hero points | `say("4 GATES")` | ding ×4, buzz |
| a1 | `gatehall`: `pot_el(fill=0)` pops in empty | hero peers in | `mini_card` GATE 1 OF 4 / THE POT | bell |
| a2 | `stage` blue: `coin_rain` pours into `pot_el`, fill rises 0 → 0.6; `sign_el("ONE COUNTRY")` flips in | — | `say("SUBSCRIPTIONS + ADS")`; chip ABOUT 2/3 OF ITS MUSIC MONEY · Spotify | coin pour |
| a3 | `stage` blue: zoom out, the pot becomes one of many small `pot_el` in a row, sign gone | hero wow | `say("$11 BILLION+")`, chip ALL COUNTRIES · PAID TO THE MUSIC INDUSTRY IN 2025 · Spotify | chaching |
| b1 | `stage` teal: `slice_el` swap to a small `pie_coin` wedge | hero | `mini_card` GATE 2 OF 4 / YOUR SLICE | bell |
| b2 | `stage` teal: `plays_grid` dots pop one by one, a few orange, no numbers | — | `say("YOUR SHARE")`; chip OF ALL PLAYS IN THAT COUNTRY | clicks |
| b3 | `stage` purple: small `pot_el` + `tag_el("$100")`, `plays_grid(total=100, mine=5)` | — | `say("$100 POT")`, `say("100 PLAYS")`; chip MADE-UP NUMBERS (held to b6) | ding ×2 |
| b4 | same: 5 orange dots flash, `tag_el("YOU: $5")` pop | hero smirk | `say("5 OF 100")`; chip MADE-UP NUMBERS | chaching |
| b5 | same: wipe to `calendar_el("NEXT","MONTH")`, grid grows to `plays_grid(total=200, mine=5)`, orange dots stay | hero looks around | `say("SAME $100")`, `say("200 PLAYS")`; chip MADE-UP NUMBERS | clicks fast |
| b6 | same: `tag_el("YOU: $2.50")` slam on top of $5 | hero sweat | `say("HALF")`; chip NOT ONE FAN LOST; chip MADE-UP NUMBERS | thud |
| c1 | `gatehall`: `gate_el(count="0")` closed, counter rolling | hero walks up | `mini_card` GATE 3 OF 4 / THE LINE | bell |
| c2 | `gatehall`: counter rolls fast to 1,000, barrier swing up green `gate_el(open_=True, count="1,000")`; then `magnifier_el` over 3 faces | hero wow | `say("1,000 A YEAR")`; chip SPOTIFY · SINCE APRIL 2024 · RECORDING ROYALTIES; chip + ENOUGH LISTENERS, NUMBER NOT PUBLIC | tick roll, ding |
| c4 | `gatehall`: counter drops to 999, barrier slam red, coin bounces away | hero sweat | `say("999 = OUT")`; chip SONGWRITER ROYALTIES ARE SEPARATE | clunk |
| c5 | `stage` navy: `coin_el` tiny on empty floor, then `tag_el("2–3¢ A MONTH")` pop, then chip | — | `say("PENNIES")`; chip AVERAGE, TRACKS UNDER 1,000 · Spotify; chip PAYOUT MINIMUMS, USUALLY $2–$50 | ting, pop |
| c6 | `stage` navy: the pennies roll across the floor toward a bigger track's coin stack | — | `say("SHARED OUT")`; chip SPOTIFY SAYS IT DOESN'T PROFIT | coin roll |
| d1 | `gatehall`: `booth_el("MIDDLEMAN")` slides in, coin pipe stops at it | hero | `mini_card` GATE 4 OF 4 / THE MIDDLEMAN | bell |
| d2 | `gatehall` MEDIUM: `coin_rain` from above lands on `booth_el("LABEL OR DISTRIBUTOR")`, hero's hand empty | hero reaches, sweat | `say("NOT TO YOU")`; chip Spotify FAQ | coin ting |
| d3 | same: `contract_el` flips up on the counter; one coin passes to hero | hero smirk then sus | `say("YOUR DEAL DECIDES")`; chip SPOTIFY CAN'T SEE IT | paper |
| e1 | `subscriber`: whip to hero on the other side, holds `phone_el`, one band poster `sign_el("ONE BAND")`, `notes` | hero smirk | `mini_card` SWITCH SEATS / SUBSCRIBER | whoosh |
| e2 | `subscriber`: `coin_el` flies off the phone, past the band sign, into a far `pot_el` | hero wow, looks round | `say("IT GOES IN THE POT")`; chip SPLIT BY EVERYBODY'S PLAYS | coin, plop |
| e3 | `subscriber`: coin arrow straight to the band (`dim_arrow`), then `mini_card` A STUDY | hero thinks | `say("ONLY WHO YOU PLAY?")`; chip USER-CENTRIC PAY | pop |
| e4 | `stage` plum: `quote_card("a maximum of a few euros per year on average per artist", "French National Music Centre, Jan 2021")` slide up, then zoom to the chips | hero reads | chip BEYOND THE TOP 10,000 · FRANCE, 2019 DATA; chip THE STUDY DOESN'T SAY WHICH IS FAIRER | scratch, thud |
| e5 | `stage` plum: `line_chart` swings up and down, two arrows pop | hero wow | `say("BIGGER SWINGS")`; chip PRO MUSIK STUDY, SOUNDCLOUD, 2023 · via MBW | whoosh, pop |
| t1 | `recording`: phone shows play count, count fades, `contract_el` slides over | hero nods | `say("COUNT ≠ PAYCHECK")` → `say("READ YOUR DEAL")`; chip CHECK THE 1,000 LINE | ding |
| z1 | end card = frame-1 gate + `pot_el`, hero and friend | hero points | `choice_card("ONLY THE ARTISTS YOU PLAY?","YES","NO",y=1120)`; `say("COMMENT ONE WORD")` | bell, pop ×2 |
| z2 | end card holds | friend waves, holds `mic_el` | `say("SAVE + SEND")`; `series_badge`; chip TO A NEW ARTIST | dings |

Post: first line keyword "How Spotify royalties work: why 999 plays can pay zero (2026)". firstCommentText "Should your subscription pay only the artists you play: YES or NO?". Say in caption: a CNM study (France, 2019 data) and a Pro Musik SoundCloud study (2023) disagree on how much would change; rules apply to recording royalties; figures are Spotify's own; the pot example uses made-up numbers.
