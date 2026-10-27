"""A83-0 reciprocal form/program dependency; source-only, NOT approved art."""
from dataclasses import dataclass, replace
from hashlib import sha256
from math import hypot, isfinite
import json

PROTECTED = {
 'art':'NOT_APPROVED','overall_art':'HOLD',
 'formal':{x:'NOT_RUN' for x in ('S1','G1','G2','G3')},
 'minecraft_construction':'FORBIDDEN','city_integration':'FORBIDDEN',
 'formal_body_samples':331,'formal_foot_samples':993,'half_width_m':0.65,
 'foot_relative_m':(0.15,3.25),'historic_body_interference_ceiling':45,
 'historic_unsupported_foot_ceiling':0,'formal_safety_qa':'NOT_RUN',
}
MIN_DEPTH={'market':18.,'workshop':20.,'reading':16.,'residence':21.}
WALL=1.8
HEIGHT=13.

@dataclass(frozen=True)
class Station:
 ident:str
 district:str
 use:str
 point:tuple
 outward:tuple
 requested_depth_m:float
 authored_exterior_m:float

# Three authored, nonidentical site sections, NOT certified districts or routes.
STATIONS=(
 Station('W0','west','market',(-1090,-330,36),(-.84,.54),35,41),
 Station('W1','west','workshop',(-800,-110,49),(-.70,.71),51,48),
 Station('W2','west','residence',(-550,140,62),(-.46,.89),37,55),
 Station('W3','west','reading',(-300,240,70),(-.15,.99),32,46),
 Station('C0','center','reading',(-290,-390,82),(.24,-.97),36,42),
 Station('C1','center','market',(-50,-150,93),(.50,-.87),58,59),
 Station('C2','center','workshop',(220,110,107),(.82,-.57),41,64),
 Station('C3','center','residence',(410,350,120),(.96,-.28),47,53),
 Station('E0','east','workshop',(500,-130,129),(-.44,-.90),43,49),
 Station('E1','east','residence',(730,100,145),(-.18,-.98),55,58),
 Station('E2','east','reading',(990,290,160),(.16,-.99),33,40),
 Station('E3','east','market',(1200,510,173),(.41,-.91),39,47),
)
def validate_flags(flags):
 if flags!=PROTECTED:raise ValueError('PROTECTED_GATES_OR_SAFETY_CONTRACT_CHANGED')

def solve(s):
 x,y,z=s.point;nx,ny=s.outward
 if not all(isfinite(v) for v in (x,y,z,nx,ny,s.requested_depth_m,s.authored_exterior_m)):
  raise ValueError('NONFINITE_GEOMETRY')
 if not .99<hypot(nx,ny)<1.01:raise ValueError('BAD_OUTWARD_UNIT_VECTOR')
 if s.use not in MIN_DEPTH:raise ValueError('UNSUPPORTED_PROGRAM')
 # Shared unknown solves a joint program/exterior target (neither is post-applied).
 d=.6*(s.requested_depth_m+WALL)+.4*s.authored_exterior_m
 usable=d-WALL
 if usable<MIN_DEPTH[s.use]:raise ValueError('INSUFFICIENT_PROGRAM_DEPTH')
 return {'id':s.ident,'district':s.district,'use':s.use,
         'depth_m':usable,'offset_m':d,
         'outer':(x+nx*d,y+ny*d,z),
         'inner':(x+nx*(d-WALL),y+ny*(d-WALL),z),
         'civic_edge':s.point}

def witness(stations=STATIONS,flags=PROTECTED):
 validate_flags(flags)
 if len(stations)!=12 or {s.district for s in stations}!={'west','center','east'}:
  raise ValueError('MISSING_MULTIDISTRICT_SECTION')
 if len({s.ident for s in stations})!=len(stations):
  raise ValueError('DUPLICATE_STATION_ID')
 if {s.use for s in stations}!=set(MIN_DEPTH):
  raise ValueError('MISSING_REAL_USE_INTENT')
 solved=[solve(s) for s in stations]
 vertices=[];faces=[]
 for p in solved:
  ids={}
  for k in ('outer','inner'):
   x,y,z=p[k];ids[k]=len(vertices)
   vertices.extend(((x,y,z),(x,y,z+HEIGHT)))
  p['vertex_ids']=ids
 bydistrict={d:[p for p in solved if p['district']==d] for d in ('west','center','east')}
 for district,group in bydistrict.items():
  if len(group)!=4:raise ValueError('BAD_DISTRICT_STATION_COUNT')
  for a,b in zip(group,group[1:]):
   for side in ('inner','outer'):
    v=a['vertex_ids'][side];w=b['vertex_ids'][side]
    faces.extend(((v,w,w+1),(v,w+1,v+1)))
 points=[p['outer'] for p in solved]
 span=[max(v[i] for v in points)-min(v[i] for v in points) for i in range(3)]
 if span[0]<1800 or span[1]<700 or span[2]<100:
  raise ValueError('INCOMPLETE_THREE_SCALE_RESEARCH_EXTENT')
 return {'stations':solved,'vertices':vertices,'triangles':faces,
         'districts':list(bydistrict),'span_m':[span[0],span[1],span[2]+HEIGHT],
         'scope':'SPARSE_G0_BOUNDARY_WITNESS_NOT_CITY',
         'rendered_3d':'NOT_RUN','real_rooms':0,'full_3d_walkability':'NOT_TESTED',
         'load_safety':'NOT_TESTED','art':'NOT_APPROVED','gate':'A83_0_SOURCE_ONLY'}

