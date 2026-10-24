"""A6 autonomous real-GLB geometric study; no Blender / Minecraft.
Input: A5 original GLB. Y-up glTF coordinates, unlike Z-up .blend.
This script edits named meshes and exports a separate non-production GLB.
"""
import argparse, json, math
from pathlib import Path
import numpy as np
import trimesh
from trimesh.visual.material import PBRMaterial

STONE=(190,202,203,255)
DARK=(49,81,91,255)
GLASS=(50,121,146,210)
def color(mesh,rgba):
    mesh.visual=trimesh.visual.TextureVisuals(material=PBRMaterial(
        baseColorFactor=np.array(rgba,dtype=np.uint8),
        metallicFactor=.18,roughnessFactor=.64,doubleSided=True))
    return mesh

def make_loft(rows, rgba):
    verts=[]
    for z,c,l,r,bot,top in rows:
        verts.extend([[l,bot,z],[r,bot,z],[r,top,z],[l,top,z]])
    faces=[(0,2,1),(0,3,2)]
    for i in range(len(rows)-1):
        a,b=4*i,4*(i+1)
        for j in range(4):
            u,v=a+j,a+(j+1)%4;U,V=b+j,b+(j+1)%4
            faces.extend([(u,v,U),(v,V,U)])
    n=4*(len(rows)-1)
    faces.extend([(n,n+1,n+2),(n,n+2,n+3)])
    return color(trimesh.Trimesh(vertices=verts,faces=faces,process=False),rgba)

def gallery_rows(sign, part):
    rows=[]
    for i in range(31):
        s=i/30;z=-22.5+45*s
        bulge=math.sin(math.pi*s)
        center=sign*(22+2.5*bulge)+2.3*math.sin(2*math.pi*s)
        width=17.3+2.8*bulge
        floor=43.5+2.4*bulge+.6*math.cos(2*math.pi*s)
        roof=floor+9.1+3*bulge
        if part=="FLOOR": lo,hi=floor-1.4,floor+.4
        elif part=="ROOF": lo,hi=roof-1.7,roof+1.1
        else: lo,hi=floor+.4,roof-1.7
        left,right=center-width/2,center+width/2
        if part=="LEFTGLASS":right=left+.65
        if part=="RIGHTGLASS":left=right-.65
        rows.append((z,center,left,right,lo,hi))
    return rows

def cylinder(a,b,r,rgba):
    a,b=np.asarray(a,float),np.asarray(b,float)
    direction=b-a
    m=trimesh.creation.cylinder(radius=r,height=np.linalg.norm(direction),sections=10)
    m.apply_transform(trimesh.geometry.align_vectors([0,0,1],direction/np.linalg.norm(direction)))
    m.apply_translation((a+b)/2)
    return color(m,rgba)

def generate(source,output):
    base=trimesh.load(source,force="scene")
    if len(base.graph.nodes_geometry)!=436:
        raise ValueError("Expected 436 named A5 meshes; refusing unrelated model")
    result=trimesh.Scene()
    removed=[]
    for name in base.graph.nodes_geometry:
        mat,g=base.graph[name]
        drop=name.startswith(("Sky chamber ","TRANSVERSE outer load shell",
             "TRANSVERSE inner load shell","TRANSVERSE glazed occupied band",
             "TRANSVERSE diaphragm"))
        if drop:
            removed.append(name)
            continue
        mat=np.array(mat,copy=True)
        if name.startswith("Transverse vault ground footing"):
            mat[0,3]-=13
        result.add_geometry(base.geometry[g].copy(),geom_name=name,node_name=name,transform=mat)
    names=[]
    def add(name,mesh):
        result.add_geometry(mesh,geom_name=name,node_name=name)
        names.append(name)
    for side in [-1,1]:
        for typ in ["FLOOR","ROOF","LEFTGLASS","RIGHTGLASS"]:
            name="A6_CURVED_SKY_"+("WEST" if side<0 else "EAST")+"_"+typ
            add(name,make_loft(gallery_rows(side,typ),GLASS if "GLASS" in typ else STONE))
        for k,z in enumerate([-22,-12,0,12,22]):
            s=(z+22.5)/45;u=math.sin(math.pi*s)
            c=side*(22+2.5*u)+2.3*math.sin(2*math.pi*s)
            w=17.3+2.8*u
            h=43.5+2.4*u+.6*math.cos(2*math.pi*s)
            roof=h+9.1+3*u
            for j,x in enumerate((c-w/2,c+w/2)):
                add("A6_SKY_SUPPORT_%s_%s_%s"%(side,k,j),
                    cylinder([x,h,z],[x,roof,z],.55,DARK))
    for side in [-1,1]:
        x=-43+side*6.8
        for i in range(72):
            a=math.pi*i/72;b=math.pi*(i+1)/72
            add("A6_TRANSVERSE_%s_RIB_%02d"%(side,i),
                cylinder([x,2+52*math.sin(a),61*math.cos(a)],
                         [x,2+52*math.sin(b),61*math.cos(b)],1.9,STONE))
    for k,t in enumerate(np.linspace(.08,math.pi-.08,13)):
        y=2+52*math.sin(t);z=61*math.cos(t)
        add("A6_TRANSVERSE_WEB_%02d"%k,
            cylinder([-49.8,y,z],[-36.2,y,z],.8,DARK))
    for side in [-1,1]:
        for end in [-1,1]:
            block=trimesh.creation.box(extents=[5.2,2.8,14])
            block.apply_translation([-43+side*6.8,1.4,end*54])
            add("A6_TRANSVERSE_BASE_%s_%s"%(side,end),color(block,STONE))
    output.mkdir(parents=True,exist_ok=True)
    (output/"a6_orbital_commons_study.glb").write_bytes(result.export(file_type="glb"))
    (output/"a6_orbital_commons_study.obj").write_text(result.export(file_type="obj"),encoding="utf8")
    checks={
      "input_meshes":len(base.graph.nodes_geometry),
      "result_meshes":len(result.graph.nodes_geometry),
      "removed_named_meshes":len(removed),
      "new_named_meshes":len(names),
      "bounds_xyz":result.bounds.tolist(),
      "total_triangles":int(sum(len(m.faces) for m in result.geometry.values())),
      "curved_lofts_watertight":all(result.geometry[k].is_watertight for k in names if k.startswith("A6_CURVED_SKY")),
      "art_status":"HOLD",
      "human_walking":"NOT VERIFIED: no proof of apertures through all main-shell intersections",
      "hardware":"NOT CONSTRUCTED",
    }
    (output/"a6_reproducible_geometry_qa.json").write_text(
      json.dumps(checks,indent=2,ensure_ascii=False)+"\n",encoding="utf8")
    return checks

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--input",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    print(json.dumps(generate(args.input,args.out),ensure_ascii=False,indent=2))
