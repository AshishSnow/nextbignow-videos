"""Layout check: where does on-screen TEXT land vs the platform UI (Instagram Reels + YouTube Shorts), and is frame 1 alive?

R&D Visuals run, 28 Oct 2026.  Usage:
    python3 studio/tools/layout_check.py $P [--step 3] [--fake-align] [--json out.json]
How it works: every sampled frame is rendered twice in-process — normally, and with the caption helpers switched off
(ed_show/ui_word/wui/iui, say, chip/src, title3d, part_badge, hud_*). The pixel difference is exactly our caption text
(the film grain is deterministic per frame), so we know where every caption sits without OCR.
Zones (1080x1920) = PLAYBOOK §6: top 250 px, bottom 420 px, left 60 px, right 120 px. Measured UI (Sep 2026, third-party): IG organic
top 250, bottom 319, left 86, right 119; YT Shorts ~288 top, ~288 bottom (long titles go higher), ~140 right (action buttons).
Prints a summary, writes frames/layout_sheet.jpg (red = UI zones, magenta = caption pixels inside a UI zone).
--fake-align builds work/align.json + a silent work/vo.wav from scripts/vo_lines.py (~170 wpm) when no VO exists yet
(lets you check layouts of a script before any audio; timings are approximate)."""
import os, sys, json, math, argparse
import numpy as np, cv2

TOP, BOTTOM, LEFT, RIGHT = 250, 420, 60, 120   # = PLAYBOOK §6 (IG measured 250/319/86/119; YT ~288/288/–/140)
W_, H_ = 1080, 1920
TEXT_FUNCS = ["ed_show", "say", "title3d", "part_badge", "hud_clock", "hud_rule", "hud_timer", "hud_choice"]


def fake_align(P):
    import soundfile as sf
    ns = {}; exec(open(f"{P}/scripts/vo_lines.py").read(), ns)
    t = 0.25; words = []; lines = {}
    for L in ns["LINES"]:
        lid, text, speed, pause = L[0], L[1], L[2], L[3]
        ws = text.split(); st = t
        for w in ws:
            words.append(dict(line=lid, w=w, t=round(t, 3))); t += 60 / 170 / max(0.5, speed) * (1.0 + 0.25 * ("," in w or "." in w))
        lines[lid] = dict(start=round(st, 3), end=round(t, 3)); t += pause * 1.6 + 0.1
    json.dump(dict(lines=lines, words=words, dur=round(t, 3), LEAD=0.0, fake=True), open(f"{P}/work/align.json", "w"))
    y = np.zeros(int(48000 * t), np.float32)          # quiet tone under each word, so mouths still move (talk())
    for w in words:
        i = int(w["t"] * 48000); y[i:i + 12000] = 0.01 * np.sin(np.arange(len(y[i:i + 12000])) * 0.05)
    sf.write(f"{P}/work/vo.wav", y, 48000)


def load(P):
    os.environ["PROJ"] = P
    D = f"{P}/scripts"; ns = {"__name__": "layout_check", "__file__": f"{D}/anim.py"}
    src = open(f"{D}/anim.py").read()
    files = [x.strip().strip('"') for x in src.split("for _p in (")[1].split(")")[0].split(",") if x.strip()]
    extra = sorted(x for x in os.listdir(D) if x.startswith("anim_props") and x.endswith(".py") and x not in files)
    if extra and "anim_shots.py" in files:          # topic props (anim_props4.py …) the video run added to anim.py
        i = files.index("anim_shots.py"); files = files[:i] + extra + files[i:]
    for p_ in files:
        if os.path.exists(f"{D}/{p_}"): exec(compile(open(f"{D}/{p_}").read(), f"{D}/{p_}", "exec"), ns)
    return ns


def install_switch(ns):
    state = {"off": False}
    for name in TEXT_FUNCS:
        if name in ns and callable(ns[name]):
            orig = ns[name]
            def wrap(*a, _o=orig, **k):
                if state["off"]: return None
                return _o(*a, **k)
            ns[name] = wrap
    if "chip" in ns:
        oc = ns["chip"]
        def chip(*a, **k):
            pm, al = oc(*a, **k)
            return (pm * 0, al * 0) if state["off"] else (pm, al)
        ns["chip"] = chip
    return state


def zones_mask():
    m = np.zeros((H_, W_), bool)
    m[:TOP] = True; m[H_ - BOTTOM:] = True; m[:, :LEFT] = True; m[:, W_ - RIGHT:] = True
    return m


