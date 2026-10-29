"""D47: independent descriptive 2D-render + saved 3D similarity gate for D46 A/B.
Not an automatic beauty classifier. It rejects claiming 'new architectural language' on nearly unchanged
human views / geometry. The 2% diagnostic threshold is exploratory, NOT a formal pre-registered benchmark.
"""
import argparse,hashlib,json
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
import trimesh
VIEWS=['01_overall','02_arrival','03_human_court','04_maker_eyes','05_research_eyes','06_upper_room']

def geom(path):
    s=trimesh.load(path,force='scene',process=False);m={}
    for n in s.graph.nodes_geometry:
        t,k=s.graph[n];q=s.geometry[k].copy();q.apply_transform(t);m[str(n)]=q
    return m

def main():
    arg=argparse.ArgumentParser();arg.add_argument('--out',default='d46_build');a=arg.parse_args();out=Path(a.out)
    aa=geom(out/'d46_a_baseline.glb');bb=geom(out/'d46_b_baseline.glb')
    common=set(aa)&set(bb)
    same=sum(1 for n in common if aa[n].vertices.shape==bb[n].vertices.shape and np.array_equal(aa[n].vertices,bb[n].vertices))
    comparisons={}
    for k in VIEWS:
        ap=out/'A'/(k+'.png');bp=out/'B'/(k+'.png')
        im0=np.asarray(Image.open(ap).convert('RGB'),dtype=np.int16)
        im1=np.asarray(Image.open(bp).convert('RGB'),dtype=np.int16)
        if im0.shape!=im1.shape:raise AssertionError(f'not same canvas {k}')
        diff=np.abs(im1-im0)
        changed=(diff.max(axis=2)>20)
        comparisons[k]={'pixel_changed_pct_over20RGB':round(float(changed.mean()*100),3),
                        'mean_absolute_RGB_difference':round(float(diff.mean()),3),
                        'A_sha256':hashlib.sha256(ap.read_bytes()).hexdigest(),
                        'B_sha256':hashlib.sha256(bp.read_bytes()).hexdigest()}
    unchanged=['01_overall','05_research_eyes','06_upper_room']
    exploratory=sum(comparisons[x]['pixel_changed_pct_over20RGB']<2 for x in unchanged)
    stop=(exploratory>=2 and same/len(bb)>.65)
    # Actual visual judgment is human reading of images; do not claim percent means artistic quality.
    assert stop,"D47 diagnostic definition changed: carefully inspect candidate and update authored review"
    result={'stage':'D47','scope':'REPRODUCED_GLb_VTK_VIEW_DIFFERENCE_DIAGNOSTIC_ONLY',
       'candidate_A_nodes':len(aa),'candidate_B_nodes':len(bb),'shared_nodes':len(common),
       'unchanged_shared_node_meshes':same,'unchanged_fraction_of_B':round(same/len(bb),4),
       'view_differences':comparisons,
       'method':{'threshold':'RGB max-channel absolute difference >20 on same-resolution images',
                 'diagnostic':'views with less than 2% changed pixels; threshold exploratory NOT formal art metric'},
       'underpowered_aesthetic_change_flag':stop,'human_artist_review':'REJECT_BOTH_A_AND_B',
       'release_or_adoption':False,'reason':'variant primarily adds isolated objects; no genuine new shared civic interior',
       'official_QA':'NOT_RUN','formal_art_G0':'NOT_RUN',
       'minecraft_construction':'FORBIDDEN','city_integration':'FORBIDDEN','adopted':0}
    (out/'d47_visual_difference_result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    # A focused crop comparison for the art reviewer: genuine renderer frames only.
    bw,bh=660,400
    montage=Image.new('RGB',(bw*2,(bh+45)*3),(245,246,244));d=ImageDraw.Draw(montage)
    for row,v in enumerate(('01_overall','03_human_court','06_upper_room')):
        for col,variant in enumerate(('A','B')):
            im=Image.open(out/variant/(v+'.png')).convert('RGB');im.thumbnail((bw-10,bh-10))
            montage.paste(im,(col*bw+5,row*(bh+45)+35))
            d.text((col*bw+10,row*(bh+45)+10),f'{variant} | {v} | changed {comparisons[v]["pixel_changed_pct_over20RGB"]}% (A-v-B)',fill=(34,48,45))
    montage.save(out/'D47_same_camera_visual_similarity.png')
    print(f'D47 VIEW GATE: STOP. {same}/{len(bb)} unchanged B meshes; upper view {comparisons["06_upper_room"]["pixel_changed_pct_over20RGB"]}% different; both ART REJECT')
if __name__=='__main__':main()
