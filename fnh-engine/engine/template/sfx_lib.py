sfx = np.zeros((NS, 2), np.float32)


def add(x, t, gain=1.0):
    i = int(t * SR)
    if i < 0: x = x[-i:]; i = 0
    j = min(NS, i + len(x))
    if j > i: sfx[i:j] += x[: j - i] * gain


def whoosh(dur=0.5, peak=0.55, f_lo=300, f_hi=3800, level=-21):
    n = int(dur * SR); noise = rng.standard_normal(n).astype(np.float32)
    f, t2, Z = signal.stft(noise, SR, nperseg=1024); x = t2 / dur
    fc = np.where(x < peak, f_lo * (f_hi / f_lo) ** (x / peak), f_hi * (f_lo * 1.6 / f_hi) ** ((x - peak) / (1 - peak)))
    mask = np.exp(-0.5 * ((np.log2(np.maximum(f, 20))[:, None] - np.log2(fc)[None]) / 0.8) ** 2)
    _, w = signal.istft(Z * mask, SR, nperseg=1024); w = w[:n]; te = np.arange(n) / n
    w = w * np.where(te < peak, (te / peak) ** 2.5, np.exp(-(te - peak) / 0.12)); w = w / (np.abs(w).max() + 1e-9) * db(level)
    p = np.linspace(0, 1, n); return np.stack([w * (1 - 0.5 * p), w * (0.5 + 0.5 * p)], 1)


def boom(level=-14, tau=0.45):
    n = int(1.3 * SR); t2 = np.arange(n) / SR; fr = 32 + 80 * np.exp(-t2 / 0.06)
    s = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t2 / tau) * np.minimum(1, t2 / 0.003)
    cl = signal.sosfilt(signal.butter(2, 1800, "low", fs=SR, output="sos"), rng.standard_normal(n)) * np.exp(-t2 / 0.015)
    x = s + 0.3 * cl / np.abs(cl).max(); x = x / np.abs(x).max() * db(level); return np.stack([x, x], 1)


def click(level=-30):
    n = int(0.03 * SR); t2 = np.arange(n) / SR
    x = signal.sosfilt(signal.butter(2, [1500, 7000], "band", fs=SR, output="sos"), rng.standard_normal(n)) * np.exp(-t2 / 0.004)
    x = x / np.abs(x).max() * db(level); return np.stack([x, x * 0.9], 1)


def pop(level=-26, f0=900):
    n = int(0.12 * SR); t2 = np.arange(n) / SR; fr = f0 * (1 + 1.2 * np.exp(-t2 / 0.012))
    x = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t2 / 0.03) * np.minimum(1, t2 / 0.001)
    x = x / np.abs(x).max() * db(level); return np.stack([x, x], 1)


def ding(level=-26, f0=1318.5):
    n = int(1.2 * SR); t2 = np.arange(n) / SR
    x = sum(a * np.sin(2 * np.pi * f0 * r * t2) * np.exp(-t2 / d) for r, a, d in ((1, 1, 0.5), (2.0, 0.35, 0.25), (2.76, 0.2, 0.15)))
    x *= np.minimum(1, t2 / 0.002); x = x / np.abs(x).max() * db(level); return np.stack([x, x], 1)


def scratch(level=-24, dur=0.32):
    n = int(dur * SR); t2 = np.arange(n) / SR
    x = signal.sosfilt(signal.butter(2, [800, 5000], "band", fs=SR, output="sos"), rng.standard_normal(n))
    x *= (0.6 + 0.4 * np.sin(2 * np.pi * 38 * t2)) * np.minimum(1, t2 / 0.01) * np.exp(-t2 / 0.2)
    x = x / np.abs(x).max() * db(level); return np.stack([x * 0.8, x], 1)





def card_in(t, lv=-27):
    add(whoosh(0.35, level=lv, f_lo=700, f_hi=5200), t - 0.22); add(pop(lv + 2, 900), t + 0.05)


def swish(t, lv=-26):  # highlighter swipe
    add(whoosh(0.3, peak=0.4, f_lo=1500, f_hi=7000, level=lv), t - 0.12)


def glitch(t, lv=-23):
    add(scratch(lv, 0.22), t - 0.08)
    for i in range(4): add(click(lv - 6), t - 0.08 + i * 0.045)


def doorbell(level=-17):
    out = []
    for f0, dur in ((659.25, 0.55), (523.25, 1.1)):
        n_ = int(dur * SR); t2 = np.arange(n_) / SR
        x = sum(a * np.sin(2 * np.pi * f0 * r * t2) * np.exp(-t2 / dd) for r, a, dd in ((1, 1, 0.6), (2.0, 0.25, 0.3), (3.0, 0.1, 0.15)))
        out.append(x * np.minimum(1, t2 / 0.003))
    x = np.concatenate(out); x = x / np.abs(x).max() * db(level); return np.stack([x, x], 1)


def buzzer(level=-19, dur=0.55):
    n_ = int(dur * SR); t2 = np.arange(n_) / SR
    x = signal.square(2 * np.pi * 118 * t2) * 0.6 + signal.square(2 * np.pi * 121 * t2) * 0.4
    x = signal.sosfilt(signal.butter(2, 2500, "low", fs=SR, output="sos"), x) * np.minimum(1, t2 / 0.01) * np.minimum(1, (dur - t2) / 0.05)
    x = x / np.abs(x).max() * db(level); return np.stack([x, x], 1)


def chaching(level=-18):
    a_ = ding(level, 2093)[: int(0.5 * SR)]; b_ = ding(level + 1, 2637)
    out = np.zeros((int(0.12 * SR) + len(b_), 2), np.float32); out[: len(a_)] += a_; out[int(0.12 * SR):] += b_
    nz = signal.sosfilt(signal.butter(2, [3000, 9000], "band", fs=SR, output="sos"), rng.standard_normal(int(0.25 * SR)))
    nz *= np.exp(-np.arange(len(nz)) / SR / 0.06); nz = nz / np.abs(nz).max() * db(level - 6)
    out[: len(nz)] += np.stack([nz, nz], 1); return out


def thud(level=-15):
    return boom(level, 0.18) + np.pad(click(level - 4), ((0, int(1.3 * SR) - int(0.03 * SR)), (0, 0)))


def beep(level=-22, f0=2900, dur=0.11):
    n_ = int(dur * SR); t2 = np.arange(n_) / SR
    x = np.sin(2 * np.pi * f0 * t2) * np.minimum(1, t2 / 0.004) * np.minimum(1, (dur - t2) / 0.01)
    x = x / np.abs(x).max() * db(level); return np.stack([x, x], 1)


def creak(level=-26, dur=0.5):
    n_ = int(dur * SR); t2 = np.arange(n_) / SR
    fr = 180 + 60 * np.sin(2 * np.pi * 3 * t2)
    x = signal.sawtooth(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t2 / 0.25)
    x = signal.sosfilt(signal.butter(2, [400, 2500], "band", fs=SR, output="sos"), x)
    x = x / np.abs(x).max() * db(level); return np.stack([x * 0.8, x], 1)


def scratch_card(t0, dur, level=-22):
    n_ = int(dur * SR); tt_ = np.arange(n_) / SR
    x = signal.sosfilt(signal.butter(2, [1800, 9000], "band", fs=SR, output="sos"), rng.standard_normal(n_))
    x *= (0.45 + 0.55 * np.abs(np.sin(2 * np.pi * 9 * tt_))) * np.minimum(1, np.minimum(tt_, dur - tt_) / 0.03)
    add(np.stack([x, x * 0.9], 1).astype(np.float32) / np.abs(x).max() * db(level), t0)


def clink(t0, level=-24, f0=3300):
    add(ding(level, f0)[: int(0.25 * SR)], t0); add(ding(level - 4, f0 * 1.31)[: int(0.2 * SR)], t0 + 0.012)


def honk(level=-19, dur=0.42):
    n_ = int(dur * SR); tt_ = np.arange(n_) / SR
    x = signal.square(2 * np.pi * 349 * tt_) * 0.5 + signal.square(2 * np.pi * 440 * tt_) * 0.5
    x = signal.sosfilt(signal.butter(2, 2200, "low", fs=SR, output="sos"), x) * np.minimum(1, tt_ / 0.01) * np.minimum(1, (dur - tt_) / 0.04)
    x = x / np.abs(x).max() * db(level); return np.stack([x, x], 1).astype(np.float32)


def crt_off(level=-17, dur=0.5):
    n_ = int(dur * SR); tt_ = np.arange(n_) / SR
    fr = 1600 * np.exp(-tt_ / 0.12) + 60
    x = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-tt_ / 0.2) + 0.3 * rng.standard_normal(n_) * np.exp(-tt_ / 0.05)
    x = x / np.abs(x).max() * db(level); return np.stack([x, x], 1).astype(np.float32)


def bubbles(t0, n_=7, level=-26):
    for i in range(n_): add(pop(level - (i % 3), 1300 + 220 * (i % 4)), t0 + i * 0.11 + 0.03 * (i % 2))


# ---- foley added by FreshNestHub ep 10 (sugar rush): vinyl record scratch, candy-wrapper crinkle, cartoon boing, key jingle, lock click ----
def rec_scratch(level=-16):
    """vinyl record scratch ('wikka'): two fast strokes = band-passed noise + a buzzy tone whose pitch follows the hand speed."""
    out = []
    for d, up in ((0.11, True), (0.16, False)):
        n_ = int(d * SR); t2 = np.arange(n_) / SR; k = t2 / d
        sp = np.sin(np.pi * k) if up else np.sin(np.pi * k) ** 0.7
        fr = 120 + 1400 * sp
        tone = signal.sawtooth(2 * np.pi * np.cumsum(fr) / SR) * 0.6
        noi = rng.standard_normal(n_)
        f_, t_, Z = signal.stft(noi, SR, nperseg=256)
        fc = 400 + 3000 * np.interp(t_ / d, k, sp)
        mask = np.exp(-0.5 * ((np.log2(np.maximum(f_, 20))[:, None] - np.log2(fc)[None]) / 0.6) ** 2)
        _, w_ = signal.istft(Z * mask, SR, nperseg=256); w_ = w_[:n_]
        x = (tone + 1.5 * w_ / (np.abs(w_).max() + 1e-9)) * sp
        out.append(x)
    x = np.concatenate(out); x = signal.sosfilt(signal.butter(2, [150, 6000], "band", fs=SR, output="sos"), x)
    x = x / np.abs(x).max() * db(level); return np.stack([x, x * 0.9], 1)


