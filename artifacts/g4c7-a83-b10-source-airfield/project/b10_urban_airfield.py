"""A83-B10: 2D negative-space-first source model, never a true 3D/city safety gate.

The occupancy slice represents candidate AIR at one common datum only.
It is not floors, accessible routes, building structure, a real room, or fine art.
"""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import numpy as np
from scipy.ndimage import binary_dilation, distance_transform_edt, label

ROOT = Path(__file__).resolve().parent
STEP = 3.0  # source sampling metres, NOT an accessibility clearance certificate
X = np.arange(-900., 901., STEP)
Y = np.arange(-450., 451., STEP)
XX, YY = np.meshgrid(X, Y)
BASE = {
    'stage': 'A83-B10', 'model': 'NEGATIVE_SPACE_FIRST_2D_SOURCE',
    'centres': [
      {'id': 'W', 'x': -700., 'y': -15., 'rx': 114., 'ry': 100., 'programs': ['market','making','homes']},
      {'id': 'C', 'x': 5., 'y': 30., 'rx': 136., 'ry': 116., 'programs': ['civic','reading','research','homes']},
      {'id': 'E', 'x': 700., 'y': 0., 'rx': 121., 'ry': 104., 'programs': ['living','education','recreation']},
    ],
    'public_spine': {'base_halfwidth_m': 34., 'lateral_sway_m': 70.},
    'dwelling_margin_m': 93.,
    # Three multidirectional civic spurs, not a single long B6 ribbon.
    'branches': [
      {'id':'CULTURE_N','sx':-470., 'ex':-490., 'ey':285., 'width':34.},
      {'id':'SCIENCE_S','sx':-75., 'ex':-115., 'ey':-310., 'width':37.},
      {'id':'NEIGHBORHOOD_N','sx':385., 'ex':455., 'ey':300., 'width':34.},
      {'id':'WORKSHOP_S','sx':585., 'ex':585., 'ey':-280., 'width':34.}
    ],
    'status': {'real_3d':'NOT_RUN','room_enclosure':'NOT_TESTED','continuous_human_sweep':'NOT_RUN',
               'load_support':'NOT_TESTED','formal_s1_g1_g2_g3':'NOT_RUN',
               'art':'HOLD','formal_art_adoptions':0,'minecraft_construction':'FORBIDDEN'}
}

def centreline(x, sway):
    # The path is a source airfield, not a hand-drawn transit line or real path.
    return sway*np.sin((x + 120.)/265.) + 22.*np.sin((x-70.)/106.)

def fields(data=None, break_at=None, narrow_at=None, drop_branch=None):
    d=copy.deepcopy(data or BASE)
    spine=d['public_spine']
    y=centreline(XX, spine['lateral_sway_m'])
    # Source air is one continuous branching free-space volume in THIS 2D slice.
    half=spine['base_halfwidth_m']*(1.+.11*np.sin(XX/112.))
    if narrow_at is not None:
        half=np.where(abs(XX-narrow_at)<=12., .8, half)
    air=(np.abs(YY-y)<=half)
    for c in d['centres']:
        air|=(((XX-c['x'])/c['rx'])**2+((YY-c['y'])/c['ry'])**2<=1.)
    for b in d['branches']:
        if b['id']==drop_branch:continue
        x0,y0=b['sx'],float(centreline(b['sx'],spine['lateral_sway_m']))
        x1,y1=b['ex'],b['ey']
        dx,dy=x1-x0,y1-y0
        t=np.clip(((XX-x0)*dx+(YY-y0)*dy)/(dx*dx+dy*dy),0.,1.)
        dist2=(XX-x0-t*dx)**2+(YY-y0-t*dy)**2
        air|=(dist2<=b['width']**2)
        air|=(((XX-x1)/55.)**2+((YY-y1)/62.)**2<=1.)
    if break_at is not None:
        air[:, np.abs(X-break_at)<=7.5] = False
    cells=int(round(d['dwelling_margin_m']/STEP))
    envelope=binary_dilation(air,iterations=cells)
    inhabited=envelope & ~air
    # The envelope is derived FROM public space; it isn't authored independently.
    return {'air':air,'urban_envelope':envelope,'inhabited_candidate':inhabited}

def _find_cell(c):
    return int(np.argmin(abs(Y-c['y']))),int(np.argmin(abs(X-c['x'])))

def _connected_clearance(mask, nodes, clearance_m=5.):
    edt=distance_transform_edt(mask)*STEP
    valid=mask & (edt>=clearance_m)
    components,count=label(valid, structure=np.ones((3,3),dtype=np.int8))
    at=[]
    for n in nodes:
        iy,ix=_find_cell(n)
        at.append(int(components[iy,ix]))
    connected=all(c>0 for c in at) and len(set(at))==1
    return connected,count,at,valid,edt

