# G4-C7 A73 — 公共動線を単一幾何原本にした実形状コンパイラ（G0・ART HOLD）

2026-10-27 JST / 開始HEAD `0b61df21fd641ec8ea4e9970eff2c26b46e97710` / **正式採用0、全体ART HOLD、Minecraft Education施工・都市統合禁止**

## 根本問題と今回の変更
A72では「真正Blenderの床・実室・壁・開口・40踏面」を作ったが、同じ公共空間に用途が実際につながっていなかった。市場の入口床接合約2.25m、工房約0.07m、研究閲覧0mかつ1.30mの離隔、住宅への上下動線未定義。遠近真正Cycles2画像は低層施設/巨大壁でART REJECT。旧原型の改修・増築・装飾はしない。

**A73では、一つの公共動線グラフの端点から入口、道路床、建築室床を同時に導出する。** 「室ごとの3Dを先に作り、最後に床を合わせる」工程を逆転した。これは美術的な突破ではなく、A72にあった根本的な設計矛盾を**新しい案へ引き継がないための基礎技術**。

原本：[`a73_topology_fabric.py.gz`](../artifacts/g4c7-a73-route-derived-architecture/a73_topology_fabric.py.gz)（gunzip後Python SHA-256 `d3ee82add5f1aafc97284a564043df2503b7350ea7bb5ee19201c1c2689da553`）。専用GitHub ActionsではSHAを照合し、[原本Python](../tools/g4c7_a73_topology_fabric.py)、[生成された本物の3D三角形OBJ](../artifacts/g4c7-a73-route-derived-architecture/g0-output/a73_continuous_route_and_rooms.obj)、[同じ計画を示す2D SVG](../artifacts/g4c7-a73-route-derived-architecture/g0-output/a73_route_floor_door_plan.svg)、[PNG表示](../artifacts/g4c7-a73-route-derived-architecture/g0-output/a73_route_floor_door_plan.png)と[証拠JSON](../artifacts/g4c7-a73-route-derived-architecture/g0-output/a73_manifest.json)をappend-only保存する。**Actions結果を実確認するまではGitHub生成物が保存済みとしない**。

## ローカルで実行・確認済みの客観結果
- Shapely 2.1.2を用いた単一設計原本に市場、工房、閲覧/研究、住宅の4用途・公共交点・複数高さの歩行路を記述。
- **市場4.0m/4.0m、工房4.2m/4.2m、閲覧4.6m/4.6m、住宅4.0m/4.0m**：各開口全幅が**同じ設計高さの床面ポリゴン**に交わる。設計時に両者を同じ歩行路から生成するため偶然の交差ではない。
- 3組の階段を定義：20段×0.18m→3.6m、20段→さらに7.2m、30段→最終12.6m。踏面奥行き0.32mのルートに対し水平ラン6.4m/6.4m/9.6mを照合。地上から住宅・庭園まで13本の有向エッジをつないだグラフの到達判定PASS。
- 故意不正**9/9検出**：偽美術PASS、偽G2 PASS、施工許可、階段高さ不一致、住宅経路の断絶、過大入口、狭すぎる公共路、閲覧経路断絶、数km都市完成の偽宣言。
- G0の本物のOBJ三角形面は**744頂点・248三角形**。各階の床面・屋内床・分割された入口壁、階段70踏面の概念的メッシュを生成。Blender/Cyclesの真正二視点画像でも、美術的に完成した建築でもない。
- 単一図面とOBJは必要な接続を記録する**デバッグ用標本**であり、超未来都市造形としては未審査/未採用。

## 独立技術検証と限界
ローカル`python tools/g4c7_a73_topology_fabric.py --verify --negatives --build` は完了。GitHubでは [専用Actions](../.github/workflows/verify_g4c7_a73_topology.yml) が原本をSHA復元して再実行し、4つの入口接続・3つの階段・OBJ三角形・SVG/PNGおよび保護フラグを検査する。

**重要：同じ高さの床が入口全幅と接するのは必要条件に過ぎず、正式な経路安全性・G2/G3合格ではない。** 衝突・頭上空間・実支持・連続衝突掃引・車椅子の連続アクセス・避難・採光・構造計算・内部装飾・質の高い外形は未検査。生成OBJは将来の作者が選定した美術形態を支える**床・入口接続の幾何原本**であり、数km級都市の見栄えを示していない。

## 次工程のゲート
**同じ箱・厚板・低層施設のBlenderモデルをもう1個生成することを成果としない。** 次のA74ではこの接続済み幾何の周囲を単に箱で塞がず、「屋外に見える実用途の深さ」および「強い都市独自の遠景」の両方を作者が形状として具体的に設計できる候補だけを、A53/A72で実績のある真正Blender編集基盤で1個反証する。美術が弱ければ描画を停止し、ART HOLDを維持。

既存通常CI`build/g4c4_access_baseline.json`欠落FAILは未修正。偽baseline/テストskip禁止。旧331人体、993足元、半幅0.65、足元高さ+0.15〜+3.25、衝突45以下、未支持0、負対照の正式G2/G3契約は不変。全world/USED/CSV/ZIP/OBJ/GLB/PNG/.blendの原本を保護。Work使用はユーザーの事前承認なしには行わない。

**A73判定：公共路から開口/実床/段差を共有生成する基礎技術を制作。美術的突破は未実証で正式採用0、全体ART HOLD、S1/G1/G2/G3すべてNOT RUN、Minecraft施工・都市統合禁止。**

## A73独立GitHub Actionsと原本一致：確定版

- [専用Actions #40487809349](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/40487809349) **SUCCESS**。圧縮原本の SHA-256、Pythonの実行、9個の故意不正、4用途の同じ高さでの入口全幅・床接触、3つの階段、OBJ頂点数/三角形数、SVG→PNG寸法をそれぞれ独立検査した。これは**局所設計データの技術PASS**であり、美術PASS／正式歩行PASSではない。
- bot保存コミット [`218fd0644c8f59fa9d3e39434b20bcfe598f5329`](https://github.com/ryomashibaba/makecode-limitlab/commit/218fd0644c8f59fa9d3e39434b20bcfe598f5329) に復元Python、生成OBJ(744頂点/248三角形)、SVG、実PNG、検証JSONを**append-only**保存。Python Git blob `3d66148a672bb37482ae0139276a57edcbcc35ef`、OBJ `b0ce4cd3041f43acfd7f34e753d9d3b48fbeec47`、manifest `923325af6f1b0ce876e4ac6a5f80154428dd04bc`、SVG `1b72958788cd39283807142b4f8bff54b448dcb5` はローカル原本と**4/4一致**。PNGはActionsでラスタ化した技術的な2Dレイアウト図（真正3Dレンダではない）。
- [通常CI #40487809254](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/40487809254) **FAIL**。428件中1件のエラー、従来の`build/g4c4_access_baseline.json`が欠落。偽baseline/skipなし。
- 図の美術判定：**都市のアート対象外**。これは人が住む未来都市ではなく、共有床・4室と階段の検証用標本であり、生成OBJの美術採用をしない。過去のA72の美術失敗を造形上克服したとは主張しない。
- 次A74の原則：**新たな美術方向を作者が視覚評価してから**、この設計原本と接続検査を内部構造として再利用。G0接続検査を通過しても都市外観が弱ければART HOLD/REJECTにする。S1/G1/G2/G3全てNOT RUN、施工・都市統合禁止。
