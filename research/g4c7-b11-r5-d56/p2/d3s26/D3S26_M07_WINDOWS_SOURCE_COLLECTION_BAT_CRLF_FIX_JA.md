# G4-C7 / D3S26-M07 — Windows原本収集キットの起動不具合修正（2026-10-31 JST）

ユーザーよりM06の「M06_原本を自動収集.batを実行すると開いてすぐ閉じた」と報告。元M06 BAT原本を実バイト検査し、改行が**LFのみ（CRLF 0行、LF 18行）**であることを確認。この書式はWindows CMD上での不具合原因となる可能性はあるが、実機ログ不在のため因果関係は断定しない。ほかの可能性（Python起動失敗、ZIP内からの部分実行など）もある。

修正版ZIP「D3S26_M07_WINDOWS_FIX.zip」を新規作成。5ファイル/5682 bytes、ZIP CRC PASS、SHA256: `dbfc52a9818caa242f4a858dd9eddc884e88145117348a08040391167104c319`。元M06キットは無改変。

**修正内容**
- Windowsの.cmd/.batを**CRLF改行・ASCIIコマンド・BOMなし**に統一。
- `M07_ここをダブルクリック.cmd`（同等のASCII名 `RUN_M07.cmd` も同梱）から `cmd /K` でコンソールを維持。子ランナーに`pause`も保持。
- Pythonランチャー `py -3` の実動作を検査し、不可なら `python` の実動作をチェック。失敗時メッセージを消さない。
- 対象M02.blendを15秒以内で自動探索し、未発見の場合はファイル選択ダイアログを試行。選択不可/エラー時は`M07_OUTPUT_NEW_ONLY/M07_LAST_RESULT.txt`を保存する。
- 原本を読み取り専用に扱い、前後SHA256とmtime・ZIP内容のSHA256/CRCを確認。出力は新規ZIPのみ、原本上書きなし。
- python AST/py_compile PASS。**模擬BLENDERヘッダー付きファイル**を用いた収集→ZIP→再読込→不変性検査PASS。ヘッダー不正の負の検査でERRORログと非ゼロ終了を確認。

**未検証:** ユーザーWindows実機、実M02原本の取得、実Blenderでのシーン編集、ART改善、正式331/993安全QA。これらをPASSとは報告しない。今回のZIPは会話添付のみであり、GitHubにバイナリ保存済みと主張しない。

前回までの正規境界：全体ART HOLD、正式採用0、Minecraft Education施工/都市統合禁止、PR #53 Draft/Open維持、main変更禁止、append-only研究記録。
