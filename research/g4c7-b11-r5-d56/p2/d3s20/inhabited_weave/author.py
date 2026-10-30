"""G4-C7 / D3S20 inhabited weave exploratory authoring model.
Research only. Does NOT establish ART pass, Minecraft construction, continuous
human safe walking, or structural engineering. XYZ: X east, Y north, Z up.
Public connective graph + inhabited room/outer mass are derived from one plan.
"""
from __future__ import annotations
import json, argparse, hashlib
from pathlib import Path
import numpy as np
import trimesh

COLOR={'road':[90,116,132,255], 'street_edge':[191,160,113,255],
 'civic':[199,165,113,255],'culture':[204,138,125,255],
 'market':[198,172,114,255],'forge':[111,137,158,255],
 'research':[107,169,182,255],'residence':[174,179,157,255],
 'education':[170,147,184,255],'terrace':[107,122,134,255],
 'rail':[208,190,146,255],'glazing':[104,201,213,195],
 'garden':[84,150,117,255],'support':[66,82,106,255],
 'solar':[112,163,177,255]}
# A graph, not disconnected blocks. Edge 'segment positions' control both street
# geometry and adjacently inhabited room orientation and entrance (one source).
BASE={
 'nodes':{'W':[-320,-77,10], 'F':[-210,-52,10], 'C':[-45,-10,10],
  'R':[105,55,10], 'E':[310,129,10], 'S':[-148,-191,10],
  'T':[245,-150,10], 'M':[-115,133,10], 'G':[65,191,10],
  'N':[-57,221,10], 'D':[-185,62,10]},
 'edges':[['W','F'],['F','C'],['C','R'],['R','E'],['S','F'],
  ['S','C'],['C','M'],['M','G'],['G','R'],['R','T'],['T','C'],
  ['F','D'],['D','M'],['M','N'],['N','G']],
 'programs':[
  ['forge','F','C', 1,  44,60,55,1],
  ['civic_hall','C','R',-1, 57,69,63,2],
  ['exchange','C','M', 1, 40,53,32,3],
  ['culture','M','G',-1, 39,60,53,4],
  ['learning','G','N', 1, 36,55,38,5],
  ['research','R','E', 1, 51,61,69,6],
  ['habitat','R','G',-1, 39,62,48,7],
  ['transit','T','R',-1, 38,64,36,8],
  ['civic_workshop','F','D',1,31,48,34,9],
  ['garden_housing','D','M',-1,39,43,39,10],
  ['public_service','C','S',1,30,49,35,11],
  ['orbital_studio','G','R',1,40,56,60,12],
 ],
 'ground_z':10, 'street_width':18, 'portal_width':12,
 'research_span':1.0,
}

def plan(**updates):
 import copy
 p=copy.deepcopy(BASE)
 # Coupled changes modify the same node which anchors both streets and rooms.
 # The second test changes a room's functional width; its incident street
 # clearance is derived from this width (bounded to avoid nonsensical widths).
 if 'research_shift_y' in updates: p['nodes']['R'][1]+=updates['research_shift_y']
 if 'research_span' in updates:p['research_span']=updates['research_span']
 return p

def prism_poly(pts,z0,z1):
 p=np.array(pts,float);n=len(p)
 verts=np.array([[*xy,z] for z in (z0,z1) for xy in p],float)
 faces=[]
 for i in range(1,n-1):faces.extend([[0,i+1,i],[n,n+i,n+i+1]])
 for i in range(n):j=(i+1)%n;faces.extend([[i,j,i+n],[j,j+n,i+n]])
 return trimesh.Trimesh(vertices=verts,faces=faces,process=False)

def world(local_center,t,n,u,v):return np.array(local_center)+u*t+v*n

