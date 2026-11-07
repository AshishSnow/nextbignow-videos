"""Motion test B: 3D toy / clay, 10.5 s of the Coca-Cola hook. Eevee (software GL), rendered on twos (12 fps held to 24) like stop-motion clay.
Usage: python3 anim3d.py OUTDIR [first last]  -> OUTDIR/f_####.png (12 fps frame numbers)"""
import bpy, math, sys, os, time, wave
import numpy as np
from mathutils import Vector

OUTD = sys.argv[1]; os.makedirs(OUTD, exist_ok=True)
HERE = os.path.dirname(os.path.abspath(__file__)); FONT = "/home/claude/studio/fonts/ttf/RubikMonoOne.ttf"
FPS = 12; DUR = 10.6; SPLIT = 4.6
RANGE = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (0, int(DUR * FPS))

# mouth from the voice track (RMS per 1/12 s)
with wave.open("/home/claude/studio/projects/coke-dollar/work/mix.wav") as wf:
    sr = wf.getframerate(); ch = wf.getnchannels(); a = np.frombuffer(wf.readframes(int(sr * DUR) + sr), np.int16).astype(np.float32)
a = a.reshape(-1, ch).mean(1) / 32768; hop = sr // FPS
RMS = np.array([np.sqrt(np.mean(a[i * hop:(i + 1) * hop] ** 2) + 1e-9) for i in range(len(a) // hop)]); RMS = np.clip(RMS / np.percentile(RMS, 95), 0, 1)


def srgb(r, g, b): return tuple(((x / 255) ** 2.2) for x in (r, g, b))


def mat(name, col, rough=0.55, sss=0.0, metal=0.0, trans=0.0, ior=1.45, coat=0.0, emit=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*col, 1); b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal
    b.inputs["Subsurface Weight"].default_value = sss; b.inputs["Transmission Weight"].default_value = trans; b.inputs["IOR"].default_value = ior
    b.inputs["Coat Weight"].default_value = coat
    if emit: b.inputs["Emission Color"].default_value = (*col, 1); b.inputs["Emission Strength"].default_value = emit
    return m


def add(o, m): o.data.materials.append(m); return o


def sphere(loc, r, m, scale=(1, 1, 1), parent=None):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=40, ring_count=20); o = bpy.context.object; o.scale = scale
    for p in o.data.polygons: p.use_smooth = True
    add(o, m)
    if parent: par(o, parent)
    return o


def capsule(a, b, r, m, parent=None):
    a, b = Vector(a), Vector(b); d = b - a
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d.length, location=(a + b) / 2, vertices=28); o = bpy.context.object
    o.rotation_mode = "QUATERNION"; o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d)
    for p in o.data.polygons: p.use_smooth = True
    add(o, m); objs = [o, sphere(a, r, m), sphere(b, r, m)]
    if parent: [par(x, parent) for x in objs]
    return objs


def empty(loc, parent=None):
    e = bpy.data.objects.new("e", None); bpy.context.collection.objects.link(e); e.location = loc
    if parent: par(e, parent)
    return e


def par(o, p):
    bpy.context.view_layer.update()
    mw = o.matrix_world.copy(); o.parent = p; o.matrix_parent_inverse = p.matrix_world.inverted(); o.matrix_world = mw


def text3d(s, loc, size, m, ext=0.12):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90), 0, 0)); t = bpy.context.object
    t.data.body = s; t.data.font = bpy.data.fonts.load(FONT); t.data.size = size; t.data.extrude = ext; t.data.bevel_depth = 0.03
    t.data.align_x = "CENTER"; t.data.align_y = "CENTER"; t.data.materials.append(m); return t


def area(loc, rot, size, power, col):
    bpy.ops.object.light_add(type="AREA", location=loc, rotation=rot); l = bpy.context.object; l.data.size = size; l.data.energy = power; l.data.color = col; return l


