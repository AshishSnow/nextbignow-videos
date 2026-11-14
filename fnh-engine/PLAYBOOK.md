# FreshNestHub autonomous reel engine — PLAYBOOK v4 "CHUBBY" (approved by owner 26 Oct 2026)

Runs every 5 hours. Every run makes ONE new vertical animated reel (45 s–3 min — as long as full understanding needs) for **FreshNestHub** — fun, surprising
**food + health facts** — and posts it to **Instagram @fnhtruths** and **YouTube Shorts (@FreshnestHub)** via Metricool.
The owner (Ashish) is usually not watching: decide, build, verify, post, log. Never ask questions mid-run.

**CURRENT character + look = Chubby INK (28 Oct, owner-approved; first full episode = 17, 31 Oct). Reference episodes for the ink look:
`episodes/17-sugar-rot-teeth/` (props, places, acting, script registers) and `episodes/18-milk-boils-over/` (stove place, hand poses, follow-through, cut-away pot). Older notes below describe v4/v5; follow them only where they don't conflict.
Since 7 Nov (owner 6 Nov: "blueprint, board style with white background, 2D, no 3D"): explanation shots = the white DRAW-ON BOARD (ep 27 section), story shots = Chubby INK in lit places.**

**Approved style = `template/` (episode 07 "carrots turn your skin orange", posted 26 Oct 18:00 IST). Copy its approach.**
- Bright animated sets (studio engine: gradient stage + big colour circle, flat shaded props, punchy transitions,
  screen shake on impacts), like the owner's OopsMyBusiness / NextBigNow reels — but with FreshNestHub's OWN mascot.
- Mascot **"Chubby"** (`template/fnh_char.py` v1 shapes, overridden by `fnh_char3d.py` v2 look): round head, brown hair +
  curl, round mint-green HOODIE belly, shaded sleeves, jeans, white sneakers. NEVER use the OopsMyBusiness square-face guy (`guy()` from anim_base) or any other mascot.
- Voice (since 27 Oct 23:30, owner: "more mature, more natural"): a grown-up, warm, calm-confident guy — Kokoro
  am_michael .4 / am_puck .3 / am_eric .3, own register (voice.env "M2"). Simple words, stakes, short sentences, real pauses.
- **v5 LOOK (27 Oct, owner: "colours, more natural, 3D; change the clothes"; references = cinematic AI reels + cel-shaded
  3D cartoons)**: Chubby v2 (`template/fnh_char3d.py`: 3D-shaded skin/hoodie/jeans/sneakers, warm-brown outlines, key
  light from top-left + warm rim), cinematic light + colour on every frame (`template/anim_cine.py`), REAL PLACES with
  light and depth for story moments (kitchen / room / golden-hour outdoors), big 3D words behind the hero. Worked example (how to
  use places, counter_front, title3d, mood, finish looks): `episodes/v5-demo-onion-hook/anim_shots.py`. Never copy a reference character; never use any copyrighted character.
- Topics: food + health facts that make people say "wait, what?" (see topic_ideas.md).

**OWNER FEEDBACK 28 Oct 12:40 IST (CURRENT, overrides the v5 look where they conflict): "The 3D character is not looking good, and

> **OWNER — 11 Nov 2026 17:00 IST: "Hindi only" for YouTube.** Daily runs make the English Instagram DRAFT only and NEVER post English to YouTube; they also write a matching Hindi script (episodes/NN-slug/hindi_youtube.md). He makes the Bunty MP3 in ElevenLabs and sends it in chat, where the Hindi Short is built (bright set style of 30/31/32) and posted to YouTube.
> **OWNER — 11 Nov 2026 YouTube fix (CURRENT): Shorts get ~0-7 views each; Oct 12-Nov 11 traffic = search 59, channel 8, Shorts feed 4 (YouTube is not distributing them) while Instagram gives 1-2k.**
> - Max ONE FNH YouTube Short per 20 h (Hindi shorts made in chat count). If one exists, still make the IG draft but schedule YT 20 h after it.
> - Frame 0 = hook picture + question caption. No fade-in, no title build-up, no blank frame.
> - LENGTH 35-50 s (hard cap 58 s). Studio 28-day data: stayed-to-watch 40%, avg view 31% on 70-95 s Shorts; YouTube advises one clear takeaway in 30-45 s. A bigger topic becomes Part 1/Part 2, never a longer video. Payoff before 60% of runtime.
> - YT title = the exact searched question, <= 60 chars, no emoji/hashtags. Description line 1 repeats it. 3 hashtags incl. #shorts. videoCoverMilliseconds on the clearest hook frame.
> - Every run: log the Shorts-feed share (YTTS) in performance.md; suggest one YouTube audio-library track mood too.

> **OWNER — 9 Nov 2026 21:12 IST: "English video is good, like garlic breath. Don't give that continuous background music —
> I'll add music from Insta and YouTube (soft or hard, whichever fits best) at volume 50-60. In-between object sounds are fine."**
> So, from ep 30 on: stay in ENGLISH (the garlic-breath / ep 27 look and voice); the mix has NO baked-in music bed
> (template mix.py: BED=0 by default) — keep every per-moment SFX/foley (pops, whooshes, crunches, dings, stings) and
> the VO. Still write music.py only if a moment needs a short musical sting/SFX; no continuous score.
> In the run summary AND in Instagram firstComment-free notes, suggest ONE in-app track mood for him: "soft" (lo-fi /
> acoustic / chill piano — calm, explainer moments) or "hard" (upbeat trap / phonk / energetic pop — fast, funny, shock
> topics), plus 2-3 search words to type in the Instagram/YouTube music library, at volume 50-60 under the voice.
> **Instagram = DRAFT (owner, 9 Nov 21:22: "Save as a draft")**: create the Instagram reel with draft=true (he adds the
> in-app music and posts it himself); the YouTube short is still scheduled normally.

> **OWNER APPROVED — 7 Nov 2026 23:01 IST: "Sleepy feeling after big meal is good video with voice nice."** Episode 27
> (`episodes/27-sleepy-after-eating/`) is the current reference: the draw-on blueprint board on white for every explanation,
> Chubby acting (nodding off), one lavender accent, erase cuts with pen/eraser foley, a new music genre with a score that reacts to
> the story, and the Kokoro M2 voice with wide-range payoff lines (range_expand 1.55-1.6, base +1.0-1.2). Keep this look and voice;
> improve inside it (new hero props, sharper hooks, tighter pauses), don't swap it. (The 6 Nov 3D/Zack-style and fast-cut
> neon experiments for ep 26 were NOT approved — not posted.)
the scripts don't sound natural. Make the character more interesting; improve the scripts." Also: the scheduled tasks now run on
the Fable model.** -> Until a new character is approved, every run must: (1) spend its visual upgrade on CHUBBY HIMSELF (not on new
places): a face with real personality (bigger expressive eyes with lids + pupils that lead the action, eyebrows that shape every
emotion, a mouth with teeth/tongue for big reactions, cheeks, a real nose), a body with a silhouette (not a blob: shoulders, a neck,
hands with fingers, clothes with folds/seams/texture, a signature item e.g. a chef's apron + rolled sleeves or a cap), poses with
weight and anticipation, idle life (breathing, blinks, hair bounce), and acting beats that match each line; test a 6-expression sheet
before using him. (2) Write the script as a PERSON talking, not as lines engineered for the TTS score: contractions, direct address,
small jokes, surprise ("wait..."), rhythm changes, no filler openers ("Here's the thing:", "So yes,", "Now,"), no textbook phrasing;
read it aloud in your head; the UTMOS gate stays but a natural line beats a higher-scoring stiff one.

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
3. EVERY DAY (first run of each IST day): re-check the algorithms (WebSearch: Instagram Reels + YouTube Shorts ranking
   news, policy changes) and update section A; run the trend + topic scan (section A2) and refresh topic_ideas.md.
4. Choose this video's upgrades: at least ONE voice + ONE visual/edit + ONE topic/script improvement (section C, the
   daily scans or your learnings). Apply them and log them in section E. Never ship a video identical in method to the last.
5. Learn ONE new craft skill (improvements.md section G): research it, apply it in this video, add it to the journal,
   and if it works put it into `template/anim_fx.py` (craft library, loaded in every episode) or the voice/mix tools.
   The goal is learning and getting better — not chasing view counts.

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

## 4. Script — `scripts/vo_lines.py` (length = whatever the topic needs for FULL understanding: 45 s to 3 min)
**Owner, 26 Oct 23:25: "It's not important to make a 1-minute video — go 2 or 3 minutes if needed. Script and visuals
that make people UNDERSTAND what they are watching matter the most."**
- Length follows the content: a simple fact can be 45–60 s; a "how it works" topic 1.5–3 min. Hard cap 2:55 (both
  platforms treat vertical videos up to 3 min as Shorts/Reels). Never pad; never cut an explanation short to save time.
- Roughly 150–160 words per minute of video at the calmer A pace (≈ 120–145 words ≈ 50 s; ≈ 260–300 words ≈ 1:50).
- Clarity first: define every term the moment it appears (with a picture), one idea per line, everyday comparisons
  ("as big as…", "like a…"), "first / then / finally" signposting, and a 1-line recap before the twist/CTA.
- Longer videos need re-hooks every 20–30 s (a new question, "but here's the weird part…", a mini-reveal) so
  people keep watching; chapter-like beats: hook -> what it is -> how it works step by step -> proof/number -> twist -> takeaway.
Format: `(id, text, speed, pause_after, base_semitones, range_expand, [stressed words], ending)`; see template.
- Per-line speed variety (ep 09, +0.2 UTMOS vs all-1.0): questions/reveals 0.96–0.97, explanations 1.0, quick facts
  1.02–1.03; "..." before payoff words; keep the "q" rise on questions (also wh-questions). Pauses 0.30–0.45 s.
  Stressed words = 1–3 per line, copied exactly as written (with punctuation). Gate: voice_report utmos_chunk20 and
  utmos_line_mean vs the last episode (whole-file utmos is length-biased).
