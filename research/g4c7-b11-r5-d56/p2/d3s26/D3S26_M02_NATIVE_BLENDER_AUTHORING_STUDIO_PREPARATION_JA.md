# G4-C7 / D3S26-M02 — Blender直接編集スタジオ準備・検証記録

**実施日:** 2026-10-31 JST  
**確定判定:** AUTHORING TOOLING STATIC PASS / BLENDER RUNTIME NOT RUN / CITY ART HOLD / 正式採用0件  
**施工:** Minecraft Education への書込み0・既存都市への統合禁止継続

## 決定の理由
D3S26-A01は実店舗入口の限定検査0/11、先細りの塔/箱の量産でART REJECT。M01は店舗や階段等の局所TECHは改善したが、都市の造形が低層キャンパスへ回帰しCITY ART REJECT。**これ以上同じ部材自動配置で都市候補を生成しない。** 人間の活動・街路・視界と主形状を**Blender画面で直接編集する制作媒体**に切り替える。M02は*媒体の準備段階*であり、新都市案のART合否ではない。

## 実際に作成した成果物
会話添付 `D3S26_M02_VISUAL_AUTHORING_STUDIO.zip` の6ファイル:
- `M01_REFERENCE_ONLY.glb`: M01の基準モデル（過去ART REJECT）、参照専用。元GLBのSHA256 `f15e5e7d845e00a774a0f43db22dec6f8ed59e7cdcdab1b42b9b321bf8f79c5a` 照合済み。
- `M02_SPACE_CONTRACT.json`: 店頭、製造者、来訪者、研究観察者、ギャラリー、住民の6活動アンカー/公共活動ストーリー/絶対QAと禁止境界。
- `M02_make_studio.py`: Blender 5.xのネイティブ作者シーン構築用スクリプト。参考M01を選択不可の別コレクションに隔離。市民活動アンカー、未検証の公共ストーリーボード曲線、**頂点をBlender Edit Modeで直接動かせる**非破壊サブディビジョン付き曲面制御メッシュ3枚（製造/研究/住民）と固定8カメラ（南・北・斜視・地区・街路・製造者・研究者・住民）を構成する。Blenderから**新規ファイル名**で .blend 保存する設計。未完成形状はART採用としない。
- `M02_START_WINDOWS.bat`: WindowsのBlender 5.xを使うワンクリック起動補助。既存プロジェクトを上書きしない。
- `M02_INDEPENDENT_STATIC_AUDIT.json` と `README_JA.txt`。

## 現環境で実施した検証
- Python 3.13によるスクリプトAST構文検査PASS。
- M01実GLB原本SHA一致。
- 編集制御メッシュにおける全52三角形（20 + 16 + 16）を別Python計算で確認。ゼロ面積三角形0、編集頂点数48（18 + 15 + 15）。これは**Blender内部でサブディビジョン後のメッシュを評価したわけではない**。
- ZIP 17,679 bytes、CRC PASS、SHA256 `c7edf328c0db8e8bdb3211eb7a915b77d5b5add5e1129aaa776b829e31e243e5`。
- Blender本体がChat実行環境に存在しないため、**Blender内実行、.blendファイル実生成、固定カメラレンダリングはNOT RUN**。コードを作っただけで「直接編集成功」「都市美術改善」としない。

## 次の実行ゲート
1. ZIP展開後、Blender 5.xインストール済みのWindowsで `M02_START_WINDOWS.bat` を実行。初回 .blend生成・エラーの有無を確認。
2. Blender画面で3つの主形状メッシュを直接動かし、市民眼高と南北遠景を**同じ保存 .blend**から比較する。美術失敗なら主形状を延命せず作者方式を再検討する。
3. 実開口・経路幅・製造/研究視線・上下移動は**保存GLBの独立再読込**で限定QAし、正規331人体/993足元、G0/S1/G1/G2/G3は独立条件を満たすまでNOT RUNとする。
4. 最終Minecraft Education施工はMakeCodeのみ。現時点の施工禁止は解除しない。

**GitHub保存範囲:** このテキスト記録のみ。ZIP/GLB/BLEND/PNGをGitHubへ保存済みとは主張しない。Draft PR #53 / 既存研究 / main は保護。
