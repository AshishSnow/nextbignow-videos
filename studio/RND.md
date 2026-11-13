# R&D — how the studio gets better between videos

A separate scheduled R&D run (no posting) improves the studio one focus area at a time. The video runs read
`PLAYBOOK.md`/`VOICE.md`; this file holds the rules, the rotation, the backlog and the log of experiments.

## Rules
0. **Writers' room first (since 31 Oct, STORY.md §8):** if `episodes/queue/` holds fewer than 3 REVIEWED episodes, this run writes
   1–2 complete episodes (vo_lines.py + shots.md + SOURCES, story_check 7/7 + all S-gates, a fresh-eyes subagent review) and marks
   them REVIEWED in `episodes/README.md`. Only when the queue is full does the rotation below apply. Runs: once a day, 02:41 UTC (scheduled task list, 3 Nov; 3 a day was the 31 Oct plan).
1. One focus area per run. Pick the one with the oldest "last worked" date, unless something is broken or the data
   clearly says otherwise. **Voice has priority until the narrator clearly meets `VOICE.md`'s spec.**
2. Write the hypothesis before building. Research first (primary sources, dated), then experiment in
   `$STUDIO/projects/lab_<date>`; measure before and after **on the same material** (≥ 2 different scripts for voice).
3. Keep only what measures better, or equal and simpler. Template changes must pass `bash studio/tools/smoke_test.sh`.
   Reusable code → `template/` or `lib/`; rules → `PLAYBOOK.md`/`VOICE.md`; numbers → the log below; anything not
   adopted → `studio/lab/<topic>/` with notes.
4. Never post, never touch Metricool beyond read-only analytics, never touch other brands or `fnh-engine/`, only change
   `studio/`. No MP4s or big media in git (narrator reference clips < 1 MB in `studio/voices/` only).
   Open-weight, commercial-use models only; never clone a real person; never ElevenLabs.
5. Every run also: refresh `PERFORMANCE.md` (Metricool, last 21 days); if `ALGORITHM.md` is > 3 days old, research it; if
   `topic_bank.md` has fewer than 10 Ready topics, add verified ones first (owner, 27 Oct: "topics need to improve — something interesting").
   Voice has had 3 runs in a row — give the other areas (Topics, Story, Visuals, Sound) their turn unless voice is broken.
6. Finish within 2 h; don't push template changes near the episode run (21:05 UTC).

## Focus rotation
| Area | What it covers | Last worked |
|---|---|---|
| Voice | engine, narrator reference, prosody, pace, post chain | 2026-11-10 (speed column found inert on Chatterbox; PSOLA re-time rejected; narrator_hype → default CBV) |
| Sound | music score, SFX, mix levels, loudness | 2026-10-27 (run 6: word guard + `tools/mix_check.py`) |
| Visuals | props, sets, mascot acting, transitions, safe zones, frame 1 | 2026-11-06 (3 worlds + 21 Skia props in nbnkit, incl. the credit-score redraw; writers' room run) |
| Story | hooks, re-hooks, structure, endings/takeaways, length | 2026-11-03 (hook + length audit n = 18, blind AI panel rejected, R8 re-tested) |
| Tooling | render speed, smoke tests, QA automation | 2026-11-07 (side job of the writers' room run: board_check reads whiteboard boards; human_check stress/symbol notes) |
| Analytics | what the numbers say, cover frames, captions, posting times | never as a focus (refreshed every run; 31 Oct: first rows for the 4 story-type videos, media-kit baseline in BRAND.md §5) |
| Writers' room | episode scripts + storyboards + sources in `episodes/queue/` (default job — rule 0) | 2026-11-12 (W7 overbooking (HIW) REVIEWED, human_check 6/6, story 7/7 + 6/6; props `plane_m`, `boardpass_m`, `gatedesk_m`; human_check `note number` for British 'and' in numbers) |
| Brand | BRAND.md readiness: media-kit numbers, brand-safety rules, sponsor formats, disclosure templates, community | 2026-10-31 (interactive: BRAND.md) |
| Topics | keep `topic_bank.md` interesting and verified: research what makes business stories fascinating, verify 3–5 new topics per run (primary sources), score them with PLAYBOOK §2's interest test, retire weak ones | 2026-11-13 (R&D Topics run: WHITEBOARD shelf 7 → 11 unbuilt ≥ 20/25 — W16 ZIP code 24, W17 milk date 24, W18 coin kiosk 22, W19 hidden-city 21; BIG shelf + B9 Domino's 22, B10 Wrigley 21; cash-only laws banked as a 19 backup) |

## Backlog (add ideas, strike when done)
Voice
- ~~Kokoro weak lines~~ — done 27 Oct run 3: they come from our PSOLA; per-line prosody gate (`PGATE` 0.15, template) → worst line 3.98/4.05 → 4.25.
- Chain drops on short lines: airline a3 raw 4.263 → +EQ 4.259 → +voice_clean 4.217 → +room 4.149; t3 4.327 → 4.263 at voice_clean
  (de-ess cut up to −10.8 dB). EQ is neutral → A/B a lighter de-esser and a drier room (−24 dB vs −21) per line on 3 scripts.
- ~~Chatterbox hybrid: last-word pitch move on low lines~~ — done 27 Oct run 2: `lib/end_contour.py`, low_fall −1.3 → −4.0 (gas), −1.0 → −3.5 (Costco) at ≤ 0.01 per-line UTMOS.
- Chatterbox retakes for *weak* lines too (per-line UTMOS < 4.3, e.g. Duolingo a2 = 3.91 with uptalk): extend `lab/voice_engine/take_picker.py`
  (sampled takes) to also pick by per-line UTMOS and low_fall, then run end_contour on the winner; punctuation variants as a fallback.
- Second scorer that hears intonation: UTMOSv2 or Audiobox-Aesthetics CE/PQ (arXiv 2608.09930) — licence, onnx, RAM on 2 CPUs.
- Shorter hook questions that actually rise (q_rise currently negative on long hooks, both engines; PSOLA rises on Chatterbox made it worse, 27 Oct).
- Second synthetic reference with more smile/energy; paralinguistic `[chuckle]` at one funny line.
- ~~Expressiveness metric: per-line final rise/fall~~ — done 27 Oct (`q_rise_st`, `low_fall_st` in tts_bakeoff.py).
- Magpie TTS (NVIDIA Open Model License) if it can run without torch.
- Ming-3.0-tts-0.5B (MIT; top open-licence arena score; free-text delivery instructions) — first CPU test. NeuTTS **Air** (Apache) as a
  CPU fallback (not 2E/Nano: revenue-capped licence).
- Misread lines with Chatterbox: instead of rephrasing, sample 2 extra takes (temp ~0.7) and keep the one that reads back exactly —
  code ready in `lab/voice_engine/take_picker.py` (ASR exactness first, then UTMOS).
Sound
- A/B music bed level vs avg watch; ~~sidechain ducking depth~~ (done 27 Oct run 6: word guard); SFX density per 10 s.
- **Mastering (found 27 Oct run 6): ffmpeg loudnorm never runs linear on our mixes** — pre-master PLR is 15–19 dB (printer −16.3 LUFS /
  −1.0 dBTP, gas −17.1/−0.3, Hoover −19.5/−1.0) but −11 LUFS at −1.5 dBTP needs ≤ 9.5 dB, so loudnorm falls back to *dynamic* mode
  (LRA squashed to ~2 LU; even a −14 target stays dynamic). A plain 4×-oversampled look-ahead limiter in front did not fix it (6 dB GR
  on 25 % of samples, still dynamic). Next: an explicit chain — gentle bus compressor (2:1, slow) + true-peak limiter with ≤ 3 dB GR,
  then a *linear* gain to −11 — and measure pumping (short-term loudness variance in gaps), LRA, phone ESTOI and UTMOS of the voice
  stem through the master gain curve, vs today. YouTube turns anything above −14 LUFS down (Wikipedia/YouTube −14 reference), so the
  extra 3 dB only matters on Instagram, whose normalisation is undocumented — keep −11 until measured.
- Phone-speaker check of SFX *audibility*: guard keeps words clear, but are SFX in the gaps still heard on a phone (most SFX
  energy below 300 Hz in boom/thud)? Measure phone-band SFX level vs bed; brighten booms with a 1–3 kHz click layer if needed.
Analytics
- Pull follower growth (brandSummary / IGFO*) and audience countries (demographic connector) next run — the media kit needs both (BRAND.md §5).
- YouTube vs Instagram per topic: YT winners differ (Compaq 1,332 YT vs 130 IG) — pull YTVP06/08 every run and compare after 10 posts.
Story
- Writers' room lessons (5 Nov): (a) check a neat twist against both sides: "America taxes with no form, Britain reports with no tax" sounded great and was false; the plain version was stronger; (b) read your source's own example against your hook: YouTube's example pays a million views $405, our hook said under $200; say the gap, don't hide it; (c) a threshold right after "report everything" sounds like a free pass: say what happens below it; (d) a count word must mean one kind of thing ("four cuts" was a fee, a share, a percent and a yes/no → "four stops"); (e) a US fee in a US + UK video needs "in America" aloud.
- Writers' room lessons (4 Nov, review of the first two HOW IT WORKS): (a) check a made-up example against its own story: "everyone listens twice as much" doubles your plays too, so the point vanished; (b) answer the hook aloud: "why doesn't it know your salary?" had no answer until the review; (c) the word the video is about must be said in line 1 ("a number" hid "credit score"); (d) a true fact can be harmful next to another: "zero is worse than a little" after "pay in full" reads as "carry debt", cut; (e) a qualifier on a chip doesn't correct the voice when the voice misleads: say it; (f) when your only evidence comes through the company, read the primary study and say the counter-evidence.
- Writers' room lesson (2 Nov): a how-to's twist must help the *seat* (a first-timer), not the system in general — "2,200 new applications" read as good
  news until the review noticed they go to 2022 lists; and a preference poll ("tacos or coffee") is not a choice — ask about the decision the story raised.
- Writers' room lesson (1 Nov): numeric *ranges* ("four to eight thousand") fail R5 — say "several thousand" and put the range in the caption;
  old regulator cases must say the year aloud; a how-to's "trap" step must not paint a legal category (a likely sponsor) as a scam.
- ~~Length gate~~ — tested 3 Nov, **rejected**: avg watch in *seconds* does not fall with length (rho +0.32, n = 18); "hold % of length" falls partly by arithmetic. The 80–105 s band has the best seconds (25.0, n = 4), so aim there when the story allows, no gate. IKEA (~125 s) and nickel Coke (~120 s) stay as written.
- Next Story test worth running: real comment rate by end-question type (YOUR MOVE FIGHT/FOLD vs how-to STAY/MOVE vs GYM/OFFICE) once the Pepsi rows land.
- Writers' room next: SPOT THE TRICK #2 = the airport (walk-through duty-free, $6 water vs 'street pricing' airports, currency kiosks, 'pay in home currency');
  WHO REALLY OWNS IT #1 candidates: AB InBev 'craft' beers, store brands; YOUR MOVE EP 3 candidates: Burger King Whopper Detour (A, seat = the CMO:
  TROLL / PLAY SAFE), Knight Capital (A, seat = the CTO at 9:30: HALT / TRADE), frozen-chicken tax / Ford vans (A: BOLT SEATS / PAY 25 %), LEGO 2004 (SELL PARKS / KEEP).