def geom_hash(points):
 return sha256(json.dumps(points,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def counterfactuals():
 base=witness()
 base_out=geom_hash([p['outer'] for p in base['stations']])
 base_in=geom_hash([p['inner'] for p in base['stations']])
 sample=list(STATIONS)
 sample[5]=replace(sample[5],requested_depth_m=sample[5].requested_depth_m+9)
 prog=witness(tuple(sample))
 sample=list(STATIONS)
 sample[5]=replace(sample[5],authored_exterior_m=sample[5].authored_exterior_m+12)
 form=witness(tuple(sample))
 po=geom_hash([p['outer'] for p in prog['stations']])
 pi=geom_hash([p['inner'] for p in prog['stations']])
 fo=geom_hash([p['outer'] for p in form['stations']])
 fi=geom_hash([p['inner'] for p in form['stations']])
 checks={
  'program_edit_moves_actual_outer_vertices':po!=base_out,
  'program_edit_moves_actual_inner_vertices':pi!=base_in,
  'exterior_edit_moves_actual_inner_vertices':fi!=base_in,
  'exterior_edit_moves_actual_outer_vertices':fo!=base_out,
  'program_changes_usable_depth':prog['stations'][5]['depth_m']!=base['stations'][5]['depth_m'],
  'exterior_changes_usable_depth':form['stations'][5]['depth_m']!=base['stations'][5]['depth_m'],
  'common_surface_topology_stable':len(prog['triangles'])==len(form['triangles'])==len(base['triangles']),
 }
 if not all(checks.values()):raise AssertionError('ONE_WAY_OR_FAKE_RECIPROCAL_GEOMETRY')
 return {'checks':checks,'baseline_outer_coordinate_sha256':base_out,
         'baseline_inner_coordinate_sha256':base_in,'program_edit_outer_sha256':po,
         'exterior_edit_inner_sha256':fi}

def refuse_negative_controls():
 tests={}
 def reject(name,fn):
  try:fn()
  except (ValueError,AssertionError):tests[name]=True
  else:tests[name]=False
 reject('forbid_art_pass',lambda:witness(flags={**PROTECTED,'art':'APPROVED'}))
 reject('forbid_formal_g2',lambda:witness(flags={**PROTECTED,'formal':{**PROTECTED['formal'],'G2':'PASS'}}))
 reject('forbid_construction',lambda:witness(flags={**PROTECTED,'minecraft_construction':'ALLOWED'}))
 reject('forbid_safety_contract_relaxation',lambda:witness(flags={**PROTECTED,'formal_foot_samples':1}))
 reject('reject_missing_district',lambda:witness(STATIONS[:-4]))
 reject('reject_duplicate_station',lambda:witness((STATIONS[0],)+STATIONS[:11]))
 reject('reject_invalid_unit_normal',lambda:witness((replace(STATIONS[0],outward=(3.,3.)),)+STATIONS[1:]))
 reject('reject_unsafe_shallow_program',lambda:witness((replace(STATIONS[0],requested_depth_m=2,authored_exterior_m=2),)+STATIONS[1:]))
 reject('reject_missing_use',lambda:witness(tuple(replace(s,use='market') if s.use=='residence' else s for s in STATIONS)))
 if not all(tests.values()):raise AssertionError('NEGATIVE_CONTROL_FAILED')
 return tests

def main():
 p=witness()
 print(json.dumps({
  'purpose':'A83-0 falsifiable reciprocal boundary, not art',
  'actual_control_points':len(p['stations']),
  'sparse_actual_3d_triangles':len(p['triangles']),
  'designed_span_m':p['span_m'],
  'art':'NOT_APPROVED','construction':'FORBIDDEN','rendered_3d':'NOT_RUN',
  'real_rooms':0,'formal_G2_G3':'NOT_RUN',
  'counterfactuals':counterfactuals(),'negative_controls':refuse_negative_controls(),
 },indent=2,sort_keys=True))

if __name__=='__main__':main()
