"""D13 actual research-program ablation: reread persistent PLY, export ablated GLB.
Tests whether changing research activity actually changes authored envelope.
Outcome expected FAIL for ART CAUSALITY (no envelope dependence), never art PASS.
"""
from pathlib import Path
import json,hashlib,trimesh
ROOT=Path(__file__).resolve().parent
results=[]
for n in ('canyon','braided','courts'):
 f=ROOT/n;man=json.loads((f/'manifest.json').read_text())
 roles=list(man['roles']); assert 'research' in roles and 'inhabited' in roles
 bodies=[];scene=trimesh.Scene()
 for tag in roles:
  p=f/f'{tag}.ply';mesh=trimesh.load(p,force='mesh')
  if tag=='research':continue
  scene.add_geometry(mesh,geom_name=tag);bodies.append(mesh)
 scene.export(f/'no_research.glb')
 faces_full=man['faces'];faces_without=sum(len(m.faces) for m in bodies)
 original_shell_sha=man['roles']['inhabited']['sha256']
 # This is the same original cached skin, not regenerated based on program removal.
 same_shell=hashlib.sha256((f/'inhabited.ply').read_bytes()).hexdigest()==original_shell_sha
 assert faces_full-faces_without==man['roles']['research']['faces'] and same_shell
 results.append({'variant':n,'original_faces':faces_full,'without_research_faces':faces_without,
        'removed_faces':faces_full-faces_without,
        'removed_mesh_fraction':round((faces_full-faces_without)/faces_full,5),
        'same_envelope_mesh_sha256':original_shell_sha,
        'envelope_unchanged_under_activity_ablation':same_shell,
        'ablation_glb_sha256':hashlib.sha256((f/'no_research.glb').read_bytes()).hexdigest(),
        'interpretation':'REMOVING program only deletes separate research floor, no authored exterior form is regenerated'})
print(json.dumps(results,indent=2))
assert all(x['removed_mesh_fraction']<.001 for x in results)
(ROOT/'ablation.json').write_text(json.dumps({'stage':'D13','result':'PRE_ART_REJECT_ACTIVITY_DOES_NOT_DRIVE_ENVELOPE',
 'cases':results,'G0':'NOT_RUN','formal_S1_G1_G2_G3':'NOT_RUN','art_adopted':0,
 'Minecraft':'FORBIDDEN'},indent=2))