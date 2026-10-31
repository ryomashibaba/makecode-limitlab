"""D3S20 research ONLY: section-coupled city blockout. NOT a safe city, not MakeCode code.
Public section is the input; frontages/usable-floor candidates derive from its edges.
No Minecraft operations. All coordinates are exploratory conceptual units (X east,Y north,Z up).
"""
from __future__ import annotations
import json, math, sys
from pathlib import Path
import numpy as np
import trimesh

ROOT=Path(__file__).resolve().parent
STATIONS_Y=np.array([-238.,-156.,-72.,5.,86.,165.,243.])
CENTER_X=np.array([-13.,23.,5.,-29.,2.,29.,4.])
LEFT_W=np.array([42.,45.,51.,58.,47.,42.,51.])
RIGHT_W=np.array([35.,43.,43.,52.,63.,53.,42.])
WEST_TOP=np.array([92.,185.,124.,255.,190.,176.])
EAST_TOP=np.array([160.,105.,222.,152.,273.,207.])

# Sequence is the design input, not copied boxes. Variants change public space geometry,
# neighborhood interface, and a skyline structural edge in the same derivation.
def author(civic_shift=0., void_width_factor=1.0, out=None):
    cy=CENTER_X.copy();cy[2:5]+=civic_shift*np.array([0.5,1.0,0.45]);
    lw=LEFT_W*void_width_factor; rw=RIGHT_W*void_width_factor
    scene=trimesh.Scene()
    stats={"roles":{},"programs":{},"stations":[],"entry_points":[],"public_axes":[],"named_meshes":{}}
    mats={"basalt":[51,69,87,255],"white":[196,207,210,255],"terrace":[113,145,147,255],"glass":[63,178,208,255],"amber":[224,168,94,255],"copper":[161,98,74,255],"park":[62,147,111,255],"path":[149,175,180,255],"deep":[34,50,69,255],"spine":[80,118,146,255]}
    def add(name,mesh,role,material,program):
        mesh.visual.face_colors=np.array(mats[material],dtype=np.uint8)
        scene.add_geometry(mesh,geom_name=name,node_name=name)
        stats['roles'][role]=stats['roles'].get(role,0)+1
        stats['programs'][program]=stats['programs'].get(program,0)+1
        stats['named_meshes'][name]=role
    def box(name,loc,size,role,material,program):
        if min(size)<=0: raise ValueError((name,loc,size))
        m=trimesh.creation.box(extents=size);m.apply_translation(loc);add(name,m,role,material,program)
    def beam(name,a,b,width,height,role,material,program):
        a=np.array(a,float);b=np.array(b,float);d=b-a; l=np.linalg.norm(d)
        if l<1e-4:return
        m=trimesh.creation.box(extents=[width,l,height]);rot=trimesh.geometry.align_vectors([0,1,0],d/l);m.apply_transform(rot);m.apply_translation((a+b)/2)
        add(name,m,role,material,program)
    def loft(name,sections,role,material,program):
        # 2d rectangles per floor; connect four corners across level, with flat caps.
        vertices=[]
        for x,y,z,w,depth in sections:
            vertices += [[x-w/2,y-depth/2,z],[x+w/2,y-depth/2,z], [x+w/2,y+depth/2,z],[x-w/2,y+depth/2,z]]
        n=len(sections); faces=[]
        faces += [(0,2,1),(0,3,2)]
        for j in range(n-1):
            for k in range(4):
                a=4*j+k;b=4*j+(k+1)%4;c=4*(j+1)+k;d=4*(j+1)+(k+1)%4
                faces.extend([(a,b,d),(a,d,c)])
        k=4*(n-1);faces.extend([(k,k+1,k+2),(k,k+2,k+3)])
        m=trimesh.Trimesh(vertices=vertices,faces=faces,process=True)
        add(name,m,role,material,program)
    # A continuous, non straight public canyon. Readability and open-air volume are intentional.
    for i in range(len(STATIONS_Y)-1):
        y0,y1=STATIONS_Y[i:i+2];yy=(y0+y1)/2;length=(y1-y0)
        x0,x1=cy[i:i+2];left0,left1=x0-lw[i],x1-lw[i+1];right0,right1=x0+rw[i],x1+rw[i+1]
        xc=(x0+x1)/2
        # Central walkway is made from 3 ribbons, not a symbolic line; floor height 7-13.
        v0=8 + 2.3*math.sin(i*.85);v1=8+2.3*math.sin((i+1)*.85)
        for k,(offset,color) in enumerate([(-0.2,'white'),(0.,'path'),(.2,'white')]):
            a=(x0+offset*(lw[i]+rw[i])*.45,y0,v0)
            b=(x1+offset*(lw[i+1]+rw[i+1])*.45,y1,v1)
            beam(f'civic_spine_{i}_{k}',a,b,(lw[i]+rw[i])*(.16 if k!=1 else .34),2.4,'public_axis',color,'civic')
        stats['public_axes'].append([[float(x0),float(y0),float(v0)],[float(x1),float(y1),float(v1)]])
        stats['stations'].append(dict(i=i,y0=float(y0),y1=float(y1),left0=float(left0),left1=float(left1),right0=float(right0),right1=float(right1),xc=float(xc)))
        for side in (-1,1):
            side_label='west' if side<0 else 'east'
            prog=(['exchange','forge','academy','civic','park','culture'] if side<0 else ['market','habitat','culture','habitat','research','habitat'])[i]
            ztop=(WEST_TOP if side<0 else EAST_TOP)[i]
            # The inner edge is geometrically coupled to the public canyon's air-width.
            ed0=left0 if side<0 else right0; ed1=left1 if side<0 else right1
            depth=122 if side<0 else 115
            # body is not a solid building: open multi-level terraces, upright frames,
            # and a distinct, inhabited architectural facade with large voids.
            front0=ed0+side*7;front1=ed1+side*7
            back0=ed0+side*depth;back1=ed1+side*(depth+18*(i%2))
            nlevels=([3,6,4,7,5,6] if side<0 else [5,4,7,5,8,6])[i]
            zmin=9.; rise=(ztop-zmin)/nlevels
            for lev in range(nlevels+1):
                z=zmin+lev*rise
                fringe=(lev/nlevels)**1.2
                # Floor spans a LARGE fraction of the section, then a meaningful sky void.
                xfront=front0*(1-fringe)+front1*fringe
                xback=back0*(1-fringe)+back1*fringe
                width=abs(xback-xfront)
                xm=(xfront+xback)/2
                shape_z=z+ (2 if lev%3==0 else 0)
                # truss/terrace floor slabs, with actual separation (air) between floors.
                box(f'{side_label}_{i}_floor_{lev}',(xm,yy,shape_z),(width,length*.98,2.6),'usable_floor_candidate', 'terrace' if lev%3 else 'basalt',prog)
                # outer facade massing is tall, coherent, and visibly stratified, not floating.
                if lev<nlevels:
                    xouter=xback - side*3
                    for q,fy in enumerate([-.43,.43]):
                        y=yy+fy*length
                        beam(f'{side_label}_{i}_support_{lev}_{q}',(xouter,y,z+2.5),(xouter,y,z+rise-2.3),5.8,5.8,'structural_candidate','deep',prog)
                    # non-uniform facade screen openings. All glass is opaque color, not physically glazed.
                    if lev%2==0:
                        xgl=xback-side*2
                        beam(f'{side_label}_{i}_facade_{lev}',(xgl,yy-length*.41,z+rise*.51),(xgl,yy+length*.41,z+rise*.51),3.0,2.0,'facade_rib','glass',prog)
                # skywalks face the central void; there is no guarantee of full accessibility
                if lev in (1,nlevels//2,nlevels-1):
                    xwalk=xfront+side*10
                    beam(f'{side_label}_{i}_balcony_{lev}',(xwalk,yy-length*.43,z+2),(xwalk,yy+length*.43,z+2),11,2,'public_gallery_candidate','amber' if prog in ('market','exchange','culture') else 'glass',prog)
            # A contiguous row of nonuniform skyline slabs/fin towers, derived from section's heights.
            # Every upper marker must have below it a z-continuous vertical sequence of frame columns.
            if i in (1,3,4) or (side>0 and i==2):
                for f in range(3 if prog!='research' else 4):
                    yyf=y0+length*(f+1)/(4 if prog!='research' else 5)
                    xfront=(front0+front1)/2
                    depth_f=24+8*math.cos(f*2+i)
                    xpos=xfront+side*(26+f*19)
                    height=ztop+(f+1)*7-(i%3)*14
                    loft(f'{side_label}_{i}_vertical_{f}',[(xpos,yyf,zmin+1,depth_f,15),(xpos+side*5,yyf+3,height*.47,depth_f*.80,18),(xpos+side*4,yyf-2,height,depth_f*.53,10)],'vertical_mass_candidate','white' if f%2 else 'spine',prog)
            # Open void is deliberately large and dictated by useful floor/terrace modules.
            # The skyline's edge is NOT independent of the canyon cross-section.
            if i in (0,2,4) and side==1:
                beam(f'{side_label}_{i}_skyline_ridge',(back0,yy-length*.48,ztop),(back1,yy+length*.48,ztop-13),5,3.5,'facade_rib','glass',prog)
            stats['entry_points'].append(dict(side=side_label,program=prog,i=i,at=[float((front0+front1)/2),float(yy),float(zmin+2.5)],status='NOT_SWEPT'))
    # Crossings depend on both banks of the same space—not disconnected bridges joining nodes.
    for i,lev in [(1,0),(2,1),(3,2),(4,1)]:
        st=stats['stations'][i];y=(st['y0']+st['y1'])/2
        x0=(st['left0']+st['left1'])/2; x1=(st['right0']+st['right1'])/2
        z=[11.,49.,96.][lev]
        beam(f'cross_civic_{i}',(x0-13,y,z),(x1+13,y,z),17,3.6,'public_crossing_candidate','white','civic')
        for side_id,side_x in enumerate([x0-13,x1+13]):
            # framed gateways visualizing program destination at each end
            beam(f'cross_gateway_{i}_{side_id}',(side_x,y-9,z),(side_x,y-9,z+27),3,3,'structural_candidate','amber','civic')
            beam(f'cross_gateway_{i}_{side_id}b',(side_x,y+9,z),(side_x,y+9,z+27),3,3,'structural_candidate','amber','civic')
    # Landmark civic interior: x east-west and y north-south axis crossing, not a sealed monolith.
    # No independent mega roof is allowed; canopy is segmented with daylight gaps.
    cx,cz=float(np.interp(5,STATIONS_Y,cy)),10
    for k in range(5):
        xx=cx+(k-2)*32
        for yi in (-40,42):
            beam(f'civic_portico_{k}_{yi}',(xx,yi,cz+3),(xx+8,yi,cz+71-abs(k-2)*4),5,5,'public_pavilion_frame','white','civic')
        beam(f'civic_roof_louver_{k}',(xx,-40,cz+68-abs(k-2)*4),(xx+8,42,cz+68-abs(k-2)*4),6,3,'roof_louver','glass','civic')
    # Atrium void remains open, but there is no evidence of safe access to upper galleries.
    # A few true greenery fragments, all carried by a nearby building deck; not freestanding trees.
    for i in (0,2,4,5):
        st=stats['stations'][i];yy=(st['y0']+st['y1'])/2
        x=(st['left0']+st['left1'])/2-48
        box(f'green_planter_{i}',(x,yy,15),(26,22,2),'landscape_candidate','park','park')
    if out is None: out=ROOT/'CIVIC_CANYON_PILOT.glb'
    scene.export(out)
    stats['declared_stage']='PRE_ART_RESEARCH_ONLY';stats['saved_glb']=str(Path(out).name)
    stats['civic_shift']=civic_shift;stats['void_width_factor']=void_width_factor
    stats['critical_unverified']=['continuous_human_sweep','real_interior_room_connectivity','support','load_path','egress','staircases','Minecraft_makecode','331_993_formal_QA']
    return stats

if __name__=='__main__':
    root=ROOT
    p=root/'CIVIC_CANYON_PILOT.glb'
    base=author(out=p)
    (root/'AUTHOR_AUDIT.json').write_text(json.dumps(base,ensure_ascii=False,indent=2),encoding='utf-8')
    if '--counterfactual' in sys.argv:
        author(civic_shift=24.,out=root/'COUNTERFACTUAL_CIVIC_SHIFT.glb')
        author(void_width_factor=.80,out=root/'COUNTERFACTUAL_WIDTH_SHRINK.glb')
    print('saved',p,'named geometries',len(base['named_meshes']))