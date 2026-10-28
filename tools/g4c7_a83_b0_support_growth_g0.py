"""A83-B0 source feasibility study. No actual room, load certification, art or Minecraft action."""
import hashlib
import json
from math import cos, hypot, isfinite, pi, sin

MAX_DESIGN_GRADE = 0.08
MIN_HEADROOM = 4.0

def _area(poly):
    return abs(sum(a[0]*b[1]-b[0]*a[1]
                   for a,b in zip(poly,poly[1:]+poly[:1])))/2

def _inside(poly,x,y):
    # Source uses convex polygons; inclusive on an edge.
    sign=None
    for a,b in zip(poly,poly[1:]+poly[:1]):
        c=(b[0]-a[0])*(y-a[1])-(b[1]-a[1])*(x-a[0])
        if abs(c)<1e-6:continue
        if sign is None:sign=c>0
        elif sign!=(c>0):return False
    return sign is not None

def _point(p):
    return len(p)==3 and all(isinstance(v,(int,float)) and isfinite(v) for v in p)

def _issues(model):
    problems=[]
    districts=model.get('districts',[])
    if len(districts)!=3 or len({d.get('id') for d in districts})!=3:
        problems.append('DISTRICT_COUNT_OR_DUPLICATE')
    zones=model.get('zones',[])
    ids=[z.get('id') for z in zones]
    if len(ids)!=len(set(ids)) or len(zones)<6:problems.append('ZONE_ID_OR_COUNT')
    lookup={z.get('id'):z for z in zones}
    for d in districts:
        zs=[z for z in zones if z.get('district')==d.get('id')]
        if len(zs)<2 or len({z.get('program') for z in zs})<2 or len({z.get('floor_z') for z in zs})<2:
            problems.append('NOT_MULTIPROGRAM_MULTILEVEL:'+str(d.get('id')))
    for z in zones:
        poly=z.get('footprint',[])
        try:
            valid=(len(poly)>=3 and all(len(p)==2 and all(isfinite(v) for v in p) for p in poly)
                and _area(poly)>=700 and z['ceiling_z']-z['floor_z']>=MIN_HEADROOM
                and z['floor_z']>0)
        except (TypeError,KeyError,ValueError):
            valid=False
        if not valid:problems.append('INVALID_OCCUPIED_VOLUME_SEED:'+str(z.get('id')))
    supports=model.get('supports',[])
    for z in zones:
        good=[]
        for s in supports:
            if s.get('zone')!=z.get('id'):continue
            p=s.get('path',[])
            if len(p)<2 or not all(_point(q) for q in p):continue
            if abs(p[0][2])>1e-6 or abs(p[-1][2]-z['floor_z'])>1e-6:continue
            if any(b[2]<=a[2] for a,b in zip(p,p[1:])):continue
            if not _inside(z['footprint'],p[-1][0],p[-1][1]):continue
            good.append(s)
        if len(good)<2 or hypot(good[0]['path'][0][0]-good[1]['path'][0][0],
                               good[0]['path'][0][1]-good[1]['path'][0][1])<8:
            problems.append('UNROOTED_OR_DETACHED_SUPPORT:'+str(z.get('id')))
    for d in districts:
        links=[r for r in model.get('routes',[]) if r.get('district')==d.get('id')]
        valid=False
        for r in links:
            a,b=lookup.get(r.get('from')),lookup.get(r.get('to'))
            pts=r.get('path',[])
            if not a or not b or len(pts)<2 or not all(_point(p) for p in pts):continue
            if a.get('district')!=d.get('id') or b.get('district')!=d.get('id'):continue
            if abs(pts[0][2]-a['floor_z'])>1e-6 or abs(pts[-1][2]-b['floor_z'])>1e-6:continue
            if not _inside(a['footprint'],*pts[0][:2]) or not _inside(b['footprint'],*pts[-1][:2]):continue
            slopes=[]
            for u,v in zip(pts,pts[1:]):
                dist=hypot(v[0]-u[0],v[1]-u[1])
                slopes.append(float('inf') if dist<1e-8 else abs(v[2]-u[2])/dist)
            if max(slopes)<=MAX_DESIGN_GRADE and a['floor_z']!=b['floor_z']:
                valid=True
        if not valid:problems.append('NO_GRADE_FEASIBLE_DESIGN_ROUTE:'+str(d.get('id')))
    if any(model.get(s) for s in ('art_pass','formal_g2_pass','minecraft_construction_enabled')):
        problems.append('FORBIDDEN_CLAIM_OR_CONSTRUCTION')
    return problems

def evaluate(model):
    problems=_issues(model)
    # These anchors are source witnesses, not a facade, watertight rooms or true triangles.
    anchors=[]
    for z in sorted(model.get('zones',[]),key=lambda z:z['id']):
        for x,y in z.get('footprint',[]):
            anchors.append((z['id'],round(x,6),round(y,6),round(z['floor_z'],6)))
    digest=hashlib.sha256(json.dumps(anchors,sort_keys=True).encode()).hexdigest()
    return {'gate':'A83_B0_SOURCE_ONLY_G0',
            'source_geometry_consistent':not problems,
            'rejected_reasons':problems,
            'occupied_boundary_digest':digest,
            'true_3d_rooms':'NOT_TESTED',
            'true_openings':'NOT_TESTED',
            'actual_supported_loads':'NOT_TESTED',
            'continuous_human_walk':'NOT_TESTED',
            'interdistrict_connections':'NOT_TESTED',
            'true_3d_art_images':'NOT_RUN',
            'art_approval':'HOLD_NOT_AUTOMATED',
            'formal_s1_g1_g2_g3':'NOT_RUN',
            'minecraft_construction':'FORBIDDEN'}

def _hexagon(x,y,r,angle):
    return [[round(x+r*cos(angle+2*pi*i/6),6),
             round(y+r*sin(angle+2*pi*i/6),6)] for i in range(6)]

def sample_model():
    """Six potential activity volumes across three districts; strictly not adopted art."""
    model={'districts':[{'id':'W'},{'id':'C'},{'id':'E'}],
           'zones':[],'supports':[],'routes':[]}
    for d,x,y,angle in [('W',-620,-70,.2),('C',30,100,.55),('E',690,-100,.1)]:
        centers=[(x-55,y-65,36,'MARKET' if d=='W' else 'CIVIC'),
                 (x+95,y+95,50,'RESIDENCE' if d!='C' else 'WORKSHOP')]
        for i,(cx,cy,z,program) in enumerate(centers):
            zid=d+str(i)
            model['zones'].append({'id':zid,'district':d,'program':program,
                'footprint':_hexagon(cx,cy,58+9*i,angle+i*.21),
                'floor_z':z,'ceiling_z':z+12+3*i})
            for j in (-1,1):
                model['supports'].append({'zone':zid,'path':[[cx+16*j,cy-3*j,0],
                                                          [cx+12*j,cy+8*j,z]]})
        a,b=centers
        model['routes'].append({'district':d,'from':d+'0','to':d+'1',
            'path':[[a[0],a[1],a[2]],[(a[0]+b[0])/2,(a[1]+b[1])/2,(a[2]+b[2])/2],
                    [b[0],b[1],b[2]]]})
    return model

if __name__=='__main__':
    print(json.dumps(evaluate(sample_model()),indent=2,ensure_ascii=False))
