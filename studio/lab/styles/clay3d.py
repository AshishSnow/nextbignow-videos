"""Style test B: 3D CLAY / toy-studio look (Blender Cycles, CPU). One frame of the Coca-Cola hook.
Usage: python3 clay3d.py out.png [samples]"""
import bpy, math, sys, os, time
from mathutils import Vector

OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/studio/lab/styles/clay3d.png"
SPP = int(sys.argv[2]) if len(sys.argv) > 2 else 48
HERE = os.path.dirname(os.path.abspath(__file__))
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene


def mat(name, col, rough=0.55, sss=0.0, metal=0.0, trans=0.0, ior=1.45, coat=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*col, 1); b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal
    b.inputs["Subsurface Weight"].default_value = sss; b.inputs["Subsurface Radius"].default_value = (0.3, 0.15, 0.1)
    b.inputs["Transmission Weight"].default_value = trans; b.inputs["IOR"].default_value = ior; b.inputs["Coat Weight"].default_value = coat
    return m


def srgb(r, g, b): return tuple(((x / 255) ** 2.2) for x in (r, g, b))


def obj_smooth(o, lv=2):
    m = o.modifiers.new("sub", "SUBSURF"); m.levels = lv; m.render_levels = lv
    for p in o.data.polygons: p.use_smooth = True


def add(o, m):
    o.data.materials.append(m); return o


def sphere(loc, r, m, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=48, ring_count=24); o = bpy.context.object; o.scale = scale
    for p in o.data.polygons: p.use_smooth = True
    return add(o, m)


def capsule(a, b, r, m):
    a, b = Vector(a), Vector(b); d = b - a
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d.length, location=(a + b) / 2, vertices=32); o = bpy.context.object
    o.rotation_mode = "QUATERNION"; o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d)
    for p in o.data.polygons: p.use_smooth = True
    add(o, m); sphere(a, r, m); sphere(b, r, m); return o


# ---------------------------------------------------------------- world, backdrop
sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = SPP; sc.cycles.use_denoising = True
sc.cycles.max_bounces = 6; sc.render.resolution_x = 1080; sc.render.resolution_y = 1920; sc.render.film_transparent = False
sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "AgX - Punchy"
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True; w.node_tree.nodes["Background"].inputs[0].default_value = (*srgb(255, 200, 120), 1)
w.node_tree.nodes["Background"].inputs[1].default_value = 0.35

# a seamless cyclorama in punchy blue, and the big colour disc behind the hero object
bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 6, 0)); bg = bpy.context.object
bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.object.mode_set(mode="OBJECT")
bg.data.vertices[0].co.y, bg.data.vertices[1].co.y = -20, -20
add(bg, mat("floor", srgb(30, 110, 235), 0.7))
bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 9, 10), rotation=(math.radians(90), 0, 0)); add(bpy.context.object, mat("wall", srgb(30, 110, 235), 0.7))
bpy.ops.mesh.primitive_cylinder_add(radius=3.2, depth=0.3, location=(0.3, 8.6, 4.6), rotation=(math.radians(90), 0, 0), vertices=128)
add(bpy.context.object, mat("disc", srgb(255, 190, 30), 0.35, coat=0.3))
bpy.ops.mesh.primitive_torus_add(major_radius=3.2, minor_radius=0.18, location=(0.3, 8.45, 4.6), rotation=(math.radians(90), 0, 0))
add(bpy.context.object, mat("ring", srgb(255, 120, 30), 0.3))

# ---------------------------------------------------------------- the $1 note: thin bent slab with our flat texture
bpy.ops.mesh.primitive_plane_add(size=1, location=(0.6, 2.4, 3.9)); bill = bpy.context.object
bill.scale = (3.4, 1.47, 1); bill.rotation_euler = (math.radians(78), math.radians(-8), math.radians(-6))
bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.subdivide(number_cuts=24); bpy.ops.object.mode_set(mode="OBJECT")
sol = bill.modifiers.new("t", "SOLIDIFY"); sol.thickness = 0.02
bend = bill.modifiers.new("b", "SIMPLE_DEFORM"); bend.deform_method = "BEND"; bend.angle = math.radians(28); bend.deform_axis = "Y"
mb = mat("bill", (1, 1, 1), 0.6); nt = mb.node_tree; tex = nt.nodes.new("ShaderNodeTexImage"); tex.image = bpy.data.images.load(f"{HERE}/bill_tex.png")
nt.links.new(tex.outputs["Color"], nt.nodes["Principled BSDF"].inputs["Base Color"]); add(bill, mb)
for p in bill.data.polygons: p.use_smooth = True

