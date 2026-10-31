# D3S26-M08 — M07 INVALID_HEADERの誤判定を修正（2026-10-31 JST）

## ユーザー実行ログ
M07_LAST_RESULT.txt に Status: INVALID_HEADER / BLENDERヘッダがありません と記録。対象パスは M03キットのM02_OUTPUT_NEW_ONLYにあるD3S26_M02_EDITABLE_AUTHOR_SCENE_20261031_171058_851631.blend。M07は先頭7バイトが `BLENDER` でなければ無条件に拒否するコードだった。

## 重要な根本原因候補
Blenderは通常の `BLENDER` 開始ファイルだけでなく、gzip `1F 8B`、Zstandard `28 B5 2F FD` で圧縮された.blendファイルを読み込める。Blender公式Gitソース `blender/tools/modules/blendfile.py` に識別実装あり。したがってM07は**正常な圧縮ファイルも誤ってINVALID_HEADERにしていた**。ただしユーザー実ファイルの先頭バイトは未取得のため、実原因が圧縮か破損かはまだ断定できない。

## M08の実装と検証
- 会話納品：`D3S26_M08_COMPRESSED_BLEND_FIX.zip`（6068 bytes、SHA256 `5526df2d50de41fb196edccc957e7d71ed2f8b05e362bc2adfabce9a7c876724`、ZIP CRC PASS、4ファイル）。
- Windows CRLF/BOMなし CMD（日本語名＋ASCII別名）、Python 3の実起動確認、pause保持。
- 既知のM03/M02出力パス優先の探索、.blend1/.blend2同一名バックアップ対応、原本・バックアップは読み取り専用でZIPへコピー。
- `BLENDER` 通常形式、gzipを展開し内部BLENDER識別、zstd識別（Python zstandardモジュール利用可なら内部も確認、未導入なら署名のみであると明記）。未知形式は元ファイルのサイズ、先頭16バイトHEX、SHA256をログへ記録。
- 出力は元.blendまたは.blend1、manifest、READMEだけを含む新規ZIP。原本の前後SHA256・mtime、不変性、ZIP SHA256、CRCを確認。
- Python構文PASS、模擬gzip-Blender収集ZIP照合PASS、無効現行.blend→有効.blend1復旧PASS、完全無効の異常系ログPASS、zstd署名認識PASS。**ユーザー実ファイルがgzip/zstdかどうか、実Blenderで開くかはNOT RUN**。

全体ART HOLD、正式採用0、331/993・G0/S1/G1/G2/G3 NOT RUN、Minecraft Education施工・統合禁止、main変更なし、PR #53 Draft/Open継続。M08 ZIP本体をGitHubにアップロードしたとは主張しない。