def crinkle(level=-24, dur=0.45):
    """candy-wrapper crinkle: sparse bright crackles with a slow envelope."""
    n_ = int(dur * SR); t2 = np.arange(n_) / SR
    x = rng.standard_normal(n_) * (rng.random(n_) < 0.02)
    x = signal.sosfilt(signal.butter(2, [2500, 11000], "band", fs=SR, output="sos"), x)
    x = signal.lfilter([1], [1, -0.6], x) * np.sin(np.pi * t2 / dur)
    x = x / (np.abs(x).max() + 1e-9) * db(level); return np.stack([x, np.roll(x, 90)], 1)


def boing(level=-20, f0=220, dur=0.5):
    n_ = int(dur * SR); t2 = np.arange(n_) / SR
    fr = f0 * (1 + 0.35 * np.sin(2 * np.pi * 14 * t2) * np.exp(-t2 / 0.25)) * (1 + 0.6 * np.exp(-t2 / 0.03))
    x = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t2 / 0.22) * np.minimum(1, t2 / 0.003)
    x = x / np.abs(x).max() * db(level); return np.stack([x, x], 1)


def jingle(level=-24):
    out = np.zeros((int(0.55 * SR), 2), np.float32)
    for j in range(5):
        y = ding(level - 4, 3200 + 500 * rng.random())[: int(0.25 * SR)] * np.exp(-np.arange(int(0.25 * SR)) / SR / 0.05)[:, None]
        i = int(j * 0.05 * SR); out[i:i + len(y)] += y
    return out


def lock_click(level=-15):
    out = np.zeros((int(0.12 * SR), 2), np.float32)
    for k, (d0, f0) in enumerate(((0.0, 3200), (0.045, 2400))):
        n_ = int(0.05 * SR); t2 = np.arange(n_) / SR
        x = (np.sin(2 * np.pi * f0 * t2) + 0.6 * signal.sosfilt(signal.butter(2, [1500, 9000], "band", fs=SR, output="sos"), rng.standard_normal(n_))) * np.exp(-t2 / 0.006)
        i = int(d0 * SR); out[i:i + n_] += np.stack([x, x], 1)
    return out / np.abs(out).max() * db(level)

# ---- ep 11 foley: ice_crack (freeze-over), sip (slurp), chatter (teeth), wind (cold gust) ----
def ice_crack(level=-16, dur=0.6):
    """freeze-over: dense bright crackles that thin out + a low 'crunch' body (ice forming fast)."""
    n_ = int(dur * SR); t2 = np.arange(n_) / SR
    dens = 0.08 * np.exp(-t2 / 0.18) + 0.004
    x = rng.standard_normal(n_) * (rng.random(n_) < dens)
    x = signal.lfilter([1], [1, -0.85], x)
    hi = signal.sosfilt(signal.butter(2, [1800, 12000], "band", fs=SR, output="sos"), x)
    lo = signal.sosfilt(signal.butter(2, [120, 900], "band", fs=SR, output="sos"), rng.standard_normal(n_)) * np.exp(-t2 / 0.06)
    y = hi / (np.abs(hi).max() + 1e-9) + 0.6 * lo / (np.abs(lo).max() + 1e-9)
    y = y / np.abs(y).max() * db(level); return np.stack([y, np.roll(y, 70)], 1)


def sip(level=-24, dur=0.35):
    n_ = int(dur * SR); t2 = np.arange(n_) / SR
    x = rng.standard_normal(n_); fc = 900 + 1600 * t2 / dur
    y = np.zeros(n_)
    for i in range(0, n_, 512):
        sos = signal.butter(2, [fc[i] * 0.7, fc[i] * 1.3], "band", fs=SR, output="sos"); y[i:i + 512] = signal.sosfilt(sos, x[i:i + 512])
    y *= np.sin(np.pi * t2 / dur) ** 0.6 * (0.6 + 0.4 * np.sin(2 * np.pi * 18 * t2))
    y = y / (np.abs(y).max() + 1e-9) * db(level); return np.stack([y, y], 1)


def chatter(level=-26, dur=0.6, rate=16):
    out = np.zeros(int(dur * SR))
    for j in range(int(dur * rate)):
        c = pop(level, 2200 + 300 * rng.random())[:, 0][: int(0.03 * SR)] * np.exp(-np.arange(int(0.03 * SR)) / SR / 0.006)
        i = int(j / rate * SR); out[i:i + len(c)] += c[: len(out) - i]
    return np.stack([out, out], 1)


def wind(level=-27, dur=1.2):
    n_ = int(dur * SR); t2 = np.arange(n_) / SR
    x = rng.standard_normal(n_); y = np.zeros(n_)
    fc = 600 + 500 * np.sin(np.pi * t2 / dur) + 200 * np.sin(2 * np.pi * 1.3 * t2)
    for i in range(0, n_, 1024):
        sos = signal.butter(2, [fc[i] * 0.8, fc[i] * 1.25], "band", fs=SR, output="sos"); y[i:i + 1024] = signal.sosfilt(sos, x[i:i + 1024])
    y *= np.sin(np.pi * t2 / dur) ** 1.2
    y = y / (np.abs(y).max() + 1e-9) * db(level); return np.stack([y, np.roll(y, 300)], 1)


# ---- ep 12 (silver leaf): metal strike, paper rustle, metal-detector beeps ----
def clang(level=-20, f0=1250, dur=0.5):
    """metal strike: a few inharmonic partials (bar/plate modes) with fast attack + a click of noise."""
    n_ = int(dur * SR); t2 = np.arange(n_) / SR; y = np.zeros(n_)
    for r, a, tau in ((1.0, 1.0, 0.18), (2.76, 0.6, 0.09), (5.4, 0.35, 0.05), (8.93, 0.2, 0.03)):
        y += a * np.sin(2 * np.pi * f0 * r * t2 + rng.uniform(0, 6)) * np.exp(-t2 / tau)
    y += 0.5 * signal.sosfilt(signal.butter(2, [2000, 9000], "band", fs=SR, output="sos"), rng.standard_normal(n_)) * np.exp(-t2 / 0.004)
    y = y / np.abs(y).max() * db(level); return np.stack([y, np.roll(y, 40)], 1)


def rustle(level=-26, dur=0.5):
    n_ = int(dur * SR); t2 = np.arange(n_) / SR
    x = rng.standard_normal(n_) * (0.4 + 0.6 * (rng.random(n_) < 0.08))
    y = signal.sosfilt(signal.butter(2, [1500, 7000], "band", fs=SR, output="sos"), x) * np.sin(np.pi * t2 / dur) ** 0.7
    y = y / (np.abs(y).max() + 1e-9) * db(level); return np.stack([y, np.roll(y, 120)], 1)


def det_beep(t0, t1, level=-25, f0=1900):
    """metal detector: beeps that get faster and higher until t1."""
    tt = t0; k = 0
    while tt < t1:
        q = clamp((tt - t0) / max(0.1, t1 - t0)); add(beep(level, f0 + 700 * q, 0.06), tt); tt += 0.32 - 0.24 * q; k += 1



# ---- ep 13 foley: chop (knife through onion onto a board), hiss (gas), snip (scissors), plip (water drop), sizzle (frying pan), squirt (juice spray) ----
def _st(y, d=60): return np.stack([y, np.roll(y, d)], 1)


def chop(level=-20):
    """knife through an onion onto a board: wet crunch + a low wooden knock."""
    n_ = int(0.25 * SR); t2 = np.arange(n_) / SR
    cr = signal.sosfilt(signal.butter(2, [900, 6000], "band", fs=SR, output="sos"), rng.standard_normal(n_) * (rng.random(n_) < 0.3)) * np.exp(-t2 / 0.04)
    kn = np.sin(2 * np.pi * 180 * t2) * np.exp(-t2 / 0.05) + 0.5 * np.sin(2 * np.pi * 420 * t2) * np.exp(-t2 / 0.02)
    y = 0.7 * cr / (np.abs(cr).max() + 1e-9) + kn / np.abs(kn).max()
    return _st(y / np.abs(y).max() * db(level))


def hiss(level=-24, dur=0.8):
    n_ = int(dur * SR); t2 = np.arange(n_) / SR
    y = signal.sosfilt(signal.butter(2, [2500, 9000], "band", fs=SR, output="sos"), rng.standard_normal(n_)) * np.sin(np.pi * t2 / dur) ** 0.6
    return _st(y / np.abs(y).max() * db(level), 200)


def snip(level=-20):
    out = np.zeros(int(0.2 * SR))
    for k, f0 in ((0, 3800), (int(0.07 * SR), 4300)):
        t2 = np.arange(int(0.05 * SR)) / SR; y = np.sin(2 * np.pi * f0 * t2) * np.exp(-t2 / 0.008) + 0.4 * rng.standard_normal(len(t2)) * np.exp(-t2 / 0.003)
        out[k:k + len(y)] += y
    return _st(out / np.abs(out).max() * db(level))


def plip(level=-24, f0=900):
    t2 = np.arange(int(0.12 * SR)) / SR; f = f0 + 1400 * np.exp(-t2 / 0.02)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t2 / 0.03)
    return _st(y / np.abs(y).max() * db(level))


def sizzle(level=-26, dur=2.0):
    n_ = int(dur * SR); t2 = np.arange(n_) / SR
    y = signal.sosfilt(signal.butter(2, [3000, 11000], "band", fs=SR, output="sos"), rng.standard_normal(n_)) * 0.4
    cr = (rng.random(n_) < 0.0015) * rng.uniform(-1, 1, n_); y += signal.sosfilt(signal.butter(2, 2000, "high", fs=SR, output="sos"), cr) * 3
    y *= np.minimum(1, np.minimum(t2 / 0.2, (dur - t2) / 0.3))
    return _st(y / np.abs(y).max() * db(level), 300)


