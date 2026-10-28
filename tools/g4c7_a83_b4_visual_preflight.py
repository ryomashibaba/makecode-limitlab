"""Independent A83-B4 2D visual disconnection counterexample. Never certifies true 3D."""
import json, math, xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/'artifacts'/'g4c7-a83-b4-authorial-frontage'

def area(poly):
    return abs(sum(x*y2-x2*y for (x,y),(x2,y2) in zip(poly,poly[1:]+poly[:1])))*.5

def polygons(path,min_area=2500):
    root=ET.parse(path).getroot()
    out=[]
    for el in root.iter():
        if el.tag.split('}')[-1]!='polygon':continue
        pts=[]
        for pair in el.attrib['points'].split():
            a,b=pair.split(',')
            pts.append((float(a),float(b)))
        if area(pts)>=min_area:out.append(pts)
    return out

def orientation(a,b,c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])

def between(a,b,c):
    return (min(a[0],b[0])-1e-8<=c[0]<=max(a[0],b[0])+1e-8
        and min(a[1],b[1])-1e-8<=c[1]<=max(a[1],b[1])+1e-8)

def segments_touch(a,b,c,d):
    o1,o2,o3,o4=(orientation(a,b,c),orientation(a,b,d),
                  orientation(c,d,a),orientation(c,d,b))
    if (o1>0)!=(o2>0) and (o3>0)!=(o4>0) and all(abs(o)>1e-8 for o in (o1,o2,o3,o4)):
        return True
    return any(abs(v)<1e-8 and between(u,w,z) for u,w,z,v
               in [(a,b,c,o1),(a,b,d,o2),(c,d,a,o3),(c,d,b,o4)])

def point_in(poly,p):
    x,y=p;inside=False
    for a,b in zip(poly,poly[1:]+poly[:1]):
        if abs(orientation(a,b,p))<1e-8 and between(a,b,p):return True
        if (a[1]>y)!=(b[1]>y):
            cross=a[0]+(y-a[1])*(b[0]-a[0])/(b[1]-a[1])
            if cross>=x:inside=not inside
    return inside

def intersect(a,b):
    if (max(x for x,_ in a)<min(x for x,_ in b)-1e-8 or
        max(x for x,_ in b)<min(x for x,_ in a)-1e-8 or
        max(y for _,y in a)<min(y for _,y in b)-1e-8 or
        max(y for _,y in b)<min(y for _,y in a)-1e-8):
        return False
    if any(segments_touch(p,q,r,s)
        for p,q in zip(a,a[1:]+a[:1])
        for r,s in zip(b,b[1:]+b[:1])):return True
    return point_in(a,b[0]) or point_in(b,a[0])

def components(shapes):
    pending=set(range(len(shapes)));out=[]
    while pending:
        seen=set();stack=[next(iter(pending))]
        while stack:
            i=stack.pop()
            if i in seen:continue
            seen.add(i)
            stack.extend(j for j in pending if j not in seen and intersect(shapes[i],shapes[j]))
        pending-=seen;out.append(sorted(seen))
    return out

def analyze():
    macro=polygons(ROOT/'macro_authorial_section.svg')
    eye=polygons(ROOT/'public_eye_authorial_section.svg')
    from g4c7_a83_b4_authorial_frontage import load,components as abstract_components
    d=load()
    nodeids=[n['id'] for n in d['public_nodes']]
    abstract=abstract_components(nodeids,d['links'])
    # Ground baseline y=725 is explicitly authored in public_eye_authorial_section.svg.
    floating_count=sum(max(y for _,y in poly)<724.0 for poly in eye)
    issues=[]
    if len(abstract)==1 and len(components(macro))>1:
        issues.append('ABSTRACT_NETWORK_CONNECTED_BUT_VISIBLE_MAIN_MASSES_DETACHED')
    if len(components(eye))>1:
        issues.append('PUBLIC_EYE_FRONTAGES_ARE_DISCONNECTED_2D_POLYGONS')
    if floating_count==len(eye):
        issues.append('PUBLIC_EYE_FOUR_MAIN_FORMS_DO_NOT_TOUCH_DRAWN_GROUND')
    # The 2D drawings are not two projections of one actual world-space mesh.
    issues.append('NO_SHARED_TRUE_3D_SCENE_FOR_MACRO_AND_PUBLIC_EYE')
    return {'stage':'A83_B4_VISUAL_FALSIFICATION_G0',
            'abstract_graph_components':len(abstract),
            'macro_main_polygons':len(macro),
            'macro_visible_components':len(components(macro)),
            'public_eye_main_polygons':len(eye),
            'public_eye_visible_components':len(components(eye)),
            'public_eye_unconnected_to_drawn_ground':floating_count,
            'reasons_to_stop_before_3d':issues,
            'authorial_2d_judgement':'PRE_3D_DESIGN_REJECT',
            'true_3d_art':'NOT_RUN','formal_art_adoptions':0,
            's1_g1_g2_g3':'NOT_RUN','minecraft_construction':'FORBIDDEN'}

if __name__=='__main__':print(json.dumps(analyze(),ensure_ascii=False,indent=2))
