"""Editorial pen-and-ink look (owner reference, 21 Nov 2026): cream paper, black ink line art, crosshatch shading by tone,
only two accents survive (antique gold, deep red). Works as a post-pass on any rendered RGB frame."""
import numpy as np, cv2

PAPER = np.array([247, 243, 234], np.float32)
INKC = np.array([34, 32, 30], np.float32)
GOLD = np.array([214, 160, 46], np.float32)
RED = np.array([150, 22, 34], np.float32)
_H = {}


def _hatch(h, w):
    if (h, w) in _H: return _H[(h, w)]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    rng = np.random.default_rng(3)
    wob = cv2.resize(rng.normal(0, 1.2, (h // 40 + 2, w // 40 + 2)).astype(np.float32), (w, h), interpolation=cv2.INTER_CUBIC)
    def lines(u, period, width):
        ph = np.mod(u + wob, period); return np.clip(1.0 - np.abs(ph - period / 2) / width, 0, 1)
    h1 = lines(xx + yy, 11.0, 1.3)          # 45 deg
    h2 = lines(xx - yy, 11.0, 1.3)          # -45 deg
    h3 = lines(yy * 1.0 + xx * 0.25, 7.0, 1.2)
    grain = rng.normal(0, 1, (h, w)).astype(np.float32)
    grain = cv2.GaussianBlur(grain, (0, 0), 0.8)
    fib = cv2.GaussianBlur(rng.normal(0, 1, (h, w)).astype(np.float32), (0, 0), 6)
    _H[(h, w)] = (h1, h2, h3, grain, fib); return _H[(h, w)]


def ink(rgb):
    """rgb: HxWx3 uint8 -> HxWx3 uint8 in the sketch look."""
    h, w = rgb.shape[:2]
    h1, h2, h3, grain, fib = _hatch(h, w)
    f = rgb.astype(np.float32) / 255.0
    L = 0.299 * f[..., 0] + 0.587 * f[..., 1] + 0.114 * f[..., 2]
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV).astype(np.float32)
    H_, S_, V_ = hsv[..., 0] * 2, hsv[..., 1] / 255, hsv[..., 2] / 255
    # tone: lift so bright flat fills read as paper, mids get light hatch, darks get crosshatch
    d = np.clip((0.88 - L) / 0.62, 0, 1)
    d = cv2.GaussianBlur(d, (0, 0), 1.0)
    hat = np.zeros_like(d)
    hat = np.maximum(hat, h1 * np.clip((d - 0.18) / 0.15, 0, 1) * 0.75)
    hat = np.maximum(hat, h2 * np.clip((d - 0.45) / 0.15, 0, 1) * 0.8)
    hat = np.maximum(hat, h3 * np.clip((d - 0.7) / 0.12, 0, 1) * 0.85)
    wash = 0.22 * d                                      # pencil-grey wash under the hatching
    # line art: strong luminance edges + already-dark outlines
    g8 = (L * 255).astype(np.uint8)
    ed = cv2.Canny(cv2.GaussianBlur(g8, (0, 0), 1.2), 40, 110).astype(np.float32) / 255
    ed = cv2.GaussianBlur(ed, (0, 0), 0.7) * 1.6
    dark = np.clip((0.22 - L) / 0.12, 0, 1)
    a = np.clip(np.maximum.reduce([hat, ed, dark]) + wash, 0, 1)
    a = np.clip(a * (1 + 0.12 * grain), 0, 1)
    paper = PAPER * (1 + 0.012 * fib[..., None])
    out = paper * (1 - a[..., None]) + INKC * a[..., None]
    # accents: saturated yellows/oranges -> antique gold, saturated reds/pinks -> deep red (keep their ink lines on top)
    gold = ((H_ > 16) & (H_ < 62) & (S_ > 0.45) & (V_ > 0.55)).astype(np.float32)
    red = (((H_ < 12) | (H_ > 330)) & (S_ > 0.5) & (V_ > 0.45)).astype(np.float32)
    gold = cv2.GaussianBlur(gold, (0, 0), 0.8); red = cv2.GaussianBlur(red, (0, 0), 0.8)
    keep = np.clip(1 - np.maximum(ed, dark), 0, 1)
    for m, col in ((gold, GOLD), (red, RED)):
        mm = (m * keep * 0.92)[..., None]
        tinted = col * (0.85 + 0.15 * (1 - hat[..., None]))
        out = out * (1 - mm) + tinted * mm
    return np.clip(out, 0, 255).astype(np.uint8)