def squirt(level=-24, dur=0.35):
    n_ = int(dur * SR); t2 = np.arange(n_) / SR
    y = signal.sosfilt(signal.butter(2, [600, 4000], "band", fs=SR, output="sos"), rng.standard_normal(n_)) * np.exp(-t2 / 0.08)
    return _st(y / np.abs(y).max() * db(level), 90)


# ---- ep 14 foley: gulp, rip (sticker peel), rattle (key jiggling in a lock), buzz (bee), tick (clock), charge (rising bleeps) ----
def gulp(level=-20):
    t2 = np.arange(int(0.22 * SR)) / SR; f = 420 * np.exp(-t2 / 0.08) + 120
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t2 / 0.22) ** 0.5
    return _st(y / np.abs(y).max() * db(level))


def rip(level=-20, dur=0.35):
    n_ = int(dur * SR); t2 = np.arange(n_) / SR
    y = signal.sosfilt(signal.butter(2, [1200, 7000], "band", fs=SR, output="sos"), rng.standard_normal(n_) * (rng.random(n_) < 0.35)) * np.minimum(1, (dur - t2) / 0.1)
    return _st(y / np.abs(y).max() * db(level))


def rattle(level=-20, dur=0.6, rate=22):
    out = np.zeros(int(dur * SR))
    for k in range(int(dur * rate)):
        t2 = np.arange(int(0.03 * SR)) / SR; f0 = 2600 + 400 * (k % 2)
        y = np.sin(2 * np.pi * f0 * t2) * np.exp(-t2 / 0.006) + 0.5 * rng.standard_normal(len(t2)) * np.exp(-t2 / 0.002)
        i0 = int(k / rate * SR); out[i0:i0 + len(y)] += y[: len(out) - i0]
    return _st(out / np.abs(out).max() * db(level))


def buzz(level=-26, dur=1.0, f0=230):
    t2 = np.arange(int(dur * SR)) / SR; f = f0 + 12 * np.sin(2 * np.pi * 7 * t2)
    y = signal.sawtooth(2 * np.pi * np.cumsum(f) / SR) * (0.7 + 0.3 * np.sin(2 * np.pi * 31 * t2))
    y = signal.sosfilt(signal.butter(2, [200, 3000], "band", fs=SR, output="sos"), y) * np.minimum(1, np.minimum(t2 / 0.08, (dur - t2) / 0.15))
    return _st(y / np.abs(y).max() * db(level), 120)


def tick(level=-27):
    t2 = np.arange(int(0.04 * SR)) / SR; y = np.sin(2 * np.pi * 3200 * t2) * np.exp(-t2 / 0.004)
    return _st(y / np.abs(y).max() * db(level))


def charge(t0, t1, level=-27):
    k = 0; tt = t0
    while tt < t1: add(beep(level, 900 + 160 * k, 0.05), tt); tt += 0.12; k += 1


# ---- ep 15 foley: chocolate snap, gooey melt, crystal-brick clack, fridge hum, fridge door suction ----
def snap(level=-14):
    t2 = np.arange(int(0.18 * SR)) / SR
    crack = rng.standard_normal(len(t2)) * np.exp(-t2 / 0.006)
    crack = signal.sosfilt(signal.butter(2, [1800, 12000], "band", fs=SR, output="sos"), crack)
    ring = (np.sin(2 * np.pi * 3100 * t2) + 0.6 * np.sin(2 * np.pi * 4700 * t2)) * np.exp(-t2 / 0.02) * 0.35
    body = np.sin(2 * np.pi * 420 * t2) * np.exp(-t2 / 0.015) * 0.5
    y = crack + ring + body
    return _st(y / np.abs(y).max() * db(level))


def melt(level=-24, dur=0.9):
    t2 = np.arange(int(dur * SR)) / SR
    y = signal.sosfilt(signal.butter(2, 700, "low", fs=SR, output="sos"), rng.standard_normal(len(t2)))
    f = 320 * np.exp(-t2 / 0.4) + 90
    y = y * 0.6 + np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.5
    y *= np.sin(np.pi * np.clip(t2 / dur, 0, 1)) ** 1.5
    return _st(y / np.abs(y).max() * db(level), 90)


def clack(level=-24, f0=1900):
    t2 = np.arange(int(0.06 * SR)) / SR
    y = np.sin(2 * np.pi * f0 * t2) * np.exp(-t2 / 0.008) + 0.4 * rng.standard_normal(len(t2)) * np.exp(-t2 / 0.003)
    return _st(y / np.abs(y).max() * db(level))


def fridge_hum(level=-30, dur=2.0):
    t2 = np.arange(int(dur * SR)) / SR
    y = 0.6 * np.sin(2 * np.pi * 100 * t2) + 0.3 * np.sin(2 * np.pi * 200 * t2) + 0.08 * np.sin(2 * np.pi * 1260 * t2) * (1 + 0.3 * np.sin(2 * np.pi * 3 * t2))
    y *= np.minimum(1, np.minimum(t2 / 0.2, (dur - t2) / 0.3))
    return _st(y / np.abs(y).max() * db(level), 200)


def suction(level=-22):
    t2 = np.arange(int(0.25 * SR)) / SR
    y = signal.sosfilt(signal.butter(2, [300, 2500], "band", fs=SR, output="sos"), rng.standard_normal(len(t2))) * np.exp(-t2 / 0.05)
    y += np.sin(2 * np.pi * (180 + 600 * t2) * t2) * np.exp(-t2 / 0.06)
    return _st(y / np.abs(y).max() * db(level))


# ---- ep 16 foley: bubble-gum pop, wet gut squelch, rubbery stretch creak, stomach growl, spit ----
def bubble_pop(level=-14):
    t2 = np.arange(int(0.25 * SR)) / SR
    thump = np.sin(2 * np.pi * (140 * np.exp(-t2 / 0.05) + 60) * t2) * np.exp(-t2 / 0.05)
    snap_ = np.sin(2 * np.pi * np.cumsum(1400 * np.exp(-t2 / 0.02) + 300) / SR) * np.exp(-t2 / 0.025)
    air = signal.sosfilt(signal.butter(2, [1500, 8000], "band", fs=SR, output="sos"), rng.standard_normal(len(t2))) * np.exp(-t2 / 0.01)
    y = thump + 0.7 * snap_ + 0.5 * air
    return _st(y / np.abs(y).max() * db(level))


def squelch(level=-22, dur=0.6):
    t2 = np.arange(int(dur * SR)) / SR
    y = signal.sosfilt(signal.butter(2, [200, 1800], "band", fs=SR, output="sos"), rng.standard_normal(len(t2)))
    y *= (0.6 + 0.4 * np.sin(2 * np.pi * 9 * t2)) * np.sin(np.pi * np.clip(t2 / dur, 0, 1))
    y += 0.6 * np.sin(2 * np.pi * np.cumsum(220 * np.exp(-t2 / 0.3) + 70) / SR) * np.sin(np.pi * np.clip(t2 / dur, 0, 1))
    return _st(y / np.abs(y).max() * db(level), 120)


def stretch(level=-24, dur=0.7, up=True):
    t2 = np.arange(int(dur * SR)) / SR
    f = (180 + 220 * t2 / dur) if up else (400 - 220 * t2 / dur)
    ph = 2 * np.pi * np.cumsum(f) / SR
    y = (np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.3 * np.sin(3 * ph)) * (0.7 + 0.3 * np.sin(2 * np.pi * 23 * t2)) * np.sin(np.pi * np.clip(t2 / dur, 0, 1))
    return _st(y / np.abs(y).max() * db(level))


def growl(level=-16, dur=1.2):
    t2 = np.arange(int(dur * SR)) / SR
    y = signal.sosfilt(signal.butter(2, 220, "low", fs=SR, output="sos"), rng.standard_normal(len(t2))) * 2
    y += np.sin(2 * np.pi * np.cumsum(70 + 20 * np.sin(2 * np.pi * 3 * t2)) / SR)
    y *= (0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 5 * t2))) * np.minimum(1, np.minimum(t2 / 0.1, (dur - t2) / 0.3))
    return _st(y / np.abs(y).max() * db(level), 200)


def spit(level=-18):
    t2 = np.arange(int(0.2 * SR)) / SR
    y = signal.sosfilt(signal.butter(2, [800, 6000], "band", fs=SR, output="sos"), rng.standard_normal(len(t2))) * np.exp(-t2 / 0.04)
    y[: int(0.01 * SR)] += np.sin(2 * np.pi * 300 * t2[: int(0.01 * SR)]) * 2
    return _st(y / np.abs(y).max() * db(level))




# ---------------- ep 17 (31 Oct) foley: crunch (candy bite), fizz (sour sweet), nibble (tiny munching), tooth_crack, wash (saliva wave), scrub (toothbrush), squeak ----------------
def crunch(level=-16):
    t2 = np.arange(int(0.22 * SR)) / SR
    nz = signal.sosfilt(signal.butter(2, [900, 7000], "band", fs=SR, output="sos"), rng.standard_normal(len(t2)))
    envl = np.exp(-t2 / 0.03) + 0.7 * np.exp(-((t2 - 0.09) / 0.02) ** 2)
    knock = np.sin(2 * np.pi * 160 * t2) * np.exp(-t2 / 0.03)
    y = nz * envl + 0.6 * knock
    return _st(y / np.abs(y).max() * db(level))


def fizz(level=-24, dur=0.8):
    t2 = np.arange(int(dur * SR)) / SR
    y = signal.sosfilt(signal.butter(2, [2500, 9000], "band", fs=SR, output="sos"), rng.standard_normal(len(t2))) * np.sin(np.pi * np.clip(t2 / dur, 0, 1)) ** 0.5
    for k in rng.integers(0, len(t2) - 400, 40): y[k:k + 300] += np.sin(2 * np.pi * rng.uniform(1500, 4000) * t2[:300]) * np.exp(-t2[:300] / 0.004) * 1.5
    return _st(y / np.abs(y).max() * db(level), 90)


def nibble(level=-26, dur=0.5, rate=14):
    t2 = np.arange(int(dur * SR)) / SR
    y = np.zeros(len(t2))
    for k in range(int(dur * rate)):
        i = int(k / rate * SR); seg = t2[: int(0.02 * SR)]
        y[i:i + len(seg)] += signal.sosfilt(signal.butter(2, [1200, 5000], "band", fs=SR, output="sos"), rng.standard_normal(len(seg))) * np.exp(-seg / 0.004)
    return _st(y / (np.abs(y).max() + 1e-9) * db(level), 70)


