"""A83-1: fail-closed occupied-depth and exterior-envelope coupling.

This creates only sparse G0 analytical boundary/floor triangles, not usable
rooms, a connected city, or an ART candidate. Earlier A83-0 is immutable.
"""
from dataclasses import replace
from hashlib import sha256
from math import hypot, isfinite, sqrt
import json

from g4c7_a83_reciprocal_grammar_g0 import STATIONS, PROTECTED, MIN_DEPTH, WALL

# Independently authored HARD limits. Never derive these from edited requests.
MAX_EXTERIOR_M = dict(zip(
    ('W0','W1','W2','W3','C0','C1','C2','C3','E0','E1','E2','E3'),
    (60.,70.,70.,61.,63.,78.,76.,69.,67.,76.,61.,66.)))
DISTRICTS=('west','center','east')
SUBDIVISIONS=16
EPS=1e-7


def between(a,b,t):
    return tuple((1-t)*x+t*y for x,y in zip(a,b))


def add(a,b):
    return tuple(x+y for x,y in zip(a,b))


def sub(a,b):
    return tuple(x-y for x,y in zip(a,b))


def scaled(v,k):
    return tuple(x*k for x in v)


def length(v):
    return sqrt(sum(x*x for x in v))


def normalized(v):
    n=length(v)
    if n<0.99 or n>1.01:
        raise ValueError('BAD_AUTHOR_NORMAL')
    return scaled(v,1/n)


def unit_interpolated(v):
    n=length(v)
    if n<1e-9:
        raise ValueError('OPPOSING_INTERPOLATED_NORMALS')
    return scaled(v,1/n)


def cross(a,b):
    return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])


def solve_station(s,hard_cap_m):
    if s.use not in MIN_DEPTH or s.requested_depth_m<MIN_DEPTH.get(s.use,float('inf')):
        raise ValueError('PROGRAM_DEPTH_BELOW_MINIMUM')
    values=(*s.point,*s.outward,s.requested_depth_m,s.authored_exterior_m,hard_cap_m)
    if not all(isfinite(x) for x in values):
        raise ValueError('NONFINITE_INPUT')
    n=normalized(s.outward)
    if s.authored_exterior_m<0 or s.authored_exterior_m>hard_cap_m:
        raise ValueError('AUTHOR_EXTERIOR_OUTSIDE_HARD_LIMIT')
    minimum=s.requested_depth_m+WALL
    if minimum>hard_cap_m+EPS:
        raise ValueError('HARD_ENVELOPE_CANNOT_FIT_REQUIRED_ROOM')
    # The old A83 interpolation could shrink a room below its requested depth.
    # The target is SOFT, but room demand and city-side limit are HARD.
    preference=.6*(minimum+8.)+.4*s.authored_exterior_m
    offset=max(minimum,min(hard_cap_m,preference))
    civic=s.point
    inner=add(civic,scaled((*n,0.),offset-WALL))
    outer=add(civic,scaled((*n,0.),offset))
    if length(sub(inner,civic))+EPS<s.requested_depth_m:
        raise AssertionError('ACTUAL_REQUIRED_ROOM_DEPTH_VIOLATED')
    return {'id':s.ident,'district':s.district,'use':s.use,
            'required_m':s.requested_depth_m,'usable_m':offset-WALL,
            'exterior_m':offset,'hard_cap_m':hard_cap_m,
            'civic':civic,'inner':inner,'outer':outer,'normal':n}


def witness(stations=STATIONS,caps=MAX_EXTERIOR_M,flags=PROTECTED):
    if flags!=PROTECTED:
        raise ValueError('PROTECTED_GATES_OR_SAFETY_CONTRACT_CHANGED')
    if len(stations)!=len(STATIONS) or tuple(s.ident for s in stations)!=tuple(s.ident for s in STATIONS):
        raise ValueError('STATION_TOPOLOGY_CHANGED')
    if set(caps)!=set(MAX_EXTERIOR_M):
        raise ValueError('MISSING_HARD_LIMIT')
    for original,s in zip(STATIONS,stations):
        if (original.district,original.use,original.point)!=(s.district,s.use,s.point):
            raise ValueError('UNREVIEWED_PROGRAM_OR_SITE_TOPOLOGY_CHANGE')
    rows=[solve_station(s,caps[s.ident]) for s in stations]
    vertices=[];triangles=[];samples=[]
    for district in DISTRICTS:
        group=[p for p in rows if p['district']==district]
        if len(group)!=4:
            raise ValueError('DISTRICT_SECTION_SIZE_CHANGED')
        for a,b in zip(group,group[1:]):
            # A sampled ruled floor surface: civic edge and occupied inner boundary.
            # Continuous walking, spatial enclosure and load transfer NOT established.
            k=len(vertices)
            vertices.extend((a['civic'],b['civic'],b['inner'],a['inner']))
            triangles.extend(((k,k+1,k+2),(k,k+2,k+3)))
            for tri in triangles[-2:]:
                v0,v1,v2=(vertices[i] for i in tri)
                if length(cross(sub(v1,v0),sub(v2,v0)))<EPS:
                    raise ValueError('DEGENERATE_TRUE_FLOOR_TRIANGLE')
            for i in range(SUBDIVISIONS+1):
                t=i/SUBDIVISIONS
                c=between(a['civic'],b['civic'],t)
                r=between(a['inner'],b['inner'],t)
                n=unit_interpolated(between(a['normal'],b['normal'],t))
                actual=sum(x*y for x,y in zip(sub(r,c)[:2],n))
                required=(1-t)*a['required_m']+t*b['required_m']
                if actual+EPS<required:
                    raise ValueError('INTERPOLATED_CLEAR_DEPTH_FAIL_'+a['id']+'_'+b['id'])
                samples.append({'from':a['id'],'to':b['id'],'t':t,
                                'depth_m':actual,'required_m':required})
    return {'rows':rows,'vertices':vertices,'triangles':triangles,'samples':samples,
            'scope':'A83_1_SAMPLED_FLOOR_BOUNDARY_NOT_OCCUPIED_CITY',
            'mesh_type':'TRUE_TRIANGLE_RIBBON_G0_ONLY',
            'actual_rooms':0,'interdistrict_crossings':0,
            'doorways':0,'upper_level_connections':0,'full_city':False,
            'rendered_art':'NOT_RUN','art':'NOT_APPROVED',
            'formal':{k:'NOT_RUN' for k in ('S1','G1','G2','G3')},
            'minecraft_construction':'FORBIDDEN','city_integration':'FORBIDDEN',
            'walking':'NOT_TESTED','support':'NOT_TESTED'}


