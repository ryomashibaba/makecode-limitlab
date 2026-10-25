#!/usr/bin/env python3
"""G4-C7 A19 non-destructive OBJ replay / GLB conversion / matched four-view renderer.

Standard-library only. The archived OBJ files are the exact geometry source.
This script replays them; it does NOT regenerate the original parametric masses,
claim watertight union, run the 331/993 route sweep, edit Minecraft, or certify ART.
"""
from __future__ import annotations
import argparse
import json
import math
import struct
from pathlib import Path
from html import escape

COLORS = {
    "porcelain": ("#c7d6dc", (.78, .84, .87, 1.)),
    "slate": ("#5c788a", (.36, .47, .54, 1.)),
    "cobaltGlass": ("#54b7bb", (.33, .72, .73, 1.)),
    "terrace": ("#e5b67e", (.90, .71, .49, 1.)),
    "planting": ("#739f86", (.45, .62, .52, 1.)),
    "structure": ("#83949d", (.51, .58, .62, 1.)),
}
NAMES = {
    "a": "civic_caldera",
    "b": "trifurcated_commons",
    "c": "porous_agora",
}
TITLES = {
    "a": "CIVIC CALDERA",
    "b": "TRIFURCATED COMMONS",
    "c": "POROUS AGORA",
}
CAMERAS = {
    "front": (0., 156., -370.),
    "oblique": (275., 218., -270.),
    "side": (385., 180., 0.),
    "aerial": (180., 455., -195.),
}
TARGET = (0., 71., 0.)
SCALE = 1.27

def sub(a, b):
    return tuple(x-y for x,y in zip(a,b))

def dot(a, b):
    return sum(x*y for x,y in zip(a,b))

def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1],
            a[2]*b[0]-a[0]*b[2],
            a[0]*b[1]-a[1]*b[0])

def normalized(a):
    n=math.sqrt(dot(a,a))
    if n <= 0.: raise ValueError("Zero-length normal")
    return tuple(x/n for x in a)

def read_obj(path: Path):
    """Triangular OBJ with explicit materials. Reject all unsupported geometry."""
    verts, faces = [], []
    material = "porcelain"
    for raw in path.read_text(encoding="utf-8").splitlines():
        s=raw.split()
        if not s: continue
        if s[0]=="v":
            assert len(s)==4, (path,raw)
            verts.append(tuple(float(x) for x in s[1:]))
        elif s[0]=="usemtl":
            material=s[1]
            assert material in COLORS
        elif s[0]=="f":
            assert len(s)==4 and len(verts)>0
            idx=[int(t.split("/")[0])-1 for t in s[1:]]
            assert all(0 <= x < len(verts) for x in idx), (path,raw)
            faces.append((*idx, material))
    assert verts and faces, path
    assert all(math.sqrt(dot(cross(sub(verts[b],verts[a]),
                                   sub(verts[c],verts[a])),
                             cross(sub(verts[b],verts[a]),
                                   sub(verts[c],verts[a])))) > 1e-8
               for a,b,c,_ in faces), "Degenerate triangle"
    return {"verts":verts,"faces":faces}

def pad(data: bytes, byte: bytes) -> bytes:
    return data+byte*((-len(data))%4)

def export_glb(data, path: Path):
    verts, faces = data["verts"], data["faces"]
    positions=b"".join(struct.pack("<fff",*v) for v in verts)
    groups={name:[] for name in COLORS}
    for a,b,c,m in faces: groups[m].extend((a,b,c))
    chunks=[positions]+[b"".join(struct.pack("<I",i) for i in groups[m])
                        for m in COLORS]
    views=[]; offset=0
    for i,chunk in enumerate(chunks):
        views.append({"buffer":0,"byteOffset":offset,"byteLength":len(chunk),
                      "target":34962 if i==0 else 34963})
        offset+=len(chunk)
    bboxmin=[min(v[i] for v in verts) for i in range(3)]
    bboxmax=[max(v[i] for v in verts) for i in range(3)]
    accessors=[{"bufferView":0,"componentType":5126,
                "count":len(verts),"type":"VEC3",
                "min":bboxmin,"max":bboxmax}]
    primitives=[]
    for i,(name,ids) in enumerate(groups.items()):
        accessors.append({"bufferView":i+1,"componentType":5125,
                          "count":len(ids),"type":"SCALAR"})
        if ids:
            primitives.append({"attributes":{"POSITION":0},"indices":i+1,
                               "material":i,"mode":4})
    mats=[{"name":m,"doubleSided":True,
           "pbrMetallicRoughness":{"baseColorFactor":rgb,
                                    "metallicFactor":.14,"roughnessFactor":.64}}
          for m,(_,rgb) in COLORS.items()]
    gltf={"asset":{"version":"2.0","generator":"G4C7 A19 archived-OBJ replay"},
          "scene":0,"scenes":[{"nodes":[0]}],
          "nodes":[{"mesh":0,"name":"G4C7_A19_SCOUT_ART_HOLD"}],
          "meshes":[{"primitives":primitives}],"materials":mats,
          "buffers":[{"byteLength":offset}],"bufferViews":views,
          "accessors":accessors}
    js=pad(json.dumps(gltf,separators=(",",":")).encode("ascii"),b" ")
    bi=pad(b"".join(chunks),b"\0")
    length=12+8+len(js)+8+len(bi)
    glb=(struct.pack("<III",0x46546c67,2,length)
         +struct.pack("<II",len(js),0x4E4F534A)+js
         +struct.pack("<II",len(bi),0x004E4942)+bi)
    path.write_bytes(glb)
    data_back=path.read_bytes()
    assert struct.unpack_from("<III",data_back,0)==(0x46546c67,2,len(data_back))
    assert struct.unpack_from("<II",data_back,12)==(len(js),0x4E4F534A)
    assert struct.unpack_from("<II",data_back,20+len(js))==(len(bi),0x004E4942)

