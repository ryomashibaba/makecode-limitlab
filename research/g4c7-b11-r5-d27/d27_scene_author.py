"""D27 scene-first, fully reproducible 2D author study, NOT a 3D city."""
from pathlib import Path
from html import escape
import json, math, argparse

SCENES=[
 ("arrival","地上入口","街の生活を感じながら公共文化空間へ入る"),
 ("making","制作実演","設備と手仕事が通行人から見える"),
 ("exchange","文化交流","制作と研究の両方が同じ視野に入る"),
 ("research","公開研究","歩いて研究現場の入口へ達する"),
 ("upper","上層生活","住居と文化街路がつながるべき着地点"),
]
PROTECTION={"art":"ART HOLD","adopted":0,"formal_G0":"NOT_RUN",
            "formal_S1_G1_G2_G3":"NOT_RUN","true_3d":"NOT_RUN",
            "upper_level_continuous_path":"NOT_MODELED",
            "minecraft_construction":"FORBIDDEN",
            "city_integration":"FORBIDDEN","main":"UNTOUCHED","PR53":"DRAFT_OPEN"}
CANDIDATES=[
 {"id":"A","name":"ほどける文化の継ぎ目","principle":"a single pedestrian sequence interleaves maker, learning, research and dwelling through connected inhabited thresholds",
 "view_eye":[0,-34],"maker_target":[-30,-6],"research_target":[29,-1],
 "route":[[0,-82],[-5,-65],[-17,-42],[-30,-16],[-14,-12],[0,-4],[15,-1],[29,12],[13,30]],
 "enclosure":[[[-70,-38],[-61,37]],[[-61,37],[-31,58]],[[31,59],[67,35]],[[67,35],[70,-38]]],
 "program":[{"id":"maker_workshop","role":"maker","center":[-34,-2],"outline":[[-65,-37],[-25,-34],[-17,9],[-45,31],[-67,17]]},
            {"id":"public_research","role":"research","center":[33,15],"outline":[[24,-28],[65,-28],[69,25],[43,43],[20,29]]},
            {"id":"shared_exchange","role":"shared","center":[0,-5],"outline":[[-18,-20],[15,-19],[19,27],[-17,29]]},
            {"id":"residential_threshold","role":"housing","center":[6,55],"outline":[[-26,42],[25,39],[34,74],[-25,78]]}],
 "section_profile":[[0,384],[65,385],[112,350],[154,316],[205,333],[245,290],[278,315],[314,300],[350,357],[395,325],[443,367],[485,384],[520,384]],
 "sky_void":"open court between maker and research thresholds (NOT a measured sky view)",
 "vertical_cores":[[-46,38],[49,37]],
 "art_note":"The section remains an illustrative skyline; risk of two cliff-banks and disconnected upper residences. No pre-3D approval."},
 {"id":"B","name":"旋回する研究の舞台","principle":"program rooms alternate around a single excavated public rotor",
 "view_eye":[0,-60],"maker_target":[-27,23],"research_target":[27,23],
 "route":[[0,-85],[-6,-65],[-16,-38],[-27,-10],[-15,7],[4,21],[27,25],[30,43]],
 "enclosure":[[[-62,1],[64,1]],[[-61,1],[-40,54]],[[64,1],[43,54]]],
 "program":[{"id":"maker_wedge","role":"maker","center":[-31,24],"outline":[[-63,5],[-17,6],[-13,44],[-52,64]]},
            {"id":"research_wedge","role":"research","center":[30,24],"outline":[[13,5],[63,4],[53,64],[12,47]]},
            {"id":"public_rotor","role":"shared","center":[0,4],"outline":[[-15,-26],[18,-26],[35,10],[0,36],[-33,11]]},
            {"id":"upper_lodging","role":"housing","center":[4,56],"outline":[[-21,42],[30,42],[30,74],[-17,74]]}],
 "section_profile":[[0,384],[75,371],[116,283],[163,228],[226,198],[286,228],[349,287],[395,369],[520,384]],
 "sky_void":"circular opening indicated but overhead weather protection not designed",
 "vertical_cores":[[-42,42],[43,42]],
 "art_note":"Rotunda is a megastructure primitive; front ring blocks maker/research from public eye. Reject before true 3D."},
]
def point(p,ox=90,oy=246,s=2.15):
    return (ox+((p[0]+90)*s),oy+((95-p[1])*s))
def path_poly(points, ox=90, oy=246, scale=2.15):
    ps=[point(p,ox,oy,scale) for p in points]
    return " ".join(f"{x:.1f},{y:.1f}" for x,y in ps)
def text(x,y,v,size=20,color="#1d3644",weight=500):
    return f'<text x="{x}" y="{y}" fill="{color}" font-family="Noto Sans CJK JP, Noto Sans JP, sans-serif" font-size="{size}" font-weight="{weight}">{escape(str(v))}</text>'
