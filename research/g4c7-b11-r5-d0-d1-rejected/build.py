"""G4-C7 B11-R5 D0/D1: inhabitance-led megastructure hypothesis.
RESEARCH ONLY; no safety, art, or Minecraft certification.
Pure geometrical source: numpy, trimesh, vtk only.  The same parts feed all views.
"""
from pathlib import Path
import json, hashlib, math, sys
import numpy as np
import trimesh
OUT=Path(__file__).resolve().parent
PARTS={k:[] for k in ['terrain','civic','workshop','gallery','research','habitation','shell','support','skylight']}
COLORS={'terrain':[77,99,114,255],'civic':[236,199,138,255],'workshop':[230,154,113,255],'gallery':[89,215,210,255],'research':[142,172,224,255],'habitation':[223,217,187,255],'shell':[195,209,217,255],'support':[108,128,153,255],'skylight':[107,239,211,255]}


def quad(a,b,c,d,part):
    v=np.asarray([a,b,c,d],float)
    if not np.isfinite(v).all():raise ValueError('invalid coordinates')
    PARTS[part].append(trimesh.Trimesh(vertices=v,faces=[[0,1,2],[0,2,3]],process=False))

def poly_slab(points,zlo,zhi,part):
    pts=np.asarray(points,float);n=len(pts)
    if n<3:raise ValueError('empty slab')
    vs=np.vstack([np.c_[pts,np.full(n,zlo)],np.c_[pts,np.full(n,zhi)]])
    fs=[]
    for j in range(1,n-1):fs.extend([[0,j+1,j],[n,n+j,n+j+1]])
    for j in range(n):k=(j+1)%n;fs.extend([[j,k,n+k],[j,n+k,n+j]])
    PARTS[part].append(trimesh.Trimesh(vertices=vs,faces=fs,process=False))

def segment(a,b,w,thickness,part):
    a=np.array(a,float);b=np.array(b,float);d=b-a;h=np.linalg.norm(d[:2]);u=np.array([-d[1]/h,d[0]/h,0])
    corners=np.array([a+u*w/2,a-u*w/2,b-u*w/2,b+u*w/2]);
    roof=corners+np.array([0,0,thickness]);floor=corners-np.array([0,0,thickness]);
    vs=np.vstack([floor,roof]);fs=[[0,1,2],[0,2,3],[4,6,5],[4,7,6]]
    for i in range(4):j=(i+1)%4;fs.extend([[i,j,j+4],[i,j+4,i+4]])
    PARTS[part].append(trimesh.Trimesh(vertices=vs,faces=fs,process=False))

def fold(knots,widths,tilts,thickness,part):
    """Hollow-space boundary from activity-linked nonparallel arch strips.
    Each knot fixes a section with left and right roof edges; no circular bands.
    """
    knots=np.asarray(knots,float);p=[]
    for i,k in enumerate(knots):
        f=knots[min(i+1,len(knots)-1)]-knots[max(i-1,0)];length=np.linalg.norm(f[:2]);
        u=np.array([-f[1]/length,f[0]/length,0]);a=k+u*widths[i]*.5+[0,0,tilts[i]];b=k-u*widths[i]*.5-[0,0,tilts[i]]
        p.append((a,b))
    vs=[]
    for a,b in p:vs.extend([a,b,a-np.array([0,0,thickness]),b-np.array([0,0,thickness])])
    for i in range(len(p)-1):
        v0=4*i;v1=4*(i+1)
        for a,b,c,d in [(0,1,1,0),(0,2,2,0),(1,3,3,1),(2,3,3,2)]:
            # Handles top, each side and bottom of thick fold between successive sections
            if a==b:continue
            quad(vs[v0+a],vs[v0+b],vs[v1+c],vs[v1+d],part)
        quad(vs[v0],vs[v0+1],vs[v1+1],vs[v1],part)
        quad(vs[v0+2],vs[v1+2],vs[v1+3],vs[v0+3],part)
    a,b=p[0];quad(a,b,b-[0,0,thickness],a-[0,0,thickness],part)
    a,b=p[-1];quad(a-[0,0,thickness],b-[0,0,thickness],b,a,part)

def ribbon(points,widths,part,thickness=2.0):
    """Footway / sheltered viewing gallery surface. A ribbon is not a certified ramp."""
    fold(points,widths,[0.0]*len(points),thickness,part)


