# --- FNH logo B (verified-leaf bubble) override
_LBS = cairo.ImageSurface.create_from_png('/home/claude/studio/fnh_logoB_2048.png')
def logo(c, x, y, r):
    s = r / 860.0
    c.save(); c.translate(x - 1003 * s, y - 1004 * s); c.scale(s, s); c.set_source_surface(_LBS, 0, 0); c.get_source().set_filter(cairo.FILTER_BEST); c.paint(); c.restore()
