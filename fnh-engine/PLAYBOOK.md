# FreshNestHub autonomous reel engine — PLAYBOOK

Every run makes ONE new 30–45 s vertical reel for **FreshNestHub** (skin, hair, beauty, body and home-hygiene
curiosities for a worldwide English audience), hosted by **Nessa** (stick-figure host, female voice ~30),
and posts it to **Instagram @fnhtruths** and **YouTube Shorts (@FreshnestHub)** through Metricool.
The owner (Ashish) is usually not watching: decide, build, verify, post, log. Never ask questions mid-run.

Benchmark: `episodes/01-face-mites/` (posted 25 Oct 2026) — study its `render.py` before building anything.

---------------------------------------------------------------------------------------------------
## 0. Setup (≈5 min)
```
# repo is attached with add_repo(owner="AshishSnow", repo="nextbignow-videos", access="push")
git clone --depth 1 https://github.com/AshishSnow/nextbignow-videos /home/claude/nextbignow-videos
bash /home/claude/nextbignow-videos/fnh-engine/setup.sh          # installs kit to /home/claude/reel-kit
```
ENG=/home/claude/nextbignow-videos/fnh-engine

## 1. Claim a topic (avoid repeats and parallel-run collisions)
1. `git pull` then read `topics_done.md` (all past topics + openings used) and `topic_ideas.md`.
2. Pick a topic NOT in topics_done (no near-duplicates either). Prefer `topic_ideas.md`, or find a better one
   (WebSearch: recent science news on skin/hair/body/beauty, weird beauty-industry facts, myths).
3. Topic test — all must be true:
   - Instantly clear in 3 s, gross/surprising/"wait, what?", relevant to the viewer's own body/home/beauty routine.
   - Can be SHOWN with real-looking animation (inside the body, macro skin, cross-sections, products, objects).
   - Backed by ≥ 2 reputable sources (university, peer-reviewed journal, NIH/NHS/CDC/FDA/WHO/AAD, major newsroom).
4. Immediately append a line `CLAIMED <date-time IST> | NN-slug | working title` to `topics_done.md`, commit and
   push (fetch + rebase first). NN = next number.

## 2. Research (≈10 min)
- WebSearch/WebFetch the primary sources. Write down every fact you will say, with its source URL.
- Numbers must match the source. If a claim is contested, say "scientists think…" or drop it.
- NO dosing, treatment or diagnosis advice. Only safe general tips (e.g. "remove makeup before bed",
  "see a dermatologist if…"). No real private people. Celebrities only for documented public facts. No brand names/logos.

