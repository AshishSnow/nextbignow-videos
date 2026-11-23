import sys, os, json, math, subprocess
sys.path.insert(0, '/home/claude/tort')
from kit import *
from PIL import ImageFont, ImageDraw, ImageFilter
CREAM_BG = (236, 228, 214); BLACK_BG = (24, 22, 21); INKC = (28, 22, 20)
ACC = rgb(RED)

def load_lines(d):
    L = json.load(open(d + '/lines.json')); S = [l['start'] for l in L]; E = [l['start'] + l['dur'] for l in L]
    return L, S, E

class Ctx:
    def __init__(self, d, file_no, nslides):
        self.d = d; self.L, self.S, self.E = load_lines(d); self.file_no = file_no; self.n = nslides
        self.END = self.E[-1] + .5
    def wt(self, i, frac): return self.S[i] + self.L[i]['dur'] * frac
    def wf(self, i, word):
        tx = self.L[i]['text'].lower(); k = tx.find(word.lower()); return self.wt(i, max(0, k) / max(1, len(tx)))

_PAPER = {}
def base(dark=False):
    k = dark
    if k not in _PAPER:
        col = np.array(BLACK_BG if dark else CREAM_BG, np.float32)
        fr = np.ones((H, W, 3), np.float32) * col
        rng = np.random.default_rng(1); noise = rng.normal(0, 5 if not dark else 3, (H, W, 1)); fr += noise
        # halftone dots (comic touch)
        yy, xx = np.mgrid[0:H, 0:W]; dots = ((xx % 14 - 7) ** 2 + (yy % 14 - 7) ** 2) < 3.2
        fr[dots] += (-10 if not dark else 7)
        # thin vertical grid lines like the essay reference
        for x in (90, 540, 990):
            fr[:, x:x + 2] += (-14 if not dark else 14)
        _PAPER[k] = np.clip(fr, 0, 255).astype(np.uint8)
    return _PAPER[k].copy()

def font(path, size, bold=False):
    f = ImageFont.truetype(path, size)
    if path == INTER:
        try: f.set_variation_by_name('Bold' if bold else 'Medium')
        except Exception: pass
    return f

