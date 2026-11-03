# G4-C7 R1 — 不採用都市の真正Blender GUI可視化復旧・限定TECH（2026-11-03 JST）

## 実結果・美術への影響（最優先）

**前回R1 Civic EstuaryのEARLY ART REJECTは一切撤回しない。全体ART HOLD／正式採用0。**
本工程では**不採用の実際の保存Blender都市**を変更せず、従来の全画素RGB(24,24,24)問題を再現しない真正X11のビューポート画面を取得した。これは**実複雑シーンのGUI読み取り・視点ナビゲーションについての限定TECH PASS**であり、真正GUIをAIが自主的に美術編集した証明ではない。都市の形状・住居・工場・公共空間は改善していない。

## 現物・起動経路

- 成功した専用CI：[ #41611672731 ](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41611672731)、**completed/success**。保存した画像・実ウィンドウ情報・独立ピクセル監査は [GitHub恒久アーカイブ](../../../../artifacts/g4c7-r1-rejected-native-x11-real-pixel-audit-HOLD/)。
- 実装 [読み取り専用X11キャプチャ](../../../../tools/g4c7_r1_rejected_native_x11_readonly_capture.sh)、[画素と元シーンの独立ゲート](../../../../tools/g4c7_r1_x11_readonly_visual_gate.py)、[専用CI](../../../../.github/workflows/g4c7-r1-rejected-native-x11-visual-gate.yml)。
- Blender **4.5.15** を公式SHA256検証のうえXvfbで起動。**最初から最後まで同じ保存原本を開いた**まま、実キーボードの `Home`（全体を画面へ）→ `KP_1`（Front Orthographic）で表示操作。scrotでBlenderウィンドウの実ピクセルとX11 rootの実ピクセルを別経路で記録。
- 入力は前回正式に不採用とされた **R1_CIVIC_ESTUARY_GUI_DIRECT_EDIT_NOT_ART.blend**。SHA256 **cadf0678f7a57636dbebe7432e95d4aae98a2a0cc57215652177d9cbd6ef0e06**。CIで前後検証済み、再保存・メッシュ変更ゼロ。保護v3元原本SHA256 **536e451c763c4326421b13285abf1056a3a11d755028f8ff20b54b99b08a0249**をCIで照合、不変更。
- 画面出力 `X11_REJECTED_R1_BEFORE_WINDOW.png` と `X11_REJECTED_R1_AFTER_WINDOW.png`：両方**1600×900**。前のPNG SHA256 **e38e9980819067972994ad8e3f8203ea922f419b8a9c493a646298af10b388a2**、後のPNG SHA256 **77e69709e3c32eec40375091a4ddba7a3466f2a8c3475d6230c093a5fdd8d456**。独立ルートスクショも同じ場面が映り、それぞれこのSHAと一致。
- 画素監査：160×90縮小標本の異色数 **1261→859**、最大チャンネル標準偏差 **14.4001→14.21**、大差分サンプル **918/14400**。単色ではない。Blenderウィンドウ識別情報も保存済み。
- **画像現物を別途人間目視相当の画像確認で照合**：1枚目はBlender編集UI、オブジェクト一覧、選択されている「CONTEXT_ONLY garden-bearing research terrain」、不採用の反復塔/工場が映る斜め俯瞰のUser Perspective。2枚目は同じ編集UI・同一都市が横から映るFront Orthographic。**単純な数値変化だけで「見えた」と判定したわけではない。**
- 一時Actions Artifact **13219516759** と、研究ブランチに保存された同一画像・監査JSONを区別。恒久保存CIとGitHub実ファイルの存在を双方確認。

## 技術的な厳密な範囲・原因未確定

- **今回成立：** 既存の千メッシュ超の複雑な不採用Blender保存3DのGUI上の可視化、X11真正画像取得、視点変更の実画面差、ソースSHA不変、append-onlyアーカイブ。
- **不成立：** 高品質なAI GUI直接美術制作、建物/住宅/工場の美術改善、AIによる画像に基づく判断→意味のある3D造形の反復編集、自律品質保証。
- 先行CI #41609556650 では実GUI入力によるオブジェクト変換が観測され、別名保存/独立再読込したが、前後GUIスクリーンショットが両方RGB(24,24,24)で不可視だった。今回の別プロセス新起動・read-onlyナビゲーションでは画面が可視。**なぜ前回だけ単色になったかの単一の根本原因は未確定**である。今回のX11を前回のGUI内表示と偽って置き換えたり、撮れたことだけで完全な閉ループTECH PASSにしない。
- `R1_CIVIC_ESTUARY` 形状自体は巨大青緑隔壁・多角柱同型塔・空白街路・居住体験欠落により**引き続きEARLY ART REJECT**。同案を追加装飾・色調・塔増加で救済することは禁止。

## 次の本来の美術工程／継続条件

1. **新しい試案を空の自動プリミティブ大量生成で立ち上げない。** R1は高品質都市作者設計が主役。宏観街区密度＋公共街路＋住居入口/前室/居間/窓＋宇宙機製造設備・見学隔壁＋研究文化施設を**同一保存Blender原本で最初から並行**造形する。
2. 続く真の能力証明は**映っている都市の写真を実際に読み、作者がその画面をもとに建築的・構成的な編集指示を選び、GUI上で意味のある設計変更を行い、同じ3D原本を独立保存・再読込し真正AERIAL/PUBLIC_EYE/HABITAT_EYEを絶対美術審査すること**。既存不採用案の改修で済ませない。
3. その制作能力がChat＋既存GitHub Actionsだけでは使えないなら、**自律R1作者制作は未成立**と明記する。Work/クラウドPC/追加有料サービス/Solを無断使用しない。品質の小幅な犠牲を伴うローカルLLM置換も禁止。

## 不変憲章

R0〜R5固定、ART-FIRST/QUALITY-FIRST。331人体・993足元・人体半幅0.65・足元相対+0.15〜+3.25m・干渉上限45・未支持0は**正式契約不変更**、正式G0/S1/G1/G2/G3はNOT RUN。MakeCodeの新都市施工コストNOT EVALUATED。Minecraft Education施工・既存都市統合禁止、world writes 0。main/保護v3/旧原本/失敗証拠不変更、PR #53 Open/Draft維持。本人の正式ART採用0件。WorkとSolは事前明示許可制。新アカウント・有料外部サービスは今回未使用。