def audit(data=None, break_at=None, narrow_at=None, drop_branch=None):
    d=copy.deepcopy(data or BASE)
    f=fields(d,break_at,narrow_at,drop_branch)
    err=[]
    nodes=d['centres']
    if len(nodes)!=3 or [n['id'] for n in nodes]!=['W','C','E']:err.append('DISTRICT_SET')
    if any(len(set(n['programs']))<3 for n in nodes):err.append('PROGRAMMATIC_COLLAPSE')
    if d['status']!=BASE['status']:err.append('FALSE_ART_SAFETY_OR_CONSTRUCTION')
    endpoint_nodes=[{'id':b['id'],'x':b['ex'],'y':b['ey']} for b in d['branches']]
    connected,count,at,valid,edt=_connected_clearance(f['air'],nodes+endpoint_nodes)

    if not connected:err.append('PUBLIC_AIR_SOURCE_DISCONNECTED_AT_5M_CENTRE_CLEARANCE')
    base=f['urban_envelope']
    # An actual (sampled) reciprocal dependency: edit civic space changes urban silhouette.
    altered=copy.deepcopy(d)
    altered['centres'][1]['rx']+=42.
    altered['centres'][1]['ry']+=25.
    changed=fields(altered)['urban_envelope']
    boundary_difference=int(np.count_nonzero(base^changed))
    if boundary_difference<30:err.append('EXTERIOR_DOES_NOT_RESPOND_TO_PUBLIC_SPACE')
    margin=f['inhabited_candidate']
    if not (np.any(margin) and np.any(f['air'])):err.append('NO_TWO_SIDED_OCCUPANCY')
    return {
      'stage': d['stage'],'source_scale':{'metres_per_grid_cell':STEP, 'width_m':1800,'depth_m':900},
      'source_2d_air_connected_at_5m_centre_clearance':connected,
      'labelled_clearance_components':count,'public_node_labels':at,
      'public_branch_count':len(d['branches']),
      'public_air_source_area_m2':int(f['air'].sum()*STEP*STEP),
      'inhabited_envelope_source_area_m2':int(margin.sum()*STEP*STEP),
      'altered_civic_void_causes_envelope_change_cells':boundary_difference,
      'failures':err,'source_preflight_pass':not err,
      'actual_floor':'NOT_TESTED','actual_room_enclosure':'NOT_TESTED',
      'real_3d':'NOT_RUN','full_human_sweep_331_foot_993':'NOT_RUN',
      'structural_load_and_vertical_routes':'NOT_TESTED','formal_s1_g1_g2_g3':'NOT_RUN',
      'art_status':'HOLD_NO_VISUAL_ADOPTION','formal_art_adoptions':0,
      'minecraft_construction':'FORBIDDEN',
      'caveat':'2D sample negative-space topology; a connected slice is not a traversable building or compelling macro silhouette'
    }

def export(data=None):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap
    d=data or BASE
    model=fields(d)
    audit_result=audit(d)
    image=np.zeros_like(model['air'],dtype=np.uint8)
    image[model['inhabited_candidate']]=1
    image[model['air']]=2
    fig,ax=plt.subplots(figsize=(15,8),dpi=160)
    fig.patch.set_facecolor('#091b26');ax.set_facecolor('#091b26')
    ax.imshow(image,extent=(X.min(),X.max(),Y.min(),Y.max()),origin='lower',
              cmap=ListedColormap(['#091b26','#477683','#d6bb82']),interpolation='nearest',vmin=0,vmax=2)
    for n in d['centres']:
        ax.plot(n['x'],n['y'],'o',mec='#eaf4f7',mfc='#123342',markersize=10,markeredgewidth=2)
        ax.text(n['x'],n['y']-48,n['id'],color='#f6f3e8',fontsize=16,ha='center',weight='bold')
    for b in d['branches']:
        ax.plot(b['ex'],b['ey'],'o',mec='#eaf4f7',mfc='#143543',markersize=7,markeredgewidth=1.5)
        off=-35 if b['ey']>0 else 40
        ax.text(b['ex'],b['ey']+off,b['id'].replace('_',' '),color='#ebeff1',fontsize=10,ha='center')
    ax.set_xlim(-900,900);ax.set_ylim(-450,450);ax.set_aspect('equal')
    ax.set_xticks([-800,-400,0,400,800]);ax.tick_params(colors='#aabec6',labelsize=11)
    ax.set_title('G4-C7 / A83-B10  —  CANDIDATE SHARED AIRFIELD (2D SOURCE)',
                 color='#f1eee7',fontsize=19,pad=22)
    fig.text(.13,.13,'Gold = candidate PUBLIC AIR (2D only)    Blue = derived occupied margin    Charcoal = outside',
             color='#c9d6d9',fontsize=13)
    fig.text(.13,.095,'No actual rooms, vertical routes, support, human sweep, or true 3D. ART HOLD / NO CONSTRUCTION.',
             color='#edc786',fontsize=12)
    ax.set_xlabel('metres · conceptual source coordinates',color='#aec0c5',fontsize=11)
    fig.subplots_adjust(bottom=.2)
    p=ROOT/'B10_SOURCE_PLAN.png';fig.savefig(p,facecolor=fig.get_facecolor(),bbox_inches='tight');plt.close(fig)
    # Zoom into the central public region at consistent real dimensions.
    fig,ax=plt.subplots(figsize=(12,8),dpi=160)
    fig.patch.set_facecolor('#091b26');ax.set_facecolor('#091b26')
    ax.imshow(image,extent=(X.min(),X.max(),Y.min(),Y.max()),origin='lower',
              cmap=ListedColormap(['#091b26','#477683','#d6bb82']),interpolation='nearest',vmin=0,vmax=2)
    ax.set_xlim(-260,285);ax.set_ylim(-270,250);ax.set_aspect('equal')
    ax.plot(5,30,'o',mec='white',mfc='#143543',markersize=11,markeredgewidth=2)
    ax.set_title('CENTRAL CITY / zoom of EXACT SAME SOURCE MASK',color='#f1eee7',fontsize=18,pad=20)
    ax.tick_params(colors='#aabec6')
    fig.text(.1,.07,'NOT A GROUND-FLOOR PLAN. No physical floors or enclosed rooms have been built.',color='#edc786',fontsize=12)
    fig.savefig(ROOT/'B10_SOURCE_CENTRE.png',facecolor=fig.get_facecolor(),bbox_inches='tight');plt.close(fig)
    (ROOT/'B10_AUDIT.json').write_text(json.dumps(audit_result,indent=2,ensure_ascii=False)+'\n')
    return audit_result

if __name__=='__main__':print(json.dumps(export(),ensure_ascii=False,indent=2))
