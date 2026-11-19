import sys; sys.path.insert(0, '/home/claude/glasses'); sys.argv = ['x']
exec(open('/home/claude/glasses/scenes.py').read().split("if __name__")[0])
def thumb():
    fr = np.zeros((H, W, 3), np.uint8); fr[:] = paper(RED, .8); rays(fr, 1.0, 'FFFFFF', .14, cy=1100)
    put_rgba(fr, load_st('handphone', w=700), 330, 1130, 1.0, 1.0, -14)
    xstamp(fr, 330, 1100, 1.0, 1.25)
    put_rgba(fr, load_st('glasses', w=700), 700, 1380, 1.0, 1.0, 8)
    burst(fr, 'BYE!', 860, 980, 1.0, r=130, col=YEL, size=78, rot=10)
    title(fr, 'YOUR PHONE', 520, 1.0, size=150, fill='FFFFFF', rot=-3)
    title(fr, 'IS DONE?!', 700, 1.0, size=190, fill=YEL, rot=-3)
    logo(fr); return fr
im = thumb(); Image.fromarray(im).save('/home/claude/glasses/out/thumb_glasses.jpg', quality=95); print('ok')
