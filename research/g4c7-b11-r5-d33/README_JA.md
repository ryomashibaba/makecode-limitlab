# D33 再生成原本

`d33_source_min.br.b64` は生成器・独立GLB監査を、Python ASTで改行整形してBrotli圧縮した2ファイルの可逆保存形式。GitHubに公開するのは研究用ソースのみ。モデルの美術・施工採用ではない。

復元手順（GitHub Actionsも同じ処理）：

```python
from pathlib import Path
import base64,brotli,hashlib
p=Path('research/g4c7-b11-r5-d33/d33_source_min.br.b64')
s=p.read_text().strip()
assert hashlib.sha256(s.encode()).hexdigest()=='86227abfe1210a0f9abc3db2d0332cad777e3252548b6d400c11b3ac3beefe34'
raw=brotli.decompress(base64.b64decode(s))
n=int.from_bytes(raw[:4],'big')
assert 0<n<len(raw)-4
Path('d33_inhabited_fault.py').write_bytes(raw[4:4+n])
Path('d33_independent_saved_glb_audit.py').write_bytes(raw[4+n:])
```

復元したAST整形コードで再生成したGLB3件とJSON2件のSHA256は、元の生成器と同一。原本は使用者にZIPでも提供する。安全検査ではなく局所3D研究。
