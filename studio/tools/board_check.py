#!/usr/bin/env python3
"""Board check — pre-flight for a writers'-room episode folder (vo_lines.py + shots.md) before anyone renders.

Usage:
  python3 studio/tools/board_check.py studio/episodes/queue/03-ikea-maze [--strict] [--json OUT]
  python3 studio/tools/board_check.py --all studio/episodes/queue            # one line per episode + totals

What it measures (no audio, no render; ~0.2 s per board):
  B1 rows ↔ lines   every VO line has exactly one storyboard row, in script order, no unknown ids
  B2 assets         every set / prop / cast look the board names exists in template/scripts (or is listed as "missing" =
                    the build brief: what the build run must write first). Registry = `def name(` in template/scripts/*.py,
                    set names from `_FLOOR` / `_STORY_SETS` / `SET_LIGHT.update(...)`, looks from `LOOKS`.
  B3 captions       `say("…")` is measured with the real Anton font at 150 px: the helper shrinks anything wider than 800 px,
                    so a caption that would render at < 60 % (≈ 90 px tall) is flagged — shorten it or split it in two.
                    `chip "…"` must stay ≥ 19 px after shrinking (PLAYBOOK §6: long chips become unreadable); `quote_card`
                    ≤ 5 wrapped lines at 58 px; `hud_rule` text ≤ 560 px at 50 px.
  B4 static rows    a row whose line is ≥ 4 s (0.40 s/word + pause, as story_check) with no visible change in the shot/props
                    cells (→, pop, slide, flip, cut, zoom, …) — PLAYBOOK §6: the picture changes every 2–3 s.
  B5 signature beats  series badge in the first 2 rows, cold_open/hud_clock in the first 3, "Oops" rows == "Oops" lines (≤ 1),
                    the series end card in the last 2 rows (YOUR MOVE: choice_card/hud_choice; SPOT THE TRICK: choice_card or
                    a SAVE pill; WHO REALLY OWNS IT: choice_card or TAG).
Exit 1 on B1/B5 failures (and on missing assets with --strict, for the build run after it wrote them). Captions and static rows
are warnings. Output ends with a BUILD BRIEF: the missing assets grouped by kind with the rows that use them.
"""
import argparse, glob, json, os, re, runpy, sys

HERE = os.path.dirname(os.path.abspath(__file__)); STUDIO_DIR = os.path.dirname(HERE)
TEMPLATE = os.path.join(STUDIO_DIR, "template", "scripts")
R = os.environ.get("STUDIO", "/home/claude/studio")
F_ANTON = f"{R}/fonts/anton/package/files/anton-latin-400-normal.woff"
F_PFI = f"{R}/fonts/playfair/package/files/playfair-display-latin-700-italic.woff"
F_INTER = ["/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf", "/usr/share/fonts/opentype/inter/Inter-Bold.otf"]
SEC_PER_WORD = 0.40
SAY_W, SAY_SIZE, SAY_MIN_SCALE = 800, 150, 0.60
CHIP_W, CHIP_MIN = 800, 19
QUOTE_W, QUOTE_SIZE, QUOTE_MAX_LINES = 820 - 80, 58, 5
RULE_MAX_W = 560
STATIC_SEC = 4.0
SHOT_RE = re.compile(r"[\s,]*(WIDE|MEDIUM|CU|two-shot|frame 1|top-down)\b")
SETWORD_RE = re.compile(r"\b([a-z][a-z0-9_]*)[\s,]+(?:WIDE|MEDIUM|two-shot)\b")
CHANGE_RE = re.compile(r"(→|->|\bpop|\bslide|\bflip|\bcut\b|\bzoom|\broll|\bswing|\bwalk|\bslam|\bdrop|\bfly|\bfall|\bspin|\bpush|\bpan\b|\bwhip|\bthen\b|\bturn|\bstand|\btake|\blean|\bkneel|\bhug|\bpoint|\bwave|\bempt|\bopen|\bclose|\bnod|\breach|\bappear|\bhighlight|\bstamp|\bflash|\bglow|\bdissolve|\bhop|\bflutter|\brain|\blight up|\blit\b|\bsnap|\bpull|\bset.{0,6}down|\bswap|\bsplit|\bhand|\bone by one|×\d|\bx\d|\bmultipl|\bgrow|\brise|\bfade|\bticks?\b|\bcount)", re.I)
SET_STOP = {"end", "split", "frame", "hero", "cu", "wide", "medium", "two", "ots", "data", "lab", "street", "lecture", "highway",
            "desk", "table", "gallery", "judge", "marketing", "bottling", "home", "office1950s"}
