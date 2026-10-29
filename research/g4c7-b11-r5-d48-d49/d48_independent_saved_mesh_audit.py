"""D48 independent audit; intentionally NEVER import the author generator.
Checks only saved GLB nodes/triangles with measured geometry. Does NOT certify safety or art.
"""
import argparse,copy,json,math
from pathlib import Path
import numpy as np
import trimesh
from shapely.geometry import MultiPoint,Point,Polygon

PROTECT={'art':'ART HOLD','adopted':0,'G0':'NOT_RUN','S1_G1_G2_G3':'NOT_RUN',
 'construction':'FORBIDDEN','city_integration':'FORBIDDEN','PR53':'DRAFT_OPEN','main':'UNTOUCHED'}

def load(path):
 s=trimesh.load(path,force='scene',process=False);d={}
 for n in s.graph.nodes_geometry:
  T,k=s.graph[n];m=s.geometry[k].copy();m.apply_transform(T);assert len(m.faces)>1;n=str(n)
  if n in d:raise AssertionError('dup '+n)
  d[n]=m
 return d

def xyshape(m):
 return MultiPoint(m.vertices[:,:2]).convex_hull

def zmax(m):return float(m.bounds[1,2])

def xy_overlap(a,b):return float(xyshape(a).intersection(xyshape(b)).area)

def approx_room_void(d):
 # Deliberately modest: checking 3 sample interiors against geometry AABB, not watertightness.
 samples=[(13,22,10.8),(18,29,10.8),(23,24,10.8)]
 room={n:m for n,m in d.items() if n.startswith('room__')}
 return {str(p):[n for n,m in room.items() if np.all(np.array(p)>m.bounds[0]+1e-5) and np.all(np.array(p)<m.bounds[1]-1e-5)] for p in samples}

def verify(states,manifest):
 assert manifest['stage']=='D48' and manifest['protection']==PROTECT
 a=states['baseline'];n=states['no_maker'];r=states['no_research']
 assert all(len(states[k])==manifest['cases'][k]['nodes'] for k in states)
 assert all({'shared__site','shared__middle_landing','shared__upper_landing','shared__gallery',
   'shared__upper_door_bridge','room__actual_hollow_floor','room__only_room_ceiling',
   'room__front_lintel'}.issubset(d) for d in states.values())
 for role,removed in [('maker',n),('research',r)]:
  names={key for key in a if key.startswith(role+'__')}
  assert len(names)>=7
  assert not any(x.startswith(role+'__') for x in removed)
  assert {x for x in a if x not in names}==set(removed)
  assert f'{role}__work_floor' in names
  assert ('maker__sculpted_hearth_cliff' if role=='maker' else 'research__folded_instrument_recess') in names
 # Exactly two flights of actual step solids; consistent .18 increments; first + second reach top4 and7.24.
 for fl,start,final in [('out',.76,4.0),('return',4.0,7.24)]:
  tops=[zmax(a[f'shared__stair_{fl}_{i}']) for i in range(18)]
  assert all(abs(tops[i]-(start+.18*(i+1)))<1e-3 for i in range(18))
  assert abs(tops[-1]-final)<1e-3
 for name,z in [('shared__middle_landing',4.0),('shared__upper_landing',7.24),
                ('shared__gallery',7.24),('shared__upper_door_bridge',7.24),
                ('room__actual_hollow_floor',7.24),('room__only_room_ceiling',14.05)]:
  assert abs(zmax(a[name])-z)<1e-3,(name,zmax(a[name]))
 overlaps={
  'upper_landing_gallery':xy_overlap(a['shared__upper_landing'],a['shared__gallery']),
  'gallery_bridge':xy_overlap(a['shared__gallery'],a['shared__upper_door_bridge']),
  'bridge_room':xy_overlap(a['shared__upper_door_bridge'],a['room__actual_hollow_floor'])}
 assert all(v>.18 for v in overlaps.values()),overlaps
 # Room is separated into actual physical walls and empty interior samples (this cannot prove complete sealed enclosure).
 assert len([x for x in a if x.startswith('room__hollow_wall_')])==4
 assert len([x for x in a if x.startswith('room__front_entrance_jamb_')])==2
 assert 'room__east_actual_glass' in a
 samples=approx_room_void(a)
 assert all(not hit for hit in samples.values()),samples
 # Door opening nominal data must match the TWO jambs and higher lintel. No fake solid vertical door.
 poly=np.array(manifest['room_polygon'],float);edge=float(np.linalg.norm(poly[1]-poly[0]));lo,hi=manifest['room_entrance']['t_range']
 width=edge*(hi-lo);assert width>4.5
 assert a['room__front_lintel'].bounds[0,2]>=11.34
 assert manifest['room_entrance']['z_clear']==[7.24,11.35]
 # The author hasn't proved one enclosed civic room; do not allow passing this as G0 or habitable safe.
 return {'cases':{k:len(v) for k,v in states.items()},'maker_removed':len(a)-len(n),
 'research_removed':len(a)-len(r),'stair_steps':36,'stair_mid_top':4.0,'stair_upper_top':7.24,
 'upper_level_floor_overlaps_area_m2_model_units':{k:round(v,4) for k,v in overlaps.items()},
 'door_nominal_clear_width':round(width,4),'door_nominal_clear_height':4.11,
 'hollow_room_3d_sample_obstructions':samples,'upper_room_geometry':'LIMITED_PASS',
 'shared_civic_indoor_enclosure':'FAIL_OPEN_AIR_CORRIDOR','art':'REJECT','adopted':0}