## 3. Script (MrBeast energy, Zack D. Films clarity) — 90–115 words, 30–45 s
Structure (each line becomes one shot):
1. **INTRO QUESTION (0–2.5 s, mandatory, owner's rule):** Nessa asks a "Do you know…?" question that names the
   topic so the viewer instantly knows what the video is about, e.g. "Do you know what happens to your skin
   when you pop a pimple?" / "Do you know your lipstick might be made of bugs?". On screen at the same time:
   the topic visual + a two-tier title (small "do you know" line + 1–3 big words). Visual first, text supports it.
2. Shock fact / reveal (punch + shake).
3. 4–6 escalating facts, each with its own visual; one "but wait" twist.
4. One practical, safe takeaway (tip card with a check that ticks).
5. **Loop ending:** last line flows back into the opening question (no "follow us" line in the VO).
- Simple words, numbers written as words in voice text, short sentences, contrast of HIGH (excited) and LOW
  (whisper) lines. Max ~4 caption moments per video (key moments only).

## 4. Build the episode
```
cp -r $ENG/episodes/01-face-mites $ENG/episodes/NN-slug
```
Rewrite inside `episodes/NN-slug/`:
- `lines.py` — LINES = [(id, text)] exactly as spoken (used for alignment; keep caps/ellipses fine).
- `voice.py` — only the PLAN list (+ moods if needed). Moods: hook, excited, curious, whisper, cheeky, serious, warm.
  Keep the MOOD table (it gives the loud-highs / soft-lows the owner asked for). Output must stay `work/take.wav`.
- `timeline.py` — events via F(line_id, word) and the shot list ORDER/TRANS (whip, pop, zoomblur, dip, punch,
  flash, flashp). One shot per line or per beat; 1.5–4 s each.
- `render.py` — keep everything above `# ================= shots` (helpers) and the compose/camera/main
  section; replace the `shot_*` functions, PUNCH/SHAKE lists and any scene builders that don't fit.
- `music.py` / `mix.py` — keep helpers, rewrite the cue sections for the new events (SFX on every moment,
  hard stops before reveals, music box / soft pad under whispers). Keep `BED` and the line-gain `LG` dict
  (update ids). Target VO/bed ≥ 12 dB on every line (printed by mix.py).

### Visual rules (owner's preferences — all mandatory)
- 1080×1920, 30 fps. **All text centred on x = 540 (true centre, `CX`), width ≤ 840 px (`MAXW`, auto-fit in
  `tier()`).** Nothing important in top 250 px, bottom 420 px, right 120 px, left 60 px. Key visuals central.
- Vibrant, saturated MrBeast-style colour, never washed out or dull; beautiful designed backgrounds in every shot.
- Approved look: bright designed sets with a big colour circle, real-looking objects/creatures, big words tucked
  behind objects, editorial two-tier type (small lowercase line + huge Anton word).
- Real-looking visuals: procedural skin macro (`gen_skin`), shaded 3D sphere-stamp creatures/tubes
  (`draw_mite`, `sphere`, `stamp`), cross-section blocks (see `follicle_block`), lens zooms, cards with subtle 3D.
- Nessa (`nessa.py`): poses stand, wave, point, pointup, shock, cheer, think, whisper, shrug, hips, magnify,
  mirror, cover, cradle, wipe, stretch; expressions smile, talk, wow, shock, whisper, mischief, laugh, worried,
  gross, think, sleep, sleepsmile, nervous; styles nessa, mom, guy, guy2, bald, girl, girl2; `head()` for close-ups.
  Mouth follows the voice via `mouth(t)`. She appears in most shots (reacting), never covering the key visual.
- No emoji, no persistent counters/meters, captions only on key moments, screen shake on impacts,
  scene-matched colour, a sound effect for each moment.
- **New opening every time** — check the "opening" column in topics_done.md and never reuse one.

### Test before the full render (mandatory)
```
cp $ENG/episodes/NN-slug/lines.py /home/claude/reel-kit/english/scripts/vo_lines.py
cd /tmp && python3 -I $ENG/episodes/NN-slug/voice.py
python3 -I /home/claude/reel-kit/english/scripts/align_en.py /home/claude/reel-kit/english/work/take.wav 1.0
python3 -I $ENG/episodes/NN-slug/timeline.py
GUIDES=1 python3 -I $ENG/episodes/NN-slug/render.py /tmp/x.mp4 0,45,90,...   # 2-3 frames per shot
```
Frames land in `/home/claude/reel-kit/english/frames/r_NNNN.jpg`. Look at every one (Read the images or a tiled
sheet): text centred and inside the guides, no overlaps, nothing clipped, no empty frames, colours vivid.
Fix and re-test until clean. Then:
```
bash $ENG/build_ep.sh NN-slug        # voice -> align -> timeline -> music -> mix -> 2x parallel render -> mux
```
Verify the printout: 1080×1920, 30–46 s, I ≈ −14 LUFS, peak ≤ −1.4 dBTP, and look at
`/home/claude/outputs/NN-slug_sheet.jpg`. Render takes ~10–20 min.

## 5. Host + post
```
bash $ENG/host_video.sh NN-slug push        # prints RAW_URL=https://raw.githubusercontent.com/...
```
Metricool brand **Freshnesthub**: `blogId = 7643474`, timezone `Asia/Calcutta`.
Schedule 10 minutes from now (ISO, +05:30). Make TWO posts (each platform gets its own copy):

Instagram (`providers:[{"network":"instagram"}]`):
```
{"autoPublish":true,"descendants":[],"draft":false,"firstCommentText":"","hasNotReadNotes":false,
 "media":["<RAW_URL>"],"videoCoverMilliseconds":<ms of the intro title frame, ~1500-2700>,
 "mediaAltText":[],"providers":[{"network":"instagram"}],
 "publicationDate":{"dateTime":"YYYY-MM-DDTHH:MM:SS","timezone":"Asia/Calcutta"},
 "shortener":false,"smartLinkData":{"ids":[]},"text":"<IG caption>",
 "instagramData":{"type":"REEL","showReelOnFeed":true,"isAiGenerated":true}}
```
YouTube (`providers:[{"network":"youtube"}]`, no cover fields):
```
 ... "text":"<YT description>",
 "youtubeData":{"title":"<title>","type":"short","privacy":"public","tags":[...8-12 tags],
                "category":"EDUCATION","madeForKids":false,"isAiGeneratedContent":false}
```
AI disclosure: Instagram `isAiGenerated: true` (Nessa's voice is realistic AI audio — Meta requires the label).
YouTube `isAiGeneratedContent: false` because the video is fully animated (YouTube exempts clearly
unrealistic/animated content). If a video ever contains realistic AI footage of real-looking scenes, set it true.

### SEO copy rules (owner's rules)
- IG caption: line 1 = the exact search phrase (e.g. "Carmine (crushed bugs) is in red lipstick."), 2–3 short
  lines of facts, a share/comment question, `Sources: ...`, then **exactly ≤ 5 hashtags**:
  1 exact topic + 2 niche + 1 broad + `#freshnesthub`.
- YouTube title: keyword first, ≤ 60 chars. Description: first sentence contains the keyword, 2–3 lines,
  "Animated explainer. Narration voice is AI-generated.", Sources line, then 3 hashtags. Tags: 8–12 phrases.
- No emoji in copy.

After `createScheduledPost` returns, check each `media` URL now starts with `https://static.metricool.com/`
(Metricool copied the file). Then `bash $ENG/host_video.sh NN-slug delete`.

## 6. Log + commit (code only, never commit mp4 to main)
Replace your CLAIMED line in `topics_done.md` with:
`| date IST | NN-slug | title | opening used | IG plannerUrl | YT plannerUrl |`
Commit `episodes/NN-slug/` + `topics_done.md` (+ `runs_log.md`) to main (fetch + rebase, then push).

## 7. Failure policy
- Facts can't be verified → choose another topic. Build fails → fix and retry (max 2 full renders).
- If still failing, do NOT post anything half-done. Append the reason to `runs_log.md`, mark the CLAIMED line
  `FAILED`, commit, and end the run.
- Never delete or edit already-published posts. Never touch other Metricool brands (nextbignow, Oopsmybusiness).