def tooth_crack(level=-14):
    t2 = np.arange(int(0.6 * SR)) / SR
    sn = signal.sosfilt(signal.butter(2, [1800, 9000], "band", fs=SR, output="sos"), rng.standard_normal(len(t2))) * np.exp(-t2 / 0.012)
    cr = signal.sosfilt(signal.butter(2, [300, 2500], "band", fs=SR, output="sos"), rng.standard_normal(len(t2))) * (0.5 + 0.5 * signal.square(2 * np.pi * 38 * t2)) * np.exp(-t2 / 0.18)
    y = sn * 2 + cr * 0.8 + np.sin(2 * np.pi * 90 * t2) * np.exp(-t2 / 0.05)
    return _st(y / np.abs(y).max() * db(level))


def wash(level=-22, dur=1.0):
    t2 = np.arange(int(dur * SR)) / SR
    y = signal.sosfilt(signal.butter(2, [300, 3000], "band", fs=SR, output="sos"), rng.standard_normal(len(t2))) * np.sin(np.pi * np.clip(t2 / dur, 0, 1))
    y += 0.5 * np.sin(2 * np.pi * np.cumsum(180 + 60 * np.sin(2 * np.pi * 7 * t2)) / SR) * np.sin(np.pi * np.clip(t2 / dur, 0, 1)) ** 2
    return _st(y / np.abs(y).max() * db(level), 150)


def scrub(level=-26, dur=1.2, rate=5.5):
    t2 = np.arange(int(dur * SR)) / SR
    y = signal.sosfilt(signal.butter(2, [1500, 7000], "band", fs=SR, output="sos"), rng.standard_normal(len(t2))) * (0.25 + 0.75 * np.abs(np.sin(np.pi * rate * t2))) * np.sin(np.pi * np.clip(t2 / dur, 0, 1)) ** 0.4
    return _st(y / np.abs(y).max() * db(level), 60)


def squeak(level=-22):
    t2 = np.arange(int(0.3 * SR)) / SR
    y = np.sin(2 * np.pi * np.cumsum(1800 + 1400 * t2 / 0.3) / SR) * np.sin(np.pi * np.clip(t2 / 0.3, 0, 1)) ** 0.6
    return _st(y / np.abs(y).max() * db(level))


# ---------------- ep 18 (milk boils over): kitchen boil foley ----------------
def simmer(level=-28, dur=2.0, rate=9):
    """a rolling boil: random low plips over a soft rumble."""
    t2 = np.arange(int(dur * SR)) / SR
    y = signal.sosfilt(signal.butter(2, [80, 400], "band", fs=SR, output="sos"), rng.standard_normal(len(t2))) * 0.25
    for k in range(int(dur * rate)):
        i = int(rng.uniform(0, dur - 0.08) * SR); seg = t2[: int(0.07 * SR)]; f0 = rng.uniform(300, 900)
        y[i:i + len(seg)] += np.sin(2 * np.pi * np.cumsum(f0 * (1 + 0.8 * np.exp(-seg / 0.01))) / SR) * np.exp(-seg / 0.02) * rng.uniform(0.4, 1.0)
    y *= np.sin(np.pi * np.clip(t2 / dur, 0, 1)) ** 0.3
    return _st(y / (np.abs(y).max() + 1e-9) * db(level), 120)


def foam_rise(level=-22, dur=1.6):
    """the foam climbing: a band-passed noise swell rising in pitch and loudness, with little pops on top."""
    t2 = np.arange(int(dur * SR)) / SR; x = t2 / dur
    nz = rng.standard_normal(len(t2))
    f_, tt_, Z = signal.stft(nz, SR, nperseg=1024); fc = 400 * (3000 / 400) ** (tt_ / dur)
    mask = np.exp(-0.5 * ((np.log2(np.maximum(f_, 20))[:, None] - np.log2(fc)[None]) / 0.9) ** 2)
    _, y = signal.istft(Z * mask, SR, nperseg=1024); y = y[: len(t2)] * (0.15 + 0.85 * x ** 1.6)
    for k in range(18):
        i = int(rng.uniform(0.2, dur - 0.05) * SR); seg = t2[: int(0.03 * SR)]
        y[i:i + len(seg)] += np.sin(2 * np.pi * rng.uniform(900, 2200) * seg) * np.exp(-seg / 0.006) * 0.8
    return _st(y / (np.abs(y).max() + 1e-9) * db(level), 100)


def spill_sizzle(level=-16, dur=1.4):
    """milk hitting the flame: a sharp sizzle burst + a steam hiss that decays."""
    t2 = np.arange(int(dur * SR)) / SR
    sz = signal.sosfilt(signal.butter(2, [2000, 9000], "band", fs=SR, output="sos"), rng.standard_normal(len(t2))) * (0.6 + 0.4 * np.abs(np.sin(2 * np.pi * 37 * t2)))
    hs = signal.sosfilt(signal.butter(2, [800, 4000], "band", fs=SR, output="sos"), rng.standard_normal(len(t2)))
    y = sz * np.exp(-t2 / 0.35) * 1.2 + hs * np.exp(-t2 / 0.9) * 0.6 + np.sin(2 * np.pi * 70 * t2) * np.exp(-t2 / 0.06)
    return _st(y / np.abs(y).max() * db(level), 80)


def pop_bubble(level=-24, f0=1200):
    t2 = np.arange(int(0.08 * SR)) / SR
    y = np.sin(2 * np.pi * np.cumsum(f0 * (1 + 2.0 * np.exp(-t2 / 0.006))) / SR) * np.exp(-t2 / 0.014)
    y += signal.sosfilt(signal.butter(2, [2500, 8000], "band", fs=SR, output="sos"), rng.standard_normal(len(t2))) * np.exp(-t2 / 0.004) * 0.6
    return _st(y / np.abs(y).max() * db(level))


def knob(level=-24):
    """gas knob: a click + a short gas whoosh."""
    t2 = np.arange(int(0.5 * SR)) / SR
    y = signal.sosfilt(signal.butter(2, [1500, 6000], "band", fs=SR, output="sos"), rng.standard_normal(len(t2))) * np.exp(-t2 / 0.005) * 2
    y += signal.sosfilt(signal.butter(2, [300, 2000], "band", fs=SR, output="sos"), rng.standard_normal(len(t2))) * np.exp(-((t2 - 0.12) / 0.08) ** 2) * 0.5
    return _st(y / np.abs(y).max() * db(level))




# ---- ep 19 (31 Oct): creep (browning spreading), machine_whir (the PPO enzyme machine), dunk (slice into water), squeeze (lemon), shimmer (cold sparkle) ----
def creep(level=-26, dur=2.0):
    """the browning spreading: a soft granular crackle whose grains get denser and lower as it goes."""
    t2 = np.arange(int(dur * SR)) / SR; y = np.zeros(len(t2))
    for k in range(int(dur * 60)):
        i = int((rng.uniform(0, 1) ** 0.6) * (dur - 0.05) * SR); seg = t2[: int(0.02 * SR)]; f0 = rng.uniform(1800, 4200) * (1 - 0.5 * i / len(t2))
        y[i:i + len(seg)] += np.sin(2 * np.pi * f0 * seg) * np.exp(-seg / 0.004) * rng.uniform(0.3, 1.0)
    drone = signal.sosfilt(signal.butter(2, [90, 260], "band", fs=SR, output="sos"), rng.standard_normal(len(t2))) * (t2 / dur) ** 1.5 * 0.5
    y = y + drone
    y *= np.sin(np.pi * np.clip(t2 / dur, 0, 1)) ** 0.4
    return _st(y / (np.abs(y).max() + 1e-9) * db(level), 90)


def machine_whir(level=-26, dur=0.6, f0=140):
    """PPO the tiny machine: a motor whir (buzzy saw at f0 rising) + a little click at the end."""
    t2 = np.arange(int(dur * SR)) / SR
    ph = 2 * np.pi * np.cumsum(f0 * (1 + 0.6 * t2 / dur)) / SR
    y = (signal.sawtooth(ph) * 0.5 + np.sin(ph * 2) * 0.3) * np.exp(-t2 / (dur * 0.6))
    y = signal.sosfilt(signal.butter(2, 2200, "low", fs=SR, output="sos"), y)
    i = int((dur - 0.05) * SR); seg = t2[: int(0.03 * SR)]
    y[i:i + len(seg)] += signal.sosfilt(signal.butter(2, [2000, 6000], "band", fs=SR, output="sos"), rng.standard_normal(len(seg))) * np.exp(-seg / 0.004) * 0.8
    return _st(y / (np.abs(y).max() + 1e-9) * db(level))


def dunk(level=-20, dur=0.7):
    """a slice dropped into water: a plop (pitched blip down) + a slosh (band-passed noise swell)."""
    t2 = np.arange(int(dur * SR)) / SR
    y = np.sin(2 * np.pi * np.cumsum(420 * (1 + 1.5 * np.exp(-t2 / 0.02))) / SR) * np.exp(-t2 / 0.05) * 1.2
    sl = signal.sosfilt(signal.butter(2, [300, 2600], "band", fs=SR, output="sos"), rng.standard_normal(len(t2))) * np.exp(-((t2 - 0.14) / 0.12) ** 2) * 0.7
    y = y + sl
    return _st(y / (np.abs(y).max() + 1e-9) * db(level), 70)


def squeeze(level=-24, dur=0.8):
    """a lemon squeezed: a wet squirt + three drips."""
    t2 = np.arange(int(dur * SR)) / SR
    y = signal.sosfilt(signal.butter(2, [900, 5000], "band", fs=SR, output="sos"), rng.standard_normal(len(t2))) * np.exp(-t2 / 0.12) * (0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 23 * t2)))
    for k in range(3):
        i = int((0.25 + 0.16 * k) * SR); seg = t2[: int(0.06 * SR)]
        y[i:i + len(seg)] += np.sin(2 * np.pi * np.cumsum((1500 + 300 * k) * (1 + 0.8 * np.exp(-seg / 0.008))) / SR) * np.exp(-seg / 0.015) * 0.8
    return _st(y / (np.abs(y).max() + 1e-9) * db(level))


