# OopsMyBusiness autopilot — playbook

One run = one finished, fact-checked, original Short/Reel, scheduled on the **OopsMyBusiness** brand in Metricool.
Follow every section. Quality beats speed: never post a broken, unchecked or unsourced video — if a step fails and
can't be fixed, stop, schedule nothing, and report what failed.

**Every video must be better than the last one** (owner's standing order). Before building, do the learning loop in
`IMPROVEMENTS.md`: refresh `PERFORMANCE.md` from analytics, refresh `ALGORITHM.md` if older than 7 days, pick at least one
voice upgrade and one visual/story upgrade, test them, keep only what measures better, and log it.

**Since 30 Oct every video is an EPISODE of a series** (owner: "the storyline and everything need to be good… keep in mind that later
I will get brand deals"). **Read STORY.md (what we tell and how: hero = "you", series, beat sheets, writing rules) and BRAND.md
(brand-safety rules, sponsor-readiness metrics) before this file's craft sections.** Scripts come from the writers' room queue
(`studio/episodes/`), already story-checked and reviewed; the build run re-verifies the facts and makes it beautiful.

**Time budget:** take your time — a good episode takes 90–150 minutes. Don't rush any step. The only hard limit: be finished
(scheduled, logged, pushed) about 30 minutes before the next run starts (the episode task fires once a day, 21:05 UTC).

## 0. Setup (fresh workspace)
```bash
# repo is attached + cloned at /home/claude/nextbignow-videos (see run prompt)
bash /home/claude/nextbignow-videos/studio/setup.sh          # models, soundfont, fonts, libs -> /home/claude/studio
P=$(bash /home/claude/nextbignow-videos/studio/new_project.sh <slug>)   # project from template
```
Disk is limited (~8 GB free) and RAM ~7 GB, 2 CPUs (full render ≈ 11 min): delete `work/part*.mp4`, frames and old projects after posting.

## 1. Channel and audience
- OopsMyBusiness = business secrets / hidden business models / how companies really make money. Audience: US, UK, Europe.
- Faceless, fully animated: square-face stick-figure mascot (cream rounded-square head, black stick body, orange tie), bright designed sets.
- Brand names may be said and written as plain text (commentary). **Never draw a real logo, mascot, packaging or trade dress** (e.g. no green siren, no golden arches). Use generic props.

## 2. Topic — interesting first (pick one, never repeat)
Owner, 27 Oct: "topics need to improve — something interesting." Twelve videos in a row used the same formula ("how company X
really makes money"); it has become predictable. From now on the topic must pass the **interest test** and the **type mix**.

**Where topics come from:** `studio/topic_bank.md` first — researched, fact-checked candidates with hooks, story beats and sources
(re-check any number that could have changed). Also read `studio/topics.md` **and** the brand's last 90 days of posts in Metricool
(owner also uploads manually); never repeat a topic or close variant. The R&D runs keep the bank stocked.

**Interest test** (score 1–5 each; write the scores in the CLAIMED line of topics.md):
1. *Wait-what* — would a friend say "no way" after the one-line hook? (Curiosity comes from a gap between what we know and what
   we just learned — Loewenstein 1994; surprise and awe make people share — Berger & Milkman 2012.)
2. *Story* — real people or a company, something at stake, a turn, an ending (a blunder, a gamble, a stunt, a rivalry, a comeback).
3. *Your life* — it touches something in the viewer's hand, wallet, phone or street.
4. *Picture* — the whole idea can be drawn as one cartoon in frame 1 (no real logos needed).
5. *Fresh* — not one of the usual top-10 YouTube business explainers, and a different type from the last two videos.
6. *Share/save* — a takeaway or "you won't believe this" fact people send to a friend.
7. *Verifiable* — primary sources exist for every number.
Pass = total ≥ 26 / 35, *Wait-what* ≥ 4 and *Verifiable* = 5. Otherwise pick another topic.
**Plus two gates (30 Oct, STORY.md §6, BRAND.md §3) — both must be yes:**
- *Seat + choice:* there is a real person's seat the viewer can sit in at a moment of decision, and an honestly debatable two-option
  question (YOUR MOVE) — or ≥ 3 tricks the viewer can spot tomorrow (SPOT THE TRICK) — or ≥ 3 "doors" to one owner (WHO REALLY OWNS IT).
- *Brand-safe:* none of the skip topics (deaths/tragedy as the core, violence, crime glorification, politics, religion, health
  claims, gambling, crypto, investment tips) and it can be told curious-not-cruel.

**Type mix** — never two of the same type in a row; type F at most 1 in 3 videos:
A. Wild true story (blunder, gamble, stunt, scandal with a twist) · B. Everyday object, absurd economics · C. Hidden giant (one
company behind "competing" brands) · D. Origin twist (a famous company or product began as something absurd) · E. Psychology or
pricing trick you can spot tomorrow · F. Hidden business model ("how X really makes money").
Data (27 Oct, PERFORMANCE insight I): B and E reels held ~68 % past 3 s / 23 s avg vs F ~57 % / 18 s → prefer B/E/A/C/D;
Each bank entry lists the only numbers that verified and the popular myths to avoid — keep to them.

**Hook:** concrete thing + impossible-sounding claim in ≤ 12 words, as a question ("Do you know a man tried to buy a fighter jet
with Pepsi points?"). Best data so far: an everyday object + a "that can't be right" comparison (printer ink vs champagne: 74 % 3-s rate).
- Avoid: medical/health claims, politics, legal accusations, anything defamatory or speculative about named people (court and
  regulator findings, stated as such, are fine).

## 3. Research and fact rules (strict)
- Use WebSearch/WebFetch. Every number in the script needs a primary source (SEC 10-K/10-Q/8-K, company release, government data such as FDIC/BLS)
  or two reputable outlets. Use the **latest** data available today; say "last year"/"in 2025" precisely.
- Round honestly ("about $1.7 billion", "over $200 million"). Quotes must be real (light profanity removal is fine).
- **Fetching (3 Nov):** a guessed or stored URL can time out (PROVENANCE_REQUIRED). WebSearch for the page first, then fetch the URL the search returned (5 Nov: also holds when a web-fetch subagent does the fetching: search in the parent first, hand it those URLs). No curl, mirrors or archives. Don't drop a fact as unverifiable until you have tried this.
- Keep a list of sources; put a short "Sources:" line in the post text and a small source chip on screen for key stats.

## 4. Script (`scripts/vo_lines.py`)
**Structure comes from STORY.md** (§4 beat sheet for the series, §5 writing rules): second person present tense, the viewer in the
seat by line 3, stakes by 15 s, one "Oops." at most, the series ending (YOUR MOVE: "Comment FIGHT or FOLD"). Put `SERIES`, `PART`, `EP`
at the top of vo_lines.py; `tools/story_check.py` must pass 7/7 R-gates and all S-gates. The rules below are the craft details.
Format: `(id, text, speed, pause, base_semitones, range_expand, [stressed words], ending)` — see `examples/*/vo_lines.py`.
- Length = whatever the story needs for a viewer to fully understand it — usually 60–100 s, and up to ~3 min is fine (owner,
  27 Oct: "no need to stick to 1 minute — 2–3 minutes is fine; what matters most is that viewers understand"). Never pad.
  MrBeast-style: simple words, stakes, short sentences — but **never rushed**: speed ≈ 1.0, real pauses before reveals
  (0.35–0.6 s; one longer 0.6–0.8 s beat before the biggest reveal), one idea per line, one focus word per sentence (VOICE.md).
  Videos over ~75 s: a re-hook every 20–30 s.
- Hook questions: a *wh*-question ("Why would a credit card pay an airline eight billion dollars?") falls naturally — give it
  ending `None` and stress the number; only yes/no hooks get `"q"` (VOICE.md research: rising statements sound unsure).
- Line 1 = an intro **question** inside 3 s that names the brand/topic and the surprising claim, so viewers instantly know what the video is about (e.g. "Do you know Starbucks is sitting on one point seven billion dollars… of your money?"). Vary the wording each video.
- Middle: 3–4 clear beats (steps/secrets/reasons) — vary the structure from the previous video. Explain each beat with a
  concrete everyday example the viewer recognises (a receipt, a cup, a card swipe), not abstract numbers alone.
- **Re-hook** around the middle (an open loop: "but the third trick is the sneakiest…") so people don't swipe at 40%.
- Payoff twist line, a **takeaway the viewer can use** (worth saving), then CTA: "Send this to the friend who …!" (tied to the topic).
- **Loop ending:** if possible the last line flows back into the first frame, so a rewatch feels seamless.
- Line ids: hook `i*`, beats `a*`/`b*`/`c*`/`d*`, ending `e1`, CTA `e2` (the template's shots use these). Unique words help timing anchors.
- Numbers: write them as words the TTS reads cleanly ("one point seven billion", "four ninety-nine"). Check abbreviations in the ASR read-back.

**Story rules (R&D Story run, 27 Oct — evidence and numbers in `lab/story/NOTES.md`).** Before `make_vo.py`, run
`python3 /home/claude/nextbignow-videos/studio/tools/story_check.py $P` and fix every flag (aim 7/7; log the score in the run log):
- **R8 Roadmap (cheap, keep it; n = 18 on 3 Nov shrank the 27 Oct gap to +1.8 s avg watch / +1.6 points of length, so it is no longer "the strongest signal"):** promise a count in the first 4 lines and label the items. Our 4 reels with
  "Step one / Secret two…" held 29–34 % of their length on Instagram, the 2 without 19–24 % (n = 6; works for type F too).
  The last 5 videos dropped it. Per type: A/D story → "…flipped in three moves. And the last one is the cruelest." (Move one /
  Move two / Move three = eras or turns); B object → "three reasons…"; E trick → "N tricks, the last one is the sneakiest";
  C hidden giant → "N brands you'd never guess". Save the strongest item for last (suspense: Ely et al. 2015).
- **R2 Open loops:** a question, teaser ("so what did Lizzie get?", "here's the clever part") or item label at least every 25 s.
- **R5 Load:** one figure per sentence, ≤ 18 words per sentence (split "278,000 in year one. Over 1.7 million in year two.").
- **R6 No recap lines;** **R4 no "and then" chains** (link beats by cause: but/so/because — craft rule, don't overdo it: our data
  did not reward sprinkling "but").
- **R7 Ending:** twist → loop line → short takeaway → "Send this to the friend who…", ≤ 18 s from the twist to the end.
- Write real good/bad swings (a win, then a blow) — emotional volatility and reversals predict engagement (Berger 2021, Knight 2024).

## 5. Voice (local, no ElevenLabs)
`python3 scripts/make_vo.py` — Kokoro blend **am_michael 0.5 + am_eric 0.3 + am_fenrir 0.2** in its **own register** (no global
pitch lift), Praat PSOLA prosody for per-line highs and lows, stressed words, question rises, low endings; calm, unhurried pace
(~180 wpm while speaking, real pauses). Chosen by the 26 Oct voice lab (UTMOS naturalness 4.12 → 4.36; see IMPROVEMENTS.md).
`SPLIT` 0.12 (default since 27 Oct): each sentence of a line is generated by its own Kokoro call with a 0.12 s gap — long
multi-sentence lines sound less rushed (UTMOS 4.23 → 4.38 on the Duolingo script). Knobs (env, defaults = lab winner): `VMIX` blend, `SPD` 0.88 (speed multiplier), `PZ` 1.6 (pause multiplier), `PMIN` 0.3 s,
`GT` 0 (= keep own pitch; **every global lift tested so far lowered naturalness**), `EXS` 1.0 (range expansion), `BMP` 1.0 (stress bumps), `STR` 1.0.
Since 27 Oct (R&D run 3) make_vo has a **per-line prosody gate** (`PGATE=0.15`): any line that loses > 0.15 UTMOS to the PSOLA
moves is re-rendered with softer moves (it prints `prosody gate …` with the lines it softened). Leave it on; `PGATE=0` only for A/B.
Since 27 Oct the cleanup chain is lighter (`DEESS=-8`, `ROOM_DB=-27`, `COMP=1.5`; old: −11/−21/2.2): per-line UTMOS 4.396 → 4.425, worst line
3.996 → 4.063 on the De Beers script (chain-only A/B on one fixed raw take, `lab/voice_chain/chain_ab.py`).
Write line speeds 1.0–1.06 and pauses 0.2–0.45 in `vo_lines.py` as in the examples; SPD/PZ make them calm.
**Since 12 Nov the episode narrator is `CBV=usa_narr` (owner 11 Nov: "American accent so it catches USA people"): cash-rewards reached 172.8 wpm overall with no tempo step (UTMOS 4.42); skip `tempo.py` when voice_report already says ≥ 165.** **Chatterbox (the default engine) ignores the speed column (R&D 10 Nov):** keep writing speeds for Kokoro fallback, but on Chatterbox pace comes from the reference (`CBV`, default `narrator_hype` since 10 Nov, phrase rate ~170–183 wpm) + pauses + `trim_gaps.py`. Don't time-stretch (PSOLA ±5 % cost 0.06–0.09 per-line UTMOS). To speed up, cut words; to slow down, add a pause where a number lands.
Pace check (28 Oct, Hoover): line speeds of 1.0–1.02 with the default SPD 0.88 gave only 152 wpm speaking (target 165–190). If
`voice_report` says < 165 wpm, re-run with `SPD=0.96` (Hoover: 152 → 160 wpm, per-line UTMOS 4.439 → 4.423, range 18.0 → 17.7 st,
ASR clean) — or write line speeds 1.02–1.06 from the start. **Compare takes on per-line UTMOS (mean/min), not the chunked whole-file
number:** two Hoover takes that differed in only two lines scored 4.44 vs 4.31 chunked but 4.421 vs 4.423 per-line.
Run voice_report only after make_vo has fully exited (it reads `work/align.json`, written last; a report on a fresh vo.wav with the
old align.json gives wrong per-line numbers).
Weak short reveal lines (per-line UTMOS < 4.2, e.g. "Her income? Zero." 4.14): first lengthen the text slightly ("Her income that year?
Zero." → 4.29, 27 Oct Monopoly A/B) — 2–3-word lines are always the weakest. Yes/no hook questions get softened by the prosody gate
(q_rise −1…−2 st): keep them short and put the key word last.
**Since 1 Nov (drone episode, 2nd script after glasses): `EXS` default 1.15** (template make_vo) — A/B on the same text at SPD 1.0: EXS 1.0
per-line UTMOS 4.407 (min 4.28), 18.1 st, low_fall −6.0 st vs **EXS 1.15 4.407 (min 4.31), 18.8 st, low_fall −6.3 st**, 168 wpm, 0 ASR bad lines.
Line speeds 1.0–1.04 need `SPD=1.0` to reach ≥ 165 wpm (SPD 0.96 gave 163 wpm on the same script). voice_report's ASR normaliser now reads
"twelve hundred" = "$1,200" (it was a false bad line).
**13 Nov (7-Eleven, 3 takes): `make_vo.py` was OOM-killed (6 GB, memory cgroup) at its last stage on the first run of every take — the take's `flat_*.npz` cache survives, so just run make_vo again (it finishes in ~2 min from the cache); never run music/mix/anim tests while a take is generating. Comping 3 takes lifted per-line UTMOS 4.429 / 4.412 → **4.463, min 4.23 → 4.34**. usa_narr spoke this script at 149 wpm (raw) → trim_gaps 153.8 → `tempo.py $P 1.07 --keep i6` **164.6 wpm**, per-line 4.441: a line whose words fuse when sped up (ASR 'ice dock' → 'iStock') stays at normal speed with `--keep`.** **After comping (8 Nov): `python3 studio/tools/trim_gaps.py $P` caps dead air inside lines (Chatterbox leaves 2 s+ gaps) — then music, mix, render. Since 9 Nov its defaults are 0.55 → 0.42 s (sentence ends inside a line, VOICE.md's 350–500 ms): on the dropship VO that cut 13 gaps / 7.1 s and took the overall pace from 161 to 171 wpm with per-line UTMOS unchanged (4.462 → 4.458); designed beats between lines are untouched.** **Since 6 Nov the template default is Chatterbox + `narrator_brisk`, END_ST −5.5 (`python3 scripts/make_vo.py`; VOICE.md table). Takes differ line by line and misread at random, so generate 3–4 and comp them: `cp work/vo.wav work/vo_n1.wav; cp work/align.json work/align_n1.json; python3 tools/voice_report.py $P work/vo.wav > work/vr_n1.log`, repeat with `rm work/flat_*.npz`, then `tools/comp_takes.py $P <tag>` per take, 5.5 min each. Read asr_bad_lines of every take first: set a misread line's score to 0 in voice_report.json so comp replaces it. Rewrite a text change as: edit, new take, set that line's text in the base align.json + its score 0, comp.**
Alternative engine (opt-in, see `VOICE.md`): `ENGINE=chatterbox python3 scripts/make_vo.py` — Chatterbox-Turbo (MIT) in our own
synthetic narrator's voice, +0.06 UTMOS per line; since 27 Oct its `low` lines get a last-word fall (`lib/end_contour.py`, `ENDS=0` to
disable, `END_ST` depth, default −4 st) so reveals land (−3.5…−4 st vs −1 before), but its questions still fall → Kokoro stays the default. (27 Oct note that its output is deterministic was wrong: re-running gives different audio, VOICE.md 6 Nov.)
QA: `python3 /home/claude/nextbignow-videos/studio/tools/voice_report.py $P` (years like "twenty twenty", "ten and a half" and decades like "nineteen eighties" are normalised; since 27 Oct it also prints per-line UTMOS mean/min, weak lines < 4.2, q_rise/low_fall, and scores files > 80 s in ≤ 60 s chunks — a 117 s VO got OOM-killed as one piece) → UTMOS ≥ 4.0 (aim ≥ 4.3), `asr_bad_lines` empty,
pitch range ≥ 15 st, speaking pace 165–190 wpm. Fix spelling/phrasing and regenerate if a line reads back wrong.
A/B voice variants **one at a time** (copy the project to `projects/<slug>_B` and run there): the box has ~7 GB RAM and two Kokoro or
UTMOS jobs in parallel get OOM-killed silently (log just stops).
Output: `work/vo.wav`, `work/align.json` (word times used everywhere via `T(line_id, word)`).

## 6. Visual style (non-negotiable)
- **After posting, check delivery (6 Nov: reselling failed on Instagram, "Media container not created", while YouTube published, and nobody noticed for hours):** at the start of every run, read the last post's `providers[].status` with `getScheduledPosts`; report any `ERROR` at the top of the run summary and in PERFORMANCE.md. Never re-post on your own: the owner decides.
- 1080×1920, 24 fps. Safe zone: nothing important in top 250 px, bottom 420 px, right 120 px, left 60 px. Key visuals central.
  (Measured app UI, Sep 2026: IG Reels top 250 / bottom 319 / left 86 / right 119; YT Shorts ~288 top, ~288 bottom + long titles,
  ~140 right — our zone is the safe union except YT's right buttons; keep text ≤ 800 px wide, centred.) Since 28 Oct (R&D Visuals
  run) the caption helpers enforce it: leads/tails shrink to `maxw`, `say` max 800 px, `title3d` fits its extrusion + shadow,
  chips shrink to ≤ 800 px, and `ed_show`/`ui_word`/`say`/`title3d`/`hud_*`/chips are nudged back inside when they poke out by
  < 220 px (`SAFE=0` disables). Props, map labels and text you draw yourself are NOT nudged — check them with layout_check.
  **Check:** `python3 /home/claude/nextbignow-videos/studio/tools/layout_check.py $P` (after make_vo; `--fake-align` works before
  any audio) → renders every 3 s + the first 3 s twice (with/without captions), prints frames whose caption pixels fall in a UI zone
  and writes `frames/layout_sheet.jpg` (red = UI, magenta = caption in UI). Fix every settled violation (whip/blur transition
  frames that span the full width are fine). Source chips: centre y ≤ 1465.
- Bright, vibrant, extra-saturated sets (`stage(scheme, sun_colour, x, y, R)` — big colour circle), beautiful background in every shot.
  Schemes: cream, sky, yellow, purple, teal, red, emerald, orange, pink. Change scheme every shot; match colour to the moment.
- **Cinematic texture (owner's references, 27 Oct — top story reels):** real-looking light, depth and atmosphere, a film look, and a
  giant 3D word tucked behind the hero object. `scripts/anim_cine.py` (on by default, `CINE=0` = old flat look) turns every
  `stage()` into a lit world with depth (golden-hour skyline for orange/yellow, blue-sky skyline for sky, city night for
  purple/teal, wooden desk for cream, lit studio for red/emerald/pink — or pick one: `world(kind, scheme, t)`), turns the colour
  circle into a glowing disc, and turns `finish()` into a film grade (contrast curve, warm/teal split tone, bloom, halation,
  lens fringe, film grain, vignette). Use per shot:
  - `title3d(f, "WORD", y, t, t0)` — big extruded 3D word, centred, fits the safe zone; draw it BEFORE the hero so the hero
    overlaps it. Use in the hook and on 1–2 big reveals (never on every shot; never the same word as the caption above it).
  - `light_rays(f, x, y, col, strength)` for reveals, `bokeh(f, ...)` for magic/money moments, `dof(f, sigma)` to blur a
    background layer before drawing the sharp hero, `light_wrap(...)` to rim-light a hero in its scene.
  - Check test frames for haze: colours must stay vibrant (owner hates washed-out); if a shot looks foggy, lower `bloom` or the
    disc `op`, or pick a darker scheme. Render cost ≈ +0.2 s/frame (a 2-min video renders ~4 min longer).
- All on-screen text truly centred at x = 540 (keep `ui_word` default x; no off-centre captions), max width ~840 px.
- Two-tier editorial captions **only at key moments** (`ui_word(f, lead, BIG, y≈470, t, t0, ...)`): one big word/number + small lead.
  No word-by-word subtitles, no emoji, no persistent counters/meters.
- First 3 s: a strong visual (object + action) + one short caption with the brand/claim. No giant text-only opener.
  **Frame 1 is already interesting** (the most surprising object of the video, mid-motion) — YouTube counts views from the
  first frame and the seed audience decides in about 1–2 s whether to swipe. (Data check, 28 Oct, PERFORMANCE Q: on our 9 posted
  reels no first-3-s visual feature predicted the 3-s rate — 5 opened on an empty disc and did about as well as the rest; the
  topic and the hook *line* decide. Keep frame 1 alive because it is cheap, but spend the effort on the topic and line 1.)
- At least 18 shots; the picture changes every 2–3 s (new prop, zoom, angle or set). Every claim in the VO gets its own visual.
- Every non-scene shot: a real prop or diagram that shows the idea (props in `anim_props*.py`; write new ones per topic in a new `anim_props4.py`
  and add it to `anim.py`'s exec list). Big objects, movement on beat (pin/pop, flips, slams), screen shake on impacts (`IMPACTS`),
  transitions vary: cut, whip, focus, zoom, punch, flash.
- **Cast look (owner, 31 Oct): colourful stick men and girls** — `anim_stick.py` (default on; STORY.md §2b). Mix men and girls every episode.
- **NextBigNow look (owner, 4 Nov: "too cartoon")** — `anim_nbn.py` (default on; STORY.md §2b): NBN stick rig, two-tier captions, one brand pill + one quiet line, light dust.
- **Real NBN kit (5 Nov): `template/scripts/nbnkit/` + `examples/spotify-999/anim_shots.py` is the start point for new episodes** (STORY.md §2b): it looks like the NextBigNow feed because it is the same drawing code. ~6 fps per process, so a 136 s episode renders in ~4.5 min. `skia.ContourMeasureIter` doesn't exist in skia-python: use `partial_pts`. Layout check: name captions `say` / `fnote` so it can switch them off; the frame-0 WARN (core detail 0.02) is a false alarm on smooth Skia frames, look at the frame.
- **Skia props, 5 Nov (`nbnkit/__init__.py`, HOW TO START EP 5 + HOW IT WORKS EP 3):** worlds `pack_room` (night stockroom), `waterworks` (pump room); `jacket(worn=)`, `price_tag`, `stamp`, `listing_card`, `receipt(rows, total=, prog=)`, `tax_form(ghost=True)` (dashed: the form that never came), `line_tally`, `parcel`, `tank(fill, label)`, `pipe(pts, flow, t)` (coins ride it), `valve`, `split_bar`, `feed_phone` (plain scrolling cards with an AD card, no app UI), `line_meter`. **Anton has no →, ≠ or ≈: they render as a box. Write THEN / ABOUT.** Lab pattern: `lab/story_kit/storyboard_ep5_ep3b.py` (don't name a variable `HERE`: nbnkit's star import overwrites it).
- **6 Nov (HOW TO START EP 5, `examples/reselling-tax/`):** new nbnkit `rack`, `swing`, `jacket_grid` (a legal count you can see land). **The one pill carries the chapter (`HOW TO START · STEP 2 OF 4`)**: a re-hook and a progress bar with no second line on screen. **The rack is the roadmap:** numbered jackets hanging, one returns at the left on each step card. New SFX `rewind`, `hanger`, `stamp_hit`. `say(t1=)` in this example closes the old caption 0.2 s sooner: no ghost overlap on the change, use it. Don't leave a card off-centre on an empty disc while it is the only idea: centre it, slide it aside when its partner arrives.
- **6 Nov (R&D, HOW TO START EP 6 + HOW IT WORKS EP 4 + credit score):** nbnkit gained `home_kitchen`, `oven`, `cookie`, `cookie_tray`, `cookie_grid`, `muffin`, `cell_bars`, `cake_box(lines=)`; `hotel_lobby`, `elevator(price=, floor_=, open_=)` (a price where the floor number goes, four lamps), `hotel_card`, `ticket`, `front_desk`, `room_key`; `car_lot`, `car`, `score_slices`, `gauge`, `cycle_strip`, `credit_report` (Skia versions of the old cv2 credit-score props). Lab sheets `lab/story_kit/storyboard_ep6_ep4b.jpg`, `storyboard_ep2_skia.jpg`. A `stamp` on top of a `label_card` hides the word: put it beside.
- **7 Nov (HOW TO START EP 7, `examples/export-start/`):** nbnkit/board.py gained `us_m` (hand-drawn lower-48 outline, no map data), `tollgate_m`, `scroll_m` (parchment unrolls, then a document quote writes on line by line: use it for any real quote from a law/filing), `candle_m`, `clipboard_m` (the roadmap as a checklist, `hot=` circles the trap step), `digits_m`, `grid100_m` (a share you can count), `namecard_m`, `list_m` (scribbled list, one row lights up), `folder_m`, `searchbar_m`, `laptop_m`, `eu_door_m`. Stamps stacked under a card read as clutter: give each stamp its own row. A `say()` that starts at t=0 is half-written on frame 1: start it at t0=−2 so the hook word is already on the board. **board `say()` now centres on the safe zone (x 510, big word ≤ 840 px)**: the old centre-540 / 860-px cap put 340–1,150 px of every wide caption into the right UI zone on all whiteboard episodes (layout_check 26 of 43 frames → 0).
- **Clean look (owner, 3 Nov): like NextBigNow** — `anim_clean.py` (default on; STORY.md §2b): flat deep gradient sets, no grain/haze, captions in the top band, one idea per frame. **Topics (3 Nov): informative + interesting** — HOW IT WORKS + HOW TO START first (episodes/README priority, topic_bank H1–H7 / T1–T7).
- **Story scenes, full frame (owner, 27 Oct: "it's using full frame and looks engaging… colours, more natural and 3D, change
  the style of clothes").** At least half the shots are **character-driven full-frame scenes**, not a prop on a glow disc:
  - Sets (`scripts/anim_sets.py`): `f = set_view(name, t, zoom, cx, cy, blur)` fills 1080x1920 edge to edge — `street`, `study`,
    `parlor`, `office`, `store`, `dusk` (field at sunset, tree line, ground fog). It also sets the matching character light.
    Write a new set per topic when none fits (factory, bank, kitchen…) in the same file style: perspective floor, texture,
    occlusion, one light pool. Mood FX: `smoke(f, t)`, `embers(f, t)`, `glow_eyes(f, x, y)`.
  - Cast (`scripts/anim_mascot3d.py`): `person(f, x, y, s, who, …)` = lit 2.5D characters (rounded volumes, key + ambient +
    rim light, contact occlusion, cast shadow). Looks: `hero` (orange hoodie — our recurring narrator character), `friend` (tee),
    `creator` (jacket), `exec` (suit), `inventor` (dress, bun), `lady` (long hair), `oldman` (cardigan, glasses), `worker`
    (overalls, cap), `kid`, `mystery` (dark coat + hat, shadowed face). Re-dress anyone per story with a dict:
    `who={"base": "exec", "top": (120, 30, 40), "hair": "curly"}`. Same pose args as `guy()` (`la/ra/ll/rl/lean/sit/mouth/
    brow/expr/look/hold/sweat`) plus `back=True` for over-the-shoulder. `guy()` = the hero.
  - Shot sizes: vary every 2–3 s — **wide** (s≈0.7–0.9, whole set), **medium two-shot** (s≈1.2–1.4, feet near y≈1900,
    `set_view(..., zoom≈1.25, blur≈2.5)`), **close-up** (`person_head_at(f, 540, 860, 2.6, who)` + `blur≈6–7` on the set),
    **over-the-shoulder** (`person(..., s≈2.5, back=True, shadow=False)` bottom-left + the other character mid-frame),
    **foreground hand** (`fg_hand(f, x, y, s≈1.9)`, blurred, for "you" moments).
  - Captions in scenes: `say(f, "HE GOT $500", y≈1300–1420)` — big white condensed text with a black stroke at lower-middle,
    never over a face. Series badge: `part_badge(f, "PART 2", "THE REAL INVENTOR")`.
  - HUD (pick 1–2 per video, only when they add tension): `hud_clock(f, "DAY 1", "6:14 AM", "PLACE")` (top-left),
    `hud_rule(f, 1, "NEVER SELL THE PATENT", y)`, `hud_timer(f, secs, y=…)` (don't overlap the clock), `hud_choice(f,
    "MOST OF YOU SAID", "DON'T SELL", y)` (series callbacks to comments).
  - Data shots (numbers, charts) still use the prop/disc style, but cut back to a scene within one or two shots.
  - Render cost: ≈0.1 s per character per frame at s≈1.3; scenes with 2–3 characters are fine.
  Never borrow other creators' characters or any franchise character (e.g. no Pokémon) — ours only.
- On-screen source chip for key stats (`chip("Source: …", INK, WHITE, 24)` near y≈1430).
- End: phone "SEND THIS" CTA scene, then the OopsMyBusiness logo sting ("follow for more business secrets").
- Moving objects must stay inside x 140–940 (or fade out near the edges): camera shake/zoom uses BORDER_REFLECT, so anything
  touching the frame edge is mirrored back in as a duplicate.
- Plan the hook shot so the money reveal lands **inside** shot 0: cut to the next shot only after the line's key number
  (shot boundaries are word anchors — check them against `align.json` before rendering).
- Try something new every video (new props, new layout idea such as split screen / map / chart / stamp / vault) — never clone the last video.
- Captions live at y≈380–560: any tall prop (price sign, phone, bar) must start below y≈620 or it collides with the big word (caught in 27 Oct test frames).
- Loop ending: let the last story line end on the exact composition of frame 1 (same set, scheme, prop positions) so a rewatch feels seamless.
- Long source chips: keep ≤ ~60 characters at size ≥ 19, or they run edge to edge and can't be read on a phone.
- Contrast (27 Oct test frames): the `wui` caption (white lead, yellow big word) is unreadable on the **cream** scheme, and
  `bars()` labels are ink, unreadable on dark schemes (emerald, purple). Data-viz shots → sky/orange/yellow (with `col=WHITE`
  for the big word on yellow); keep cream for ink captions only.
- Generic props added 27 Oct (De Beers): `gem_el` (cut diamond, `cracked=`), `ring_el`, `pillow_el`, `hangtag_el` + `swing_tag` (hanging price tag),
  `bride_icon` (person icon array, lit/unlit), `sparkle`, `vault_wall` (drawer wall), `hourglass`, `minecart_el`, `poster_el` (vintage print ad, serif),
  `typewriter` (types text in sync with the VO), `medal_el`, `line_chart` (animated), `flask_el` (lab bell jar), `closed_sign_el`.
- Generic props added 27 Oct (Monopoly origin): `board_el` (square game board, INVENTED street names, no colour bands/GO arrow — never real
  game trade dress) + `board_xy` (square centres, for hopping pawns), `pawn_el`, `house_el`, `book_el` (rulebook cover, fist/hands icon),
  `gamebox_el`, `census_el`, `gavel_el`, a **woman character** `lizzie`/`woman` (guy + dress + hair bun) and `hat` (fedora) for a second
  man — history stories need more than one person. `poster_el(..., ring=False)` drops the De Beers ring drawing (it showed through the text).
- Wild-story structure that worked (28 Oct, Hoover): stakes first ("three bosses fired, European business sold"), then the roadmap
  "three mistakes, the last one the cruelest", each mistake opened with a `MISTAKE #n` chip + `say()` label, a recurring cast (the boss,
  the family, the travel agent) across sets, and the loop line that repeats the hook question ("what happens when everyone says yes?").
- Origin/history stories (type D/A): one person per era, a year card (split-flap `flapboard("1904")`) at every jump in time, and a
  spotlight-alone shot for the "and what happened to her?" re-hook.
- Real people's names in the VO: Kokoro/ASR mangle rare surnames ("Frances Gerety" → "Francis Jarity") — drop the name from the VO or put it on screen only.
  Same for rare company/brand names (28 Oct: "EssilorLuxottica" → "Essiler Luxotica", "Varilux" → "Var Relux", "LensCrafters" → "Lens Crafters"
  = a false ASR flag): say a descriptive name in the VO ("the frame giant"), write the real name on screen; split CamelCase brands ("Lens Crafters").
- Generic props added 28 Oct (Hoover free flights): `vacuum_el` (generic upright vacuum), `wing_el` + `winged_vacuum` (flapping
  feathered wings on any object), `sky_bg` (open sky, no ground — for flying objects), `ticket_el` (paper airline ticket, any destination),
  `carton_el` (appliance box with a plain label), `ad_poster_el` (1990s shop promo with starburst + "*conditions apply"), `form_el`
  (claim form), `pin_el` (map pin + label), `atlantic` (ocean map with flight arc); `cheque_el(..., year=)`; full-frame set `airport`;
  SFX `whirr` (motor) and `jet` (fly-by) in sfx_lib.
- **Captions on light full-frame sets** (store, office, parlor, airport, street): `ui_word` with a white/yellow lead disappears on light
  walls (caught 28 Oct) → use `say()` (white/yellow with black stroke) or a coloured `chip()`; keep `ui_word` for prop shots on stage().
  Scene captions go at y≈520–830 when characters fill the lower half (faces sit at y≈1250–1400 for s≈0.7–0.9).
- Things held overhead (boxes, placards): centre them at `feet_y − 520·s − 90` so they sit above the head, not over the face; keep
  placards inside x 250–830 or their text runs off the frame.
- Generic props added 28 Oct (banana clones): `banana_el` (generic curved banana, `brown=` dying, `label=` sticker), `bunch_el`, `slice_el`
  (cross-section), `copier_el` (office photocopier — "clones" visual), `plant_el` (banana plant, `sick=` 0..1 droop/brown), full-frame
  `plantation_view(t, zoom, cx, cy, blur, sick=)` and `soil_view` (+ `spores`, `hyphae`), a **Latin America map** (`map_view` →
  `(frame, cam)`, `map_pt(lon, lat, cam)`, `blight` spreading blob, `map_pin`; `sepia=True` for history), `sepia_tone(f, k)` for
  flashbacks, `spray_el`, `helix` (DNA), `basket_el`, `numcard_el` (roadmap cards, `down=True` = "?"), `stand_el` (market stand).
  Map shapes are hand-simplified lon/lat polygons (MAP_SA, MAP_CA, …) — add regions the same way.
- **The template `worker` look (red cap, red shirt, blue overalls) reads as a famous game plumber** (caught 28 Oct) — always re-dress it
  (e.g. straw hat `hair="hat"`, white shirt, brown overalls) and check every new outfit for franchise look-alikes.
- Spread-over-time stories: a map with year pins popping on the VO words (one `blight` + pin per place) explains "it is moving" faster
  than any text; keep pin labels short (year in the pin, country in an offset chip) — country names on pins overlapped at 80 px apart.
- Generic props added 28 Oct (glasses / hidden giant): `glasses_el` (round, oval, cat, sport shield, thin rect; `clear=` optical,
  `smart=`+`led=` AI glasses — never Wayfarer-like shapes), `glasses_tree` (one trunk, many branches ending in different glasses = "one
  owner" frame 1), `door_el` (numbered roadmap door that swings open on light), `shopfront`/`shopfront_el` (plain-text sign), `lens_el`,
  `plan_card_el` (insurance card), `rx_el`, `eyechart_el`, `hub_map` (one centre node, spokes pop on the VO words), `stock_crash`; full-frame
  sets `mall` and `optician` (`set_view("mall"|"optician", ...)` + `mall_dressing`/`optician_dressing`).
- **Hidden-giant (type C) structure that worked (28 Oct, glasses):** frame 1 = one object that visibly holds all the "rival" things (tree
  of glasses + a shop sign + an insurance card); roadmap as physical doors ("four doors to your eyes, the fourth is the sneakiest") with a
  `DOOR #n` chip + door swinging open per item; one mini-story with a rival (Oakley 2001 → bought 2007) as the mid-video re-hook; the twist
  as a hub diagram whose spokes pop on each word; loop back to the frame-1 tree. Name the giant on screen, not in the VO, if ASR mangles it.
- **Story kit 2 (31 Oct, `template/scripts/anim_story2.py`, SPOT THE TRICK store world):** full-frame sets `maze_store` (one-way showroom
  path with grey floor arrows + a far EXIT sign), `market_hall` (racks of cardboard boxes), `store_cafe` (canteen); props `bin_el(item=)`
  (cardboard "bulla bulla" tub), `arrow_floor(f, x, y, s, ang)` (floor decal drawn on the frame; 90 = towards the camera), `flatpack_el(built=0..1)`
  (box → wobbly shelf), `tray_el`, `shortcut_door_el(open_=)`, `exit_sign_el(mirror=)`, `list_el("LAMP")`, `turnstile_el`, `heart_el(cracked=)`.
  Lab frames: `lab/story_kit/storyboard_ikea_st1.jpg`. Pattern for new kits: one file per world, sets registered via `_STORY_SETS.update` +
  `_FLOOR.update` + `SET_LIGHT.update`, added to anim.py's exec list, checked with `board_check --strict` and a 10–12-row lab render with guides.
- **Props kit 5 (2 Nov, HOW TO START EP 3 food truck, `template/scripts/anim_props5.py`, in anim.py's exec list):** `foodtruck_el(w, open_=True, menu="TACOS",
  glow, permit=True, col)` (step-van side view: striped awning + lit window when open, shutter when closed, menu board, permit sticker or a red dashed empty
  outline, reads at w 260–900), `permit_el(w, price="$200", stamped=False)` (plain city permit card, no seal), set `commissary` (garage-kitchen base: roll-up
  door, prep table, hose reel, drain, bay lines; sign sits right of the cold-open card). Cast in front of the truck hides `menu` → `menu=None` or stand by the wheels.
- **Props kit 4 (1 Nov, HOW TO START drone episode, `template/scripts/anim_props4.py`, in anim.py's exec list):** `home_el(w, sign="FOR SALE")`
  (suburban house), `aerial_view(t, zoom, cx, cy, rot)` (full-frame top-down "seen from the drone" yard: hip roof, pool, trees, drive, street) +
  `viewfinder(f, t, alt)` (drone-camera HUD: brackets, blinking REC, altitude), `route_map(f, t, k, n_red, labels, t_pop=)` (the step roadmap as
  a dotted flight route with 5 numbered waypoint cards; the drone flies to waypoint k), `remote_id_el` + `waves(f, x, y, t)` (broadcast rings),
  `shield_el(text)` (insurance), `airspace_phone_el(ok)` (generic map: red NO FLY ring, green zone, status bar), `nofly_ring(f, x, y, rx, t)`,
  `photo_el("home"|"roof"|"party", w)` (aerial print), `pc_el(w, k, label)` (exam monitor + progress bar), `controller_el`, `uk_eu_card_el`
  (outline-only region cards, no flags). Drone prop: `drone_el(w, t)` in anim_stick.py. SFX `rotor(dur, level, f0)` (quadcopter buzz) and
  `shutter()` in sfx_lib.
- **HOW TO START step pattern (1 Nov):** each step opens on a full-frame set with the cast + `cold_open(f, "STEP n OF 5", "HOW TO START", detail)`
  + one big `say(TITLE)` at **y ≈ 700** — at y 560 the caption collided with the cold-open card (caught in test frames). Then 2–4 prop shots
  (one per fact: price tag drop, stamp, calendar, chip with the source), back to a scene within ≤ 2 shots. Show the waypoint cards from the
  shot start (an empty disc waited ~1 s for the word "five").
- **Staging helpers (2 Nov, HOW TO START EP 2 vending, `template/scripts/anim_props4.py`):** `thought(f, x, y, w, el)` (dream cloud), `notes(f, x, y, t)`
  (rising music notes — a jingle, a "singer"), `coin_rain(f, t, t0, x, y)` (money draining), `split_wipe(f, g, t, t0)` (right half wipes to a second
  frame: "meanwhile" / cause → effect). Flashback block = `sepia_tone` on every shot of the era + `calendar_el` counting back on the first one.
  Never give a character `phone_el()` / `phone2_el()` to hold — they render as a huge phone with an old chat / a "SEND THIS" button over the face;
  use a chip ("CALLING PAST BUYER #3…") or a `bubble_el`. Keep `say()` off giant-head close-ups (`person_head_at` s ≥ 1.8): put the caption at y 450–600.
- **Props kit 6 (3 Nov, Pepsi pilot, `template/scripts/anim_props6.py`, in anim.py's exec list):** `can_el`, `can_pile(f, cx, base_y, w, rows)`, `padlock_el(w, n, open_)` (roadmap locks), `calculator_el(w, display)`, `moneybag_el(w, label)`, `tee_el`, `jacket_el`, `envelope_el`. `bottlecap_el` has no size argument and is huge: `rot_comp(..., scale≈0.26)`. `choice_card(y≈1410)` covers a hero standing at feet y 1840: stand him at feet y≈1340. **Writers: name every prop by its function in the row; board_check only sees `*_el` names, so a prop written in prose ("three padlocks") can be missing without any warning.**
- **3 Nov (HOW TO START EP 3):** `talk(t)` now returns sound-shape mouths on the stick cast (`VISEME=0` = old): they read in close-ups (`person_head_at` s ≈ 1.5), so give the mentor at least two. `rope(f, x0, x1, y, t, t_close)` and `steam(f, x, y, t)` in anim_props5. SFX `sizzle`, `hose`, `rattle`. **`sepia_tone()` returns the frame: write `f[:] = sepia_tone(f, k)`** (the helper in examples before 3 Nov silently did nothing). Stamps are unreadable over busy props; use `tag_el` there. `form_el` crops long titles below w≈300.
- **Props kit 7 (4 Nov, HOW TO START EP 4, `template/scripts/anim_props7.py`):** `house_flat_el(w, wall, roof, win, door, snow_)` + `roof_pts` / `eave_pts`, `bulb_string(f, pts, t, t_on, speed, step, r, on, dead=)` (glowing bulbs that switch on in a wave along any polyline), `ladder(f, x0, y0, x1, y1)` (foot → top), `tape_run`, `snow(f, t, n)`, `spool_el`, `year_strip_el(w, lit)`, `dim_arrow`, `power_line`, `mini_card(f, top, mid)` (use instead of `cold_open` on clean episodes: small, ends above y≈400). Sets in CLEAN_SETS: wintry, garage, frostdusk, roofday, depot, january, ladderday; `_CLEAN_FLOOR` sets a snow or grass floor. SFX `bell_shake`, `tape_zip`. Second voice: `VOICES = {line_id: "af_heart:1.0"}` in vo_lines.py; give its lines 6+ words. **Any episode with a physical risk (ladders, roofs, tools): show the safe version in every frame (dry daylight, ground level in the hook), say the limit aloud, and send it to review before the first render.** Wrap `person` for idle life (see examples/christmas-lights/anim_shots.py): it costs nothing and removes the frozen look.
- Generic props now in `template/anim_props3.py` (27 Oct): `plane_el`, `card_el` (rewards card, no network logo), `cheque_el`,
  `balance` (scale that tips), `flapboard` (split-flap departures board), `mile_el` token, `chest_el` (chains/padlock),
  `suitcase_el`, `rulebook_el`, `terminal_el`, `runway`, plus `clouds`, `arrow`/`along` (animated money-flow maps) and `dial`.

## 7. Build and test
```bash
python3 /home/claude/nextbignow-videos/studio/tools/board_check.py studio/episodes/queue/<NN-slug>   # pre-flight + BUILD BRIEF (31 Oct)
cd $P && python3 scripts/make_vo.py              # voice + timings
# write scripts/anim_shots.py (SHOTLIST + shot functions + IMPACTS) — start from template/examples
python3 -I scripts/anim.py x 2,40,100,...          # test frames -> frames/r_NNNN.jpg ; LOOK at them with safe-zone guides
python3 scripts/music.py && python3 scripts/mix.py # score (edit cues section) + mix (edit SFX section) -> work/mix.wav
python3 studio/tools/trim_gaps.py $P && python3 studio/tools/tempo.py $P 1.05   # pace (11 Nov): dead air out, then +5 % WSOLA (-0.02 UTMOS)
bash scripts/render_all.sh                         # -> work/final.mp4  (~10–15 min, run in background)
```
- **Board pre-flight (R&D Tooling run, 31 Oct):** `tools/board_check.py <episode folder>` reads the queued `vo_lines.py` + `shots.md` and
  prints the **BUILD BRIEF** — every set / prop / cast look the storyboard names that does not exist in `template/scripts` (write those
  first, in `anim_story.py` style, then re-run with `--strict` until it passes) — plus rows↔lines, `say()` captions that would shrink
  below 60 % (the helper fits text into 800 px: "BEAT IT: ASK FOR THE SHORTCUT" renders 69 px tall — split or shorten), long chips,
  quote cards over 5 lines, rows of ≥ 4 s with no visible change, and the signature beats (badge, cold open, one Oops, series end card).
  Found on the first run (31 Oct): 13 of 31 captions on the two new boards would have rendered at 42–57 %; 16 assets to write.
- Music: new genre each video (used so far: funk, boom-bap, synth-pop, bluegrass, pizzicato, big-band swing, salsa, chiptune, surf-rock, bossa nova, film-noir heist jazz, ragtime stride piano, 90s British ska, calypso steel band (+ mento flashback); next try disco, marching band, baroque harpsichord, sea shanty, etc.) using GeneralUser GS GM programs;
  cues land on every reveal (`hit`, `stab`, `riser`, `sparkle`). (+ doo-wop, 3 Nov; winter jazz waltz, 4 Nov; bedroom pop, 5 Nov; lo-fi hip-hop, 6 Nov; board asks for minimal UK garage (Shorts money).) Mix targets (template pre-limiter `LIM=-8` since 3 Nov: reaches −10.9 LUFS, −1.4 dBFS): master **−11 LUFS, −1.0 dBTP** (template loudnorm TP −1.0 since 2 Nov — at −1.5 the limiter capped loudness at −11.9 LUFS); VO/bed ≥ 14 dB per line
  (mix.py prints it); voice clean and on top.
- Word guard (since 27 Oct R&D run 6, template default `GUARD=12`): mix.py keeps music + SFX ≥ 12 dB under every word on a phone
  speaker, so SFX can sit right on the reveal word. Keep `bed = bed_carve.guard(...)` when you copy an older example's mix.py (examples
  before 28 Oct don't have it). Check: `python3 /home/claude/nextbignow-videos/studio/tools/mix_check.py $P` → momentary LD p5 ≥ 10 LU,
  no line < 10 LU, ESTOI phone ≥ 0.95; log the numbers. mix.py prints `loudnorm mode` (dynamic is expected for now — R&D backlog).
- VO level automation (`LINE_DB` in mix.py, since 27 Oct): quiet intimate/"secret" lines −2 to −3 dB, lift reveal lines +1 dB; a −60 dB room tone fills the gaps so pauses don't drop to digital silence.
- SFX per moment (`sfx_lib.py`: whoosh, boom, pop, ding, click, thud, chaching, clink, scratch, card_in, buzzer, creak, …).

## 8. QA before posting (all must pass)
1. Contact sheet of the final (1 frame / 2 s) — look at every frame: no broken layouts, nothing in unsafe zones, text spelled right, no logos.
   `tools/layout_check.py $P`: 0 settled caption violations, frame 0 not empty (no WARN). Log "layout N viol" in the run log.
2. `ffprobe`: 1080×1920, h264 + aac; `ebur128`: about −11 LUFS, peak ≤ −1 dBTP; `tools/mix_check.py`: LD p5 ≥ 10 LU, ESTOI phone ≥ 0.95.
3. Facts on screen and in VO match the sources.
4. `python3 studio/tools/voice_report.py $P work/vo.wav` — UTMOS ≥ 4.0 (aim ≥ 4.3), no ASR bad lines, pitch range ≥ 15 st, 165–190 wpm. Put the numbers in the run log.
4b. `python3 studio/tools/story_check.py $P` — ≥ 6/7 story rules and R8 roadmap passed (it reads real times from `work/align.json`).
5. Score the quality bar in `IMPROVEMENTS.md` (hook, clarity, pacing, voice, visual, audio, ending). Anything below 4 → fix it first.
6. Originality: it must not look like the previous video with new text (YouTube treats "minor template changes" as unoriginal).
   At least one new prop set, one new layout idea and a different music genre.

## 9. Host and post
- **GitHub rejects files over 100 MB** (pre-receive hook): the crf-14 master can be 115 MB at 80 s. Before hosting, re-encode:
  `ffmpeg -i final.mp4 -c:v libx264 -preset medium -crf 18 -maxrate 9M -bufsize 18M -tune animation -pix_fmt yuv420p -c:a copy -movflags +faststart final_post.mp4` (≈24 MB, visually identical on a phone).
- Never commit MP4s to `main`. Host on a throwaway branch: `bash studio/host_video.sh push $P/work/final.mp4 <slug>` → prints
  `RAW_URL=…` (public, 200). After `createScheduledPost` returns a `static.metricool.com` media URL, run
  `bash studio/host_video.sh delete <slug>`. If the returned media is NOT on static.metricool.com, keep the branch and say so in the report.
  (As of 27 Oct, branch deletes from the cloud sandbox fail with HTTP 403 — leftover `omb-*` branches are harmless; list them in the report so the owner can delete them. Push each host attempt under a new slug: re-pushing an existing branch is rejected.)
- Metricool: brand **Oopsmybusiness, blogId `7643430`**, timezone `Asia/Calcutta`. Never post to other brands.
- Time (since 31 Oct, BRAND.md §5): **two episodes a day, slots 00:00 and 05:00 IST** (18:30 / 23:30 UTC = UK evening and US
  evening). `getScheduledPosts` for 7643430 (next 3 days) and use the earliest of those slots that is ≥ now + 20 min AND ≥ 4.5 h
  after the latest scheduled post and has no post yet; a Part 2 takes the same slot as its Part 1, one day later.
  **Owner's safety rule: never two posts less than 4.5 h apart.**
- `createScheduledPost` (see the Starbucks post in topics.md for a working example):
  - providers: instagram + youtube; `media`: [raw URL]; `videoCoverMilliseconds`: a frame with the hook caption visible.
  - `text`: line 1 = keyword sentence (brand + claim); 2–3 short lines of value; CTA line; "Follow for more business secrets.";
    "Sources: …"; then **exactly 5 hashtags** (topic/brand, niche, broad). No emoji. ≤ 2,000 characters.
  - `instagramData`: {type REEL, showReelOnFeed true, collaborators [], isAiGenerated true} (AI voice = realistic-sounding audio);
    `firstCommentText` = the episode's question in one line ("FIGHT or FOLD — what would you do?") so the comment thread starts there.
  - Series line in the text after the first line ("Your Move · Ep 1 · Part 1"); the CTA line repeats the choice ("Comment FIGHT or FOLD").
  - Sponsored episodes (only when a real deal exists): BRAND.md §4 disclosure — on-screen "Ad · Paid partnership with X" from the
    first second, said in the first 5 s, text starts with "Ad:", Instagram paid-partnership label, YouTube paid-promotion box, "(Ad)" in the title.
  - YouTube title: keyword first **and the most surprising number + an open loop** ("Airline Miles: Why Amex Paid Delta $8.2B").
    First YouTube data (27 Oct): number/tension titles got 740–1,360 views, flat statement titles 41–326.
  - `youtubeData`: {title ≤ 50 chars keyword-first, type short, privacy public, tags 5–8 search phrases, category EDUCATION,
    madeForKids false, isAiGeneratedContent false} (animation + generic narrator = no YouTube AI disclosure).
  - `mediaAltText`: one sentence describing the video with the keyword.
- Append the line to `studio/topics.md`, commit + push.

## 10. Learn, log, report
- Add the run to `IMPROVEMENTS.md` log (upgrades tried, voice_report numbers, kept/dropped) and update `PERFORMANCE.md`.
- Commit + push `studio/` changes (fetch + rebase first; another task shares this repo — only touch `studio/`).
- Final message: title, scheduled time (IST), 1-line topic summary, what improved vs last video, what the data said, sources.
  Clean up the project's work files.
