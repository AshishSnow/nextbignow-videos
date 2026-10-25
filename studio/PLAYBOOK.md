# OopsMyBusiness autopilot — playbook

One run = one finished, fact-checked, original Short/Reel, scheduled on the **OopsMyBusiness** brand in Metricool.
Follow every section. Quality beats speed: never post a broken, unchecked or unsourced video — if a step fails and
can't be fixed, stop, schedule nothing, and report what failed.

## 0. Setup (fresh workspace)
```bash
# repo is attached + cloned at /home/claude/nextbignow-videos (see run prompt)
bash /home/claude/nextbignow-videos/studio/setup.sh          # models, soundfont, fonts, libs -> /home/claude/studio
P=$(bash /home/claude/nextbignow-videos/studio/new_project.sh <slug>)   # project from template
```
Disk is limited (~8 GB free): delete `work/part*.mp4`, frames and old projects after posting.

## 1. Channel and audience
- OopsMyBusiness = business secrets / hidden business models / how companies really make money. Audience: US, UK, Europe.
- Faceless, fully animated: square-face stick-figure mascot (cream rounded-square head, black stick body, orange tie), bright designed sets.
- Brand names may be said and written as plain text (commentary). **Never draw a real logo, mascot, packaging or trade dress** (e.g. no green siren, no golden arches). Use generic props.

