"""G4-C7 B11-R2: falsifiable, real-triangle dependency study, NOT city art or safety QA.

The semantic requirements yield public void, occupied bands, and external outline
from a shared cross-section; no independently placed 'decorative road'.
"""
from __future__ import annotations
import argparse, hashlib, json, math
from pathlib import Path
import numpy as np
import trimesh

N=81
XS=np.linspace(-185.,185.,N)
ROUTE_NODES=(-132.,-36.,64.,143.)
GROUPS=('public','occupied','envelope','supports','activity')
COLORS={'public':(85,174,196,255),'occupied':(154,185,190,255),'envelope':(57,99,145,255),'supports':(82,105,113,255),'activity':(244,184,94,255)}

def gaussian(x,center,width):return np.exp(-((x-center)/width)**2)

def parameters(plaza_demand=1.,home_need=1.,bridge_open=True):
    """One design brief. Plaza demand and housing need both alter *real* public/occupied/envelope geometry."""
    if not (.7<=plaza_demand<=1.4 and .7<=home_need<=1.4):
        raise ValueError('OUTSIDE_DEFINED_SOURCE_STUDY_RANGE')
    x=XS
    activity=(gaussian(x,-116,48)+1.20*gaussian(x,35,71)+.75*gaussian(x,136,39))
    center=14*np.sin(x/95)+4*np.sin(x/31)
    void_half=11.+plaza_demand*(6.+5.5*activity)-home_need*1.8
    depth=10.+home_need*(8.+2*activity)+plaza_demand*.8
    outer_half=void_half+depth
    top=33.+7*activity+6*home_need+5*plaza_demand
    # Source-only temporary void cut: falsifiable by a bridge-volume blocker.
    if not bridge_open:
        void_half=np.array(void_half)
        void_half[np.abs(x-35.)<16.]=.25
    return dict(x=x,center=center,void=void_half,room=depth,outer=outer_half,roof=top,
                activity=activity,plaza_demand=plaza_demand,home_need=home_need,bridge_open=bridge_open)

class Builder:
 def __init__(self):
    self.tris={g:[] for g in GROUPS}
 def triangle(self,group,a,b,c):self.tris[group].append([a,b,c])
 def quad(self,group,a,b,c,d):
    self.triangle(group,a,b,c);self.triangle(group,a,c,d)
 def strip(self,group,lower,upper):
    for i in range(N-1):
      self.quad(group,lower[i],lower[i+1],upper[i+1],upper[i])
 def mesh(self,group):
    tri=np.asarray(self.tris[group],dtype=np.float64)
    v=tri.reshape(-1,3)
    return trimesh.Trimesh(vertices=v,faces=np.arange(len(v)).reshape(-1,3),process=False)

def design_mesh(brief):
    x,cy,w,d,h=(brief[k] for k in ('x','center','void','room','roof'))
    b=Builder()
    # Two sides of one actual civic void at low and upper levels. A band may be
    # empty on one side; facades below are split to preserve actual openings.
    def p(y,z):return np.stack([x,y,np.full(N,z)],axis=1)
    # lower shared slab and two occupied floor strata, all from identical boundaries
    b.strip('public',p(cy-w,0),p(cy+w,0))
    b.strip('public',p(cy-w*.53,17),p(cy+w*.53,17))
    for sign in (-1,1):
      inside=cy+sign*w
      outer=cy+sign*(w+d)
      for z in (0,13,27):
       b.strip('occupied',p(inside,z),p(outer,z))
      # Each occupied section's own upper termination derives from the room demand.
      b.strip('envelope',np.stack([x,outer,h-6],axis=1),np.stack([x,inside+sign*2.5,h],axis=1))
      # irregular facades with 4 named passages, no fake closed rectangular room assertions
      for i in range(N-1):
       cx=(x[i]+x[i+1])/2
       opening=any(abs(cx-node)<8 for node in ROUTE_NODES)
       for z0,z1 in ((0,13),(13,27),(27,42)):
        if opening and z0 in (0,13):
         # Real opening: no triangles across the central 3.8m tall access region.
         base=z0+4.4
        else:base=z0
        # facade boundary portions above the apertures and full facades elsewhere
        aa=(x[i],inside[i],base);bb=(x[i+1],inside[i+1],base)
        cc=(x[i+1],inside[i+1],z1);dd=(x[i],inside[i],z1)
        if z1>base:b.quad('envelope',aa,bb,cc,dd)
       # real outside skin whose extent is dictated by the same room depth
       lo=(x[i],outer[i],0);hi=(x[i],outer[i],h[i]);lo2=(x[i+1],outer[i+1],0);hi2=(x[i+1],outer[i+1],h[i+1])
       b.quad('envelope',lo,lo2,hi2,hi)
      # grouped support sections, explicitly *not* analyzed for structural load
      for i in range(0,N,8):
        xi=x[i]; yi=outer[i]-sign*1.2;zt=h[i]
        a=(xi-1,yi-1,0);c=(xi+1,yi+1,zt)
        for j in range(4):
         angle=j*math.pi/2; ang2=(j+1)*math.pi/2
         p0=(xi+1.4*math.cos(angle),yi+1.4*math.sin(angle),0)
         p1=(xi+1.4*math.cos(ang2),yi+1.4*math.sin(ang2),0)
         p2=(p1[0],p1[1],zt);p3=(p0[0],p0[1],zt)
         b.quad('supports',p0,p1,p2,p3)
    # activity-led facing galleries: top/width based on same civic nodes and shared surfaces
    for node in ROUTE_NODES:
      ix=np.argmin(abs(x-node)); z=28.+7*brief['activity'][ix]
      for s in (-1,1):
       inner=cy[ix]+s*(w[ix]*.55); outer=cy[ix]+s*(w[ix]+d[ix]*.42)
       xx=x[ix];r=3.
       b.quad('activity',(xx-r,inner,z),(xx+r,inner,z),(xx+r,outer,z),(xx-r,outer,z))
    return {g:b.mesh(g) for g in GROUPS}

