"""D24 real-3D experimental civic street / occupied terraces. Not a certified city.
Architectural hypothesis: a walkable civic sequence generates deeply open maker/research
frontages and staggered inhabited terraces. ART review remains independent, not certified.
"""
import argparse,json,math
from pathlib import Path
import numpy as np
import trimesh

P={'ground':(202,198,185,255),'route':(220,177,124,255),'maker':(166,196,185,255),
'research':(117,177,186,255),'culture':(193,177,153,255),'housing':(165,177,153,255),
'stone':(103,128,132,255),'glazing':(99,187,204,255),'wood':(218,167,106,255),
'plant':(79,136,105,255),'person':(203,107,83,255),'art':(214,184,121,255),
'metal':(72,95,105,255),'glass':(141,215,223,255)}
ROUTE=[(3,-85),(5,-64),(1,-43),(-3,-18),(-4,4),(-1,26),(5,49),(8,72),(7,88)]
BLOCKS=[
 {'name':'maker','side':-1,'y0':-66,'y1':-11,'front':-25,'back':-91,'z':36,'role':'maker'},
 {'name':'culture','side':-1,'y0':-10,'y1':39,'front':-28,'back':-89,'z':25,'role':'culture'},
 {'name':'west_home','side':-1,'y0':41,'y1':85,'front':-32,'back':-79,'z':47,'role':'housing'},
 {'name':'research','side':1,'y0':-47,'y1':22,'front':25,'back':90,'z':43,'role':'research'},
 {'name':'east_home','side':1,'y0':24,'y1':84,'front':34,'back':99,'z':58,'role':'housing'},
]
EYES={'civic':(2,-41,2.3),'maker':(-9,-36,2.3),'research':(13,-28,2.3)}
TARGETS={'maker':(-42,-29,2.9),'research':(44,-22,3.2)}
CAMERAS={
 '01_macro':((208,-242,166),(0,2,18),49),
 '02_district':((136,-152,91),(0,-1,16),58),
 '03_civic_eye':((2,-67,2.5),(1,-8,10),78),
 '04_maker_eye':((-7,-47,2.35),(-43,-25,7),70),
 '05_research_eye':((8,-43,2.35),(44,-21,9),71),
 '06_upper':((42,65,33),(-22,0,16),72),
}

def add(scene,name,m,role):
    colors=np.asarray(P[role],dtype=np.uint8)
    m.visual.vertex_colors=np.tile(colors,(len(m.vertices),1))
    scene.add_geometry(m,geom_name=name,node_name=name)

def box(scene,name,p,extent,role):
    m=trimesh.creation.box(extents=extent);m.apply_translation(p);add(scene,name,m,role)

def span(scene,name,a,b,width,height,role):
    a,b=np.asarray(a,float),np.asarray(b,float);d=b-a
    l=np.linalg.norm(d[:2]);m=trimesh.creation.box(extents=(l,width,height))
    m.apply_transform(trimesh.transformations.rotation_matrix(math.atan2(d[1],d[0]),[0,0,1]))
    m.apply_translation((a+b)/2);add(scene,name,m,role)

def floor(scene,name,x0,x1,y0,y1,z,role='stone',thick=1.3):
    box(scene,name,((x0+x1)/2,(y0+y1)/2,z-thick/2),(abs(x1-x0),y1-y0,thick),role)

