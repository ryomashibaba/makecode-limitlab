"""G4-C7 B11-R5 D4: core pre-3D planar/vertical design checks.
Requires shapely>=2; schematic spatial hypothesis only, no actual OBJ/PLY or safe route.
The extended local image/contract generator is archived separately in conversation.
"""
from collections import defaultdict, deque
from shapely.geometry import Polygon, LineString, box
from shapely.affinity import translate

W=Polygon([(-155,-92),(85,-110),(155,-45),(140,62),(65,83),(-122,75),(-161,10)])
R=Polygon([(-115,135),(10,119),(76,136),(140,126),(265,168),(259,307),
           (163,331),(85,300),(-12,331),(-109,282)])
ROOF=W.buffer(6,join_style=2)
CORES={'E1':(-180,119),'E2':(184,119)}
PUBLIC_Y=119
SERVICE=LineString([(415,-159),(260,-161),(163,-123),(45,-49)])
PUBLIC=LineString([(-410,119),(-180,119),(-5,119),(184,119),(425,119)])

def public_reachable(enabled):
    layers=('ground','gallery','research','sky')
    adj=defaultdict(set)
    for lv in layers:
        for c in ('E1','E2'):
            adj[f'{lv}:E1'].add(f'{lv}:E2');adj[f'{lv}:E2'].add(f'{lv}:E1')
    for c in enabled:
        for a,b in zip(layers,layers[1:]):
            x=f'{a}:{c}';y=f'{b}:{c}';adj[x].add(y);adj[y].add(x)
    seen={'ground:E1'};queue=deque(seen)
    while queue:
        for v in adj[queue.popleft()]:
            if v not in seen:seen.add(v);queue.append(v)
    return 'sky:E1' in seen and 'research:E2' in seen

def run():
    assert not ROOF.intersects(R) and W.distance(R)>15
    assert all(box(x-8,y-8,x+8,y+8).intersection(ROOF).area==0
               for x,y in CORES.values())
    assert PUBLIC.distance(SERVICE)>20
    assert public_reachable({'E1'}) and public_reachable({'E2'})
    assert not public_reachable(set())
    relocated=translate(R,xoff=-180,yoff=-205)
    assert ROOF.intersection(relocated).area>0
    for h in (70,90):
        roof_top=18+h+16
        conflict=(ROOF.intersection(R).area>0 and 132-roof_top<12)
        injected=(ROOF.intersection(relocated).area>0 and 132-roof_top<12)
        assert not conflict and injected==(h==90)
        print(f'D4 {h}m: XY roof/research overlap 0; research setback {W.distance(R):.3f}m; '
              f'floor/roof top z gap {132-roof_top}m; injection detected={injected}')
    print('PRE-3D SPATIAL CONTRACT ONLY: G0 NOT RUN, ART HOLD, S1-G1-G2-G3 NOT RUN, Minecraft FORBIDDEN')
if __name__=='__main__': run()