- Line 1 (`i1`) = clear intro question inside 3 s: "Do you know…?" naming the food/body thing + the surprise.
- Then: confirm/wow line → explain step by step (one idea per line, each will get its own shot) → a number/evidence
  line → one honest catch or safe tip → a twist/bonus fact → CTA "Send this to the friend who …!" tied to the topic.
- Numbers as words ("ten a day", "four milligrams"). Avoid words the TTS/ASR confuses (check the read-back).

### Script voice (28 Oct, owner: "scripts don't sound natural") — write it as a PERSON talking
Before any line goes to the voice engine, it must pass this: would a real person say it to a friend across a table?
- NO filler openers: "Here's the thing:", "So yes,", "Now,", "Scientists call it", "Experts say" as a sentence start, "It's called X."
  as its own flat line. Name things inside a real sentence: "That squeeze has a name: peristalsis. Fancy word, simple move."
- Talk TO the viewer: "you", "your", questions you'd really ask ("Ever wondered where it goes?"), small reactions ("wait...",
  "yeah, really", "I know."). One small joke per 30 s. Vary rhythm: a 3-word line after a 15-word one.
- Say it the easy way: "it comes out whole", not "it exits the body intact". Numbers as feelings: "that's sixty-one THOUSAND hours"
  with a beat before the big number. Explain, then confirm: "...so it just rides along. Like a passenger."
- Read every line aloud in your head. If it sounds like a textbook or a caption, rewrite it. The UTMOS gate still applies, but a
  natural line always beats a stiffer line that scores 0.02 higher. Reduce stressed-word markup; let the sentence carry the stress.
Sample rewrite (ep 16, same facts):
  OLD: "Here's the thing: your gut doesn't have to digest something to move it."   -> NEW: "And that's the part everyone gets wrong. Your gut doesn't need to digest something to move it along."
  OLD: "So yes, the chewy part stays in one piece, all the way through."           -> NEW: "So the chewy bit? Yeah, it really does stay in one piece. All the way through."
  OLD: "That squeeze rolls along like a wave. It's called peristalsis."             -> NEW: "The squeeze travels down the tube like a wave. There's a name for that: peristalsis."
  OLD: "Scientists call it a housekeeping wave."                                     -> NEW: "Doctors actually call it the housekeeping wave. It's sweeping the floor between meals."
  OLD: "Seven years would be over sixty thousand hours. The real number? About forty." -> NEW: "Seven years is... sixty-one thousand hours. The real number is about forty. Forty!"

## 5. Build
```
P=$(bash $ENG/new_ep.sh NN-slug)          # project = studio template + FreshNestHub template (ep 07 files)
# write $P/scripts/vo_lines.py, then:
cd $P && (set -a; . $ENG/voice.env; set +a; python3 scripts/make_vo.py) && python3 $ENG/engine/tools/asr_check.py $P
# every line must read back right. voice.env = the channel voice; voice upgrades are logged in improvements.md
# make_vo has the per-line prosody gate (PGATE 0.15, ep 12): lines our PSOLA hurts are re-rendered softer. Take-to-take
# noise is ~+-0.04 UTMOS: if a take misses the gate by a hair, render a second take before rewriting.
python3 $ENG/engine/tools/voice_report.py $P   # UTMOS (naturalness 1-5), pace, pitch range, ASR — gate in improvements.md B.2
# utmos_lines = per-line scores: rewrite the weakest lines (name-then-define order, shorter) before shipping
python3 -c "import json;A=json.load(open('work/align.json'));[print(w['line'],w['w'],w['t']) for w in A['words']]"
```
Then write (read the template versions first — they are the reference; use the craft helpers in `anim_fx.py`):
- `scripts/anim_props6.py` — NEW props for this topic (PIL supersampled, gradient `shape_grad`, soft shadows `_ov`,
  ink outlines where needed, cache with `gcache`). Reuse existing props when they fit (list below).
- `scripts/anim_shots.py` — SHOTLIST (about one shot per 2.5–3.5 s, i.e. ~18 shots per minute; every shot must SHOW
  the idea being said so a viewer understands even on mute; cut on word times `T(line, word)`), one
  `shot_<ID>(t, n)` per shot, `IMPACTS` (shake on every big moment). Keep `ui_word/rays/slam/ring/rs/_bl/compose` as in
  the template. Transitions vary: cut, whip, zoom, flash, punch, focus.
