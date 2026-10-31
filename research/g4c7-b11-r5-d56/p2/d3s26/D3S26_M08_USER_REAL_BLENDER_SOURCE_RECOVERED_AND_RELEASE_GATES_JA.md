# G4-C7 D3S26 — M08実機原本復旧確認と以後の不具合防止ゲート
2026-10-31 JST

## 実際に確認した成果
ユーザー提出 `M08_NATIVE_BLEND_HANDOFF_a3df137b2028_20261031T092514600189Z.zip` と `M08_LAST_RESULT.txt` を独立検証。M08ログは `SUCCESS`、形式 `BLENDER_ZSTD`、M03原本SHA一致を報告。

収集ZIP: **154,819 bytes**, SHA256 `b37c1027d1ebdaaf462e4160a5114f018b9ffbf3bd7792d970df67ee262409cd`。3ファイル、ZIP CRC PASS。
ネイティブ `.blend`: **154,282 bytes**, SHA256 **`a3df137b20287b9a3bef0b7fc121ea46ed7e091c8cb6ed9d7452ffa281d9678b`**（M03保存.blend記録と完全一致）。先頭Zstandard識別子 `28 B5 2F FD`。Chat実行環境にて`zstd`で実際に展開：**1,427,436 bytes**、Blender形式ヘッダー `BLENDER17-01v0502` を確認。別途Blenderアプリを用いた `.blend` 完全ロード・視覚審査は未実施。原本は保存・展開・検査を通じ改変していない。GitHubにはこのテキスト報告のみ追加（バイナリ原本は会話添付）。

## 修正原因
M07はファイルの先頭7バイトが `BLENDER` に一致することだけを要求していたため、実ユーザーファイルの**正常なZstandard圧縮形式**を `INVALID_HEADER` と誤判定した。M08の改善でこの形式が収集可能になり、元M03 SHAも一致した。今回の観測でこの原因が確定した。

## 今後の配布前QA（同じバグと手戻りを避ける）
- 正常: 通常のBLENDER、gzip、Zstandardを識別。実バイトまたはサイズ/ハッシュ付き再現用fixtureで処理。
- 異常: 無効ヘッダー、破損圧縮、入力ファイル不在、誤選択、SHA不一致、バックアップ変種、空白を含むWindowsパス。手順の成功判定とログが一致すること。
- Windowsバッチは**CRLF/BOMなし**で用意し、失敗時に画面が閉じずエラー・終了コード・ログを記録。実Windowsで未実行の場合は明示する。
- 実ユーザー原本の読み取り専用、上書き禁止、既存証拠append-only、CRCとSHAの照合を必須にする。
- テストPASSは対象の範囲のみ表示し、静的PASSを実Blender動作PASSやART PASSへ読み替えない。過剰な回収キットや技術デモを増殖させず、次は**実3D美術制作**を優先する。

## 次の実制作ゲート
実際に取得済みの編集可能M02 `.blend` の保護コピーをBlenderで開き、主形状・公共街路・実室・研究/製造の視界と南北遠景を**同じシーンで直接再制作**。固定8視点で編集前後を比較し、作品そのものの魅力を判断する。従来の自動box/slab/棚・薄殻を再量産しない。現Chat環境にBlender本体はなく、現時点でこの直接編集はNOT RUN。

**正式状態:** 全体ART HOLD、正式美術採用0、331/993正規QA・G0/S1/G1/G2/G3 NOT RUN、Minecraft Education施工・既存都市統合禁止。main変更なし、PR #53はDraft/Open継続。
