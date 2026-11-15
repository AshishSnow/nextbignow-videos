def frame(T):
    fr = np.zeros((H, W, 3), np.uint8)
    if T >= BRAND0:
        sc_brand(fr, T, T - BRAND0)
    else:
        l = TL[0]
        for x in TL:
            if x['start'] <= T: l = x
        t = T - l['start']
        SCENES[l['id']](fr, T, t, l)
        # whip-in on scene change (not between hook parts)
        if 0 <= t < .14 and l['id'] != 'h1':
            k = 1 - t / .14; sh = int(k * 120); fr[:] = np.roll(fr, sh, axis=1)
            fr[:] = (fr * (1 - .35 * k) + 255 * .35 * k).astype(np.uint8)
        subtitle(fr, T)
    overlay(fr, LOGO)
    put_rgba(fr, logo_word(), 112 + 200, 316, 1.0, 1.0, -2)
    if T < BRAND0: put_rgba(fr, credit_img(CREDIT), 30, 960, 1.0, 1.0, 0)
    return fr

def seg(i0, i1):
    os.makedirs(D + '/segs', exist_ok=True)
    f0, f1 = int(i0 * FPS), int(min(i1, TOTAL) * FPS)
    tmp = f'{D}/segs/seg_{i0:05.1f}.tmp.mp4'
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
    for fi in range(f0, f1): p.stdin.write(frame(fi / FPS).tobytes())
    p.stdin.close(); p.wait(); os.rename(tmp, tmp.replace('.tmp', ''))

if __name__ == '__main__':
    if sys.argv[1] == 'stills':
        for a in sys.argv[2:]:
            T = float(a); Image.fromarray(frame(T)).save(f'/tmp/cs_{a}.png')
    elif sys.argv[1] == 'seg':
        seg(float(sys.argv[2]), float(sys.argv[3]))
    elif sys.argv[1] == 'total':
        print(TOTAL)
