"""Render our own generic office chair (no brand design) in Blender Cycles as transparent PNG cut-outs, for the bright explainer sets.
Usage: python3 chair3d.py OUTDIR  -> chair_clean.png, chair_worn.png, chair_side.png, chair_pile.png"""
import bpy, math, sys, os, random
from mathutils import Vector

OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)


def srgb(r, g, b): return tuple(((x / 255) ** 2.2) for x in (r, g, b))


def mat(name, col, rough=0.5, metal=0.0, coat=0.0, noise=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; b = nt.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*col, 1); b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal
    b.inputs["Coat Weight"].default_value = coat
    if noise:   # fabric weave / grime
        tx = nt.nodes.new("ShaderNodeTexNoise"); tx.inputs["Scale"].default_value = 260; mx = nt.nodes.new("ShaderNodeMixRGB"); mx.blend_type = "MULTIPLY"
        mx.inputs["Fac"].default_value = noise; mx.inputs["Color1"].default_value = (*col, 1)
        nt.links.new(tx.outputs["Color"], mx.inputs["Color2"]); nt.links.new(mx.outputs["Color"], b.inputs["Base Color"])
    return m


def rbox(loc, size, m, bevel=0.05, rot=(0, 0, 0), seg=4):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot); o = bpy.context.object; o.scale = size
    bv = o.modifiers.new("b", "BEVEL"); bv.width = bevel; bv.segments = seg
    o.modifiers.new("s", "SUBSURF").levels = 1
    for p in o.data.polygons: p.use_smooth = True
    o.data.materials.append(m); return o


def cyl(a, b, r, m, verts=24):
    a, b = Vector(a), Vector(b); d = b - a
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d.length, location=(a + b) / 2, vertices=verts); o = bpy.context.object
    o.rotation_mode = "QUATERNION"; o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d)
    for p in o.data.polygons: p.use_smooth = True
    o.data.materials.append(m); return o


def sph(loc, r, m):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=24, ring_count=12); o = bpy.context.object
    for p in o.data.polygons: p.use_smooth = True
    o.data.materials.append(m); return o


def chair(x=0, y=0, rz=0.0, fabric=(40, 44, 54), worn=False, tilt=0.0):
    objs = []
    fab = mat("fab", srgb(*fabric), 0.85, noise=0.35 if not worn else 0.8)
    mesh = mat("mesh", srgb(*(int(c * 0.8) for c in fabric)), 0.7, noise=0.5)
    plast = mat("plast", srgb(30, 30, 34) if not worn else srgb(70, 66, 60), 0.45, coat=0.2)
    chrome = mat("chrome", (0.75, 0.75, 0.78), 0.18 if not worn else 0.5, metal=1.0)
    rub = mat("rub", srgb(20, 20, 22), 0.6)
    # five-star base + casters
    for i in range(5):
        a = i * math.tau / 5; e = (math.cos(a) * 0.62, math.sin(a) * 0.62, 0.16)
        objs.append(cyl((0, 0, 0.2), e, 0.05, plast))
        objs.append(sph((e[0], e[1], 0.09), 0.08, rub))
        if worn and i == 2: objs[-1].scale = (1, 1, 0.5)   # a broken wheel
    objs.append(cyl((0, 0, 0.18), (0, 0, 0.62), 0.05, chrome))       # gas lift
    objs.append(cyl((0, 0, 0.55), (0, 0, 0.66), 0.13, plast))
    objs.append(rbox((0, 0, 0.72), (1.0, 0.98, 0.1), plast, 0.04))      # seat pan
    objs.append(rbox((0, -0.02, 0.81), (0.96, 0.94, 0.16), fab, 0.08, seg=6))   # seat cushion, rounded
    bk = rbox((0, 0.5, 1.4), (0.9, 0.1, 1.05), mesh, 0.09, rot=(math.radians(-10), 0, 0), seg=6)  # backrest, curved round the back
    bd = bk.modifiers.new("bend", "SIMPLE_DEFORM"); bd.deform_method = "BEND"; bd.angle = math.radians(-40); bd.deform_axis = "Z"; objs.append(bk)
    fr = rbox((0, 0.56, 1.4), (0.98, 0.06, 1.13), plast, 0.05, rot=(math.radians(-10), 0, 0))
    bd = fr.modifiers.new("bend", "SIMPLE_DEFORM"); bd.deform_method = "BEND"; bd.angle = math.radians(-40); bd.deform_axis = "Z"; objs.append(fr)
    objs.append(rbox((0, 0.42, 1.12), (0.7, 0.08, 0.16), fab, 0.06, rot=(math.radians(-10), 0, 0)))   # lumbar pad
    objs.append(rbox((0, 0.62, 0.85), (0.12, 0.1, 0.4), plast, 0.03))   # spine
    for sx in (-1, 1):   # armrests
        objs.append(cyl((sx * 0.5, 0.05, 0.75), (sx * 0.52, 0.05, 1.0), 0.035, plast))
        objs.append(rbox((sx * 0.52, 0.0, 1.02), (0.1, 0.5, 0.05), plast, 0.03))
    if worn:   # stains and a tear
        st = mat("stain", srgb(120, 100, 80), 0.9)
        for (sx, sy, r) in ((0.15, -0.1, 0.12), (-0.25, 0.15, 0.08)):
            o = rbox((sx, sy, 0.83), (r * 2, r * 1.6, 0.005), st, 0.02); objs.append(o)
    root = bpy.data.objects.new("root", None); bpy.context.collection.objects.link(root)
    for o in objs: o.parent = root
    root.location = (x, y, 0); root.rotation_euler = (tilt, 0, rz)
    return root