def setup(bgcol, disc):
    bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
    sc.render.engine = "BLENDER_EEVEE"; sc.eevee.taa_render_samples = 8
    sc.render.resolution_x, sc.render.resolution_y = 810, 1440
    sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "AgX - Punchy"
    w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (*srgb(255, 210, 150), 1); w.node_tree.nodes["Background"].inputs[1].default_value = 0.45
    bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 0, 0)); add(bpy.context.object, mat("floor", srgb(*bgcol), 0.7))
    bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 9, 10), rotation=(math.radians(90), 0, 0)); add(bpy.context.object, mat("wall", srgb(*bgcol), 0.7))
    if disc:
        bpy.ops.mesh.primitive_cylinder_add(radius=3.3, depth=0.3, location=(0.3, 8.6, 4.7), rotation=(math.radians(90), 0, 0), vertices=96)
        add(bpy.context.object, mat("disc", srgb(*disc), 0.35, coat=0.3))
        bpy.ops.mesh.primitive_torus_add(major_radius=3.3, minor_radius=0.18, location=(0.3, 8.45, 4.7), rotation=(math.radians(90), 0, 0))
        add(bpy.context.object, mat("ring", srgb(255, 120, 30), 0.3))
    area((-5, -6, 9), (math.radians(55), 0, math.radians(-38)), 6, 2600, (1, 0.93, 0.82))
    area((6, -3, 5), (math.radians(70), 0, math.radians(60)), 4, 900, (0.75, 0.85, 1))
    area((0, 5, 10), (math.radians(-40), 0, 0), 5, 1500, (1, 0.95, 0.9))
    bpy.ops.object.camera_add(location=(0.15, -12.5, 4.9), rotation=(math.radians(88.5), 0, 0)); cam = bpy.context.object; sc.camera = cam; cam.data.lens = 40
    return sc, cam


def guy(X, Y, Z=0.0, jumper=(232, 50, 60)):
    """our own clay guy (not any existing character): parts parented to a root, arms to shoulder pivots"""
    skin = mat("skin", srgb(236, 180, 140), 0.5, sss=0.15); jm = mat("jumper", srgb(*jumper), 0.75); jeans = mat("jeans", srgb(40, 60, 120), 0.8)
    hair = mat("hair", srgb(60, 36, 24), 0.7); white = mat("eyew", (0.95, 0.95, 0.95), 0.2); black = mat("eyeb", (0.01, 0.01, 0.01), 0.2)
    root = empty((X, Y, Z)); R = {"root": root}
    capsule((X - 0.26, Y, Z + 0.35), (X - 0.24, Y, Z + 1.35), 0.22, jeans, root); capsule((X + 0.26, Y, Z + 0.35), (X + 0.24, Y, Z + 1.35), 0.22, jeans, root)
    for sx in (-0.26, 0.26): sphere((X + sx, Y - 0.12, Z + 0.18), 0.26, mat("shoe", srgb(245, 245, 245), 0.6), (1, 1.5, 0.6), root)
    body = empty((X, Y, Z + 1.4), root); R["body"] = body
    sphere((X, Y, Z + 2.05), 0.62, jm, (1, 0.8, 1.25), body)
    for side, sx in (("L", -1), ("R", 1)):
        sh = empty((X + sx * 0.55, Y, Z + 2.45), body); R["sh" + side] = sh
        capsule((X + sx * 0.55, Y, Z + 2.45), (X + sx * 0.75, Y - 0.05, Z + 1.55), 0.17, jm, sh)
        sphere((X + sx * 0.78, Y - 0.05, Z + 1.38), 0.2, skin, parent=sh)
    head = empty((X, Y, Z + 2.9), body); R["head"] = head
    capsule((X, Y, Z + 2.8), (X, Y, Z + 3.0), 0.16, skin, head)
    sphere((X, Y, Z + 3.55), 0.66, skin, (1, 0.95, 1.05), head); sphere((X, Y + 0.08, Z + 4.05), 0.62, hair, (1.05, 1.0, 0.55), head)
    R["eyes"] = []
    for ex in (-0.24, 0.24):
        e = sphere((X + ex, Y - 0.56, Z + 3.68), 0.16, white, (1, 0.6, 1.15), head); R["eyes"].append(e)
        sphere((X + ex, Y - 0.66, Z + 3.66), 0.075, black, parent=head)
    R["mouth"] = sphere((X, Y - 0.58, Z + 3.2), 0.15, mat("mouth", srgb(60, 12, 20), 0.6), (1.4, 0.35, 0.3), head)
    sphere((X - 0.62, Y - 0.1, Z + 3.45), 0.12, skin, parent=head); sphere((X + 0.62, Y - 0.1, Z + 3.45), 0.12, skin, parent=head)
    return R


def ease(x): x = min(1, max(0, x)); return x * x * (3 - 2 * x)


def back(x, s=1.7): x = min(1, max(0, x)); return 1 + (s + 1) * (x - 1) ** 3 + s * (x - 1) ** 2


