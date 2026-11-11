"""A plain ballpoint pen (no brand), Blender Cycles, transparent PNG cut-outs: pen.png (diagonal hero) and pen_flat.png (lying flat)."""
import bpy, math, sys, os
from mathutils import Vector
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)


def srgb(r, g, b): return tuple(((x / 255) ** 2.2) for x in (r, g, b))


def mat(col, rough=0.3, metal=0.0, coat=0.6):
    m = bpy.data.materials.new("m"); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*col, 1); b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal; b.inputs["Coat Weight"].default_value = coat
    return m


def lathe(prof, m, steps=64):
    me = bpy.data.meshes.new("p"); me.from_pydata([(r, 0, z) for r, z in prof], [(i, i + 1) for i in range(len(prof) - 1)], [])
    o = bpy.data.objects.new("p", me); bpy.context.collection.objects.link(o)
    s = o.modifiers.new("s", "SCREW"); s.steps = steps; s.render_steps = steps; s.use_smooth_shade = True
    o.data.materials.append(m); return o


def pen(root_rot):
    body = mat(srgb(20, 70, 200), 0.25); chrome = mat((0.8, 0.8, 0.84), 0.15, 1.0, 0); black = mat(srgb(20, 20, 26), 0.4)
    parts = [lathe([(0, 0), (0.012, 0.0), (0.05, 0.16), (0.07, 0.24), (0.07, 0.3), (0, 0.3)], chrome),            # tip cone
             lathe([(0, 0.3), (0.082, 0.3), (0.085, 0.5), (0.085, 1.0), (0.085, 1.42), (0, 1.42)], body),         # barrel
             lathe([(0, 0.48), (0.09, 0.48), (0.09, 0.62), (0, 0.62)], black),                                   # grip
             lathe([(0, 1.42), (0.088, 1.42), (0.088, 1.5), (0, 1.5)], chrome),                                  # ring
             lathe([(0, 1.5), (0.06, 1.5), (0.06, 1.62), (0.04, 1.66), (0, 1.66)], body)]                        # button
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -0.105, 1.18)); clip = bpy.context.object; clip.scale = (0.05, 0.03, 0.5)
    clip.modifiers.new("b", "BEVEL").width = 0.01; clip.data.materials.append(chrome); parts.append(clip)
    root = bpy.data.objects.new("r", None); bpy.context.collection.objects.link(root)
    for p in parts: p.parent = root
    root.location = (0, 0, -0.8); root.rotation_euler = root_rot; return root


def scene(cam=(0, -4.2, 0.4)):
    bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
    sc.render.engine = "CYCLES"; sc.cycles.device = "CPU"; sc.cycles.samples = 48; sc.cycles.use_denoising = True
    sc.render.resolution_x, sc.render.resolution_y = 900, 900; sc.render.film_transparent = True
    sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "AgX - Base Contrast"
    w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True; w.node_tree.nodes["Background"].inputs[1].default_value = 0.7
    for loc, rot, pw in (((-3, -3, 4), (55, 0, -40), 700), ((3, -2, 2), (65, 0, 60), 300), ((0, 3, 3), (-45, 0, 180), 400)):
        bpy.ops.object.light_add(type="AREA", location=loc, rotation=tuple(math.radians(v) for v in rot)); l = bpy.context.object; l.data.size = 3; l.data.energy = pw
    bpy.ops.object.camera_add(location=cam); c = bpy.context.object; sc.camera = c; c.data.lens = 60
    c.rotation_euler = (Vector((0, 0, 0)) - Vector(cam)).to_track_quat("-Z", "Y").to_euler()


scene(); pen((math.radians(-10), math.radians(-38), 0)); bpy.context.scene.render.filepath = f"{OUT}/pen.png"; bpy.ops.render.render(write_still=True)
print("done", flush=True)
