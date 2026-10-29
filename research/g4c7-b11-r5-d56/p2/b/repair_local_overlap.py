"""R2: cut a real stair clearance from the intersecting district wall.
The R1 failure and trace are preserved. No global shape/detail refinement.
"""
import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parent; O=R/'B2R2'; O.mkdir(exist_ok=False)
bpy.ops.wm.open_mainfile(filepath=str(R/'B2R1/B2R1.blend'))
bpy.ops.mesh.primitive_cube_add(size=1,location=(-25,23.1,15.5)); cut=bpy.context.object
cut.name='TEMP_ACTUAL_STAIR_CLEARANCE_CUT'; cut.dimensions=(6,11,11)
bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
ob=bpy.data.objects['MAKER_ACTUAL_WINDOW_WALLS']; bpy.context.view_layer.objects.active=ob
mod=ob.modifiers.new('R2 real stair headroom subtraction','BOOLEAN'); mod.object=cut; mod.operation='DIFFERENCE'
bpy.ops.object.modifier_apply(modifier=mod.name); bpy.data.objects.remove(cut,do_unlink=True)
s=bpy.context.scene; s['study']='B2R2'; s['repair']='Actual district wall subtraction over 4 failed stair body segments; ART REJECT unchanged'
bpy.ops.wm.save_as_mainfile(filepath=str(O/'B2R2.blend'),compress=True)
bpy.ops.object.select_all(action='DESELECT')
for ob in s.objects:
 if ob.type=='MESH' and not ob.name.startswith('CONTEXT'): ob.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(O/'B2R2.glb'),use_selection=True,export_format='GLB')
for ob in list(s.objects):
 if ob.type=='MESH' and not ob.name.startswith('CONTEXT'): bpy.data.objects.remove(ob,do_unlink=True)
bpy.ops.import_scene.gltf(filepath=str(O/'B2R2.glb'))
conditions=json.loads((R/'B2R1/camera_conditions.json').read_text())
conditions['geometry']='Reimported persisted B2R2 GLB; actual wall cut, no hidden objects'
(O/'camera_conditions.json').write_text(json.dumps(conditions,indent=2))
for name in conditions['cameras']:
 s.camera=bpy.data.objects[name]; s.render.filepath=str(O/(name+'.png'))
 bpy.ops.render.render(write_still=True); print('R2_RENDER',name,flush=True)
