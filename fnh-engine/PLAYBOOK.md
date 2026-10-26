# FreshNestHub autonomous reel engine — PLAYBOOK (v3 "BODY FILES", 26 Oct 2026)

Runs every 5 hours. Every run makes ONE new 45–62 s vertical reel for **FreshNestHub — BODY FILES**: surprising,
genuinely interesting **health / human-body** explainers ("what really happens when…") for a worldwide English
audience, and posts it to **Instagram @fnhtruths** and **YouTube Shorts (@FreshnestHub)** through Metricool.
The owner (Ashish) is usually not watching: decide, build, verify, post, log. Never ask questions mid-run.

**Owner feedback 26 Oct (episodes 01–04 were rejected):** he did NOT like the vibrant stick-figure sets, the
Nessa character or the young voice, and found beauty-trivia topics boring. From episode 05 on:
- **Look = clean white-paper medical explainer** (`kit/english/scripts/plates.py`), **no mascot / no stick figure**.
- **Voice = mature British female narrator** (Kokoro `bf_emma`, `en-gb`), calm documentary pace — owner picked it.
- **Topics = health / body, interesting and useful** (see topic_ideas.md UP NEXT).

**Benchmark/template: `episodes/05-knuckle-crack/`** — study its `render.py`, `voice.py`, `music.py`, `mix.py`
before building anything. Copy it for every new episode. Ignore episodes 01–04 (old rejected style).

---------------------------------------------------------------------------------------------------
## 0. Setup (≈5 min)
```
# repo is attached with add_repo(owner="AshishSnow", repo="nextbignow-videos", access="push")
git clone --depth 1 https://github.com/AshishSnow/nextbignow-videos /home/claude/nextbignow-videos
bash /home/claude/nextbignow-videos/fnh-engine/setup.sh          # installs kit to /home/claude/reel-kit
```
ENG=/home/claude/nextbignow-videos/fnh-engine

## 1. Claim a topic (avoid repeats and parallel-run collisions)
1. `git pull` then read `topics_done.md` (past topics + openings) and `topic_ideas.md`.
2. Take the FIRST topic in the "UP NEXT" list that is not yet in topics_done. If it fails verification, take the next.
   When UP NEXT is empty, find new ones of the same kind (WebSearch recent health/body science, myths, case reports).
3. Topic test — all must be true:
   - About the viewer's own body/health, instantly clear, makes people say "wait, really?" and want to share it.
   - Can be SHOWN inside the body: X-ray / MRI plates, textbook cross-sections, step-by-step process diagrams.
   - Backed by ≥ 2 reputable sources (peer-reviewed journal, university, NIH/NHS/CDC/WHO/Mayo Clinic, major newsroom).
4. Immediately append `CLAIMED <date-time IST> | NN-slug | working title` to `topics_done.md`, commit and push
   (fetch + rebase first). NN = next number.

## 2. Research (≈10 min)
- WebSearch/WebFetch the primary sources. Write down every fact you will say, with its source URL.
- Numbers must match the source. Contested science → "one study found…" / "scientists think…", or drop it.
- NO dosing, treatment or diagnosis advice. Only safe general tips ("if it hurts or swells, talk to a doctor").
  Include one honest nuance/catch when the evidence has one (like the 1990 grip study in episode 05).
- No real private people; no brand names or logos.

## 3. Script — calm, clear, explained (45–62 s, 120–150 words, 12–15 lines)
1. **INTRO QUESTION (0–3 s, mandatory):** "Do you know what really happens when…?" naming the topic. On screen at
   the same moment: the topic visual (e.g. X-ray plate) + a two-row Anton headline with the key word in red.
2. Bust the common belief or state the surprise (stamp "MYTH" / reveal).
3. **Explain step by step** (5–7 lines), one diagram state per line: anatomy → what changes → the key moment.
4. The evidence: a named study/scan/experiment with a plate and a small source line.
5. One honest nuance + one safe tip card.
6. **Loop ending:** the last line returns to the opening question/visual (no "follow us" in the VO).
- Short sentences, everyday words, numbers as words in the voice text. Split a line into phrases only at real pauses.

## 4. Build the episode
```
cp -r $ENG/episodes/05-knuckle-crack $ENG/episodes/NN-slug
```
Rewrite inside `episodes/NN-slug/`:
- `lines.py` — LINES = [(id, text)] exactly as spoken.
- `voice.py` — only the PLAN list (moods: hook, calm, emph, soft, question, warm). Keep `bf_emma`, `en-gb` and the
  MOOD table. Pauses: 0.3 s inside a line, 0.55–0.75 s between lines.
