"""D16 independent 2D geometric SUBSET gate, not full local generator or real 3D.
The complete source/GeoJSON/independent audit lives in the conversation ZIP.
"""
import json
from pathlib import Path
from shapely.geometry import Polygon, box, LineString, Point
GROUND=box(-336,0,336,18)
MAKER={
 'estuary':[(-301,99),(-267,112),(-198,108),(-119,105),(-80,94),(-80,103),(-124,117),(-201,122),(-275,122),(-305,109)],
 'terrace':[(-301,101),(-254,113),(-183,109),(-109,98),(-79,103),(-83,118),(-175,128),(-267,126),(-303,114)]}
RESEARCH={
 'estuary':[(80,96),(113,110),(190,119),(269,111),(300,95),(302,110),(272,128),(186,134),(109,124),(80,109)],
 'terrace':[(80,105),(115,121),(209,116),(274,104),(295,95),(303,109),(271,123),(200,133),(115,134),(80,119)]}
RESEARCH_BEARING=Polygon([(170,18),(186,18),(222,116),(202,120)])
CORES={'E1':box(-265,18,-247,221),'E2':box(247,18,265,221)}
def witness(v):
 maker=Polygon(MAKER[v]);research=Polygon(RESEARCH[v])
 assert maker.is_valid and research.is_valid and maker.disjoint(research)
 d=research.area
 assert round(d,1)=={'estuary':3449.,'terrace':3425.5}[v]
 assert RESEARCH_BEARING.area==1868.0
 assert d/(maker.area+research.area)>.15
 assert RESEARCH_BEARING.intersects(GROUND)
 eye=(-7,24.65)
 for x in (-148,148):
  for dz in (-2,0,2):
   ray=LineString([eye,(x,28+dz)])
   assert all(not q.intersects(ray) for q in [maker,research,*CORES.values()])
 sky=LineString([(0,25),(0,265)])
 assert all(not q.intersects(sky) for q in [maker,research,*CORES.values()])
 assert box(-12,90,12,101).intersects(sky)
 for name,core in CORES.items():
  x=-256 if name=='E1' else 256
  for z in (20,132,206):
   landing=box(x-15,z-1,x+15,z+1)
   assert core.intersects(landing) and core.contains(Point(x,z))
 assert not box(308,131,340,133).intersects(CORES['E2'])
 return {'variant':v,'canopy_area_removed_m2':round(d,1),'bearing_area_removed_m2':1868.,
   'sky_subset_ray_clear':True,'six_core_landing_slice_witnesses':True,
   'two_cones_three_rays_each_subset_clear':True,
   'scope':'INDEPENDENT_2D_SUBSET_ONLY','art':'PRE-3D ART REJECT',
   'formal_QA':'NOT_RUN','Minecraft':'FORBIDDEN'}
if __name__=='__main__':
 out={'stage':'B11-R5 D16','variants':[witness(v) for v in ('estuary','terrace')],
 'full_local_source_present_in_GitHub':False,'true_3D':'NOT_RUN','G0':'NOT_RUN',
 'adopted':0,'overall':'ART HOLD','construction':'FORBIDDEN'}
 Path('d16_subset_results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
 print('D16 independent subset PASS; full pre-3D source in ZIP, NO ART/QA/CONSTRUCTION')