LOOK_WORDS = None  # filled from the registry


def registry():
    funcs, sets, looks = set(), set(), set()
    for p in sorted(glob.glob(os.path.join(TEMPLATE, "*.py"))):
        src = open(p, encoding="utf-8").read()
        funcs.update(re.findall(r"^def ([A-Za-z_][A-Za-z0-9_]*)\s*\(", src, re.M))
        for m in re.finditer(r"_FLOOR\s*=\s*dict\(([^)]*)\)", src): sets.update(re.findall(r"([a-z][a-z0-9_]*)\s*=", m.group(1)))
        for m in re.finditer(r"_FLOOR\.update\(([^)]*)\)", src): sets.update(re.findall(r"([a-z][a-z0-9_]*)\s*=", m.group(1)))
        for m in re.finditer(r"SET_LIGHT\.update\(([^)]*)\)", src): sets.update(re.findall(r"([a-z][a-z0-9_]*)\s*=", m.group(1)))
        for m in re.finditer(r"_STORY_SETS\s*=\s*\{([^}]*)\}", src): sets.update(re.findall(r"\"([a-z][a-z0-9_]*)\"", m.group(1)))
        m = re.search(r"^LOOKS\s*=\s*\{(.*?)^\}", src, re.M | re.S)
        if m: looks.update(re.findall(r"^\s*\"([a-z][a-z0-9_]*)\"\s*:", m.group(1), re.M))
    return funcs, sets, looks


def load_lines(folder):
    p = os.path.join(folder, "vo_lines.py")
    if not os.path.exists(p): p = os.path.join(folder, "scripts", "vo_lines.py")
    g = runpy.run_path(p)
    return g["LINES"], {k: g.get(k) for k in ("SERIES", "PART", "EP")}


def words(t): return re.findall(r"[A-Za-z0-9$£€%']+", t.replace("-", " ").replace("…", " "))


def parse_board(folder):
    p = os.path.join(folder, "shots.md")
    if not os.path.exists(p): raise SystemExit(f"no shots.md in {folder}")
    text = open(p, encoding="utf-8").read()
    pre, rows = [], []
    for ln in text.splitlines():
        s = ln.strip()
        if s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if not cells or cells[0].lower() == "line" or set(cells[0]) <= set("-: "): continue
            first = re.sub(r"[`*_]", "", cells[0]).strip()
            m = re.match(r"([a-z]{1,2}\d{1,2}[a-z]?)\b", first)
            rows.append({"id": m.group(1) if m else None, "cells": cells, "raw": s})
        elif not rows: pre.append(ln)
    return "\n".join(pre), rows, text


_FONTS = {}


def font(path, size):
    try:
        from PIL import ImageFont
        k = (path, int(size))
        if k not in _FONTS: _FONTS[k] = ImageFont.truetype(path, int(size))
        return _FONTS[k]
    except Exception:
        return None


def text_w(path, size, s, est_em=0.46):
    f = font(path, size)
    return f.getlength(s) if f else len(s) * size * est_em


def inter_path():
    for p in F_INTER:
        if os.path.exists(p): return p
    return None


STR = r"\"((?:[^\"\\]|\\.)*)\""
SAY_RE = re.compile(r"\bsay\(\s*(?:f\s*,\s*)?" + STR)
RULE_RE = re.compile(r"\bhud_rule\(\s*(?:f\s*,\s*)?\d+\s*,\s*" + STR)
CHIP_RE = re.compile(r"\bchip\s*\(?\s*" + STR)
QUOTE_RE = re.compile(r"\bquote_card\(\s*(?:f\s*,\s*)?" + STR + r"\s*,\s*" + STR)