def shimmer(level=-26, dur=1.2):
    """a cold high sparkle (the Arctic apple): detuned high sines with a slow flutter."""
    t2 = np.arange(int(dur * SR)) / SR; y = np.zeros(len(t2))
    for k, f0 in enumerate((2637, 3136, 3951, 5274)):
        y += np.sin(2 * np.pi * f0 * (1 + 0.002 * np.sin(2 * np.pi * (5 + k) * t2)) * t2) * np.exp(-t2 / (0.5 + 0.1 * k)) * (0.5 + 0.5 * np.sin(2 * np.pi * (3 + k) * t2)) / (k + 1)
    return _st(y / (np.abs(y).max() + 1e-9) * db(level), 110)


# ---- ep 20 (1 Nov) foley: security camera hum, microwave hum + end beeps, spore shell crack, germ giggle, pedal bin ----
def cctv_hum(level=-32, dur=3.0):
    """security camera: 50 Hz mains hum with harmonics + a faint servo whir that rises and falls."""
    t2 = np.arange(int(dur * SR)) / SR
    y = sum(np.sin(2 * np.pi * 50 * k * t2) / k for k in (1, 2, 3, 5)) * 0.4
    y += signal.sosfilt(signal.butter(2, [1800, 4200], "band", fs=SR, output="sos"), rng.standard_normal(len(t2))) * (0.15 + 0.15 * np.sin(2 * np.pi * 0.7 * t2))
    y *= np.minimum(1, np.minimum(t2 / 0.2, (dur - t2) / 0.3))
    return _st(y / (np.abs(y).max() + 1e-9) * db(level))


def micro_hum(level=-28, dur=2.0):
    """microwave running: a 100 Hz transformer hum + a soft turntable rattle."""
    t2 = np.arange(int(dur * SR)) / SR
    y = (np.sin(2 * np.pi * 100 * t2) + 0.5 * np.sin(2 * np.pi * 200 * t2) + 0.25 * np.sign(np.sin(2 * np.pi * 100 * t2))) * 0.5
    y += signal.sosfilt(signal.butter(2, [400, 1600], "band", fs=SR, output="sos"), rng.standard_normal(len(t2))) * 0.12 * (0.5 + 0.5 * np.sin(2 * np.pi * 3 * t2))
    y *= np.minimum(1, np.minimum(t2 / 0.05, (dur - t2) / 0.1))
    return _st(y / (np.abs(y).max() + 1e-9) * db(level))


def micro_beep(t0, level=-24):
    for j in range(3): add(beep(level, 2000, 0.16), t0 + j * 0.28)


def shell_crack(level=-20):
    """a spore's armour cracking: a dry woody snap (band-passed click burst) + a few crumbs."""
    t2 = np.arange(int(0.4 * SR)) / SR
    y = signal.sosfilt(signal.butter(2, [700, 3500], "band", fs=SR, output="sos"), rng.standard_normal(len(t2))) * np.exp(-t2 / 0.012)
    for k in range(4):
        i = int((0.05 + 0.06 * k + rng.uniform(0, 0.02)) * SR); seg = t2[: int(0.015 * SR)]
        y[i:i + len(seg)] += signal.sosfilt(signal.butter(2, [2000, 6000], "band", fs=SR, output="sos"), rng.standard_normal(len(seg))) * np.exp(-seg / 0.003) * 0.5
    return _st(y / (np.abs(y).max() + 1e-9) * db(level))


def giggle(level=-27, dur=0.5):
    """a germ giggle: a fast run of pitched chirps going up and down."""
    t2 = np.arange(int(dur * SR)) / SR; y = np.zeros(len(t2))
    for k in range(7):
        i = int(k * dur / 7 * SR); seg = t2[: int(0.045 * SR)]; f0 = 1200 + 300 * math.sin(k * 1.3)
        y[i:i + len(seg)] += np.sin(2 * np.pi * np.cumsum(f0 * (1 + 0.4 * np.sin(2 * np.pi * 30 * seg))) / SR) * np.exp(-seg / 0.02)
    return _st(y / (np.abs(y).max() + 1e-9) * db(level), 80)


def pedal_bin(t, lv=-20):
    add(clang(lv - 2, 700, 0.4), t); add(thud(lv), t + 0.3); add(crunch(lv - 4), t + 0.33)


# ---- ep 21 foley (bread): bread_knock (a stale slice on wood: dull, short knock), nail_tink (a nail taking a hit: bright little ping), toaster_lever (a ratchet click down), toaster_pop (the spring: thunk + twang), crust_crack (a dry crust breaking), freeze_creak (ice tightening)
def bread_knock(level=-14):
    n_ = int(0.12 * SR); t2 = np.arange(n_) / SR
    y = (np.sin(2 * np.pi * 170 * t2) + 0.6 * np.sin(2 * np.pi * 330 * t2) + 0.25 * rng.standard_normal(n_)) * np.exp(-t2 / 0.022)
    return _st(y / np.abs(y).max() * db(level))


def nail_tink(level=-22):
    n_ = int(0.2 * SR); t2 = np.arange(n_) / SR
    y = (np.sin(2 * np.pi * 2600 * t2) + 0.5 * np.sin(2 * np.pi * 4100 * t2)) * np.exp(-t2 / 0.035)
    return _st(y / np.abs(y).max() * db(level))


def toaster_lever(level=-20):
    n_ = int(0.25 * SR); y = np.zeros(n_)
    for j in range(5):
        i = int((0.02 + j * 0.03) * SR); m = int(0.012 * SR)
        y[i:i + m] += rng.standard_normal(m) * np.exp(-np.arange(m) / (0.003 * SR))
    i = int(0.19 * SR); t2 = np.arange(n_ - i) / SR; y[i:] += np.sin(2 * np.pi * 240 * t2) * np.exp(-t2 / 0.02) * 1.4
    return _st(y / np.abs(y).max() * db(level))


def toaster_pop(level=-15):
    n_ = int(0.55 * SR); t2 = np.arange(n_) / SR
    y = np.sin(2 * np.pi * 150 * t2) * np.exp(-t2 / 0.03) * 1.2 + np.sin(2 * np.pi * (520 + 70 * np.sin(2 * np.pi * 34 * t2)) * t2) * np.exp(-t2 / 0.13) * 0.5
    return _st(y / np.abs(y).max() * db(level))


def crust_crack(level=-20, dur=0.4):
    n_ = int(dur * SR); y = np.zeros(n_)
    for j in range(16):
        i = int(rng.uniform(0, n_ * 0.8)); m = int(rng.uniform(0.002, 0.008) * SR)
        y[i:i + m] += rng.standard_normal(m) * rng.uniform(0.3, 1.0)
    y = signal.sosfilt(signal.butter(2, 1500, "high", fs=SR, output="sos"), y)
    return _st(y / (np.abs(y).max() + 1e-9) * db(level))


def freeze_creak(level=-26, dur=0.9):
    n_ = int(dur * SR); t2 = np.arange(n_) / SR; f_ = 300 + 900 * t2 / dur
    y = np.sign(np.sin(2 * np.pi * np.cumsum(f_ / 7) / SR * 7)) * (0.5 + 0.5 * np.sin(2 * np.pi * 21 * t2)) * np.minimum(t2 / 0.1, (dur - t2) / 0.2).clip(0, 1)
    y = signal.sosfilt(signal.butter(2, [500, 3200], "band", fs=SR, output="sos"), y)
    return _st(y / (np.abs(y).max() + 1e-9) * db(level))


# ---- ep 22 foley: soft_flop (a limp snack sagging), footstep (a heavyset flat plant on stone), clip_snap (airtight jar clip), oven_ding, soggy (a backbeat that lost its crunch), drink (a straw gulp) ----
def soft_flop(level=-18):
    t2 = np.arange(int(0.3 * SR)) / SR
    y = np.sin(2 * np.pi * (170 - 240 * t2) * t2) * np.exp(-t2 / 0.09) + 0.3 * signal.sosfilt(signal.butter(2, 500, "low", fs=SR, output="sos"), rng.standard_normal(len(t2))) * np.exp(-t2 / 0.06)
    return _st(y / np.abs(y).max() * db(level))


def footstep(level=-24, heavy=1.0):
    t2 = np.arange(int(0.16 * SR)) / SR
    y = np.sin(2 * np.pi * (95 + 40 * np.exp(-t2 / 0.015)) * t2) * np.exp(-t2 / (0.03 * heavy)) + 0.35 * signal.sosfilt(signal.butter(2, [500, 2600], "band", fs=SR, output="sos"), rng.standard_normal(len(t2))) * np.exp(-t2 / 0.012)
    return _st(y / np.abs(y).max() * db(level))


def clip_snap(level=-16):
    t2 = np.arange(int(0.2 * SR)) / SR
    y = np.sin(2 * np.pi * 2300 * t2) * np.exp(-t2 / 0.008) + 0.8 * np.sin(2 * np.pi * 420 * t2) * np.exp(-t2 / 0.03) + 0.5 * rng.standard_normal(len(t2)) * np.exp(-t2 / 0.004)
    return _st(y / np.abs(y).max() * db(level))


def oven_ding(level=-20):
    t2 = np.arange(int(1.0 * SR)) / SR
    y = (np.sin(2 * np.pi * 1760 * t2) + 0.5 * np.sin(2 * np.pi * 3520 * t2) + 0.25 * np.sin(2 * np.pi * 5280 * t2)) * np.exp(-t2 / 0.3)
    return _st(y / np.abs(y).max() * db(level))


def soggy(level=-20):
    t2 = np.arange(int(0.18 * SR)) / SR
    y = signal.sosfilt(signal.butter(2, 380, "low", fs=SR, output="sos"), rng.standard_normal(len(t2))) * np.exp(-t2 / 0.05) + 0.7 * np.sin(2 * np.pi * 130 * t2) * np.exp(-t2 / 0.04)
    return _st(y / np.abs(y).max() * db(level))