- ~~Validate R8~~ — done 3 Nov, n = 18: roadmap 21.7 s / 59.8 % 3-s vs none 19.9 s / 53.1 % (was "+10 points" at n = 6). Keep as cheap structure, not as a proven lever.
- Real reversal detection for story_check (good/bad polarity per line, e.g. a small lexicon or hand tags) — keyword "but" counts
  did not track retention.
- Comment test: one specific A/B question in the last line vs the friend CTA (comments ~0; owner's references 75–300 per reel).
Visuals / Story / Tooling
- **Story-kit assets still missing for queued boards (write before their build run, `board_check --strict` tells you):** `04-nickel-coke` needs
  sets office1950, oval_office, soda_fountain + props billboard_el, bottle_el, contract_el, memo_el (~~vending_el~~ written 1 Nov, use `era="1950"`) + a `MAP_US` polygon for
  `map_view` — 8 assets, ≈ 1 R&D run (the IKEA kit took one run for 3 sets + 9 props, `template/scripts/anim_story2.py` is the pattern).
  Next after that: WHO REALLY OWNS IT #1 will need a "street of shopfronts" set (shopfront_el exists) and a hub/door kit (door_el, hub_map exist).
- Tooling next: (a) `say()` could wrap to two lines itself when a caption would shrink below ~60 % (today it only scales down — the
  board_check B3 warnings are the measure: 13 of 31 captions on the two new boards); (b) board_check B4 (static rows) is a verb
  heuristic — replace it with real shot counts once anim_shots.py exists (parse SHOTLIST, compare with align.json: ≥ 1 visual change
  per 3 s); (c) a `US`/`EU`/`UK` map polygon set for `map_view` (the nickel-Coke board needs a US map); (d) render-speed profile of
  one full episode (anim_cine grade + mascot3d per frame) — never measured as a focus.
- ~~Cinematic texture~~ — done 27 Oct (interactive): `template/scripts/anim_cine.py` (lit worlds with depth, glow disc, 3D titles behind the
  hero, light rays, bokeh, DOF, film grade), default on. Next: prop **materials** (specular highlights, subtle texture on paper/metal/
  wood props, soft contact shadows everywhere), and speed (grade now ~0.22 s/frame after the 27 Oct cleanup; next: fuse the tone curve into a LUT).
- ~~Mascot upgrade~~ — done 27 Oct; ~~full-frame scenes + lit cast~~ — done 27 Oct evening (interactive, owner's references:
  "full frame… colours, more natural and 3D, change the style of clothes"): `anim_mascot3d.py` is now a lit 2.5D renderer
  (per-part normals from distance fields, key/ambient/rim light presets, contact occlusion, cast shadows), 10 looks with real
  clothes; `anim_sets.py` = full-frame sets (street/study/parlor/office/store/dusk), camera framing, foreground hand, smoke/embers/
  eyes, captions, part badge, HUD (clock, rule pill, timer, audience choice). Next: walk/run cycles with arm swing, sitting at
  a desk, 3/4 head turns, hands that grip props, more sets per topic (factory, bank, kitchen, night city), and a hair/fabric
  texture pass. Measure: does avg watch % rise on scene-heavy videos vs the disc style (compare from the next 5 posts).
- Story format from the owner's references (27 Oct): multi-part series ("Part 3") and audience choices ("comment A or B — you pick
  what happens next") get 75–300 comments per reel vs our ~0 — test a two-part story with a choice CTA and compare comments/shares.
- Photoreal background plates from a local open image model (owner's reference reels use realistic AI imagery): check licence
  (commercial use) + CPU speed at 1080×1920 on 2 cores; only for backgrounds behind our own mascot/props; label AI as we do now.
- ~~First-frame test sheet~~ — done 28 Oct run 7 (first 3 s of the 14 posted MP4s, `lab/visuals/`; no feature predicts the 3-s rate, n = 9).
- ~~Smoke test that renders video~~ — done 28 Oct run 7 (layout_check + 1 s anim.py encode of the Hoover shots).
- Props/labels that draw their own text (map pins, price signs, source chips placed by hand at y > 1465) are not nudged by the safe area:
  banana's chips still touch the bottom zone by ≤ 9 px; an optional `layout_check --strict` could flag prop text too (OCR-free: render
  with props on/off is not possible generically — needs per-prop text tagging).
- Retention per shot type: once Metricool returns per-second retention (not available now), compare scene vs disc shots.
- `_CINE_T` (window twinkle time) is set by the *previous* frame's finish() — harmless off-by-one in sequential renders, but parallel
  part renders start each part with t = 0 for the first frame's windows; set it at the top of compose() if a flicker is ever seen.

## Log
- 2026-11-03 (02:41 UTC run) | Story (+ Visuals for tonight's build) | Queue 4 REVIEWED, bank ≥ 10 Ready → rule (c); Voice/Sound/Story tied at 27 Oct; Story chosen (owner's priority, and 3 older rules had never been re-tested on n > 6).
  **Hypotheses, written first:** (1) our data supports a length gate (backlog); (2) hook wording features predict the 3-s rate; (3) R8 roadmap still separates at n ≥ 10; (4) a blind panel of simulated viewers can pre-screen hooks, if it first predicts the 18 real rates.
  **Results (18 animated reels, `lab/story/hook_length_audit.py`, `hook_panel_*`):** (1) **rejected** — length vs avg-watch seconds rho +0.32 (p 0.20); length vs hold % −0.53 (p 0.03) is largely arithmetic (hold = seconds / length); bands <80 s 18.2 s · 80–105 s 25.0 s · 105–125 s 22.4 s · 125 s+ 21.9 s. No gate; the two long queued scripts not cut. (2) **rejected** — hook words −0.24 (p 0.35), real "you/your" −0.10, ellipsis −0.17. (3) **shrunk** — roadmap 21.7 s / 23.8 % / 59.8 % 3-s (n = 11) vs none 19.9 s / 22.2 % / 53.1 % (n = 7); the 27 Oct "+10 points" was n = 6. (4) **rejected** — 5 independent Sonnet raters with different viewer personas, shuffled lists, no data: panel mean vs real 3-s **rho 0.00 (p 0.99)**, top half 55.9 % vs bottom half 58.6 %, inter-rater +0.42, so they agree with each other and not with viewers; drone (real 75.9 %) and vending (68.2 %) ranked 16th and 18th of 18. Data caveat: 4 raters answered by list position rather than the printed id, mapped back by position; one dropped an item (banana). So no hook was changed on its score. Rule added: fresh-eyes reviews judge accuracy/clarity/safety, not watchability (STORY §6). 3-s rate vs views rho +0.80 (p < 0.001): the opening is what buys reach.
  **Bug found and fixed:** README/STORY told the episode task to build Part 2 on the "second run after Part 1". The task now fires once a day (scheduled task list, 3 Nov), so Part 2 would have posted 48 h after a Part 1 that says "Part two tomorrow". Now: next run. Cadence text corrected in BRAND/PLAYBOOK/RND (1 + 1 run a day, not 2 + 3).
  **Visuals:** tonight's top entry (Pepsi P1) had only a 31 Oct lab sheet in the retired 3D cast, and `board_check --strict` passed while the board's prose named props that did not exist. Wrote props kit 6 (`anim_props6.py`: can_el, can_pile, padlock_el, calculator_el, moneybag_el, tee_el, jacket_el, envelope_el); props named in the rows. Before → after on the same board: 7 prose-only props that did not exist → 0 (a flip chart in c2 stays prose, the build can drop it); 12-row line-art sheet with guides (`lab/story_kit/storyboard_pepsi_lineart.jpg`, 0.03–0.29 s/frame). The sheet caught 3 layout problems before a render (giant bottle caps over the jet, end-card pills on the hero's face, end-card jet off the left edge), fixed, 4 placement notes in the shots.md header. Not rendered with audio; the build run still decides shots.
  Analytics: IG rows unchanged (no food-truck row yet); **YouTube still blind**: no YTVP rows after 28 Oct, and account-level views (YTEV02) stop 30 Oct, so this looks like a Metricool sync problem, not a reach problem (owner: check the YouTube connection in Metricool). First YT subscriber number: 41. ALGORITHM.md refreshed, partially: Metricool, SocialBee and OutlierKit pages were blocked (PROVENANCE_REQUIRED), only ZoomSphere's relay of Mosseri was read.
  Lesson: the bigger gain was re-testing our own rules; 3 of 4 did not survive more data. | kept: kit 6, rules, timing fix; dropped: length gate, hook-wording rules, AI hook panel — measure: Pepsi P1 real comments vs 1 real comment channel-wide on autopilot posts; panel's frozen score for food truck 47/100 (ranks low) vs its real 3-s tomorrow
- 2026-11-02 (02:41 UTC run) | Writers' room (data override of rule 0) + Visuals | Queue held 4 REVIEWED (Pepsi P1/P2, IKEA, nickel Coke) and the bank
  ≥ 10 Ready, so rule 0 didn't fire and the rotation said Voice/Sound/Story (27 Oct). Overrode it on data: the last two episode runs both built
  **HOW TO START** (drone 1 Nov, vending 2 Nov) and the drone how-to is the channel's best on every sponsor metric (3-s 75.9 %, 20 reactions on
  1,180 reach = 17 / 1,000 vs 1.1 before), but the queue held **0** HOW TO START scripts — tonight's build would have had to research from scratch.
  **Hypothesis:** a HOW TO START episode whose hook is a *mystery the steps solve* ("why would a vendor pay thousands to rent a $200 permit?") and
  whose steps are told in the order you must do them passes 7/7 + 6/6 and a fresh-eyes review, and with its assets pre-written the build needs
  0 new code. **Research:** NYC Health Mobile Food Vendors page + release 015-26 (13 Mar 2026) verified today (cap by law; ≥ 2,200 supervisory
  license applications/yr from 1 Jul 2026 for 5 yrs under LL 54 + 59 of 2026, offered to the 2022 lists; daily commissary return; ~5,800 permits;
  no list for the personal license). **WebFetch was blocked session-wide after the first batch** (permission timeout, unattended) → MyCity fees,
  DOI 2009, Queens Daily Eagle 2025 and Square stay at the 1 Nov check, marked ⚠ with a BUILD GATE + a verified-only fallback hook in SOURCES.md.
  Caught: the Eagle story is about *street vendors* (mostly carts) → hook says "food vendor", not "food truck"; the 500/1,500/200 split and an
  "11k waitlist" exist only on secondary sites → kept out. **Script:** first draft 6/7 (R7 25 s twist→end) → 7/7 + 6/6 after 3 trims. **Review**
  (independent subagent, saw only STORY/BRAND + the 3 files): **"not ready" (close)** — 9 must-fixes, all applied: hook scope, "can't sell" ambiguity,
  "buy the truck last" contradicting step 4, e3 overreach (the Mar 2026 list reopening), t1 "adds applications" ≈ permits, **the twist was false
  comfort** for a first-timer (the 2,200 go to 2022 lists) → takeaway "Not on one? Try working a truck first.", **"tacos or coffee" wasn't a decision**
  → "Still New York? STAY or MOVE?", renting read like a tip → "outside the official system" + "Back in 2009", an unsourced pinned reply. Re-check
  7/7 + 6/6 (~102 s, twist→end 18.0 s). Lesson for STORY.md: a how-to's twist must help *the seat* (the first-timer), not the industry in general.
  **Visuals:** wrote `foodtruck_el(w, open_, menu, glow, permit, col)`, `permit_el(w, price, stamped)`, set `commissary` (`template/scripts/anim_props5.py`,
  in anim.py's exec list). Before → after on the same board: `board_check --strict` FAIL (3 missing) → PASS (0 missing, 0 warnings); lab sheet of 6 rows
  with safe-zone guides (`lab/story_kit/storyboard_foodtruck_ep3.py/.jpg`), 0.04–0.33 s/frame; 2 fixes after the first sheet (COMMISSARY sign collided
  with the cold-open card → moved right; i1 captions/permit/tag re-placed), 4 placement notes in the shots.md header. Smoke test PASSED with the
  food-truck board added to its `--strict` list. Analytics: Metricool IG + YT pulls identical to the 02:40 IST snapshot (no row yet for vending EP 2,
  posted 23:30 UTC); ALGORITHM.md 2 days old → not redone. | kept — measure: EP 3's 3-s rate and saves per reach vs EP 1 (75.9 % / 12 per 1,000)
  and EP 2; comments on STAY/MOVE vs GYM/OFFICE (a story-tension question vs a preference poll)
- 2026-11-01 | Topics (+ writers' room) | Queue held 4 REVIEWED and the bank 16 Ready, so rule 0 didn't fire; Topics, Story, Sound and Voice all
  tied at 27 Oct. Chose Topics because the data said so: HOW TO START is ~40 % of the mix (STORY.md §3) but had **0** banked topics and no
  queued episode — the drone episode was researched at build time. **Hypothesis:** a verified HOW TO START shelf + one REVIEWED episode in the
  queue keeps the series at its share without build-time research, and a consumer-protection hook ("the singer") gives a how-to the curiosity
  gap the 21 Oct list-style how-to lacked (4,640 IG views but 2.9 s avg watch / 13 % 3-s). **Result:** shelf 0 → 4 (#25 home bakery TX+UK 31/35,
  #26 print-on-demand 29/35, #27 pressure washing 30/35 — not Ready until a 2nd primary source, #28 NYC food truck 32/35), all with dated
  primary links (sourcing subagent; CDPH 2026 caps + Etsy fee page + food.gov.uk were blocked here). HOW TO START EP 2 (vending) written from FTC
  primary releases (1998 Operation Vend Up Broke, 2004, 2006, 2009) + the FTC Business Opportunity Rule page; story_check first draft 4/7 R
  (R2 35-s gap, R5 three two-number ranges, R7 35 s twist→end) → 7/7 R + 6/6 S after 6 edits; fresh-eyes review "ready after must-fixes"
  (7 must: year said aloud, "charged some sellers", problem→protection order, step 4 not "the trap" (sponsor fairness), step-3 re-hook,
  VO = end card, US-only) → applied, 7/7 + 6/6 again, ~107 → ~102 s; board_check PASS 0 warnings. Retention test of the hypothesis: when
  EP 2 posts, compare its 3-s rate / avg watch with the 21 Oct list how-to and EP 1 (PERFORMANCE U2). Also wrote `vending_el` (props kit 4,
  incl. `era="1950"` for the nickel-Coke board): 0.3–0.7 s/frame, lab sheet looked at, EP 2 build brief 1 → 0 missing, nickel 8 → 7; smoke test PASSED.
- 2026-10-27 | Voice | Hypothesis: an LLM-style open TTS (Chatterbox-Turbo, MIT) conditioned on our own synthetic narrator gives more
  natural delivery than Kokoro + PSOLA, at ≥ equal intelligibility and acceptable CPU cost. Built `tools/tts_bakeoff.py`
  (engine A/B with whole + per-line UTMOS, range, wpm, ASR, RTF) and `lib/cb_turbo.py`. Results (Kokoro shipped → Chatterbox q4
  slow-ref shipped, UTMOS whole/per-line): gas i1–b2 4.474/4.43 → 4.544/4.494; gas b3–e2 4.257/4.38 → 4.336/4.459; more rows below.
  Range 18.1–18.3 → 17.0–17.2 st (still ≥ 15), ASR 0 bad lines on both. q8 LM RTF 12.7 → q4 LM RTF 1.8 at equal score.
  Reference sets pace: flat ref 186 wpm/13.2 st, slow PSOLA ref 165 wpm/16.4 st. → see "Decision" line below.
  Duolingo 91 s 4.375/4.424 → 4.519/4.484; Costco 83 s 4.340/4.405 → 4.471/4.468. New line-end metric: Chatterbox's reveal
  lines fall only −0.2…−2.5 st vs Kokoro+PSOLA −4.2…−7.2 st; PSOLA on top of Chatterbox costs −0.23 UTMOS.
  **Decision: not adopted as default** (gains are acoustic; it loses the landed endings our format needs). Kept as opt-in
  `ENGINE=chatterbox` in make_vo.py (+ `PROSODY` switch), lib/cb_turbo.py, voices/narrator_slow.*, setup downloads (q4).
  Smoke test (new tools/smoke_test.sh) passed on both engines. Next voice run: hybrid endings (see VOICE.md "Next").
- 2026-10-27 | Voice (interactive session with the owner, in parallel with the R&D run) | Deep research → narrator spec with sources
  (VOICE.md "Research basis"); 16-variant Kokoro lab (26 Oct: no global pitch lift, SPD .88/PZ 1.6 → the current default);
  Chatterbox fp32/q8 bake-off with 5 references; Qwen3-TTS 0.6B as engine (3.95) and 1.7B VoiceDesign as reference maker (too
  high-pitched); **hybrid lead:** Chatterbox with a *flat* Kokoro reference (`voices/narrator_flat_ref24k.wav`) + half-strength
  PSOLA cost only −0.005 UTMOS (4.471 → 4.466) and raised range 13.6 → 16.2 st on the Starbucks script (full PSOLA: −0.10);
  line-end melody (main's scorer, Starbucks script): Kokoro main default 4.345 / low_fall −4.3 / q_rise +0.9 / 18.2 st;
  Chatterbox flat ref 4.471 / −0.6 / −1.3 / 13.6 st; + half PSOLA 4.466 / **−0.2** / −1.2 / 16.2 st; + full PSOLA 4.368 / −0.2 / 19.2 st;
  best-of-3 takes 4.478 / +0.1. → **Half/full-strength PSOLA adds range but does NOT land the endings** (Chatterbox's last words
  resist the generic ending curve). Confirms the R&D decision: Kokoro stays default. Endings need a targeted last-word move
  (bigger, on the final stressed syllable only) or a reference whose sentences end low. | confirms Kokoro default; lead for hybrid
- 2026-10-27 (run 2) | Voice | Hypothesis: moving pitch only on the last word of `low` lines in a Chatterbox take (PSOLA on that slice,
  cross-faded in) lands reveal lines at ≤ −4 st without global PSOLA's −0.23 UTMOS. 6 versions on gas/Costco/Duolingo (lab/voice_endings/).
  Final (−4 st, start ≥ 0.5 s before last voiced frame, cap uptalk at line median, floor 85 Hz, per-line UTMOS gate 0.05):
  gas low_fall −1.3 → **−4.0**, UTMOS 4.522/4.480 → 4.513/4.476; Costco −1.0 → **−3.5**, per-line 4.474 → 4.468 (whole 4.501 → 4.380,
  whole-file score noise — per-line min 4.43 → 4.41); Duolingo −0.2 → −1.7 (moved lines −2…−3.5 each; its a2 line is a 3.91 uptalk
  line the gate skipped). Kokoro shipped on the same scripts: 4.317/4.399, 4.321/4.402, 4.382/4.428; low_fall −4.8/−4.9/−7.1.
  Question rises (+3…+4.5 st) on Chatterbox: q_rise worse (−1.8 → −2.1) → off. **Decision:** endings ON by default inside
  `ENGINE=chatterbox` (`ENDS=0` to disable); Kokoro stays the default engine (Chatterbox still: falling questions, one weak line on
  Duolingo). Also: ASR scorer now reads "$1.50" == "a dollar fifty" (Costco's 2 false "bad lines"); smoke test exercises a low line.
  Analytics: Metricool IG reel stats frozen since ~26 Oct evening IST (identical 3 pulls); YouTube numbers arrive for the first time.
- 2026-10-27 (run 3) | Voice | Hypothesis: Kokoro's weak lines (worst 3.98 gas, 4.05 airline) can be lifted to ≥ 4.2 without losing melody.
  Diagnosis first: flat Kokoro lines all score 4.43–4.52; our PSOLA prosody makes the weak ones (gas c1 4.45 → 3.93) → the planned
  Kokoro retakes were dropped unbuilt. Built a per-line prosody gate (re-render a line at 0.6/0.3 strength if PSOLA costs it > 0.15).
  Same 3 scripts, shipped chain, UTMOS whole / per-line (min): gas 4.234/4.379 (3.98) → 4.373/4.411 (4.25), range 18.1 → 17.8;
  Duolingo 4.386/4.423 (4.37) → 4.421/4.421 (4.33), 18.4 → 18.3; airline 4.394/4.390 (4.05) → 4.402/4.406 (4.25), 18.4 → 18.2;
  low_fall unchanged (−4.8/−6.6/−5.0), ASR 0 bad lines. Not adopted: global clip −7/+8 st (range 15.0), puck .1 blend default (equal).
  **Decision: `PGATE=0.15` is the template default** (`PGATE=0` disables); smoke test checks it runs; passed. lab/voice_gate/.
  Analytics: Metricool Instagram reel stats identical for the 5th pull (frozen since 26 Oct); YouTube still updates.
- 2026-10-27 | Topics (interactive session; owner: "topics need to improve — something interesting") | Hypothesis: 12 videos in a row
  used one formula ("how company X really makes money"); fresh story types (wild true stories, everyday-object economics, hidden giants,
  origin twists) will hold attention and get shared more. Built the interest test + type mix (PLAYBOOK §2) and `topic_bank.md`;
  3 research agents verified 15 candidates against primary sources (court opinions, SEC/DOJ/Mint/FAO documents, company reports) →
  16 Ready entries scored 26–32/35, with myths flagged (Pepsi jet price, Hoover "£100m", Nintendo love hotels, Kodak "hid it",
  "80% of eyewear", banana "extinction"). Hoover needs one more major outlet for the £48m before use. | kept — measure 3-s rate,
  avg watch, shares and saves by type in PERFORMANCE.md after ~5 new-type videos
- 2026-10-27 (run 4) | Topics | Trigger: topic_bank.md had **0 Ready** topics (rule 5) and the owner asked for more interesting topics.
  Hypothesis: non-F types (B everyday object, E trick, A wild story, C hidden giant, D origin twist) can be verified to primary-source
  standard and score ≥ 26/35 on the §2 interest test, giving the video runs a 2-day queue that never repeats a type. Method: 4 parallel
  research passes (12 candidates, primary sources: court opinions, DOJ, US Mint/Treasury, peer-reviewed papers, SEC, official
  histories), myth hunt per topic, my own spot-checks (Pepsi opinion jet cost: UW copy "$23 million", another copy summarised as $28M →
  VO says "over twenty million"; Common Cents Act dates conflict → "passed Congress in 2026"). **Result: 11 verified (27–30/35, all
  verifiable = 5 when limited to the listed numbers), 1 near-ready (Hoover), 2 dropped as myths/thin (Pepsi Soviet navy, hot dogs
  10 vs 8).** The interactive session had meanwhile pushed 16 Ready → merged: 5 overlapped (penny, Hoover, Pepsi jet, Nintendo,
  glasses — my extra cautions/sources added to theirs), **7 new unique entries 17–23** → bank now **23 Ready**. Myths caught that a script would likely have repeated: McDonald's Monopoly "$24M" (court/DOJ: >$13M /
  >$20M), Nintendo love hotels, the 1899 Coke contract "freezing" the price, "Toblerone left Switzerland", cake-mix egg, Oakley 1996.
  Data: by type, B/E reels averaged ~68 % 3-s / 23 s / ~1,350 views vs F ~57 % / 17.7 s / ~255 (PERFORMANCE insight I) → pick order
  in topic_bank.md starts B → E → C → A → D. Analytics: Metricool still frozen (7th identical pull, IG + YT). ALGORITHM.md is 1 day old → not redone.
- 2026-10-27 | Visuals (interactive; owner sent reference reels: cinematic AI story reels with golden light, depth of field, film
  grain and a giant 3D title behind the hero) | Built `anim_cine.py`: same shot code, new look — measured on 3 past videos (De Beers,
  gas station, airline miles): renders fine, colours kept vibrant after a second tuning pass (first pass was hazy: bloom 0.32 → 0.18,
  contrast S-curve 0.18 → 0.42, saturation 1.08 → 1.16), cost +0.19 s/frame. Hook demo with `title3d("DIAMONDS")` behind the ring.
  | kept (template default; CINE=0 to switch off)
- 2026-10-27 | Visuals (interactive; owner sent 3D-look cartoon story reels: "improve our character, not follow exactly, 3D, better colours")
  | Built `anim_mascot3d.py`: same identity (square face, orange tie), new volume and colour (shaded head + hair, royal-blue suit,
  shirt, tie, pocket square, cel-shaded limbs, hands with thumbs, shoes, ground shadow); same `guy()`/`head_el()` API → checked on
  6 poses and 4 De Beers shots (holding props, expressions, edges). Fixed a blush bug (PIL draw punched holes in the face alpha —
  also present in the old head). | kept (template default; MASCOT3D=0 to switch off)
- 2026-10-27 | Visuals (interactive; owner: "it's using full frame and looks engaging", then "not about face or dress — colours,
  more natural and 3D, change the style of clothes") | Rebuilt the cast as a lit 2.5D renderer (each part → mask → distance-field
  height → normals; one lighting pass with key, coloured ambient, rim, specular, contact AO; soft cast shadow), 10 looks incl.
  hoodie/tee/jacket/suit/dress/cardigan/overalls/coat; hero is now the orange-hoodie character. New `anim_sets.py`: 6 full-frame
  sets, set_view camera (+ matching light), close-up/OTS/foreground-hand framing, smoke/embers/eyes, `say` captions, part badge,
  HUD set. cine_grade 0.35 → 0.22 s/frame (same output, max diff 0.005). Old shots render unchanged in API (S1/S7 De Beers with
  holds checked). Cost ≈0.1 s per character per frame. | kept (template default); PLAYBOOK §6 now asks for ≥50% scene shots
- 2026-10-27 (run 5) | Story | Hypothesis: avg watch is stuck at 13–23 s at every length, so the middle leaks; measurable script
  features (hook, open-loop gaps, reversals, connectors, figures per sentence, recaps, roadmap, ending) should line up with the
  retention we have, and a script fixing the weak ones can be checked before any audio. Research (sub-agent, primary sources, in
  lab/story/NOTES.md): curiosity gaps (Kang 2009), suspense model (Ely et al. 2015), emotional volatility/reversals (Berger, Kim &
  Meyer 2021; Knight et al. 2024), story speed (Toubia et al. 2021 PNAS), causal coherence (Trabasso & van den Broek 1985), LC4MP
  load; myths flagged: Zeigarnik memory effect (meta-analysis 2025: no effect), 8-second attention span. Built `tools/story_check.py`
  (7 gates, no audio needed; real times from work/align.json) and ran it on 13 example scripts vs Instagram rows of 6 animated reels
  (Spearman, n = 6): **item labels rho +0.93 with avg-watch % of length; roadmap 29–34 % (Costco, Starbucks, Planet Fitness, printer
  ink; + restaurant 33 %) vs none 19–24 % (Amazon, Chick-fil-A)**; keyword reversal/"but" counts ran the other way (−0.60/−0.72) →
  info only, not gates; hook length not punished (+0.77, confounded). Before/after on the same material (Monopoly, same facts):
  4/7 → 6/7, longest stretch without a question/teaser 38 → 25 s, twist→end 22 → 17 s, roadmap none → "three moves" (+3 s).
  Finding: the last 5 videos (Visa → Monopoly) all dropped the roadmap the older winners had. **Kept:** story_check in PLAYBOOK §4
  (+ QA 4b) and smoke test; R8 roadmap per type. Not validated on views yet (Metricool frozen, 9th identical pull) → prediction
  in PERFORMANCE K. ALGORITHM.md 1 day old → not redone. No template code changed.
- 2026-10-27 (run 6) | Sound | Hypothesis: on a phone speaker, SFX hits and loud notes land on top of words more often than the
  mix.py "VO/bed ≥ 14 dB" print suggests (it measures whole lines with a 150 Hz high-pass); a word guard that keeps the bed ≥ 12 dB under
  the voice in the phone band (300 Hz–10 kHz, 50 ms bed windows vs 300 ms voice level, max dip 10 dB) lifts the worst moments to the
  ≥ 10 LU commentary-over-music recommendation (Torcoli et al., JAES 67(12) 2019; non-experts prefer ~4 LU more) and raises
  intelligibility, without changing loudness. Built `tools/mix_check.py` (per-line + 400 ms momentary loudness difference voice − bed,
  K-weighted, phone band; phone + full-band ESTOI; I/TP/LRA) and `lab/sound/` (hook.py, soundlab.py). Same VO/music/SFX, rebuilt from
  examples/ (Kokoro default VO): **printer ink** momentary LD p5 8.5 → 12.1 LU, windows < 10 LU 6.2 → 2.6 %, line min 12.7 → 15.3,
  ESTOI phone 0.952 → 0.962 (full 0.947 → 0.959); **gas station** p5 7.5 → 12.0, < 10 LU 8.3 → 3.2 %, line min 8.3 (b2 under 10) → 12.5,
  ESTOI 0.950 → 0.960 (0.946 → 0.956); **Hoover** p5 9.7 → 13.0, < 10 LU 5.3 → 2.1 %, line min 9.0 (d5) → 17.1, ESTOI 0.952 → 0.959
  (0.940 → 0.950). I/TP unchanged (−11.7…−11.8 / −1.5). Cost: bed −1.6 LU during speech, −0.7 LU in gaps (gas); parakeet ASR on the
  phone-filtered final mix: WER 0.119 → 0.114 (gas), 0.106 → 0.106 (Hoover; errors are number spellings) → no regression. Max dip 18 vs
  10 dB: equal within 0.6 % → kept 10 (SFX keep punch). Guard 10 dB: weaker (p5 11.4). **Kept:** `bed_carve.guard()` default in
  template mix.py (`GUARD=12`, 0 = off; lib == lab output to 1e-8), mix.py saves work/stem_vo.wav + stem_bed.wav and prints the
  loudnorm mode; template TP −1.0 → −1.5 dBTP (examples since Hoover already used −1.5; template had drifted); smoke test now checks
  the guard (synthetic bed: p5 5.1 → 10.6 LU); setup installs pystoi + pyloudnorm (MIT). Found, not fixed: loudnorm runs in dynamic mode
  on every mix (backlog). Analytics: IG pull ≈ identical to 01:45 IST (±3 views), De Beers still 0 (same-day), YouTube rows frozen
  since 27 Oct. ALGORITHM.md 1 day old → not redone.
- 2026-10-28 (run 7) | Visuals | Bank had 20 Ready → not Topics; Visuals/Tooling never worked → Visuals. Hypothesis A (data): something
  measurable in the first 3 s (frame-0 content, caption timing, motion, cuts, colour) explains why some reels lose viewers at 3 s (Duolingo
  24.8 % vs printer 73.7 %). Hypothesis B (craft): captions land in the platform UI (IG/YT overlays) more often than PLAYBOOK §6 assumes,
  and the caption helpers can keep them out automatically without changing the look. Research: measured app safe zones (adchecklab,
  verified 28 Sep 2026: IG organic 250/319/86/119 px; Meta ads 14 %/35 %/6 %), ClipSpeed (Sep 2026: YT ~288/288/140), Reap (7 Sep 2026: no
  official organic specs exist). **A — rejected:** `lab/visuals/first3s_features.py` on the 14 posted MP4s (hosting branches) vs IG 3-s rate,
  n = 9: every feature |rho| ≤ 0.27 (≤ 0.58 without Duolingo, none p < 0.1); 5 reels opened on an empty disc (mean 3-s 56.5 %) vs 4 with
  object + caption (57.6 %; 68.5 % without Duolingo, whose first 3 s look like gas station's) → topic/hook line decide (PERFORMANCE Q).
  **B — kept:** built `tools/layout_check.py` (renders each sampled frame twice, captions on/off, diff = exact caption pixels; zones = PLAYBOOK;
  `--fake-align` needs no audio) and ran it on all 15 examples rebuilt with the template (590 frames, every 3 s + first 3 s ×9). Before → after
  the template fix, same shots and timings: frames with captions in a UI zone **51 → 17** (settled, excluding full-width whip blurs 47 → 13),
  **in the first 3 s 16 → 2** (Hoover 9 → 0: the 3D "HOOVER" title's extrusion reached x 975; gas station 4 → 0: unclamped lead line to x 981),
  right-edge hits 16 → 3, bottom 17 → 8 (banana source chips at y ≈ 1550 now stop at 1505–1509), De Beers 4 → 0, airline 2 → 0. Remaining:
  ≤ 231-px anti-alias specks (Chick-fil-A, Costco), Hoover t = 39/87 s hairlines, whip transitions. Render cost 1.25 s/frame both ways.
  Template: ed_el lead/tail fit `maxw`; `safe_xy()` + `SAFE` switch in anim_base; ed_show/say/title3d/hud_rule/hud_choice + every chip nudge
  inside (< 220 px intrusions only); say max_w 860 → 800; title3d fits visible width incl. extrusion/shadow and centres the visible mass;
  chip max 800 px; part_badge title ≤ 600 px; hud_choice y 1480 → 1420, width 900 → 800; hud_clock y 262 → 272. Smoke test now renders video
  (layout_check on the Hoover shots + 1 s anim.py encode); passed. PLAYBOOK §6/§8 updated. Analytics: IG + YT pulls identical to 06:00 IST
  (no rows for Monopoly/Hoover/banana yet). ALGORITHM.md 2 days old → not redone.
- 2026-10-31 (run 8, scheduled 08:41 UTC) | Writers' room (rule 0: queue held 2 REVIEWED < 3) | Hypothesis: two complete episodes in the new
  format — a SPOT THE TRICK set in one store with the strongest trick happening *after* the viewer leaves, and a YOUR MOVE with a CEO seat
  and a coin-shaped dilemma — pass story_check 7/7 + 6/6 and an independent fresh-eyes review, and give the next two video runs something
  that can be *sent* and *answered* (PERFORMANCE S: reactions 1.6 / 1,000 reach, comments 0 on all 29 posts). Research: 2 research
  subagents (primary sources: Inter IKEA FY25 release, Norton/Mochon/Ariely 2012 PDF, UCL lecture listing, IKEA history page, Ingka
  newsroom, Fortune 2023; Levy & Young abstract + Young & Levy WP 2013-06, 1920 and 1983 court records, Coca-Cola history pages, NPR
  Planet Money, Emory Report, Coin World) + my own spot checks of the IKEA FY25 page and the IKEA-effect PDF. Myths caught and kept out:
  "60 % unplanned" as a study (it is Penn's estimate), "Harvard and Duke", "the 1899 contract froze the price until 1959", "92¢ from
  1899", a quoted Woodruff letter (none exists), "nickel-plus-penny machines", "30 % come just to eat". Built: `episodes/queue/03-ikea-maze`
  (SPOT THE TRICK #1, type E, 7/7 + 6/6, ~125 s est.) and `episodes/queue/04-nickel-coke` (YOUR MOVE EP 2, type B, single part, 7/7 + 6/6,
  ~120 s est.), each with vo_lines.py + shots.md + SOURCES.md. Fresh-eyes reviews (two independent subagents, given only STORY/BRAND +
  the three files): both "ready after must-fixes" — 7 + 7 must-fixes applied (IKEA: yellow-bag trade dress, unsupported "every store",
  attribution beyond sources, "sells you the work" framing, a missing Beat-it, verbless takeaway; Coke: New York 6¢ was Dec 1950 = before
  the 1953 ask (chronology), price-fixing cuts both ways, "a dime" undefined for UK/EU ears, the decision never posed before the outcome,
  Treasury quote credited to the wrong source, 1886 was a fountain glass, stressed-word tags) + most should-fixes. Result: queue = 4
  REVIEWED (pilot P1/P2 + #3 + #4), types A/A/E/B, series mix 3 YOUR MOVE : 1 SPOT THE TRICK. Analytics: first Instagram rows for the
  four story-type videos (PERFORMANCE S–V; media-kit baseline into BRAND.md §5); ALGORITHM.md refreshed (Mosseri 16/23 Oct on sends,
  AI content and scheduling; YouTube AI-label rules 27 May 2026; Shorts originality 1 Oct 2026). No template code changed; no render.
  | kept — measure: sends + saves + comments per 1,000 reach and comment count on #3/#4 vs the 1.6 baseline; hold % of length vs 15–23 %
- 2026-10-31 | Story + Brand (interactive; owner 30 Oct: "story line and everything need to be good, and topic… later I will get brand deals")
  | Data (Metricool 31 Oct 00:30 IST, 16 animated reels): story-shaped videos hold longest (Monopoly 31.2 s avg = channel best) but
  sends/saves/comments ≈ 0 and reach per reel fell ~1,300 → ~150 (27–28 Oct); Instagram ranks on watch time + sends per reach.
  Built: STORY.md (hero = "you", three series YOUR MOVE / SPOT THE TRICK / WHO REALLY OWNS IT, beat sheets, writing rules, signature
  beats incl. one "Oops."), BRAND.md (what sponsors buy, YPP/creator-marketplace eligibility, brand-safety rules, sponsor formats,
  disclosure, media-kit metrics, cadence), story_check S-gates (series, seat, stakes ≤ 15 s, series ending, Oops ≤ 1, part logic;
  "problem"/"question" now count as roadmap labels), writers' room `episodes/` with the pilot YOUR MOVE EP 1 Parts 1–2 (Pepsi jet;
  both 7/7 R + 6/6 S), PLAYBOOK gates (seat + choice, brand-safe) + posting (2 a day at 00:00/05:00 IST, firstCommentText = choice).
  Scheduled tasks: episodes 16:05 + 21:05 UTC; R&D → writers' room 3×/day. | kept; measure: sends + comments per 1,000 reach on the
  first 5 episodes vs the 16 animated reels before (≈ 0)
- 2026-10-31 (run 9, scheduled 08:41 UTC) | Tooling (rule 0: queue = 4 REVIEWED ≥ 3; bank 16 Ready ≥ 10; Tooling "never" worked) |
  Hypothesis: the four queued storyboards contain defects a build run would only meet at render time (assets that do not exist in the
  template, captions that the `say()` helper shrinks until they are unreadable, rows that do not match the script, missing signature
  beats), and a pre-flight that parses `vo_lines.py` + `shots.md` against the template's registry can find them in < 1 s and hand the
  build run a BUILD BRIEF. Built `tools/board_check.py` (B1 rows↔lines/order, B2 sets/props/looks vs `def`/`_FLOOR`/`LOOKS` registry,
  B3 caption widths with the real Anton/Inter/Playfair fonts — say < 60 %, chip < 19 px, quote > 5 lines, hud_rule > 560 px — B4 rows
  ≥ 4 s without a visible change, B5 badge/cold-open/one-Oops/series end card; `--all`, `--strict`, `--json`; 0.1 s for 4 boards).
  **Before (4 boards, hand-written headers):** 0 failures, **13 of 31 `say()` captions on the two new boards would have rendered at
  42–57 % (63–85 px tall)**, 2 header-listed props never used in a row (IKEA `arrow_floor`, `tray_el`), 2 rows naming a set that does
  not exist ("bedroom" vs `bedroom90s`), 1 reuse claim that is false (nickel Coke "US map" — `map_view` is Latin America only), 16
  assets to write (IKEA 8, Coke 8). Negative test: a copy of the pilot with a dropped row, a duplicated row, no badge and no end card →
  5 FAILs, exit 1. **After** the board fixes (captions split into two `say()` lines or shortened, set names corrected, the two props
  placed in rows, the US-map gap written into the board + README): 0 failures, 0 caption warnings, 9 static-row warnings left
  (heuristic, info). Kept: tool + a `board_check` line in smoke_test.sh (all queue boards parse; the pilot passes `--strict`, so the
  story kit must stay complete), rules in PLAYBOOK §7, STORY §7, episodes/README. Not changed: template code. Analytics: Metricool
  pull identical to 31 Oct 14:30 IST (no post since 28 Oct); first account-level numbers: 57 followers (53 → 57 over 24–29 Oct),
  account reach 3,076 (25 Oct) → 436 (28 Oct) → 8 (30 Oct) with nothing posted; IG country demographics return no rows (< 100
  followers). ALGORITHM.md dated today → not redone. | kept — measure: the build run's time-to-first-test-frame and whether any
  "missing asset" surprises survive the brief; caption readability on the rendered #3/#4 contact sheets
  Follow-up (same session): story kit `template/scripts/anim_story.py` (cold_open, series_badge, oops_beat, quote_card, choice_card,
  set_front occluder; sets bedroom90s / schoolyard / courtroom; props jumpjet_el, crt_tv_el, catalog_el, coupon_el, mailbox_el), part_badge
  subtitle right-aligned (never meets the cold-open card); pilot storyboard rendered (`lab/story_kit/`); fresh-eyes review of the pilot →
  7 must-fixes applied (chronology: PepsiCo sued first; cheque returned; 1996 ad change ≠ admission; FIGHT/FOLD + JOKE/DEAL choices;
  "put up" not "lend"; Statute of Frauds wording). smoke_test PASSED (video path loads the kit).
- 2026-10-31 (run 10, scheduled 12:41 UTC) | Visuals (rule 0: queue = 4 REVIEWED ≥ 3; bank 16 Ready ≥ 10; rotation: Sound/Story/Topics/Visuals
  all 27–28 Oct — Visuals chosen because the 21:05 UTC build is `03-ikea-maze` and its BUILD BRIEF listed 8 assets that did not exist, which
  the build run would otherwise have to write inside its own 90–150 min) | Hypothesis: the IKEA board's missing sets/props can be written in the
  story-kit style (lit, generic, no trade dress) so that `board_check --strict` passes and every storyboard row renders readably inside the
  safe zone with the existing cast, at ≤ 0.5 s draw cost per frame. Built `template/scripts/anim_story2.py` (loaded by anim.py after
  anim_story.py): sets `maze_store` (one-way path: dashed snaking line + perspective `arrow_floor` decals, room-set alcoves, far EXIT sign),
  `market_hall` (dark high ceiling, racks of cardboard boxes, SELF-SERVE sign), `store_cafe` (windows, MENU board, counter with heat lamps, long
  tables); props `bin_el` (4 item kinds), `arrow_floor`, `flatpack_el(built)`, `tray_el`, `shortcut_door_el(open_)`, + `exit_sign_el(mirror)`,
  `list_el`, `turnstile_el`, `heart_el` the rows also need. **Before → after on the same board:** `board_check 03-ikea-maze --strict` FAIL
  (8 missing) → PASS (0 missing, 0 failures); queue total 16 → 8 missing assets (all nickel-Coke). Lab render of 12 rows with safe-zone guides
  (`lab/story_kit/storyboard_ikea_st1.py` + `.jpg`): every caption inside the zones, hero/cast/props read on a phone-size thumbnail; three
  look fixes after the first sheet (arrows were invisible on the pale floor → darker + a snaking dashed path; candle pile read as blank blocks →
  shaded cylinders with wicks; flat box too thin → real box with top/side faces). Draw cost 0.07–0.52 s per frame before the grade (sets are
  cached after the first frame). smoke_test PASSED twice (video path loads the new kit; board_check now also runs `--strict` on the IKEA board
  so the kit must stay complete). Kept: anim_story2.py, anim.py exec list, smoke_test line, 4 shot-placement notes in the IKEA shots.md header
  (BEAT IT captions at y≈700/830, bin CU placement, one-word pills, staff re-dress dict). Analytics: Metricool IG + YT pulls identical to
  31 Oct 14:30 IST (nothing posted since 28 Oct; glasses reel still PENDING for 19:30 IST). ALGORITHM.md dated today → not redone.
  | kept — measure: the 21:05 UTC build's time-to-first-test-frame and whether it needs any asset beyond the kit; caption readability on its contact sheet
- 2026-11-04 | Writers' room (focus a: queue held 0 REVIEWED HOW IT WORKS / HOW TO START) | Hypothesis: a HOW IT WORKS can stay one picture per beat in the clean look and still pass all gates and an independent attack on clarity, accuracy and brand safety. Wrote H1 Spotify (four physical gates, dot grid where your share visibly shrinks, seat switch to subscriber) and H2 credit score (one pie filling through the video, statement timing strip, the report). **Result:** story_check 7/7 + 6/6 both, board_check --strict PASS 0 missing both; fresh-eyes "ready after must-fixes" both (6 + 9 must-fixes, all applied; one was a real logic error in our own example, one a line that could read as "carry debt"). Lab sheet 16 frames looked at: overlapping `say()` in stills is a lab artefact only; tags too wide side by side; stamps at size 44 vanish on green; `choice_card` default y hits heads, use y=1120; `phone_el` shows old restaurant text. New: props kit 8 (`anim_props8.py`), 6 clean sets, `gate`/`slice` labels + `gates`/`slices` count promise in story_check, HOW IT WORKS beat sheet in STORY.md. No viewer data yet: first test = insight Z. Length estimate 131–135 s by story_check's 0.40 s/word, above the 80–105 s band; left as written because insight X found no seconds penalty, but the next writer should aim shorter. | kept
- 2026-11-05 | Writers' room (focus a: queue held 1 REVIEWED HOW IT WORKS / HOW TO START) | Hypothesis: a how-to with a tax question anyone with a closet can use, and an explainer with no gates or pot, can both pass all gates and a hostile review, and be ready to build with 0 new code. **Result:** T2 reselling (HOW TO START EP 5) and H3 Shorts money (HOW IT WORKS EP 3): story_check first drafts 5/7 and 4/7 → 7/7 + 6/6 both; board_check --strict PASS, 0 missing both; ~127 s and ~137 s by estimate (fixes added ~20 s, trimmed back). Fresh-eyes "ready after must-fixes" both: 10 + 11 must-fixes, all applied, two of them changed the core of the episode (a false twist; the source's own example contradicting the hook). Queue: REVIEWED HOW IT WORKS / HOW TO START 1 → 3. **Fetching:** subagents hit PROVENANCE_REQUIRED on every guessed URL again; WebSearch in the parent first, then a web-fetch agent on the returned URLs, worked on all but 2 pages (the rule in PLAYBOOK §3 holds across agents). **Visuals:** 11 Skia props + 2 held worlds in nbnkit; 16-frame lab sheet looked at twice. It caught: Anton has no → or ≠ or ≈ (tofu box in the caption), `line_meter` label under the hero, tank label behind the liquid. **Bugs found:** `tools/smoke_test.sh` had been dead since the nbnkit folder landed (5 Nov): `cp` without -r stops it at line 9 with `set -e`, so the template had no working test; fixed, PASSED, new boards added to its --strict list. board_check's registry didn't read nbnkit, so Skia props looked missing; fixed. Analytics: IG rows unchanged from the 02:40 IST pull; Spotify EP 1 has no row yet; YouTube rows stop at vending (2 Nov). ALGORITHM.md is 1 day old → not redone. No render with audio. | kept — measure: EP 5 saves ≥ 10 / 1,000 reach + comments on FAIR / NOSY; EP 3 against insight Z
- 2026-11-06 | Writers' room (focus a: queue held 2 REVIEWED HOW IT WORKS / HOW TO START) | Hypothesis: a how-to whose hook is a law you can feel (jail for a muffin) and an explainer held in one object (an elevator showing a price) can pass all gates and a hostile review with 0 assets left for the build. **Result:** #25 home bakery (HOW TO START EP 6) + H4 hotel fees (HOW IT WORKS EP 4): story_check first drafts 5/7 and 6/7 → 7/7 + 6/6 both, board_check --strict PASS, 0 missing both. Fresh-eyes "ready after must-fixes" both: 9 + 8 must-fixes, all applied. **Three caught real errors in our own lines, all checked against the source pages:** "you're the only check" (Texas DSHS keeps complaint records and holds emergency powers), "in England it's recommended" (only the certificate is; training is required), "only tax can come later" (optional extras too); a fourth was stating a 2019 commission practice in the present while dropping the author's doubt. The review's lead also found StubHub's $10M FTC settlement (Apr 2026), which closes a loop inside the hotel episode. Fixes grew the bakery to ~173 s by estimate; cut back to ~150 s by moving the mail rule to a chip and dropping one worked price. Still long: the next writer should scope a rule-heavy how-to to one state + one country from the first draft. Queue: REVIEWED 2 → 4. **Visuals:** home_kitchen, hotel_lobby, car_lot + 21 props in nbnkit; the credit-score props (the next build) redrawn in Skia, its board mapped; 3 lab sheets looked at, two fixes (stamp hid its label word, receipt total overlapped). story_check knows `floors`. **Found in the read-only pull:** reselling failed on Instagram (planner status ERROR, "Media container not created"), YouTube fine; rule added in PLAYBOOK §6; owner told. ALGORITHM.md: 4 dated rows, no ranking change. Fetching: subagent got PROVENANCE_REQUIRED once on a search-returned Texas URL; the reviewer opened it later. | kept
- 2026-11-06 | Story/writing (owner: "research how to write like a human") | Research subagent → WRITING.md (21 rules) + tools/human_check.py (H1–H6). Baseline: credit script 1/6 (tells: picture this / here's the catch / here's why; But/So/And 27 %; "Slice N" template ×5; no person), queued hotel 2/6, shorts-money 3/6, bakery 3/6. Contractions (1.00) and sentence-length CV (0.60) were already fine. Links: en.wikipedia.org/wiki/Wikipedia:WikiProject_AI_Cleanup · arxiv.org/abs/2406.07016 · cmu.edu/dietrich/news/news-stories/2025/large-language-models-writing-text · support.gptzero.me (burstiness) · vanderburg.org/etc/quotes/provost-five · npr.org/2023/02/17/1156597697 · edis.ifas.ufl.edu/publication/wc193 · rosetta.to/u/vidiq/how-jenny-hoyos-actually-makes-viral-shorts · simonwillison.net/2024/Sep/15/how-to-succeed-in-mrbeast-production · journals.sagepub.com/doi/10.1177/009365087014004005 · elevenlabs.io/docs (numbers, pauses).
- 2026-11-07 (02:42 UTC run) | Writers' room (focus a: 0 REVIEWED whiteboard episodes that pass human_check; the queue's 11/12/13 score 2–3/6) | **Hypothesis:** two whiteboard HOW IT WORKS scripts on the owner's order (W1 → W4 built live → W6) can pass human_check --strict 6/6, story_check 7/7 + 6/6 and board_check --strict with 0 missing assets, and survive an independent attack, inside one run. **Research:** two sourcing subagents (primary pages: Groundwork + CR + Instacart blog + NY AG + FTC 2025/2026; FTC complaint ¶7/¶113, order, 25 Sep 2025 + 17 Sep 2026 releases, Amazon statement, GOV.UK) + one verbatim re-read of the FTC release/complaint. **Result:** both REVIEWED. First drafts: same cart human 4/6 (flat run, contractions 0.83), story 5/7 (2 numbers in a sentence; S2), 143 s → cut to ~129 s; Prime human 4/6 ('the' opener 19 %, 'The FTC…' skeleton ×4, an -ing tail), story 4/7 (hook not a question, R2 gap 44 s, no 'who' in the CTA). Fresh-eyes reviews (no context, only the files): both 'ready after must-fixes' — 8 + 10 must-fixes, mostly **accuracy/attribution, not voice** ('a handful of stores' was wrong — it was 10 retail partners and random *shoppers*; 'negligible' came from the CR statement, not the blog; present tense for a flow that changed in Apr 2023; '$200' is a total cap for some; 'a year later' at 11 months) + 7 stress-word typos. All applied; re-gated 6/6, 7/7, 6/6. **Visuals:** 10 board props written into `nbnkit/board.py` (`tag_m`, `carton_m`, `phone_m`, `cart_m`, `coin_m`, `cursor_m`, `button_m`, `door_m`, `maze_m` (deterministic DFS maze + green solve path), `helmet_m`); `browser_m` takes url/title (defaults unchanged); lab sheet `lab/story_kit/storyboard_w1_w6.py` (8 frames mid-draw + done, looked at: helmet redrawn once, carton lid moved behind the eggs). **Tooling:** board_check now reads whiteboard boards (`| Row | Line(s) |`, spans 'a1–a3', whiteboard B5, marker verbs count as change) — before: the built export board = 17 failures (unreadable), after: 1 (a real note row); old boards unchanged (7/7 PASS). human_check prints `note stress` / `note symbols` (not gates): audit of 40 scripts → 1 real miss (bakery a5, fixed). Rules 22–24 in WRITING.md. Smoke test PASSED (1 m 14 s). **Rebase found the NOTEBOOK look** (paper.py, pushed 08:32 IST by the owner's session): board-module props (house_m, stamp_m and today's 10) still drew in marker on paper because they resolve ink/hatch/mtext in nbnkit.board's namespace → paper.py now rebinds those names on the module (only when the notebook look runs). Before/after lab frame: marker outlines + blue hatch on ruled paper → graphite outlines, pencil shading, Caveat handwriting; smoke test PASSED again. | kept — measure: the build run needs 0 new drawings for either board; IG 3-s and saves vs the currency-button (same look, same series)
- 2026-11-08 (02:42 UTC run) | Writers' room (focus a: 1 REVIEWED whiteboard episode in the queue, W1 same cart) | **Hypothesis:** the room can reach 3 REVIEWED whiteboard scripts in one run *and* fix the rotation gap (queue held only HOW IT WORKS) by writing one HOW TO START (T9) + the next priority HOW IT WORKS (W2), each passing human_check --strict 6/6, story_check 7/7 + 6/6, board_check --strict with 0 missing, and an independent attack. **Research:** two sourcing subagents on primary pages (16 CFR 435 via govinfo, FTC business guide, FR 2026-18853 = no 2026 penalty change, FTC Fashion Nova 2020, legislation.gov.uk CRA s.28 + CCR 2013, GOV.UK 5 Nov 2026; Boston Fed 10-3 Aug 2010 PDF, Nilson 2024 press release, Richmond Fed 2011, St. Louis Fed Apr 2026, EPC May 2024, Visa surcharge Q&A, GOV.UK 2018, EU 2015/751) + 15 USC 1666f read on govinfo. Caught before writing: no "$54,540" 2026 penalty exists; Agarwal 2023's $15bn is between cardholders (US data), not from cash payers; Boston Fed Feb vs Aug 2010 numbers differ. **Result:** both REVIEWED, 3 REVIEWED whiteboard in the queue (17, 15, 18). First drafts: dropship human 6/6 but story 3/7 + 4/6 (hook 18 words, no seat in 3 lines, no stakes by 15 s, 2 numbers in a sentence, tail 21 s, no takeaway verb), 5 rounds to 7/7; cash human 4/6 (flat run, -ing tail), story 6/7 (R2 26-s gap), 139 → 135 s. Fresh-eyes reviews: both "ready after must-fixes" — 7 + 5 must-fixes, again **mostly scope and definitions, not voice** (UK delivers vs US ships; the study's "cash" includes debit; a rebuttal that answered a different claim; an unsourced "most beginners"; a settlement read as a fine) + 2 TTS risks ("two-day" → "today", "US" → "us"). All applied, re-gated 6/6, 7/7, 6/6. **Visuals:** 7 board props written into `nbnkit/board.py` (`parcel_m`, `lamp_m`, `ship_m`, `giftcard_m`, `cup_m`, `cash_m`, `wallet_m`), lab frames looked at (gift-card label re-fit, wallet "0" moved into the pocket); smoke_test PASSED. **Tooling:** human_check prints `note caps …` for acronyms that read as words (US/IT/OK…): 5 hits in older queue scripts (11 ×2, 12, 13, and our own 17 — fixed). WRITING.md rules 26 (caps) + 27 (study definitions, rebuttal scope). **Measured:** gates as above; review must-fixes 7 + 5 (7 Nov: 8 + 10). **Next:** whiteboard BIG (B3 Michelin — verify first-guide year on a Michelin page) then W7 overbooking; rewrite 11/12/13 with the caps fix.
- 2026-11-09 (02:41 UTC run) | Writers' room (focus a: 2 REVIEWED whiteboard episodes, both HOW IT WORKS — no BIG or HOW TO ready for the rotation) | **Hypothesis:** a BIG story built to end on a copyable rule (insight AL: BIGs hold least and earn ~0 saves) and a UK how-to with a surprising legal line can both pass human_check --strict 6/6, story_check 7/7 + 6/6 and a hostile review with 0 assets left for the build. **Result: yes.** B6 Netflix 2011 → queue/19 (first draft human_check 5/6, story 4/7: four 2-figure sentences, a 32-s gap without a turn, 19 s tail; fixed → 6/6, 7/7 + 6/6, ~132 s est.) and T8 childminding → queue/20 (first draft 4/6 + 5/7 + 5/6: 'Step N:' template ×4, 'enhanced' flagged, no seat line, 147 s est.; fixed → 6/6, 7/7 + 6/6, ~142 s est.). Both fresh-eyes reviews 'ready after must-fixes', 8 must-fixes applied; as on 7–8 Nov the catches were **scope and logic, not voice**: a carve-out that hit the seat (friend = 3 h), a fee that didn't fit the scenario's ages (£35 vs £103), a reaction line that contradicted the story just told (back down), an unsourced adjective ('furious'), a period word that rounded the record ('one summer'). New rules WRITING 29–31. **Tooling:** `human_check.py` now prints `note memory …` for narrator reactions told as a past discovery ("I didn't expect…", "when I…") — audit of 13 queue + 30 example scripts: 1 hit (queue/18 cash rewards d5), fixed, still 6/6 + 7/7. **Visuals:** `disc_m`, `tv_m`, `clock_m` (shaded n-hour wedge), `firstaid_m` (green first-aid cross, not the Red Cross emblem) in nbnkit/board.py; lab sheet looked at (lab/story_kit/props_9nov.jpg); smoke test PASSED. Metricool: IG rows unchanged since the 9 Nov 02:45 IST pull (dropship has no row yet), YouTube import still stuck at 3 Nov; ALGORITHM.md 3 days old (not > 3) → not re-researched. Next: W7 overbooking (HIW) + a whiteboard HOW TO (T11/T12), or rewrite 13 hotel fees; judge Netflix on saves/1,000 reach vs Southwest/Coca-Cola (0–1 saves).
- 2026-11-10 (02:41 UTC run) | Voice (focus c: queue held 3 REVIEWED whiteboard episodes = full; WHITEBOARD shelf holds exactly 8 unbuilt topics ≥ 20/25 (W3, W5, W7–W12; W4 = currency button, built) = full; oldest areas Voice + Sound 27 Oct, Voice has priority) | **Hypothesis:** the line speeds the last three episode runs tuned (0.94–0.97) don't reach Chatterbox; a real per-line PSOLA speed can put brisk's ~185 wpm phrase rate inside 160–180 for ≤ 0.02 per-line UTMOS; and the owner's 8 Nov `narrator_hype` reference beats brisk on the next two queued scripts. **Result:** (1) confirmed — `make_vo.py` never passes a speed to Chatterbox; the 7/10 Nov pace "gains" were script/take differences (VOICE.md corrected). (2) PSOLA re-time costs 0.06–0.09 per-line UTMOS for ±4–6 % → rejected (`lab/voice_engine/pace_lab.py` kept for future pace A/Bs on the same audio). (3) hype vs brisk, first 10 lines of 19 Netflix + 20 childminding, 2 takes each: per-line 4.492 vs 4.469 / 4.479 vs 4.423, min 4.40 vs 4.29 / 4.40 vs 4.12, range +2.0 / +0.9 st, low_fall −4.2 vs −1.4 / −3.6 vs −2.3, phrase rate 170 vs 184 / 183 vs 193, ASR bad 0 vs 2 → **`CBV` default = narrator_hype** (template make_vo; smoke test PASSED; CBV=narrator_brisk restores the old voice). Costs: overall 156–165 wpm, F0 +4 Hz. Every-run: ALGORITHM.md researched (only dated news: Reels series linking ended 28 Oct; YouTube spam 30-day lock test 29 Oct; no ranking change), PERFORMANCE insight AO (no new numbers; same-cart row not in yet), all posts PUBLISHED, owner's Michelin post had the IG AI label off. **Next run:** writers' room (tonight's build drops the REVIEWED queue to 2): W7 overbooking (HIW) + a whiteboard HOW TO (T11 bookkeeping); voice follow-up = the episode run reports hype's full-VO numbers (wpm_overall, F0) and the owner's ear; then Sound (last worked 27 Oct).
- 2026-11-11 (02:45 UTC run) | Writers' room (focus a: REVIEWED whiteboard queue was 2 after the Netflix build — 20 childminding, 18 cash rewards — and the rotation had no BIG) | **Hypothesis:** a BIG and a HOW TO written to the WRITING rules pass all three gates first time or within 3 rewrites, and an independent fresh-eyes reader still finds must-fixes the gates can't (logic, scope, sponsor framing). **Result:** confirmed. Both scripts reached human_check 6/6 + story 7/7 + 6/6 in 3–5 tool rewrites (gate misses: one flat run of 4, '-ing' tails ', shipping included' / ', shipping, fees', hook 17–20 words, 2 numbers per sentence ×3, a 35-s stretch with no question). Both reviews said 'ready after must-fixes' and every must-fix was something no gate measures: (7-Eleven) a takeaway with no result on record behind it, an order-of-events error (rescue agreed Mar 1990, before the Oct 1990 Chapter 11), a rounded-up count (12,712 → 'about 13,000'), 'Share' as a comment word colliding with the share button; (POD) a hook that framed a supplier's product cost as a skim (sponsor risk), 'a quarter' meaning 25¢ next to 'a quarter of the price', spoken numbers that didn't add up, a scope overclaim (Etsy-only 2024 count said as 'shops'). → WRITING rules 34–36. Research: 2 sourcing subagents (52 + 36 tool calls; every number on a page they opened). Props: `ice_m`, `riceball_m`, `truck_m`, `sunglasses_m`, `manual_m`, `tee_m`, `costbar_m` → board.py (lab sheet props_11nov.jpg; smoke test PASSED). Every-run: all posts to 11 Nov 05:00 IST PUBLISHED (no provider ERROR), ALGORITHM.md 1 day old (skipped), PERFORMANCE snapshot (Netflix row not in yet). **Next run:** writers' room again only if the queue drops below 3 — W7 overbooking (HIW) is next; else Sound (last worked 27 Oct).
- 2026-11-12 (02:42 UTC run) | Writers' room (focus a, by need: the queue held exactly 3 REVIEWED whiteboard scripts, but tonight's build takes 7-Eleven → 2, and the rotation had **no HOW IT WORKS** after childminding) | **Hypothesis:** a HOW IT WORKS on a topic most adults half-know (overbooking) can still carry a "wait, what?" if the hook is the money (US law can pay 4× your fare) and the count is the turn (1 in 36,000 bumped against their will, volunteers ~12× as many); it passes all gates within 3 rewrites, and fresh eyes still find must-fixes no gate catches. **Result:** confirmed. 23-overbooking reached human_check 6/6 + story 7/7 + 6/6 in 4 tool rewrites (gate misses: hook not a question, no stakes by 15 s, 2 numbers per sentence ×2, a flat run of 4, ', depending' tail, R7 tail 19–20 s, contractions 0.89). The review ("ready after must-fixes") found 6 must-fixes, all logic/attribution: GAO's 1-in-10 is cited literature (opened the footnote), "no cap" contradicted the $9,950 memo, "law sets the price" (it sets a minimum), a roadmap line that didn't fit thing 1, "a seat that might not be there" (backwards), and a 110/100 tally with no source → WRITING rules 38–39. Research: 1 sourcing subagent (55 tool calls; it mis-stated volunteers as "1 in 30" — the real figure is ~1 in 3,070; caught by recomputing every ratio). Props `plane_m`, `boardpass_m`, `gatedesk_m` → board.py (lab sheet props_12nov.jpg, first render had an unreadable pass header → fixed). **Tooling:** human_check now prints `note number` for a British "and" inside a number (American narrator): 9 hits in 7 queued scripts; 7-Eleven d1 fixed (still 6/6, 7/7). Smoke test PASSED. Every-run: all posts to 12 Nov 07:22 IST PUBLISHED, no ERROR; ALGORITHM.md 2 days old (skipped); Metricool IG import frozen since ~10 Nov (insight AS). **Next run:** if 7-Eleven builds tonight the queue is 3 (childminding, overbooking, POD) with no BIG → writers' room only if it drops below 3; else Sound (last worked 27 Oct). Owner: check the Netflix reel's Insights in the app if Metricool still shows 5 views.
- 2026-11-13 (02:41 UTC run) | Topics (focus b: the queue held exactly 3 REVIEWED whiteboard scripts that pass human_check --strict 6/6 (20, 22, 23), so not (a); the WHITEBOARD shelf held **7** unbuilt topics ≥ 20/25 (W3, W5, W8–W12) after W7 was queued — below 8; and the BIG shelf's best was B5 IKEA 21 with B8 unsourced) | **Hypothesis:** three parallel sourcing subagents, each given 2–3 candidates picked for "a rule or number about something the viewer already uses" (PERFORMANCE insight AV: those hooks open at ~70 % 3-s vs ~48 % for brand history), can verify ≥ 4 new topics ≥ 20/25 on primary pages in one run and give the BIG shelf a topic that beats B5's 21. **Method:** candidates chosen against topics.md, the queue, the bank and 90 days of IG captions (49 posts, IGRE03: no overlap — 'coin' hit = vending, 'pizza' = gas-station Casey's); agents told to confirm each line on the cited page and list myths; I scored with the 5 × 5 whiteboard scale. **Result:** 7 candidates checked, **6 banked ≥ 20** (W16 ZIP code at the till 24 — Pineda 2011 + Tyler 2013 + FTC data-append quote; W17 the date on your milk 24 — FSIS "except for infant formula", ReFED 3bn lb, EU Art. 24, Morrisons/WRAP; W18 coin kiosk 22 — Coinstar "up to 15.9% + up to $0.99", eGift 0 %, charity 7.5–10 % kept; W19 hidden-city 21 — AA conditions of carriage + Skiplagged judgment $9.4M on *copyright*; B9 Domino's 22 — 8-K "+14.3%", Slate customer lines; B10 Wrigley 21 — Britannica premium story, Mars ~$23bn 8-K), 1 below the bar (cash-only laws 19: "since 1978" secondary, SF repeal pending). Shelf **7 → 11** unbuilt ≥ 20; BIG best **21 → 22**. Myths caught by the agents before any script: "Williams-Sonoma was found to…" (only alleged), "debit cards too" (no source), "record for fast food" and Domino's stock multiples (unverified), "Skiplagging is illegal" (copyright verdict), "Coinstar 11.9 %" (now up to 15.9 %), "expired food is safe", Wrigley "invented gum"/Spearmint 1893. **Kept:** topic_bank entries + new W build order (W16 → W17 → W3 → W18 → W5 → W9 → W19); README next-writers'-room order (B9 Domino's first for the BIG gap). No template change, no render. **Next:** writers' room (tonight's childminding build leaves 2 REVIEWED): write **B9 Domino's (BIG)** + **W16 ZIP code (HIW)**.
