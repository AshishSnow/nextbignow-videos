# FreshNestHub autonomous reel engine — PLAYBOOK v4 "CHUBBY" (approved by owner 26 Oct 2026)

Runs every 5 hours. Every run makes ONE new 45–62 s vertical animated reel for **FreshNestHub** — fun, surprising
**food + health facts** — and posts it to **Instagram @fnhtruths** and **YouTube Shorts (@FreshnestHub)** via Metricool.
The owner (Ashish) is usually not watching: decide, build, verify, post, log. Never ask questions mid-run.

**Approved style = `template/` (episode 07 "carrots turn your skin orange", posted 26 Oct 18:00 IST). Copy its approach.**
- Bright animated sets (studio engine: gradient stage + big colour circle, flat shaded props, punchy transitions,
  screen shake on impacts), like the owner's OopsMyBusiness / NextBigNow reels — but with FreshNestHub's OWN mascot.
- Mascot **"Chubby"** (`template/fnh_char.py`): round head with a hair curl, big round mint-green shirt belly,
  stick arms + legs. NEVER use the OopsMyBusiness square-face guy (`guy()` from anim_base) or any other mascot.
- Voice: energetic young male (studio `make_vo.py`: Kokoro am_eric/am_fenrir blend + Praat prosody). MrBeast-style
  script: simple words, high energy, stakes, short sentences — but NOT rushed (speed 1.0, real pauses).
- Topics: food + health facts that make people say "wait, what?" (see topic_ideas.md).

Rejected (never go back): Nessa stick-girl + beauty trivia (ep 01–04), white-paper medical plates + British female
voice (ep 05), OopsMyBusiness mascot (ep 06). Ignore episodes 01–06 except as history.

---------------------------------------------------------------------------------------------------
## 0. Setup (≈5 min)
```
# repo attached with add_repo(owner="AshishSnow", repo="nextbignow-videos", access="push")
git clone --depth 1 https://github.com/AshishSnow/nextbignow-videos /home/claude/nextbignow-videos
ENG=/home/claude/nextbignow-videos/fnh-engine
bash $ENG/setup.sh                      # studio engine -> /home/claude/studio (models, soundfont, fonts, python libs)
```
Never edit anything outside `fnh-engine/` (studio/ and oopsmybusiness/ belong to another channel).

## 1. Learn first (≈10 min) — mandatory, see improvements.md
1. Read `improvements.md` (algorithm notes, protocol, backlog, learnings, changelog) and `performance.md`.
2. Refresh performance.md from Metricool analytics (exact metric ids are in its header) and write 1–2 dated learnings.
3. If the algorithm notes are older than 7 days, re-check (WebSearch: Instagram Reels + YouTube Shorts ranking news)
   and update section A.
4. Choose this video's upgrades: at least ONE voice + ONE visual/edit improvement (section C or your learnings).
   Apply them in this episode and log them in section E at the end. Never ship a video identical in method to the last.

## 2. Claim a topic
1. `git pull`, read `topics_done.md` (titles + openings already used) and `topic_ideas.md`.
2. Take the FIRST "UP NEXT" topic not in topics_done. If facts don't hold up → next. If the list is empty, find new
   ones of the same kind (food science, everyday-body facts, food myths) with WebSearch.
3. Topic test: instantly clear in 3 s, surprising, about food/the viewer's own body, can be SHOWN with Chubby + props,
   ≥ 2 reputable sources (NIH/NHS/CDC/FDA/WHO/Mayo/Cleveland Clinic, universities, journals, major outlets).
4. Append `CLAIMED <date time IST> | NN-slug | working title` to topics_done.md, commit, fetch+rebase, push.
   NN = next free episode number (the highest NN in topics_done/episodes + 1); slug = the topic's slug.
   Topic choice may follow the learnings (e.g. broad, everyday topics reach more) — skip ahead in the list if justified.

## 3. Research (≈10 min)
WebSearch/WebFetch the sources; write down every fact + URL. Numbers must match the source; contested → "scientists
think…" or drop it. NO dosing, treatment or diagnosis advice; at most one safe general tip ("if X, see a doctor").
No brand names/logos in visuals (generic "a can of cola" is fine), no real private people.

