"""Independent read-only checks of persisted GLBs. No author imports; no formal human QA."""
from pathlib import Path
import numpy as np,json,hashlib
import trimesh
R=Path(__file__).resolve().parent
names=['CIVIC_CANYON_PILOT.glb','COUNTERFACTUAL_CIVIC_SHIFT.glb','COUNTERFACTUAL_WIDTH_SHRINK.glb']
scenes=[trimesh.load(R/n,force='scene') for n in names]
def bound(s):return np.asarray(s.bounds,dtype=float)
def stats(s):
 ms=list(s.geometry.values());return dict(geometries=len(ms),triangles=int(sum(len(m.faces) for m in ms)),vertices=int(sum(len(m.vertices) for m in ms)),bounds=np.round(bound(s),6).tolist(),extents=np.round(s.extents,6).tolist())
base=scenes[0]; report={'study':'D3S20 independent persisted GLB broad-phase only','models':{n:stats(s) for n,s in zip(names,scenes)}}
report['files_sha256']={n:hashlib.sha256((R/n).read_bytes()).hexdigest() for n in names}
# Exact saved geometry coordinates. Compare mesh rather than author's data.
def compare(a,b):
 common=set(a.geometry)&set(b.geometry); changed=[]; roles={}
 for n in sorted(common):
  v=a.geometry[n].vertices;w=b.geometry[n].vertices
  ischanged=v.shape!=w.shape or (np.max(np.abs(v-w))>1e-4)
  if ischanged:
   changed.append(n)
   role='public_axis' if 'civic_spine_' in n else 'crossing' if n.startswith('cross_civic') else 'built_frontage' if n.startswith(('west_','east_')) else 'other'
   roles[role]=roles.get(role,0)+1
 return {'same_geometry_names':len(common),'changed':len(changed),'changes_by_kind':roles,'public_spine_changed':any(n.startswith('civic_spine') for n in changed),'frontage_changed':any(n.startswith(('west_','east_')) for n in changed),'examples':changed[:12]}
report['counterfactuals']={n:compare(base,s) for n,s in zip(names[1:],scenes[1:])}
# Open air sample along the public axis, deliberately not a continuous body test.
# Other structures are checked by fast AABB that can produce FALSE positives.
samples=[]; blocks=[]
for i in range(6):
 y0,y1=[-238.,-156.,-72.,5.,86.,165.,243.][i:i+2]
 x0,x1=[-13.,23.,5.,-29.,2.,29.,4.][i:i+2]
 for t in (.2,.4,.6,.8):
  x=(1-t)*x0+t*x1;y=(1-t)*y0+t*y1
  z=13.0
  pt=np.array([x,y,z]); samples.append(pt)
  hit=[]
  for n,m in base.geometry.items():
   if n.startswith(('civic_spine','cross_civic')): continue
   bb=m.bounds
   if np.all(pt>=bb[0]) and np.all(pt<=bb[1]): hit.append(n)
  if hit:blocks.append({'station':i,'point':np.round(pt,3).tolist(),'potential_aabb_hits':hit[:12]})
report['limited_24_public_eye_sample']={'sample_points':len(samples),'points_with_potential_aabb_obstruction':len(blocks),'examples':blocks[:8], 'limitation':'AABB broad-phase, neither actual mesh intersection nor human 3D sweep'}
# negative control in independent broad-phase detector (not saved to city scene)
synthetic=np.array([[samples[0][0]-2,samples[0][1]-2,11],[samples[0][0]+2,samples[0][1]+2,16]])
report['synthetic_obstruction_detected']=bool(np.all(samples[0]>=synthetic[0]) and np.all(samples[0]<=synthetic[1]))
# Root of the previous failures: no enclosed rooms, no continuous vertical access; do not infer from floor counts.
report['design_rejection_flags']=['a near-uniform row of 3-8 horizontal floor plates on each of 12 sides','public axes do not imply real room entrance/physical route','no built staircases or landing sequence','study silhouette does not cover original intended X+-400/Y+-280/Z0..400 envelope']
report['formal_331_993']='NOT RUN';report['makecode_instruction_counts']='NOT MEASURED'
(R/'INDEPENDENT_AUDIT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2)[:9000])