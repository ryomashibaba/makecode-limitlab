# G4-C7 / D3S26-M03 — 保存.blend同一原本8視点一括監査キット

**記録日:** 2026-10-31 JST  
**正式結果:** TOOLING STATIC PASS / BLENDER RUNTIME NOT RUN / CITY ART HOLD / 正式採用0 / Minecraft Education施工禁止。

## M02から進めた部分
M01では入口・視線・階段の限定TECHが改善したが、都市は低層キャンパスへ戻りART REJECT。M02でBlenderの直接主形状編集用シーン生成スクリプトを静的に準備したが、実Blender実行はNOT RUN。M03は**M02の状態を過大評価せず、保存.blendの固定視点出力を一操作にまとめる制作・レビュー手段**の実装。新しい完成都市や正式なB案候補ではない。

会話ZIP `D3S26_M03_ONE_CLICK_BLENDER_REVIEW_KIT.zip` にM01参照GLB、M02制御シーン作成スクリプト、M03一括監査スクリプト、Windowsバッチ2本、空間契約、説明、検査記録を含む**11ファイル**。最終ZIP **25,334 bytes**、CRC PASS、SHA256 **af090bbf4f10d58f0f8a4e2c6069b5f4b81b75ba0b092f3da0252de18b92bc80**。ZIPは会話添付に存在し、GitHubへバイナリを保存済みと主張しない。

## M03の実装機能（ただしBlender実走は未確認）
- `M03_RUN_AND_OPEN.bat`: Windows Blender 5.xを探し、M02の保存シーンがなければ新規生成。保存.blendを背景で読み、8固定カメラのPNGを撮影してからエディタを開く。M02のソースと旧成果を上書きしない。
- `M03_REVIEW_SAVED_SCENE.bat`: メッシュを編集して.blend保存後、同じ固定カメラで再撮影。
- `M03_capture_review.py`: 入力が専用のM02_OUTPUT_NEW_ONLY内の正規 .blend であること、PROJECT/NO-WRITE/QA NOT_RUNマーカー、参照GLBのSHA256、カメラ8台/編集メッシュ3点を確認。不一致なら停止する。
- 保存.blendのSHA256を開始/終了時に比較し、撮影中に原本が更新された場合は同一原本証拠として認めない。
- 南北遠景、斜視、地区、街路眼高、製造者眼高、研究者眼高、住民眼高の**8視点をその.blend自身から**描画する。BlenderのCYCLES 10 samples / 960×540で実行する設定。
- 編集用3制御メッシュ**のみ**をGLBにエクスポートし、Blenderで再インポートして頂点/ポリゴン数が存在することを確認。これは都市全域3Dでも実室でも施工可能モデルでもない。
- カメラ行列、入力.blend SHA256、再読込集計、PNG8点、未完成GLB、README、manifestを別名のM03_OUTPUT_NEW_ONLYに記録し、CRC検査付きZIPとしてまとめる。
- .blendは読込みのみであり、scriptにsave_as_mainfile/open_mainfile呼び出しはない。Minecraft Educationには一切接続・書込みしない。

## 実際にこのChat環境で検証したこと
- M02/M03両PythonスクリプトのAST構文PASS。
- M01参照GLB SHA256 `f15e5e7d845e00a774a0f43db22dec6f8ed59e7cdcdab1b42b9b321bf8f79c5a`一致。trimeshで原本106 geometryを確認。
- M03の安全マーカー、入力.blendディレクトリ制限、原本ハッシュ再確認、8カメラ定義、未完成形状専用GLB書出設定、source save禁止、正式QA NOT_RUN、Minecraft書込み0を静的検査。
- ZIP 11ファイル、CRC PASS、サイズとSHA確認。
- **Blender本体不在。実行、.blend作成、Blender画像8点の実生成・確認、GLBの実再読込はすべてNOT RUN。** これらをPASSとして報告しない。

## 制作方針
次段階はBlenderで**実際に直接主形状を編集した**同一シーンを南北/人間眼高から批判的に確認する。M01系の箱を増やして作品化せず、巨大都市の奥行・居住可能な厚み・用途と外形の因果関係を満たさなければ美術採用しない。美術的に有望な候補のみ実室・実開口・上下移動・正規331人体/993足元等へ進む。

全体ART HOLD、正式採用0。正式G0/S1/G1/G2/G3 NOT RUN、MakeCode実機施工なし。PR #53 Draft/Openを維持、mainを変更しない、過去原本を上書きしない。