def scene(res=(1000, 1000), cam_loc=(2.6, -3.4, 1.9), target=(0, 0, 0.8), lens=50):
    bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
    sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = 48; sc.cycles.use_denoising = True
    sc.render.resolution_x, sc.render.resolution_y = res; sc.render.film_transparent = True
    sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "AgX - Base Contrast"
    w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True; w.node_tree.nodes["Background"].inputs[0].default_value = (1, 0.97, 0.92, 1); w.node_tree.nodes["Background"].inputs[1].default_value = 0.6
    for loc, rot, sz, pw in (((-3, -3, 4), (55, 0, -40), 4, 900), ((3.5, -1, 3), (65, 0, 70), 3, 380), ((0, 3, 4), (-45, 0, 180), 3, 500)):
        bpy.ops.object.light_add(type="AREA", location=loc, rotation=tuple(math.radians(v) for v in rot)); l = bpy.context.object; l.data.size = sz; l.data.energy = pw
    bpy.ops.object.camera_add(location=cam_loc); cam = bpy.context.object; sc.camera = cam; cam.data.lens = lens
    d = Vector(target) - Vector(cam_loc); cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    return sc


def render(name):
    bpy.context.scene.render.filepath = f"{OUT}/{name}.png"; bpy.ops.render.render(write_still=True); print("rendered", name, flush=True)


scene(); chair(rz=math.radians(-28)); render("chair_clean")
scene(); chair(rz=math.radians(25), fabric=(110, 96, 84), worn=True, tilt=math.radians(4)); render("chair_worn")
scene(); chair(rz=math.radians(-28), fabric=(30, 90, 170)); render("chair_blue")
scene(res=(1400, 1000), cam_loc=(4.8, -6.4, 3.6), target=(0, 0, 0.9), lens=45)
random.seed(4); cols = [(40, 44, 54), (110, 96, 84), (30, 90, 170), (150, 40, 50), (60, 60, 64), (90, 110, 80)]
for i in range(11):
    chair(x=random.uniform(-2.2, 2.2), y=random.uniform(-1.4, 1.6), rz=random.uniform(0, math.tau), fabric=random.choice(cols), worn=random.random() < 0.5,
          tilt=random.uniform(-0.15, 0.15))
render("chair_pile")