def banc(scene,b):
    key=b['name'];side=b['side'];f=b['front'];o=b['back'];a=b['y0'];z=b['y1'];ht=b['z'];role=b['role'];
    small=min(o,f);large=max(o,f);gap=large-small
    floor(scene,key+'__ground_floor',small,large,a,z,0.5,role)
    # Concave graduated public thresholds facing a single continuous promenade.
    # Deep front openings are real VOID not blue painted wall, allowing activity exposure.
    bounds=[a,a+(z-a)*.23,a+(z-a)*.56,z]
    for i in range(4):
        y=a+(z-a)*i/4
        box(scene,f'{key}__ground_pier_{i}',(f+side*1.7,y,6.3),(3.8,3.5,11.4),'stone')
    ymid=(a+z)/2
    floor(scene,key+'__rear_backbone',o,f+side*18,a,z,13.4,'stone',3.1)
    box(scene,key+'__rear_wall',((o+side*3),ymid,ht*.48),(5,z-a,ht*.96),'stone')
    # Stepped occupied terraces: each level is bordered by a thick grounded rear building mass;
    # NOT a continuous unsupported elevated sidewalk or bridge.
    for level,H in enumerate((14.2,26.8,39.4,51.6)):
        if H+4>ht:continue
        depth=17+5.0*(level%2);yA=a+2+(level%2)*4;yB=z-2-(level%3)*4
        xinner=f+side*(7+level*4);xouter=f+side*(depth+17+level*4)
        lo,hi=sorted((xinner,xouter))
        floor(scene,f'{key}__inhabited_level_{level}',lo,hi,yA,yB,H,'housing' if role=='housing' else role,2.0)
        # Exterior supports are continuous enclosed solid volumes rooted at ground.
        for at in [yA+1,yB-1]:
            box(scene,f'{key}__bearing_mass_{level}_{int(at)}',(xouter+side*1,at,H*.50),
                (9,5,H),'stone')
        # Distinct inhabited scale is visible as window bays and balcony openings.
        for q in range(3):
            yy=yA+(q+.5)*(yB-yA)/3
            box(scene,f'{key}__window_{level}_{q}',(xouter+side*1,yy,H+4.2),
                (3.2,(yB-yA)/4.5,5.5),'glazing')
        for q in range(4):
            yy=yA+(q+.5)*(yB-yA)/4
            box(scene,f'{key}__planter_{level}_{q}',(xinner,yy,H+1.2),
                (3.5,3.8,1.6),'plant')
    # Short independent roof pieces are supported by the thick rear building, not mega-canopies.
    strips=6
    for j in range(strips):
        ya=a+j*(z-a)/strips;yb=a+(j+1)*(z-a)/strips
        rise=1.5*math.sin(j*.85+(.5 if side==1 else 0))
        floor(scene,f'{key}__top_ridge_{j}',o,f+side*(21+2*math.sin(j)),ya,yb,ht+rise,role,1.6)
    # A clear activity-specific open bay (no separate opaque pavilion inserted in front).
    if key=='maker':
        for j in range(3):
            box(scene,f'maker__equipment_{j}',(-42,-49+14*j,1.65),(9,6,2.5),'wood')
            box(scene,f'maker__machine_{j}',(-42,-49+14*j,4.3),(2.2,2.2,3.4),'metal')
        span(scene,'maker__gantry',(-52,-28,10),(-35,-28,10),1.8,1.2,'metal')
    if key=='research':
        for j in range(4):
            box(scene,f'research__instrument_{j}',(45,-36+13*j,2.3),(4.2,3.6,3.2),'glass')
            box(scene,f'research__lab_table_{j}',(52,-36+13*j,1.2),(7,4,1.8),'metal')
    if key=='culture':
        for j in range(4):
            box(scene,f'culture__table_{j}',(-39,-3+9*j,1.2),(7,3,1.2),'wood')
    return {'id':key,'role':role,'xfront':f,'xback':o,'y':(a,z),'height':ht}

