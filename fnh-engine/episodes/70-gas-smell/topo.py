"""minimal TopoJSON decoder -> {name: [rings of (lon,lat)]}"""
import json, numpy as np
def load(path, obj):
    d = json.load(open(path)); tr = d.get('transform'); arcs = []
    for a in d['arcs']:
        a = np.array(a, float)
        if tr: a = np.cumsum(a, 0) * tr['scale'] + tr['translate']
        arcs.append(a)
    def arc(i): return arcs[i] if i >= 0 else arcs[~i][::-1]
    def ring(r): return np.concatenate([arc(i) for i in r])
    out = {}
    for g in d['objects'][obj]['geometries']:
        nm = (g.get('properties') or {}).get('name', str(g.get('id'))); rs = []
        if g['type'] == 'Polygon': rs = [ring(r) for r in g['arcs']]
        elif g['type'] == 'MultiPolygon': rs = [ring(r) for p in g['arcs'] for r in p]
        out.setdefault(nm, []).extend(rs)
    return out
