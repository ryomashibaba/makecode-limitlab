"""Independent readback of persisted B11-R5 D1 meshes: deliberately limited audit."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import hashlib,json,math
import numpy as np
import trimesh
ROOT=Path(__file__).resolve().parent

def check(name):
 folder=ROOT/name
 man=json.loads((folder/'manifest.json').read_text())
 check={}
 for category,sha in man['part_sha256'].items():
  p=folder/(category+'.ply');m=trimesh.load(p,force='mesh',process=False)
  assert hashlib.sha256(p.read_bytes()).hexdigest()==sha
  assert len(m.faces)>0 and np.isfinite(m.vertices).all()
  area=m.area_faces
  check[category]={'faces':int(len(m.faces)),'zero_area_faces':int(np.sum(area<1e-6)), 'watertight':bool(m.is_watertight), 'is_winding_consistent':bool(m.is_winding_consistent), 'components':int(len(m.split(only_watertight=False)))}
 obj_sha=hashlib.sha256((folder/'model.obj').read_bytes()).hexdigest()
 assert obj_sha==man['obj_sha256']
 path=np.array([[-565,-330,28],[-392,-232,37],[-225,-162,58+(man['workshop_clear_height_input_m']-62)*.35],[-28,-50,78+(man['workshop_clear_height_input_m']-62)*.6],[128,81,112+(man['workshop_clear_height_input_m']-62)],[216,194,153+(man['workshop_clear_height_input_m']-62)]],float)
 slopes=np.abs(np.diff(path[:,2]))/np.linalg.norm(np.diff(path[:,:2],axis=0),axis=1)
 # This lower bound is not a ray-based evaluation of real headroom; it deliberately blocks false certification.
 low_roof_knot=58+(man['workshop_clear_height_input_m']-62)-10
 bound=low_roof_knot-27
 out={'variant':name,'obj_hash_verified':True,'meshes':check,'gallery_pitched_segments_percent':np.round(100*slopes,2).tolist(),
      'unverified_clearance_input_m':man['workshop_clear_height_input_m'], 'lowest_arch_section_minus_workshop_floor_m':bound,
      'clearance_certified':False,'rooms_certified':False,'continuous_walk_certified':False,'structural_support_certified':False,
      'G0_art':'REJECT__SHELF_ROOF_AND_FLOATING_UPPER_BOXES','S1_G1_G2_G3':'NOT_RUN','minecraft_construction':'FORBIDDEN'}
 (folder/'audit.json').write_text(json.dumps(out,indent=2,ensure_ascii=False))
 return out

out={x:check(x) for x in ['baseline','clearance_plus20']}
base=out['baseline'];more=out['clearance_plus20']
assert base['obj_hash_verified'] and more['obj_hash_verified']
assert base['gallery_pitched_segments_percent']!=more['gallery_pitched_segments_percent']
assert base['lowest_arch_section_minus_workshop_floor_m']<62
assert more['lowest_arch_section_minus_workshop_floor_m']<82
p=ROOT/'montage.png';imgs=[]
try:font=ImageFont.truetype('DejaVuSans.ttf',27)
except:font=ImageFont.load_default()
for i,x in enumerate(['macro','district','public_eye','upper_eye']):
 im=Image.open(ROOT/'baseline'/(x+'.png')).convert('RGB');im.thumbnail((870,560))
 tile=Image.new('RGB',(900,610),(16,24,37));tile.paste(im,((900-im.width)//2,45))
 ImageDraw.Draw(tile).text((16,10),['01 / CITY - macro','02 / DISTRICT - side','03 / PUBLIC - eye','04 / UPPER - eye'][i],font=font,fill=(230,231,233))
 imgs.append(tile)
canvas=Image.new('RGB',(1800,1220),(14,21,31))
for i,t in enumerate(imgs):canvas.paste(t,((i%2)*900,(i//2)*610))
canvas.save(p,optimize=True)
print(json.dumps({x:{'faces_by_parts':{k:v['faces'] for k,v in o['meshes'].items()},'slope_percent':o['gallery_pitched_segments_percent'],'clearance_delta_bound_m':o['lowest_arch_section_minus_workshop_floor_m']} for x,o in out.items()},indent=2))