def build(case):
    scene=trimesh.Scene()
    box(scene,'site_terrain',(0,0,-1.3),(225,207,2.6),'ground')
    for i,(a,b) in enumerate(zip(ROUTE,ROUTE[1:])):
        span(scene,f'civic_walk_{i}',(*a,.42),(*b,.42),12.0,.68,'route')
    # Two cultural squares with integrated public furnishings / trees.
    floor(scene,'civic_shared_court',-20,21,-15,27,.48,'route',.8)
    floor(scene,'civic_south_concourse',-19,20,-76,-38,.48,'route',.8)
    for i,(x,y) in enumerate([(-15,3),(14,29),(-8,-62),(16,-10),(10,57)]):
        m=trimesh.creation.cylinder(radius=1.4,height=1.0,sections=12);m.apply_translation((x,y,1.4));add(scene,f'civic_planter_{i}',m,'stone')
        trunk=trimesh.creation.cylinder(radius=.35,height=5.3,sections=10);trunk.apply_translation((x,y,4.5));add(scene,f'civic_tree_trunk_{i}',trunk,'wood')
        ball=trimesh.creation.icosphere(subdivisions=1,radius=3.9);ball.apply_translation((x,y,8));add(scene,f'civic_tree_crown_{i}',ball,'plant')
    roles=[]
    for b in BLOCKS:
        if case=='no_maker' and b['name']=='maker':continue
        if case=='no_research' and b['name']=='research':continue
        roles.append(banc(scene,b))
    for n,(x,y) in enumerate([(-6,-30),(7,-17),(-9,12),(6,36),(0,-55),(-14,46)]):
        c=trimesh.creation.cylinder(radius=.51,height=1.73,sections=8);c.apply_translation((x,y,1.4));add(scene,f'public_person_{n}',c,'person')
    return scene,roles

def render(path,out):
    import vtk
    saved=trimesh.load(path,force='scene',process=False)
    out.mkdir(parents=True,exist_ok=True)
    for key,(eye,target,fov) in CAMERAS.items():
        ren=vtk.vtkRenderer();ren.SetBackground(.89,.94,.97)
        win=vtk.vtkRenderWindow();win.SetOffScreenRendering(1);win.AddRenderer(ren);win.SetSize(1200,700)
        for node in saved.graph.nodes_geometry:
            transform,gn=saved.graph[node];g=saved.geometry[gn].copy();g.apply_transform(transform)
            if not len(g.faces):continue
            pts=vtk.vtkPoints();pts.SetNumberOfPoints(len(g.vertices))
            for i,p in enumerate(g.vertices):pts.SetPoint(i,*[float(v) for v in p])
            cells=vtk.vtkCellArray()
            for tri in g.faces:
                f=vtk.vtkTriangle()
                for j,k in enumerate(tri):f.GetPointIds().SetId(j,int(k))
                cells.InsertNextCell(f)
            pdata=vtk.vtkPolyData();pdata.SetPoints(pts);pdata.SetPolys(cells)
            m=vtk.vtkPolyDataMapper();m.SetInputData(pdata)
            actor=vtk.vtkActor();actor.SetMapper(m)
            col=np.asarray(g.visual.vertex_colors)
            if len(col):actor.GetProperty().SetColor(*(col.mean(axis=0)[:3]/255).tolist())
            actor.GetProperty().SetAmbient(.28)
            ren.AddActor(actor)
        cam=ren.GetActiveCamera();cam.SetPosition(*eye);cam.SetFocalPoint(*target);cam.SetViewUp(0,0,1);cam.SetViewAngle(fov)
        ren.ResetCameraClippingRange();win.Render()
        w=vtk.vtkWindowToImageFilter();w.SetInput(win);w.Update();pw=vtk.vtkPNGWriter()
        pw.SetFileName(str(out/(key+'.png')));pw.SetInputConnection(w.GetOutputPort());pw.Write();win.Finalize()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='d24_build');v=ap.parse_args();out=Path(v.out);out.mkdir(parents=True,exist_ok=True)
    manifest={'stage':'B11-R5 D24','category':'LOCAL_SAVED_3D_EXPERIMENT','route':ROUTE,'eyes':EYES,'targets':TARGETS,'scenes':{},
      'protection':{'ART':'HOLD','adopted':0,'formal_G0':'NOT_RUN','formal_S1_G1_G2_G3':'NOT_RUN','construction':'FORBIDDEN','integration':'FORBIDDEN','draft_PR53':'OPEN','main':'UNTOUCHED'}}
    for case in ('baseline','no_maker','no_research'):
        scene,roles=build(case)
        fp=out/f'd24_{case}.glb';fp.write_bytes(scene.export(file_type='glb'))
        manifest['scenes'][case]={'file':fp.name,'roles':roles,'nodes':len(scene.graph.nodes_geometry)}
    (out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    render(out/'d24_baseline.glb',out)
    print('D24 three saved GLBs and 6 rendered views. No ART PASS or certification.')
if __name__=='__main__':main()
