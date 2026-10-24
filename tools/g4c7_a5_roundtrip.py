"""Run in Blender opened on A5 BLEND; reimport GLB/OBJ in separate scenes."""
import bpy,sys,json
from pathlib import Path
from mathutils import Vector
root=Path(sys.argv[sys.argv.index('--')+1]).resolve()
def snapshot(scene):
    meshes=[o for o in scene.objects if o.type=='MESH']
    pts=[o.matrix_world@Vector(c) for o in meshes for c in o.bound_box]
    lo=[min(p[i] for p in pts) for i in range(3)]; hi=[max(p[i] for p in pts) for i in range(3)]
    return {'meshes':len(meshes),'min':lo,'max':hi,'vertices':sum(len(o.data.vertices) for o in meshes)}
base=snapshot(bpy.data.scenes['A5_B_ORBITAL_COMMONS']); report={'blend':base}
for kind in ['glb','obj']:
    scene=bpy.data.scenes.new('VERIFY_'+kind); bpy.context.window.scene=scene
    if kind=='glb': bpy.ops.import_scene.gltf(filepath=str(root/'a5_orbital_commons.glb'))
    else: bpy.ops.wm.obj_import(filepath=str(root/'a5_orbital_commons.obj'))
    result=snapshot(scene); report[kind]=result
    assert result['meshes']==base['meshes'],(kind,result,base)
    assert max(abs(result[key][i]-base[key][i]) for key in ['min','max'] for i in range(3))<.001,(kind,result,base)
report['verdict']='GEOMETRY_ROUNDTRIP_PASS_NOT_ART_OR_WALK_PASS'
(root/'roundtrip_qa.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
print(report)
