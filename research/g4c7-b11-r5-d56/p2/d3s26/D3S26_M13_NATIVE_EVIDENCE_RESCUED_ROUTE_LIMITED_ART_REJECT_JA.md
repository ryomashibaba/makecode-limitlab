# D3S26-M13 — CI二段階バグの特定と真正Blender原本の回収、限定的動線検査、ART REJECT
**2026-10-31 JST／正式採用0／全体ART HOLD／Minecraft Education施工・都市統合禁止**

## 1. 実行事実
- [初回GitHub Actions run #41194570915](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41194570915) = FAILURE。公式bpy導入とソースpreflight成功後、行184の `'M13_CROSS_STREET_AWNING_%02'%i` による `ValueError: incomplete format`。制作/撮影未実施。
- 研究ブランチ上の既存workflowのソース復旧段階で、**元envelope（13,427 bytes、SHA256 9c42fcd5b50b3917e26fa69c2b94289d0a9a3e379dd17f5cf71b3db73bdfd45e）を保全したまま**該当文字列を `%02d` に修正。ASTの文字列書式検査を追加。修正commit `e9fd84a006527d605f9281d72bc3271350b41350`。
- [修正後GitHub Actions run #41199223120](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41199223120) は**ジョブ全体FAILURE**だが、公式Blender 4.5.15の実シーン制作、編集可能.blend、真正GLB、8視点のCycles画像生成を**すべて実施**。最後に行247 `a.update(...)` で `AttributeError: 'str' object has no attribute 'update'` を発生。製作中に同名変数 `a` が文字列に上書きされた可能性が高いが、当該変数代入の履歴をここでは確証していない。**manifest出力・本来のGitHub内正規readback QA・CIでの可読ソース追加は未実施**。
- workflowの `if: always()` artifact archiveは成功。保護ブランチにバイナリは書かれていない。

## 2. 実データ回収と独立検査
- GitHubアーティファクト #13041718108 を会話に取得：`G4C7_D3S26_M13_NATIVE_EVIDENCE_PARTIAL.zip`、4,195,954 bytes、SHA256 `82d8aa876c280d422392921184de0603aae49f02121ba866fc63c0cbe46eb1b7`、ZIP CRC PASS。**10 files** = native .blend 1、GLB 1、PNG 8。オリジナルmanifestなし。
- 編集可能ネイティブ .blend **1,609,855 bytes**、SHA256 `0950a2bb166e5db302ca100638e3aab7764ca702babd842aae193e2417d6b319`。Chat側で完全なBlender再オープンまではNOT RUN、ただしCI内でのBlender保存は実施。
- GLB SHA256 `5211a8509324ab8e5a0e6c60571d9066b262ba74e7b795cb0390b0edcda4cdfb`。独立 `trimesh` による保存GLB再読込 **174 geometry / 2,018 triangles**。PNGは8枚・全て実900×540、独立デコーダで8/8成功、SHAを別のJSONに保存。
- 36のメッシュ名 `M13_TRUE_STAIR1_TREAD_01..18` / `M13_TRUE_STAIR2_TREAD_01..18` が存在し、GLBの実ワールド座標で各階段の段差 **0.30**、踏面横幅 **5.5**、奥行 **0.75**。第1フライト上端高さ0.3–5.4、第2フライト5.7–10.8。
- 階段→踊り場→研究橋→研究床、踊り場→第二階段→踊り場→住居橋→住居床は、独立した**外接箱の水平投影・境界隣接**では接続・連続候補を持つ。ただし外接箱は実歩行の証明ではない。完全な幅方向の衝突・人体・足元支持・開口・頭上・手摺の正規QAは**NOT RUN**。ソースの平坦経路808/808点は設計上の限定チェックに留まる。公式G0/S1/G1/G2/G3、331人体/993足元は NOT RUN。
- 実画像は `M13_8VIEW_CYCLES_CONTACT.jpg` としてChatに整理。GitHubに実画像やバイナリをgit commitしたとは主張しない。

## 3. 美術評価と進退
市場通りから奥の階段、製造空間の通り抜け、研究・居住への上下動線の**視覚的理解は、M12の離散した高層彫刻案より改善**した。ただし最終8視点の全景は**約4棟の単純箱型低層施設、薄板の屋根、黒く開いた足元・床裏**が主役。約10km級の独創的な未来文明都市の美しさ／密度／遠景／人が住み続ける建築厚みは成立しない。**M13のCITY ART = REJECT。正式採用0。** ユーザーの最終美術承認ではなく助手の厳格な暫定評価。

**今後の開発順序**は「使える連続公共動線→実開口→居室・製造/研究の活動と採光→都市全体を決める非反復の建築形状」を維持する。ただしM13の低層箱形キャンパスを装飾・増築して延命しない。M11・M12の高層彫刻への逆戻りもしない。

## 4. 再発防止と次の実装
- 次の本番作業前に `a.update` の短命ループ変数衝突を、独立した `audit_manifest` 名の辞書として修正する。元の回収済みsource envelopeと本制作原本は必ず保護。
- **書式・変数名衝突等、コード実行でのみ判明するエラーを早期に検出**する短いヘッドレススモークテストを本レンダリングより前に配置。実装・実行未確認のものをPASSと報告しない。
- M13は視覚的不合格であり、CIを緑色にする目的だけで8枚を再レンダリングしない。今回のGitHub artifactと独立監査が技術検査の代替証拠であるが、正規CI PASSではないことを明記する。
- mainの変更なし、PR #53 Draft/Open維持、正式採用0、Minecraft Education施工/統合禁止。
