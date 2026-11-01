# D3S26-M16 / M16B — 既存BLENDの2段階直接編集と8視点比較、ART REJECT
**2026-11-01 JST / M16 & M16B TECH PASS / ART REJECT, 0 ADOPTED / formal QA NOT RUN**

## 計画・実現結果
M15Cの既存編集可能BLENDを原本として、**全く新しい箱型模型を作るのではなく**、保存原本を実際のBlender 4.5.15で再オープンし、画像で見えた問題のある現実のメッシュオブジェクトを削除・置換する2段階のネイティブ編集を実施。Windows操作、Blender再セットアップ、ユーザーによるZIPアップロードはすべて0回。M15C保護原本はSHA256 `4b17686607764fbfcddd54e32b132c2a8bea04f21a5c46ae0ff7525955bc9132`。GitHub Actionsの過去の成功Artifactから取得し、同一SHAをブロック検査。

### M16実行
- コミット `634eb9ab1905c2b7c1cf599d53932b4f03216e64`。[M16 run #41254354425](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41254354425) **全工程SUCCESS**。
- 4つの巨大な不透明外壁（工房西側、市場東側、研究北側、住居アプローチ）を、実柱・窓の開口・自然光を取り入れる透過面へ置換。工房の巨大な一枚屋根を分節。住居の入口、実床、作業机、座席、採光窓を新しいネイティブオブジェクトとして追加。研究・住居カメラの目線2件を再配置。
- 既存.blendの実編集結果を新しい.blendとGLBに保存し、8枚の真正Cycles PNGを撮影。CI独立ハッシュ/PNG監査PASS。会話へ証拠ZIP `D3S26_M16_NATIVE_EDIT_EVIDENCE.zip`を取得。ZIP SHA256 `a8564417d5005926c3b6d12818219f8576f749571ae5433948a6b3c18adb4080`、独立CRC/SHA PASS。保存GLB独立読込 **162 geometry / 4,296 triangles**（元M15Cは126 / 3,994）。
- 従来は外壁が真っ黒/無表情だった遠景に、実柱と窓の分節が見える。ただし研究者視点はかえって大きな壁が正面を塞ぎ、住居視点には開口の柱が被っていた。**M16だけでは視覚改善と判定できなかった。**

### M16B（同じ原本の2回目の直接修正）
- M16の保存.blend（SHA256 `842ea0bc63f062eef39b6637066661c1f0d307d2b2110bb4a1d9868e91d4678b`）を次工程の入力として保護。前回の実GLBから三角面への独立視線交差テストを実施。研究者アイレベルは近距離**6.56模型単位**で不透明な `MAKER_NORTH_THICK_WALL` に接触。住居は入口柱、製造者は大きなガラス面が視界を阻害していた。
- M16Bソース `tools/g4c7_d3s26_m16b_second_visual_edit.py` は、工房北の実壁を開口・柱・透過面で直接置換し、工房正面の大きいガラスパネル2枚を削除。製造者・研究者・居住者の各カメラを実活動を見やすくするよう修正。**カメラ変更の3枚は固定カメラでの同条件比較ではない**。
- 最初のM16B run #41254673249 は誤ったダウンロード元Artifact名で**FAIL**。workflowの参照先を修正commit `a6828efac4dee3087f0716def4f59f8bf323aee7`。再実行 [run #41254690217](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41254690217) は全工程 **SUCCESS**。
- M16Bネイティブ.blend SHA256 `8dff09ae7cd8e08c8278d9d5e61ef66754213a50bb8c979c6916df484760e762`、GLB SHA256 `e1e3a35ad6bf74e01f2fb96db01299724195439b77e3138ec1fc51ad4adc1e69`。真正Cycles PNG 8/8ハッシュPASS、GLB独立再読込 **170 geometry / 4,382 triangles**。会話ZIP `D3S26_M16B_NATIVE_EDIT_EVIDENCE.zip` SHA256 `c253258c32c633edc056cf11a3686c83c278b60e65162a7b718930f18f98876c`。
- GLB独立視線再検査で研究者視線の最初の交差物体は**9.02模型単位**先の新しい透明採光パネルであり、元の不透明北壁は除去済。工房正面の元パネル2枚も非存在を確認。透明パネルは現実の見通し・採光品質の保証ではない。

## 実視点の厳格評価（ART HOLD / REJECT）
- 遠景：不透明外壁の一部は柱/採光面に置き換わったが、大規模な低層箱型建築・板状屋根がなお支配する。美しい未来都市とは評価できない。
- `maker_eye`：2回目は工房の内部作業台や設備が以前より読める。視点変更の影響もあるため**限定改善候補**に留める。
- `research_eye`：元の不透明な壁衝突を修正したものの、白い柱・すりガラスに近い面が視界の大半を占める。**目標の見通しと公共性は未達**。
- `resident_eye`：専用の居室床・家具・窓を初めて表現したが、巨大な柱と単調な床/家具が目立ち、実生活の魅力や私的領域の成熟は不足。
- 8視点画像の比較原本はChatの `M16_BEFORE_AFTER_TRUE_BLENDER_8_VIEWS.jpg`、`M16_TO_M16B_ACTUAL_CYCLES_COMPARISON.jpg`、`M15C_M16_M16B_EYE_VIEW_THREE_STAGE.jpg` として確保。3つの人間眼高は後段でカメラを変更したため絶対比較指標に用いない。

**結論：原本を守るBlender上の真正二段階直接編集・再撮影・独立再読込はTECH PASS。部分的な実開口/住居機能や工房視認性は前進。しかし総合ART REJECT、正式採用0。** 単にガラス・家具・柱の追加を重ねて小さな建物を延命しない。今後は居住する建築の視覚設計と都市全体の美術品質の両方を成立させる作者媒体が必要。

## 安全・施工・保護
本結果は真の自由通行、階段/橋の人体幅、head clearance、331人体/993足元、公式G0/S1/G1/G2/G3を**未検証**。Minecraft Education施工・都市統合 **禁止**、実施工時はMakeCodeのみ。main変更なし。PR #53 Draft/Openの研究ブランチへ**テキスト監査だけappend-only**。BLEND/GLB/PNGはGitHub Actions artifactとChat側のZIPに存在し、Gitツリーの恒久バイナリとして保存されたとは主張しない。
