"""work/align.json -> work/timeline.json — BODY FILES 05 'What really happens when you crack your knuckles'."""
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
END = round(lines["loop"]["end"] + 0.6, 3)


def norm(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


def F(lid, sub, nth=0):
    return [x["t"] for x in WD[lid] if norm(sub) == norm(x["w"])][nth]


ev = dict(
    t_crack0=F("intro", "crack"), t_knuckles0=F("intro", "knuckles?"),
    t_bones0=F("myth", "bones"), t_grinding=F("myth", "grinding"), t_isnt=F("myth", "isn't."),
    t_joint=F("joint", "joint:"), t_two=F("joint", "two"), t_capsule=F("joint", "capsule,"),
    t_slippery=F("fluid", "slippery"), t_synovial=F("fluid", "synovial"),
    t_pull=F("pull", "pull"), t_apart=F("pull", "apart,"),
    t_pressure=F("pressure", "pressure"), t_drops=F("pressure", "drops."),
    t_split=F("cavity", "split"), t_pocket=F("cavity", "pocket"), t_forms=F("cavity", "forms"), t_crack=F("cavity", "crack"),
    t_2015=F("mri", "twenty"), t_filmed=F("mri", "filmed"), t_mri=F("mri", "MRI"),
    t_wait=F("wait", "wait"), t_half=F("wait", "half"), t_again=F("wait", "again."),
    t_arthritis=F("question", "arthritis?"),
    t_doctor=F("unger", "doctor"), t_left=F("unger", "left"), t_twice=F("unger", "twice"), t_sixty=F("unger", "sixty"),
    t_xrays=F("result", "X-rays?"), t_no=F("result", "No"), t_either=F("result", "either"),
    t_study=F("nuance", "study"), t_swelling=F("nuance", "swelling"), t_grip=F("nuance", "grip."),
    t_hurt=F("tip", "hurt"), t_talk=F("tip", "talk"),
    t_now=F("loop", "Now"), t_crack2=F("loop", "crack"),
)

b = {}
b["H1"] = 0.0
b["MY"] = lines["myth"]["start"] - 0.2
b["JT"] = lines["joint"]["start"] - 0.2
b["FL"] = lines["fluid"]["start"] - 0.12
b["PL"] = lines["pull"]["start"] - 0.15
b["PR"] = lines["pressure"]["start"] - 0.15
b["CV"] = lines["cavity"]["start"] - 0.2
b["MR"] = lines["mri"]["start"] - 0.15
b["WT"] = lines["wait"]["start"] - 0.2
b["QU"] = lines["question"]["start"] - 0.2
b["UN"] = lines["unger"]["start"] - 0.25
b["RS"] = lines["result"]["start"] - 0.15
b["NU"] = lines["nuance"]["start"] - 0.2
b["TP"] = lines["tip"]["start"] - 0.2
b["LP"] = lines["loop"]["start"] - 0.15
ORDER = ["H1", "MY", "JT", "FL", "PL", "PR", "CV", "MR", "WT", "QU", "UN", "RS", "NU", "TP", "LP"]
TRANS = {"MY": "slide", "JT": "push", "FL": "cut", "PL": "cut", "PR": "cut", "CV": "cut", "MR": "slide", "WT": "push", "QU": "slide",
         "UN": "push", "RS": "cut", "NU": "slide", "TP": "push", "LP": "slide"}
shots = [dict(id=k, start=round(b[k], 3), end=round(b[ORDER[i + 1]], 3) if i + 1 < len(ORDER) else END, trans=TRANS.get(k, "cut"))
         for i, k in enumerate(ORDER)]
json.dump(dict(lines=lines, words=WD, shots=shots, events=ev, END=END, LEAD=LEAD), open(f"{S}/work/timeline.json", "w"), indent=1)
print("END", END)
for s in shots:
    print(f"{s['id']:4s} {s['start']:6.2f} -> {s['end']:6.2f} ({s['end'] - s['start']:.2f}s) in:{s['trans']}")
