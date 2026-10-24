"""Build an offline comparison page with an embedded, dependency-free OBJ viewer.
Usage: python tools/g4c7_a5_package.py ARTIFACT_DIRECTORY
"""
import sys,json,math,hashlib,struct
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

root=Path(sys.argv[1]).resolve()
views=['front','oblique','side','aerial']
colors={}; current=None
for line in (root/'a5_orbital_commons.mtl').read_text().splitlines():
    if line.startswith('newmtl '): current=line[7:]
    if line.startswith('Kd '): colors[current]=[float(x) for x in line[3:].split()]
verts=[]; triangles=[]; color=[.6,.7,.7]
for line in (root/'a5_orbital_commons.obj').read_text().splitlines():
    if line.startswith('v '): verts.append([float(x) for x in line[2:].split()])
    elif line.startswith('usemtl '): color=colors.get(line[7:],color)
    elif line.startswith('f '):
        ids=[int(t.split('/')[0])-1 for t in line[2:].split()]
        for i in range(1,len(ids)-1):
            p=[verts[j] for j in [ids[0],ids[i],ids[i+1]]]
            a=[p[1][j]-p[0][j] for j in range(3)]; b=[p[2][j]-p[0][j] for j in range(3)]
            n=[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
            length=math.sqrt(sum(v*v for v in n)) or 1; n=[v/length for v in n]
            for v in p: triangles.extend(round(x,4) for x in v+n+color)

try: font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',32)
except OSError: font=ImageFont.load_default()
for v in views:
    board=Image.new('RGB',(2048,830),'#14212a'); draw=ImageDraw.Draw(board)
    for i,(folder,label) in enumerate([('before_district','A4 / BEFORE'),('after','A5 / ART HOLD')]):
        im=Image.open(root/folder/(v+'.png')).convert('RGB'); im.thumbnail((1024,768))
        board.paste(im,(i*1024,62)); draw.text((i*1024+24,14),label+' / '+v.upper(),font=font,fill='white')
    board.save(root/('compare_'+v+'.jpg'),quality=94)

html='''<!doctype html><html lang="ja"><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>G4-C7 A5 | Orbital Commons | ART HOLD</title><style>
*{box-sizing:border-box}body{margin:0;background:#101b23;color:#e9eeee;font:16px system-ui;line-height:1.7}main{max-width:1300px;margin:auto;padding:28px}h1{font-size:36px;line-height:1.2}a{color:#84ded4}button{background:#28434d;color:white;border:1px solid #4d747e;padding:10px 18px;cursor:pointer;border-radius:6px}canvas{width:100%;height:620px;display:block;background:#8495a0;touch-action:none}img{width:100%;display:block}figure{margin:22px 0}figcaption{padding:10px;background:#24343d}.hold{color:#ffc77c}nav{display:flex;gap:10px;flex-wrap:wrap}.panel{padding:18px;background:#1c2e38;margin:20px 0}details{margin:15px 0}small{color:#a9bdc6}</style><main>
<small>MAKECODE LIMITLAB / G4-C7 A5 / OFFLINE DESIGN RESEARCH</small><h1>Orbital Commons<br>文化地区を、一つの巨大立体空間へ。</h1>
<p class="hold">自己審査：ART HOLD。Minecraft施工禁止。都市全体の合格・歩行検証・構造強度の証明ではありません。</p>
<p>A4の5棟＋公共核を、2本の中空アーチ・偏心した直交ヴォールト・上空2層空間・楕円回廊・段丘広場へ再編。既存22棟のモデルは別ファイルに保全しています。</p>
<nav><a href="a5_orbital_commons.blend">BLEND</a><a href="a5_orbital_commons.glb">GLB</a><a href="a5_orbital_commons.obj">OBJ</a><a href="a5_orbital_commons.mtl">MTL</a><a href="a4_restored.blend">復元A4 BLEND</a><a href="REPORT_JA.md">審査・引継ぎ全文</a></nav>
<div class="panel"><strong>実3Dを回して確認</strong><p>ドラッグで回転、ホイールで拡大縮小。形状は配布OBJから読み取ってページに内蔵。通信・外部ライブラリ不要。</p>
<nav><button data-yaw="0" data-pitch="0.12">正面</button><button data-yaw="0.70" data-pitch="0.48">斜視</button><button data-yaw="1.5708" data-pitch="0.12">側面</button><button data-yaw="0.7" data-pitch="1.32">俯瞰</button></nav></div><canvas id="viewer" aria-label="回転できるA5の3Dモデル"></canvas><p id="status"></p>
<h2>同じ撮影条件で比較</h2><p>左：A4文化地区／右：A5。各元画像は2048×1536。照明・カメラ・縮尺を共通化。</p>'''
for v,label in zip(views,['正面','斜視','側面','俯瞰']):
    html+=f'<figure><a href="compare_{v}.jpg"><img src="compare_{v}.jpg" alt="{label}の改善前後"></a><figcaption>{label} / <a href="before_district/{v}.png">A4原寸</a> / <a href="after/{v}.png">A5原寸</a></figcaption></figure>'
html+='''<h2>4方向の自己審査</h2><ul><li>正面 HOLD：大開口は明確。ただし直交ヴォールトの端面が左側の開口を隠す。</li><li>斜視 改善：地区全体を跨ぐ厚い構造と広場の関係が読める。上空接合部に重なりが残る。</li><li>側面 HOLD：直交アーチで改善したが、手前の主アーチ端面が2枚の大壁として見える。</li><li>俯瞰 HOLD：楕円回廊と公共軸は明確。上部はまだH字の箱的な梁に読める。</li></ul>
<p>回廊と外殻の貫通開口、上階への連続経路、水平な室内床、道路との段差処理は未設計です。A4の到達PASSはA5へ移植していません。旧G4-C6の施工ログPASSと都市景観REJECTも独立に保持します。</p>
<script>
const raw=__GEOMETRY__;
const c=document.getElementById('viewer'),gl=c.getContext('webgl');
if(!gl){document.getElementById('status').textContent='WebGL未対応。BLEND/GLB/OBJまたは画像で確認してください。'}else{
const vs=`attribute vec3 p;attribute vec3 n;attribute vec3 col;uniform vec3 eye;uniform vec3 right;uniform vec3 up;uniform vec3 forward;uniform float aspect;varying vec3 color;varying vec3 norm;void main(){vec3 q=p-vec3(0.,24.,0.)-eye;float d=dot(q,forward);gl_Position=vec4(dot(q,right)*1.8/aspect,dot(q,up)*1.8,1.001*d-0.2,d);color=col;norm=n;}`;
const fs=`precision mediump float;varying vec3 color;varying vec3 norm;void main(){float light=.45+.55*abs(dot(normalize(norm),normalize(vec3(-.4,.8,.5))));gl_FragColor=vec4(pow(color,vec3(.7))*light,1.);}`;
function shader(type,src){let s=gl.createShader(type);gl.shaderSource(s,src);gl.compileShader(s);if(!gl.getShaderParameter(s,gl.COMPILE_STATUS))throw Error(gl.getShaderInfoLog(s));return s}
let prog=gl.createProgram();gl.attachShader(prog,shader(gl.VERTEX_SHADER,vs));gl.attachShader(prog,shader(gl.FRAGMENT_SHADER,fs));gl.linkProgram(prog);if(!gl.getProgramParameter(prog,gl.LINK_STATUS))throw Error(gl.getProgramInfoLog(prog));gl.useProgram(prog);
let buffer=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,buffer);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array(raw),gl.STATIC_DRAW);
['p','n','col'].forEach((name,i)=>{let a=gl.getAttribLocation(prog,name);gl.enableVertexAttribArray(a);gl.vertexAttribPointer(a,3,gl.FLOAT,false,36,i*12)});
let yaw=.7,pitch=.48,distance=265,drag=null;
function norm(a){let l=Math.hypot(...a);return a.map(v=>v/l)}function cross(a,b){return[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]}
function render(){let dpr=Math.min(devicePixelRatio,2);c.width=c.clientWidth*dpr;c.height=c.clientHeight*dpr;gl.viewport(0,0,c.width,c.height);gl.enable(gl.DEPTH_TEST);gl.clearColor(.50,.58,.63,1);gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);let eye=[distance*Math.sin(yaw)*Math.cos(pitch),distance*Math.sin(pitch),distance*Math.cos(yaw)*Math.cos(pitch)],forward=norm(eye.map(v=>-v)),right=norm(cross(forward,[0,1,0])),up=cross(right,forward);for(let [name,v] of Object.entries({eye,right,up,forward}))gl.uniform3fv(gl.getUniformLocation(prog,name),v);gl.uniform1f(gl.getUniformLocation(prog,'aspect'),c.width/c.height);gl.drawArrays(gl.TRIANGLES,0,raw.length/9)}
c.onpointerdown=e=>{drag=[e.clientX,e.clientY];c.setPointerCapture(e.pointerId)};c.onpointermove=e=>{if(!drag)return;yaw-=(e.clientX-drag[0])*.008;pitch=Math.max(-.1,Math.min(1.5,pitch+(e.clientY-drag[1])*.008));drag=[e.clientX,e.clientY];render()};c.onpointerup=()=>drag=null;c.onwheel=e=>{e.preventDefault();distance=Math.max(110,Math.min(600,distance*Math.exp(e.deltaY*.001)));render()};document.querySelectorAll('button').forEach(b=>b.onclick=()=>{yaw=+b.dataset.yaw;pitch=+b.dataset.pitch;render()});window.onresize=render;render();document.getElementById('status').textContent=(raw.length/27).toLocaleString()+' triangles / 実OBJ形状 / 材質は概念色';
}
</script></main></html>'''
(root/'index.html').write_text(html.replace('__GEOMETRY__',json.dumps(triangles,separators=(',',':'))),encoding='utf-8')
print('Packaged comparison board and embedded viewer',len(triangles)//27,'triangles')
