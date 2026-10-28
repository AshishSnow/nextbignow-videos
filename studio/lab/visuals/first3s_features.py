"""First-3-second features of finished videos (R&D Visuals run, 28 Oct 2026).
Usage: python3 first3s_features.py a.mp4 b.mp4 ... > features.csv
Decodes the first 3 s at 270x480 (gray + colour), and audio, and prints one CSV row per video."""
import sys, subprocess, numpy as np
W, H, FPS = 270, 480, 24
def frames(p, secs=3.0):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-t", str(secs), "-vf", f"scale={W}:{H}",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3).astype(np.float32)
def audio(p, secs=3.0):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-t", str(secs), "-ac", "1", "-ar", "16000",
                          "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.float32)
def edges(g):
    gx = np.abs(np.diff(g, axis=1))[:-1]; gy = np.abs(np.diff(g, axis=0))[:, :-1]
    return (gx + gy) > 40
def colourful(rgb):  # Hasler & Suesstrunk 2003
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]; rg = r - g; yb = .5 * (r + g) - b
    return float(np.hypot(rg.std(), yb.std()) + .3 * np.hypot(rg.mean(), yb.mean()))
# zones in 1080x1920 px -> scaled /4
S = 4
TOP, BOT, RIGHT, LEFT = 250 // S, (1920 - 420) // S, (1080 - 120) // S, 60 // S
CAP = (250 // S, 620 // S)        # caption band
CORE = (620 // S, 1500 // S)      # hero band
def feats(p):
    F = frames(p); g = F.mean(-1); n = len(F)
    e = [edges(x) for x in g]
    core = lambda E: E[CORE[0]:CORE[1], LEFT:RIGHT].mean()
    cap = lambda E: E[CAP[0]:CAP[1], LEFT:RIGHT].mean()
    d = np.abs(np.diff(g, axis=0)).mean(axis=(1, 2))           # per-frame motion
    cuts = int((d > 25).sum())
    capd = np.array([cap(E) for E in e]); t_cap = next((i / FPS for i, v in enumerate(capd) if v > 0.03), 9.9)
    # ink in unsafe side strips inside the caption band (text running into UI)
    side = np.mean([E[CAP[0]:CAP[1], RIGHT:].mean() + E[CAP[0]:CAP[1], :LEFT].mean() for E in e[12:]])
    topz = np.mean([E[:TOP].mean() for E in e[12:]])
    a = audio(p); fr = a[: len(a) // 160 * 160].reshape(-1, 160); db = 20 * np.log10(np.sqrt((fr ** 2).mean(1)) + 1e-9)
    t_audio = next((i * 0.01 for i, v in enumerate(db) if v > -35), 9.9)
    return dict(f0_core_edges=core(e[0]), f12_core_edges=core(e[12]), f0_cap=cap(e[0]), t_caption=t_cap,
                motion_1s=float(d[:23].mean()), motion_3s=float(d.mean()), cuts_3s=cuts, colour_f0=colourful(F[0]),
                luma_f0=float(g[0].mean()), side_ink=float(side), top_ink=float(topz), t_audio=t_audio,
                f0_vs_f36=float(np.abs(g[0] - g[min(36, n - 1)]).mean()))
if __name__ == "__main__":
    rows = [(p.split("/")[-1].rsplit(".", 1)[0], feats(p)) for p in sys.argv[1:]]
    keys = list(rows[0][1]); print("video," + ",".join(keys))
    for name, f in rows: print(name + "," + ",".join(f"{f[k]:.4f}" for k in keys))
