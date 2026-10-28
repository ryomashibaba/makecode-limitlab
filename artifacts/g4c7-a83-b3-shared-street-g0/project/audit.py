"""Independent OBJ triangle witness of B3; never art/safety certification."""
from pathlib import Path
import json, hashlib, math, copy
import numpy as np
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'output'

def read_obj(filename):
    vs=[];groups={};name=None
    for s in Path(filename).read_text().splitlines():
        a=s.split()
        if not a:continue
        if a[0]=='o':name=a[1];groups.setdefault(name,[])
        elif a[0]=='v':vs.append(tuple(map(float,a[1:4])))
        elif a[0]=='f':
            assert name is not None
            face=[int(x.split('/')[0])-1 for x in a[1:]]
            assert len(face)==3
            groups[name].append(face)
    verts=np.array(vs,dtype=np.float64)
    return {name:verts[np.array(f,dtype=int)] for name,f in groups.items() if f}

def hit_count(tri, origin, direction, length=6.0):
    # Exact stored OBJ floats; Moller-Trumbore no culling.
    if len(tri)==0:return 0
    a=tri[:,0];e1=tri[:,1]-a;e2=tri[:,2]-a
    d=np.broadcast_to(np.asarray(direction,dtype=float),e1.shape)
    h=np.cross(d,e2);det=np.sum(e1*h,axis=1)
    with np.errstate(divide='ignore',invalid='ignore'):
        inv=np.where(abs(det)>1e-10,1.0/det,0.0)
        s=np.asarray(origin,dtype=float)-a
        u=np.sum(s*h,axis=1)*inv
        q=np.cross(s,e1)
        v=np.sum(d*q,axis=1)*inv
        t=np.sum(e2*q,axis=1)*inv
    good=(abs(det)>1e-10)&(u>=1e-6)&(v>=1e-6)&(u+v<1-1e-6)&(t>1e-5)&(t<length)
    return int(np.sum(good))

def audit(mesh,meta):
    bad=[];door_results=[]
    for d in [{'id':'W','cx':-210,'cy':0,'sx':1,'sy':.86},
              {'id':'C','cx':0,'cy':26,'sx':1.2,'sy':1.10},
              {'id':'E','cx':225,'cy':-12,'sx':.91,'sy':1.0}]:
        id=d['id'];cx=d['cx'];cy=d['cy'];sx=d['sx'];sy=d['sy']
        zmid=next(z['shared_mid_floor_z'] for z in meta['regions'] if z['id']==id)
        for label,edge_y,dx,level,side in [
          ('lower',cy+8*sy,sx,.05,1),('upper',cy+91*sy,-1.5*sx,zmid,-1)]:
            name=f'{id}_{label}_facade_true_open'
            if name not in mesh:
                bad.append('MISSING_WALL:'+name);continue
            tris=mesh[name]
            x=cx+dx;y=edge_y-side*2
            center=hit_count(tris,(x,y,level+3),(0,side,0))
            sid=hit_count(tris,(x+20*sx,y,level+3),(0,side,0))
            above=hit_count(tris,(x,y,level+9),(0,side,0))
            door_results.append({'name':name,'center_clear':center==0,'side_solid':sid>0,'lintel_solid':above>0})
            if center!=0 or sid==0 or above==0:bad.append('MESH_DOOR_RAY_FAIL:'+name)
        group=id+'_true_shared_mid_floor'
        if group not in mesh:
            bad.append('MISSING_SHARED_SLAB:'+id)
        elif not np.allclose(mesh[group][:,:,2],zmid,atol=1e-5):
            bad.append('WRONG_SHARED_SLAB_HEIGHT:'+id)
        stairs=[]
        for i in range(80):
            st=id+'_actual_stair_tread_'+str(i)
            if st not in mesh:bad.append('MISSING_TREAD:'+st);break
            stairs.append((mesh[st][:,:,2].min(),mesh[st][:,:,2].max()))
        if len(stairs)==80:
            expected=[(i+1)*zmid/80 for i in range(80)]
            if not np.allclose([x[1] for x in stairs],expected,atol=1e-5):bad.append('TREAD_TOP_PROGRESS_FAIL:'+id)
            if id+'_upper_gallery' not in mesh:bad.append('MISSING_GALLERY:'+id)
            else:
                g=mesh[id+'_upper_gallery']
                if not np.isclose(g[:,:,2].max(),zmid,atol=1e-5):bad.append('GALLERY_NOT_AT_UPPER_FLOOR:'+id)
                # Actual last-tread footprint must overlap the landing footprint in XY.
                last=mesh[id+'_actual_stair_tread_79'];lmin=last[:,:,:2].min(axis=(0,1));lmax=last[:,:,:2].max(axis=(0,1))
                gmin=g[:,:,:2].min(axis=(0,1));gmax=g[:,:,:2].max(axis=(0,1))
                if any(lmax[k]<=gmin[k] or gmax[k]<=lmin[k] for k in range(2)):
                    bad.append('UPPER_STAIR_TO_GALLERY_DISCONNECTED:'+id)
                # Portal boundary touches the shared upper gallery footprint, not 9m away.
                rear=cy+91*sy
                if not (gmin[1]-1e-5<=rear<=gmax[1]+1e-5):bad.append('GALLERY_MISSES_REAR_PORTAL:'+id)
    if 'continuous_civic_ground' not in mesh:bad.append('DISCONNECTED_REGION_GROUND')
    return {'stage':'A83_B3_G0_INDEPENDENT_RELOADED_TRIANGLE_ONLY',
      'n_triangle_groups':len(mesh), 'observed_doors':door_results,
      'observed_shared_slabs':sum((q+'_true_shared_mid_floor') in mesh for q in ('W','C','E')),
      'observed_full_stairs':sum(all((q+'_actual_stair_tread_'+str(i)) in mesh for i in range(80)) for q in ('W','C','E')),
      'failures':bad,'narrow_g0_triangle_gate':not bad,
      'full_human_sweep':'NOT_TESTED','true_supported_load':'NOT_TESTED',
      'formal_s1_g1_g2_g3':'NOT_RUN','art':'NEVER_AUTOMATED','minecraft':'FORBIDDEN'}

if __name__=='__main__':
    meta=json.loads((OUT/'manifest.json').read_text());path=OUT/'a83_b3_integrated_civic_study.obj'
    assert hashlib.sha256(path.read_bytes()).hexdigest()==meta['mesh']['obj_sha256']
    result=audit(read_obj(path),meta)
    (OUT/'independent_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    assert result['narrow_g0_triangle_gate'],result['failures']