def shaded(hexstr,normal):
    light=max(.52,min(1.18,.78+.30*dot(normal,normalized((-.4,.86,-.3)))))
    rgb=[int(hexstr[i:i+2],16) for i in (1,3,5)]
    return "#"+"".join(format(max(0,min(255,round(v*light))),"02x") for v in rgb)

def render_three(models,cam_name,path):
    width,height,pane=1590,475,525
    eye=CAMERAS[cam_name]
    fw=normalized(sub(TARGET,eye))
    rt=normalized(cross((0.,1.,0.),fw))
    up=normalized(cross(fw,rt))
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
         f'<rect width="{width}" height="{height}" fill="#0c1827"/>','<defs>']
    for i in range(3):
        out.append(f'<clipPath id="pane{i}"><rect x="{i*pane+5}" y="46" width="{pane-10}" height="391"/></clipPath>')
    out.append("</defs>")
    for i,mark in enumerate(NAMES):
        m=models[mark]; cx=i*pane+pane/2; cy=245
        out.append(f'<rect x="{i*pane+5}" y="46" width="{pane-10}" height="391" rx="7" fill="#182a3a" stroke="#384c5f"/>')
        out.append(f'<g clip-path="url(#pane{i})">')
        for g in range(18):
            y=90+g*24
            out.append(f'<path d="M{i*pane+5} {y} H{(i+1)*pane-5}" stroke="#2a3c50" stroke-width=".6"/>')
        tris=[]
        for a,b,c,material in m["faces"]:
            pts=[m["verts"][id] for id in (a,b,c)]
            center=tuple(sum(p[j] for p in pts)/3 for j in range(3))
            n=normalized(cross(sub(pts[1],pts[0]),sub(pts[2],pts[0])))
            if dot(n,sub(eye,center))<=0: continue
            coords=[]
            for p in pts:
                d=sub(p,TARGET)
                coords.append(f'{cx+dot(d,rt)*SCALE:.2f},{cy-dot(d,up)*SCALE:.2f}')
            depth=dot(sub(center,eye),fw)
            tris.append((depth," ".join(coords),shaded(COLORS[material][0],n)))
        tris.sort(reverse=True,key=lambda t:t[0])
        out.extend(f'<polygon points="{pts}" fill="{col}" stroke="#253545" stroke-width=".29" stroke-linejoin="round"/>'
                   for _,pts,col in tris)
        out.append('</g>')
        out.append(f'<rect x="{i*pane+5}" y="46" width="{pane-10}" height="391" rx="7" fill="none" stroke="#435a70"/>')
        out.append(f'<text x="{i*pane+18}" y="31" fill="#e8f0f4" font-size="18" font-family="sans-serif" font-weight="bold">{mark.upper()} — {escape(TITLES[mark])}</text>')
        out.append(f'<text x="{i*pane+18}" y="458" fill="#a4b9c7" font-size="13" font-family="sans-serif">{len(m["faces"])} triangles | ART HOLD; engineering unverified</text>')
    out.append(f'<text x="1572" y="24" text-anchor="end" fill="#a2bac9" font-size="12" font-family="sans-serif">A19 / {cam_name.upper()} / SAME CAMERA + SCALE / Y-UP CONCEPT</text>')
    out.append('</svg>')
    path.write_text("".join(out),encoding="utf-8")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--source",type=Path,default=Path("artifacts/g4c7-a19-scout"))
    ap.add_argument("--out",type=Path,default=Path("build/g4c7_a19_replay"))
    args=ap.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/"fourview").mkdir(exist_ok=True)
    models={}
    for mark,suffix in NAMES.items():
        models[mark]=read_obj(args.source/f"a19_{mark}_{suffix}.obj")
        export_glb(models[mark],args.out/f"a19_{mark}_{suffix}_replay.glb")
    for camera in CAMERAS:
        render_three(models,camera,args.out/"fourview"/(camera+"_three_way_matched.svg"))
    summary={"ART":"HOLD","Minecraft":"PROHIBITED","city_integration":"PROHIBITED",
             "route_331_993":"NOT RUN ON SCOUT",
             "candidate_geometry_counts":{k:{"vertices":len(m["verts"]),
                     "triangles":len(m["faces"])} for k,m in models.items()}}
    (args.out/"replay_manifest.json").write_text(
        json.dumps(summary,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,indent=2))

if __name__=="__main__":
    main()