_LOGO = None
def logo(fr): pass
def header(fr, cx, slide, T, dark):
    im = Image.new('RGBA', (W, 120), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    c = (190, 182, 170, 255) if dark else (110, 100, 90, 255)
    f = font(INTER, 26, True)
    d.text((160, 40), f'NEXTBIGNOW  —  FILE {cx.file_no:02d}', font=f, fill=c)
    d.text((990, 40), f'{slide:02d} / {cx.n:02d}', font=f, fill=c, anchor='ra')
    d.line((90, 88, 990, 88), fill=c[:3] + (90,), width=2)
    prog = clamp(T / cx.END); d.line((90, 88, 90 + 900 * prog, 88), fill=ACC + (255,), width=5)
    put_rgba(fr, np.array(im), CX, 290, 1.0, 1.0, 0)
    global _LOGO
    if _LOGO is None:
        lg = Image.open('/home/claude/nextbignow-videos/NextBigNow_logo_transparent.png').convert('RGBA'); lg.thumbnail((64, 64)); _LOGO = np.array(lg)
    put_rgba(fr, _LOGO, 118, 287, 1.0, 1.0, 0)

def headline(fr, lines, T, t0s, y=390, dark=False, size=128):
    """lines: list of (text, style) style in {'main','grey','hl'}; appears per t0s with slide-up."""
    f = font(ANTON, size); lh = int(size * 1.02); yy = y
    for (txt, sty), t0 in zip(lines, t0s):
        if T < t0: yy += lh; continue
        u = eout(clamp((T - t0) / .28))
        bb = f.getbbox(txt); w = bb[2] - bb[0] + 40; h = lh + 10
        im = Image.new('RGBA', (w + 20, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        if sty == 'hl':
            pw = (w - 10) * eout(clamp((T - t0) / .35))
            d.rectangle((4, int(size * .1), 4 + pw, int(size * 1.12)), fill=ACC + (255,))
            col = (255, 248, 236)
        elif sty == 'grey': col = (120, 112, 104) if not dark else (110, 104, 98)
        else: col = (245, 238, 226) if dark else INKC
        d.text((16, -int(size * .08)), txt, font=f, fill=col + (255,))
        a = np.array(im); a[..., 3] = (a[..., 3] * u).astype(np.uint8)
        put_rgba(fr, a, 90 + (w + 20) / 2, yy + h / 2 + 30 * (1 - u), 1.0, 1.0, 0)
        yy += lh
    return yy

def small(fr, txt, x, y, T, t0, dark=False, col=None, size=40, center=False):
    if T < t0: return
    u = eout(clamp((T - t0) / .3)); f = font(INTER, size, True); bb = f.getbbox(txt)
    im = Image.new('RGBA', (bb[2] + 20, bb[3] + 16), (0, 0, 0, 0))
    c = col or ((235, 228, 216) if dark else INKC)
    ImageDraw.Draw(im).text((8, 4), txt, font=f, fill=tuple(c) + (255,))
    a = np.array(im); a[..., 3] = (a[..., 3] * u).astype(np.uint8)
    cx = x if center else x + (bb[2] + 20) / 2
    put_rgba(fr, a, cx, y + 16 * (1 - u), 1.0, 1.0, 0)

def pill(fr, cx, T, dark=False):
    """small rounded subtitle pill, 2-3 words, current word in accent colour"""
    for i, l in enumerate(cx.L):
        if cx.S[i] - .05 <= T < cx.E[i] + .1:
            words = l['text'].split(); tx = l['text']; pos = []; p = 0
            for w_ in words: k = tx.find(w_, p); pos.append(k / len(tx)); p = k + len(w_)
            cur = max([j for j in range(len(words)) if cx.wt(i, pos[j]) <= T] or [0])
            g0 = (cur // 3) * 3; grp = words[g0:g0 + 3]
            f = font(INTER, 30, True); txt = ' '.join(grp); bb = f.getbbox(txt)
            w = bb[2] - bb[0] + 56; h = 58
            im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
            fill = (44, 40, 38, 235) if dark else (250, 246, 238, 245); out = (90, 84, 78, 255) if dark else (60, 52, 46, 255)
            d.rounded_rectangle((1, 1, w - 2, h - 2), radius=29, fill=fill, outline=out, width=2)
            x = 28
            for j, w_ in enumerate(grp):
                c = ACC if g0 + j == cur else ((235, 228, 216) if dark else INKC)
                d.text((x, h / 2), w_, font=f, fill=c + (255,), anchor='lm'); x += f.getbbox(w_ + ' ')[2]
            put_rgba(fr, np.array(im), CX, 1452, 1.0, 1.0, 0)
            return

def cut(fr, rgba, x, y, T, t0=0.0, sc=1.0, rot=0.0, bob=6, glow=False):
    if rgba is None or T < t0: return
    u = back(clamp((T - t0) / .35))
    im = glow_outline(rgba, 14, (255, 255, 255)) if glow else rgba
    put_rgba(fr, im, x, y + bob * math.sin(T * 2.2), sc * u, 1.0, rot)

def sfx_mix(d, events, total):
    lib = '/home/claude/nextbignow-videos/sfx-library/mixkit'
    inputs = ['-i', f'{d}/vo.wav']; filt = []; k = 1
    for t, sid, g in events:
        p = f'{lib}/mk_{sid}.mp3'
        if not os.path.exists(p) or t < 0: continue
        inputs += ['-i', p]; filt.append(f'[{k}:a]volume={g},adelay={int(t*1000)}|{int(t*1000)}[s{k}]'); k += 1
    mix = ''.join(f'[s{j}]' for j in range(1, k))
    fc = ';'.join(filt) + (';' if filt else '') + f'{mix}amix=inputs={k-1}:normalize=0[fx];[fx][0:a]sidechaincompress=threshold=0.05:ratio=4:release=200[duck];[0:a][duck]amix=inputs=2:normalize=0,apad,atrim=0:{total},loudnorm=I=-14:TP=-1.5[out]'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error'] + inputs + ['-filter_complex', fc, '-map', '[out]', '-ar', '48000', f'{d}/mix.wav'], check=True)

def render(d, frame_fn, total, out):
    n = int(math.ceil(total * 30))
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '30', '-i', '-',
                          '-i', f'{d}/mix.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', '-pix_fmt', 'yuv420p',
                          '-c:a', 'aac', '-b:a', '320k', '-shortest', out + '.tmp.mp4'], stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(frame_fn(i / 30).tobytes())
    p.stdin.close(); p.wait(); os.replace(out + '.tmp.mp4', out)

# ---------------- v2: full-episode helpers ----------------
def cta(fr_unused, T, t0, plat, ig_line, cx):
    fr = base(True); header(fr, cx, cx.n, T, True)
    if plat == 'ig':
        headline(fr, [('SEND THIS TO', 'main'), (ig_line, 'hl')], T, [t0, t0 + .25], dark=True, size=120)
        small(fr, 'Follow @nextbignow for what happens next', 90, 760, T, t0 + .5, True, col=rgb(YEL), size=34)
    else:
        headline(fr, [('SUBSCRIBE', 'hl'), ('FOR WHAT', 'main'), ('HAPPENS NEXT.', 'main')], T, [t0, t0 + .2, t0 + .35], dark=True, size=130)
    burst(fr, 'NEXT BIG NOW', 760, 1150, T - t0 - .3, r=150, col=RED, size=40, rot=8)
    return fr

def thumb(path, lines, cut_rgba, cut_xy=(CX, 1180), burst_txt=None, dark=False, extra=None):
    fr = base(dark); rays(fr, 0.4, 'FFFFFF' if not dark else '444444', .08, CX, 1200)
    headline(fr, lines, 9, [0] * len(lines), y=330, dark=dark, size=150)
    if extra: extra(fr)
    if cut_rgba is not None: put_rgba(fr, glow_outline(cut_rgba, 16, (255, 255, 255)), cut_xy[0], cut_xy[1], 1.0, 1.0, -3)
    if burst_txt: burst(fr, burst_txt, 820, 1560, 1.0, r=140, col=YEL, size=40, rot=8)
    lg = Image.open('/home/claude/nextbignow-videos/NextBigNow_logo_transparent.png').convert('RGBA'); lg.thumbnail((120, 120))
    put_rgba(fr, np.array(lg), 950, 230, 1.0, 1.0, 0)
    Image.fromarray(fr).save(path, quality=95); return fr

def render2(d, frame_fn, cx, plat, out, thumb_fr=None, ig_line='A FRIEND.', cta_len=1.6):
    total = cx.END + cta_len
    n = int(math.ceil(total * 30))
    vf = ['-vf', 'scale=1440:2560:flags=lanczos'] if plat == 'yt' else []
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '30', '-i', '-',
                          '-i', f'{d}/mix.wav', '-map', '0:v', '-map', '1:a'] + vf + ['-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', '-pix_fmt', 'yuv420p',
                          '-c:a', 'aac', '-b:a', '320k', '-shortest', out + '.tmp.mp4'], stdin=subprocess.PIPE)
    for i in range(n):
        T = i / 30
        if plat == 'yt' and thumb_fr is not None and i < 9: fr = thumb_fr
        elif T >= cx.END: fr = cta(None, T, cx.END, plat, ig_line, cx)
        else: fr = frame_fn(T)
        p.stdin.write(fr.tobytes())
    p.stdin.close(); p.wait(); os.replace(out + '.tmp.mp4', out)