def check(folder, funcs, sets, looks, strict=False):
    lines, meta = load_lines(folder)
    pre, rows, full = parse_board(folder)
    ids = [l[0] for l in lines]; texts = {l[0]: l[1] for l in lines}; pauses = {l[0]: l[3] for l in lines}
    rep = {"folder": os.path.basename(os.path.abspath(folder)), "series": meta.get("SERIES"), "part": meta.get("PART"), "ep": meta.get("EP"),
           "lines": len(lines), "rows": len(rows), "fail": [], "warn": [], "missing": {}, "sets_used": [], "looks_used": [], "captions": 0}
    # B1 rows <-> lines
    row_ids = [r["id"] for r in rows]
    for r in rows:
        if r["id"] is None: rep["fail"].append(f"B1 row without a line id: {r['cells'][0][:60]!r}")
    unknown = [i for i in row_ids if i and i not in ids]
    if unknown: rep["fail"].append(f"B1 rows for ids not in vo_lines.py: {unknown}")
    missing_rows = [i for i in ids if i not in row_ids]
    if missing_rows: rep["fail"].append(f"B1 lines without a storyboard row: {missing_rows}")
    dup = sorted({i for i in row_ids if i and row_ids.count(i) > 1})
    if dup: rep["fail"].append(f"B1 duplicate rows: {dup}")
    seq = list(dict.fromkeys(i for i in row_ids if i in ids))
    if seq != [i for i in ids if i in seq]:
        rep["fail"].append(f"B1 rows out of script order: board {seq} vs script {[i for i in ids if i in seq]}")
    # B2 assets — per row, then the preamble (header "new assets" lists are checked too, but reported separately)
    def refs(cell):
        out = []
        for m in re.finditer(r"set_view\(\s*[\"']([a-z0-9_]+)[\"']", cell): out.append(("set", m.group(1)))
        for m in re.finditer(r"\"base\"\s*:\s*\"([a-z0-9_]+)\"", cell): out.append(("look", m.group(1)))
        for m in re.finditer(r"\bwho\s*=\s*\"([a-z0-9_]+)\"", cell): out.append(("look", m.group(1)))
        for m in re.finditer(r"\*\*([a-z][a-z0-9_]*)([^*]*)\*\*", cell):
            w, rest = m.group(1), m.group(2)
            if w in sets or (("_" in w or re.search(r"\d", w)) and not w.endswith("_el")) or SHOT_RE.match(rest): out.append(("set", w))
        plain = re.sub(r"`[^`]*`", " ", cell)
        named = [x for x in sets if re.search(rf"\b{x}\b", plain)]
        out += [("set", x) for x in named]                      # "street set, 1950", "office: hero on the phone"
        has_set = bool(named) or re.search(r"\b[a-z_]+_view\b|sky_bg|map_view", cell)
        for m in SETWORD_RE.finditer(plain):                   # "bedroom90s MEDIUM", "highway WIDE"
            w = m.group(1)
            if w in sets or ("_" in w and not w.endswith("_el")) or re.search(r"\d", w): out.append(("set", w))
            elif not has_set and w not in SET_STOP and len(w) > 3: out.append(("setword", w))
        for m in re.finditer(r"`([^`]+)`", cell):
            tok = m.group(1).strip()
            code = re.sub(STR, '""', tok)                      # drop string literals: "Leonard v. PepsiCo (1999)" is not a call
            for fn in re.findall(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\(", code): out.append(("func", fn))
            if re.fullmatch(r"[a-z][a-z0-9_]*", tok): out.append(("tok", tok))
        for m in re.finditer(r"\b([a-z][a-z0-9]*(?:_[a-z0-9]+)*_(?:el|view|dressing))\b", cell): out.append(("func", m.group(1)))
        return out

    def classify(kind, name):
        if kind == "func":
            if name in funcs: return ("ok", "func")
            if name in {"f", "t", "t0", "who", "label", "y", "x", "s"}: return ("ok", "arg")
            return ("missing", "prop" if name.endswith(("_el", "_view", "_dressing")) else "func")
        if kind == "set": return ("ok", "set") if name in sets else ("missing", "set")
        if kind == "setword": return ("ok", "set") if name in sets else ("setword", "set")
        if kind == "look": return ("ok", "look") if name in looks else ("missing", "look")
        if kind == "tok":
            if name in funcs: return ("ok", "func")
            if name in looks: return ("ok", "look")
            if name in sets: return ("ok", "set")
            if name in SET_STOP or len(name) < 3: return ("ok", "word")
            if name.endswith(("_el", "_view", "_dressing")): return ("missing", "prop")
            if "_" in name or name.endswith(("store", "hall", "cafe", "office", "room", "yard", "shop", "plant", "fountain")): return ("missing", "set")
            return ("missing", "unknown")
        return ("ok", kind)

    missing, sets_used, looks_used, setwords = {}, set(), set(), {}
    for r in rows:
        for cell in r["cells"]:
            for kind, name in refs(cell):
                st, k = classify(kind, name)
                if st == "ok" and k == "set": sets_used.add(name)
                if st == "ok" and k == "look": looks_used.add(name)
                if st == "setword":
                    setwords.setdefault(name, []).append(r["id"]); continue
                if st == "missing":
                    d = missing.setdefault(name, {"kind": k, "rows": [], "context": ""})
                    if r["id"] not in d["rows"]: d["rows"].append(r["id"])
                    if not d["context"]:
                        i = cell.find(name); d["context"] = re.sub(r"\s+", " ", cell[max(0, i - 40): i + 60]).strip()
        # bare look words in the cast column (informational)
        if len(r["cells"]) > 2:
            for w in re.findall(r"`([a-z]+)`", r["cells"][2]):
                if w in looks: looks_used.add(w)
    header_missing = {}
    for kind, name in refs(pre):
        st, k = classify(kind, name)
        if st == "missing" and name not in missing: header_missing[name] = k
    rep["missing"] = missing; rep["header_only_missing"] = header_missing
    for w, rids in sorted(setwords.items()):
        rep["warn"].append(f"B2 {','.join(dict.fromkeys(rids))}: '{w} WIDE/MEDIUM' names no registered set — write the set's registered name (e.g. bedroom90s, street) or list the new set in the build brief")
    rep["sets_used"] = sorted(sets_used); rep["looks_used"] = sorted(looks_used)
    # B3 captions
    inter = inter_path()
    for r in rows:
        cells = " ".join(r["cells"])
        for m in SAY_RE.finditer(cells):
            s = m.group(1); rep["captions"] += 1
            w = text_w(F_ANTON, SAY_SIZE, s); sc = min(1.0, SAY_W / max(1, w))
            if sc < SAY_MIN_SCALE:
                rep["warn"].append(f"B3 {r['id']}: say({s!r}) renders at {sc:.0%} size ({int(SAY_SIZE * sc)} px tall) — shorten to ≲ {int(len(s) * sc / SAY_MIN_SCALE)} chars or split into two say() calls")
        for m in CHIP_RE.finditer(cells):
            s = m.group(1); sz = 26
            if inter:
                while text_w(inter, sz * 2, s) / 2 + 44 > CHIP_W and sz > 14: sz -= 1
            elif len(s) > 60: sz = 18
            if sz < CHIP_MIN: rep["warn"].append(f"B3 {r['id']}: chip {s!r} shrinks to {sz} px ({len(s)} chars) — keep source chips ≤ ~60 chars")
        for m in QUOTE_RE.finditer(cells):
            q = m.group(1); n_lines, cur = 1, ""
            for wd in q.split():
                cand = (cur + " " + wd).strip()
                if text_w(F_PFI, QUOTE_SIZE, cand, 0.5) > QUOTE_W and cur: n_lines += 1; cur = wd
                else: cur = cand
            if n_lines > QUOTE_MAX_LINES: rep["warn"].append(f"B3 {r['id']}: quote_card wraps to {n_lines} lines ({len(q.split())} words) — trim the quote to the key clause")
        for m in RULE_RE.finditer(cells):
            s = m.group(1); w = text_w(F_ANTON, 50, s)
            if w > RULE_MAX_W: rep["warn"].append(f"B3 {r['id']}: hud_rule {s!r} is {int(w)} px at 50 px (max ~{RULE_MAX_W}) — shorten")
    # B4 static rows
    for r in rows:
        if r["id"] not in texts: continue
        est = SEC_PER_WORD * len(words(texts[r["id"]])) + float(pauses.get(r["id"]) or 0)
        shotcells = " ".join(r["cells"][1:])
        if est >= STATIC_SEC and not CHANGE_RE.search(shotcells):
            rep["warn"].append(f"B4 {r['id']}: ~{est:.1f} s on one picture — add a second shot, a prop reveal or a camera move")
    # B5 signature beats
    head2 = " ".join(x["raw"] for x in rows[:2]); head3 = " ".join(x["raw"] for x in rows[:3]); tail2 = " ".join(x["raw"] for x in rows[-2:])
    if not re.search(r"series_badge|part_badge", head2): rep["fail"].append("B5 no series_badge/part_badge in the first 2 rows")
    if not re.search(r"cold_open|hud_clock", head3): rep["fail"].append("B5 no cold_open/hud_clock in the first 3 rows")
    oops_rows = sum(1 for x in rows if "oops_beat" in x["raw"]); oops_lines = sum(1 for l in lines if re.search(r"\boops\b", l[1], re.I))
    if oops_rows != oops_lines or oops_rows > 1: rep["fail"].append(f"B5 oops_beat rows {oops_rows} vs 'Oops' lines {oops_lines} (max 1)")
    series = (meta.get("SERIES") or "").upper()
    end_ok = {"YOUR MOVE": r"choice_card|hud_choice", "SPOT THE TRICK": r"choice_card|hud_choice|\bSAVE\b", "WHO REALLY OWNS IT": r"choice_card|hud_choice|\bTAG\b"}.get(series, r"choice_card|hud_choice|\bSAVE\b|\bTAG\b")
    if not re.search(end_ok, tail2): rep["fail"].append(f"B5 no series end card ({end_ok}) in the last 2 rows")
    if strict and missing: rep["fail"].append(f"B2 --strict: {len(missing)} assets missing from template/scripts: {sorted(missing)}")
    rep["ok"] = not rep["fail"]
    return rep


def fmt(rep, brief=True):
    out = [f"board_check {rep['folder']} — {rep['series']} EP {rep['ep']} part {rep['part']}: {rep['lines']} lines / {rep['rows']} rows, "
           f"sets {len(rep['sets_used'])} ({', '.join(rep['sets_used'])}), looks {', '.join(rep['looks_used']) or '-'}, say captions {rep['captions']}"]
    for f in rep["fail"]: out.append("  FAIL " + f)
    for w in rep["warn"]: out.append("  warn " + w)
    m = rep["missing"]
    if brief:
        out.append(f"  BUILD BRIEF — {len(m)} assets to write before rendering" + ("" if m else " (none)"))
        for kind in ("set", "prop", "look", "func", "unknown"):
            for name, d in sorted(m.items()):
                if d["kind"] == kind: out.append(f"    {kind:5s} {name:22s} rows {','.join(d['rows'])}: {d['context']}")
        hm = rep.get("header_only_missing") or {}
        if hm: out.append(f"    (named in the header only, no row uses them: {', '.join(f'{k} ({v})' for k, v in sorted(hm.items()))})")
    out.append(f"  RESULT {'PASS' if rep['ok'] else 'FAIL'}: {len(rep['fail'])} failures, {len(rep['warn'])} warnings, {len(m)} missing assets")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("folder", nargs="?"); ap.add_argument("--all"); ap.add_argument("--strict", action="store_true")
    ap.add_argument("--json"); ap.add_argument("--no-brief", action="store_true")
    a = ap.parse_args()
    funcs, sets, looks = registry()
    if not funcs: raise SystemExit(f"no template functions found under {TEMPLATE}")
    if not os.path.exists(F_ANTON): print(f"note: {F_ANTON} not found — caption widths are estimated (run setup.sh for exact numbers)", file=sys.stderr)
    folders = [a.folder] if a.folder else []
    if a.all: folders += sorted(d for d in glob.glob(os.path.join(a.all, "*")) if os.path.isdir(d) and os.path.exists(os.path.join(d, "shots.md")))
    if not folders: ap.error("give an episode folder or --all DIR")
    reps = [check(f, funcs, sets, looks, a.strict) for f in folders]
    for r in reps: print(fmt(r, brief=not a.no_brief))
    if len(reps) > 1:
        print(f"TOTAL {len(reps)} boards: {sum(len(r['fail']) for r in reps)} failures, {sum(len(r['warn']) for r in reps)} warnings, "
              f"{sum(len(r['missing']) for r in reps)} missing assets ({len({n for r in reps for n in r['missing']})} unique)")
    if a.json: json.dump(reps if len(reps) > 1 else reps[0], open(a.json, "w"), indent=1)
    sys.exit(0 if all(r["ok"] for r in reps) else 1)


if __name__ == "__main__":
    main()