def render_svg(c):
    L=['<svg xmlns="http://www.w3.org/2000/svg" width="1560" height="960" viewBox="0 0 1560 960">',
       '<rect width="1560" height="960" fill="#f6f4eb"/>',
       '<rect width="1560" height="165" fill="#163b4d"/>',
       text(45,62,"G4-C7 / B11-R5 D27 — SCENE-FIRST AUTHOR STUDY",23,"#c9dce5",650),
       text(45,119,f'{c["id"]}｜{c["name"]}',42,"#fff2d6",720),
       '<rect x="38" y="192" width="720" height="521" rx="18" fill="#e3eee8" stroke="#b1c6c0" stroke-width="2"/>',
       '<rect x="780" y="192" width="742" height="521" rx="18" fill="#eaf0ee" stroke="#b1c6c0" stroke-width="2"/>',
       text(63,225,"GROUND EXPERIENCE / 2D PROGRAM ONLY",19,"#42616c",700),
       text(805,225,"AUTHORIAL SILHOUETTE / NOT 3D",19,"#42616c",700)]
    colors={'maker':'#d79f66','research':'#68a2aa','housing':'#849c85','shared':'#e6dcb7'}
    for p in c["program"]:
        pts=path_poly(p["outline"])
        L.append(f'<polygon points="{pts}" fill="{colors[p["role"]]}" fill-opacity=".65" stroke="#42616c" stroke-width="2"/>')
        x,y=point(p["center"])
        L.append(text(f"{x-35:.1f}",f"{y:.1f}",p["role"].upper(),16,"#1a3545",700))
    for a,b in c["enclosure"]:
        x,y=point(a);X,Y=point(b)
        L.append(f'<line x1="{x}" y1="{y}" x2="{X}" y2="{Y}" stroke="#314f60" stroke-width="10" stroke-linecap="round"/>')
    L.append(f'<polyline points="{path_poly(c["route"])}" fill="none" stroke="#ca6c52" stroke-width="5" stroke-linecap="round" stroke-dasharray="13 8"/>')
    ex,ey=point(c["view_eye"])
    for target,key in [(c["maker_target"],"maker"),(c["research_target"],"research")]:
        tx,ty=point(target); L.append(f'<line x1="{ex:.1f}" y1="{ey:.1f}" x2="{tx:.1f}" y2="{ty:.1f}" stroke="#fff" stroke-width="3" stroke-dasharray="7 6"/>')
    L.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="11" fill="#253f50" stroke="white" stroke-width="3"/>')
    for i,co in enumerate(c["route"]):
        x,y=point(co); L.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="#9c4137"/>')
    L.append(text(65,685,"視線と経路は平面概念線。人体・通行・視認の認証ではない。",16,"#556c72"))
    # skyline: hand-authored vector geometry, identical source record as the plan
    q=" ".join(f"{800+x*1.30:.1f},{y+107:.1f}" for x,y in c["section_profile"])
    L.append(f'<polygon points="{q} 1476,690 800,690" fill="#658b90" stroke="#315a68" stroke-width="3"/>')
    for i in range(10):
        x=860+(i%5)*130;y=505+(i//5)*70
        L.append(f'<rect x="{x}" y="{y}" width="65" height="17" rx="2" fill="#a8c7c2" opacity=".8"/>')
    L.append('<path d="M 1050 675 Q 1135 588 1200 635 Q 1255 576 1360 672" fill="none" stroke="#e5b16c" stroke-width="10" stroke-linecap="round"/>')
    L.append('<circle cx="1165" cy="410" r="45" fill="#f1d79a" opacity=".65"/>')
    L.append(text(810,686,"概念シルエットは実メッシュではなく作者の仮説",17,"#546b73"))
    L.append('<rect x="38" y="738" width="1484" height="184" rx="18" fill="#e4e9e2"/>')
    L.append(text(56,773,"FIVE EXPERIENCE SCENES  /  同じ歩行者による連続体験",20,"#244755",700))
    for i,(name,ja,desc) in enumerate(SCENES):
        x=60+i*290
        L.append(f'<circle cx="{x+18}" cy="813" r="15" fill="#b5714a"/>')
        L.append(text(x+12,820,str(i+1),17,"white",700))
        L.append(text(x,855,ja,19,"#1f3d4a",690))
        L.append(text(x,879,desc[:17],15,"#536d74"))
        if i<4:L.append(f'<path d="M {x+220} 816 l 35 0 m -9 -7 l 9 7 -9 7" fill="none" stroke="#b18764" stroke-width="2"/>')
    L.append(text(54,941,"ART HOLD / NO ART ADOPTION / NO TRUE 3D / NO FORMAL G0-S1-G1-G2-G3 / NO MINECRAFT",17,"#9c5b40",650))
    L.append("</svg>")
    return "\n".join(L)+"\n"

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--out",default="d27_build");o=Path(ap.parse_args().out);o.mkdir(parents=True,exist_ok=True)
    data={"stage":"B11-R5 D27","study":"SCENE_FIRST_AUTHOR_2D_ONLY",
      "scenes":[{"id":i,"name":n,"human_experience":t} for i,n,t in SCENES],
      "candidates":CANDIDATES,"protection":PROTECTION,
      "evidence_limits":["2D segment visibility only","illustrative skyline is not a mesh","open sky not measured in 3D",
      "no functioning lift/stairs","no continuous 3D body sweep","activity removal logic does not prove architectural necessity"]}
    (o/"d27_author_original.json").write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    for c in CANDIDATES:
        (o/f'd27_{c["id"].lower()}_plate.svg').write_text(render_svg(c),encoding="utf-8")
    # Complete author role sets for counterfactual evidence. For research only.
    cases={}
    for c in CANDIDATES:
        roles={p["id"]:p for p in c["program"]}
        cases[c["id"]]={
          "baseline":list(roles),
          "no_maker":[k for k,v in roles.items() if v["role"]!="maker"],
          "no_research":[k for k,v in roles.items() if v["role"]!="research"],
          "all_roles":{k:v["role"] for k,v in roles.items()}}
    (o/"d27_role_counterfactuals.json").write_text(json.dumps(cases,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("D27 source-derived AUTHOR SVG and counterfactual data created; true 3D NOT RUN; ART HOLD.")
if __name__=="__main__":main()
