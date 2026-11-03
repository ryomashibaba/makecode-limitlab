# G4-C7 M37-P2：本物のBlender GUI 2画面をX11経由で復元（2026-11-03）

**限定TECH成立：2つのBlender VIEW_3D領域の外部X11ピクセルを、座標・ウィンドウ名・SHAと実ピクセル一致から独立検証。自律GUI作者編集は未達。ART HOLD、正式採用0。**

## 一次証拠
- [実行 #41572794264](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41572794264) のArtifact ID **13209321279** の実PNGをダウンロード・直接目視。Blender 4.5.15、左右のVIEW_3D、Outliner、グリッド、プロパティが表示され、以前のQuick Setupモーダルは消えている。保護v3空BLENDで、都市メッシュ0。
- Blender内部 `screenshot_area` のMACRO_EDITORは**1×1黒PNG**、LIVEDは未作成（API撮影経路失敗）。一方X11のBlenderウィンドウは1600×900で実表示、window PNG SHA256 `2240be8ca820033f7bf5f282bf6a3a29c923c5f99bdfaf69e275ef718ed1dd36`。
- Blender記録のVIEW_3D領域座標を左上原点へ正確に変換し、X11の元ウィンドウから抽出。MACRO657×783、SHA `ac34c13084ec18d3289e6a2bae10a65f321f37550200e11f1b22a43dca5c7a9a`、LIVED661×783、SHA `3d9c054e6b17bd5fa9afa8d65e98c7c3f8b39be2923e62e23c791ce09ec46c4a`。
- [X11 read-only visual context bridge](../../../tools/g4c7_m37p2_x11_visual_context_bridge.py)をこの実Artifact上で走らせ、**両領域のウィンドウ切り出しピクセル完全一致、保護原本SHA、GUIタイトル、非黒と色数**を検証して PASS。失敗を伴う偽造画像・黒画像・座標ずれなどを拒否する[11件の隔離テスト](../../../tests/test_g4c7_m37p2_x11_visual_context_bridge.py)も11/11 PASS。
- [既存GUI CI](../../../.github/workflows/g4c7-m37p2-genuine-live-gui-context-capture.yml)を改修し、既知のBlender撮影API exit8だけをX11経路へ流し、独立検証が成功しない限りFAILする。新版CI [#41597467506](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41597467506) はこの記録時点ではQueuedであり、クラウド新環境でのPASSは未確認。

## 重要な区別と次工程
- X11が元Blender領域の実ピクセルを取得できた**読み取り能力**と、Blender内部の撮影API修復、モデルによるマウス・キーボード操作、都市3Dの実作者編集は別。後者はすべて未実証。空のGUIを取り出せたことを美術進歩とは呼ばない。
- Blender/Cyclesによる以前の[本物の4画像](M37P2_20261103_TRUE_CYCLES_FOUR_VIEW_FINAL_EARLY_ART_REJECT_JA.md)は実証済みだが、作品はEARLY ART REJECT。これ以上同型の箱・壁・塔を生成器で再提出しない。次は同じネイティブBlender都市作品を見て**直接作者編集→保存差分→真正Cycles→視覚批評**する経路を開通できるか調査する。WorkとSolは本人の事前承認まで不使用。
- R0〜R5、全体ART HOLD／採用0、331人体993足元とG0/S1/G1/G2/G3 NOT RUN、MakeCode未評価、Minecraft施工禁止、main・保護v3不変、PR #53 Draftを維持。
