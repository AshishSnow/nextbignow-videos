"""work/align.json -> work/timeline.json — FreshNestHub 'Your tattoo is being eaten by your own cells' (macrophages), host NESSA."""
import json, sys, re
sys.path.insert(0, "/home/claude/reel-kit/english/scripts")
from vo_lines import LINES

S = "/home/claude/reel-kit/english"
AL = json.load(open(f"{S}/work/align.json"))
LEAD = 0.25
WD = {}
for w in AL["words"]:
    WD.setdefault(w["line"], []).append(dict(w=w["w"], t=round(w["t"] + LEAD, 3)))
lines = {lid: dict(start=round(AL["lines"][lid]["start"] + LEAD, 3), end=round(AL["lines"][lid]["end"] + LEAD, 3)) for lid, _ in LINES}
END = round(lines["loop"]["end"] + 0.45, 3)


def norm(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


def F(lid, sub, nth=0):
    return [x["t"] for x in WD[lid] if norm(sub) == norm(x["w"])][nth]


ev = dict(
    t_doyou=F("intro", "Do"), t_tattoo0=F("intro", "tattoo"), t_eaten0=F("intro", "eaten"), t_own=F("intro", "own"), t_cells0=F("intro", "cells"),
    t_tiny=F("name", "Tiny"), t_immune=F("name", "immune"), t_called=F("name", "called"), t_macro=F("name", "macrophages"), t_holding=F("name", "holding"),
    t_ink1=F("name", "ink"), t_right1=F("name", "right"),
    t_first=F("needle", "First"), t_needle=F("needle", "needle"), t_pushes=F("needle", "pushes"), t_below=F("needle", "below"),
    t_outer=F("needle", "outer"), t_into=F("needle", "into"), t_dermis=F("needle", "dermis"),
    t_outer2=F("shed", "outer"), t_sheds=F("shed", "sheds"), t_every=F("shed", "every"), t_but1=F("shed", "but"), t_dermis2=F("shed", "dermis"),
    t_stays=F("shed", "stays"),
    t_body=F("invader", "body"), t_treats=F("invader", "treats"), t_invader=F("invader", "invader"), t_sends=F("invader", "sends"),
    t_macro2=F("invader", "macrophages"),
    t_swallow=F("swallow", "swallow"), t_ink3=F("swallow", "ink"), t_cant=F("swallow", "can't"), t_break=F("swallow", "break"),
    t_down=F("swallow", "down"), t_so=F("swallow", "so"), t_hold=F("swallow", "hold"),
    t_all=F("see", "All"), t_those=F("see", "those"), t_cells4=F("see", "cells"), t_tattoo4=F("see", "tattoo"), t_see=F("see", "see"),
    t_but=F("wait", "But"), t_wait=F("wait", "wait"), t_these=F("wait", "these"), t_dont=F("wait", "don't"), t_live=F("wait", "live"),
    t_forever=F("wait", "forever"),
    t_when=F("die", "When"), t_dies=F("die", "dies"), t_spills=F("die", "spills"), t_ink6=F("die", "ink"),
    t_fresh=F("recap", "fresh"), t_macro7=F("recap", "macrophage"), t_gobbles=F("recap", "gobbles"), t_back=F("recap", "back"), t_up=F("recap", "up"),
    t_scientists=F("mice", "Scientists"), t_cycle=F("mice", "cycle"), t_mice=F("mice", "mice"), t_twenty=F("mice", "twenty"),
    t_eighteen=F("mice", "eighteen"),
    t_some=F("lymph", "Some"), t_bits=F("lymph", "bits"), t_drift=F("lymph", "drift"), t_lymph=F("lymph", "lymph"), t_nodes=F("lymph", "nodes"),
    t_getting=F("tip", "Getting"), t_choose=F("tip", "Choose"), t_licensed=F("tip", "licensed"), t_studio=F("tip", "studio"), t_let=F("tip", "let"),
    t_heal=F("tip", "heal"),
    t_so9=F("loop", "So"), t_tattoo9=F("loop", "tattoo"), t_love=F("loop", "love"), t_is9=F("loop", "is"), t_eaten9=F("loop", "eaten"),
    t_right=F("loop", "right"), t_now=F("loop", "now"),
)

b = {}
b["H1"] = 0.0
b["AN"] = lines["name"]["start"] - 0.12
b["ND"] = lines["needle"]["start"] - 0.12
b["SD"] = lines["shed"]["start"] - 0.12
b["IV"] = lines["invader"]["start"] - 0.12
b["SW"] = lines["swallow"]["start"] - 0.12
b["SE"] = lines["see"]["start"] - 0.12
b["WT"] = lines["wait"]["start"] - 0.12
b["DI"] = lines["die"]["start"] - 0.12
b["RC"] = lines["recap"]["start"] - 0.12
b["MC"] = lines["mice"]["start"] - 0.12
b["LY"] = lines["lymph"]["start"] - 0.12
b["TP"] = lines["tip"]["start"] - 0.12
b["LP"] = lines["loop"]["start"] - 0.12
b["LQ"] = ev["t_eaten9"] - 0.15
ORDER = ["H1", "AN", "ND", "SD", "IV", "SW", "SE", "WT", "DI", "RC", "MC", "LY", "TP", "LP", "LQ"]
TRANS = {"AN": "pop", "ND": "zoomblur", "SD": "whip", "IV": "flash", "SW": "zoomblur", "SE": "punch", "WT": "flash", "DI": "dip", "RC": "flashp",
         "MC": "whip", "LY": "zoomblur", "TP": "pop", "LP": "dip", "LQ": "punch"}
shots = [dict(id=k, start=round(b[k], 3), end=round(b[ORDER[i + 1]], 3) if i + 1 < len(ORDER) else END, trans=TRANS.get(k, "cut"))
         for i, k in enumerate(ORDER)]
json.dump(dict(lines=lines, words=WD, shots=shots, events=ev, END=END, LEAD=LEAD), open(f"{S}/work/timeline.json", "w"), indent=1)
print("END", END)
for s in shots:
    print(f"{s['id']:4s} {s['start']:6.2f} -> {s['end']:6.2f} ({s['end'] - s['start']:.2f}s) in:{s['trans']}")
