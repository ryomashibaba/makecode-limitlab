# A72 — 個別編集可能な真正Blender建築断面への制作方法転換（G0）

2026-10-27 JST／開始HEAD `14b388b0c002c7993495d3fa1dae3374b0b99b51`／**正式美術採用0、全体ART HOLD、施工・都市統合禁止**。

## 設計改革

A66「多角柱」、A67「258の分離した開放小室」、A68「12枚の厚板」、A69「実室を持つ低層キャンパス」、A70「段状山の2D構想」、A71「閉じた鋸歯状巨大塊の構想」はいずれも**正式ART REJECTまたはHOLD**。各段階の技術PASSは美術の進歩ではない。A71の不合格画像は**3Dへ押し出さない**。

A72では[新しい作者別編集Blenderソース](../tools/g4c7_a72_native_authoring.py)を実装した。これは**A53/A59の主形状を引き継がない独立コード**である。
- 1つの公共結節に、市場・工房・上階閲覧室・上階住宅をそれぞれ異なる**手指定の平面多角形**で設計。
- 各室について、実床（厚み付き面）、独立した分割壁、**入口が実際に抜けている**前面、上部まぐさ、個別に編集可能な非対称屋根のメッシュを用意。名前だけ「居住」で厚板を認定するA68の誤りは再利用しない。
- 1枚の巨大板、長い巨大外殻、塔群、筒、閉じた段状山を**自動生成しない**。
- 独立した40踏面（20+20）と踊り場の実メッシュ、四用途の家具・活動領域を出力。**正式歩行・支持・身体干渉・採光を保証しない**。
- 一つの本物の.blendに眼高1.7mの近景と同じシーンの斜視カメラを保持し、Blender Foundation公式`bpy==4.5.15`、Cycles 960×720 2視点をレンダリングする。前A59同様、編集可能な.blendをappend-only保存予定。

## 独立反証
- `python tools/g4c7_a72_native_authoring.py --preflight --negatives` ：設計データと故意不正7件を検出（GitHub Actionsの実行結果確定までPASS未主張）。
- 専用Actions [A72 Blender](../.github/workflows/verify_g4c7_a72_blender.yml)は真の.blen d（.blend）を再読込し、4室の物理床・開口、40踏面、2カメラ、2枚の実PNGとSHAを照合する。
- ここで合格するのは**本物の3Dファイルが存在するという技術的再現性だけ**。アートやS1/G1/G2/G3の合否ではない。

## 芸術的な厳格ゲート
実画像の近景が白通路・暗い壁・汎用の商業施設なら即REJECT。斜視が学校・低層キャンパス・不規則な四角い屋根なら即REJECT。新しいモデルを大規模に量産せず、その後の形態制作も停止する。特定用途が見える**実室の奥行き**と、未来都市らしい建築全体の圧倒的な意匠は独立した課題として審査。

**S1/G1/G2/G3正式ゲート全てNOT RUN、G2歴史契約331人体・993足元・半幅0.65・足高さ+0.15〜+3.25・干渉45以下・未支持0・故意負対照を維持**。Minecraft Educationへの施工・都市統合は禁止。歴代world/USED/CSV/ZIP/OBJ/GLB/PNG/.blendは変更しない。Work未使用（明示承認制）。通常CI既存の`build/g4c4_access_baseline.json`欠落も偽修復しない。

**A72事前段階の判定**：本物の作者編集可能な3D制作方法を新規実装。真正実行と画像審査は未確定、ART HOLD。

## A72真正画像の独立審査 — 技術再現SUCCESS・美術ART REJECT
- [A72専用Blender/Cycles Actions #40481208513](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/40481208513) **SUCCESS**。A72 Python設計、故意不正7件、Blender Foundation bpy 4.5.15、真正Cycles 960×720の2視点、Blender .blend再オープン、PNG SHA/CRCなどを独立確認。
- bot append-only [d5b9a8d7af37634f775f0559c2431e12a95547b7](https://github.com/ryomashibaba/makecode-limitlab/commit/d5b9a8d7af37634f775f0559c2431e12a95547b7) が[編集可能Blender原本](../artifacts/g4c7-a72-authored-native/native-output/a72_authored_true_section.blend)および[真正近景](../artifacts/g4c7-a72-authored-native/native-output/render_public_heart.png)、[真正斜視](../artifacts/g4c7-a72-authored-native/native-output/render_oblique.png)、[manifest](../artifacts/g4c7-a72-authored-native/native-output/a72_native_manifest.json)を保護。
- 保存PNG2枚をGitHubからbase64再取得し、独立目視。**OBLIQUE ART REJECT**：三〜四棟の単純な折れ屋根の低層施設の集合。圧倒的な未来文明の固有な巨大造形は皆無。**PUBLIC HEART ART REJECT**：暗く無地の左右壁、大きな無人の公共床、不自然に浮いた階段が主役。市場・工房・閲覧の実活動が全く読み取りづらい。A69低層キャンパスへの回帰。
- **重要な技術反証**：開口形状ができていても公共床へ到達できるとは限らない。Pythonの部屋前面・プラザの原本ポリゴン・閲覧アプローチ床の2D同一高さ投影を独立のShapelyで測定。市場6m開口の床交差2.251339m、工房6m開口の床交差**0.069874m（約7cm）**、閲覧室6.4m開口の床交差**0m**でアプローチと最短**1.302364m離隔**。住宅床は12.6mでそこへ向かう独立階段が未定義。数値は**G0局所床接続の不備**であり正式G2/G3ではない。
- [独立幾何反証コード](../tools/g4c7_a72_access_postmortem.py)と[専用Actions](../.github/workflows/verify_g4c7_a72_access_defects.yml)でこの既知欠陥を**PASS=再検出**として自動再現し、設計が可用と誤報することを防止。**この再現テストの成功を到達性PASSとして扱わない。**
- **A72 ART REJECT、全体ART HOLD、正式美術採用0**。新3Dを延命・複製・窓や照明で誤魔化さない。将来は**都市の外形と人が実際に使う面を同一の設計判断で確定する工程**へ転換。正式S1/G1/G2/G3 NOT RUN・施工/都市統合FORBIDDEN・過去全原本不変更。

## A72 access regression Actions：独立実行確定

- [A72既知欠陥再現 Actions #40481921861](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/40481921861) **SUCCESS**。原本`tools/g4c7_a72_native_authoring.py`のGit blob SHA `a76d14d88f12d36009448cc241a8d653a39b719a`を固定したうえで、Shapelyによる公共床と各実開口の局所的な接触長を再計算。**成功は「接続欠陥を再現した」の意味であり、アクセス/歩行/美術をPASSしたのではない**。
- 独立Blender/Cycles真正制作SUCCESS [#40481208513](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/40481208513) は、同一モデルの2視点と可編集.blendがGitHubで作れる技術の証拠に限定。画像を目視して近景・遠景ともART REJECTで確定。
- 通常CI [#40481208357](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/40481208357) **FAIL**：428件中1件のsetup error、従来からの`build/g4c4_access_baseline.json`の欠落を実ログで再確認。偽baselineやskipなし。
- **A72の最終結論は「本物の3Dを作るツールができても、建築美術と実到達性を保証しない」**。A73はこの原型に窓・橋・屋根を足すのではなく、都市形態の作者的な独創性とその空間配置を独立に再構成する。ART HOLD、採用0、S1/G1/G2/G3 NOT RUN、Minecraft施工・都市統合禁止。