## 4. Script — `scripts/vo_lines.py` (12–15 lines, 125–150 words, 45–55 s of voice; longer only if data says it holds)
Format: `(id, text, speed, pause_after, base_semitones, range_expand, [stressed words], ending)`; see template.
- Speed 1.0 everywhere, pauses 0.30–0.45 s. Stressed words = 1–3 per line, copied exactly as written (with punctuation).
- Line 1 (`i1`) = clear intro question inside 3 s: "Do you know…?" naming the food/body thing + the surprise.
- Then: confirm/wow line → explain step by step (one idea per line, each will get its own shot) → a number/evidence
  line → one honest catch or safe tip → a twist/bonus fact → CTA "Send this to the friend who …!" tied to the topic.
- Numbers as words ("ten a day", "four milligrams"). Avoid words the TTS/ASR confuses (check the read-back).

## 5. Build
```
P=$(bash $ENG/new_ep.sh NN-slug)          # project = studio template + FreshNestHub template (ep 07 files)
# write $P/scripts/vo_lines.py, then:
cd $P && (set -a; . $ENG/voice.env; set +a; python3 scripts/make_vo.py) && python3 $ENG/engine/tools/asr_check.py $P
# every line must read back right. voice.env = the channel voice; voice upgrades are logged in improvements.md
python3 -c "import json;A=json.load(open('work/align.json'));[print(w['line'],w['w'],w['t']) for w in A['words']]"
```
Then write (read the template versions first — they are the reference):
- `scripts/anim_props6.py` — NEW props for this topic (PIL supersampled, gradient `shape_grad`, soft shadows `_ov`,
  ink outlines where needed, cache with `gcache`). Reuse existing props when they fit (list below).
- `scripts/anim_shots.py` — SHOTLIST (16–20 shots, 1.5–4.5 s each, cut on word times `T(line, word)`), one
  `shot_<ID>(t, n)` per shot, `IMPACTS` (shake on every big moment). Keep `ui_word/rays/slam/ring/rs/_bl/compose` as in
  the template. Transitions vary: cut, whip, zoom, flash, punch, focus.
- `scripts/music.py` — cues on every reveal. **New genre each video** (template = bouncy food-funk with marimba/slap
  bass + 1940s march section; others: synth-pop, lo-fi hip hop, latin, orchestral pizzicato, surf rock, chiptune…).
- `scripts/mix.py` — an SFX for every moment (crunch, pop, ding, boing, whoosh, thud, buzzer, ping, drone… or new
  synthesized ones). Keep the bed level and loudnorm section. VO/bed must be ≥ 14 dB on every line (printed).

### Chubby API (`fnh_char.py`)
`chub(f, x, y, s, la, ra, ll, rl, mouth, blink, brow, look, expr, tint, hold, hold_off, hold_front, bob, op, lean, squash, sit, nose, cap)`
- (x, y) = feet baseline; height ≈ 480·s; head centre ≈ (x, y − 420·s). Typical: s 0.8–1.15 at y 1440–1480.
- arms (upper°, fore°) from straight down, + = outward: relaxed (20, 10); cheer (150, 170); point (70, 40);
  scratch head (−150, −150); hand to mouth (148, −130) + `hold=carrot_side(...)`, `hold_front=True`; hold up (150, 175).
- `expr`: n, wow, sus, smirk, sad, happy; `mouth`: 0, 1, 2, 3, "o" (`talk(t)` lip-syncs to the VO, `munch(t)` chews);
  `brow`: n, up, sus, sad; `look=(−1..1, −1..1)`.
- `tint` 0..1 turns skin orange (only when the story is a colour change); `nose=0..1` shows/tints a nose; `cap=True` pilot cap.
- `chub_head_only(f, x, y, s, t, ...)` for big face close-ups; `logo_el()` = FreshNestHub logo with Chubby's head.
Chubby appears in most shots, reacting to the fact (eating, shocked, pointing, cheering). Give him a different action
in every video.

### Reusable props (already loaded)
anim_props: tag_el, bubble_el, magnifier_el, glow, steam, coin_el, phone_el · anim_props2: calendar_el(top, big),
sign_el, phone2_el(msg1, msg2, pressed), check_el(r, ok), cash_el · anim_props3: stamp_el, vault_door_el, app_phone_el ·
anim_props4: burst_el, readout_el, dial(f, x, y, s, "mph"|"g", v, txt), stopwatch_el, splash, eye_el, molar_el,
forceps_el, weight_el, bscale_el, seat_el, wheel_el, belt_draw, bars2 (comparison bars), speed_lines, add_patch ·
anim_props5: carrot_el, carrot_side, dots (pigment/particles), machine_el, capsule_el, gauge_tube, vessel (blood flow),
skin_block (skin layers), palm_el, sole_el, eye2_el(sclera, skin), baby, bowl_el, spoon_el, plane_el, prop_disc,
radar_screen, moon, zzz_moon, mirror_el.