def mutations(states,m):
 # Hand-crafted defects in independently loaded geometry / metadata.
 def cpy():return {k:v.copy() for k,v in states.items()},copy.deepcopy(m)
 names=['forge_adopted','maker_leak','research_leak','missing_bridge','broken_upper_landing',
        'bad_middle_landing','blocked_room_sample','deleted_door_jamb','remove_research_cliff',
        'forged_formal_qa']
 for name in names:
  d,p=cpy()
  if name=='forge_adopted':p['protection']['adopted']=1
  elif name=='maker_leak':d['no_maker']['maker__work_floor']=d['baseline']['maker__work_floor']
  elif name=='research_leak':d['no_research']['research__work_floor']=d['baseline']['research__work_floor']
  elif name=='missing_bridge':del d['baseline']['shared__upper_door_bridge']
  elif name=='broken_upper_landing':
   f=d['baseline']['shared__upper_landing'].copy();f.apply_translation((0,0,1));d['baseline']['shared__upper_landing']=f
  elif name=='bad_middle_landing':
   f=d['baseline']['shared__middle_landing'].copy();f.apply_translation((0,0,-.5));d['baseline']['shared__middle_landing']=f
  elif name=='blocked_room_sample':
   f=trimesh.creation.box(extents=(3,3,2));f.apply_translation((13,22,10.8));d['baseline']['room__fake_solid_filling']=f;p['cases']['baseline']['nodes']+=1
  elif name=='deleted_door_jamb':del d['baseline']['room__front_entrance_jamb_0']
  elif name=='remove_research_cliff':del d['baseline']['research__folded_instrument_recess']
  else:p['protection']['G0']='PASS'
  try:verify(d,p)
  except (AssertionError,KeyError,IndexError):continue
  raise AssertionError('MISS: '+name)
 return names

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',default='d48_build');args=ap.parse_args();p=Path(args.out)
 m=json.loads((p/'manifest.json').read_text(encoding='utf8'))
 states={k:load(p/f'd48_{k}.glb') for k in ['baseline','no_maker','no_research']}
 result=verify(states,m);changes=mutations(states,m)
 r={'stage':'D48','scope':'INDEPENDENT_SAVED_MESH_LIMITED_QA_ONLY','technical':result,
    'detected_negative_mutations':len(changes),'mutation_names':changes,
    'art_judgment':'PRE_G0_REJECT_OPEN_AIR_TWO_FACADE_FAILURE',
    'formal_G0_S1_G1_G2_G3':'NOT_RUN','not_certified':['architectural beauty','whole shared room enclosed',
      'rainproofness','structural safety','full body-volume traversal','fire safety'],
    'construction':'FORBIDDEN','city_integration':'FORBIDDEN','adopted':0}
 (p/'d48_independent_result.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 print('D48 independent savedGLB audit PASS (10/10 mutations); artistic failure open-air corridor. ART HOLD.')
if __name__=='__main__':main()
