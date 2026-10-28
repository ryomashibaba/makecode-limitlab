"""A83-2 conservative certificate of a continuous section's required depth.

Only certifies a 1D trace between two station rows of A83-1, with stored
floating-point coordinates interpreted as exact rational input values.
It does NOT certify rooms, routing, support, collision, or ART approval.
"""
from fractions import Fraction as F
from math import comb


def fraction(x):
    return F.from_float(float(x))


def p_add(a,b):
    return tuple((a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0)
                 for i in range(max(len(a),len(b))))


def p_neg(a):return tuple(-x for x in a)


def p_mul(a,b):
    c=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return tuple(c)


def p_linear(a,b):return (fraction(a),fraction(b)-fraction(a))


def p_dot(aa,bb):
    out=(F(0),)
    for a,b in zip(aa,bb):out=p_add(out,p_mul(a,b))
    return out


def bernstein(coeffs):
    n=len(coeffs)-1
    return tuple(sum((coeffs[j]*F(comb(k,j),comb(n,j)) for j in range(k+1)),F(0))
                 for k in range(n+1))


def split(controls):
    """De Casteljau at exactly t=1/2, exact rational."""
    levels=[tuple(controls)]
    while len(levels[-1])>1:
        prev=levels[-1]
        levels.append(tuple((prev[i]+prev[i+1])/2 for i in range(len(prev)-1)))
    return (tuple(row[0] for row in levels),
            tuple(row[-1] for row in reversed(levels)))


def certify_nonnegative(coeffs,max_depth=28,strict=False):
    """Conservative: even a tiny uncertified interval is a FAIL, never a PASS."""
    queue=[(bernstein(coeffs),0)]
    subdivisions=0
    while queue:
        b,depth=queue.pop()
        if (all(x>0 for x in b) if strict else all(x>=0 for x in b)):
            continue
        if any(x<0 for x in (b[0],b[-1])) or (strict and (b[0]<=0 or b[-1]<=0)):
            return False,subdivisions,'NONPOSITIVE_ENDPOINT'
        if depth>=max_depth:
            return False,subdivisions,'UNRESOLVED_FAIL_CLOSED'
        left,right=split(b)
        subdivisions+=1
        queue.extend([(right,depth+1),(left,depth+1)])
    return True,subdivisions,'CERTIFIED_FOR_STORED_COORDINATES'


def segment_polynomials(a,b):
    """n(t) interpolates A83-1 stored normals and delta(t) joins civic to inner."""
    v0=tuple(a['inner'][i]-a['civic'][i] for i in (0,1))
    v1=tuple(b['inner'][i]-b['civic'][i] for i in (0,1))
    n0,n1=a['normal'],b['normal']
    delta=[p_linear(v0[i],v1[i]) for i in (0,1)]
    normal=[p_linear(n0[i],n1[i]) for i in (0,1)]
    demand=p_linear(a['required_m'],b['required_m'])
    p=p_dot(delta,normal)
    q=p_dot(normal,normal)
    discriminant=p_add(p_mul(p,p),p_neg(p_mul(p_mul(demand,demand),q)))
    return p,q,discriminant


def certify_segment(a,b):
    p,q,f=segment_polynomials(a,b)
    evidence={}
    for name,poly,strict in [('positive_interpolated_normal',q,True),
                             ('forward_depth',p,False),
                             ('unbroken_required_depth',f,False)]:
        passed,subdivisions,reason=certify_nonnegative(poly,strict=strict)
        evidence[name]={'certified':passed,'subdivisions':subdivisions,'reason':reason}
        if not passed:
            raise ValueError('A83_2_CONTINUOUS_DEPTH_UNCERTIFIED_'+name+'_'+reason)
    return evidence


def certify_witness(witness):
    if witness.get('scope')!='A83_1_SAMPLED_FLOOR_BOUNDARY_NOT_OCCUPIED_CITY':
        raise ValueError('INCORRECT_G0_SCOPE')
    rows=witness['rows']
    if len(rows)!=12 or len(witness['triangles'])!=18:
        raise ValueError('INCOMPLETE_SOURCE_GEOMETRY')
    regions=['west','center','east']
    out=[]
    for district in regions:
        group=[x for x in rows if x['district']==district]
        if len(group)!=4:raise ValueError('DISTRICT_MEMBERSHIP_CHANGED')
        for a,b in zip(group,group[1:]):
            out.append({'edge':a['id']+'-'+b['id'],'proof':certify_segment(a,b)})
    return {'sections_certified':len(out),'proofs':out,
            'scope':'G0_CONTINUOUS_SECTION_ONLY_NOT_WALKING_OR_ROOM',
            'actual_rooms':0,'art':'NOT_APPROVED','formal':'NOT_RUN',
            'construction':'FORBIDDEN'}


def main():
    import sys,json
    from pathlib import Path
    sys.path.insert(0,str(Path(__file__).resolve().parent))
    from g4c7_a83_1_feasible_boundary import witness
    result=certify_witness(witness())
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
