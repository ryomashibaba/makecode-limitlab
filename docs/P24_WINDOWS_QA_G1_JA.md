# P2.4 G1 — Windows QA read-only observer

## 役割と最重要制限

既存P2.3を**書き換えず**、OMEN 1台のWindows上で実機CSVを確認する補助ツールです。
Minecraft起動・MakeCode貼付・建築開始・クリップボード操作・ラッチ作成や削除・CSV変更は**一切しません**。
新規のMinecraft施工には引き続きユーザー承認が必要です。失敗時の自動再試行は禁止です。

G1はWindows QAの一部であり、**ワンクリック準備（G2）は未実装**です。

## 使い方

すでにGitHubリポジトリをローカルに置いている場合、PowerShellを開きます。

```powershell
cd "$HOME\Documents\makecode-limitlab"
python tools\qa_p24.py inspect
```

これは既存ファイルを調べるだけです。P23の使用済みラッチも変更しません。
検査表示は `HISTORICAL_INSPECTION_NOT_NEW_RUN` と明示され、過去の成功CSVを今回の新しい成功と偽りません。

**承認済みの新しいMinecraft実機試験を始める前**に次を起動すると、CSVの変化を監視できます。

```powershell
python tools\qa_p24.py watch
```

既定で2秒おきに最大15分確認します。画面操作を奪いません。
監視開始時点に存在したCSVは過去の記録とみなし、その**後に変化し、続く2回の読み取りで安定したCSV**だけを判定します。
`FAST_COMPLETED_SAMPLED_NOT_EXACT` は「サンプル確認済み・全域完全一致未証明」で、完走したときも形状の美しさは別途目視確認します。
`STOPPED` も正常に検出し、繰り返し施工は指示しません。
`WATCH_TIMEOUT` は新しい安定した終了CSVが得られなかった意味で、Minecraft試験完了を意味しません。

**重要：** この監視ツール自身は建築開始を承認せず、Minecraftへ入力も行いません。監視中のCSVが別のプロセスから更新されたときは、その内容を読み取って報告するだけです。

結果とログは標準出力（PowerShellの画面）のみで、GitHubに自動送信されません。
必要なレポートだけユーザーが選んでChatに共有します。作業フォルダーは既定で
`%USERPROFILE%\Downloads\MakeCode_LimitLab` を参照します。
場所が異なる場合は `--output-root "D:\path\to\MakeCode_LimitLab"` で変更できます（参照のみ）。

## 安全条件

- P2.3のソースはGit blob SHA `5bd354d31f5b42797f95a04afc70b1f022e95ad3` で読み取り専用検証します。
- ソース不一致は `SOURCE_MISMATCH` と報告し、コピー・貼付はしません。
- `READY_P23` と `USED_P23` を区別し、使用済みラッチは必ず維持します。
- CSVの形式・工程・回数・完走判定は既存の厳格な `tools/analyze_p23.py` を再利用します。
- 観測用IDはログの紐付け用で、ゲームの新しい実行許可やラッチ解除には**なりません**。
- P2.3実機未実施の状態は、このツールのCI成功だけでは変わりません。

## 次の工程

G2で安全なワンクリック準備を検討しますが、`COPY_P23.ps1 -PrepareOnly` はラッチを作り得るため読み取り専用処理へ混ぜません。
既存コードや使用済みラッチを触らず、G3で実機試験、G4で都市品質・汎用設計へ進みます。
