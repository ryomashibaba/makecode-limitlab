# G4-C7 A53 — EDITABLE ART STUDIO / Blenderネイティブ制作方式へのG0移行

**2026-10-26 JST／基点 `d05a81e728a0172926e6da4d70a2c4acc69f3c00`。最終状態：G0制作パイプライン候補実装・データ検証完了／新S1実レンダ NOT RUN／G1/G2/G3 NOT RUN／全体ART HOLD。**

## 1. A52までの問題とA53で本当に変更した内容

A34〜A52の継続的な美術REJECTを重く見て、従来の `extrude()/ribbon()/box()` を加算する方式で「別の巨大都市のようなモデル」を量産する進め方を止める。A52実3Dは低層の床・斜材・巨大面が支配し、公共室から市場のプログラム可視面は0%、文化1.90%、閲覧2.32%でS1 ART REJECT。技術的なOBJ/GLB・PNG保存の成功は美術の改善を意味しなかった。

A53では**編集可能な元造形を第一成果物**とし、以下をGitHubへ実装した。

- `artifacts/g4c7-a53-editable-studio/scene_plan.json`：両側の都市建築を設計者が直接動かせる12断面ステーション、用途が定義された4室の占有領域、公共街路および上層遊歩道の制御点、9つの視点契約、材質・光、厳格安全境界。
- `tools/g4c7_a53_blender_scene.py`：Python標準ライブラリでシーン計画をpreflightする経路と、Blenderネイティブの編集可能な**メッシュ帯／Bezier曲線／材質／Cyclesカメラ／3光源**を作成する経路を分離。作成時には各オブジェクトを用途別のCollectionへ格納、Solidifyは破壊的メッシュ化せずモディファイアとして保持。
- `artifacts/g4c7-a53-editable-studio/g0_preflight.json`：シーン構成の独立検査結果（Chat側JS検査）、故意に破壊した負の対照5件の結果を保存。

**今回はBlenderを実行していない。** 現環境で `blender` 実行ファイルと `bpy` を確認できなかったため、.blend、CyclesのPNG、材質・照明の実レンダ、美術判定は生成/実施していない。実行できなかったことを、動いたことにすり替えない。

## 2. G0 2案比較（どちらも美術合格ではない）

| | A《CIVIC STRATA / 居住都市層》 | B《INVERTED HANGING VALLEY / 吊り下げ谷殿》 |
|---|---|---|
| 主造形 | 公共室と用途の深い建築帯を、12の手動編集可能な断面と4用途から同時構成。離れたカメラも設計初期から契約化 | 巨大な外殻・屋根・浮遊壁から視覚的ランドマークを作り、その中へ用途を後付け |
| A51からの方法変化 | 独立したBlender Mesh/Bezierカーブ/Surface厚み/材質/光を**後から人間が編集可能**。単なるパラメータ押し出しの自動生成を主制作にしない | A34–37の採石場、A45の巨大屋根・暗い公共室を再発する可能性が高い |
| A53扱い | **編集可能シーンのG0製作実験対象**（S1未審査） | **G0で停止**。外殻・屋根・浮遊構造の永久禁止ではない |

A案の内部・外部を美術的に合格と判定したわけではない。とくに断面が対向する「谷」に変化する危険、北側の連結と実居住階層が人間目線から見えない危険は強い。評価には必ずBlender実レンダが必要。

## 3. 再利用可能な実制作操作と安全

ローカル環境にBlenderがある場合のみ、リポジトリルートから次を実行する設計。

まず純Pythonの構成検査（Blenderは不要）：
```powershell
python tools/g4c7_a53_blender_scene.py --preflight
```

次にBlender実制作・9視点レンダ（Blender実行可能ファイルがPATHにある場合）：
```powershell
blender -b --factory-startup --python tools/g4c7_a53_blender_scene.py -- --build --render
```

実行予定の生成先：`artifacts/g4c7-a53-editable-studio/blender-output/` の新規 `a53_civic_strata_editable.blend` と `render_<view>.png` 計9枚。**既に同名がある場合には上書き拒否**。GitHubにBlenderバイナリや実レンダがあるとは主張しない。

Blender 4.5 Python APIの`Material.surface_render_method`やCycles設定の公式仕様と照合し、不要な外部アカウントは前提にしない。参照：<https://docs.blender.org/api/4.5/bpy.types.Material.html>。

## 4. 今回実行できたQA、できなかったQA

| QA | 実績 |
|---|---|
| GitHub A52 HEAD・監査・引き継ぎ確認 | PASS |
| A53断面コントロール計12点の高さ・単調順序・左右関係 | PASS（Chat独立JS計算） |
| 4用途領域の面積・高さ・重複ID | PASS（Chat独立JS計算） |
| 9視点定義のID一意性・存在 | PASS（Chat独立JS計算） |
| 故意の断面順序破綻・退化多角形・カメラ欠損・施工許可誤設定・高さ逆転 | **5/5検出PASS** |
| Blender Pythonコードの実Python AST/CLIプリフライト | **NOT RUN** |
| `bpy`の実シーン作成・ネイティブ.blend保存 | **NOT RUN** |
| 材質/影/光を含むCyclesレンダ・9視点の実画像 | **NOT RUN** |
| S1人間目線、G1都市全景の実3D美術判定 | **NOT RUN** |
| G2人間歩行／G3 331人体・993足元・負対照 | **NOT RUN** |

A53のG0条件は「ツールを作った」だけで**美しい未来都市建築が成立したという主張ではない**。プロジェクト全体のART HOLDを維持する。

## 5. A54への明確な次工程

1. **まずPython `--preflight` とBlenderでの実シーン生成を実行**する。無条件に次の建築形状を制作しない。Blender実環境がない場合はツール導入方法を再検討する。追加アカウント作成や大規模手動工程はユーザーに無断で要求しない。
2. Cyclesによる9視点（人間目線5＋遠景4）の実レンダが取得できた場合に限り、人間が画像を観察してA53案の**S1を正式に判定**する。閲覧・市場・文化・居住の利用可能な室としての視覚成立と、都市としての一体感を別々に審査。
3. そこで学習環境に合わない、採石場・巨大屋根・単独キャンパス・大きな空白に見えるなら**ART REJECTで即停止**。材質変更で悪い建築を隠す改善はしない。
4. S1が仮に合格しても全都市級G1は別判定、支持床/実歩行G2、安全G3の正式PASSも別。Minecraft Education施工・統合の許可とは無関係。

**恒久制約：ART-FIRST／QUALITY-FIRST、全体 ART HOLD、Minecraft Education施工／都市統合禁止、旧world/USED/CSV/ZIP/GLB/OBJ/PNG破壊・上書き禁止、人体331、足元993、人体半幅0.65、足元相対+0.15〜+3.25、歴史的身体表面干渉上限45、未支持足元0、負の対照必須、Work使用はユーザーの事前明示承認が必要。**
