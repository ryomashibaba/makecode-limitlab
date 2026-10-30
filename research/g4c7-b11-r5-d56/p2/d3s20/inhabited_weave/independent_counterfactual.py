"""Saved-mesh counterfactuals: independent comparison, not ART or walk proof."""
import sys,json
from pathlib import Path
import numpy as np,trimesh
from author import build,plan
p=Path(__file__).resolve().parent
variants=[('shift_research_Y_26',dict(research_shift_y=26)),('narrow_research_20pct',dict(research_span=.8))]
base=trimesh.load_scene(p/'INHABITED_WEAVE.glb')
res=[]
for label,changes in variants:
 out=p/'counterfactuals'/label
 build(out,plan(**changes))
 other=trimesh.load_scene(out/'INHABITED_WEAVE.glb')
 changed=[]
 for key in sorted(set(base.geometry)&set(other.geometry)):
  aa,bb=base.geometry[key].vertices,other.geometry[key].vertices
  if aa.shape!=bb.shape or not np.allclose(aa,bb,atol=1e-5):changed.append(key)
 street=[x for x in changed if x.startswith('public_')];rooms=[x for x in changed if ('research_' in x or 'orbital_studio_' in x)]
 res.append({'case':label,'changed_named_meshes':len(changed),'changed_public_road_meshes':len(street),
             'changed_research_related_meshes':len(rooms),'sample_street_changes':street[:10],
             'saved_glb_both_external_and_internal_mesh_change':bool(street and rooms),
             'limitations':'Geometry only, neither volume clearance nor continuous traversal nor art proof'})
(p/'COUNTERFACTUAL_AUDIT.json').write_text(json.dumps(res,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(res,indent=2,ensure_ascii=False))
