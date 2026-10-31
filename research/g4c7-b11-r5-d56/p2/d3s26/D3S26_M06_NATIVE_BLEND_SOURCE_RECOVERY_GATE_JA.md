# G4-C7 D3S26-M06 — ネイティブBlender原本収集の障害解消
**2026-10-31 JST / SOURCE COLLECTION TOOL PASS / ORIGINAL SOURCE NOT YET RETRIEVED / CITY ART HOLD**

## 作業の判断
M03のBlender実行・保存原本8固定視点撮影は実績があるが、提出ZIPには .blend 原本が入っておらず、M04-M05ではネイティブ編集ができなかった。D3S26 A01/M04-Bの両制作方向は美術不合格のため、**同じPython自動生成法で第三案を量産しない**。今回は編集可能原本を収集する一回操作の仕組みを制作・検証した。

## 作成・確認した実成果
- 会話添付 `D3S26_M06_NATIVE_BLEND_HANDOFF_KIT.zip`（**4,815 bytes**、ZIP SHA256 **`cb2a02c190011cbe537db53bce14abc80a4b9ded050184604a6166e113ec137a`**）。3ファイル、ZIP CRC PASS。
- `M06_原本を自動収集.bat` : Windows Python 3を検出し、クリックまたはドラッグ＆ドロップで収集器を起動。
- `M06_collect_native_blend.py`: M02原本 `D3S26_M02_EDITABLE_AUTHOR_SCENE_20261031_171058_851631.blend` を優先して探す。自動検索で見つからなければ原本のドラッグ＆ドロップに対応。M03の実行記録にある元原本のSHA256 `a3df137b20287b9a3bef0b7fc121ea46ed7e091c8cb6ed9d7452ffa281d9678b` に照合し、変更済みなら異なるSHAを原文で記録するだけで破壊しない。
- ローカルの `.blend` を読み取り専用でコピーした後に前後SHA256とファイル更新時刻を照合。不一致なら不安定なZIPを廃棄。ZIP内の `.blend` ハッシュを再計算してCRCを確認。
- ZIPには元 `.blend` / 監査JSON / READMEだけを含む。すでに提出済みのM03画像や他プロジェクトのファイルは含めない。大容量ファイルは上限安全対策により停止。
- Python AST/py_compile PASS、模擬Blenderヘッダ付きテスト原本を使った収集→ZIP→再読込→SHA照合の実行テストPASS。**実M02原本の収集は NOT RUN**。したがって実Blenderの再起動・編集・レンダリング・都市美術改善はこの工程では未実施。

## 次に必要な完了条件
1. Windows側でM06 BATを一回実行し、生成された `M06_NATIVE_BLEND_HANDOFF_*.zip` を会話へ添付する。
2. `.blend` の実バイト列を確認して、M03実8視点と同一保存シーンの各オブジェクト/構図を特定する。Blenderのネイティブ環境で**主形状と生活空間を直接編集**し、改訂原本を別名保存する。
3. 保存後は同一8視点から市民眼高、南北遠景、内外実空間を比較して美術審査する。実開口/全幅動線/階段/反事実/正式331/993 QAは未実行のままとし、画像やメッシュ数で代用しない。

## 保護
現時点の CITY ART HOLD / 正式採用0 / Minecraft Education施工・既存都市統合禁止。将来の施工はMakeCodeのみ。main変更なし、PR #53 Draft/Open継続、過去原本の上書きなし。GitHubには本テキスト記録のみ追加、BlenderやZIPの実データをGitHub保存済みと主張しない。