def create(clearance=62, variant='base'):
    assert 45<=clearance<=85
    delta=clearance-62
    # Broad differentiated site edges, not a full-city rectangular base floor.
    poly_slab([[-760,-405],[-585,-532],[-255,-495],[-24,-340],[-115,-188],[-420,-175],[-703,-255]],-4,5,'terrain')
    poly_slab([[-220,-370],[120,-390],[420,-240],[585,-70],[557,175],[328,243],[60,113]],-9,5,'terrain')
    poly_slab([[-455,110],[-245,175],[10,378],[335,455],[488,617],[140,667],[-210,541],[-560,350]],-30,9,'terrain')

    # Sequence A: southern public entry where both visitor flows enter a civic threshold.
    poly_slab([[-695,-388],[-540,-410],[-392,-314],[-440,-206],[-601,-227]],10,17,'civic')
    poly_slab([[-382,-326],[-190,-361],[-37,-226],[-90,-78],[-300,-102],[-425,-185]],15,22,'civic')
    # Sequence B: actual workshop floor controls the span to be cleared.
    hall=[[-342,-252],[-104,-306],[108,-187],[129,-19],[-9,104],[-249,63],[-359,-86]]
    poly_slab(hall,20,27,'workshop')
    # Work hall's occupiable clear height is clearance, not a label-only input.
    # Folded public roof is raised with clearance, and research / gallery interface follows.
    fold([[-491,-316,58+delta],[-418,-175,91+delta],[-286,-37,127+delta],[-84,82,135+delta],[108,199,110+delta],[337,269,152+delta]],
         [90,160,225,195,117,52],[10,-17,38,-33,22,4],13,'shell')
    fold([[-261,-397,54+delta],[-132,-296,88+delta],[28,-140,124+delta],[156,26,141+delta],[226,187,174+delta],[361,338,207+delta]],
         [42,142,178,152,104,25],[-7,30,-16,26,-12,0],11,'shell')
    # The workshop has two genuinely open ends and daylight between diverging roof wings.
    # Wide lower buttresses are not wall-like constant-height extrusion.
    poly_slab([[-469,-209],[-421,-115],[-355,-37],[-303,-75],[-371,-211]],12,74+delta,'support')
    poly_slab([[86,-232],[138,-184],[194,-48],[145,16],[89,-47]],11,85+delta,'support')
    # The visiting route has galleries at different heights; vertical links are proposals, NOT tested.
    ribbon([[-565,-330,28],[-392,-232,37],[-225,-162,58+delta*.35],[-28,-50,78+delta*.6],[128,81,112+delta],[216,194,153+delta]],
           [34,28,27,22,19,25],'gallery')
    # B's work process has purpose-built overlook bays and skylight apertures.
    poly_slab([[-246,-59],[-96,-117],[20,-34],[-83,36]],62+delta*.4,66+delta*.4,'gallery')
    # Research / Culture: asymmetrical elevated occupied terraces and volumetric rooms.
    culture_z=144+delta
    poly_slab([[-16,128],[147,84],[348,169],[306,332],[104,323],[-91,234]],culture_z,culture_z+12,'research')
    poly_slab([[95,244],[252,203],[380,329],[283,456],[75,419]],culture_z+44,culture_z+53,'research')
    # Institution walls enclose partial real volumes; no fake claim to certified rooms.
    poly_slab([[36,142],[159,136],[189,240],[98,269]],culture_z+12,culture_z+62,'research')
    poly_slab([[205,211],[302,220],[319,315],[238,347]],culture_z+12,culture_z+79,'research')
    # A landscape roof grows from the research volume into the inhabited ridge.
    fold([[30,100,culture_z+95],[110,174,culture_z+108],[204,290,culture_z+160],[285,415,culture_z+185],[387,542,culture_z+220]],
         [170,226,164,131,43],[24,-26,34,-21,5],18,'shell')
    # Upper inhabited mass is a deliberately varied spatial cluster, not repeated units on shelves.
    residents=282+delta*.75
    clusters=[([[-162,271],[-35,229],[63,329],[0,454],[-135,411]],residents-17,residents+37),
              ([[-40,367],[100,341],[172,460],[75,546],[-80,526]],residents+51,residents+116),
              ([[186,369],[305,338],[396,452],[293,532],[183,504]],residents+3,residents+67),
              ([[44,525],[176,491],[275,606],[126,639]],residents+82,residents+142)]
    for footprint,z1,z2 in clusters:poly_slab(footprint,z1,z2,'habitation')
    # Upper civic terraces face away from the private frontages; connectedness unresolved.
    ribbon([[-91,238,culture_z+18],[23,296,culture_z+52],[127,350,residents+4],[256,429,residents+40],[289,520,residents+88]],
           [27,23,24,22,20],'gallery',thickness=3)
    # Deep apertures are located along visible workshop/public sightlines (no fake vertical windows).
    fold([[-325,-141,142+delta],[-232,-60,152+delta],[-126,12,150+delta]],
         [28,36,29],[-3,5,-7],3,'skylight')
    # Integrated support branches (not load-engineered).
    for a,b,w in [([-210,-58,22],[-146,-15,127+delta],22),
                  ([118,18,16],[150,62,139+delta],19),
                  ([81,166,29],[108,173,culture_z+95],24),
                  ([305,293,16],[273,348,culture_z+111],19),
                  ([130,421,48],[100,445,residents+10],30)]:segment(a,b,w,9,'support')
    # Urban sight-line slots: open space is not filled with a ring or central dark void.
    metadata={
        'project':'G4-C7 B11-R5 D0-D1','variant':variant,'workshop_clear_height_input_m':clearance,
        'programs':['two-sided civic entrance','open fabrication workshop','public observation gallery','elevated research and culture','upper inhabited mass'],
        'causal_dependency':{'workshop_roof':f'clearance delta={delta}', 'public_overlook_height':62+delta*.4,'research_base_height':culture_z,'inhabitation_base_height':residents},
        'unverified':['waterproof enclosed rooms','person-width path','continuous stairs and ramp grades','loads and support','egress','natural light performance','MakeCode conversion','Minecraft construction'],
        'formal_331_993':'NOT_RUN','formal_S1_G1_G2_G3':'NOT_RUN','G0_art':'NOT_ADOPTED','minecraft':'FORBIDDEN','research_only':True
    }
    return metadata

