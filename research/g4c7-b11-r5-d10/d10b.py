"""D10B fresh non-adopted function-first full-3D mock-up. NOT a city/artwork.
Dedicated common-eye sightlines, two physical shaft frames + three landings,
ground and research-height connected-floor *candidate* (no functioning lifts).
"""
from pathlib import Path
import json,hashlib
import numpy as np,trimesh
P=Path(__file__).resolve().parent/'d10b';P.mkdir(exist_ok=True)
COLOR={'ground':(57,71,80,255),'floor':(226,192,129,255),'maker':(220,143,110,255),
'research':(114,177,214,255),'structure':(122,149,174,255),'glass':(93,214,210,175),
'machine':(230,95,90,255),'core':(105,172,183,255),'habitat':(168,195,157,255)}
parts={k:[] for k in COLOR}
def add(m,k):m.visual.vertex_colors=np.tile(COLOR[k],(len(m.vertices),1));parts[k].append(m)
def box(c,d,k):
 m=trimesh.creation.box(extents=d);m.apply_translation(c);add(m,k)
def rod(a,b,r,k):add(trimesh.creation.cylinder(radius=r,segment=[a,b],sections=9),k)
def ribbon(points,w,k,thickness=.8):
 for a,b in zip(points,points[1:]):
  a=np.array(a,float);b=np.array(b,float);d=b-a;u=np.array([-d[1],d[0],0])/np.linalg.norm(d[:2])*w/2
  top=np.array([a-u,a+u,b+u,b-u]);bot=top-[0,0,thickness];v=np.vstack([top,bot]);f=[]
  for j in range(1,3):f.extend([[0,j,j+1],[4,4+j+1,4+j]])
  for j in range(4):q=(j+1)%4;f.extend([[j,q,q+4],[j,q+4,j+4]])
  add(trimesh.Trimesh(vertices=v,faces=f,process=False),k)
def main():
 box((0,0,15),(600,440,5),'ground')
 # Ground-level public promenade, both lift lobbies geometrically touching the same floor.
 ribbon([(-235,20,18),(-120,20,18),(-20,20,18),(95,20,18),(140,20,18),(235,20,18)],12,'floor')
 # More than a label: actual maker floor, open frontage and sculptural machinery.
 box((-145,-118,19),(222,160,2),'maker')
 box((-154,-123,23),(36,32,6),'machine')
 box((-100,-139,28),(42,20,14),'machine')
 rod((-156,-118,26),(-156,-118,60),1.8,'machine')
 for x in (-238,-36):
  for y in (-184,-74):rod((x,y,18),(x,y,90),1.8,'structure')
 # Maker's roof underside at z89, physical floor top z20 =>69m. Use 90m roof for 70m margin.
 box((-146,-126,94),(218,150,8),'structure')
 # Wide northward opening: only top and corner supports, no solid sightline wall.
 ribbon([(-140,20,18),(-140,-21,18),(-140,-49,18)],7,'floor')
 # Ground research demonstration is on same lived public level, exposed without wall.
 box((96,93,19),(142,100,2),'research')
 for x in (66,105,140):box((x,91,23),(16,14,5),'research')
 ribbon([(95,20,18),(95,49,18),(95,79,18)],8,'floor')
 # Actual upper-floor promenade connects the two core frames with one continuous surface.
 ribbon([(-120,20,112),(-20,20,112),(95,20,112),(140,20,112)],14,'floor')
 # Research upper floor directly attached to transfer corridor (touching strip 20..74).
 box((110,63,111.4),(110,85,1.2),'research')
 ribbon([(96,20,112),(96,45,112),(96,65,112)],9,'floor')
 box((108,70,119),(70,22,14),'research')
 box((108,58,118),(60,1.6,12),'glass')
 # A sky-level public terrace, explicitly not pretending there are rooms/true residence.
 ribbon([(-120,20,209),(-20,20,209),(95,20,209),(140,20,209)],12,'floor')
 box((95,55,208.5),(80,70,1),'habitat')
 ribbon([(95,20,209),(95,55,209)],8,'floor')
 for x in (-120,140):
  for dx in (-6,6):
   for dy in (-6,6):rod((x+dx,20+dy,18),(x+dx,20+dy,212),.65,'core')
  for z in (18,112,209):box((x,20,z-.6),(14,14,1.2),'core')
 # No fake actual lift cars or doors. Program stays on HOLD.
 scene=trimesh.Scene();meshes=[];cat={}
 for k,arr in parts.items():
  if not arr:continue
  m=trimesh.util.concatenate(arr);meshes.append(m);scene.add_geometry(m,geom_name=k)
  m.export(P/f'{k}.ply');cat[k]=hashlib.sha256((P/f'{k}.ply').read_bytes()).hexdigest()
 full=trimesh.util.concatenate(meshes);full.export(P/'study.obj');scene.export(P/'study.glb')
 manifest={'name':'D10B function-first local nucleus NOT artwork','faces':len(full.faces),'bounds_m':full.bounds.tolist(),
  'sha256_obj':hashlib.sha256((P/'study.obj').read_bytes()).hexdigest(),
  'sha256_glb':hashlib.sha256((P/'study.glb').read_bytes()).hexdigest(),
  'ply_sha256':cat,'public_eye_xyz':[-20,20,21.7],
  'maker_target_xyz':[-154,-123,26],'research_target_xyz':[95,91,22],
  'upper_floor_target_z':112,'roof_soffit_target_z':90,
  'formal_qa':'NOT_RUN','art':'NOT_ADOPTED','minecraft':'FORBIDDEN',
  'unsupported':['elevator transport is a schematic shaft frame','no structure loads','no emergency egress',
  'not a certified walkable route','not entire city','not human-safe machinery']}
 (P/'manifest.json').write_text(json.dumps(manifest,indent=2))
 print('built',manifest['faces'],manifest['bounds_m'])
if __name__=='__main__':main()