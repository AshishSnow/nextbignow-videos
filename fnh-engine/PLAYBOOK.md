# FreshNestHub autonomous reel engine — PLAYBOOK v4 "CHUBBY" (approved by owner 26 Oct 2026)

Runs every 5 hours. Every run makes ONE new vertical animated reel (45 s–3 min — as long as full understanding needs) for **FreshNestHub** — fun, surprising
**food + health facts** — and posts it to **Instagram @fnhtruths** and **YouTube Shorts (@FreshnestHub)** via Metricool.
The owner (Ashish) is usually not watching: decide, build, verify, post, log. Never ask questions mid-run.

**CURRENT character + look = Chubby INK (28 Oct, owner-approved; first full episode = 17, 31 Oct). Reference episodes for the ink look:
`episodes/17-sugar-rot-teeth/` (props, places, acting, script registers) and `episodes/18-milk-boils-over/` (stove place, hand poses, follow-through, cut-away pot). Older notes below describe v4/v5; follow them only where they don't conflict.**

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
