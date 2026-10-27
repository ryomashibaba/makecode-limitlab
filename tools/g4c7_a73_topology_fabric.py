#!/usr/bin/env python3
"""A73 G0: one path datum generates corridor floor, doorway and room floor.

No aesthetic certification; no support/collision/illumination/real navigation QA.
Never alters earlier models. Uses only Shapely and Python standard library.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, math, struct, zlib
from collections import defaultdict, deque
from pathlib import Path
from shapely.geometry import LineString, Point, Polygon, box
from shapely.ops import unary_union, triangulate

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts/g4c7-a73-route-derived-architecture/g0-output'
STAGE='A73'
NODES={
 'PUBLIC_EYE':(0.,-16.,0.), 'CIVIC_HEART':(0.,-3.,0.),
 'MARKET_ENTRY':(-12.,1.,0.),'MAKER_ENTRY':(12.,1.,0.),
 'STAIR1_START':(0.,6.,0.),'STAIR1_END':(0.,12.4,3.6),
 'MID_CIVIC':(0.,16.5,3.6),'STAIR2_START':(5.,18.,3.6),
 'STAIR2_END':(11.4,18.,7.2),'READING_ENTRY':(10.,31.,7.2),
 'STAIR3_START':(16.,26.,7.2),'STAIR3_END':(25.6,26.,12.6),
 'HOUSING_ENTRY':(27.,42.,12.6),'GARDEN':(35.,45.,12.6)}
EDGES=[
 ('PUBLIC_EYE','CIVIC_HEART','level',0),
 ('CIVIC_HEART','MARKET_ENTRY','level',0),
 ('CIVIC_HEART','MAKER_ENTRY','level',0),
 ('CIVIC_HEART','STAIR1_START','level',0),
 ('STAIR1_START','STAIR1_END','stair',20),
 ('STAIR1_END','MID_CIVIC','level',0),
 ('MID_CIVIC','STAIR2_START','level',0),
 ('STAIR2_START','STAIR2_END','stair',20),
 ('STAIR2_END','READING_ENTRY','level',0),
 ('STAIR2_END','STAIR3_START','level',0),
 ('STAIR3_START','STAIR3_END','stair',30),
 ('STAIR3_END','HOUSING_ENTRY','level',0),
 ('HOUSING_ENTRY','GARDEN','level',0)]
ROOMS=[
 {'id':'MARKET','node':'MARKET_ENTRY','depth':19.,'front_width':12.,'door_width':4.0,'rear_slant':2.0,'program':'public_market'},
 {'id':'MAKER','node':'MAKER_ENTRY','depth':21.,'front_width':14.,'door_width':4.2,'rear_slant':-2.5,'program':'making_and_workshop'},
 {'id':'READING','node':'READING_ENTRY','depth':23.,'front_width':17.,'door_width':4.6,'rear_slant':3.0,'program':'research_and_library'},
 {'id':'HOUSING','node':'HOUSING_ENTRY','depth':18.,'front_width':13.,'door_width':4.0,'rear_slant':-2.0,'program':'housing'}]
CONTRACT={'stage':'A73','art':'NOT_APPROVED','overall_art':'HOLD',
 'formal':{k:'NOT_RUN' for k in ['S1','G1','G2','G3']},
 'minecraft_construction':'FORBIDDEN','city_integration':'FORBIDDEN',
 'corridor_width_m':5.6,'stair_rise_m':.18,'stair_going_m':.32,
 'eye_height_above_floor_m':1.7,'model_is_full_city':False}

def make_plan(nodes=None,edges=None,rooms=None,contract=None):
 nodes=nodes or NODES; edges=edges if edges is not None else EDGES
 rooms=rooms if rooms is not None else ROOMS; contract=contract or CONTRACT
 errors=[]
 if contract.get('stage')!='A73' or contract.get('art')!='NOT_APPROVED' or contract.get('overall_art')!='HOLD':errors.append('PREMATURE_ART')
 if any(contract.get('formal',{}).get(k)!='NOT_RUN' for k in ('S1','G1','G2','G3')):errors.append('PREMATURE_FORMAL_GATE')
 if contract.get('minecraft_construction')!='FORBIDDEN' or contract.get('city_integration')!='FORBIDDEN':errors.append('CONSTRUCTION_UNLOCKED')
 if contract.get('model_is_full_city') is not False:errors.append('FAKE_FULL_CITY')
 width=contract.get('corridor_width_m',0)
 if width<4.8:errors.append('INSUFFICIENT_DESIGN_CORRIDOR')
 if contract.get('eye_height_above_floor_m')!=1.7:errors.append('WRONG_EYE_HEIGHT')
 if len(set(nodes))!=len(nodes) or set(nodes)!={k for k in NODES}:errors.append('NODE_ID_MISMATCH')
 if len(rooms)!=4 or {r['id'] for r in rooms}!={'MARKET','MAKER','READING','HOUSING'}:errors.append('PROGRAM_MISMATCH')
 adj=defaultdict(list);walk=[];stairs=[]
 for a,b,kind,steps in edges:
  if a not in nodes or b not in nodes:
   errors.append('MISSING_EDGE_NODE');continue
  A,B=nodes[a],nodes[b]
  horizontal=math.dist(A[:2],B[:2]);rise=B[2]-A[2]
  if kind=='level':
   if abs(rise)>1e-8:errors.append('LEVEL_Z_GAP_'+a)
   elif horizontal<=0:errors.append('ZERO_LEVEL_EDGE')
   else:walk.append((a,b,A[2],LineString([A[:2],B[:2]])))
  elif kind=='stair':
   expected=steps*contract.get('stair_rise_m',0)
   distance=steps*contract.get('stair_going_m',0)
   if steps not in (20,30) or abs(rise-expected)>1e-8 or abs(horizontal-distance)>1e-8:errors.append('STAIR_STEP_GEOMETRY_'+a)
   else:stairs.append((a,b,steps,A,B))
  else:errors.append('UNKNOWN_EDGE_TYPE')
  adj[a].append(b)
 seen={'PUBLIC_EYE'};q=deque(seen)
 while q:
  for neighbor in adj[q.popleft()]:
   if neighbor not in seen:seen.add(neighbor);q.append(neighbor)
 for required in ['MARKET_ENTRY','MAKER_ENTRY','READING_ENTRY','HOUSING_ENTRY','GARDEN']:
  if required not in seen:errors.append('DISCONNECTED_'+required)
 levels=defaultdict(list)
 for a,b,z,line in walk:levels[z].append(line.buffer(width/2,cap_style=3,join_style=2))
 floors={z:unary_union(polys) for z,polys in levels.items()}
 room_geos={}
 if len({r['node'] for r in rooms})!=len(rooms):errors.append('SHARED_ROOM_ANCHOR')
 for room in rooms:
  label=room['id']; node=room['node']; target=nodes.get(node)
  incoming=[(a,b,ln) for a,b,z,ln in walk if b==node]
  if not incoming or target is None:
   errors.append('UNREGISTERED_DOOR_'+label);continue
  a,_,ln=incoming[-1];A=nodes[a];B=target
  dx=B[0]-A[0];dy=B[1]-A[1];length=math.hypot(dx,dy)
  ux,uy=dx/length,dy/length
  px,py=-uy,ux
  fw=room['front_width']; dw=room['door_width'];depth=room['depth']
  if fw<dw+3 or dw<3.5 or depth<14:errors.append('INSUFFICIENT_ROOM_'+label)
  L=(B[0]-px*fw/2,B[1]-py*fw/2)
  R=(B[0]+px*fw/2,B[1]+py*fw/2)
  opening=LineString([ (B[0]-px*dw/2,B[1]-py*dw/2), (B[0]+px*dw/2,B[1]+py*dw/2)])
  back_center=(B[0]+ux*depth+px*room['rear_slant'],B[1]+uy*depth+py*room['rear_slant'])
  rear_l=(back_center[0]-px*(fw*.59),back_center[1]-py*(fw*.59))
  rear_r=(back_center[0]+px*(fw*.68),back_center[1]+py*(fw*.68))
  poly=Polygon([L,R,rear_r,rear_l])
  if not poly.is_valid or poly.area<100:errors.append('DEGENERATE_ROOM_'+label)
  floor=floors.get(B[2])
  if floor is None:
   errors.append('MISSING_ROOM_FLOOR_LEVEL_'+label);continue
  contact=opening.intersection(floor).length
  if contact<dw-1e-5:errors.append('DOOR_DOES_NOT_MEET_FLOOR_'+label)
  if opening.distance(floor)>1e-8:errors.append('DOOR_FLOOR_GAP_'+label)
  room_geos[label]={'z':B[2],'door':opening,'polygon':poly,'contact':contact,'node':node,'program':room['program'], 'end_of_approach':node, 'entrance_width':dw}
 # Prevent path clips through walls except for the intended open doorway; negative checks.
 if errors:raise ValueError('A73_G0_REJECT: '+','.join(sorted(set(errors))))
 return {'nodes':nodes,'edges':edges,'rooms':room_geos,'floors':floors,'stairs':stairs,'contract':contract}

def run_negative_controls():
 cases=[('art',lambda n,e,r,c:c.__setitem__('art','PASS')),
  ('g2',lambda n,e,r,c:c['formal'].__setitem__('G2','PASS')),
  ('construction',lambda n,e,r,c:c.__setitem__('minecraft_construction','ALLOWED')),
  ('stair_height',lambda n,e,r,c:n.__setitem__('STAIR2_END',(11.4,18,7.1))),
  ('drop_housing',lambda n,e,r,c:e.__setitem__(slice(None),[x for x in e if x[1]!='HOUSING_ENTRY'])),
  ('door_too_wide',lambda n,e,r,c:r[0].__setitem__('door_width',18.0)),
  ('narrow_corridor',lambda n,e,r,c:c.__setitem__('corridor_width_m',2.0)),
  ('unreachable_reading',lambda n,e,r,c:e.__setitem__(slice(None),[x for x in e if x[1]!='READING_ENTRY'])),
  ('fake_fullcity',lambda n,e,r,c:c.__setitem__('model_is_full_city',True))]
 for label,edit in cases:
  n,e,r,c=copy.deepcopy(NODES),copy.deepcopy(EDGES),copy.deepcopy(ROOMS),copy.deepcopy(CONTRACT)
  edit(n,e,r,c)
  try:make_plan(n,e,r,c)
  except ValueError:print('NEGATIVE_CAUGHT',label)
  else:raise AssertionError('NEGATIVE_ESCAPED '+label)
 print('A73_G0_NINE_NEGATIVE_CASES_PASS__NO_ART_OR_SAFETY_PASS')

def report(plan):
 return {'stage':'A73','evidence':'G0_GENERATIVE_GEOMETRIC_CONTACT_ONLY_NOT_NAVMESH',
 'architectural_intent':'door_opening_and_floor_derived_from_same_walk_graph',
 'art':'NOT_APPROVED','overall_art':'HOLD','formal':CONTRACT['formal'],
 'construction':'FORBIDDEN','city_integration':'FORBIDDEN',
 'local_floor_contact':{k:{'height_m':v['z'],'door_width_m':v['entrance_width'],
 'same_height_floor_contact_m':round(v['contact'],6),'room_floor_area_m2':round(v['polygon'].area,2)} for k,v in plan['rooms'].items()},
 'stair_flights':[{'from':a,'to':b,'steps':steps,'rise_m':round(B[2]-A[2],3),
  'horizontal_run_m':round(math.dist(A[:2],B[:2]),3)} for a,b,steps,A,B in plan['stairs']],
 'limits':['No global collision/clearance', 'No actual walking', 'No support loads or evacuation',
 'Room furnishing and heights not built','No proper daylight', 'Not an attractive full future city','G2/G3 not executed']}

def write_obj(plan,out):
 vertices=[];faces=[];groups=[]
 def triangle(points):
  start=len(vertices)
  vertices.extend(points)
  faces.append((start+1,start+2,start+3))
 def floor_polygon(poly,z,key):
  polys=[poly] if poly.geom_type=='Polygon' else list(poly.geoms)
  for p in polys:
   for tri in triangulate(p):
    if p.covers(tri.representative_point()):
     a,b,c=tri.exterior.coords[:3]
     triangle([(a[0],a[1],z),(b[0],b[1],z),(c[0],c[1],z)])
 for z,shape in plan['floors'].items():floor_polygon(shape,z,f'PUBLIC_FLOOR_{z}')
 for k,r in plan['rooms'].items():
  floor_polygon(r['polygon'],r['z'],k+'_TRUE_FLOOR')
  # real wall aperture from same shared segment; other walls remain separated faces
  room=next(x for x in ROOMS if x['id']==k);target=NODES[room['node']]
  front=r['polygon'].exterior.coords[:2];a,b=front
  mid=((a[0]+b[0])/2,(a[1]+b[1])/2)
  factor=room['door_width']/room['front_width']
  u=(mid[0]+(a[0]-mid[0])*factor,mid[1]+(a[1]-mid[1])*factor)
  v=(mid[0]+(b[0]-mid[0])*factor,mid[1]+(b[1]-mid[1])*factor)
  def wall_seg(x,y,z0,z1):
   triangle([(x[0],x[1],z0),(y[0],y[1],z0),(y[0],y[1],z1)])
   triangle([(x[0],x[1],z0),(y[0],y[1],z1),(x[0],x[1],z1)])
  for x,y in [(a,u),(v,b)]:wall_seg(x,y,r['z'],r['z']+5.3)
  wall_seg(u,v,r['z']+4.0,r['z']+5.3)
  coords=list(r['polygon'].exterior.coords)
  for x,y in zip(coords[1:-1],coords[2:]):wall_seg(x,y,r['z'],r['z']+5.3)
 for s,e,n,A,B in plan['stairs']:
  dx=(B[0]-A[0])/n;dy=(B[1]-A[1])/n
  length=math.hypot(dx,dy);perp=(-dy/length,dx/length)
  for i in range(n):
   cx=A[0]+dx*(i+.5);cy=A[1]+dy*(i+.5);z=A[2]+(i+1)*.18
   a=(cx-perp[0]*1.9-dx/2,cy-perp[1]*1.9-dy/2,z)
   b=(cx+perp[0]*1.9-dx/2,cy+perp[1]*1.9-dy/2,z)
   c=(cx+perp[0]*1.9+dx/2,cy+perp[1]*1.9+dy/2,z)
   d=(cx-perp[0]*1.9+dx/2,cy-perp[1]*1.9+dy/2,z)
   triangle([a,b,c]);triangle([a,c,d])
 out.write_text('# A73 G0 only: no structural/walking/art approval\n'+\
  ''.join('v %.5f %.5f %.5f\n'%p for p in vertices)+\
  ''.join('f %d %d %d\n'%f for f in faces))
 return {'mesh_vertices':len(vertices),'mesh_triangles':len(faces)}

def diagram_svg(plan):
 # Plan view of floors and shared door endpoints; documentation only, not aesthetic art.
 colors={0:'#7fc9b3',3.6:'#bfaddb',7.2:'#f2c17b',12.6:'#cf9da8'}
 out=['<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="1000" viewBox="0 0 1400 1000">',
 '<rect width="1400" height="1000" fill="#0d1a2b"/>',
 '<text x="35" y="49" fill="#e6f5f0" font-size="28" font-family="Arial" font-weight="bold">A73 — SINGLE GEOMETRY DATUM / G0 TOPOLOGY PROOF ONLY</text>',
 '<text x="35" y="80" fill="#8fbdc6" font-size="16" font-family="Arial">Real connected room entrances and public floor are generated from one shared graph. NOT FUTURE CITY ART.</text>']
 def co(p):return 450+p[0]*10,880-p[1]*10
 for z,shape in sorted(plan['floors'].items()):
  polys=[shape] if shape.geom_type=='Polygon' else list(shape.geoms)
  for poly in polys:
   pts=' '.join('%.1f,%.1f'%co(pt) for pt in list(poly.exterior.coords))
   out.append(f'<polygon points="{pts}" fill="{colors[z]}" opacity="0.32" stroke="{colors[z]}" stroke-width="2"/>')
 for key,x in plan['rooms'].items():
  polypts=' '.join('%.1f,%.1f'%co(p) for p in x['polygon'].exterior.coords)
  out.append(f'<polygon points="{polypts}" fill="{colors[x["z"]]}" opacity="0.30" stroke="#e9ecf0" stroke-width="3"/>')
  a,b=x['door'].coords
  ax,ay=co(a);bx,by=co(b)
  out.append(f'<line x1="{ax}" y1="{ay}" x2="{bx}" y2="{by}" stroke="#fff5b3" stroke-width="7"/>')
  p=x['polygon'].representative_point();xx,yy=co((p.x,p.y))
  out.append(f'<text x="{xx:.1f}" y="{yy:.1f}" fill="white" font-family="Arial" font-size="18">{key}</text>')
 for a,b,n,A,B in plan['stairs']:
  ax,ay=co(A[:2]);bx,by=co(B[:2])
  out.append(f'<line x1="{ax}" y1="{ay}" x2="{bx}" y2="{by}" stroke="#ffda87" stroke-width="7" stroke-dasharray="10 8"/>')
 out.extend(['<rect x="980" y="120" width="385" height="825" rx="12" fill="#192b3d" stroke="#51677e"/>',
 '<text x="1010" y="166" fill="white" font-size="21" font-family="Arial">Floor datum levels</text>'])
 for i,(z,color) in enumerate(colors.items()):
  y=220+i*90
  out.append(f'<rect x="1010" y="{y-21}" width="38" height="26" fill="{color}"/>')
  out.append(f'<text x="1063" y="{y}" fill="white" font-size="20" font-family="Arial">z = {z:.1f} m</text>')
 out.extend(['<text x="1010" y="665" fill="#fff5b3" font-size="18" font-family="Arial">Yellow = shared doorway</text>',
 '<text x="1010" y="700" fill="#fff5b3" font-size="18" font-family="Arial">Dashed = stairs</text>',
 '<text x="1010" y="750" fill="#ffcece" font-size="17" font-family="Arial">No real walkability claim.</text>',
 '<text x="1010" y="788" fill="#ffcece" font-size="17" font-family="Arial">No support or G2/G3 QA.</text>',
 '<text x="1010" y="826" fill="#ffcece" font-size="17" font-family="Arial">No aesthetic approval.</text>','</svg>'])
 return '\n'.join(out)

def main():
 pa=argparse.ArgumentParser();pa.add_argument('--verify',action='store_true');pa.add_argument('--negatives',action='store_true');pa.add_argument('--build',action='store_true');args=pa.parse_args()
 plan=make_plan()
 r=report(plan)
 print(json.dumps(r,indent=2,ensure_ascii=False))
 if args.negatives:run_negative_controls()
 if args.build:
  if OUT.exists() and any(OUT.iterdir()):raise FileExistsError('A73 outputs are append-only: '+str(OUT))
  OUT.mkdir(parents=True,exist_ok=True)
  metrics=write_obj(plan,OUT/'a73_continuous_route_and_rooms.obj')
  (OUT/'a73_route_floor_door_plan.svg').write_text(diagram_svg(plan))
  r['mesh']=metrics;r['artifact_kind']='G0_EDITABLE_OBJ_TRUE_MESH_AND_SCHEMATIC_SVG_NOT_RENDERED_CYCLES'
  (OUT/'a73_manifest.json').write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n')
  print('A73_TECH_G0_DERIVED_CONNECTIVITY_AND_REAL_OBJ_SAVED__ART_HOLD')
if __name__=='__main__':main()
