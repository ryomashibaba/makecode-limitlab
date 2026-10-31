# G4-C7 / D3S26-M15C — GitHub Actionsのみで直接Blender室内実制作、8視点実画像で美術不採用
**2026-11-01 JST / 研究ブランチのみ / ART HOLD・正式採用0**

## 目的とユーザー負担
M15の第三者Blender MCP導入・ZIP展開・ローカルCodex設定を当面保留した。ユーザーに一切Windows操作を依頼せず、**Chat→既存GitHubコネクタ→GitHub ActionsのBlender→証拠取得→Chatによる実画像審査**という一連の作業を実際に完了。M15Cでは都市の巨大外殻や反復塔の量産をやめ、一つの公共建築室内（市場/工房/アトリウム庭園/上階研究ギャラリー/住居アプローチ）に実際の空間要素を組み込んだ。**ただしGUIを直接操作したわけではなく、Blender APIを用いたコードによる作者指定形状作成である**。ユーザーの操作回数は0。

## 真正Blender実行と取得した原本
- [run #41253780068](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41253780068) は**全ステップSUCCESS**。事前構文検査、公式Blender bpy 4.5.15 LTS導入、ネイティブシーン編集保存、Cycles8視点撮影、GLB出力、独立画像・ファイルSHA検証、Actions artifact保存を実行。
- 実装commit `7f7823f964de7ab6b8cd17df5d29668176baca2b`、ソース `tools/g4c7_d3s26_m15c_occupied_interior.py`、workflow `.github/workflows/g4c7-d3s26-m15c-interior.yml`。
- Actions artifact #13062002761 を会話に取得。ZIP `D3S26_M15C_NATIVE_INTERIOR_EVIDENCE.zip` **4,673,906 bytes**、SHA256 `ad0f2d4db84ce9c703e430c86296de709e92a4c9afece78739f677a38c3a00a0`、CRC PASS、11ファイル（.blend 1 / GLB 1 / PNG 8 / manifest 1）。
- 真正編集可能 `M15C_EDITABLE_PUBLIC_INTERIOR.blend` SHA256 `4b17686607764fbfcddd54e32b132c2a8bea04f21a5c46ae0ff7525955bc9132`。保存GLB `M15C_PUBLIC_INTERIOR_NOT_ART_APPROVED.glb` SHA256 `66edfd04a7a5901cf7bf59d6802a593c36b1dab616a91ca47cd7d16326e8b2ad`。全8 PNG 960×540、manifest SHAと独立照合PASS。
- GLBをChat側で独立trimeshで再読込し **126 mesh geometry nodes / 3,994 triangle faces**。命名された40個の `TRUE_STAIR_1_TREAD_01..20` と `TRUE_STAIR_2_TREAD_01..20` が実メッシュとして存在。市場・製造室床・研究ギャラリー床・接続ブリッジ・住居側床のオブジェクトも確認。**正式人体衝突/支持/開口幅/手摺/頭上/実歩行経路は未検査**。GLB座標系はBlenderとは軸が異なるため、GLBのY-up boundsをBlenderのZ高さと混同しない。
- 8視点Cycles本物の画像からコンタクトシート `D3S26_M15C_8_VIEW_CYCLES_REVIEW.jpg` を生成しChatに保存。この画像は画像生成AIやVTK代用ではない。
- ZIPと写真はGitHub Actions artifactおよびChat添付。**研究ブランチのGit treeに巨大バイナリをcommitしたとは主張しない**。

## 実画像を見た批判的判定
南北/斜視/地区では公共庭園・工房・研究階段が以前より読めるものの、**大きな暗色の箱壁と薄い屋根板・まばらな活動オブジェクトが主役**で、未来文明の独創的建築/都市の一体感や厚い生活空間は成立しない。
- street_eye: 中央の植栽と空間に明るさがあり、眼高構成をある程度評価できる。
- maker_eye: 上方の大きな面と壁が視界を遮る。仕事場の居場所・目的地・抜けの表現が弱い。
- research_eye: 眼前に大きな壁とバルコニー縁があり、研究者の眺め・外界との関係が乏しい。
- resident_eye: 白い大床面と樹冠が支配し、居住空間と公共空間の分離・住居入口が読み取れない。
- 追加問題: Stair踏板は40個あるが、構造支持、階段の連続的な利用可能性、足元衝突は未証明。3Dカメラでは全体が単純な中規模キャンパスに見える。より高い屋根や細い照明を足す「装飾だけの改善」で解決しない。

**結論：M15CはTECH PASS、CITY ART REJECT。完成美術採用0。** この案の外形を延命しない。M11〜M14と同様に単純なコード主導の外形制作が本質的な壁であることをさらに確認した。

## 次回以降の方針
- **ユーザー操作0を原則維持**。追加のZIPダウンロード/コマンド/ローカルプラグイン導入はまず依頼しない。必要性が本当に確定した場合のみ理由と最小限操作を相談する。
- 今回のBlender CIは有効な技術的パイプライン。だがループそのものはまだ「GUIを直接観察して手で美術を編集する」方式ではない。これを同一視しない。
- 次は同じ形式のPythonによる箱・外殻候補を追加で量産しない。可視編集を実際に制御する方法がなければ、芸術的進捗を偽らず、必要な接続機能を明確にして止める。別プロジェクトHALO-9の10km級ルールをLimitLabに持ち込まない。
- 正式331人体/993足元・G0/S1/G1/G2/G3はNOT RUN、ART HOLD、正式採用0、Minecraft Education施工/都市統合禁止。main編集・merge・force pushなし。PR #53 Open/Draft継続。
