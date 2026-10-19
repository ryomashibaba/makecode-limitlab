# MakeCode LimitLab — P2.4S R2：CSV誤判定を避ける独立再試験

## 2026-10-19 実機で確認できたこと

- P2.4Rのチャット表示エラー（`>=`）は解消。
- `labarea24r` は正常表示。高さ範囲 Y=96..179。
- `labcity24r` は設計を開始し、`PRECHECK AIR site base y96` まで進んだ。
- その後 `PREVIOUS_CSV_PRESERVE` で停止。**建築処理を開始した証拠はない**。
- 以前のCSVが実在するか、`file.readFile` の欠損ファイルに対する戻り値が原因かは、スクリーンショットからは不明。Minecraft Education公式は欠損ファイルの戻り値を明記していない。

## 根本的な対応

1. `file.readFile(CSV)!=""` を**ファイルの存在判定に利用しない**。
2. PowerShellが毎回UTC時刻＋UUIDで新しい出力フォルダーを発行し、そのフォルダーが存在しないことをチェックしてから作成する。
3. 固有の新しい`READY_P24S`ラッチと固有CSVパスをコンパイル済みMakeCodeコードへ埋め込む。各試験のコードは別の出力フォルダーを使用する。
4. P2.3/P2.4Rの既存CSV・ラッチ・GitHubを削除/上書き/解除しない。G1〜G3の仕様も保持。
5. ゲーム内での75点AIR検査は引き続きラッチ消費前。検査失敗時のみ、安全位置へ移動して同じ新Runでやり直せる。
6. 実際の施工を開始したら同じRunでは再実行しない。結果ZIPは非公開で保存する。
7. 都市生成の幾何データは前版と同じ（192×192、8棟、中央広場、計157 fill＋5 clone予定）。品質調整は景観確認後に実施。

## OMENの最短操作

Minecraft Educationの既存ワールドを破棄する必要はない。ただし施工は**破棄可能なLimitLab専用試験ワールド**に限定する。

PowerShellで、既存ブランチの未コミット変更を確認してから：

```powershell
cd "$HOME\Documents\makecode-limitlab"
git status --short
git fetch origin dev/p24s-r2-unique-run-output
git switch --track origin/dev/p24s-r2-unique-run-output
.\RUN_P24S_R2.cmd
```

起動スクリプトが `COPY OK` を表示したら、Minecraft Educationで `C` → MakeCode → JavaScript を開き、
**古いコードを `Ctrl+A` で選択し、新しいコードを `Ctrl+V` で貼る**。File Read & Write拡張があることと、エラー0件を確認してから再生ボタンを押す。

次の順番でチャット入力：
1. `labarea24s`（表示のみ）
2. `labcity24s`（破棄可能ワールドなら事前承認済み、一回実行）

**P2.4Rの`labcity24r`は使わない**。古いCode Builderコードのまま操作しない。

CMDは新規結果CSVを最大20分監視し、完了・停止時に
`Downloads\MakeCode_LimitLab\P24S_R2\runs\<固有RunID>\private_results\USER_UPLOAD_THIS_P24S_....zip`
を作る。このZIPと、都市全体が分かるスクリーンショットがあればこのチャットに添付する。

20分経過・PowerShellを閉じた場合でも**施工はやり直さない**。結果の回収だけを行う場合は、最初のCMDに表示された`Private output:`のパスを使用して

```powershell
python -B .\tools\p24s_capture.py --output-root "Private outputに表示された実際のパス"
```

を実行する。このコードは正しい実パスに変更する。**上書き防止のため毎回新しいRunIDが生成される**ので、`RUN_P24S_R2.cmd` の再起動は「証拠の再回収」ではない。過去Runを消さない。

## 品質の範囲

Linux/Windows CI PASS、オフラインボクセルシミュレーションPASSは**Minecraft実機PASSではない**。`FAST_COMPLETED_SAMPLED_NOT_EXACT`も全ブロック一致を保証しない。完成した建築の視覚品質は現物の画像と実機操作で判断する。
