"""D49: a changed rendering is not beautiful or a genuinely enclosed interior.
Independent, descriptive review gate on saved D48 files. Optional D46 re-render comparisons.
"""
import argparse,hashlib,json
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
import trimesh
from shapely.geometry import MultiPoint,Point
VIEWS=['01_overall','02_arrival','03_civic_eye','04_maker_eye','05_research_eye','06_upper_room']


def load(p):
 s=trimesh.load(p,force='scene',process=False);d={}
 for node in s.graph.nodes_geometry:
  T,key=s.graph[node];m=s.geometry[key].copy();m.apply_transform(T);d[str(node)]=m
 return d

def analyse(build,prior):
 d=load(build/'d48_baseline.glb')
 # Shadow test uses actual saved mesh triangles' overhead projected footprints, excluding mere site/upper stairs.
 witnesses=[(0,-13,3.0),(0,-3,3.0),(0,8,3.0),(0,15,3.0)]
 exposed=[]
 for x,y,z in witnesses:
  overhead=[]
  for n,m in d.items():
   if n=='shared__site' or n.startswith('shared__garden') or n.startswith('shared__stair'):continue
   if m.bounds[1,2]<=z+.3:continue
   # Approx footprint; physical overhead is not enough to certify rain protection.
   poly=MultiPoint(m.vertices[:,:2]).convex_hull
   if poly.buffer(.001).covers(Point(x,y)):overhead.append(n)
  exposed.append({'sample_xy':(x,y),'overhead_footprint_candidates':overhead})
 # Public area is dominated by an open-sky street: large open air fraction is a spatial fact, not quality metric.
 open_count=sum(not v['overhead_footprint_candidates'] for v in exposed)
 assert open_count>=2, 'Stop gate no longer confirms an open-air main public space; inspect actual mesh/image and update research'
 result={'stage':'D49','local_case':'D48 Civic Rift Loom','public_indoor_witnesses':exposed,
         'public_footprint_samples_without_overhead':open_count,
         'claimed_enclosed_shared_civic_room':'FAIL',
         'artist_decision':'PRE_G0_REJECT','reason':'rendered design remains open-air corridor with two flanking building-like masses',
         'formal_art_G0':'NOT_RUN','adopted':0,'construction':'FORBIDDEN'}
 if prior and prior.is_dir():
  comparisons={}
  for v in VIEWS:
   old=np.asarray(Image.open(prior/(v+'.png')).convert('RGB'),dtype=np.int16)
   new=np.asarray(Image.open(build/(v+'.png')).convert('RGB'),dtype=np.int16)
   assert old.shape==new.shape, (v,old.shape,new.shape)
   delta=np.abs(new-old)
   comparisons[v]={'changed_pixels_gt20_rgb_pct':round(float((delta.max(axis=2)>20).mean()*100),3),
       'mean_rgb_absolute_difference':round(float(delta.mean()),3)}
  result['same_camera_D46B_to_D48_visual_difference']=comparisons
  # Genuine geometrical redesign does NOT imply aesthetic success or habitable indoor enclosure.
  oldd=load('/mnt/data/d46_study/build/d46_b_baseline.glb') if Path('/mnt/data/d46_study/build/d46_b_baseline.glb').is_file() else {}
  result['prior_D46_B_nodes_available_locally']=len(oldd)
  result['new_D48_nodes']=len(d)
  result['relative_visual_change_does_not_imply_art_pass']=True
  w=600;h=382;image=Image.new('RGB',(w*2,(h+32)*3),'#f1f1ef');dr=ImageDraw.Draw(image)
  for i,key in enumerate(('01_overall','03_civic_eye','06_upper_room')):
   for j,p in enumerate((prior,build)):
    f=Image.open(p/(key+'.png')).convert('RGB');f.thumbnail((w,h));x=j*w;y=i*(h+32)+32
    image.paste(f,(x,y));dr.text((x+9,y-23),f'{"D46B" if j==0 else "D48"} | {key}',fill='#192b2b')
  image.save(build/'D49_D46B_to_D48_same_camera_6views.png')
 (build/'d49_public_interior_stop_result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 assert result['claimed_enclosed_shared_civic_room']=='FAIL'
 assert result['artist_decision']=='PRE_G0_REJECT'
 return result

def main():
 a=argparse.ArgumentParser();a.add_argument('--out',default='d48_build');a.add_argument('--prior-render-dir');opts=a.parse_args();r=analyse(Path(opts.out),Path(opts.prior_render_dir) if opts.prior_render_dir else None)
 print(f'D49 ART STOP: {r["public_footprint_samples_without_overhead"]}/4 public overhead witness samples open; no indoor civic adoption')
if __name__=='__main__':main()