def drink(level=-24, n=3, gap=0.22):
    L = int((n * gap + 0.15) * SR); y = np.zeros(L)
    for j in range(n):
        i = int(j * gap * SR); t2 = np.arange(int(0.14 * SR)) / SR
        s_ = np.sin(2 * np.pi * (240 + 500 * t2) * t2) * np.exp(-t2 / 0.05) + 0.3 * signal.sosfilt(signal.butter(2, [600, 3000], "band", fs=SR, output="sos"), rng.standard_normal(len(t2))) * np.exp(-t2 / 0.03)
        y[i:i + len(s_)] += s_[: L - i]
    return _st(y / np.abs(y).max() * db(level))


# ep 23 foley
def crackle(level=-26, dur=1.0):
    """a burning fuse / cracker crackle: sparse random clicks over a noise floor (new foley, ep 23)."""
    N_ = int(dur * SR); x = np.zeros(N_); r_ = np.random.default_rng(int(dur * 100) + 3)
    for i in range(int(dur * 42)):
        p = r_.integers(0, max(1, N_ - 900)); L_ = r_.integers(120, 800); x[p:p + L_] += r_.normal(0, 1, L_) * np.exp(-np.linspace(0, 6, L_)) * r_.uniform(0.3, 1)
    x = x / (np.abs(x).max() + 1e-9) * db(level)
    return np.stack([x, x], 1).astype(np.float32)
def munch_sfx(level=-22, dur=1.2):
    """fast happy chewing (ep 23): soft crunches with squelchy tails."""
    N_ = int(dur * SR); x = np.zeros(N_); r_ = np.random.default_rng(5); t_ = 0.0
    while t_ < dur - 0.2:
        p = int(t_ * SR); L_ = int(0.09 * SR); x[p:p + L_] += r_.normal(0, 1, L_) * np.exp(-np.linspace(0, 5, L_)) * r_.uniform(0.6, 1); t_ += r_.uniform(0.14, 0.2)
    b_ = signal.butter(2, [300, 3200], "band", fs=SR, output="sos"); x = signal.sosfilt(b_, x); x = x / (np.abs(x).max() + 1e-9) * db(level)
    return np.stack([x, x], 1).astype(np.float32)


# ep 24: the sound of a speed ramp, a heavy slowed drop, and the FreshNestHub audio logo (1 s). audio_logo adds itself: audio_logo(t, lv)
def slowmo_swell(level=-26, dur=2.0):
    """the sound of a speed ramp: a low sine + filtered noise that slowly rise toward the impact."""
    N_ = int(dur * SR); tt = np.arange(N_) / SR; k = tt / dur
    ph = 2 * np.pi * np.cumsum(50 + 90 * k ** 2) / SR; x = 0.6 * np.sin(ph) * k
    nz = signal.sosfilt(signal.butter(2, [200, 2400], "band", fs=SR, output="sos"), np.random.default_rng(3).normal(0, 1, N_)) * k ** 2.5
    x = x + 0.5 * nz / (np.abs(nz).max() + 1e-9); x = x / (np.abs(x).max() + 1e-9) * db(level)
    return np.stack([x, x], 1).astype(np.float32)
def drip_big(level=-13):
    """a heavy, pitched-down drop landing (a slowed plip with a body)."""
    N_ = int(0.5 * SR); tt = np.arange(N_) / SR
    x = np.sin(2 * np.pi * (240 * tt + 340 * tt ** 2)) * np.exp(-tt * 9) + 0.5 * np.sin(2 * np.pi * 90 * tt) * np.exp(-tt * 14)
    x = x / (np.abs(x).max() + 1e-9) * db(level); return np.stack([x, x], 1).astype(np.float32)
def audio_logo(t, lv=-16):
    """the FreshNestHub sting (1 s): three warm rising mallet notes (Fresh-Nest-Hub) + a crunch on the last one."""
    for j, f0 in enumerate((587.3, 880.0, 1174.7)):
        N_ = int(0.6 * SR); tt = np.arange(N_) / SR; x = (np.sin(2 * np.pi * f0 * tt) + 0.3 * np.sin(2 * np.pi * f0 * 4 * tt) * np.exp(-tt * 24)) * np.exp(-tt * 7)
        x = x / (np.abs(x).max() + 1e-9) * db(lv + (j == 2) * 2); add(np.stack([x, x], 1).astype(np.float32), t + j * 0.16)
    add(crunch(lv - 4), t + 0.32)


# ---- ep 25 foley ----
def gavel(level=-13):
    """a court gavel: a hard wood knock (two bright modes + a short low body), very short."""
    N_ = int(0.28 * SR); tt = np.arange(N_) / SR; r_ = np.random.default_rng(5)
    x = 0.8 * np.sin(2 * np.pi * 1150 * tt) * np.exp(-tt * 70) + 0.7 * np.sin(2 * np.pi * 620 * tt) * np.exp(-tt * 45) + 0.9 * np.sin(2 * np.pi * 150 * tt) * np.exp(-tt * 22) + 0.4 * r_.normal(0, 1, N_) * np.exp(-tt * 180)
    x = x / (np.abs(x).max() + 1e-9) * db(level); return np.stack([x, x], 1).astype(np.float32)


def sniff(level=-22, dur=0.45):
    """a nose breathing in: band-passed noise that swells and stops."""
    N_ = int(dur * SR); k = np.arange(N_) / N_
    x = signal.sosfilt(signal.butter(2, [900, 4200], "band", fs=SR, output="sos"), np.random.default_rng(6).normal(0, 1, N_)) * k ** 1.5 * (k < 0.92)
    x = x / (np.abs(x).max() + 1e-9) * db(level); return np.stack([x, x], 1).astype(np.float32)


def torch_click(level=-24):
    N_ = int(0.05 * SR); tt = np.arange(N_) / SR; x = np.sin(2 * np.pi * 2600 * tt) * np.exp(-tt * 260) + 0.6 * np.sin(2 * np.pi * 900 * tt) * np.exp(-tt * 200)
    x = x / (np.abs(x).max() + 1e-9) * db(level); return np.stack([x, x], 1).astype(np.float32)


def press(level=-18):
    """a sealing press: a metal clunk + a short pneumatic hiss."""
    N_ = int(0.5 * SR); tt = np.arange(N_) / SR; h_ = signal.sosfilt(signal.butter(2, 3000, "high", fs=SR, output="sos"), np.random.default_rng(8).normal(0, 1, N_))
    x = np.sin(2 * np.pi * 210 * tt) * np.exp(-tt * 24) + 0.5 * np.sin(2 * np.pi * 870 * tt) * np.exp(-tt * 40) + 0.16 * h_ * np.exp(-((tt - 0.16) / 0.1) ** 2)
    x = x / (np.abs(x).max() + 1e-9) * db(level); return np.stack([x, x], 1).astype(np.float32)


# ---- ep 27 foley (the draw-on board + the nap) ----
def pen_draw(level=-30, dur=0.8, seed=7):
    """a marker on paper: band-passed noise with a fast scratchy grain, swells in and out (sync it to a draw_on stroke)."""
    N_ = int(dur * SR); tt = np.arange(N_) / SR; r_ = np.random.default_rng(seed)
    x = signal.sosfilt(signal.butter(2, [2200, 7000], "band", fs=SR, output="sos"), r_.normal(0, 1, N_))
    grain = 0.55 + 0.45 * np.abs(np.sin(2 * np.pi * (11 + 4 * np.sin(tt * 5)) * tt))
    x = x * grain * np.minimum(1, tt / 0.03) * np.clip((dur - tt) / 0.06, 0, 1)
    x = x / (np.abs(x).max() + 1e-9) * db(level); return np.stack([x, x * 0.9], 1).astype(np.float32)


def eraser(level=-28, dur=0.42):
    """an eraser wipe: a soft low-mid rub, two strokes."""
    N_ = int(dur * SR); tt = np.arange(N_) / SR; r_ = np.random.default_rng(9)
    x = signal.sosfilt(signal.butter(2, [400, 2500], "band", fs=SR, output="sos"), r_.normal(0, 1, N_)) * (0.4 + 0.6 * np.abs(np.sin(np.pi * tt / dur * 2)))
    x = x * np.minimum(1, tt / 0.02) * np.clip((dur - tt) / 0.05, 0, 1)
    x = x / (np.abs(x).max() + 1e-9) * db(level); return np.stack([x * 0.9, x], 1).astype(np.float32)


def snore(level=-24, dur=1.6):
    """a cartoon snore: a low buzzy in-breath (rising) then a soft whistle out."""
    N_ = int(dur * SR); tt = np.arange(N_) / SR; r_ = np.random.default_rng(13); h = int(N_ * 0.55)
    f0 = np.concatenate([np.linspace(70, 95, h), np.full(N_ - h, 0)]); ph = 2 * np.pi * np.cumsum(f0) / SR
    buzz_ = signal.sawtooth(ph) * signal.sosfilt(signal.butter(2, 900, "low", fs=SR, output="sos"), 0.5 + 0.5 * r_.normal(0, 1, N_))
    env = np.sin(np.pi * np.clip(tt / (h / SR), 0, 1)) * (tt < h / SR)
    wh = np.sin(2 * np.pi * np.cumsum(np.linspace(1400, 900, N_)) / SR) * np.sin(np.pi * np.clip((tt - h / SR) / (dur - h / SR), 0, 1)) * (tt >= h / SR) * 0.25
    x = buzz_ * env + wh
    x = x / (np.abs(x).max() + 1e-9) * db(level); return np.stack([x, x], 1).astype(np.float32)


def dial_ticks(t0, t1, level=-27, n_=6):
    """a dimmer knob turning: small detent clicks spread from t0 to t1."""
    for j in range(n_): add(click(level), t0 + (t1 - t0) * j / max(1, n_ - 1))


