# G4-C7 D3S26 M36 — 編集可能な二重Blender制作環境・実メッシュによる美術失敗原因監査



**2026-11-01 JST／全体ART HOLD／正式美術採用0件／Minecraft Education施工・既存都市統合禁止／main未変更／Draft PR #53 Open。**



## 意思決定：同じ形状生成ループを停止

M30〜M35では、各回の技術確認が進歩しても、押出し箱、板、巨大壁、低層キャンパス、離れた公共施設に戻り、巨大な一体未来都市の美術は不採用だった。**M36ではこれらの低品質形状の増築も新たな低品質都市候補の自動生成も行わない**。代わりに編集可能な本物のBlender原本・参照保全・人間体験/都市遠景の同時制作基盤を構築。



## 独立実メッシュによるM35の根本原因分析

M35の固定された真正GLB（SHA256 45c7bd89e0047dffaedd7ee121e9cfb1d540e58a8b3dc9ec99e22db5f56a77ca）を、元Blender作者をimportしないローカルTrimeshコードで再読込し、glTF Y-up→Blender Z-up変換した。実ジオメトリノード208件。

製造屋根、研究屋根、住宅屋根、文化屋根、上階橋の庇という**主要5件すべてがwatertightではない開放面メッシュ**。合計38三角面。実体積を囲う本物の居住建築外皮を形成しない。5個の屋根投影バウンディング面積合計53,230研究単位²は外接矩形の重複込みであり、実床面積・居住面積ではない。

元公共街路5地点・入口4件の内外計8地点・上階3地点という**合計16の限定実支持位置**を確認。居住・研究の階段各72部材、最後の踏面高さ18.0。文化視点が実段床の内部にある既知問題を再確認。存在しない公共床・偽高度500の負対照2件を検出。これらは公式331/993 QAや全人体通行安全のPASSではない。

真正GLBの上面投影図は**四隅の離れた屋根面と十字形街路**をそのまま示し、都市の市街地密度・人間の実居住を含む外形連成が不足していることを形状から裏付ける。独立検査Python/JSON/PNG/READMEとSHAは会話ZIP M36_SAVED_GLB_INDEPENDENT_FAILURE_AUDIT.zip（ZIP SHA256 82d41af2ccec4641df5f9974af224e46a2209c20e10e0924b255e238a2f51d14）に収録。**この解析ZIPはGitHubへアップロードしていない**。



## 実Blenderネイティブ制作基盤（技術方法PASS）

[M36作者Python](https://github.com/ryomashibaba/makecode-limitlab/blob/dev/g4c7-a17-monolithic-rift-fold-art-study/tools/g4c7_m36_dual_scene_artist_studio.py) は、M35検証済BLEND SHA256 2cb51ded85bb5f541fd56058f14e639098e6592e7082e41c417083a16d55dce4 をピンで照合して読み込む。既存M35参照シーンを独立保持し、**編集用に全208メッシュを208件の別データブロックへ複製**。別Blenderシーンを作成し、8個の実生活/美術目的マーカー、9固定カメラ、手編集可能だが歩行床ではないガイド曲線を配置。

参照用シーン名 M35_REJECTED_REFERENCE_LOCKED、編集用シーン名 M36_AUTHORING_STUDIO_ART_HOLD。制作環境の孤立性確認のため**編集用の屋根メッシュ1頂点だけZ+0.005研究単位変更**し、参照原本は不変と確認。これは美術向上ではない。元M35をART PASSや都市原本として採用したわけでもない。

[M36専用Actions #41288889170](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41288889170) は**全工程SUCCESS**。M35 .blendをピンのSHA256で検証、ネイティブBlender 4.5.15実行、M36の本物の .blend 作成、別Pythonプロセスで再オープン。参照原本と編集用の全メッシュの頂点/面/ローカル変換・親子関係を、元のM35 .blendの独立再オープンと比較。微小浮動小数点表現差1e-5以内、参照メッシュ破壊なし。コレクション、8目標、9カメラ、完全に独立したメッシュdatablock、0.005微小編集を確認した。旧ワールドに触れていない。

最初の2回のCIは、Blenderの評価済みワールド行列や浮動小数点ビット完全SHAを保存前後の形状破損と誤認する過剰な判定でFAIL。後続では元ネイティブBLENDと全頂点/面/ローカル変換/親子関係を厳密に独立比較して、誤検出を解消。正式QA基準は一切変更なし。



## 恒久保存した真正原本

[M36編集可能ネイティブ制作ファイル・manifest・README](https://github.com/ryomashibaba/makecode-limitlab/tree/dev/g4c7-a17-monolithic-rift-fold-art-study/artifacts/g4c7-m36-verified-native-author-studio)をDraft研究ブランチ上へ**append-only**保存済み。BLENDサイズ3,083,500 bytes、SHA256 be8d6eb0c37f58de4d677c12c4382f4f254ce51fe36e022946d4d9315301dc06。成果はBLEND原本・manifest・日本語READMEの3ファイル。旧M35の本物のモデル・原本SHAは維持。CIは [M36 workflow](https://github.com/ryomashibaba/makecode-limitlab/blob/dev/g4c7-a17-monolithic-rift-fold-art-study/.github/workflows/g4c7-m36-artist-studio-native.yml)。



## 美術・安全の最終判定

**M36制作方法 TECH PASS、M36都市形状 ART NOT ATTEMPTED/ART HOLD、M35既存都市 ART REJECT、正式採用0件。** 新しい美しい都市を完成させたと主張しない。M36の8目標マーカーとガイド曲線は実構造物・検証済動線ではない。都市の色/彫刻だけでなく、正背面スカイライン、街路と立体連絡、多用途の室内実空間を同時に改変できる状態を実制作の出発点にする。

公式G0/S1/G1/G2/G3と331人体/993足元、身体半幅0.65・相対+0.15〜+3.25・歴史的干渉上限45・未支持0、連続歩行、安全な出口、MakeCodeへの実用可能な変換・施工、都市統合は**全てNOT RUN/禁止**。Chat主体、Work無断使用なし、外注なし、main変更/PRマージなし。