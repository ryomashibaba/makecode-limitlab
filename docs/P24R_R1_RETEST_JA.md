# LimitLab — P2.4R R1 再試験（P2.3 SITE_NOT_AIR 修正版）

## 元の実機結果（2026-10-19）

G3のCSV 2件はいずれも同一SHA256のP2.3ログ。
`RUN BEGIN` → `PLAN PASS`（Fill予定157件・予定書込体積136296） → `STOP SITE_NOT_AIR_y0_x0_z0`。
**ROADS以降は0件実施。Minecraft実機建築PASSではない**。
スクリーンショットのSITE y-43..40のとおり地面内部を調査した可能性が高い。
使用済み `P23_ONCE.txt` と旧 `USER_UPLOAD_THIS_P23_STATUS.csv` は変更・削除しない。

## 2026-10-19 実機チャット構文エラー修正

ユーザーのスクリーンショットで `labarea24r` は座標 `y96..179` を正常に表示した一方、
次の `player.say` 表示文 `AIR-only sky deck Y >= 96` に対してMinecraft Education側が
`>=` を構文トークンとして扱い、赤文字の構文エラーを報告した。
これは**建築ルーチンの実行結果ではない**。画像内で `labcity24r` は未実行。

対策として問題のゲーム内表示文を `sky deck starts at Y96` に変更。
Windowsのコピー用SHA照合値も更新し、チャット表示に `<` / `>` を含まない回帰テストを追加。

**すでにこのブランチを取得しているOMENでは、新しいブランチを作り直さず、
`git pull --ff-only` の後 `RUN_P24R_R1.cmd` からコピーし直す。**
前のPowerShell監視窓は閉じてもよいが、古いP2.3/P2.4R結果や使用済みラッチは削除しない。
P2.4Rの `READY_P24R` とCSV未作成が確認できた場合にのみ再準備される。
MinecraftのCode Builderでソースを貼り替えて実行し、`labarea24r` のエラーが消えたことを先に確認する。

## 再発防止（今回実装）

- **新しいコード・チャットコマンド・CSV・ラッチ**をすべて分離：`limitlab_p24_r1.ts`、`labcity24r`、`P24R_ONCE.txt`、`USER_UPLOAD_THIS_P24R_STATUS.csv`。
- 新規結果ルート `Downloads\MakeCode_LimitLab\P24R_R1` のみ使用。P2.3の旧結果は残る。
- 開始高さは **Y = max(96, floor(現在Y)+16)**。今回のように地下から建築して空気検査に引っかかる問題を避ける。
- `labarea24r` は施工予定の **192×84×192**、浮いた試験都市のYを表示するだけ（施工しない）。
- 都市のプラン生成と75点のAIR空間検査は**一回ラッチ使用前・CSV作成前**に移動した。
- **PRECHECK BLOCKED** なら、場所を変えて `labcity24r` をもう一度呼べる（ラッチ・CSV不使用）。実際に建築処理を開始した後は再実行不可。
- 異常・使用済みラッチ・既存の新CSVを自動削除/再試行しない。
- Fill数・Clone数・都市形状をP2.3から不必要に変更しない。都市の大きな品質改善はG4へ切り離す。
- 浮遊都市はQA用の一時的な配置。最終的な自然地形への施工方法は後で設計する。

## OMENでの操作（簡潔）

現在のローカル作業に未コミット変更がないことを確認し、G3からの継続ブランチへ切り替える。

```powershell
cd "$HOME\Documents\makecode-limitlab"
git status --short
git fetch origin dev/p24r-site-preflight-recovery
git switch --track origin/dev/p24r-site-preflight-recovery
.\RUN_P24R_R1.cmd
```

その後、Minecraft Educationの**破棄可能なテストワールド**を開き、MakeCode JavaScriptを上書き貼付。File Read & Write拡張を保持し、エラー0件を確認。まず `labarea24r`、次に `labcity24r`。
**専用試験ワールドでの新規施工は事前承認済み**。保護対象の重要なワールドを選ばない。

ウィンドウが20分以内に結果を検知すると、通常は非公開ZIP
`Downloads\MakeCode_LimitLab\P24R_R1\private_results\USER_UPLOAD_THIS_P24R_*.zip`
を生成。これをChatへ共有する。完成した景観を判断するスクリーンショットがあれば添付。

結果取得までにPowerShellを閉じた場合は、実行やラッチ準備をやり直さずに
```powershell
cd "$HOME\Documents\makecode-limitlab"
python -B .\tools\p24r_capture.py
```
を実行して既存結果のみZIP化する。

**G3の失敗を消さない・再試行で記録を水増ししない・CI PASSを実機PASSとは呼ばない。**
