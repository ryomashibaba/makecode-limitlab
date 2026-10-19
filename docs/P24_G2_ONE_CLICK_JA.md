# MakeCode LimitLab P2.4 G2 — OMENワンクリック準備

**これはP2.3のMinecraft実機PASS報告ではありません。** G2はWindows上の試験準備を少ない操作へまとめた機能です。

## 目的

OMEN MAX 16のWindows 1台・Chat主体・Work原則不要の方針を継続します。
G1の読み取り専用CSV監視を使い、P2.3のコード照合・MakeCode用コードコピー・未使用ラッチ確認・CSV監視を、1つのCMD起動でまとめます。

施工、ワールド削除、既存ラッチ初期化、失敗時再実行、GitHubへの個人データ送信は**自動では行いません**。

## 初回セットアップ

GitHubのブランチ `dev/p24-g2-oneclick-preflight` をOMENの既存ローカルリポジトリへ取り込みます。G2のPRはG1の上に積まれた差分で、マージ前にmainへ移した前提では実行しないでください。

既存作業を上書きしないよう `git status` を先に確認してください。別の未コミット作業がある場合は無理に切り替えないでください。

```powershell
cd "$HOME\Documents\makecode-limitlab"
git status
git fetch origin dev/p24-g2-oneclick-preflight
git switch --track origin/dev/p24-g2-oneclick-preflight
```

すでにローカルに同名ブランチがあれば、`git switch dev/p24-g2-oneclick-preflight` で切り替えてから適切にpullしてください。**gitの競合は自動上書きしません。**

## G2を使う手順

1. まだ**新規のP2.3実機試験を実施する承認がない場合は**準備・確認だけに留め、Minecraftで `labcity23` を送信しません。
2. プロジェクト直下の `RUN_P24_G2.cmd` をダブルクリックします。
3. `PREPARED` と表示された場合、検証済みのP2.3ソースがクリップボードに入ります。
4. **破棄可能な専用ワールド**のMinecraft EducationでMakeCodeのJavaScriptに貼り付け、File Read & Write拡張を保持してエラー0件を確認します。
5. `labarea23` で施工予定領域を表示して、安全を目視確認します。
6. **別途、新規施工を承認した場合に限り** `labcity23` を一度だけ実行します。
7. Windows側はCSVの変化を最大15分確認し、既存G1ロジックで `STOPPED` / `FAST_COMPLETED_SAMPLED_NOT_EXACT` / `INCOMPLETE` を区別します。完走と景観の良さは別の評価です。

Minecraftでの実行は **貼り付け・場所確認・1回の施工** が必要です。G2だけで完全自動化するわけではありません。

## 使用済みラッチ、既存CSV、ソース不一致の場合

`RUN_P24_G2.cmd` は安全に中断します。
- `P23_ONCE.txt` が `USED_P23`：**使用済みなので絶対にリセットしない**
- `USER_UPLOAD_THIS_P23_STATUS.csv` が存在：**過去結果として保護。勝手に上書きしない**
- ラッチが不明/壊れている、参照先がリンク、ソースハッシュ不一致：**準備を拒否**

これらの状態が見つかった場合、新規の安全な試験環境・新Run ID・人間の許可に基づく独立した計画が必要です。G2にはそのための自動解除機能はありません。

## 読み取り専用の確認だけをする場合

PowerShellで下記を実行します。このモードはラッチやCSV、クリップボードを更新しません。

```powershell
powershell.exe -NoProfile -STA -ExecutionPolicy Bypass -File .\tools\P24_G2_ONE_CLICK.ps1 -Mode Inspect
```

結果ファイルのルートは既定で `%USERPROFILE%\Downloads\MakeCode_LimitLab` です。
G1/G2の検証済みMakeCodeソースはP2.3と同じです。新規P2.4施工コードは**まだ実装していません**。

## 制約・残課題

- MakeCodeの貼り付け、Code Builderの操作、Minecraftコマンド入力は手動です。
- G2準備後にMinecraftを閉じたりCSV更新が15分以内に起きなくても、G2は再実行・自動施工しません。
- G2のGitHub CIはローカルのWindows GUIやMinecraft実機の代わりにはなりません。
- G2はP2.3施工の前に安全なワールドの選択や地形・既存建築の全域保証を**行えません**。
- `README_JA.md` は古いP1.1原典なので、P2.3以降についてはこの文書と最新版READMEを優先します。
- G3でP2.3実機、次のG4で道路/建物/広場/パレットの汎用化を進めます。QAツール開発で都市研究を止めません。