# ---------------------------------------------------------------- a plain soda bottle (lathe), deep red glass + white label
prof = [(0.0, 0), (0.42, 0), (0.46, 0.15), (0.46, 1.2), (0.30, 1.75), (0.16, 2.2), (0.17, 2.45), (0.0, 2.45)]
me = bpy.data.meshes.new("bot"); me.from_pydata([(r, 0, z) for r, z in prof], [(i, i + 1) for i in range(len(prof) - 1)], [])
bot = bpy.data.objects.new("bot", me); bpy.context.collection.objects.link(bot); bot.location = (2.35, 1.2, 0)
scr = bot.modifiers.new("s", "SCREW"); scr.steps = 64; scr.render_steps = 64; scr.use_smooth_shade = True
bot.modifiers.new("sub", "SUBSURF").levels = 1
add(bot, mat("glass", srgb(150, 30, 20), 0.08, trans=0.85, ior=1.5))
bpy.ops.mesh.primitive_cylinder_add(radius=0.475, depth=0.5, location=(2.35, 1.2, 0.75), vertices=64); add(bpy.context.object, mat("label", srgb(250, 248, 240), 0.5))
bpy.ops.mesh.primitive_cylinder_add(radius=0.19, depth=0.14, location=(2.35, 1.2, 2.5), vertices=48); add(bpy.context.object, mat("cap", srgb(220, 40, 40), 0.3, metal=0.6))

# ---------------------------------------------------------------- our clay guy (own design): shocked, arms up
skin = mat("skin", srgb(236, 180, 140), 0.5, sss=0.15); jumper = mat("jumper", srgb(232, 50, 60), 0.75); jeans = mat("jeans", srgb(40, 60, 120), 0.8)
hair = mat("hair", srgb(60, 36, 24), 0.7); white = mat("eyew", (0.95, 0.95, 0.95), 0.2); black = mat("eyeb", (0.01, 0.01, 0.01), 0.2); mouthm = mat("mouth", srgb(110, 20, 30), 0.5)
X, Y = -1.9, 1.4
capsule((X - 0.26, Y, 0.35), (X - 0.24, Y, 1.35), 0.22, jeans); capsule((X + 0.26, Y, 0.35), (X + 0.24, Y, 1.35), 0.22, jeans)
for sx in (-0.26, 0.26): sphere((X + sx, Y - 0.12, 0.18), 0.26, mat("shoe", srgb(245, 245, 245), 0.6), (1, 1.5, 0.6))
torso = sphere((X, Y, 2.05), 0.62, jumper, (1, 0.8, 1.25))
capsule((X - 0.55, Y, 2.45), (X - 1.15, Y - 0.1, 3.25), 0.17, jumper); capsule((X + 0.55, Y, 2.45), (X + 1.15, Y - 0.1, 3.25), 0.17, jumper)
sphere((X - 1.2, Y - 0.1, 3.4), 0.2, skin); sphere((X + 1.2, Y - 0.1, 3.4), 0.2, skin)
capsule((X, Y, 2.8), (X, Y, 3.0), 0.16, skin)
head = sphere((X, Y, 3.55), 0.66, skin, (1, 0.95, 1.05))
sphere((X, Y + 0.08, 4.05), 0.62, hair, (1.05, 1.0, 0.55))
for ex in (-0.24, 0.24):
    sphere((X + ex, Y - 0.56, 3.68), 0.16, white, (1, 0.6, 1.15)); sphere((X + ex, Y - 0.66, 3.66), 0.075, black)
sphere((X, Y - 0.6, 3.25), 0.16, mouthm, (1, 0.5, 1.25))
sphere((X - 0.62, Y - 0.1, 3.45), 0.12, skin); sphere((X + 0.62, Y - 0.1, 3.45), 0.12, skin)

# ---------------------------------------------------------------- 3D headline in the top band
def text3d(s, loc, size, m, rot_z=0):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90), 0, math.radians(rot_z))); t = bpy.context.object
    t.data.body = s; t.data.font = bpy.data.fonts.load("/home/claude/studio/fonts/ttf/RubikMonoOne.ttf"); t.data.size = size
    t.data.extrude = 0.12; t.data.bevel_depth = 0.03; t.data.align_x = "CENTER"; t.data.align_y = "CENTER"; t.data.materials.append(m); return t
text3d("FOR $1", (0.2, 3.2, 7.25), 1.35, mat("t1", srgb(255, 255, 255), 0.25, coat=0.5))
text3d("COCA-COLA SOLD", (0.2, 3.3, 8.45), 0.62, mat("t2", srgb(255, 220, 60), 0.3))

# ---------------------------------------------------------------- lights + camera
def area(loc, rot, size, power, col):
    bpy.ops.object.light_add(type="AREA", location=loc, rotation=rot); l = bpy.context.object; l.data.size = size; l.data.energy = power; l.data.color = col; return l
area((-5, -6, 9), (math.radians(55), 0, math.radians(-38)), 6, 2600, (1, 0.93, 0.82))     # warm key
area((6, -3, 5), (math.radians(70), 0, math.radians(60)), 4, 900, (0.75, 0.85, 1))        # cool fill
area((0, 5, 10), (math.radians(-40), 0, 0), 5, 1500, (1, 0.95, 0.9))                       # top/back rim
bpy.ops.object.camera_add(location=(0.15, -12.5, 4.9), rotation=(math.radians(88.5), 0, 0)); cam = bpy.context.object; sc.camera = cam
cam.data.lens = 40; cam.data.dof.use_dof = True; cam.data.dof.focus_distance = 13.5; cam.data.dof.aperture_fstop = 5.6
sc.render.filepath = OUT; t0 = time.time(); bpy.ops.render.render(write_still=True); print("render s", round(time.time() - t0, 1))
