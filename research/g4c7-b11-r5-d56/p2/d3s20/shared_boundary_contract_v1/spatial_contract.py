"""D3S20 -- shared-boundary author-data contract, NON-CONSTRUCTION.

The purpose is to reject independent rooms + detached road/portal modeling.
This is an executable, deliberately ugly architectural *test fixture*, not a city
art hypothesis or a Minecraft MakeCode instruction generator.
Axes: X East, Y North, Z up. All units are abstract design units.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from collections import deque
from typing import Dict, Tuple, FrozenSet
import copy, json, hashlib
from pathlib import Path

CELL=4.0
WALL_THICKNESS=.20
FLOOR_THICKNESS=.24
PORTAL_WIDTH=2.4
PORTAL_HEIGHT=3.6
Cell=tuple[int,int,int]
FaceKey=tuple[Cell,Cell]

class ContractError(ValueError):
    pass

def norm_edge(a:Cell,b:Cell)->FaceKey:
    return (a,b) if a < b else (b,a)

def adjacent(a:Cell,b:Cell)->bool:
    return sum(abs(x-y) for x,y in zip(a,b))==1

@dataclass
class SpatialLedger:
    # A single source of truth: air cell ownership. Empty cells are solid/unmodeled
    # and may NOT be presented as fully engineered structural support.
    spaces: Dict[Cell,str]
    portals: dict[FaceKey,str]
    entrance: tuple[Cell,Cell]
    required: tuple[str,...]
    vertical_access: str="NOT_BUILT"
    scale: float=CELL
    envelope_span: tuple[int,int,int]=(12,9,2)
    no_city_art_claim: bool=True

    def face_inventory(self):
        faces={}
        for a,owner in self.spaces.items():
            for axis in range(3):
                for sign in (-1,1):
                    b=list(a);b[axis]+=sign;b=tuple(b)
                    key=norm_edge(a,b)
                    if key in faces:continue
                    other=self.spaces.get(b)
                    if other==owner:continue
                    kind=('floor' if axis==2 and sign==-1 else 'roof' if axis==2 and sign==1 else 'wall')
                    if other is not None and axis==2:
                        kind='interlevel_slab'
                    elif other is not None and axis!=2:
                        kind='partition'
                    elif axis!=2:
                        kind='envelope_wall'
                    faces[key]={'a':a,'b':b,'owner':owner,'other':other,'axis':axis,'sign':sign,'kind':kind,'door':key in self.portals}
        return faces

    def validate(self, demand_upper_route=False):
        errs=[]
        if not self.no_city_art_claim:errs.append('ART_CLAIM_FORBIDDEN')
        if not self.spaces:errs.append('EMPTY_AUTHOR_FIELD')
        for a,s in self.spaces.items():
            if len(a)!=3 or any(not isinstance(q,int) for q in a):errs.append('NON_GRID_SPACE_CELL');break
            if any(q<0 or q>=lim for q,lim in zip(a,self.envelope_span)):errs.append('OUT_OF_DOMAIN');break
        actual_types=set(self.spaces.values())
        for r in self.required:
            if r not in actual_types:errs.append('MISSING_PROGRAM_'+r)
        faces=self.face_inventory()
        for key,purpose in self.portals.items():
            a,b=key
            if not adjacent(a,b):errs.append('PORTAL_NOT_ADJACENT')
            if key not in faces:errs.append('PORTAL_NOT_SHARED_FACE')
            elif faces[key]['axis']==2:errs.append('HORIZONTAL_DOOR_IN_VERTICAL_FACE')
            elif self.spaces.get(a)==self.spaces.get(b):errs.append('PORTAL_WITHIN_ONE_SPACE')
            elif self.spaces.get(a) is None and self.spaces.get(b) is None:errs.append('PORTAL_BETWEEN_SOLIDS')
            elif key == norm_edge(*self.entrance) and purpose != 'external':errs.append('WRONG_ENTRANCE_USE')
            elif key != norm_edge(*self.entrance) and purpose != 'interface':errs.append('WRONG_INTERNAL_PORTAL_USE')
        if norm_edge(*self.entrance) not in self.portals:errs.append('NO_PUBLIC_ENTRANCE')
        else:
            ca,cb=self.entrance
            if (ca not in self.spaces or cb in self.spaces or self.spaces.get(ca)!='PUBLIC'):
                errs.append('ENTRANCE_NOT_PUBLIC_EXTERIOR')
        # Deliberate strictness: no conceptual road/door distance tolerance at all.
        # Each door must be on an existing air/air shared face, no portal on gap.
        g={c:set() for c in self.spaces}
        for c,owner in self.spaces.items():
            for axis in (0,1):
                for sign in (-1,1):
                    q=list(c);q[axis]+=sign;q=tuple(q)
                    if q not in self.spaces:continue
                    if self.spaces[q]==owner or norm_edge(c,q) in self.portals:
                        g[c].add(q)
        # grounded conceptual routing, no claim about body's swept volume
        root=self.entrance[0]
        seen={root} if root in self.spaces else set();qq=deque(seen)
        while qq:
            p=qq.popleft()
            for nxt in g[p]-seen:seen.add(nxt);qq.append(nxt)
        destinations={self.spaces[c] for c in seen}
        for r in self.required:
            if r!='UPPER' and r not in destinations:errs.append('UNREACHABLE_'+r)
        if demand_upper_route:errs.append('UPPER_ACCESS_NOT_BUILT')
        if self.vertical_access!='NOT_BUILT':errs.append('UNVERIFIED_VERTICAL_ACCESS_CLAIM')
        # Independent islands within a program must never be silently counted
        # as usable just because one destination of the same name is reached.
        orphan_ground=[c for c,s in self.spaces.items() if c[2]==0 and c not in seen]
        if orphan_ground:errs.append('UNREACHABLE_GROUND_CELLS')
        # There is no physical stress/load path test at this stage.
        return {'ok':not errs,'errors':sorted(set(errs)),'reached_programs':sorted(destinations),
                'active_air_cells':len(self.spaces),'shared_faces':len(faces),
                'internal_portals':sum(v=='interface' for v in self.portals.values()),
                'external_entries':sum(v=='external' for v in self.portals.values()),
                'roof_faces':sum(v['kind']=='roof' for v in faces.values()),
                'envelope_wall_faces':sum(v['kind']=='envelope_wall' for v in faces.values()),
                'vertical_access':self.vertical_access,
                'claims':['cell-level horizontal topology ONLY','no embodied passage','no structural support QA',
                          'no full-scale city 3D','no MakeCode conversion','no artistic adoption']}

    def fingerprint(self):
        faces=self.face_inventory()
        return {
            'rooms':{k:sorted([list(c) for c,s in self.spaces.items() if s==k]) for k in sorted(set(self.spaces.values()))},
            'shared_boundaries':sorted([str(k)+str(v['kind']) for k,v in faces.items()]),
            'portals':sorted([str(k)+v for k,v in self.portals.items()]),
            'outer_faces':sorted([str(k) for k,v in faces.items() if v['kind'] in ('envelope_wall','roof')]),
        }

def make_fixture():
    c={}
    def assign(name, xs, ys, z=0):
        for x in xs:
            for y in ys:
                p=(x,y,z)
                if p in c and c[p]!=name:raise ContractError(f'fixture collision {p}: {c[p]} vs {name}')
                c[p]=name
    # No detached 'road mesh': PUBLIC is an actual shared air domain.
    assign('PUBLIC',range(1,11),range(4,6))
    assign('PUBLIC',range(5,7),range(0,4))
    assign('PUBLIC',range(5,7),range(6,9))
    assign('FORGE',range(1,5),range(0,4))
    assign('RESEARCH',range(7,11),range(1,4))
    assign('MARKET',range(2,5),range(6,9))
    assign('CULTURE',range(0,2),range(6,9))
    assign('HABITAT',range(7,10),range(6,9))
    assign('UPPER',range(5,7),range(3,6),z=1)
    doors={}
    def door(a,b,tag='interface'):doors[norm_edge(a,b)]=tag
    door((1,4,0),(0,4,0),'external')
    door((3,4,0),(3,3,0))
    door((9,4,0),(9,3,0))
    door((3,5,0),(3,6,0))
    door((1,5,0),(1,6,0))
    door((8,5,0),(8,6,0))
    return SpatialLedger(c,doors,((1,4,0),(0,4,0)),('PUBLIC','FORGE','RESEARCH','MARKET','CULTURE','HABITAT'))

# Useful, non-artist-controlled mutations. They can change multiple kinds of
# surfaces, but if they break explicit portal contracts they must NOT auto-heal.
def extend_market(ledger:SpatialLedger):
    d=copy.deepcopy(ledger)
    # Extend the existing market at ground level, sharing the wall of (3,8,0).
    # The outside urban envelope is *derived*, never separately authored.
    d.envelope_span=(12,10,2)
    d.spaces[(3,9,0)]='MARKET'
    return d

def shift_market_frontage(ledger:SpatialLedger):
    d=extend_market(ledger)
    # This is a genuinely coupled frontage change. The market takes one
    # previously public walk-cell; the same shared face creates the door and
    # the traversable public field shrinks. No hand-placed portal geometry.
    d.spaces[(3,5,0)]='MARKET'
    d.portals.pop(norm_edge((3,5,0),(3,6,0)))
    d.portals[norm_edge((3,4,0),(3,5,0))]='interface'
    return d

def break_entrance(ledger:SpatialLedger):
    d=copy.deepcopy(ledger)
    d.portals.pop(norm_edge(*d.entrance))
    return d

def bridge_gap_fake(ledger:SpatialLedger):
    d=copy.deepcopy(ledger)
    # Former 'detached room + nearby road' mistake: door crosses one intervening solid cell.
    d.portals[norm_edge((3,5,0),(3,7,0))]='interface'
    return d

def orphan_research(ledger:SpatialLedger):
    d=copy.deepcopy(ledger)
    for c in list(d.spaces):
        if d.spaces[c]=='RESEARCH':d.spaces[(c[0],c[1],c[2])]='SOLID_NEIGHBOR'
    # no research-owned cell remains; catches missing real space (not a mere label)
    return d

def unsupported_upper_claim(ledger:SpatialLedger):
    d=copy.deepcopy(ledger)
    d.vertical_access='NOT_BUILT'
    return d

if __name__=='__main__':
    base=make_fixture()
    print(json.dumps({'base':base.validate(),
                      'broken':{name:fn(base).validate() for name,fn in
                      [('missing_entrance',break_entrance),('floating_portal',bridge_gap_fake),
                       ('missing_program',orphan_research)]},
                      'upper_required':base.validate(demand_upper_route=True)},indent=2))