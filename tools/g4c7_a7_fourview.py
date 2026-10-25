"""Matched-camera, GLB-derived A6/A7 four-view evidence (Pillow orthographic).
Purpose: shape comparison only. Not Blender EEVEE, engineering or Minecraft.
"""
import argparse
from pathlib import Path
import numpy as np
import trimesh
from PIL import Image,ImageDraw,ImageFont

CAMERAS={
    "front":(0,57,300),
    "oblique":(225,190,290),
    "side":(300,64,0),
    "aerial":(90,390,110),
}
TARGET=np.array([0.,24.,0.])
LIGHT=np.array([.35,.72,.44]);LIGHT/=np.linalg.norm(LIGHT)
WIDTH,HEIGHT=960,720
SCALE=285.

def mesh_color(name):
    upper=name.upper()
    if "GLASS" in upper: return np.array([69,146,157],float)
    if "SKY" in upper or "RIB" in upper or "SHELL" in upper: return np.array([224,229,223],float)
    if "RAIL" in upper or "DIAPHRAGM" in upper or "COLUMN" in upper: return np.array([62,93,106],float)
    if "POOL" in upper or "WATER" in upper: return np.array([51,140,161],float)
    if "PLANTED" in upper: return np.array([84,141,112],float)
    if "ROAD" in upper: return np.array([53,65,75],float)
    if "DECK" in upper or "PROMENADE" in upper: return np.array([200,209,195],float)
    return np.array([161,180,181],float)

def render(scene,view):
    eye=np.array(CAMERAS[view],float)
    forward=TARGET-eye
    forward/=np.linalg.norm(forward)
    right=np.cross(forward,np.array([0.,1.,0.]))
    right/=np.linalg.norm(right)
    up=np.cross(right,forward)
    image=Image.new("RGB",(WIDTH,HEIGHT),(223,235,241))
    drawer=ImageDraw.Draw(image)
    triangles=[]
    for name in scene.graph.nodes_geometry:
        transform,key=scene.graph[name]
        mesh=scene.geometry[key]
        vertices=trimesh.transform_points(mesh.vertices,transform)
        vv=vertices[mesh.faces]
        if len(vv)==0: continue
        centers=vv.mean(axis=1)-TARGET
        depths=centers@forward
        xy=np.stack([(vv-TARGET)@right,(vv-TARGET)@up],axis=2)
        normals=np.cross(vv[:,1]-vv[:,0],vv[:,2]-vv[:,0])
        nl=np.linalg.norm(normals,axis=1)
        nl=np.maximum(nl,1e-12)
        shade=np.maximum(.15,np.abs(normals@LIGHT/nl))
        base=mesh_color(name)
        px=WIDTH/2 + xy[:,:,0]*(WIDTH/SCALE)
        py=HEIGHT/2 - xy[:,:,1]*(WIDTH/SCALE)
        for i in range(len(vv)):
            if px[i].max() < 0 or px[i].min() >= WIDTH or py[i].max() < 0 or py[i].min() >= HEIGHT:
                continue
            factor=.47+.53*shade[i]
            rgb=tuple(int(v) for v in np.clip(base*factor,0,255))
            polygon=tuple((round(float(px[i,j]),2),round(float(py[i,j]),2)) for j in range(3))
            triangles.append((float(depths[i]),polygon,rgb))
    # Painter ordering (not GPU depth buffer): genuine triangle projection, no image-generation edits.
    triangles.sort(key=lambda entry:entry[0],reverse=True)
    for _,poly,fill in triangles:
        drawer.polygon(poly,fill=fill)
    return image,len(triangles)

def generate(a6_path,a7_path,out):
    out.mkdir(parents=True,exist_ok=True)
    a6=trimesh.load(a6_path,force="scene")
    a7=trimesh.load(a7_path,force="scene")
    counts={}
    for view in CAMERAS:
        left,n0=render(a6,view)
        right,n1=render(a7,view)
        composite=Image.new("RGB",(2*WIDTH,HEIGHT+36),(244,246,246))
        composite.paste(left,(0,36))
        composite.paste(right,(WIDTH,36))
        draw=ImageDraw.Draw(composite)
        draw.text((24,10),"A6 - ART HOLD",fill=(15,25,30))
        draw.text((WIDTH+24,10),"A7 - ART HOLD / GEOMETRY STUDY",fill=(15,25,30))
        composite.save(out/(view+"_a6_a7.png"),optimize=True)
        counts[view]={"a6_visible_triangles":n0,"a7_visible_triangles":n1,
                      "camera":list(CAMERAS[view]),"scale":SCALE}
    import json
    (out/"view_provenance.json").write_text(json.dumps(
        {"method":"GLB triangle orthographic Pillow painter rasterization",
         "not":"Blender EEVEE / Minecraft screenshot / depth-perfect renderer",
         "fixed_target":TARGET.tolist(),"views":counts},indent=2)+"\n")
    return counts

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--a6",type=Path,required=True)
    p.add_argument("--a7",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    print(generate(a.a6,a.a7,a.out))