# ---------------- ep 28 (8 Nov) foley: spray (a spit-take), glug (chugging from a bottle), clank (the factory), pour (water filling a tank), belt (conveyor hum) ----------------
def spray(level=-16, dur=0.5):
    """a SPIT-TAKE: a wet lip burst + a hissing spray that fans out and patters down."""
    t2 = np.arange(int(dur * SR)) / SR
    burst = signal.sosfilt(signal.butter(2, [300, 1600], "band", fs=SR, output="sos"), rng.standard_normal(len(t2))) * np.exp(-t2 / 0.02)
    hissn = signal.sosfilt(signal.butter(2, [2500, 9000], "band", fs=SR, output="sos"), rng.standard_normal(len(t2))) * np.exp(-t2 / 0.16) * np.minimum(1, t2 / 0.01)
    pat = np.zeros(len(t2))
    for j in range(14):
        i = int(rng.uniform(0.12, dur - 0.03) * SR); s_ = np.arange(int(0.012 * SR)) / SR; pat[i:i + len(s_)] += np.sin(2 * np.pi * rng.uniform(900, 2200) * s_) * np.exp(-s_ / 0.003) * 0.4
    y = 1.4 * burst + hissn + pat
    return _st(y / (np.abs(y).max() + 1e-9) * db(level))


def glug(level=-22, n=4, gap=0.2):
    """chugging: hollow bottle glugs (a falling resonant bubble each)."""
    L = int((n * gap + 0.2) * SR); y = np.zeros(L)
    for j in range(n):
        i = int(j * gap * SR); t2 = np.arange(int(0.16 * SR)) / SR
        s_ = np.sin(2 * np.pi * np.cumsum(380 - 900 * t2) / SR) * np.exp(-t2 / 0.06) * np.minimum(1, t2 / 0.004)
        y[i:i + len(s_)] += s_[: L - i]
    y = signal.sosfilt(signal.butter(2, [150, 2500], "band", fs=SR, output="sos"), y)
    return _st(y / (np.abs(y).max() + 1e-9) * db(level))


def clank(level=-24, f0=420):
    """a friendly metal clank (the factory on 2 and 4)."""
    t2 = np.arange(int(0.5 * SR)) / SR
    y = sum(a * np.sin(2 * np.pi * f0 * r * t2) * np.exp(-t2 / d) for r, a, d in ((1, 1, 0.08), (2.43, 0.6, 0.06), (3.9, 0.4, 0.04)))
    y += 0.5 * signal.sosfilt(signal.butter(2, [1500, 6000], "band", fs=SR, output="sos"), rng.standard_normal(len(t2))) * np.exp(-t2 / 0.01)
    return _st(y / (np.abs(y).max() + 1e-9) * db(level))


def pour(level=-26, dur=1.6):
    """water pouring into a tank: band noise whose pitch rises as it fills, with a bubbling texture."""
    t2 = np.arange(int(dur * SR)) / SR
    y = rng.standard_normal(len(t2)); out = np.zeros(len(t2)); seg = int(0.05 * SR)
    for i in range(0, len(t2), seg):
        fc = 500 + 1400 * i / len(t2)
        out[i:i + seg] = signal.sosfilt(signal.butter(2, [fc * 0.6, fc * 1.6], "band", fs=SR, output="sos"), y[i:i + seg])
    out *= np.minimum(1, t2 / 0.1) * np.minimum(1, (dur - t2) / 0.2) * (0.8 + 0.2 * np.sin(2 * np.pi * 9 * t2))
    return _st(out / (np.abs(out).max() + 1e-9) * db(level))


def belt(level=-32, dur=2.0):
    """a soft conveyor hum: low motor + rhythmic roller ticks."""
    t2 = np.arange(int(dur * SR)) / SR
    y = 0.6 * np.sin(2 * np.pi * 60 * t2) + 0.3 * np.sin(2 * np.pi * 120 * t2)
    y += 0.3 * signal.sosfilt(signal.butter(2, [200, 900], "band", fs=SR, output="sos"), rng.standard_normal(len(t2)))
    y *= 0.8 + 0.2 * (np.sin(2 * np.pi * 4 * t2) > 0.9)
    y *= np.minimum(1, t2 / 0.2) * np.minimum(1, (dur - t2) / 0.3)
    return _st(y / (np.abs(y).max() + 1e-9) * db(level))


# ---- ep 31 (10 Nov): SOUND DESIGN WITHOUT A MUSIC BED (owner 9 Nov: no score; he adds a track in-app at 50-60).
# Layered hits = SUB + BODY (loudest) + TRANSIENT + TAIL with aligned transients (Morphic 'How to layer sound effects'; Violet Recording 2026);
# room tone per place, low and ducked under the voice (Morphic 'Sound design basics': 'if the ambience is too loud, dialogue gets buried');
# a ~0.25 s DROP-OUT (-15 dB) of room tone + foley before the 4-5 biggest moments (Sound On Sound 2013: 'a beat of silence just before the impact');
# save the big sounds for the big moments. See episodes/31-salty-snacks-thirst/mix.py for the full pattern (PLACE map, LVL, dip).
def _st2(y): return np.stack([y, y * 0.96], 1).astype(np.float32)


def _bp(x, lo, hi): return signal.sosfilt(signal.butter(2, [lo, hi], "band", fs=SR, output="sos"), x)


def _hp(x, f0): return signal.sosfilt(signal.butter(2, f0, "high", fs=SR, output="sos"), x)


def _lp(x, f0): return signal.sosfilt(signal.butter(2, f0, "low", fs=SR, output="sos"), x)


# ---------------- the layered hit (ep 31 skill) ----------------
def layered_hit(t, level=-14, sub_f=(90, 42), body=(180, 1400), tail=1.0, bright=1.0):
    """4 layers, transients on the same sample: SUB (falling sine) + BODY (band thump, loudest) + TRANSIENT (click, -8 dB) + TAIL (filtered decay, -14 dB)."""
    n_ = int((tail + 0.4) * SR); tt = np.arange(n_) / SR
    fr = sub_f[1] + (sub_f[0] - sub_f[1]) * np.exp(-tt / 0.08)
    sub = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-tt / 0.32) * np.minimum(1, tt / 0.002)
    bd = _hp(_bp(rng.standard_normal(n_), *body), 150) * np.exp(-tt / 0.07) * np.minimum(1, tt / 0.001)
    bd = bd / (np.abs(bd).max() + 1e-9)
    tr = _hp(rng.standard_normal(n_), 2500) * np.exp(-tt / 0.006); tr = tr / (np.abs(tr).max() + 1e-9)
    tl = _lp(_hp(rng.standard_normal(n_), 300), 3500 * bright) * np.exp(-tt / (tail * 0.35)) * np.minimum(1, tt / 0.02); tl = tl / (np.abs(tl).max() + 1e-9)
    y = 0.8 * sub + 1.0 * bd + db(-8) * tr + db(-14) * tl
    y = y / (np.abs(y).max() + 1e-9) * db(level)
    st = np.stack([y, np.roll(y, 90) * 0.95], 1).astype(np.float32)               # a hair of width on the tail
    add(st, t)


def bell(level=-22, f0=1760, dur=1.0, rate=18):
    """an alarm bell ringing (struck partials + a fast hammer tremolo)."""
    n_ = int(dur * SR); tt = np.arange(n_) / SR
    x = sum(a * np.sin(2 * np.pi * f0 * m * tt) for m, a in ((1, 1), (2.76, 0.5), (5.4, 0.25)))
    x *= (0.55 + 0.45 * np.abs(np.sin(np.pi * rate * tt))) * np.minimum(1, tt / 0.005) * np.clip((dur - tt) / 0.15, 0, 1)
    return _st2(x / (np.abs(x).max() + 1e-9) * db(level))


def shaker_rattle(level=-26, dur=0.8, rate=9):
    n_ = int(dur * SR); tt = np.arange(n_) / SR
    x = _bp(rng.standard_normal(n_), 3000, 9000) * np.abs(np.sin(np.pi * rate * tt)) ** 4
    return _st2(x / (np.abs(x).max() + 1e-9) * db(level) * np.clip((dur - tt) / 0.1, 0, 1))


def tumble(level=-28, dur=1.0):
    """a dry tumbleweed: scratchy brush noise bumping along + a whistle of wind."""
    n_ = int(dur * SR); tt = np.arange(n_) / SR
    x = _bp(rng.standard_normal(n_), 1500, 6000) * (0.3 + 0.7 * np.abs(np.sin(2 * np.pi * 4.5 * tt)) ** 3)
    w = np.sin(2 * np.pi * (700 + 200 * np.sin(2 * np.pi * 0.7 * tt)) * tt) * 0.15
    y = (x / (np.abs(x).max() + 1e-9) + w) * np.sin(np.pi * tt / dur)
    return _st2(y / (np.abs(y).max() + 1e-9) * db(level))


def drain(level=-24, dur=1.2):
    """a battery draining: a falling square-ish tone that slows down."""
    n_ = int(dur * SR); tt = np.arange(n_) / SR; fr = 600 * np.exp(-tt * 1.4) + 90
    y = np.sign(np.sin(2 * np.pi * np.cumsum(fr) / SR)) * 0.4 * np.exp(-tt / dur)
    return _st2(_lp(y, 2500) / 0.4 * db(level))


def magnet_zing(level=-26, dur=0.6):
    n_ = int(dur * SR); tt = np.arange(n_) / SR; fr = 300 + 900 * tt / dur
    y = np.sin(2 * np.pi * np.cumsum(fr) / SR) * (0.6 + 0.4 * np.sin(2 * np.pi * 30 * tt)) * np.sin(np.pi * tt / dur)
    return _st2(y * db(level))


def deflate(level=-24, dur=0.7):
    """shrinking cells: a little falling 'wheee' + air."""
    n_ = int(dur * SR); tt = np.arange(n_) / SR; fr = 900 * np.exp(-tt * 2.5) + 180
    y = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-tt / dur) + 0.3 * _bp(rng.standard_normal(n_), 800, 3000) * np.exp(-tt / 0.2)
    return _st2(y / (np.abs(y).max() + 1e-9) * db(level))


def waves(level=-30, dur=3.0):
    n_ = int(dur * SR); tt = np.arange(n_) / SR
    x = _lp(rng.standard_normal(n_), 1400) * (0.35 + 0.65 * np.sin(np.pi * ((tt / 2.2) % 1)) ** 2)
    return _st2(x / (np.abs(x).max() + 1e-9) * db(level) * np.minimum(1, np.minimum(tt / 0.4, (dur - tt) / 0.4)))