def raw_digest(mesh):return hashlib.sha256(mesh.vertices.tobytes()+mesh.faces.tobytes()).hexdigest()

def profile(brief):
    return {'void_width_at_nodes_m':[round(float(2*brief['void'][np.argmin(abs(brief['x']-n))]),3) for n in ROUTE_NODES],
      'occupied_depth_at_nodes_m':[round(float(brief['room'][np.argmin(abs(brief['x']-n))]),3) for n in ROUTE_NODES],
      'outer_halfspan_max_m':round(float(brief['outer'].max()),3),
      'roof_max_height_m':round(float(brief['roof'].max()),3),
      'min_clear_void_width_m':round(float((2*brief['void']).min()),3)}

def package(root:Path,plaza=1.,home=1.,bridge_open=True):
    root.mkdir(parents=True,exist_ok=False)
    brief=parameters(plaza,home,bridge_open)
    parts=design_mesh(brief)
    manifest={'study':'B11_R2_REAL_TRIANGLE_CAUSAL_SECTION_NOT_AN_ART_CANDIDATE',
      'parameters':{'plaza':plaza,'home_need':home,'bridge_open':bridge_open},
      'source_void_width_gate':'PASS_SOURCE_ONLY' if profile(brief)['min_clear_void_width_m']>=8 else 'REJECT_NARROW_SOURCE_VOID',
      'profile':profile(brief), 'parts':{},
      'official_art':'HOLD', 'formal_adoptions':0,'real_enclosed_rooms':'NOT_TESTED',
      'human_331_foot_993':'NOT_RUN','formal_s1_g1_g2_g3':'NOT_RUN',
      'structural_load':'NOT_TESTED','actual_safe_walk':'NOT_TESTED',
      'minecraft_construction':'FORBIDDEN'}
    for name,mesh in parts.items():
      m=root/f'{name}.ply'; mesh.visual.vertex_colors=COLORS[name];mesh.export(m)
      manifest['parts'][name]={'faces':len(mesh.faces),'vertices':len(mesh.vertices),
               'triangle_digest':raw_digest(mesh), 'file_sha256':hashlib.sha256(m.read_bytes()).hexdigest()}
    (root/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    return manifest

def render(root:Path,frames=('macro','public_eye')):
    import vtk
    from PIL import Image
    for camera in frames:
      ren=vtk.vtkRenderer();ren.SetBackground(.038,.072,.112)
      for group in GROUPS:
        reader=vtk.vtkPLYReader();reader.SetFileName(str(root/(group+'.ply')));reader.Update()
        mapper=vtk.vtkPolyDataMapper();mapper.SetInputConnection(reader.GetOutputPort())
        actor=vtk.vtkActor();actor.SetMapper(mapper)
        rgb=COLORS[group];actor.GetProperty().SetColor(*(v/255 for v in rgb[:3]))
        actor.GetProperty().SetAmbient(.24);actor.GetProperty().SetDiffuse(.72);actor.GetProperty().SetSpecular(.13)
        ren.AddActor(actor)
      if camera=='macro':pos=(480,-470,320);foc=(0,0,25)
      else:pos=(-135,-16,10);foc=(18,3,17)
      c=ren.GetActiveCamera();c.SetPosition(*pos);c.SetFocalPoint(*foc);c.SetViewUp(0,0,1)
      c.SetClippingRange(.1,2000)
      w=vtk.vtkRenderWindow();w.OffScreenRenderingOn();w.SetSize(1300,840);w.AddRenderer(ren)
      w.Render()
      f=vtk.vtkWindowToImageFilter();f.SetInput(w);f.Update()
      writer=vtk.vtkPNGWriter();writer.SetFileName(str(root/(camera+'.png')));writer.SetInputConnection(f.GetOutputPort());writer.Write()
      with Image.open(root/(camera+'.png')) as im:assert im.size==(1300,840)
      w.Finalize()

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',default='output');parser.add_argument('--render',action='store_true');a=parser.parse_args()
    p=Path(a.output);p.mkdir(parents=True,exist_ok=True)
    for label,vals in [('baseline',(1.,1.,True)),('public_change',(1.22,1.,True)),('housing_change',(1.,1.24,True)),('cut',(1.,1.,False))]:
      manifest=package(p/label,*vals)
      if a.render and label in ('baseline','public_change'):
       render(p/label)
    print('B11_R2_GEOMETRY_COMPLETE__NO_ART_CANDIDATE')
