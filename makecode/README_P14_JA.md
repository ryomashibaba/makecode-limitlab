# MakeCode LimitLab P1.4 — Reliable Endurance / Measured Bulk Benchmark

## 目的と現状

P1.0：4,096/16,384ブロックの `fill` / `clone`、高速更新3方式、256KiB入出力は実機PASS。一方、`ENDURANCE_QUICK` が長時間完了せず、`labstop1`により `STOPPED USER_STOP` となった。原因は未特定。P1.3：24回QUICK + 300回SOAK30は実機PASS。

P1.4は**P1.0の大規模施工をやり直さず**、「待機だけ」「小さいブロック更新とファイル処理」「256KiB読み書き後」の条件を別々に調べる。あわせて512ブロックで `fill` / `clone` を交互に4回ずつ比較し、結果のファイル時刻マーカーを保存する。**マーカー間隔は真のAPI呼出し時間ではなく、ファイル書込や実行スケジューリングを含む概算値**である。

GitHubリポジトリ：<https://github.com/ryomashibaba/makecode-limitlab>（Public）。ユーザーの実測CSV・PC固有のパスはGitHubに登録しない。既存のP1.0・P1.3コードは変更しない。

## あなたの操作（Minecraft内は1コマンド）

1. **新規の何も大切なものがないテストワールド**、またはこれまでのLimitLab専用ワールドを使う。`MinecraftAIBuilder`など他のワールドでは実行しない。
2. `makecode/COPY_P14.cmd`をダブルクリック。`COPY OK`と出た場合だけMakeCodeのJavaScript欄へ `Ctrl+A` → `Ctrl+V`。File Read & Write拡張機能を維持する。
3. エディターのエラーが0件なら緑の再生ボタンを押し、チャットに **`labauto14`** を一度だけ入力する。
4. `LimitLab P1.4 ALL PASS status CSV ready` が出たら、`Downloads\MakeCode_LimitLab\results\USER_UPLOAD_THIS_P14_STATUS.csv` をChatGPTに送る。問題が出たら **再実行しない**。同じCSVか画像を送る。

### 状態確認・停止

- `labstatus14`：現在の段階、カウント、理由を表示する。
- `labstop14`：協調的な停止要求。即時停止は保証しないが、各段階のチェック位置で停止する。
- `labplan14`：**完全読み取り専用**。32,768 / 65,536ブロック向け幾何学的分割案だけ表示する。大規模施工を実行するコマンドは**実装していない**。

P1.4の標準試験は `loops.pause(100)`を360回（要求待機時間の合計36秒）含み、さらに施工・ファイル処理・検査時間が加わる。実時間の上限は不明。進捗CSVは25回ごとに更新される。長時間 `labstatus14` が同じ位置ならそのログを報告してほしい。

## 自動で行われること

- 空の参照領域512ブロックを全件検査し、さらに**書換え対象の8×8×8領域5つ全部**がAIRであることを比較。最大4つの候補位置を調べ、空いている場合だけ施工開始。対象外ブロックは変更しない。途中で失敗した場合も自動削除は行わない。
- `fill`と`clone`：512ブロック×各4回（A/B/B/Aに相当する交互の実行順）。コピー元の1024ブロックを全数照合し、施工後も`testForBlocks(All)`で全域一致を確認する。各試行の開始/終了は専用ログフォルダにマーカーとして記録する。
- `PAUSE150`：軽い計算+150回の100ms待機。
- `MIXED150`：小さなブロック変更+読み書き+軽い計算+150回の100ms待機。
- `IO_256K`：262,144文字を書いて読み戻し、全文照合する。
- `POSTIO60`：大容量読み書き後に60回の複合処理を実行する。
- 各段階の `BEGIN`・`PROGRESS`・`PASS`・`STOP` を**単一の状態CSV**へ更新保存。

## 出力先

`Downloads\MakeCode_LimitLab\logs` にマーカーと入出力テストデータ、`results` に状態CSV。ダウンロード直下に大量のTXTを散らかさない。個人のログを外部送信する機構はない。

## 任意のローカル分析

研究者向け。Pythonが入っている場合：

```
python tools/analyze_p14.py "%USERPROFILE%\Downloads\MakeCode_LimitLab"
python tools/plan_volume.py 16 32 64
python tools/plan_volume.py 16 64 64
```

時刻マーカーの比較結果は `results\P14_MARKER_INTERVALS_ESTIMATES.csv` に書き出せる。これは**ファイル時刻による近似**であり、短い呼び出しの精密な速度を示さない。外部時計が提供されない以上、`clone`が何倍速いかを正確な数字で断定しない。

## 検証レベル

- TypeScript 5.8.3とMinecraft APIスタブによる静的チェック：PASS（実際のMakeCodeコンパイルではない）。
- Node.jsオフラインMinecraft模擬10ケース：PASS。
- Pythonツールのユニットテスト5件：PASS。
- Windows PowerShellの準備処理はGitHub ActionsのWindowsランナーで検証予定。クリップボードの対話操作は実際のWindowsで最終確認が必要。
- **P1.4のMinecraft Education実機動作：未検証。**

## 変更しない基本方針

1. クラウドプロジェクト内のChatで開発。WorkはChatより明らかに効率が高い／Work以外でできない場合のみクラウドWorkを使い、ローカルWorkは基本使わない。
2. ユーザーの手元作業はコードの少量コピペと、稀な実機確認のみ。今回のチャットではWorkを使わない。
3. 既存のMinecraftAIBuilderやP1.0・P1.3のプログラム、ワールドを破壊しない。
4. 多工程一括開発しつつ、段階ごとの安全検査を省かない。
5. 32,768ブロック以上の施工は**P1.4で実行せずHOLD**。幾何学的分割の計画のみ用意し、実機準備が整ってから実装する。