def hatch_hiss(level=-26, dur=0.9):
    n_ = int(dur * SR); tt = np.arange(n_) / SR
    x = _hp(rng.standard_normal(n_), 2000) * np.exp(-tt / 0.35) + 0.5 * np.sin(2 * np.pi * 70 * tt) * np.exp(-tt / 0.08)
    return _st2(x / (np.abs(x).max() + 1e-9) * db(level))



# room_tone(kind, n_): 'tv' (hiss + mains hum) | 'cap' (air handling) | 'kit' (kitchen) | 'sea' (waves) | anything else = the board's quiet paper room.
# Suggested levels (dBFS before loudnorm): tv -44, cap -42, kit -46, sea -38, board -52; multiply by (1 - 0.5 * g) to duck under the voice.
def room_tone(kind, n_):
    tt = np.arange(n_) / SR; w = rng.standard_normal(n_)
    if kind == "tv":   x = _lp(w, 2500) * 0.5 + 0.25 * np.sin(2 * np.pi * 60 * tt) + _bp(rng.standard_normal(n_), 4000, 9000) * 0.08 * (rng.random(n_) < 0.02)
    elif kind == "cap": x = _lp(w, 700) * 0.8 + 0.35 * np.sin(2 * np.pi * 120 * tt) * (0.8 + 0.2 * np.sin(2 * np.pi * 0.3 * tt))
    elif kind == "kit": x = _lp(w, 1800) * 0.4 + 0.2 * np.sin(2 * np.pi * 100 * tt)
    elif kind == "sea": x = _lp(w, 1200) * (0.4 + 0.6 * np.sin(np.pi * ((tt / 2.2) % 1)) ** 2)
    else:              x = _bp(w, 200, 2500) * 0.3                                    # the board: a quiet paper room
    return x / (np.abs(x).max() + 1e-9)

# ================= ep 33: PUT THE FOLEY IN THE ROOM (craft skill) =================
# place(x, t, xpos, gain, far, where) = pan the dry effect to its on-screen x (equal power, +-0.55 max; the voice stays centred) and send it to the
# reverb of the PLACE it happens in; at the end of mix.py call reverb_returns() once. Set PLACE = {shot_id: 'kit'|'stove'|'stadium'|'board'} (board = dry)
# and define place_at(t) (see episodes/33-vitamin-c-league/mix.py). Sources: Designing Sound 'Panning reverb returns' (2012); Production Expert
# 'How to use reverb in drama production'; Krotos 'How to pan spatial audio'. Rooms: kit 8 ms / 0.35 s, stove 0.45 s, stadium = 140 + 260 ms slap-back +
# a 1.4 s darker tail. Add a new room spec in ir() for a new place.
from scipy.signal import fftconvolve


def place_at(t): return "board"


def ir(kind):
    """a synthetic stereo impulse response per place: early reflections (taps) + a diffuse decaying noise tail; L/R decorrelated."""
    spec = {"kit": dict(pre=0.008, rt=0.35, taps=((0.011, 0.5), (0.019, 0.35), (0.027, 0.25)), lp=6000),
            "stove": dict(pre=0.008, rt=0.45, taps=((0.012, 0.5), (0.021, 0.35), (0.031, 0.25)), lp=5000),
            "stadium": dict(pre=0.03, rt=1.4, taps=((0.14, 0.45), (0.26, 0.28), (0.39, 0.14)), lp=2800)}[kind]
    n_ = int((spec["pre"] + spec["rt"] * 1.2) * SR); out = np.zeros((n_, 2), np.float32)
    tt = np.arange(n_) / SR
    for ch in range(2):
        r = np.random.default_rng(100 + ch + len(kind))
        tail = r.standard_normal(n_) * np.exp(-6.9 * np.maximum(0, tt - spec["pre"]) / spec["rt"]) * (tt >= spec["pre"])
        tail = signal.sosfilt(signal.butter(2, spec["lp"], "low", fs=SR, output="sos"), tail)
        tail = tail / (np.sqrt(np.sum(tail ** 2)) + 1e-9) * 0.6
        for d_, a_ in spec["taps"]:
            k = int((d_ + 0.004 * ch) * SR)
            if k < n_: tail[k] += a_
        out[:, ch] = tail
    return out


WET = {"kit": -13, "stove": -11, "stadium": -10, "board": None}
BUS = {k: np.zeros((NS, 2), np.float32) for k in ("kit", "stove", "stadium")}


def place(x, t, xpos=540, gain=1.0, far=0.0, where=None):
    """add an effect at time t, panned to its on-screen x, sent to the reverb of the place it happens in (far 0..1 = more wet, less dry)."""
    i = int(t * SR)
    if i < 0: x = x[-i:]; i = 0
    j = min(NS, i + len(x))
    if j <= i: return
    m = x[: j - i].mean(1) if x.ndim == 2 else x[: j - i]
    p = clamp((xpos - 540) / 540, -1, 1) * 0.55                                     # equal-power pan, max +-0.55 of the width
    th = (p + 1) * math.pi / 4
    dry = 1.0 - 0.45 * far
    sfx[i:j, 0] += m * math.cos(th) * math.sqrt(2) * gain * dry
    sfx[i:j, 1] += m * math.sin(th) * math.sqrt(2) * gain * dry
    kind = where or place_at(t)
    if WET.get(kind) is not None: BUS[kind][i:j] += (m * gain * db(WET[kind]) * (1 + 1.5 * far))[:, None]


def mono(y): return np.stack([y, y], 1).astype(np.float32)


def whistle_blow(level=-20, dur=0.5):
    """a referee's pea whistle: a ~2.6 kHz tone with a fast warble (the pea) + breath noise."""
    n_ = int(dur * SR); tt = np.arange(n_) / SR
    fr = 2600 + 120 * np.sin(2 * np.pi * 34 * tt)
    y = np.sin(2 * np.pi * np.cumsum(fr) / SR) * (0.75 + 0.25 * np.sign(np.sin(2 * np.pi * 34 * tt))) + 0.15 * _bp(rng.standard_normal(n_), 2000, 6000)
    y *= np.minimum(1, tt / 0.02) * np.clip((dur - tt) / 0.05, 0, 1)
    return mono(y / (np.abs(y).max() + 1e-9) * db(level))


def crowd(level=-26, dur=2.0, cheer=0.0):
    """a stadium crowd: band-limited murmur; cheer 0..1 swells into a roar."""
    n_ = int(dur * SR); tt = np.arange(n_) / SR
    x = _bp(rng.standard_normal(n_), 300, 3000) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.7 * tt) ** 2)
    if cheer > 0: x = x * (1 + 3 * cheer * np.minimum(1, tt / 0.25) * np.exp(-np.maximum(0, tt - 0.6) / (dur * 0.5)))
    x *= np.minimum(1, tt / 0.1) * np.clip((dur - tt) / 0.3, 0, 1)
    return mono(x / (np.abs(x).max() + 1e-9) * db(level))


def drumroll(level=-24, dur=1.5):
    n_ = int(max(0.3, dur) * SR); tt = np.arange(n_) / SR
    hits = (np.sin(2 * np.pi * 14 * tt) > 0.9).astype(np.float32)
    x = _bp(rng.standard_normal(n_), 200, 5000) * np.convolve(hits, np.exp(-np.arange(400) / 80), "same")
    x *= (0.4 + 0.6 * tt / tt[-1])
    return mono(x / (np.abs(x).max() + 1e-9) * db(level))


def boing_up(level=-22, f0=260, dur=0.4):
    n_ = int(dur * SR); tt = np.arange(n_) / SR; fr = f0 * (1 + 1.6 * tt / dur) * (1 + 0.06 * np.sin(2 * np.pi * 18 * tt))
    return mono(np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-tt / (dur * 0.7)) * np.minimum(1, tt / 0.004) * db(level))


def mat_land(level=-18):
    n_ = int(0.45 * SR); tt = np.arange(n_) / SR
    y = _lp(rng.standard_normal(n_), 500) * np.exp(-tt / 0.08) * 1.5 + np.sin(2 * np.pi * 70 * tt) * np.exp(-tt / 0.12)
    return mono(y / (np.abs(y).max() + 1e-9) * db(level))


def bar_rattle(level=-24):
    n_ = int(0.6 * SR); tt = np.arange(n_) / SR
    y = sum(np.sin(2 * np.pi * f_ * tt) * a_ for f_, a_ in ((620, 1), (1490, 0.5), (2710, 0.3))) * np.exp(-tt / 0.18) * (0.6 + 0.4 * np.sin(2 * np.pi * 22 * tt))
    return mono(y / (np.abs(y).max() + 1e-9) * db(level))


def sneeze(level=-20):
    n_ = int(0.6 * SR); tt = np.arange(n_) / SR
    y = _bp(rng.standard_normal(n_), 800, 3000) * np.clip(tt / 0.3, 0, 1) * (tt < 0.32) * 0.3 + _bp(rng.standard_normal(n_), 600, 6000) * np.exp(-np.maximum(0, tt - 0.34) / 0.08) * (tt >= 0.34)
    return mono(y / (np.abs(y).max() + 1e-9) * db(level))


def boil(level=-28, dur=3.0):
    n_ = int(dur * SR); tt = np.arange(n_) / SR; y = np.zeros(n_)
    for k in range(int(dur * 22)):
        p = int(rng.uniform(0, n_ - 2000)); f_ = rng.uniform(300, 900); m_ = np.arange(1500) / SR
        y[p:p + 1500] += np.sin(2 * np.pi * f_ * (1 + 3 * m_) * m_) * np.exp(-m_ / 0.01) * rng.uniform(0.3, 1)
    y += 0.3 * _lp(rng.standard_normal(n_), 1500)
    y *= np.minimum(1, tt / 0.2) * np.clip((dur - tt) / 0.3, 0, 1)
    return mono(y / (np.abs(y).max() + 1e-9) * db(level))




def reverb_returns():
    """convolve each place bus with its room and add the wide returns to sfx (call once, after all place() calls)."""
    global sfx
    for kind, bus in BUS.items():
        if np.abs(bus).max() < 1e-7: continue
        h = ir(kind); wet = np.zeros_like(bus)
        for ch in range(2): wet[:, ch] = fftconvolve(bus[:, ch], h[:, ch])[:NS]
        sfx += wet.astype(np.float32)