def export(variant,clearance):
    for k in PARTS:PARTS[k].clear()
    meta=create(clearance,variant)
    folder=OUT/variant;folder.mkdir(parents=True,exist_ok=True)
    meshes=[]
    for category,shapes in PARTS.items():
        m=trimesh.util.concatenate(shapes)
        m.visual.vertex_colors=COLORS[category]
        m.export(folder/(category+'.ply'))
        meshes.append(m)
    full=trimesh.util.concatenate(meshes);full.export(folder/'model.obj')
    for f in folder.glob('*.ply'):meta.setdefault('part_sha256',{})[f.stem]=hashlib.sha256(f.read_bytes()).hexdigest()
    meta.update(obj_sha256=hashlib.sha256((folder/'model.obj').read_bytes()).hexdigest(),faces=len(full.faces),vertices=len(full.vertices),bounds_m=full.bounds.tolist())
    (folder/'manifest.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2))
    return full,meta

def render(folder,meta):
    import vtk
    vtk.vtkObject.GlobalWarningDisplayOff()
    geometry=[]
    for key,color in COLORS.items():
        r=vtk.vtkPLYReader();r.SetFileName(str(folder/(key+'.ply')));r.Update()
        poly=r.GetOutput();mapper=vtk.vtkPolyDataMapper();mapper.SetInputData(poly)
        actor=vtk.vtkActor();actor.SetMapper(mapper)
        actor.GetProperty().SetColor(*(v/255 for v in color[:3]))
        actor.GetProperty().SetAmbient(.32);actor.GetProperty().SetDiffuse(.68)
        actor.GetProperty().SetSpecular(.18);actor.GetProperty().SetSpecularPower(13)
        geometry.append(actor)
    pics={
      'macro':([-1540,-1870,1250],[-5,25,175],30),
      'district':([980,-990,560],[-70,50,150],45),
      'public_eye':([-780,-525,24],[-145,-65,105],65),
      'upper_eye':([170,315,340],[-300,-100,155],72)
    }
    for name,(pos,look,fov) in pics.items():
        ren=vtk.vtkRenderer();ren.SetBackground(.055,.075,.112);ren.SetBackground2(.23,.31,.42);ren.GradientBackgroundOn()
        for actor in geometry:ren.AddActor(actor)
        cam=ren.GetActiveCamera();cam.SetPosition(*pos);cam.SetFocalPoint(*look);cam.SetViewUp(0,0,1);cam.SetViewAngle(fov)
        ren.ResetCameraClippingRange()
        win=vtk.vtkRenderWindow();win.SetOffScreenRendering(1);win.SetSize(1400,900);win.SetMultiSamples(8);win.AddRenderer(ren)
        win.Render()
        f=vtk.vtkWindowToImageFilter();f.SetInput(win);f.Update()
        w=vtk.vtkPNGWriter();w.SetFileName(str(folder/(name+'.png')));w.SetInputConnection(f.GetOutputPort());w.Write()
        win.Finalize()
        print('RENDER',meta['variant'],name, flush=True)
if __name__=='__main__':
    base,m=export('baseline',62)
    assert m['faces']>100 and m['bounds_m'][1][2]>350
    trial,n=export('clearance_plus20',82)
    assert n['obj_sha256']!=m['obj_sha256']
    assert n['causal_dependency']['research_base_height']==m['causal_dependency']['research_base_height']+20
    for folder,meta in [('baseline',m),('clearance_plus20',n)]:render(OUT/folder,meta)
    print('MANIFEST',json.dumps({x:{'sha':mm['obj_sha256'],'faces':mm['faces'],'bounds':mm['bounds_m']} for x,mm in [('baseline',m),('clearance_plus20',n)]},ensure_ascii=False))
