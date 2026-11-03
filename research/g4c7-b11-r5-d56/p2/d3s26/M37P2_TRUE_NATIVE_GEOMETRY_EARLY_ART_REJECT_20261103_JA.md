# M37-P2 — 真正BLEND原本の幾何学を独立可視化・EARLY ART REJECT（2026-11-03）

**本クラウドbpy案に限定して EARLY ART REJECT（GEOMETRY / COMPOSITION）**。全体ART HOLD・正式採用0件、R0〜R5は不変。

## 元ソースと独立検証
- GitHub Actions [#41577380073](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41577380073) のArtifact 13208845765から真正`M37P2_CLOUD_AI_NATIVE_INTEGRATED_STUDY_ART_HOLD.blend`を取得。SHA256 `ac6c322e1f4a957281ca5a7f2d9633ce4d602b7254cb1717735feb6ed02e9bd6`。
- zstd展開後、Blender DNA 957構造体のサイズ・オフセットが957/957一致。実Object→Mesh→`CustomDataLayer(position)`→`.corner_vert`→polygon offsetsを解決し、BLEND原本の頂点・面・物体変換を直接抽出。ソースから別の模型を再生成したわけではない。
- **227メッシュ、2,576頂点、4,244三角形、204/227（89.9%）が8頂点の単純メッシュ**。主要な塔12本は全て45頂点・86三角形の同規格（9角形5段リング）。旧source commit `abba4c0`と修正版CI source `6077fc4`の`def review(`前の**造形構築コードが逐字同一**であることを両GitHub原本で検証。

## 7つの形状代理画像を実際に見た結果
- **AERIAL**：平坦な2岸・単純な水路・同型塔反復が支配的。都市の街区と公共空間の密度がない。
- **PUBLIC_EYE**：パネルと単純な横向き船体・ガントリーが主体。街路や公共施設として成立しない。
- **HABITAT_EYE**：単純な箱家具・露出した床と天井。生活を支える住戸建築、壁・開口の構成がない。
- **CULTURE_EYE**：机・棚が単純形状のまま露出。研究文化施設としての完成度不足。
- **FACTORY_EYE**：低分割の筒状機体・門型フレームで、製造の機能的ディテールが不足。
- **TOPDOWN / WEST_CITY_EYE**：連続街区・固有の建築立面・都市的密度の欠落。

## 証拠の範囲・運用
**画像は真正BLENDに保存された実メッシュを、独立したVTKで描いた幾何学診断**。色・照明・材質は検査用代理であり、**Blender/Cyclesの正式レンダ画像でも、原本配色評価でもない**。7点は4つの既存カメラ座標と補足3点であり、憲章所定の正式7視点ART審査とは異なる。これにより確定できるのは**形状・空間構成の欠陥**。現物Cyclesの質感・照明・配色の良否は未確認。

本案は同型塔、box/beam/room/walkway調整の繰り返しでは救済しない。真の作者造形を同一native BLEND内の都市・製造・研究文化・住戸で現物検査と反復制作できる経路を次に目指す。既存修正版Cloud CI [#41577471323](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41577471323)のCycles画像は別途現物確認し、TECH成功で自動ART昇格しない。

正式331人体993足元、G0/S1/G1/G2/G3はNOT RUN、MakeCode未評価、Minecraft施工禁止、main・保護v3を変更せず、Draft PR #53継続。Work事前承認制、Sol事前承認制、クラウドART品質優先は不変。