class Builder:
 def __init__(self):self.scene=trimesh.Scene();self.meta=[]
 def add(self,name,mesh,color,role):
  mesh.visual.face_colors=COLOR[color]
  self.scene.add_geometry(mesh,geom_name=name,node_name=name)
  self.meta.append({'name':name,'role':role,'color':color})
 def box(self,name,xyz,ext,c,role='solid',angle=0):
  mesh=trimesh.creation.box(extents=ext)
  if angle:mesh.apply_transform(trimesh.transformations.rotation_matrix(angle,[0,0,1]))
  mesh.apply_translation(xyz)
  self.add(name,mesh,c,role)
 def poly(self,name,xy,z0,z1,c,role='solid'):self.add(name,prism_poly(xy,z0,z1),c,role)
 def strip(self,name,a,b,width,z,c='road',thick=1.2):
  a,b=np.asarray(a,float),np.asarray(b,float)
  d=b[:2]-a[:2];norm=np.linalg.norm(d);n=np.array([-d[1],d[0]])/norm
  pts=[a[:2]-n*width/2,b[:2]-n*width/2,b[:2]+n*width/2,a[:2]+n*width/2]
  self.poly(name,pts,z-thick,z,c,'road')
 def room(self,name,station,other,side,width,depth,height,typ,span,street_width):
  a,b=np.asarray(station,float),np.asarray(other,float)
  t=(b[:2]-a[:2]);t/=np.linalg.norm(t);n=np.array([-t[1],t[0]])*side
  ang=np.arctan2(t[1],t[0]);w=width*(span if typ==6 else 1)
  near=street_width/2-2;far=near+depth
  c=world(a[:2],t,n,0,(near+far)/2)
  def bx(tag,u,v,z,ew,ed,eh,col,role='solid'):
   xy=world(a[:2],t,n,u,v)
   # x axis orientation tangent, y axis orientation n (if side opposite mirrored)
   self.box(name+'_'+tag,[*xy,z],[ew,ed,eh],col,role,ang if side>0 else ang+np.pi)
  col= {1:'forge',2:'civic',3:'market',4:'culture',5:'education',6:'research',7:'residence',8:'market',9:'forge',10:'residence',11:'civic',12:'research'}[typ]
  z=a[2]
  bx('floor',0,(near+far)/2,z-1,w,depth,2,'terrace','room_floor')
  # Front wall is broken by a genuinely empty 12-wide entrance.
  door=max(12,min(16,w*.24));sidew=(w-door)/2
  for i in (-1,1):
   bx(f'front_{i}',i*(door/2+sidew/2),near,z+height/2,sidew,2,height,col,'room_wall')
   bx(f'side_{i}',i*w/2,(near+far)/2,z+height/2,2,depth,height,col,'room_wall')
  bx('front_over_door',0,near,z+(height+13)/2,door,2,height-13,col,'room_wall')
  bx('back',0,far,z+height/2,w,2,height,col,'room_wall')
  # Distinct roofs and inhabited tiers, not generic floor repetition.
  if typ in (1,9):
   # Sawtooth hangar skylight geometry, structural frames indicate large internal clearance.
   for k in range(3):
    bx(f'hangar_roof_{k}',-w*.31+k*w*.31,(near+far)/2,z+height+4+(k%2)*5,w*.34,depth+3,2,'support','roof')
   for k in range(4):bx(f'roof_light_{k}',-w*.3+k*w*.2,(near+far)/2,z+height+10,w*.11,depth*.8,.5,'glazing','skylight')
  elif typ in (2,3,4,5,8,11):
   # Partial roof leaves a usable, open-air interior/civic court.
   bx('canopy',-w*.22,(near+far)/2,z+height+2,w*.52,depth+2,2,col,'roof')
   bx('solar_veil',w*.24,(near+far)*.57,z+height+13,w*.3,depth*.55,1,'glazing','skylight')
  else:
   bx('roof_slab',0,near+depth*.62,z+height+2,w*.88,depth*.72,1.8,col,'roof')
   for k in range(3):
    bx(f'overlook_{k}',-w*.24+k*w*.22,near+depth*(.54+.08*k),z+height+11+6*k,w*.19,depth*.17,1.5,'glazing','skylight')
  # Portal supplied to independent verification, and roof/metaparam have common source.
  portal=[*world(a[:2],t,n,0,near),z+2.2]
  return {'name':name,'portal':portal,'station':a.tolist(),'ground_z':z,'width':w,
          'depth':depth,'height':height,'type':typ,'far':far,'near':near,
          'plan_tangent':t.tolist(),'plan_normal':n.tolist(),'door_clearance':door}

