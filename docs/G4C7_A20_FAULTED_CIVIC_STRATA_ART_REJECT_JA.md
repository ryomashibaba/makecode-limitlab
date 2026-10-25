# G4-C7 A20：段丘峡谷一体都市の実3Dマス試作／ART REJECT

2026-10-25 JST。既存MakeCode LimitLab G4-C7研究のA20軽量美術探索。Minecraft施工・都市統合は未承認。

## 実装・保存

- source: `tools/g4c7_a20_faulted_civic_strata.mjs`（Node標準ライブラリ、geometry/GLB/OBJ/簡易QA再生成。4SVGの再レンダラーは未収録）
- saved: `artifacts/g4c7-a20-scout/a20_faulted_civic_strata.glb`, `.obj`, `a20_materials.mtl`, `a20_primitive_qa.json`, `fourview/{front,oblique,side,aerial}_a20.svg`
- shape: 西・東の非対称な都市段丘／居住崖、間に連続した大公共峡谷、横断公共街路、5層以上の住民空間・接地支柱を同時作成。前段階のリング・円筒・付け足し巨大帯との明確な差分を意図。
- data: **215** closed-volume primitive solids / **2,344** vertices / **3,828** triangles / highest Y≈**171.1** concept units. Degenerate triangles=0, per-solid signed volume <=0 count=0.
- recurring QA: 基準旧331人体・993足元・半幅0.65・足元+0.15〜3.25・負の対照・45干渉・支持不足0は一切変更なし。**A20新形状への経路QAは行っていない。**

## 4視点・美術的な失敗

実OBJ面から作成された同一スケールの front / oblique / side / aerial 比較を目視。正面は**二つの箱型積層壁**、斜視は**規則的な白い段々状ビル群**、側面は**塔の列**、俯瞰は**四角い屋上テラスの反復**が支配。峡谷中央の見通しや歩行の雰囲気には進展があるが、遠景で一体の大建築として読めない。上空の孤立した長細い床も確認できる。

**判定＝ART REJECT / ART HOLD。** 数値・GLB出力・四視点ファイルがあることは美術成功でも交通動線の安全証明でもない。これ以上同案に床を追加・厚くする・窓を増やすと同じ失敗を増幅する。**A20は次案に昇格せず、意図的な負の実体研究として保管する。**

## 次研究への方針

A19（円筒とリング）、A20（積層矩形建築）の両方をマクロ美術不合格として区別。次の軽量3D方向は『巨大負空間そのものが都市の輪郭を決め、外殻の曲面・占有公共層・支持基部が一体で変化する』ものを重点探索。単なる蛇状帯、双断崖、孤立スラブ、太アーチ、塔・箱の反復は避けるが、形態そのものは禁止しない。成功の見込みがない候補の正式QA/PR/Actions増殖を停止。

**ART HOLD / NO MINECRAFT CONSTRUCTION / NO CITY INTEGRATION.** 旧model/world/USED/CSV/ZIP/実機証拠は不変。GLBの独立第三者再読込、Boolean結合、自己交差、物理的荷重、通路の連続性は未証明。

### 固定カメラの追加比較
A19-A保存OBJとA20保存OBJの各三角形から、同一のA19撮影基準（front/oblique/side/aerial、視点・target・正投影scale完全共通）で2列の比較SVGを制作し恒久保存。場所：`artifacts/g4c7-a20-scout/matched_a19a_a20/`。再現コード：`tools/g4c7_a20_matched_review.mjs`。比較データ：`a20_matched_comparison_manifest.json`。**A20を美術合格へ変更するものではない。**