- `timeline.py` — events via F(line_id, word); shot list ORDER/TRANS (slide, push, cut). 14–18 shots, 2.2–5.5 s each.
- `render.py` — keep the camera / transitions / compose / main sections; rewrite the shot functions. Build new
  diagrams in the same style (add reusable drawing functions to `kit/english/scripts/plates.py` and commit them):
  * page = `paper()` + `header(f)`; headline(...) for 1–2 key moments per shot max; `fig_label` for diagrams.
  * dark plates (`dark_plate_with`) for X-ray / MRI / scan imagery; light plates (`plate_light`) for colour diagrams.
  * `leader()` draw-on labels in mono caps, `stamp()` for MYTH/CRACK moments, `badge()` for verdicts,
    `tip_card()` for the tip, `arrow()`, `ring_pulse()`, icons (`clock_icon`, `hand_icon`, `gauge_icon`).
  * Colours: ink black, red (#E22428) for the key word, blue for process labels, green for good verdicts,
    textbook colours inside diagrams (ivory bone, blue cartilage, pink tissue, golden fluid).
- `music.py` / `mix.py` — calm documentary piano score with a tension build into the key moment, hard stop on the
  big question; SFX for every moment (pen scribble on labels, paper slide on transitions, stamp thud, ticks, dings).
  Keep the `LG` line-gain dict (update ids) and BED; target VO/bed ≥ 15 dB on every line (printed by mix.py).

### Visual rules (mandatory)
- 1080×1920, 30 fps, white page. **All text centred at x = 540 (`CX`), width ≤ 840 px (`fit`).**
- Safe zones: nothing important in top 250 px, bottom 420 px, right 120 px, left 60 px. Headlines start at y ≈ 372;
  plates sit between y ≈ 560 and 1450. Labels inside x 60–960.
- No mascot, no emoji, no persistent counters. Captions only at key moments (headline/stamp/badge/labels).
- A new opening composition every video (check topics_done "opening" column).

### Test before the full render (mandatory)
```
cp $ENG/episodes/NN-slug/lines.py /home/claude/reel-kit/english/scripts/vo_lines.py
cd /tmp && python3 -I $ENG/episodes/NN-slug/voice.py
python3 -I /home/claude/reel-kit/english/scripts/align_en.py /home/claude/reel-kit/english/work/take.wav 1.0
python3 -I $ENG/episodes/NN-slug/timeline.py
GUIDES=1 python3 -I $ENG/episodes/NN-slug/render.py /tmp/x.mp4 0,45,90,...   # 2 frames per shot + frame 0
```
Look at every frame (Read the images or a tiled sheet): text centred and inside the guides, nothing overlapping or
clipped, diagrams readable. Fix and re-test until clean. Then:
```
bash $ENG/build_ep.sh NN-slug
```
Verify: 1080×1920, 45–62 s, I ≈ −14 LUFS, peak ≤ −1.4 dBTP; look at `/home/claude/outputs/NN-slug_sheet.jpg`.

## 5. Host + post
```
bash $ENG/host_video.sh NN-slug push        # prints RAW_URL=https://raw.githubusercontent.com/...
```
Metricool brand **Freshnesthub**: `blogId = 7643474`, timezone `Asia/Calcutta`. Schedule 10 minutes from now.
TWO posts (each platform its own copy):

Instagram (`providers:[{"network":"instagram"}]`):
```
{"autoPublish":true,"descendants":[],"draft":false,"firstCommentText":"","hasNotReadNotes":false,
 "media":["<RAW_URL>"],"videoCoverMilliseconds":<ms of the intro frame, ~1200-2000>,
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
AI disclosure: Instagram `isAiGenerated: true` (AI narrator voice). YouTube `isAiGeneratedContent: false`
(clearly illustrated diagrams, not realistic footage).

### SEO copy rules
- IG caption: line 1 = the exact search phrase ("What really happens when you crack your knuckles"), 2–3 short
  lines of facts, a share/comment question, `Sources: ...`, then **≤ 5 hashtags** (1 exact, 2 niche, 1 broad,
  `#freshnesthub`).
- YouTube title: keyword first, ≤ 60 chars. Description: keyword sentence, 2–3 lines, "Illustrated explainer.
  Narration voice is AI-generated.", Sources line, 3 hashtags. Tags: 8–12 phrases. No emoji.
After `createScheduledPost`, check each `media` URL starts with `https://static.metricool.com/`; then
`bash $ENG/host_video.sh NN-slug delete` (if the proxy refuses, note it in runs_log.md).

## 6. Log + commit (code only, never mp4 to main)
Replace your CLAIMED line in `topics_done.md` with `| date IST | NN-slug | title | opening used | IG | YT |`,
append a line to `runs_log.md`, commit `episodes/NN-slug/` + logs (+ any new reusable plates.py functions),
fetch + rebase, push.

## 7. Failure policy
- Facts can't be verified → next topic. Build fails → fix and retry (max 2 full renders).
- Still failing → do NOT post. Log the reason in `runs_log.md`, mark the CLAIMED line `FAILED`, commit, end.
- Never edit/delete published posts. Never touch other Metricool brands or other repo folders (studio/, oopsmybusiness/).