def pose_guy(R, t, n, arms_up, talk=True, sway=0.0):
    k = RMS[min(n, len(RMS) - 1)] if talk else 0
    R["mouth"].scale = (1.4 - 0.3 * k, 0.35, 0.18 + 0.9 * k)
    bl = 0.12 if (n % 37) in (0, 1) else 1.0
    for e in R["eyes"]: e.scale = (1, 0.6, 1.15 * bl)
    for side, sx in (("L", -1), ("R", 1)):
        R["sh" + side].rotation_euler = (0, sx * math.radians(-150 * arms_up - 8 * math.sin(t * 5 + sx)), 0) if False else (0, -sx * math.radians(150 * arms_up + 6 * math.sin(t * 6 + sx)), 0)
    R["body"].rotation_euler = (0, math.radians(3 * math.sin(t * 2.2) + sway), 0)
    R["head"].rotation_euler = (math.radians(4 * k), math.radians(5 * math.sin(t * 1.7)), 0)


def bill_obj(loc):
    bpy.ops.mesh.primitive_plane_add(size=1, location=loc); b = bpy.context.object; b.scale = (3.4, 1.47, 1)
    bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.subdivide(number_cuts=16); bpy.ops.object.mode_set(mode="OBJECT")
    b.modifiers.new("t", "SOLIDIFY").thickness = 0.02
    bd = b.modifiers.new("b", "SIMPLE_DEFORM"); bd.deform_method = "BEND"; bd.angle = math.radians(28); bd.deform_axis = "Y"
    mb = mat("bill", (1, 1, 1), 0.6); nt = mb.node_tree; tex = nt.nodes.new("ShaderNodeTexImage"); tex.image = bpy.data.images.load(f"{HERE}/bill_tex.png")
    nt.links.new(tex.outputs["Color"], nt.nodes["Principled BSDF"].inputs["Base Color"]); add(b, mb)
    for p in b.data.polygons: p.use_smooth = True
    return b


def bottle(loc, s=1.0):
    prof = [(0.0, 0), (0.42, 0), (0.46, 0.15), (0.46, 1.2), (0.30, 1.75), (0.16, 2.2), (0.17, 2.45), (0.0, 2.45)]
    me = bpy.data.meshes.new("bot"); me.from_pydata([(r * s, 0, z * s) for r, z in prof], [(i, i + 1) for i in range(len(prof) - 1)], [])
    o = bpy.data.objects.new("bot", me); bpy.context.collection.objects.link(o); o.location = loc
    m = o.modifiers.new("s", "SCREW"); m.steps = 48; m.render_steps = 48; m.use_smooth_shade = True
    add(o, mat("glass", srgb(150, 30, 20), 0.08, trans=0.85, ior=1.5))
    bpy.ops.mesh.primitive_cylinder_add(radius=0.475 * s, depth=0.5 * s, location=(loc[0], loc[1], loc[2] + 0.75 * s), vertices=48); lab = bpy.context.object
    add(lab, mat("label", srgb(250, 248, 240), 0.5)); par(lab, o)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.19 * s, depth=0.14 * s, location=(loc[0], loc[1], loc[2] + 2.5 * s), vertices=32); cap = bpy.context.object
    add(cap, mat("cap", srgb(220, 40, 40), 0.3, metal=0.6)); par(cap, o)
    return o


def glass_(loc):
    bpy.ops.mesh.primitive_cone_add(radius1=0.32, radius2=0.42, depth=1.1, location=(loc[0], loc[1], loc[2] + 0.55), vertices=40); g = bpy.context.object
    gm = mat("gl", (0.85, 0.93, 1), 0.05, coat=1.0); gm.node_tree.nodes["Principled BSDF"].inputs["Alpha"].default_value = 0.22
    gm.surface_render_method = "BLENDED"; add(g, gm)
    bpy.ops.mesh.primitive_cone_add(radius1=0.29, radius2=0.37, depth=0.8, location=(loc[0], loc[1], loc[2] + 0.45), vertices=40)
    add(bpy.context.object, mat("cola", srgb(110, 45, 18), 0.12, coat=0.6))
    capsule((loc[0] + 0.1, loc[1], loc[2] + 0.8), (loc[0] + 0.25, loc[1], loc[2] + 1.6), 0.04, mat("straw", srgb(250, 250, 250), 0.4))