def core_detail(img):
    g = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY).astype(np.float32)
    e = (np.abs(np.diff(g, axis=1))[:-1] + np.abs(np.diff(g, axis=0))[:, :-1]) > 40
    return float(e[620:1500, LEFT:W_ - RIGHT].mean())


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("P"); ap.add_argument("--step", type=float, default=3.0)
    ap.add_argument("--fake-align", action="store_true"); ap.add_argument("--json"); ap.add_argument("--no-sheet", action="store_true")
    a = ap.parse_args(); P = a.P.rstrip("/")
    if a.fake_align or not os.path.exists(f"{P}/work/align.json"):
        if not os.path.exists(f"{P}/work/align.json") or a.fake_align: fake_align(P)
    ns = load(P); st = install_switch(ns); FPS = ns["FPS"]; N = int(round(ns["END"] * FPS))
    early = [0, 6, 12, 18, 24, 36, 48, 60, 72]
    frames = sorted(set([n for n in early if n < N] + list(range(0, N, max(1, int(a.step * FPS))))))
    Z = zones_mask(); rows = []; thumbs = []
    for n in frames:
        ns["_CINE_T"] = n / FPS; st["off"] = False; on = np.asarray(ns["compose"](n)).astype(np.int16)
        ns["_CINE_T"] = n / FPS; st["off"] = True; off = np.asarray(ns["compose"](n)).astype(np.int16); st["off"] = False
        # (_CINE_T = time used by stage() for twinkling windows; it is set by the previous finish() call, so pin it)
        txt = np.abs(on - off).max(-1) > 28
        txt = cv2.morphologyEx(txt.astype(np.uint8), cv2.MORPH_OPEN, np.ones((2, 2), np.uint8)).astype(bool)
        bad = txt & Z
        r = dict(n=n, t=round(n / FPS, 2), text_px=int(txt.sum()), bad_px=int(bad.sum()))
        if txt.any():
            ys, xs = np.nonzero(txt); r["bbox"] = [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]
        if bad.sum() > 150:
            ys, xs = np.nonzero(bad)
            r["zones"] = sorted({z for z, c in (("top", ys.min() < TOP), ("bottom", ys.max() >= H_ - BOTTOM),
                                                 ("left", xs.min() < LEFT), ("right", xs.max() >= W_ - RIGHT)) if c})
        if n == 0: r["core_detail_f0"] = round(core_detail(off.astype(np.uint8)), 4)
        rows.append(r)
        if not a.no_sheet:
            im = on.astype(np.uint8).copy(); ov = im.copy(); ov[Z] = (ov[Z] * 0.55 + np.array([220, 30, 30]) * 0.45).astype(np.uint8)
            ov[bad] = (255, 0, 255); thumbs.append((n, cv2.resize(ov, (216, 384), interpolation=cv2.INTER_AREA)))
    viol = [r for r in rows if r["bad_px"] > 150]
    first_cap = next((r["t"] for r in rows if r["text_px"] > 400), None)
    summ = dict(project=os.path.basename(P), frames=len(rows), caption_frames=sum(r["text_px"] > 400 for r in rows),
                violating_frames=len(viol), bad_px_total=int(sum(r["bad_px"] for r in rows)),
                zones={z: sum(z in r.get("zones", []) for r in viol) for z in ("top", "bottom", "left", "right")},
                first_caption_s=first_cap, f0_core_detail=rows[0].get("core_detail_f0"),
                f0_text=rows[0]["text_px"] > 400, fake_align=bool(json.load(open(f"{P}/work/align.json")).get("fake")))
    print(json.dumps(summ))
    for r in viol: print(f"  t={r['t']:6.2f}s bad_px={r['bad_px']:6d} zones={r.get('zones')} text bbox={r.get('bbox')}")
    if summ["f0_core_detail"] is not None and summ["f0_core_detail"] < 0.03:
        print("  WARN frame 0 is nearly empty in the hero band (core detail < 0.03) — put the hook object on screen at frame 0")
    if first_cap is None or first_cap > 0.5: print(f"  WARN first caption at {first_cap}s — show the hook caption by 0.5 s")
    if a.json: json.dump(dict(summary=summ, rows=rows), open(a.json, "w"), indent=0)
    if thumbs:
        cols = 8; rws = math.ceil(len(thumbs) / cols); sheet = np.full((rws * 404, cols * 220, 3), 30, np.uint8)
        for i, (n, th) in enumerate(thumbs):
            y0, x0 = (i // cols) * 404, (i % cols) * 220; sheet[y0:y0 + 384, x0:x0 + 216] = th
            cv2.putText(sheet, f"{n / FPS:.2f}s", (x0 + 4, y0 + 399), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (230, 230, 230), 1)
        os.makedirs(f"{P}/frames", exist_ok=True)
        cv2.imwrite(f"{P}/frames/layout_sheet.jpg", cv2.cvtColor(sheet, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 82])
    return summ


if __name__ == "__main__":
    main()