## 2. Topic (pick one, never repeat)
- Read `studio/topics.md`; never repeat a topic or close variant. Also vary the *type*: hidden business model, pricing trick, psychology trick, loophole, surprising number, founder story.
- Must be instantly clear in 3 seconds and have a "wait, what?" twist. Prefer famous brands people use (global appeal).
- Idea bank (each must be verified first, skip any you can't source): IKEA maze + cheap food at exit; printer ink vs champagne price per ml;
  cinema popcorn margins; gyms profiting from members who never come; airline loyalty/credit-card money; Nespresso/Gillette razor-and-blades;
  Visa/Mastercard swipe fees; Amazon's profit coming mostly from AWS; Trader Joe's no-sales strategy; Aldi's coin cart; Rolex scarcity;
  Hermès Birkin waitlist; De Beers "diamonds are forever"; Duolingo streak psychology; Uber surge pricing; Krispy Kreme hot light;
  Chick-fil-A closed Sundays; Ferrari limited production; Disney parks pricing; Spotify royalties per stream; Netflix password sharing crackdown;
  casinos without clocks; free-to-play games and "whales"; Apple's accessories margins; Domino's as a tech company; Red Bull as a media company.
- Avoid: medical/health claims, politics, legal accusations, anything defamatory or speculative about named people.

## 3. Research and fact rules (strict)
- Use WebSearch/WebFetch. Every number in the script needs a primary source (SEC 10-K/10-Q/8-K, company release, government data such as FDIC/BLS)
  or two reputable outlets. Use the **latest** data available today; say "last year"/"in 2025" precisely.
- Round honestly ("about $1.7 billion", "over $200 million"). Quotes must be real (light profanity removal is fine).
- Keep a list of sources; put a short "Sources:" line in the post text and a small source chip on screen for key stats.

## 4. Script (`scripts/vo_lines.py`)
Format: `(id, text, speed, pause, base_semitones, range_expand, [stressed words], ending)` — see `examples/*/vo_lines.py`.
- 50–70 s total, 14–19 lines. MrBeast-style: simple words, high energy, stakes, short sentences.
- Line 1 = hook inside 3 s with the brand + the surprising claim (vary the opener: "Do you know…?", a shocking number, "This is why…", etc.).
- Middle: 3–4 clear beats (steps/secrets/reasons) — vary the structure from the previous video.
- Payoff twist line, then CTA: "Send this to the friend who …!" (always tied to the topic).
- Line ids: hook `i*`, beats `a*`/`b*`/`c*`/`d*`, ending `e1`, CTA `e2` (the template's shots use these). Unique words help timing anchors.
- Numbers: write them as words the TTS reads cleanly ("one point seven billion", "four ninety-nine"). Check abbreviations in the ASR read-back.

## 5. Voice (local, no ElevenLabs)
`python3 scripts/make_vo.py` — Kokoro blend 75% am_eric + 25% am_fenrir, Praat PSOLA prosody: lifted register (~170 Hz median),
wide pitch range, stressed words, question rises, low endings. Energy like an energetic, expressive, fun young male narrator.
Knobs (env): `EW` (eric weight 0.75), `GT` (target Hz 165), `BS` (line offsets 0.6), `EXS` 0.5, `BMP` 0.8, `STR` 1.0. Keep defaults.
QA: transcribe each line with parakeet (see `make_vo.py` align) — every line must read back correctly; fix spelling/phrasing and regenerate if not.
Clean, no hiss, natural. Output: `work/vo.wav`, `work/align.json` (word times used everywhere via `T(line_id, word)`).

## 6. Visual style (non-negotiable)
- 1080×1920, 24 fps. Safe zone: nothing important in top 250 px, bottom 420 px, right 120 px, left 60 px. Key visuals central.
- Bright, vibrant, extra-saturated sets (`stage(scheme, sun_colour, x, y, R)` — big colour circle), beautiful background in every shot.
  Schemes: cream, sky, yellow, purple, teal, red, emerald, orange, pink. Change scheme every shot; match colour to the moment.
- Two-tier editorial captions **only at key moments** (`ui_word(f, lead, BIG, y≈470, t, t0, ...)`): one big word/number + small lead.
  No word-by-word subtitles, no emoji, no persistent counters/meters.
- First 3 s: a strong visual (object + action) + one short caption with the brand/claim. No giant text-only opener.
- Every shot: a real prop or diagram that shows the idea (props in `anim_props*.py`; write new ones per topic in a new `anim_props4.py`
  and add it to `anim.py`'s exec list). Big objects, movement on beat (pin/pop, flips, slams), screen shake on impacts (`IMPACTS`),
  transitions vary: cut, whip, focus, zoom, punch, flash.
- Mascot `guy(...)` appears in several shots with expressions (wow/sus/smirk), talking mouth `talk(t)`; holds props via `hold=`.
- On-screen source chip for key stats (`chip("Source: …", INK, WHITE, 24)` near y≈1430).
- End: phone "SEND THIS" CTA scene, then the OopsMyBusiness logo sting ("follow for more business secrets").
- Try something new every video (new props, new layout idea such as split screen / map / chart / stamp / vault) — never clone the last video.

## 7. Build and test
```bash
cd $P && python3 scripts/make_vo.py              # voice + timings
# write scripts/anim_shots.py (SHOTLIST + shot functions + IMPACTS) — start from template/examples
python3 -I scripts/anim.py x 2,40,100,...          # test frames -> frames/r_NNNN.jpg ; LOOK at them with safe-zone guides
python3 scripts/music.py && python3 scripts/mix.py # score (edit cues section) + mix (edit SFX section) -> work/mix.wav
bash scripts/render_all.sh                         # -> work/final.mp4  (~10–15 min, run in background)
```
- Music: new genre each video (funk, boom-bap, lounge jazz, synth-pop, orchestral pizzicato, latin, etc.) using GeneralUser GS GM programs;
  cues land on every reveal (`hit`, `stab`, `riser`, `sparkle`). Mix targets: master **−11 LUFS, −1 dBTP**; VO/bed ≥ 14 dB per line
  (mix.py prints it); voice clean and on top.
- SFX per moment (`sfx_lib.py`: whoosh, boom, pop, ding, click, thud, chaching, clink, scratch, card_in, buzzer, creak, …).

## 8. QA before posting (all must pass)
1. Contact sheet of the final (1 frame / 2 s) — look at every frame: no broken layouts, nothing in unsafe zones, text spelled right, no logos.
2. `ffprobe`: 1080×1920, h264 + aac; `ebur128`: about −11 LUFS, peak ≤ −1 dBTP.
3. Facts on screen and in VO match the sources.

## 9. Host and post
- Copy to the repo: `oopsmybusiness/NN-slug.mp4` (next number), commit, push. Check
  `https://raw.githubusercontent.com/AshishSnow/nextbignow-videos/main/oopsmybusiness/NN-slug.mp4` returns 200 with the right size.
- Metricool: brand **Oopsmybusiness, blogId `7643430`**, timezone `Asia/Calcutta`. Never post to other brands.
- Time: `getScheduledPosts` for 7643430 (next 2 days); schedule at `max(now + 20 min, latest scheduled post + 3 h)`; prefer the higher
  value from `getBestTimeToPostByNetwork` within ±45 min of that slot. Never two posts less than 2.5 h apart.
- `createScheduledPost` (see the Starbucks post in topics.md for a working example):
  - providers: instagram + youtube; `media`: [raw URL]; `videoCoverMilliseconds`: a frame with the hook caption visible.
  - `text`: line 1 = keyword sentence (brand + claim); 2–3 short lines of value; CTA line; "Follow for more business secrets.";
    "Sources: …"; then **exactly 5 hashtags** (topic/brand, niche, broad). No emoji. ≤ 2,000 characters.
  - `instagramData`: {type REEL, showReelOnFeed true, collaborators [], isAiGenerated true} (AI voice = realistic-sounding audio).
  - `youtubeData`: {title ≤ 50 chars keyword-first, type short, privacy public, tags 5–8 search phrases, category EDUCATION,
    madeForKids false, isAiGeneratedContent false} (animation + generic narrator = no YouTube AI disclosure).
  - `mediaAltText`: one sentence describing the video with the keyword.
- Append the line to `studio/topics.md`, commit + push.

## 10. Report
Final message: title, scheduled time (IST), Metricool planner link, 1-line topic summary, sources. Clean up the project's work files.
