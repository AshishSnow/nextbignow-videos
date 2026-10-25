"""work/align.json -> work/timeline.json — FreshNestHub 'A fungus is eating your scalp' (Malassezia), host NESSA."""
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
    t_doyou=F("intro", "Do"), t_fungus=F("intro", "fungus"), t_eating=F("intro", "eating"), t_scalp=F("intro", "scalp"), t_right0=F("intro", "right"),
    t_now0=F("intro", "now"),
    t_yeast=F("name", "yeast"), t_called=F("name", "called"), t_mala=F("name", "Malassezia"), t_most=F("name", "most"), t_adults=F("name", "adults"),
    t_have=F("name", "have"),
    t_cant=F("fat", "can't"), t_fat=F("fat", "fat"), t_so=F("fat", "so"), t_feeds=F("fat", "feeds"), t_natural=F("fat", "natural"),
    t_oil=F("fat", "oil"), t_sebum=F("fat", "sebum"),
    t_first=F("chop", "First"), t_sends=F("chop", "sends"), t_enzymes=F("chop", "enzymes"), t_chop=F("chop", "chop"), t_oil2=F("chop", "oil"),
    t_fatty=F("chop", "fatty"), t_acids=F("chop", "acids"),
    t_eats=F("eat", "eats"), t_some=F("eat", "some"), t_them=F("eat", "them"), t_leaves=F("eat", "leaves"), t_rest=F("eat", "rest"),
    t_behind=F("eat", "behind"),
    t_one=F("oleic", "One"), t_leftover=F("oleic", "leftover"), t_oleic=F("oleic", "oleic"), t_acid=F("oleic", "acid"), t_soaks=F("oleic", "soaks"),
    t_skin=F("oleic", "skin"),
    t_people=F("react", "people"), t_scalp2=F("react", "scalp"), t_reacts=F("react", "reacts"), t_gets=F("react", "gets"),
    t_irritated=F("react", "irritated"), t_itchy=F("react", "itchy"),
    t_dead=F("flakes", "Dead"), t_cells=F("flakes", "cells"), t_shed=F("flakes", "shed"), t_clumps=F("flakes", "clumps"), t_and3=F("flakes", "and"),
    t_those=F("flakes", "those"), t_flakes=F("flakes", "FLAKES"),
    t_but=F("wait", "But"), t_wait=F("wait", "wait"), t_most2=F("wait", "most"), t_yeast2=F("wait", "yeast"), t_so2=F("wait", "So"),
    t_why=F("wait", "why"), t_all=F("wait", "all"), t_flakes2=F("wait", "flakes"),
    t_scientists=F("why", "Scientists"), t_think=F("why", "think"), t_depends=F("why", "depends"), t_sensitive=F("why", "sensitive"),
    t_scalp3=F("why", "scalp"),
    t_wash=F("tip", "Wash"), t_regularly=F("tip", "regularly"), t_if=F("tip", "if"), t_flakes3=F("tip", "flakes"), t_quit=F("tip", "quit"),
    t_see=F("tip", "see"), t_derm=F("tip", "dermatologist"),
    t_because=F("loop", "Because"), t_tiny=F("loop", "tiny"), t_fungus2=F("loop", "fungus"), t_having=F("loop", "having"),
    t_dinner=F("loop", "dinner"), t_head=F("loop", "head"), t_right=F("loop", "right"), t_now=F("loop", "now"),
)

b = {}
b["H1"] = 0.0
b["NM"] = lines["name"]["start"] - 0.12
b["FT"] = lines["fat"]["start"] - 0.12
b["SB"] = ev["t_feeds"] - 0.12
b["EN"] = lines["chop"]["start"] - 0.12
b["CH"] = ev["t_chop"] - 0.18
b["ET"] = lines["eat"]["start"] - 0.12
b["OL"] = lines["oleic"]["start"] - 0.12
b["RX"] = lines["react"]["start"] - 0.12
b["FL"] = lines["flakes"]["start"] - 0.12
b["WT"] = lines["wait"]["start"] - 0.12
b["SN"] = lines["why"]["start"] - 0.12
b["TP"] = lines["tip"]["start"] - 0.12
b["LP"] = lines["loop"]["start"] - 0.12
b["LQ"] = ev["t_having"] - 0.15
ORDER = ["H1", "NM", "FT", "SB", "EN", "CH", "ET", "OL", "RX", "FL", "WT", "SN", "TP", "LP", "LQ"]
TRANS = {"NM": "whip", "FT": "pop", "SB": "zoomblur", "EN": "zoomblur", "CH": "punch", "ET": "flash", "OL": "dip", "RX": "whip", "FL": "zoomblur",
         "WT": "flash", "SN": "pop", "TP": "whip", "LP": "dip", "LQ": "punch"}
shots = [dict(id=k, start=round(b[k], 3), end=round(b[ORDER[i + 1]], 3) if i + 1 < len(ORDER) else END, trans=TRANS.get(k, "cut"))
         for i, k in enumerate(ORDER)]
json.dump(dict(lines=lines, words=WD, shots=shots, events=ev, END=END, LEAD=LEAD), open(f"{S}/work/timeline.json", "w"), indent=1)
print("END", END)
for s in shots:
    print(f"{s['id']:4s} {s['start']:6.2f} -> {s['end']:6.2f} ({s['end'] - s['start']:.2f}s) in:{s['trans']}")
