# G4-C7 A75 — A73の共有動線と本物のBlender空間を単一原本で結ぶG0試作

**2026-10-27 JST / 基準HEAD `9c0384c975157fb4dedbc2f1ce4990fc0425effa` / 正式美術採用0 / 全体ART HOLD / Minecraft施工・都市統合禁止**

## 最初に確認した失敗
A70の階段状の山、A71の鋸歯状巨大塊、A72の低層キャンパスと実室・入口の接続欠陥、A74画像3案のリング・橋・水景リゾート回帰はいずれも正式採用不可。A73は唯一の接続技術上の前進だが、可用性全体や美術は証明していない。

**A75の着眼点**：既存のA73が計算した`plan['floors']`と`plan['rooms'][...]['door']`を直接読み、Blenderで真正の歩行床・実室床・分割壁・入口・70踏面へ変換。別々に指定したA72の入口・床位置の不一致を再発させない。**A73のファイルを編集しない**。

## 今回の実制作

1. [新Blender authoring source](../tools/g4c7_a75_registered_native.py)：`importlib`でA73の`make_plan()`を呼び出し、**4用途すべての入口が対応する公共床と全面的に重なること**を事前検査。A73由来の9種類の故意不正も実行可能。
2. Shapelyの三角形分割で公共通路と実室床を編集可能Blender mesh化。入口はA73の同じ実線分、周りの壁は別の非反復部材、上部には用途別の不均等な折れ面、内部に活動什器を設置。**単一A73接続路由来のモデル**。
3. 3階への上昇はA73グラフの20+20+30段を個別Blender踏面に変換。これは段の表現とグラフ整合のG0テストであり、人間の全経路歩行が成立した証拠ではない。
4. ひとつの編集可能な.blendにPUBLIC_EYE=(0,-16,1.7)および斜視の実カメラを設置し、Blender4.5/Cycles 960×720の真正二視点画像をレンダリングしてG0の美術を絶対審査。
5. [専用GitHub Actions](../.github/workflows/verify_g4c7_a75_native.yml)は従来のA73 Git blob SHAを固定し、別モデル/別原本へのすり替えを防ぐ。生成された.blendを再度開き、2カメラ、4つの実室/開口、70段、真正PNGのSHAを照合する。**独立Actions完了前は技術PASSやPNG保存済みと断言しない。**

## 作品そのものの美術ゲート

- 新試作は数kmスケールの超未来都市ではなく「一つの空間」である。入口/床接続が技術的に良くても**正式美術採用は0**。
- 斜視で4つの非対称低層建物や工房キャンパスに見えるなら即ART REJECT。人間目線で白い無人の廊下、巨大壁、装飾的屋根が主役なら即ART REJECT。
- 建築の見え方は、**本当の活動する室と都市形状が直接一致しているか**を最重視。折れ面がシルエットを少し変えるだけでは突破ではない。S1/G1/G2/G3のどれもG0では実施していない。
- 独創的な未来都市として美術採用できない場合は、同じ試作へ家具・窓・橋・屋根を追加して延命しない。A76では作品の独創的形態を決定する主体を、生成器から作者の空間設計へ変える方法を再検討。

## 不変契約
正式採用0、全体ART HOLD、S1/G1/G2/G3 NOT RUN。G2/G3旧331人体、993足元、半幅0.65、足元+0.15〜+3.25、干渉45以下、未支持0、負対照維持。Minecraft Education施工/都市統合禁止、過去world/USED/CSV/ZIP/OBJ/GLB/PNG/.blendを上書きしない。Workをユーザー承認なしに使わない。通常CI旧`build/g4c4_access_baseline.json`欠落を偽修復しない。

**現段階：実Blender統合ソースと専用Actionsを作成。真正レンダ・実画像美術評価はActions成功を確認するまで未確定。**

## 真正Blender二視点の直接画像審査後、A75最終判定

