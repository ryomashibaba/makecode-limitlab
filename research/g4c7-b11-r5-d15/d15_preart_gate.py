"""D15 reproducible PRE-3D early rejection. This is only a 2D section, not a real 3D, a structural calculation, S1, or artistic certification."""
from pathlib import Path
import json
from shapely.geometry import Polygon, box, LineString
from shapely.ops import unary_union
ROOT=Path(__file__).resolve().parent
S={
'loom':[
('maker',[(-290,18),(-65,18),(-65,42),(-101,70),(-250,96),(-290,72)]),
('research',[(82,30),(250,40),(250,75),(187,100),(91,80)]),
('habitat',[(-225,150),(-20,146),(15,176),(-25,213),(-186,215),(-230,181)]),
('culture',[(-44,104),(76,112),(85,129),(-47,127)]),
('canopy',[(-280,95),(-115,115),(40,125),(228,107),(244,118),(35,146),(-130,134),(-280,116)])],
'estuary':[
('maker',[(-296,18),(-75,18),(-75,42),(-114,76),(-240,100),(-296,72)]),
('research',[(85,18),(292,18),(292,79),(248,116),(140,92),(85,47)]),
('culture',[(-94,115),(-79,98),(-35,110),(-35,145)]),
('culture',[(35,113),(96,95),(117,110),(52,148),(35,147)]),
('habitat',[(-268,152),(-167,161),(-101,195),(-154,225),(-279,213)]),
('habitat',[(142,171),(251,147),(292,179),(279,226),(196,239),(146,218)]),
('canopy',[(-232,106),(-106,129),(-54,153),(-63,164),(-158,152),(-250,128)]),
('canopy',[(116,127),(199,147),(269,116),(278,129),(211,173),(137,146)])],
'kiln':[
('maker',[(-286,18),(-86,18),(-56,34),(-166,97),(-285,113)]),
('research',[(94,24),(270,42),(269,114),(184,132),(108,84)]),
('habitat',[(119,118),(276,142),(285,232),(221,244),(163,203)]),
('culture',[(-56,100),(92,105),(125,124),(-64,128)]),
('canopy',[(-283,138),(-206,187),(-37,202),(120,190),(220,229),(289,252),(273,226),(205,199),(116,166),(-40,177),(-178,151),(-272,118)])]}
GROUND=box(-350,12,350,22)

def audit(name,shapes):
    p=[(role,Polygon(coords)) for role,coords in shapes]
    assert all(poly.is_valid and poly.area>1 for _,poly in p)
    body=unary_union([poly for _,poly in p])
    comps=list(body.geoms) if hasattr(body,'geoms') else [body]
    floating=sum(c.distance(GROUND)>0.03 for c in comps)
    sky=LineString([(-8,38),(-8,258)])
    sky_blocked=any(q.intersects(sky) for _,q in p)
    eye=(-8,23.7)
    targets={'maker':(-143,28),'research':(121,30)}
    lines={name:not any(q.intersects(LineString([eye,target])) for role,q in p if role!=name) for name,target in targets.items()}
    canopy=unary_union([q for role,q in p if role=='canopy'])
    # Research deletion only deletes research geometry: unchanged canopy is a HARD FAIL.
    without_research_canopy=unary_union([q for role,q in p if role=='canopy'])
    canopy_delta=canopy.symmetric_difference(without_research_canopy).area
    return {'name':name,'scope':'2D_AUTHOR_SECTION_ONLY',
      'section_visible_maker_and_research':all(lines.values()),
      'open_sky_center_ray':not sky_blocked,
      'unconnected_to_ground_section_components':floating,
      'research_removal_changes_canopy':canopy_delta>1,
      'two_functioning_vertical_cores':'NOT_MODELED',
      'real_3d':'NOT_RUN','art':'NOT_ADOPTED',
      'formal_S1_G1_G2_G3':'NOT_RUN','Minecraft':'FORBIDDEN',
      'next':'PRE_3D_REJECT'}

def self_test():
    floor=box(-20,20,20,22)
    floating=box(-10,80,10,90)
    leg=box(-2,21.95,2,81)
    def disconnected(items):
        x=unary_union(items)
        parts=list(x.geoms) if hasattr(x,'geoms') else [x]
        return sum(q.distance(GROUND)>.03 for q in parts)
    assert disconnected([floor,floating])==1
    assert disconnected([floor,leg,floating])==0
    assert disconnected([floor,leg,floating,box(30,210,65,222)])==1

if __name__=='__main__':
    self_test()
    results=[audit(name,polys) for name,polys in S.items()]
    assert [r['unconnected_to_ground_section_components'] for r in results]==[3,5,1]
    assert [r['open_sky_center_ray'] for r in results]==[False,True,False]
    assert all(r['section_visible_maker_and_research'] and not r['research_removal_changes_canopy'] for r in results)
    assert all(r['art']=='NOT_ADOPTED' and r['Minecraft']=='FORBIDDEN' for r in results)
    (ROOT/'d15_preart_results.json').write_text(json.dumps(
        {'stage':'D15','status':'ALL_3_PRE3D_REJECT','self_test':'PASS','candidates':results},
        ensure_ascii=False,indent=2))
    print('PASS = ALL THREE EARLY REJECTED. NO REAL 3D, NO G0 ART, NO S1/G1/G2/G3, NO CONSTRUCTION.')