- Explaining kit (anim_fx.py, Mayer's principles): name the parts first (pre-training), label parts with `label_at`
  (leader arrow, not a far caption), `spotlight` the focus, `inset` magnified close-ups for tiny things, `pulse_path`
  for signals/flows, `recap_steps` for a 1->2->3 visual recap before the CTA, `count_up` for key numbers.
  Myth topics (ep 10, refutation text): `myth_tag` (MYTH -> red X + BUSTED) right after the myth is said, then explain;
  `split_contrast` panels for belief-vs-reality / A-vs-B tests (inside the safe zone); `chapter_card` PART n at re-hooks.
  Tiny things (ep 11, scale cues): `zoom_through(t, t0, dur, far, near, cx, cy)` = one continuous powers-of-ten push from
  something familiar into the close-up; `scale_ladder(items, cur, ...)` = "you are here" mini-map (YOU -> TONGUE x5 -> ...).
  Plan a COLOUR SCRIPT per video (ep 11: warm sets = real temperature, icy sets = what the brain feels).
  Processes (ep 12, pre-training): `cast_card(items=[(el, NAME, STATE)])` = a 2-3 s MEET THE CAST card naming the parts
  (and their states) BEFORE the process shots; `iris_mix` = "iris" transition (set `IRIS[shot] = (x, y)` on a round object
  in the previous shot) as a shape match cut; `arm_ik` (ep 12 anim_shots) when Chubby must hold a tool at a fixed point.
  Chain reactions (ep 13, progressive build-up): `chain_map(items, cur, t, t_cur, y=1395)` = a persistent strip of the WHOLE
  cause->effect chain at the bottom (past links dim, current ringed, future = '?' slots); advance `cur` on the word that names
  each link, keep main pictures in y 600-1300 while it shows, then light it up link by link as the recap. `chopper()` (lib13)
  = Chubby chopping with a knife held by IK at the grip; `knife_at(gx, gy, ang)` pivots a tool at its grip.
  Hidden quantities over time (ep 14, charts on video): `day_graph(f, t, now, lines, marks, title, ...)` = a graph of the day that
  draws itself with the voice; title = the finding, direct labels at line ends (optional (dx, dy) per line), marks = icons on the
  time axis; it returns X/Y mappers + line heads so Chubby's head can ride the 'now' point (`chub_head_only` at the head).
  Chubby has `expr="sleepy"` (heavy lids + bags) for tiredness. Score trick: `tape_stop` in ep 14 music.py (varispeed slow-down).
- `scripts/music.py` — cues on every reveal. **New genre each video** (template = bouncy food-funk with marimba/slap
  bass + 1940s march section; others: synth-pop, lo-fi hip hop, latin, orchestral pizzicato, surf rock, chiptune…).
- `scripts/mix.py` — an SFX for every moment (crunch, pop, ding, boing, whoosh, thud, buzzer, ping, drone… or new
  synthesized ones). Keep the bed level and loudnorm section. VO/bed must be ≥ 14 dB on every line (printed).

### Chubby INK (28 Oct 14:00, OWNER-APPROVED — `template/fnh_char_ink.py`, loaded last, the CURRENT character)
Owner's reference: hand-drawn round-head ink cartoon people (scribble hair, outlined clothes, thin limbs). Chubby INK is an ORIGINAL
character in that language: one wobbly warm-ink outline, scribble hair with a cowlick, dot eyes + brow strokes + mouth curve that do
all the acting, outlined mint hoodie + cream chef's apron with a pocket, rolled cuffs, ink hands with fingers, denim legs, sneakers.
COLOUR (owner chose option C): ink lines in warm dark brown (never pure black); flat fills (skin, mint, cream, denim); a soft shadow
side + light diagonal hatching; paper grain on every frame (anim_cine.finish applies it via INK_PAPER). Backgrounds: keep the lit
places but soften them 10-15 % toward paper cream so the inked character pops; ONE topic accent colour per video (gum = pink,
carrots = orange...) used on the hero prop, the 3D titles and the chips; everything else stays in the 5-colour palette (paper, ink,
mint, skin, accent). New hero props should be drawn in the same ink language: INKC outline with a fixed wobble (_wob), flat fill,
hatch on the shadow side (see _hatch) — not the glossy 3D shading of lib15/16 (keep those for old episodes only).
Same `chub(...)` API; `t=` gives breathing + blinks; `lean` tilts the head. Modes: INK_MODE = "wash" (default) | "flat" | "mono".
Sheet: /home/claude/outputs/chubby_ink_colour_options.jpg. v3 (Pixar kid) stays in the repo as a fallback (fnh_char_v3.py), not used.

### Ink prop toolkit + ink places + acting kit (ep 17, 31 Oct — the first Chubby INK episode; `anim_props_lib17.py`, `anim_cine.py`, `anim_fx.py`)
- Draw every new hero prop with the lib17 toolkit so it matches Chubby: `_cv(w, h)` (supersampled canvas -> im, d, S), `_ink_poly(d, pts, fill,
  seed)` / `_ink_ell(d, cx, cy, rx, ry, fill, seed)` (flat fill + ONE wobbly warm-ink outline, fixed per seed), `_shade(im, mask_fn, shade_fn, col)`
  (shadow side), `_hatch_in(im, box, mask_fn)` (diagonal hatching), `_face(d, S, cx, cy, s, mood, look)` (3-stroke face: n, happy, sad, ouch,
  wow, angry, love, hungry, munch), then `_done(im, w, h)`. Palette: PAPER / INKC / INK_MINT / INK_SKIN + ONE accent per video (ep 17: ACC violet
  = sugar, bacteria, acid; mint = saliva / repair). Reusable lib17 props: tooth_el(mood, film, crack, hole, spot, soft, look), teeth_row,
  bug_el / bug_crowd (bacteria citizens), candy_el(wrap|gummy|caramel|sour|choc|lolly), pail_el, acid_drop_el / acid_pool, saliva_wave,
  minerals, spit_hero_el, brush_el, paste_el, glass_el, plate_el, timer_el(k, label), podium / cloth, magnifier_ink_el.
- Places (anim_cine): `set_porch(t)` (Halloween doorstep at night, lamp), `set_bathroom(t)` (round mirror, sink at y 1330), `ink_set(scheme)` =
  a stage() softened toward paper, and `inkify(f, amt=0.13)` — call it on EVERY lit place (set_kitchen etc.) in the ink look.
- Acting (anim_fx): `POSE["point"|"present"|"cheer"|"shock"|"think"|"whisper"|"cheek"|"shrug"|"hold_up"|"arms_out"|"tada"]` = silhouette-tested
  poses (`chub(..., **POSE["shock"])`), `double_take(t, t0)` -> (look, lean, expr, brow), `flinch(t, t0)` -> (lean, squash). Check new poses
  with `python3 engine/tools/ink_sheet.py <project> out.jpg` (bottom row = black silhouettes: if the shape doesn't read, change the pose).
- Script registers (voice.env note, ep 17): asides / confiding lines base -0.6 st + speed 0.95, reveals +1.2, explanations +0.4; '...' before
  the payoff word. One-sentence jokes ('It's your spit. No, really.') score fine when they are a full natural sentence.

### Ep 18 (31 Oct, second ink episode): the STOVE place, hand poses, follow-through, the cut-away pot (`anim_cine.py`, `fnh_char_ink.py`, `anim_fx.py`, `anim_props_lib18.py`)
- Place: `set_stove(t, on=1.0, flame_w=300)` = a gas hob from the front (tiled wall + window behind, dark steel hob top at y 1300 with a cast-iron
  grate, knobs, LIVE FLAMES that flicker; `on` 0..1 = flame height, so 'turn the heat down' is one number). Pot centre for `pot_el("steel")` =
  (x, 1300 - 225 + 8); `side_flames(f, x, 1298, t, pot_w)` AFTER the pot draws flames licking up both sides; `flames(f, x, y, t, w, n, on)` anywhere.
- Chubby INK hands now have POSES: `chub(..., hand_r="grip"|"pinch"|"point"|"open", hand_l=...)` and `grip_hand(f, x, y, s, kind="grip", rot)` draws a
  fist OVER a tool handle (use with arm_ik: `spoon_at(f, gx, gy, ang)` pivots the spoon at its handle end). Pick the hand per action (grip a spoon,
  pinch a drop, point at the thing).
- FOLLOW-THROUGH (anim_fx): `drag(t, fn, frames=3, gain)` = the lagging offset of an appendage behind a motion fn(t) -> `chub(..., hair=(dx, 0))`
  shifts the scribble hair + cowlick (the hair lags the head on every jump / double take); `follow(t, t0, amp)` = overshoot + settle after the main
  part stops (used on the foam, liquids drag most); `jump_back(t, t0, dist)` = the recoil from something hot. Rule: core -> limbs -> extremities ->
  hair/cloth/liquid last; vary the lag by weight (uniform delays look robotic).
- lib18 props (ink): `pot_el(kind="steel"|"wide"|"water"|"pasta", level, foam, skin, spill)` = a CUT-AWAY pot (you see the liquid, the foam dome
  climbing above the rim, drips down the outside, an amber skin), `pot_geom(cx, cy, s, kind, level)` -> interior box + surface y for drawing things
  inside it, `bubble_el(r, jacket, mood)` (a steam bubble with an optional bead 'jacket'), `rising_bubbles(...)` (rise and pop at a surface),
  `pop_star`, `steam_wisps`, `protein_el`, `fat_el`, `sugar_cube_el`, `soap_el` / `soap_drop_el`, `spoon_el` / `spoon_at`, `butter_el`.
- Voice markup: `"word:dn"` in the stressed-words list = DROP-STRESS (the word is lowered 2 st and lengthened, not lifted) for deadpan payoffs
  ('and pop. Gone.', 'no lid.', 'you check your phone.'); A/B on ep 18 was UTMOS-neutral (+0.008 chunk20), kept for the grown-up delivery.

### Ep 19 (31 Oct, third ink episode): TIMING & SPACING kit, ink 3D titles, the LUNCH TABLE place, the apple props (`anim_fx.py`, `anim_cine.py`, `anim_props_lib19.py`)
- TIMING (anim_fx): `snap(t, t0, frames=4)` = a 4-frame pose change with overshoot (snappy, not floaty); `keyed(t, [(t0, value), ...])` /
  `pose_keys(t, [(t0, POSE), ...])` = key poses that SNAP on word times and HOLD in between; `moving_hold(t, seed)` -> dict(lean, look, bob) so a
  held pose never freezes; `take(t, t0)` = a cartoon take (3-frame anticipation down, 2-frame snap up with wide eyes, held extreme, 6-frame
  settle) -> dict(dy, squash, lean, expr, brow, look) — use it on every surprise instead of a smooth ease. Rule: few in-betweens, long holds;
  fix 'rushed' by holding the key pose longer, not by adding frames.
- `anim_cine.title_ink(f, text, y, t, t0, size, face, side)` = hand-lettered ink block title (flat face, hatched flat side, one wobbly ink outline,
  paper shadow) that snaps in; use it instead of the glossy title3d in ink episodes. When it shows the key word, the caption's big word is dropped.
- Place: `set_lunch(t)` (breakfast table by a sunny window, curtain, shelf with a fruit bowl, a wall clock at (240, 420) you can animate with a
  live hand) + `cloth_front(f, 1330)` AFTER Chubby -> he sits behind the checked cloth; props on it at y ~ 1270-1400.
- lib19 ink props: apple_el(brown, cut, mood, look, seed, white, flesh), slice_el (= a small cut half: the side-view wedge read as a BOWL in the
  test frames - a cut face with its seed star reads as apple instantly), cell_el(broken) (a cell as a room with a divider), ppo_el(mood) (the
  enzyme machine), phenol_el, o2_el, melanin_el(k) (colourless -> brown), knife_ink_el / knife_ink_at, board_ink_el, lemon_ink_el(half),
  honey_jar_el, bowl_el(level, tint), lunchbox(), sun_ink_el, food_el(kind, brown), tan_patch. Foley (sfx_lib): creep, machine_whir, dunk,
  squeeze, shimmer.
- Script devices that worked: a GUESS beat ('Quick guess, then: ...' + a held comic pause, the band drops to one fiddle note + a clock tick),
  a metaphor paid twice (the tan), a three-rule map before the fixes. Pace lesson: many short sentences inside one line slow Kokoro below the
  165-wpm gate; join them with commas or raise that line's speed.

### Ep 20 (1 Nov, fourth ink episode): CAMERA LANGUAGE kit, the NIGHT STOVE place, Chubby jaw drop + queasy face, the rice props (`anim_fx.py`, `fnh_char_ink.py`, `anim_props_lib20.py`)
- CAMERA (anim_fx): one camera idea per shot, motivated by the line: `crash_zoom(f, t, t0, z, cx, cy)` = punchline / realisation (3-frame snap,
  then HOLD); `dutch(f, t, t0, deg)` = unease; `handheld(t, amp)` -> (dx, dy, rot) for cam() = urgency / 'caught on camera'; `rack_layer(f, draw,
  sigma)` = a layer with its own focus (two layers, opposite sigmas = a rack focus); `cctv(f, t, label, 'HH:MM')` = security-camera look; push_in for
  a recap. Captions are scaled by a zoom: centre zooms at y 700-800 or draw the caption AFTER the camera move (S0 in ep 20) to keep it in the safe zone.
- Chubby INK: `mouth="jaw"` (jaw drop with tongue, use it on a take), `expr="gross"` (> < eyes + wavy mouth), POSE['sick'|'stop'|'yawn'];
  POSE dicts carry `lean` - when you also pass lean=, strip it first (ep 20 anim_shots: `nolean(POSE[...])`) or Python raises 'multiple values'.
- Place: `set_stove_night(t, lamp)` (lib20) = the stove after dinner: lights off, moonlit window, ONE warm under-cabinet lamp pooling on the pot (pot
  at (540, 1300 - 172) for rice_pot_el). Lib20 ink props: grains / rice_pot_el(level, warm, lid, mood) / rice_bowl_el(fluffy|hard|fried|salad) /
  grain_el(mood, hard) / spore_el(mood, crack) / germ_el + germ_crowd / toxin_el(mood, helmet) / microwave_el(on, timer) / thermo_ink_el(k, zone) /
  starch_rows(f, cx, cy, k, t) (retrogradation: loose swollen chains <-> tight rows, water squeezed out) / dish_el / bin_ink_el(open_) / clock_ink_el +
  clock_hands(f, x, y, hours). sfx_lib (ep 20): cctv_hum, micro_hum, micro_beep, shell_crack, giggle, pedal_bin.
- Script devices that worked: a belief flip in the hook ('the risky part isn't the reheating'), a CAUTION register on warning lines (base -0.3, range
  1.35), and a rule-of-four mnemonic (one-sentence takeaway) seeded as numbered cards and paid in the recap. Padding a line to sound casual can LOWER
  UTMOS - keep lines tight.

### Ep 21 (2 Nov, fifth ink episode): VISEMES, the MORNING WORKTOP + INSIDE-THE-SLICE places, the RACE explainer, take comping (`anim_fx.py`, `fnh_char_ink.py`, `anim_props_lib21.py`, `engine/tools/comp_takes.py`)
- `talk(t)` now returns VISEME mouths from work/align.json (`anim_fx.viseme`: vm M/B/P, vf F/V, ve EE/S/T/K, va AH, vh EH, vo OH, vu OO/W, vl L/N/D/TH; one-frame lead, tiny sounds merged, rest between words). `mouth=talk(t)` in every talking shot and use a face close-up (`chub_head_only`) when the line is an aside: the mouth is what he acts with.
- Places: `set_worktop(t)` + `worktop_front(f, 1330)` AFTER Chubby (morning kitchen, window, jars, drawers + towel, so no more empty foreground; props on it at y ~ 1200-1320); `set_crumb(t, stale, zoom)` = inside a slice (captions + diagrams stay clear, sharp pores only at the bottom).
- lib21 ink props: bread_slice_el(stale, mood, look, frozen, toast, mould), loaf_el(stale, mood, look, cap, frost), fridge_ink_el(open_, top) (top freezer + main door; shots add the loaf with a helper like ep 21 fridge_at), toaster_el + ep 21 toaster_scene (slices drawn BEFORE the toaster so they rise out of it), bread_bin_el, freezer_bag_el, nail_el, starch_guy_el, wanted_el, tomb_el, egg_el, crystal_el. Live: starch_lock(f, cx, cy, k, t, w, h, n, locks, swell) on a paper panel (k 0 = loose chains + free water, 1 = tight rows + water locked), temp_strip (thermometer ruler with a lit zone + marker), race_lanes(f, t, pos, ...) (three things race to a line: lane position = the RATE you're explaining; great for 'which is fastest').
- Voice: `python3 engine/tools/comp_takes.py <project> <tag> [margin]` keeps the best read of each identical line across takes (save a take first as work/vo_<tag>.wav + align_<tag>.json + vr_<tag>.log); confirm with voice_report. Synthetic breaths (engine/tools/add_breaths.py) lowered UTMOS: not used.
- Fetching sources: open only URLs that came from a WebSearch result; guessed URLs get refused (PROVENANCE_REQUIRED).

### Ep 22 (3 Nov, sixth ink episode): THE WALK CYCLE, three-quarter head, the PARALLAX DIWALI LANE + DIWALI ROOM, the walkable meter (`anim_fx.py`, `fnh_char_ink.py`, `anim_props_lib22.py`)
- `walk(t, x, y, s, speed, dir, period, t0, amt, track=True)` returns kwargs for chub (x, y, legs, la, ra, lean, turn, look, hair, bob): `chub(f, s=s, t=t, mouth=talk(t), **w)`. Pop `la` / `ra` when he carries something. Pass the moving x yourself with track=True, or the legs detach from the body (a bug found in the test frames). `amt` 0..1 walks him to a stop. `walk_steps(t0, t1, period)` / `footstep()` for the foley; speed 300 at period 1.08 reads as a natural heavy walk. Beat length 0.54 s locks the score to his feet.
- `chub(..., turn=-1..1)` / `chub_head_only(..., turn=)` = three-quarter head; use it whenever he looks at something at his side.
- Places: `set_lane(t, camx)` + `lane_front(f, camx)` (Diwali dusk in 4 parallax layers; feet at y 1500; scroll camx at the walk speed) and `set_droom(t, dim=)` + `table_front(f, TOP)` (night room, garland, window at y 560-1030 clear of captions, live diyas; props on the pink runner). Glow stacks fast with bloom: keep glow amt <= 0.14 per light.
- lib22 ink props: chakli_el(mood, soft) (droops + pales), sev_el, mathri_el, cracker_el, barfi_ink_el(mood, dry), cookie_el(kind, mood, change), drop_el(mood), cloud_el, straw_el, giftbox(f, x, y, s, lid, soft), gift_top(f, cx, cy, w, h, soft, dry, moods=) (top view with compartments), jar_ink_el(lid, kind, soft), oven_ink_el(on), kadai_el, paint_el, crayon_el. Live: `fly_drops(f, src, dst, t, n, rate, seed, s, arc)` (drops on arcs), `strand(f, pts, w, col)` (ink noodle), `stink`, `thirst_meter(f, t, y, band=)` -> X(v) (a 0-1 scale as a plank he walks on; good for any 'how far is it' idea), `glass_rubber(f, cx, cy, k, t)` (stiff rows <-> loose wet rows), `tank_pair(f, t, k)` (two tanks + pipe evening out). `flag()` in ep 22 anim_shots plants a labelled icon on the meter. sfx_lib (ep 22): soft_flop, footstep, clip_snap, oven_ding, soggy, drink. NOTE: card_in, clink, bubbles, micro_beep, pedal_bin add themselves and take a time first: never wrap them in add().
- Score trick: the BACKBEAT is foley: real crunches on 2 and 4 while the food is crisp, soggy thuds once it's soft (`backbeat()` in ep 22 mix.py). Voice: pause 0.1 = a LINKED line (voice.env PMIN 0.15).

### Ep 23 (4 Nov, seventh ink episode): THE FUSE, growing mould, THE CORRIDOR + MITHAI SHOP, take variants, respelling (`anim_props_lib23.py`, sfx_lib)
- Live: `fuse(f, pts, k, t, w, spark)` = a burning rope on any path (k 0..1 burnt from the free end), `sweet_fuse(f, x, y, L, k, t, curl, w, seed)` standing on a prop, `coil` (a very long one wound up), `poof` (soft mould puff), `fuzz(f, x, y, w, h, amt, t, seed, n)` = mould that GROWS from a few spots, `roots_cut(f, cx, cy, w, h, k, t, top, bk)` = cut-away with fuzz + root threads + hidden germs, `gauge(f, x, y, h, level, t)` test tube of water, `fuse_chart(f, t, t0s, y0, gap, cur=)` (the ranked list as a chart: copy the idea for any 'how long does X last' ranking), `scroll` (a list that unrolls), `dress(f, x, y, s, "aunty"|"cousin"|"boss")` + `chub(shirt=)` = other people on mute. Props: kalakand_el, rasgulla_el, rasmalai_el, sandesh_el, peda_el, boondi_el, kaju_ink_el, besan_el, patakha_el, mould_el, tray_el, tag_el2. Set the accent per video: lib23 sets ACC to marigold, your anim_props6 overrides it. `giftbox` (lib22) follows ACC.
- Places: `set_corridor(t, camx)` (Diwali apartment corridor strip; feet y 1500; doors every 420 px), `set_shop(t)` + `shop_front(f, 1300)` (mithai shop + glass counter; keep trays at y ~ 1250 so a person behind it still shows above them).
- Voice: takes at one speed are near-identical, so make alternates with SPD 0.87 / 0.893 and run comp_takes against each. Respell Indian words for Hindi vowels and check with `kokoro_onnx.tokenizer.Tokenizer().phonemize(word)`: kalaakund, rusgoola, rusmalaai, sundaysh, payda, luddoo, baysun, burfee, kaaju kutlee, boondee. T() then uses the respelled word. On screen keep the normal spelling; a Python `T(line, 'The')` matches the FIRST 'the' in the line whatever the case: use nth (it shortened a shot here).
- `mood()` works in place (returns None); `finish` looks: warm, golden, cool, night, fresh. sfx_lib (ep 23): crackle(level, dur), munch_sfx(level, dur).

### Ep 24 (5 Nov, eighth ink episode): SPEED RAMPS, the DOOR GUARD, the STARCH SPRING, the DINER (`anim_fx.py`, `anim_props_lib24.py`, sfx_lib)
- `speed_ramp(t, keys)` = story time for clock time; keys [(t, speed), ...]. Run physics on it (ep 24 `drop_scene`: y from gravity in story time, solved so the drop lands on a word). Put the slow part where the suspense is, drop the band to a heartbeat under it, foley `slowmo_swell(level, dur)` + `drip_big(level)`.
- lib24 ink props: paneer_el(mood, look, blue, oil, stache) (true 3/4 block; `top_of(x, y, s)` = its top face for stains; the old `_block` shape read as an open box), bottle_el(mood, look, cap=True) (the guard), oil_bottle_el, oil_drop_el(mood, look, ghost), iod_drop_el(mood, col=), dropper_el + dropper_at(f, tipx, tipy, s), milk_can_el, tikka_el, packet_el, menu_el, article_el, buffalo_el, flask_el, microscope_el, door_el(open_), heart_el, milkfat_el, glass2_el(col, level) (lib17 glass_el is mint), muslin_el. NOTE: fat_el follows the global ACC_L, so it turns the accent colour.
- Live: stain(f, x, y, rx, ry, k, col, seed) (anything that spreads), net_catch(f, cx, cy, w, h, k, t, fish=) (bits snap into a net that traps balls), helix(f, cx, cy, L, coil, t, lit, beads, R, turns, nb) (a chain coils into a spring; x amplitude must beat the pitch or it reads as a wave), light_in_out, phone_frame -> screen box, guard_post, waiter. Place: set_diner(t) + diner_front(f, top_y) (brick, night window, chalk menu, red booth, two lamps; stamps vanish on brick, use a chip).
- A Python `T(line, 'Its')` matches the FIRST 'it's': it shrank a shot to 0.4 s here. Use nth. audio_logo(t, lv) = the 1-s sting on the logo card.

### Ep 25 (6 Nov, ninth ink episode): TRANSLUCENCY, THE COURT, eye_lead, real clothes (`anim_props_lib25.py`, `anim_fx.py`, `fnh_char_ink.py`, sfx_lib)
- `_tl_fill(im, mask_fn, base, deep, rim, hot, light, thick, hotamt)` = translucent fill for any liquid / gel / skin-thin prop: draw it, then the ink outline over it. Set glow() behind. Used by ghee_jar_el(kind grain|liquid|split|smooth|white, level, mood, look, lid), blob(f, x, y, r, k, t, slide, col) (melting dollop with a wet trail; colour sets GOLD_C / PALM_C / PALE_C), tube_el(k, level) (acid layer turns crimson), essence_el(mood, label), glass_float(f, x, y, s, t, col, label).
- Place: `set_court(t, blur, top_y, dim)` + `bench_front(f, top_y, plate)` AFTER the judge. `judge(...)` + `judge_gavel(f, x, y, s, t, tslams, top)` + `gavel_top(f, g)` in ep 25 anim_shots = the gavel on arm IK that lands on word times (copy them). Robe = shirt=ROBE, `judge_wig(f, x, y, s)` on top. `set_store(t)` + `torch_beam(f, x0, y0, x1, y1, r, amt)` = a dark store lit by a torch; set the torch amt <= 0.75 or labels blow out.
- `chub(shirt=)` now really recolours body + sleeves and drops the apron (ep 25 fix). `eye_lead(t, t0, frm, to)` -> look, turn, lean, blink: eyes first, head 3 frames later, body last, a blink on the turn. `peek(f, t, x, y, s, expr, look)` (ep 25 anim_shots) keeps his head in a corner of diagram shots.
- Props: hand_big_el() (a big open palm with a mint cuff), palm_tree(f, x, y, s, k, t, mood) (grows from its base with snap), tin_el(fake, mood, look, seed, tag_text), label_card(f, cx, cy, t, t0s, fake, s, names, miss) (rows tick on words, misses get a red X), vanaspati_el(mood, look, tag), sesame_el, sealer_el(down), potato_el, chain_el(n, col, r, seed, mood) (a fat molecule of n beads), peaks(f, x, y, w, h, k, spike) (a chromatogram that draws itself; returns the first peak's point), test_icon_el(kind), verdict_board(f, t, t0s, y0, gap, x_ic, x_n, x_v, cur) (edit BOARD for any 'we tried them all' list), test_pill, vstamp_el(text, col, size) (a stamp on a cream slip: legible on wood, dark and pink; use it instead of stamp_el on busy backgrounds). sfx_lib: gavel, sniff, torch_click, press.
- Voice: paratones in vo_lines: a new item starts base +0.8-1.0, a closing line -0.3; neutral on UTMOS. Respell vanaspati as vanuspatee, Junagadh as Joonagurh. Never test-render during voice_report (RAM). Patch a shot by re-rendering its frames with `anim.py out A:B`, encoding the three segments with the same settings, then concat copy + mux the mix.

### Ep 27 (7 Nov, tenth ink episode): the DRAW-ON BOARD kit, nodding off, the score as a dimmer (`anim_fx.py`, `anim_props_lib27.py`, sfx_lib, ep 27 music.py)
Owner, 6 Nov 21:28 (on the 3D brain-freeze test): "use blueprint, board style with white background, don't use 3D, 2D is fine." -> ink-look episodes now put every
EXPLANATION on a white blueprint board that draws itself, while Chubby INK keeps acting in the lit places (the story). Both looks are 2D and hand-drawn.
- Board kit (anim_fx): `board_bg()` (white paper + pale blue grid), `draw_on(f, pts, k, col=BP_INK, w, seed, wob, tip, closed)` = a polyline that draws itself as k 0->1 with a
  pen tip; `draw_ell_on`, `draw_arrow_on(f, p0, p1, k, col, w, head, bend)`, `write_on(f, text, x, y, t, t0, size, col, cps)` = hand lettering (Architects Daughter, fonts/hand,
  installed by setup.sh) that writes itself left to right; `hatch_on(f, poly, k, col)` = the ONE accent pop as hatching that sweeps in; `erase_mix(prev, cur, p)` = the ERASE cut
  (add `"erase"` to compose's transitions, see ep 27 anim_shots). Rules: draw each element on the word that names it; big shape -> details -> label; one ink colour + ONE accent;
  board text >= ~60 px (the ep 27 shots wrap write_on at 1.3x: 36-50 px read too small in the test sheet); keep Chubby on the board with `peek()` at >= 0.85 head scale.
- Acting: `doze(t, t0, period, depth)` -> kwargs for chub = NODDING OFF (head sinks, lids close, then jerks up in 3 frames with wide eyes). Use it on anyone tired.
- lib27 ink props: thali_el(full|small|empty, mood), dimmer_el(k) (wall dimmer AWAKE..SLEEPY), orexin_el(lit, mood) (bulb-headed buddy), pizza_el(left), blood_el(mood),
  brain_ink_el(mood, look, level), stomach_ink_el(mood, look, grab), keys_el, envelope_el, sugar_ink_el, sofa_el, steth_el. sfx_lib: pen_draw (marker on paper, put one on every
  board shot), eraser (on every erase cut), snore, dial_ticks(t0, t1).
- Score trick: `dim_sweep(mus, keys)` in ep 27 music.py = crossfade to a low-passed copy where the story turns the lights down (the music IS the dimmer). Note: mix/music now exec
  anim_shots split at "SHOTS = [" (the shot list only), so helper code above SHOTLIST must stay plain.

### Ep 28 (8 Nov, eleventh ink episode): the MORPH CUT, the LIVER FACTORY, organ characters, tighter pauses (`anim_fx.py`, `anim_props_lib28.py`, sfx_lib, voice.env)
- `morph_mix(prev, cur, p, a, b)` (anim_fx) = a shape-match transition: a / b = (x, y, size) of the SAME object in the outgoing / incoming shot; 10 frames (0.42 s), match position first,
  then size; use it to bridge the board and the lit places (board drawing -> lit object). In compose add `elif k == "morph" and dt < 0.42: a, b = MORPH[sh["id"]]; f = morph_mix(...)`
  and a `MORPH = {shot: (a, b)}` dict (copy from ep 28 anim_shots). Seam at a pause or a fast move; not inside fast action (a hard cut is better there).
- Place: `set_factory(t, dim)` = inside the LIVER FACTORY (warm works hall, arched windows, red/blue pipes = blood in/out, lamps) + `conveyor(f, t, y=1230, speed)` (moving belt + rollers,
  props ride at y ~ 1150-1170) + `machine_el(lit)` (hopper + STEP 1 / STEP 2 lamps). Good for any 'the body processes X' idea.
- lib28 ink props: liver_el(mood, look, arms None|cross|up|work|shrug, hat), kidney_el(mood, look, flip, hat), junk_el(mood, packed) (greasy fat-soluble blob / water-blue gift box),
  detox_bottle_el(level, mood), beaker_el(fat|water, level), jerrycan_el (20 L), jug_el, prod_el(bottle|tea|patch|pills|powder) (generic, no brands), soap_bar_el, papers_el, pill_el,
  pillow_el + blanket_el (sleep without a lying body: chub_head_only on the pillow). lib28 sets ACC to lime: your anim_props6 overrides it. sfx_lib (ep 28): spray (spit-take), glug, clank, pour, belt.
- Hook data (ep 27 vs the rest): a slow first second (nodding off) held 60.7 %, an accident 75-79 %. Open MID-ACCIDENT at frame 0 (ep 28: the chug is already going, spit-take at 1.3 s).
- Voice: PZ 1.35 (tighter pauses, owner 7 Nov) is now voice.env; a rewrite can move UNCHANGED neighbour lines (b0 4.43 -> 4.26): always comp from the previous take after a rewrite.

### Ep 29 (9 Nov, twelfth ink episode): KINETIC TYPE, the OFFICE place, gas characters, EXS 0.75 (`anim_fx.py`, `anim_props_lib29.py`, voice.env)
- `kin_word(f, text, x, y, t, t0, mode, size, col, stroke=2, stroke_col=INKC, src=, t1=, amp=, stagger=)` (anim_fx) = words that REACT, letter by letter (stagger + ease-out-back entrance):
  'stink' (letters bob + sway out of phase with smell wisps), 'sneak' (tiptoe in from the left, one hop each), 'shake' (loud / alarm), 'blow' (from t1 pushed away from src=(x, y),
  nearest letters first, spinning + fading), 'drop' (from t1 they fall, bounce, lie tilted = deflated), 'breathe' (swells like lungs), 'pop'. The motion must MEAN the word; one mode
  per word; Architects Daughter at >= 100 px for headline words (two lines if > 9 letters at 150 px: 'GARLIC' / 'BREATH?' at 150 fits the safe zone, one line at 120 did not).
- Hook rule after eps 27-28 (54.9 / 60.2 % hold): the QUESTION is on screen as moving words at frame 0, over action that is already happening (the cloud already rolling into a face).
- Place: `set_office(t, dim)` + `office_front(f, top_y)` (meeting room: window + skyline, whiteboard with a chart, plant; wood table front). Other people = `chub(shirt=)` + `dress(...)`.
- lib29 ink props: garlic_bulb_el, clove_el(crush), alliin_el, enzyme_el(bite) (mint pac-man), allicin_el, gas_el2 (mauve stink cloud with a face), ams_el (bandit-masked sneaky gas),
  lungs_el(mood, look, k) (k = breath), lettuce_el, mint_sprig_el, naan_el, red_apple() (lib19 apple_el follows ACC: this keeps it red), breath_meter_el(level), tongue_teeth_el(bits),
  sweat_drop_el. Ep 29 anim_shots helpers: puff() (a cloud blown out of a mouth), wisp() (rising smell lines), kw() (kin_word with the ink stroke), board_lungs, ruler() (a 2-day
  timeline with sun/moon marks + a bar that runs to a time), bar()/chart() (a 5-bar result chart with food icons).
- Voice: EXS 0.75 in voice.env (A/B: chunk20 +0.012, first-100 s +0.13, line mean = ; f0 16.0 st). A deeper blend (michael .5) lost 0.025: M2 stays. Still true: lengthen 4-6-word
  lines into one natural sentence (b6 4.34 -> 4.43, c0 4.36 -> 4.48).
- Score: TARANTELLA (6/8, mandolin tremolo = re-struck 16ths on steel guitar, accordion off-beats, tambourine + castanets) with a tiptoe BASSOON theme for the sneaky character and the
  accordion 'breathing' (bellows swells) under the lungs (ep 29 music.py). Foley (ep 29 mix.py): stink_puff, crush, floss, exhale.

### Ep 31 (10 Nov, thirteenth ink episode, FIRST with no music bed): SOUND DESIGN WITHOUT A SCORE, the TV ROOM + THE CAPSULE, kin_word 'parch' (`engine/template/sfx_lib.py`, `anim_props_lib31.py`, `anim_fx.py`)
- No score any more (owner 9 Nov), so the foley carries the mix. sfx_lib now has `layered_hit(t, level, sub_f, body, tail, bright)` = SUB (falling sine) + BODY (loudest, high-passed)
  + TRANSIENT (-8 dB click) + TAIL (-14 dB decay), transients on the same sample; use it on the 4-5 BIGGEST moments only. `room_tone(kind, n)` ('tv' / 'cap' / 'kit' / 'sea' / board)
  under every shot per place (levels in the comment, ducked -6 dB under the voice, 20 ms crossfades at cuts), and a DROP-OUT (room tone + foley -15 dB for 0.25 s) right before each
  big hit so it lands out of silence. Copy the PLACE map / LVL / BIG / dip block from `episodes/31-salty-snacks-thirst/mix.py`. Other new foley: bell (alarm), shaker_rattle, tumble,
  drain, magnet_zing, deflate, waves, hatch_hiss. music.py in a no-score episode just writes a silent music.wav. Keep VO/bed >= 14 dB (a growl + drain hit 13 on d5: lowered).
- `kin_word(..., mode="parch", t1=)` = the word dries out (sags, ONE thin pale crack on every other letter, crumbs fall): thirsty / dry. More cracks were unreadable in the test frames.
- Places: `set_tvroom(t, flick)` + `sofa_front(f, 1360)` (movie night: cool flickering TV key light from the camera side + a warm lamp; `sofa_el()` at (x, 1340) + `chub(..., sit=True)`
  at y 1470 behind it) and `set_capsule(t, dim)` + `capsule_front(f, 1330)` (a mock spaceship module: white panels, a porthole with a painted Mars, a locker calendar, status lamps).
- lib31 ink props: chip_el(seed, bite), chips_bowl_el(level), salt_el(mood) (salt crystal buddy, accent on its shadow face), shaker_el, cell_buddy_el(mood, look, k) (k = water lost:
  shrinks + wrinkles), checker_el(mood, look, needle, ring) (a brain-pink inspector with a dial belly + an alarm bell: any 'sensor in your body'), courier_el (a hormone messenger),
  urea_el, magnet_el, wdrop_el (water drop buddy), tray_el(salty). Other people in jumpsuits = `chub(shirt=(214, 218, 226))` + dress().
- Voice: EXS 0.6 vs 0.75 on identical text = neutral (chunk20 4.491 vs 4.490, line mean 4.456 vs 4.449) but f0 range 16.3 -> 15.5 st (gate 15): voice.env stays 0.75; comp
  across the two takes instead. 'Yeah' at a line start reads as 'Yay' to ASR (and probably to people): write 'Less!' / a full sentence instead. T(line, 'it'/'the'/'and'/'your')
  matches the FIRST hit: 5 shots needed nth=1 here (a 0.2 s shot showed up in the frame list).

### Ep 33 (11 Nov, fourteenth ink episode): THE LIST REEL as a SPORTS METAPHOR, THE STADIUM, list intonation, FOLEY IN THE ROOM (`anim_props_lib33.py`, `make_vo.py`, `sfx_lib.py`)
- List topics ('foods with more X than Y'): give the whole list ONE physical metaphor where the number is a distance you can see (ep 33: a HIGH JUMP, bar height = mg per
  100 g, the familiar food sets the bar), then a screenshot LEADERBOARD recap (`board_row`, rows tick in on each spoken item). Say 'per 100 g' once on screen + in the voice,
  and add the honest catch inside the list (per 100 g vs per bite). Data: the owner's Hindi list reel = 4259 reach / 164 shares / 140 saves.
- Place: `set_stadium(t, dim, wave)` (athletics ground: stands with a dotted crowd that does a Mexican wave from t=wave, floodlights, infield, red track; dim 0..1 for a
  lights-down beat). `hj_rig(f, ..., bar=mg, px=)` = uprights with a mg scale (px per mg: 7 for numbers < 100, 3.6 up to 250) + bar + landing mat; ep 33 `jump_shot()`
  draws the athlete in front of the bar while rising and behind it while falling. lib33 props: food_el(orange|lemon|papaya|capsicum|guava|chilli, mood, look, cut, medal,
  crown) (papaya always cut: whole, it reads as a guava), athlete(...) + legs(...) (food with ink legs), jump_xy (anticipation + arc + landing squash), crown_el, whistle_el,
  clip_el, vitc_el(mood, look, k) (a vitamin C buddy that cracks/fades with k), scale_ink_el(text), bag_el(kind), el_pil (element -> PIL), board_row. Ep 33 `ref()` = Chubby as
  a referee (striped shirt over chub(shirt=), whistle, clipboard).
- Voice: `"word:up"` in the stressed list = CONTINUATION RISE (UPST 4.5 st over the last 55 % of the word; UPOFF=1 to A/B) for non-final list items; write the list with
  commas, not full stops (Kokoro falls on every full stop). Hyphenated numbers are one word: 'twenty-eight.:up'. A/B neutral-to-up on UTMOS.
- Sound: `place(x, t, xpos, gain, far, where)` + `reverb_returns()` (sfx_lib) = pan each dry effect to its on-screen x and send it to its place's room; set PLACE per shot
  and `place_at(t)` in mix.py (copy from episodes/33-vitamin-c-league/mix.py). New foley: whistle_blow, crowd(cheer), drumroll, boing_up, mat_land, bar_rattle, sneeze, boil.

### Ep 34 (12 Nov, fifteenth ink episode, FIRST under the 11 Nov 35-50 s rule): THE LOOP ENDING, THE CHAAT STALL, the RUNNY-NOSE kit (`anim_props_lib34.py`, `engine/template/sfx_lib.py`)
- 47 s total = 121 words / 11 lines / 17 shots (~2.8 s each). Payoff ('your nose thinks it's on fire') at 40 %, 'false alarm' at 56 %. A 45-s script still needs: hook question, one
  'it's not X' flip, define the one term on sight, ONE metaphor (here a fire alarm in the nose), one safe tip, the send line. Cut everything else (age, treatments, history).
- LOOP ENDING (craft skill): the last VO line names the frame-0 place ('...at every chaat stall'), then a 0.7 s logo beat, then a ~1 s TAIL shot that rebuilds frame 0's
  composition with no caption; `loop_seam(f, first, t, END, 0.33)` (lib34) crossfades the last 0.33 s into frame 0 (compose() caches rs('S0', 0)); in mix.py no SFX crosses the
  last 0.8 s and the room tone of the tail is the SAME noise as the opening (crossfaded), so the replay has no visual or audio jump. Copy the end of ep 34 anim_shots/mix.
- Place: `set_chaat(t, blur, top_y, dim)` + `cart_front(f, CART)` (pani-puri cart at dusk: striped awning across the top 250-360 px, swaying bulb string, blurred shopfronts as
  bokeh; Chubby at (540, 1520) s 1.38 behind a cart top at 1360 reads well; s 1.1 behind a 1300 cart hid his whole body in the first test).
- Chubby runny-nose kit: `nose_xy(x, y, s, t, lean, squash)` = where his nose tip is; `drip(f, nx, ny, s, t, t0, period, amt)` = a mucus drip with anticipation (swell),
  snap (lets go), gravity fall and a springy stub (follow-through); `flush(f, x, y, s, k, t)` = red cheeks + heat wiggles; `heat_lines`. Pale mucus vanished on skin: MUC is now a
  clear green with a dark green outline. lib34 props: golgappa_el(bite, pani, mood), puri_stack_el, matka_el, tissue_box_el, tissue_el(crumpled), caps_el(mood, look, k) (capsaicin =
  a red flame buddy), bell_el(lit) (fire-alarm bell), tap_el(open_k), helmet_el + ext_el (fireman Chubby), flower_ink_el (pollen = allergy icon), bowl_soup_el.
- Board: a side-profile head with the nasal passage + a nerve to a 'heat sensor' bell (ep 34 anim_shots board_head) = reusable for any 'nerve in your nose / mouth' topic.
- Sound: sfx_lib room 'street' (ir + room_tone), foley sniffle, tissue_pull, flame_whoosh, faucet.
- Voice: SPD 0.9 'Shorts pace' A/B on identical text LOST (chunk20 4.485 -> 4.464, f0 15.4 -> 15.1): keep SPD 0.88 even for short videos. The hook rewrite 'Do you know why your
  nose runs when you eat spicy food?' (verb early, food last) 4.40 -> 4.42 and b1 joined into one breath 4.42 -> 4.45.

### Ep 35 (13 Nov, sixteenth ink episode): THE BOXING RING, boxer buddies, SECONDARY ACTION, the foreground commentator (`anim_props_lib35.py`, `anim_fx.py`, `engine/template/sfx_lib.py`)
- 46 s, 8 lines / 123 words / 16 shots. A 'more X than Y' LIST idea cut to ONE item + a twist (on paper vs in your body); payoff at 50 %. Nutrient numbers: also check ABSORPTION and PER SERVING before any 'x times more' line.
- Place: `set_ring(t, blur, dim, flash)` + `ring_front(f, t, hits)` (spotlit arena, dotted crowd + camera flashes, back ropes/posts, front ropes that wobble after each hit time in `hits`); RING_FLOOR 1300. Boxers at feet y 1590, s 1.2. Any 'X vs Y' topic = a fight.
- Composition fix found in the test frames: an announcer standing BETWEEN two boxers gets punched through. Put Chubby in the FOREGROUND outside the ropes (ep 35 `announcer`: (170, 1930) s 1.42, mic + `bowtie()`), drawn after ring_front = depth + he never blocks the action.
- lib35 props: `boxer(f, x, y, s, t, kind="seed"|"milk", mood, look, punch, cuff, ko, struggle, slosh, raise_)` (ink limbs + gloves around a body element), seed_el(mood, look, hulled), milkglass_el(mood, look, level, slosh), glove_el, cuff_el (handcuffs), ca_el(cuffed, free) (calcium pebble), mic_el, til_bowl_el(label), spoon_til_el, laddoo_el, belt_el, `_seed_pts` (teardrop outline for the board). lib35 sets ACC to sesame gold: your anim_props6 overrides it.
- SECONDARY ACTION (anim_fx): `sec_bounce(t, bpm, amp)` -> (dy, squash), `sec_tap(t, period)` -> 0..1 double-tap pulse, `sec_wobble(t, hits, amp)` = damped wobble after the latest hit. ONE per shot, subordinate, off in fast beats.
- Sound: room_tone('arena') (crowd murmur; reverb 'stadium'); boxing bell = two clang(1250) at frame 0; KO = layered_hit + crowd(cheer); cuffs = lock_click + rattle (struggle) 8-10 dB under the hit.
- Voice: a '...' beat before the BIG NUMBER ('over... eight times') was neutral-positive (i2 4.48 -> 4.49); keep the hook question itself in one breath.

### Ep 36 (14 Nov, seventeenth ink episode): INVOLUNTARY ACTION (the hiccup), THE HOUSE PARTY, board breathing + balloon stomach + cord doors (`anim_props_lib36.py`, `engine/template/sfx_lib.py`)
- 49 s, 9 lines / 127 words / 18 shots (~2.7 s each). Flip at 3.8 s ('it's not the bubbles... it's your stomach'), the answer at ~42 %, the 'hic' explained at 61 %.
- INVOLUNTARY ACTION (craft skill): `hic(t, times, amp, seed)` -> dict(dy, squash, lean, arm, hair, expr, brow, mouth, k) for chub(): a reflex has NO anticipation (unlike `take`):
  2-frame jolt up, a 2-4 frame still hold, a 9-frame settle that sinks a little below rest, hair lags 3 frames, every repeat varies (amp, hold, head direction).
  `hic_word(f, t, times, x, y)` = a 'hic!' that pops out on each. Use the same 2-frame snap with no wind-up for any reflex (the dome jerking, doors slamming, a flinch from heat).
  Audio: `hic_sfx(level, pitch)` (no lead-in; vary pitch per hic). Watch out for ACCIDENTAL anticipation (nothing may move before the hit).
- Place: `set_party(t, blur, top_y, dim, balloons)` + `party_front(f, top_y)` (warm evening living room, bunting at y 170-230 ABOVE the hook words, ink balloons that bob,
  fairy lights, a striped aqua table). Chubby at (380, 1660) s 1.3 behind a table top at 1420 = big enough; table props at y ~1300-1390. Light wall -> use DARK text (INKC / ACC_S / red).
- Drinking: ep 36 `drinker()` (anim_shots) = glass at the mouth with ra=(150, -128), hold_off=(-38, -18), glass rotated +32 (top toward the mouth); sip 0 = at the chest.
- lib36 props: fizzy_glass_el(level) (generic, no brand), soda_bottle_el, balloon36_el + balloon_bob (secondary action), board torso `board_torso(... lung_k, drop, bulge, st_r, nerve_k)`
  with `dome_pts(drop, bulge)` (the diaphragm breathes: drop 0..1), a stomach that inflates like a balloon under it, the nerve with alarm pulses; `cord_doors(f, t, cx, cy, shut)` (vocal cords
  as two swing doors); `ultrasound(f, t, cx, cy, k, hics)` (a dark fan with a curled baby that jolts). Ep 36 `x_belly()` = an x-ray window on Chubby's belly drawn in the BOARD language
  (paper + blue/red ink): the dark-navy version read as a plate in the test frames.
- Sound: room tone + reverb 'party' (chatter, far clinks; a living room), `fizz_pour`.
- Voice: PZ 1.2 neutral-positive on one script (line mean +0.015); re-test before changing voice.env. One interjection ('Hic!') per video at most.

### Chubby v3 (28 Oct, `template/fnh_char_v3.py` — built first, superseded the same day by Chubby INK above)
Pixar-style kid: big lidded hazel eyes with two catchlights, thick shaped eyebrows, button nose, blush + freckles, a mouth with teeth
and tongue, a messy hair mop; neck + shoulders; cream chef's APRON over the mint hoodie (signature), rolled sleeves, HANDS with
fingers that point along the forearm, jeans with turn-ups, sneakers. Same `chub(...)` API as below, plus `t=` for idle life
(breathing + automatic blinks) — pass `t=t` in every shot. `lean` now also tilts the head. Expressions: n, happy (smile-eyes),
wow, sus, sad, smirk (one brow up), sleepy; `mouth=3` with expr="happy" = a laugh with closed eyes. Review sheet:
/home/claude/outputs/chubby_v3_sheet.jpg (regenerate with the sheet script in improvements.md G). Make him ACT: a different
pose, look and expression per shot, hands doing something, and a reaction shot on every reveal.

### Chubby API (`fnh_char.py` + `fnh_char3d.py` — same API, v2 look loaded after v1; v3 overrides both)
`chub(f, x, y, s, la, ra, ll, rl, mouth, blink, brow, look, expr, tint, hold, hold_off, hold_front, bob, op, lean, squash, sit, nose, cap)`
- (x, y) = feet baseline; height ≈ 480·s; head centre ≈ (x, y − 420·s). Typical: s 0.8–1.15 at y 1440–1480.
- arms (upper°, fore°) from straight down, + = outward: relaxed (20, 10); cheer (150, 170); point (70, 40);
  scratch head (−150, −150); hand to mouth (148, −130) + `hold=carrot_side(...)`, `hold_front=True`; hold up (150, 175).
- `expr`: n, wow, sus, smirk, sad, happy; `mouth`: 0, 1, 2, 3, "o" (`talk(t)` lip-syncs to the VO, `munch(t)` chews);
  `brow`: n, up, sus, sad; `look=(−1..1, −1..1)`.
- `tint` 0..1 turns skin orange (only when the story is a colour change); `nose=0..1` shows/tints a nose; `cap=True` pilot cap.
- `chub_head_only(f, x, y, s, t, ...)` for big face close-ups; `logo_el()` = FreshNestHub logo with Chubby's head.
- v2: `grip_hand(f, x, y, s)` draws a shaded hand OVER a held tool's handle (chopper uses it); shoulders at
  (x ± 118·s, y − 261·s) so `arm_ik` helpers still fit; `shirt=` recolours the hoodie (white = lab coat look).
Chubby appears in most shots, reacting to the fact (eating, shocked, pointing, cheering). Give him a different action
in every video.

### Reusable props (already loaded)
anim_props: tag_el, bubble_el, magnifier_el, glow, steam, coin_el, phone_el · anim_props2: calendar_el(top, big),
sign_el, phone2_el(msg1, msg2, pressed), check_el(r, ok), cash_el · anim_props3: stamp_el, vault_door_el, app_phone_el ·
anim_props4: burst_el, readout_el, dial(f, x, y, s, "mph"|"g", v, txt), stopwatch_el, splash, eye_el, molar_el,
forceps_el, weight_el, bscale_el, seat_el, wheel_el, belt_draw, bars2 (comparison bars), speed_lines, add_patch ·
anim_props5: carrot_el, carrot_side, dots (pigment/particles), machine_el, capsule_el, gauge_tube, vessel (blood flow),
skin_block (skin layers), palm_el, sole_el, eye2_el(sclera, skin), baby, bowl_el, spoon_el, plane_el, prop_disc,
radar_screen, moon, zzz_moon, mirror_el. · anim_props_lib09 (ep 09): chili_el(face, mood), chili_side, caps_el/caps (capsaicin key
molecule), tongue_el, alarm_el/alarm(ring, key_in) (receptor = heat alarm), brain_el(face, mood, alarm_lit), teacup_el,
medal_el, drink_el(kind), protein_el, bird_el, mouse_el, seeds, plant, padlock_el, key_el, fire_cone, flames_row, thermo, sweat. · anim_props_lib10 (ep 10): candy_el(col), lollipop_el, bucket_el (pumpkin pail), sugar_el(mood) (glucose cube),
packet_el, cup2_el(label), pancreas_el(awake), stomach_el, ikey_el (insulin key), cell_el(open_k, sugar_in) (cell with a door),
sugar_gauge (dial with tight-range band), thermostat_el, rating_board, party_hat_el, witch_hat_el, balloon_el, ghost_el, clock_el,
tooth, test_card_el, head_pos(x,y,s), blindfold, mom(...) (Chubby-style mom: hair + bun), scientist(...) (lab coat + goggles);
extra stage schemes "night" and "lime". · anim_props_lib11 (ep 11): mint_leaf_el(face, mood), gum_el, menthol_el/menthol (key molecule),
calarm_el/calarm(ring, key_in, jumpy) (COLD alarm), ice_block, ice_cube_el, frost(amt), snow, breath, icicles, ice_glass_el,
thermo_c (°C ticks + alarm trigger line), airmeter, ice_floor, nerve_icon_el, think_el (thought bubble); schemes "ice",
"deepice", "mintg". sfx_lib (ep 11): ice_crack, sip, chatter, wind. · anim_props_lib12 (ep 12): kaju_el(silver, face, mood, fake) (kaju katli
with crinkly silver leaf), barfi_el, plate_el/plate_of_sweets, diya_el/diya (oil lamp + flame), leaf_el (silver leaf sheet,
fake=dull), lump_el, hammer_el + hammer_swing (arc swing), packet (beating stack, gut=True variant), detector (metal
detector), kscale_el (kitchen scale readout), paper_el, elem_el (periodic tile: Ag/Al/Pb/Ni), rule_doc_el, colour_bottle_el,
cow_el, hair_cross; schemes "festive", "saffron", "steel". sfx_lib (ep 12): clang, rustle, det_beep.
anim_props_lib13 (ep 13): onion_el(face, mood, look, red), onion_half_el (cut rings), knife_el(dull) + knife_at + knife_tip,
board_el, tiles (kitchen wall), onion_cell (two rooms, breakable walls), cell_grid (microscope cells), sulfur_el, enz_el(kind 1|2,
open_, mood) + chomp(t) (enzyme pac-men), acid (live wobbly blob), gas_el/gas (gas ghost), wisps, drop_el, tears, tear_streams,
droplets (spray with gravity + slow-motion), nerve_endings, bug_el, germ_el, helix (DNA with a gene, off), switch_el, pan_el,
slowmo_ui (high-speed camera frame), mix_icon_el, acid_icon_el, sting_eye_el, chop_pose/chopper, board_onion, zz, shield_el,
gland, ring_el; schemes "kitchen", "onion", "gas", "tear". sfx_lib (ep 13): chop, hiss, snip, plip, sizzle, squirt.
anim_props_lib14 (ep 14): mug_el(col, level), battery_el(level, txt) + sticker_el (peeling fake charge), skey_el(mood) (adenosine =
sleepy key), ckey_el(mood) (caffeine = fake key, bean head), lock_el(lit) (receptor), brain_cell(f, cx, cy, w, t, locks=[(dx, key,
rot, lit)], dim, hgt) (cell with locks on top; returns keyhole points), key_pile, mask_el (smile mask on a stick), bed_el + nightcap,
bee_el(flap, mood), flower_el("coffee"|"lemon", glow), lemon_el, sun_icon, moon_icon, zzs, caf_dot; schemes "cafe", "latte", "neuro",
"dusk", "honey". sfx_lib (ep 14): gulp, rip, rattle, buzz, tick, charge.

### Cinematic kit (`anim_cine.py`, loaded after anim_fx — 27 Oct)
- `finish(f, n, look="warm"|"golden"|"cool"|"night"|"fresh")` = colour grade (cool shadows, warm highlights, S-curve) +
  adaptive bloom + vignette + grain. Every shot already calls finish(); pick the look that matches the shot's emotion.
- Places: `set_kitchen(t)` (+ `counter_front(f, 1330)` AFTER Chubby -> he stands behind the worktop; props go on top at
  y ≈ 1340), `set_room(t)` (bookshelf, wooden floor, rug), `set_dusk(t)` (golden-hour sun at (720, 980), hills, grass).
  Backgrounds are pre-blurred = depth of field; `dof(f, sigma)` blurs more for close-ups.
- Light: `god_rays(f, x, y, t, ...)`, `lamp_glow`, `haze`, `bokeh`, `dust_motes`, `light_leak`, `cast_shadow(f, x, y, w, h, skew)`,
  `mood(f, col, amt)` (colour the edges: red = danger, green = gas, blue = cold), `spotlight(f, x, y, r, amt, feather)` (anim_fx),
  `light_wrap(f, el, x, y, col)` (rim light from the scene on a hero prop).
- `title3d(f, "WORD", y, t, t0, size, face, side)` = giant extruded 3D word, drawn BEFORE Chubby/the hero so they overlap it;
  when a 3D title shows the key word, drop the ui_word caption for that moment (no duplicate text).

### Materials + new places (ep 15, `anim_cine.py` + `anim_props_lib15.py`)
- `mat_shade(mask, base, shadow, hi, kind)` / `mat_put(cv, m, ...)` (kind = gloss | satin | matte | chalky) shade a prop on Chubby's
  light model: gloss = sharp highlight + crisp window reflection, matte = soft and flat, chalky = lifted + powdery. Use it for every
  new HERO prop (build it on a `_Cv` canvas from fnh_char3d) and let the material carry meaning (fresh vs old, real vs fake).
- Places: `set_chocolatier(t)` + `marble_front(f, 1330)` (shop workroom, marble slab), `set_fridge_night(t)` (dark kitchen lit only
  by an open fridge = cold blue key light). lib15 props: choc_bar_el(kind, snap, bite), choc_piece_el, melting_piece, puddle,
  wrapped_bar_el, pod_el(open_), bean_el, butter_el, brick_el/brick_layout/lerp_layout/draw_bricks/form_stack (same bricks built
  N ways = crystal forms / structure), temp_gauge (marks), temper_chart, pot_el, pool, cake_el, jar_el (glass), mould_el, spatula_el,
  sugar_xtal; schemes cocoa, butter, crystal, chalk, frost. sfx_lib (ep 15): snap, melt, clack, fridge_hum, suction.

### Inside-the-body world + routes (ep 16, `anim_cine.py` + `anim_fx.py` + `anim_props_lib16.py`)
- `set_gut(t, squeeze=None|0..1, bend, pal)` = looking down a living intestine lit from deep inside (backlit glowing fold rims, wet
  highlights, depth fog + blur, particles); `squeeze` = depth of a travelling peristalsis ring (animate 0.9 -> 0.05 = it rushes at camera).
  Darker top band leaves room for white captions. Use it for ANY inside-the-gut / blood-vessel / airway moment (recolour with `pal`).
- `peri_tube(f, x0, x1, y, r0, xs, t, sq, cargo=el)` = side view of a gut segment: squeeze behind (red muscle) + relax in front, pushes
  `cargo`; `route_map(f, stops, k, t, token=el, times=[...])` = metro map of a journey (visited stops filled, current ringed, hour chips);
  `body_route_pts()` + `ROUTE_NAMES` (lib16) = mouth -> food pipe -> stomach -> small intestine -> large intestine -> out inside an x-ray
  Chubby (`chub(..., op=0.28)` on the "xray" scheme). lib16 props: gum_wad_el, bubble_el, splat, toothpaste_el + paste_ribbon, corn_el,
  seed_el, tar_el, stomach3_el (3D-shaded, cut-away), broom_el, bin_el(open_), birch(), pedestal() + glass_case() (museum set for open
  loops), stone_woman(); schemes flesh, gumpink, xray. sfx_lib (ep 16): bubble_pop, squelch, stretch, growl, spit.

### Visual rules (mandatory)
- 1080×1920, 24 fps. Safe zones: nothing important in top 250 px, bottom 420 px (y > 1500), right 120 px, left 60 px.
- Captions ONLY at key moments: `ui_word(f, lead, BIG, 470, …)` — small lead + one big word/number, centred x = 540,
  ≤ 840 px wide; use `[word]` for an accent colour. No word-by-word subtitles, no emoji, no persistent counters.
- First 3 s: strong visual action (Chubby doing something) + one short caption; never a giant text-only opener.
- Story moments (Chubby doing something, everyday situations, reveals) happen in a lit PLACE (set_kitchen / set_room /
  set_dusk or a new place you build with the same recipe: blurred background + sharp foreground + one light source);
  diagram / inside-the-body / molecule shots keep the colour-circle `stage()`. Change the look every shot (place, light,
  grade, mood colour) — lights-drop + red rim for danger, golden backlight for the happy reveal, shallow focus for close-ups.
- Every video: at least 3 shots in a lit place, at least 2 big 3D titles behind the hero, and one lighting beat that
  carries the emotion (lights drop / spotlight / mood colour). Captions on dark/warm places: white with shadow.
- Build ONE new place, light or material per run when the topic needs it (bathroom, supermarket, gym, street, lab...) and
  add it to anim_cine.py for every future video.
- Source chip for key numbers: `chip("Source: …", INK, WHITE, 22)` at y 1462.
- End: phone "SEND THIS" CTA with Chubby, then logo sting + "follow for more health facts".
- New opening idea every video (check the topics_done "opening" column).

### Test before the full render (mandatory)
`python3 -I scripts/anim.py x <2 frames per shot>` → frames/r_NNNN.jpg; tile them with safe-zone guides:
`python3 $ENG/engine/tools/sheet.py /tmp/sheet.jpg frames/r_*.jpg` and LOOK (Read the image). Fix overlaps, clipped
props, text in unsafe zones, props hidden behind Chubby's head (use hold_front), unreadable diagrams. Re-test.
Then: `SKIP_VO=1 bash $ENG/build_ep.sh NN-slug` (≈7 min) → /home/claude/outputs/NN-slug.mp4 + _sheet.jpg.
QA: 1080×1920, 45 s–2:55, ≈ −11 LUFS, peak ≤ −1 dBFS; look at the sheet; facts on screen = sources.

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