### Visual rules (mandatory)
- 1080×1920, 24 fps. Safe zones: nothing important in top 250 px, bottom 420 px (y > 1500), right 120 px, left 60 px.
- Captions ONLY at key moments: `ui_word(f, lead, BIG, 470, …)` — small lead + one big word/number, centred x = 540,
  ≤ 840 px wide; use `[word]` for an accent colour. No word-by-word subtitles, no emoji, no persistent counters.
- First 3 s: strong visual action (Chubby doing something) + one short caption; never a giant text-only opener.
- Change the stage scheme every shot (sky, yellow, purple, teal, red, emerald, orange, pink, cream); vibrant, never dull.
- Source chip for key numbers: `chip("Source: …", INK, WHITE, 22)` at y 1462.
- End: phone "SEND THIS" CTA with Chubby, then logo sting + "follow for more health facts".
- New opening idea every video (check the topics_done "opening" column).

### Test before the full render (mandatory)
`python3 -I scripts/anim.py x <2 frames per shot>` → frames/r_NNNN.jpg; tile them with safe-zone guides:
`python3 $ENG/engine/tools/sheet.py /tmp/sheet.jpg frames/r_*.jpg` and LOOK (Read the image). Fix overlaps, clipped
props, text in unsafe zones, props hidden behind Chubby's head (use hold_front), unreadable diagrams. Re-test.
Then: `SKIP_VO=1 bash $ENG/build_ep.sh NN-slug` (≈7 min) → /home/claude/outputs/NN-slug.mp4 + _sheet.jpg.
QA: 1080×1920, 45–62 s, ≈ −11 LUFS, peak ≤ −1 dBFS; look at the sheet; facts on screen = sources.

## 6. Host + post
`bash $ENG/host_video.sh NN-slug push` → RAW_URL. Metricool brand **Freshnesthub blogId 7643474**, tz Asia/Calcutta.
Time: `getScheduledPosts` (7643474, last 24 h → next 2 days). Post at the later of (now + 10 min) and
(latest FreshNestHub post + 4 h 30 min). TWO posts, same time:
- Instagram: providers [instagram], media [RAW_URL], videoCoverMilliseconds = a frame with Chubby + the hook caption
  (≈ 2500–3500), mediaAltText one sentence, instagramData {type REEL, showReelOnFeed true, collaborators [],
  isAiGenerated true}. Caption: line 1 = the search question ("Can eating too many carrots turn your skin orange?"),
  3–5 short lines of facts, question/CTA line, `Sources: …`, then ≤ 5 hashtags (2 topic, 1–2 niche like #healthfacts
  #foodfacts #nutritionfacts, `#freshnesthub`). No emoji. firstCommentText = one specific question that invites
  comments (e.g. "Have you ever felt this after eating pineapple? Yes or no?").
- YouTube: providers [youtube], youtubeData {title keyword-first ≤ 60 chars, type short, privacy public, tags 8–12
  phrases, category EDUCATION, madeForKids false, isAiGeneratedContent false}. Description: keyword sentence, 2–3 lines,
  "Animated explainer. Narration voice is AI-generated.", Sources, 3 hashtags incl. #shorts.
Check both returned media URLs start with https://static.metricool.com/, then `bash $ENG/host_video.sh NN-slug delete`
(the session proxy usually refuses branch deletes — just note it in runs_log).

## 7. Log + commit (code only — never commit mp4 to main)
Replace your CLAIMED line in topics_done.md with `| date | NN-slug | title | opening used | IG planner | YT planner |`,
append a runs_log.md line (duration, LUFS, peak, VO/bed min, shots, post time, links, sources, upgrades made),
add your section-E line to improvements.md and update performance.md, copy the project's
scripts to `episodes/NN-slug/`, commit, fetch + rebase, push. Delete the project's work/ and frames/ after posting.

## 8. Failure policy
Facts can't be verified → next topic. Build fails → fix and retry (max 2 full renders). Still failing → do NOT post;
log the reason, mark the CLAIMED line FAILED, commit, end. Never edit/delete published posts. Never post to other
Metricool brands (nextbignow 7639492, Oopsmybusiness 7643430).