# ---------------------------------------------------------------- SHOT 1: the $1 hook (0 – 4.6 s)
def shot1(ns):
    sc, cam = setup((30, 110, 235), (255, 190, 30))
    b = bill_obj((0.6, 2.4, 3.9)); bt = bottle((2.35, 1.2, 0)); G = guy(-1.6, 1.4)
    t1 = text3d("FOR $1", (0.2, 3.2, 7.25), 1.35, mat("t1", srgb(255, 255, 255), 0.25, coat=0.5))
    t2 = text3d("COCA-COLA SOLD", (0.2, 3.3, 8.45), 0.62, mat("t2", srgb(255, 220, 60), 0.3))
    for n in ns:
        t = n / FPS
        k = back((t - 0.15) / 0.6); b.location = (0.6, 2.4, 3.9 + 6 * (1 - ease((t - 0.1) / 0.55)))
        b.rotation_euler = (math.radians(78 + 25 * (1 - ease((t - 0.1) / 0.7))), math.radians(-8 + 4 * math.sin(t * 2)), math.radians(-6 + 30 * (1 - ease((t - 0.1) / 0.7))))
        s2 = back((t - 0.4) / 0.35); t2.scale = (s2, s2, s2); s1 = back((t - 2.2) / 0.35, 2.2); t1.scale = (s1, s1, s1)
        bt.location = (2.35, 1.2, 4 * (1 - back((t - 1.0) / 0.45)))
        pose_guy(G, t, n, arms_up=ease((t - 2.15) / 0.25) * 0.95 + 0.05)
        cam.location = (0.15 + 0.2 * math.sin(t * 0.8), -12.5 + 1.4 * ease(t / 4.6), 4.9)
        yield n


# ---------------------------------------------------------------- SHOT 2: 1899, a soda fountain (4.6 – 10.6 s)
def shot2(ns):
    sc, cam = setup((250, 140, 40), (255, 236, 200))
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0.6, 0.8, 0.95)); ctr = bpy.context.object; ctr.scale = (5.2, 1.6, 1.9)
    bv = ctr.modifiers.new("bv", "BEVEL"); bv.width = 0.12; bv.segments = 4; add(ctr, mat("ctr", srgb(140, 70, 40), 0.45))
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0.6, 0.8, 1.95)); top = bpy.context.object; top.scale = (5.5, 1.8, 0.12)
    top.modifiers.new("bv", "BEVEL").width = 0.04; add(top, mat("marble", srgb(245, 240, 232), 0.2, coat=0.4))
    for i, x in enumerate((-0.6, 1.4, 2.4)):
        pass
    # the fountain: chrome column + two taps
    capsule((0.6, 1.3, 2.0), (0.6, 1.3, 3.6), 0.22, mat("chrome", (0.8, 0.8, 0.85), 0.12, metal=1.0))
    for sx in (-1, 1): capsule((0.6, 1.3, 3.3), (0.6 + sx * 0.6, 1.0, 3.1), 0.08, mat("chrome2", (0.8, 0.8, 0.85), 0.12, metal=1.0))
    G = guy(-1.4, 1.9, 0.0, jumper=(250, 250, 250))       # soda jerk in white, behind the counter
    glasses = []
    for i, x in enumerate((1.6, 2.6)):
        glass_((x, 0.6, 2.01)); glasses.append(x)
    yr = text3d("1899", (0.4, 3.0, 7.3), 1.5, mat("yr", srgb(255, 255, 255), 0.25, coat=0.5), ext=0.18)
    lab = text3d("SODA FOUNTAINS", (0.4, 3.1, 8.6), 0.6, mat("lab", srgb(150, 30, 20), 0.35))
    cam.location = (0.4, -12.0, 5.0)
    objs_glass = [o for o in bpy.data.objects if o.name.startswith(("Cone", "Cyl", "Sphere")) and o.location.z > 2.0 and o.location.x > 1.3]
    for n in ns:
        t = n / FPS - SPLIT
        s = back(t / 0.4, 2.0); yr.scale = (s, s, s); s2 = back((t - 3.2) / 0.35); lab.scale = (s2, s2, s2)
        pose_guy(G, t, n, arms_up=0.35 + 0.25 * max(0, math.sin(t * 3)) * ease((t - 3.0) / 0.3), sway=0)
        cam.location = (0.4 + 0.8 * math.sin(t * 0.35), -12.0 + 0.9 * ease(t / 6), 5.0); cam.rotation_euler = (math.radians(88.5), 0, math.radians(3 * math.sin(t * 0.35)))
        yield n


if __name__ == "__main__":
    a, b = RANGE; allf = list(range(a, b))
    s1 = [n for n in allf if n / FPS < SPLIT]; s2 = [n for n in allf if n / FPS >= SPLIT]
    for gen in ((shot1(s1) if s1 else iter(())), (shot2(s2) if s2 else iter(()))):
        for n in gen:
            sc = bpy.context.scene; sc.render.filepath = f"{OUTD}/f_{n:04d}.png"; t0 = time.time()
            bpy.ops.render.render(write_still=True); print("frame", n, round(time.time() - t0, 1), flush=True)