def digest(rows):
    return sha256(json.dumps([(r['id'],r['civic'],r['inner'],r['outer']) for r in rows],
        separators=(',',':')).encode()).hexdigest()


def counterfactuals():
    base=witness(); s=list(STATIONS)
    s[5]=replace(s[5],requested_depth_m=s[5].requested_depth_m+5)
    by_program=witness(tuple(s))
    s=list(STATIONS)
    s[5]=replace(s[5],authored_exterior_m=s[5].authored_exterior_m+5)
    by_exterior=witness(tuple(s))
    for changed in (by_program,by_exterior):
        if digest(changed['rows'])==digest(base['rows']):
            raise AssertionError('FALSE_RECIPROCAL_COORDINATE_EFFECT')
        if any(p['depth_m']+EPS<p['required_m'] for p in changed['samples']):
            raise AssertionError('SILENT_INTERMEDIATE_ROOM_LOSS')
    return {'baseline_sha256':digest(base['rows']),
            'program_edit_sha256':digest(by_program['rows']),
            'exterior_edit_sha256':digest(by_exterior['rows']),
            'baseline_min_sample_margin_m':min(p['depth_m']-p['required_m'] for p in base['samples']),
            'program_edit_min_sample_margin_m':min(p['depth_m']-p['required_m'] for p in by_program['samples']),
            'exterior_edit_min_sample_margin_m':min(p['depth_m']-p['required_m'] for p in by_exterior['samples'])}


def negative_controls():
    attempts={}
    def must_reject(label,fn):
        try:fn()
        except (ValueError,AssertionError):attempts[label]='REJECTED'
        else:raise AssertionError('ESCAPED_INVALID_'+label)
    s=list(STATIONS);s[1]=replace(s[1],requested_depth_m=90.)
    must_reject('requested_room_over_hard_limit',lambda:witness(tuple(s)))
    s=list(STATIONS);s[5]=replace(s[5],authored_exterior_m=120.)
    must_reject('author_exterior_over_hard_limit',lambda:witness(tuple(s)))
    c=dict(MAX_EXTERIOR_M);c['C1']=50.
    must_reject('hard_cap_below_baseline_room',lambda:witness(caps=c))
    s=list(STATIONS);s[0]=replace(s[0],outward=(3.,3.))
    must_reject('invalid_normal',lambda:witness(tuple(s)))
    s=list(STATIONS);s[0]=replace(s[0],requested_depth_m=1.)
    must_reject('sub_minimum_room',lambda:witness(tuple(s)))
    must_reject('missing_district',lambda:witness(STATIONS[:-4]))
    must_reject('art_gate_forgery',lambda:witness(flags={**PROTECTED,'art':'APPROVED'}))
    must_reject('construction_gate_forgery',lambda:witness(flags={**PROTECTED,'minecraft_construction':'ALLOWED'}))
    must_reject('safety_samples_relaxed',lambda:witness(flags={**PROTECTED,'formal_foot_samples':992}))
    return attempts


def main():
    model=witness()
    print(json.dumps({'stage':'A83-1','station_count':len(model['rows']),
       'true_floor_triangles':len(model['triangles']),
       'local_depth_samples':len(model['samples']),
       'room_count':model['actual_rooms'],
       'interdistrict_crossings':model['interdistrict_crossings'],
       'rendered_art':model['rendered_art'],
       'formal':model['formal'],'art':model['art'],
       'construction':model['minecraft_construction'],
       'counterfactuals':counterfactuals(),
       'negative_controls':negative_controls()},indent=2,sort_keys=True))

if __name__=='__main__':main()
