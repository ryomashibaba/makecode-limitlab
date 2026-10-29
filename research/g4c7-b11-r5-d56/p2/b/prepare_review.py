"""Preserve first renders; save revised camera/repair evidence as new R1 files.
This is geometry repair and fair comparison, not ornamentation of rejected art.
"""
import bpy,sys,json,hashlib
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
V=sys.argv[sys.argv.index('--')+1]; O=R/(V+'R1'); O.mkdir(exist_ok=False)
bpy.ops.wm.open_mainfile(filepath=str(R/V/(V+'.blend')))
if V=='B2':
    # Finish the stair opening: the original landing overlapped its last tread.
    ob=bpy.data.objects['HOME_PRIVATE_LANDING']
    for v in ob.data.vertices:
        if abs(v.co.y-27.8)<.001: v.co.y=28.2
    # Real union, not depth bias: eliminate coplanar street/entry floor overlaps.
    target=bpy.data.objects['CORE_MAKING_FLOOR']
    bpy.context.view_layer.objects.active=target
    for name in ['CIVIC_AXIS_A_ACTUAL_STREET','CIVIC_AXIS_B_ACTUAL_STREET','STREET_ENTRY_CONTINUOUS_FLOOR']:
        other=bpy.data.objects[name]
        mod=target.modifiers.new('Actual connected floor union','BOOLEAN'); mod.object=other; mod.operation='UNION'
        bpy.ops.object.modifier_apply(modifier=mod.name); bpy.data.objects.remove(other,do_unlink=True)
for o in bpy.data.objects:
    if o.name=='CONTEXT_GROUND':
        o.scale.x=10; o.scale.y=10
CAM={
 '01_CITY':((550,-720,370),(-15,35,65),45),
 '02_REVERSE':((-550,650,340),(-10,40,75),45),
 '03_STREET_TO_MAKING':((0,-24,1.65),(0,17,6.5),23),
 '04_RESEARCH_TO_MAKING':((-3.7,12,11.65),(13,17,5.6),21),
 '05_HOME':((-12,8,17.65),(-110,-100,35),24),
}
for name,(loc,tar,lens) in CAM.items():
    c=bpy.data.objects[name]; c.location=loc
    c.rotation_euler=(Vector(tar)-c.location).to_track_quat('-Z','Y').to_euler(); c.data.lens=lens
s=bpy.context.scene; s['study']=V+'R1'; s['art']='ART REJECT; no formal adoption'
s['revision']='Camera correction for both; B2 stair aperture/landing and street union repairs only.'
s.camera=bpy.data.objects['01_CITY']
bpy.ops.wm.save_as_mainfile(filepath=str(O/(V+'R1.blend')),compress=True)
bpy.ops.object.select_all(action='DESELECT')
for ob in s.objects:
    if ob.type=='MESH' and not ob.name.startswith('CONTEXT'): ob.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(O/(V+'R1.glb')),use_selection=True,export_format='GLB')
# Actual persisted geometry reimport, with every original research mesh removed.
# Context, cameras and light rig remain identical; no object hidden to show an opening.
for ob in list(s.objects):
    if ob.type=='MESH' and not ob.name.startswith('CONTEXT'): bpy.data.objects.remove(ob,do_unlink=True)
bpy.ops.import_scene.gltf(filepath=str(O/(V+'R1.glb')))
(O/'camera_conditions.json').write_text(json.dumps({'cameras':CAM,'renderer':'Cycles CPU 24 samples','resolution':[1100,720],'geometry':'Reimported persisted R1 GLB, not live builder state','artificial_fill_lights':True,'context_excluded_from_glb':['ground','water'],'art':'REJECT','formal_331_993':'NOT RUN','formal_G0_S1_G1_G2_G3':'NOT RUN'},indent=2),encoding='utf-8')
for name in CAM:
    s.camera=bpy.data.objects[name]; s.render.filepath=str(O/(name+'.png'))
    bpy.ops.render.render(write_still=True); print('REIMPORT_RENDER',V,name,flush=True)