def build(dest, config=None):
 p=config if config is not None else plan();dst=Path(dest);dst.mkdir(parents=True,exist_ok=True)
 B=Builder();nodes={k:np.array(v,dtype=float) for k,v in p['nodes'].items()}
 streetwidth=p['street_width']
 for i,(s,e) in enumerate(p['edges']):
  w=streetwidth+(7*(p['research_span']-1) if 'R' in (s,e) else 0)
  B.strip(f'public_{i:02d}_{s}_{e}',nodes[s],nodes[e],w,nodes[s][2],'road')
 for k,v in nodes.items():
  w=(30 if k in ['C','M','R'] else 23)
  B.poly('meeting_'+k,[v[:2]+[u,vv] for u,vv in [(-w/2,-w/2),(w/2,-w/2),(w/2,w/2),(-w/2,w/2)]],v[2]-1.35,v[2],'street_edge','public_ground')
 # Consistent street-frame and localized inhabited architecture rather than detached pavilions.
 meta=[]
 for name,anchor,adj,side,w,d,h,typ in p['programs']:
  rw=streetwidth+(7*(p['research_span']-1) if anchor=='R' or adj=='R' else 0)
  # Dedicated frontage on the SAME connected roadway segment; avoid
  # placing independent portals on the same node and blocking each other.
  frontage={'civic_workshop':0.75,'public_service':0.43}.get(name,0.0)
  room_anchor=nodes[anchor]+frontage*(nodes[adj]-nodes[anchor])
  meta.append(B.room(name,room_anchor,nodes[adj],side,w,d,h,typ,p['research_span'],rw))
 # Additional urban tiers that overlap the structure of three inhabited districts, but
 # never count as accessible floors; stairs and egress are explicitly NOT BUILT.
 for k,(node,levels,width) in enumerate([('F',[93,125],49),('C',[112,157,192],61),
                                           ('R',[98,140,193,232],49),('M',[100,134],37),('G',[94,130],34)]):
  x,y,_=nodes[node]
  for i,z in enumerate(levels):
   ang=(k*.31+i*.21)
   # asymmetrical crescent balcony segments, not linear cloned tower stacks.
   for j in range(3):
    theta=ang+j*.55
    a=np.array([x+np.cos(theta)*width*.43,y+np.sin(theta)*width*.43])
    b=np.array([x+np.cos(theta+.28)*width*.7,y+np.sin(theta+.28)*width*.7])
    B.strip(f'upper_urban_terrace_{k}_{i}_{j}',[*a,z],[*b,z],8,z,'terrace',1.8)
  # Thin frame rail and light fins, still unqualified for support.
  for j in range(4):
   theta=.3+j*1.4
   xx=x+width*.58*np.cos(theta);yy=y+width*.58*np.sin(theta)
   B.box(f'urban_frame_{k}_{j}',[xx,yy,50+k*5],[1.6,1.6,65+20*(k%3)],'support','frame')
 # Midscale interstitial courtyard bands: derive from actual paired public nodes, never standalone towers.
 for i,(a,b) in enumerate([('F','C'),('C','R'),('M','G'),('D','M'),('R','G'),('C','T')]):
  st,ed=nodes[a],nodes[b];mid=(st[:2]+ed[:2])/2
  d=(ed[:2]-st[:2]);d=d/np.linalg.norm(d);n=np.array([-d[1],d[0]])
  for side in (-1,1):
   for j in range(2):
    pos=mid + n*side*(31+13*j) + d*(14*j-8)
    width=(19+5*(j==1)+2*(i%3)); height=21+(i*19+j*13)%38
    B.box(f'interstitial_{i}_{side}_{j}_floor',[*pos,9.3],[width,22,1.8],'terrace','urban_infill')
    for sgn in (-1,1):
     q=pos+n*(width*.48*sgn)
     B.box(f'interstitial_{i}_{side}_{j}_side_{sgn}',[*q,10+height/2],[1.6,22,height],'residence' if i%2 else 'culture','urban_infill_wall')
    B.box(f'interstitial_{i}_{side}_{j}_roof',[*pos,11+height],[width,22,1.3],'glazing','roof')
 glb=dst/'INHABITED_WEAVE.glb';B.scene.export(glb)
 recovered=trimesh.load_scene(glb)
 meshes=list(recovered.geometry.values());tri=sum(len(m.faces) for m in meshes)
 bbox=recovered.bounds
 summary={'study':'D3S20_INHABITED_WEAVE','status':'ART_NOT_APPROVED','reference_frame':'concept XYZ, not Minecraft construction coordinates',
  'author_geometry':len(B.scene.geometry),'reloaded_geometry':len(meshes),'reloaded_triangles':tri,
  'saved_glb_bytes':glb.stat().st_size,'saved_glb_sha256':hashlib.sha256(glb.read_bytes()).hexdigest(),
  'bounds':bbox.tolist(),'programmes':meta,'public_edges':p['edges'],
  'complete_usable_rooms':'NOT_VERIFIED','safe_continuous_human_routes':'NOT_VERIFIED',
  'stairs_landings':'NOT_BUILT','331_993_GATES':'NOT_RUN','Minecraft_construction':'PROHIBITED',
  'unknowns':'structural loading, stairs, building support, room air-volume continuum, MakeCode full conversion, art approval'}
 (dst/'AUDIT.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding='utf-8')
 return summary

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--out',default=str(Path(__file__).resolve().parent));ap.add_argument('--research-shift-y',type=float,default=0);ap.add_argument('--research-span',type=float,default=1)
 args=ap.parse_args();result=build(args.out,plan(research_shift_y=args.research_shift_y,research_span=args.research_span))
 print(json.dumps({k:v for k,v in result.items() if k not in ['programmes','public_edges']},indent=2))