- [A75真正Blender Actions #40498888014](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/40498888014) **SUCCESS**。A73のGit blob `3d66148a672bb37482ae0139276a57edcbcc35ef`を固定し、共有公共床52面、実室4つ、入口4幅の同一高さ接合4/4、階段70踏面、編集可能Blender 4.5/Cycles同一シーン2カメラの技術的整合性を再実行・再読込確認。
- GitHub Actionsによるappend-only原本保存コミット[`81e5f6e9ec817a3388393a96cc2d97f89f13dea3`](https://github.com/ryomashibaba/makecode-limitlab/commit/81e5f6e9ec817a3388393a96cc2d97f89f13dea3)。[Blender実原本](../artifacts/g4c7-a75-registered-native/native-output/a75_registered_civic_section.blend) (Git blob `83a476ea920b15b2eb5000170d28916bd4c9ed08`)、[真正Cycles近景](../artifacts/g4c7-a75-registered-native/native-output/public_eye.png) (Git blob `ce8b8ce02a47dc8746d53d6050b1a7260fbaa5aa`)、[真正Cycles斜視](../artifacts/g4c7-a75-registered-native/native-output/oblique.png) (Git blob `2a433ad75ebb6b5c9a77612a1b19ac8c9cf25757`)、[SHA manifest](../artifacts/g4c7-a75-registered-native/native-output/a75_manifest.json)を保護。画像2枚はGitHubから取得し**実際に画像として目視した**。
- **PUBLIC EYE：G0 ART REJECT。** 無地の幅広い通路・両側の高い壁、奥の不連続な上層要素が視界を占拠。市場・制作・研究・住居の奥行きや社会生活が可視化されず、A69/A72の無人キャンパスに回帰。
- **OBLIQUE：G0 ART REJECT。** 4つの低層直方形系建物に角度を変えた屋根を付け、通路で結んだ模型。独自の超未来都市のシルエット、kmスケールの社会空間、文化的な存在感は形成されていない。異形の屋根と造作は単なる外観差分であり、成功ではない。
- **深い制作判断**：A73の原本共有は技術上の欠陥を解消する必要条件だが、**A73の4用途ノードの並びを直接そのまま建物にするアーキテクチャでは、魅力的な大都市になる論理的な道筋がない**。都市の外形を4つの実室の合計として自動決定する方式を停止し、A75の箱・屋根・小物の増築も停止。
- 画像から宙に浮いたように見える上層部が存在する。支持構造は一部擬似表現のみで、**実際の全接触、構造負荷、身体衝突、連続歩行・避難は未検証**。真正レンダはそれを証明しない。美術と安全のFAIL/未検証を混ぜない。
- [通常CI #40498887896](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/40498887896) **FAIL**。428テスト中1件のsetup errorで`build/g4c4_access_baseline.json`がない。元データ欠落を偽baseline・skipで通していない。
- その場での採用なし。**A75局所TECH PASS、G0美術は二視点ART REJECT、全体ART HOLD、正式美術採用0**。S1/G1/G2/G3 NOT RUN、Minecraft施工/都市統合禁止。重要な根拠は[後追い評価JSON](../artifacts/g4c7-a75-registered-native/native-output/../a75_art_verdict.json)。

## A76へつなぐ「変えないと進まない点」
A66〜A75では、巨大塊→空室→厚板→4室→構想画→4室再び、という巡回から脱出できなかった。**機械的に室を実装することや本物のCycles画像の枚数を増やすことは、問題解決策ではない。**

次工程はまず、都市遠景で**独自の地区間階層・圧倒的なkmスケール・実居住を持つ厚い構造**が同時に理解できる形を作者が編集して完成候補を選ぶ。その後、選ばれた同じ地区の実断面・都市活動を含めた一つの編集可能Blenderモデルで正当性を反証。単純な4棟・リング・橋・空洞・観光施設をもう一つ作るだけなら3D開始を禁止。A73の入口接合方法は**合格した造形の内部設計へ**流用するにとどめる。
