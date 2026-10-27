# OopsMyBusiness autopilot — playbook

One run = one finished, fact-checked, original Short/Reel, scheduled on the **OopsMyBusiness** brand in Metricool.
Follow every section. Quality beats speed: never post a broken, unchecked or unsourced video — if a step fails and
can't be fixed, stop, schedule nothing, and report what failed.

**Every video must be better than the last one** (owner's standing order). Before building, do the learning loop in
`IMPROVEMENTS.md`: refresh `PERFORMANCE.md` from analytics, refresh `ALGORITHM.md` if older than 7 days, pick at least one
voice upgrade and one visual/story upgrade, test them, keep only what measures better, and log it.

**Time budget:** take your time — a good video takes 90–150 minutes. Don't rush any step. The only hard limit: be finished
(scheduled, logged, pushed) about 30 minutes before the next run starts (runs fire every 5 hours).

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
- Keep a list of sources; put a short "Sources:" line in the post text and a small source chip on screen for key stats.

## 4. Script (`scripts/vo_lines.py`)
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
Weak short reveal lines (per-line UTMOS < 4.2, e.g. "Her income? Zero." 4.14): first lengthen the text slightly ("Her income that year?
Zero." → 4.29, 27 Oct Monopoly A/B) — 2–3-word lines are always the weakest. Yes/no hook questions get softened by the prosody gate
(q_rise −1…−2 st): keep them short and put the key word last.
Alternative engine (opt-in, see `VOICE.md`): `ENGINE=chatterbox python3 scripts/make_vo.py` — Chatterbox-Turbo (MIT) in our own
synthetic narrator's voice, +0.06 UTMOS per line; since 27 Oct its `low` lines get a last-word fall (`lib/end_contour.py`, `ENDS=0` to
disable, `END_ST` depth, default −4 st) so reveals land (−3.5…−4 st vs −1 before), but its questions still fall → Kokoro stays the default. Its output is deterministic, so if a
line reads back wrong, rephrase it (re-running gives the same audio).
QA: `python3 /home/claude/nextbignow-videos/studio/tools/voice_report.py $P` (years like "twenty twenty", "ten and a half" and decades like "nineteen eighties" are normalised; since 27 Oct it also prints per-line UTMOS mean/min, weak lines < 4.2, q_rise/low_fall, and scores files > 80 s in ≤ 60 s chunks — a 117 s VO got OOM-killed as one piece) → UTMOS ≥ 4.0 (aim ≥ 4.3), `asr_bad_lines` empty,
pitch range ≥ 15 st, speaking pace 165–190 wpm. Fix spelling/phrasing and regenerate if a line reads back wrong.
A/B voice variants **one at a time** (copy the project to `projects/<slug>_B` and run there): the box has ~7 GB RAM and two Kokoro or
UTMOS jobs in parallel get OOM-killed silently (log just stops).
Output: `work/vo.wav`, `work/align.json` (word times used everywhere via `T(line_id, word)`).

## 6. Visual style (non-negotiable)
- 1080×1920, 24 fps. Safe zone: nothing important in top 250 px, bottom 420 px, right 120 px, left 60 px. Key visuals central.
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
  first frame and the seed audience decides in about 1–2 s whether to swipe.
- At least 18 shots; the picture changes every 2–3 s (new prop, zoom, angle or set). Every claim in the VO gets its own visual.
- Every shot: a real prop or diagram that shows the idea (props in `anim_props*.py`; write new ones per topic in a new `anim_props4.py`
  and add it to `anim.py`'s exec list). Big objects, movement on beat (pin/pop, flips, slams), screen shake on impacts (`IMPACTS`),
  transitions vary: cut, whip, focus, zoom, punch, flash.
- Mascot `guy(...)` appears in several shots with expressions (wow/sus/smirk), talking mouth `talk(t)`; holds props via `hold=`.
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
- Origin/history stories (type D/A): one person per era, a year card (split-flap `flapboard("1904")`) at every jump in time, and a
  spotlight-alone shot for the "and what happened to her?" re-hook.
- Real people's names in the VO: Kokoro/ASR mangle rare surnames ("Frances Gerety" → "Francis Jarity") — drop the name from the VO or put it on screen only.
- Generic props now in `template/anim_props3.py` (27 Oct): `plane_el`, `card_el` (rewards card, no network logo), `cheque_el`,
  `balance` (scale that tips), `flapboard` (split-flap departures board), `mile_el` token, `chest_el` (chains/padlock),
  `suitcase_el`, `rulebook_el`, `terminal_el`, `runway`, plus `clouds`, `arrow`/`along` (animated money-flow maps) and `dial`.

## 7. Build and test
```bash
cd $P && python3 scripts/make_vo.py              # voice + timings
# write scripts/anim_shots.py (SHOTLIST + shot functions + IMPACTS) — start from template/examples
python3 -I scripts/anim.py x 2,40,100,...          # test frames -> frames/r_NNNN.jpg ; LOOK at them with safe-zone guides
python3 scripts/music.py && python3 scripts/mix.py # score (edit cues section) + mix (edit SFX section) -> work/mix.wav
bash scripts/render_all.sh                         # -> work/final.mp4  (~10–15 min, run in background)
```
- Music: new genre each video (used so far: funk, boom-bap, synth-pop, bluegrass, pizzicato, big-band swing, salsa, chiptune, surf-rock, bossa nova, film-noir heist jazz, ragtime stride piano; next try reggae, disco, marching band, baroque harpsichord, etc.) using GeneralUser GS GM programs;
  cues land on every reveal (`hit`, `stab`, `riser`, `sparkle`). Mix targets: master **−11 LUFS, −1 dBTP**; VO/bed ≥ 14 dB per line
  (mix.py prints it); voice clean and on top.
- VO level automation (`LINE_DB` in mix.py, since 27 Oct): quiet intimate/"secret" lines −2 to −3 dB, lift reveal lines +1 dB; a −60 dB room tone fills the gaps so pauses don't drop to digital silence.
- SFX per moment (`sfx_lib.py`: whoosh, boom, pop, ding, click, thud, chaching, clink, scratch, card_in, buzzer, creak, …).

## 8. QA before posting (all must pass)
1. Contact sheet of the final (1 frame / 2 s) — look at every frame: no broken layouts, nothing in unsafe zones, text spelled right, no logos.
2. `ffprobe`: 1080×1920, h264 + aac; `ebur128`: about −11 LUFS, peak ≤ −1 dBTP.
3. Facts on screen and in VO match the sources.
4. `python3 studio/tools/voice_report.py $P work/vo.wav` — UTMOS ≥ 4.0 (aim ≥ 4.3), no ASR bad lines, pitch range ≥ 15 st, 165–190 wpm. Put the numbers in the run log.
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
- Time: fixed daily slots (IST): **00:00, 05:00, 10:00, 15:00, 19:30** (gaps 5/5/5/4.5/4.5 h). `getScheduledPosts` for 7643430
  (next 3 days) and use the earliest slot that is ≥ now + 20 min AND ≥ 4.5 h after the latest scheduled post and has no post yet.
  **Owner's safety rule: one reel/short per 4–5 hours — never two posts less than 4.5 h apart.**
- `createScheduledPost` (see the Starbucks post in topics.md for a working example):
  - providers: instagram + youtube; `media`: [raw URL]; `videoCoverMilliseconds`: a frame with the hook caption visible.
  - `text`: line 1 = keyword sentence (brand + claim); 2–3 short lines of value; CTA line; "Follow for more business secrets.";
    "Sources: …"; then **exactly 5 hashtags** (topic/brand, niche, broad). No emoji. ≤ 2,000 characters.
  - `instagramData`: {type REEL, showReelOnFeed true, collaborators [], isAiGenerated true} (AI voice = realistic-sounding audio).
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
