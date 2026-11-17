"""Search Wikimedia Commons and download free-licence candidates (1920px thumbs via upload.wikimedia.org)."""
import sys, json, os, re, time, subprocess, urllib.parse
UA = "OMBStudio/1.0 (https://github.com/AshishSnow/nextbignow-videos)"
OK = ("cc0", "public domain", "pd", "cc by", "cc-by")
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img", "cand")
def get(url, out=None):
    cmd = ["curl", "-sS", "-A", UA, "-m", "60", url] + (["-o", out] if out else [])
    r = subprocess.run(cmd, capture_output=True); return r.stdout
def search(key, q, n=4):
    u = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(dict(action="query", generator="search", gsrsearch="filetype:bitmap " + q,
        gsrnamespace=6, gsrlimit=20, prop="imageinfo", iiprop="url|extmetadata|size", iiurlwidth=1920, format="json"))
    for tr in range(8):
        raw = get(u)
        try: d = json.loads(raw); break
        except Exception: time.sleep(30 + 15 * tr)
    else: return []
    res = []
    for p in sorted(d.get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 99)):
        ii = p["imageinfo"][0]; m = ii["extmetadata"]; lic = m.get("LicenseShortName", {}).get("value", "")
        if not lic.lower().startswith(OK) or ii["width"] < 1000 or "nc" in lic.lower() or "nd" in lic.lower(): continue
        th = ii.get("thumburl", ii["url"]).replace("thumb.wikimedia.org", "upload.wikimedia.org")
        if ii["width"] <= 1920: th = ii["url"]
        art = re.sub("<[^>]+>", "", m.get("Artist", {}).get("value", "unknown")).strip()
        res.append(dict(title=p["title"], url=th, page=ii["descriptionurl"], author=art[:80], license=lic))
        if len(res) >= n: break
    out = []
    for i, r in enumerate(res):
        f = os.path.join(D, f"{key}_{i}.jpg")
        for tr in range(5):
            get(r["url"], f); time.sleep(8)
            if subprocess.run(["file", f], capture_output=True, text=True).stdout.find("image") >= 0: break
            time.sleep(40 + 20 * tr)
        else:
            if os.path.exists(f): os.remove(f)
            continue
        r["file"] = f; out.append(r)
    return out
if __name__ == "__main__":
    Q = json.loads(sys.argv[1]); allr = {}
    p = os.path.join(D, "cands.json")
    if os.path.exists(p): allr = json.load(open(p))
    for k, q in Q.items():
        allr[k] = search(k, q); print(k, len(allr[k]), flush=True); json.dump(allr, open(p, 'w'), indent=1); time.sleep(45)
    json.dump(allr, open(p, "w"), indent=1)
