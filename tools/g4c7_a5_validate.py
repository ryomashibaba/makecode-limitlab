"""Independent artifact checks. No artistic or walking verdict inferred."""
import sys,json,struct,hashlib
from pathlib import Path
root=Path(sys.argv[1]).resolve(); facts=json.loads((root/'model_facts.json').read_text())
if '--verify-manifest' in sys.argv:
    for line in (root/'SHA256SUMS.txt').read_text().splitlines():
        expected,name=line.split('  ',1)
        assert hashlib.sha256((root/name).read_bytes()).hexdigest()==expected,('Artifact changed',name)
checks={}
for folder in ['before_city','before_district','after']:
    for view in ['front','oblique','side','aerial']:
        path=root/folder/(view+'.png'); data=path.read_bytes()
        assert data[:8]==b'\x89PNG\r\n\x1a\n'; size=struct.unpack('>II',data[16:24]); assert size==(2048,1536),(path,size)
        checks[str(path.relative_to(root))]={'resolution':size,'bytes':len(data)}
data=(root/'a5_orbital_commons.glb').read_bytes()
assert struct.unpack('<4sII',data[:12])==(b'glTF',2,len(data))
length,kind=struct.unpack('<II',data[12:20]); assert kind==0x4e4f534a
gltf=json.loads(data[20:20+length]); assert len(gltf['meshes'])==facts['mesh_objects']
for name in ['a4_restored.blend','a5_orbital_commons.blend']:
    assert (root/name).stat().st_size>10000
roundtrip=json.loads((root/'roundtrip_qa.json').read_text()); assert roundtrip['verdict']=='GEOMETRY_ROUNDTRIP_PASS_NOT_ART_OR_WALK_PASS'
assert facts['construction_status']=='PROHIBITED'
checks['glb']={'bytes':len(data),'meshes':len(gltf['meshes']),'version':2}
report={'verdict':'ARTIFACT_FORMAT_PASS_ART_HOLD','checks':checks,'art_verdict':'HOLD','walk_verdict':'UNTESTED','construction':'PROHIBITED'}
(root/'artifact_qa.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
files=[p for p in sorted(root.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.txt' and p.suffix!='.blend1']
assert all(p.stat().st_size<100*1024*1024 for p in files)
(root/'SHA256SUMS.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(root).as_posix()+'\n' for p in files),encoding='utf-8',newline='\n')
print(report['verdict'],len(files),'files',sum(p.stat().st_size for p in files),'bytes')
