# G4-C7 A7 — Orbital Commons / 貫通開口と公共動線の造形研究

**基点：A6 PR #42（d74fa9e1c4054c152e1fcf7b0a9a4efb58ebd8c1）。A7：Draft PR #43。**

**判定：ART HOLD／Minecraft施工禁止／都市統合禁止。**

## 実装内容

A5の実GLBからA6コードを再生成し、それをA7の独立した3Dソリッド加工に使用。旧ファイルと旧ワールド、CSV、ZIP、USEDラッチは変更しない。

1. **南主アーチ東側を実開口化**：GLBのY-up座標で X=36〜71、Y=8.72〜13.55、Z=16.6〜23.4 の体積ボリュームを用意。SOUTH内殻・外殻をブーリアン差分で切除し、交差する南アーチの利用床があれば同様に切除する。単なる表示非表示やAIR宣言ではない。glTFの頂点重複は派生メッシュ上で位置溶接し、閉メッシュでなければCI失敗。
2. **支持されたデッキ**：楕円回廊からアーチ内部へY約8.918の幅5概念単位の床を架け、両端に地面に達する4本の柱を作る。
3. **地上接続路**：旧ランプの始点と公共地上東西軸の間へ、緩やかに曲がった幅10の舗装歩道を新設し、入口への地上からの連続を試みる。
4. **上空の箱状屋根の削減**：A6上空ギャラリー2枚の一体型屋根を4本の側縁曲面リボンへ交換。中央に実際のスカイスロットを残す。雨仕舞・強度・上空階の利用は未検証。

## 実体検査と負の対照

- tools/g4c7_a7_portal_route.py：実GLBのブーリアン切除前後の交差体積、ワールド配置、通過空間、床三角形への鉛直支持計算、A6元形状の衝突負対照、新橋床を取り除いた支持喪失負対照を定量化し、GLB/OBJ/JSONを出力する。
- 開口直方体はZ方向6.8・Y方向4.83、試験用通路ボックスは幅2.9・高さ3.12概念単位。幅高さは設計値であり、全長の安全な通路の存在を証明しない。
- サンプル経路：公共東西軸 → 新規アプローチ → 旧地上ランプ → 旧楕円回廊 → 新貫通デッキ。実際のGLBの床三角形と鉛直レイを交差計算し、足元に床があるかを検査する。地上からの任意経路探索や全身衝突検査ではない。
- tools/g4c7_a7_fourview.py：A6/A7実GLBの三角形からfront/oblique/side/aerialを同一正投影条件で画像化。簡易Pillowレンダラーであり、Blender EEVEEの光・深度品質とは異なる。Minecraftのスクリーンショットではない。
- .github/workflows/verify_g4c7_a7_portal.yml：上記全再現と正負QAを専用CIに集約。成功前にPASSを主張しない。汎用Verify LimitLabとは区別。

## GitHubと再現方法

専用ブランチ：dev/g4c7-a7-portal-supported-route-geometry

Draft PR：https://github.com/ryomashibaba/makecode-limitlab/pull/43

~~~bash
python -m pip install numpy==2.2.6 trimesh==4.6.13 manifold3d==3.2.1 pillow==11.3.0
python tools/g4c7_a7_portal_route.py --input artifacts/g4c7-a5/a5_orbital_commons.glb --out build/g4c7_a7
python tools/g4c7_a7_fourview.py --a6 build/g4c7_a7/source_a6/a6_orbital_commons_study.glb --a7 build/g4c7_a7/a7_orbital_commons_portal_study.glb --out build/g4c7_a7/fourview
~~~

生成成果：a7_orbital_commons_portal_study.glb / .obj、a7_geometry_route_qa.json、4視点比較PNG、view_provenance.json。GitHub Actions artifactへ保存。

## 審査境界

3Dの局所的な貫通と三角形上の床支持が将来確認できても、**Minecraft Educationでの3ブロック通路・階段・双方向の実歩行・構造耐力・道路からの歩行・美術合格のいずれも証明しない**。本工程にはMakeCode施工ソースもMinecraft実機結果もない。建築美術は別途4方向を審査し、納得できる造形に至るまでART HOLDのままにする。
