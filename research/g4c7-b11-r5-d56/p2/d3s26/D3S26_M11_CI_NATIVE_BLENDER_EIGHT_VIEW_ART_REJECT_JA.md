# G4-C7 D3S26-M11 — GitHub Actions上の真正Blender直接編集サイクル成立／CITY ART REJECT

**2026-10-31 JST。判定：Blender実行経路 TECH PASS、M11美術ART REJECT、全体 ART HOLD、正式美術採用0。**

## 制作環境の新しい実績
GitHub Actions [run #41190088190](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41190088190)で**全工程SUCCESS**。
- 研究ブランチのソース：`tools/g4c7_d3s26_m11_native_artist.py`、一つだけの持続可能な新ワークフロー `.github/workflows/g4c7-d3s26-native-artist-loop.yml`。
- 公式Blender `bpy 4.5.15 LTS`をGitHubランナーに導入し、**既存A72編集可能.blendの保護コピーを実際に読み込み、既存のREADING/HOUSINGの屋根頂点も直接編集**。新しい公共空間のファセット、ギャラリー面、植栽広場を作成。旧A72原本に書込みなし。
- 別名の新規 `.blend`、選択された実メッシュを含むGLB、同一Blenderシーンにある**固定8視点のCycles PNG**を実出力。原本/出力のSHA256、PNG実寸(800×450)、ファイルシグネチャをCI確認。branchへのバイナリ自動commitはなし。
- [run artifact](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41190088190)の成果物をChatに独立取得・再検査。`G4C7_D3S26_M11_NATIVE_CYCLES_EVIDENCE.zip`は取得時 **3.2MB**、ZIP SHA256 **`22b5d6b0d74e54a8f97986eafb3815daf12bc022feb9422e4498559899a846a4`**、CRC PASS。内包のGLBは**166 geometry、1,536三角形**を別Python/trimeshで読み込み成功、GLB SHA256 `94bf0196c0ede96bba01226d11446f25551ba3b15582705da2b1b7a06e4b9ffa`一致。8枚の画像もmanifestハッシュと全一致。
- 新しい編集.blend SHA256 `06e830dcd98c1e129fe3abdf28d1d7c94988cebeff48bbe6595df099616c016d`。GitHubアーティファクトに限った保存であり、PRブランチのGit管理下へ保存されたとは主張しない。

## 決定的な美術不合格
現実の8視点画像を確認。南北/斜視/地区の全景は**低い台地状建築、小規模な箱の密集、巨大な薄い面/屋根**を反復。地区の奥行・都市密度・独創的なスカイライン・巨大未来文明の美しさを欠く。

市場の眼高では大きな開口と小施設は見えるが、製造者眼高は暗い天井/壁に閉ざされ、研究・住居の眼高は暗く閉塞。市場・研究・居住・工作の実活動の視界と相互接続を評価できない。単に保存GLBがある・Cycles画像を撮れたことをART改善とするのは禁止。

**M11はCITY ART REJECT、正式採用0を維持。** 以前のA72の不採用美術を正式継承したのではない。A72はあくまでBlender技術seed。M02原本と同一編集ではなく、M02を改訂済みとは扱わない。既にこのプロジェクトでは簡単な幾何主導の候補が繰り返しART REJECTになったため、M11へ装飾・増棟・パネル追加をして延命せず、同じPython部材生成を別候補名で量産しない。

## 次に引き継ぐものと未解決
**引き継ぐ：** Chat→GitHub Actions→Blenderネイティブ編集→保存BLEND→真正8視点→GLB→独立監査→短いレビューの**実行できたパイプライン**。Blenderローカル起動・バッチの不具合に再依存しない。
**解決していない：** 視覚美術の作者媒体。コードの板やファセットが都市を決めてしまう方式は不採用。生活空間と都市全景を直接編集でき、実画像を観察しながら改善する方式が必要。GitHub Actionsの成功はアートの改善を意味しない。ユーザーによる美術採用判断が必須。

正式331人体/993足元、G0/S1/G1/G2/G3、実幅の動線・視線・負対照、Minecraft Education施工はNOT RUN。Minecraft Education施工・統合禁止、main変更なし、PR #53 Open/Draft継続。成果物ZIPはGitHubランナーのアーティファクト及びChat添付であり、GitHub git treeに登録したとは主張しない。
