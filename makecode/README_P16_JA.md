# MakeCode LimitLab P1.6 — 65,536ブロック分割施工 + 任意の単一命令限界探索

## 現在地（2026-10-18）

- **P1.5：Minecraft Education実機で32,768ブロックの分割 `fill`・`clone` と正確性検証がALL PASS。** 元構造物も含めて、計98,304ブロックを作成。送付されたCSVの最終行 `RUN,1,1,PASS,32768_SOURCE_FILL_CLONE_EXACT` に基づく。
- P1.0：16,384ブロック施工・256KiB I/O・更新試験PASS。一部耐久工程は長時間化し中断。
- P1.3：24回+300回の独立耐久PASS。
- P1.4：512ブロック×各4回施工PASS。PAUSE150を106/150で手動停止、原因は未確定。
- **P1.6：コード・オフラインCIで検証中。Minecraft実機PASSはまだ未確認。**

## 目的

極端に遅くなった耐久ループを本筋から切り離し、実際の **分割施工能力** と **一回のAPI命令の処理上限** を混同せず検証する。自動削除・勝手な再実行・他プロジェクトへの操作は実装しない。

### 第一段階（標準）: `labauto16`

1. 3つの施工領域（元構造物、fill先、clone先）を空気比較で完全に事前確認。**各65,536ブロック**、合計196,608ブロック。空気基準キューブ3つ（計1,536ブロック）も個別確認。最大3つの配置候補を試し、すべて空いていなければ変更せず停止。
2. 元構造物：16×64×64ブロックを、**1命令1,024ブロック**の`fill`×64回で建設。8×8×8基準パターン512ブロックを全数確認し、元構造物128タイルも比較検証。
3. fill先：同じ構造を**1命令1,024ブロック×64回**で施工。元構造物と128タイルの正確性照合。
4. clone先：**1命令4,096ブロック×16回**でコピー。元構造物と128タイルの正確性照合。
5. `USER_UPLOAD_THIS_P16_STATUS.csv`に段階ごとのBEGIN・途中経過・PASS/STOPを保存。待機による長時間耐久試験は無し。`loops.pause(1)`は停止要求に応答するための短いチェックポイントであり、**1msで実際に処理が終わるという保証はありません**。

**重要：** この段階で65536ブロックを一命令で施工したとは言えません。分割施工の実機対応規模を確かめます。

### 第二段階（任意）: `labprobe16`

**第一段階が全てPASSし、同じMakeCode実行セッションのままのときだけ**実行できます。今すぐ実行する必要はありません。

P1.6自身が作った`fill`先・`clone`先だけを追加のテスト用に上書きします。単一の `blocks.fill` / `blocks.clone` で、**4,096 → 8,192 → 16,384 → 32,768** ブロックを段階的に試します。

- `fill`：施工先を一度STONEにリセットしてから、段階ごとの重複しない領域へ**各1命令**でGOLDを配置。事前に検証したGOLD基準タイルと全数比較。
- `clone`：クローン先の各試験領域をAIRに戻してから、コピー元の同じ領域を**各1命令**で復元し、完全一致を確認。
- 途中で拒否・不一致が起きたら記録して終了。失敗した試験を自動再試行せず、次の大きさへ進まない。**32,768ブロックより大きな1命令は行いません。**
- **一度の命令に対するTRUE上限の「最大値」は推定しません。** 例えば32,768で成功しても、それ以上の命令を試していないため、下限の証明に留まります。

任意試験はP1.6の施工先を一部上書きし、失敗時に自動復旧・削除をしません。元構造物は変更しません。Minecraft APIのブロック操作がハングした場合、内部から強制キャンセルできる保証もありません。

## ユーザー操作（第一段階の実機検証時だけ）

1. [GitHub最新版ZIP](https://github.com/ryomashibaba/makecode-limitlab/archive/refs/heads/main.zip)を解凍。`makecode/COPY_P16.cmd`をダブルクリックする。今回の限定ZIPを使う場合はその`makecode`フォルダでもよい。
2. `COPY OK`を確認したらMakeCodeのJavaScriptを `Ctrl+A` → `Ctrl+V`で置き換える。既存の **File Read & Write** 拡張機能を保持する。
3. エディターでエラー0件を確認し、プレイ。**破棄可能なLimitLab専用テストワールド**にて **`labauto16` を一度だけ入力**する。
4. `ALL MAIN PASS` と表示されたら、`Downloads\MakeCode_LimitLab\results\USER_UPLOAD_THIS_P16_STATUS.csv` をチャットにアップロードする。
5. 止まる・進捗が変わらない場合は、`labstatus16`で確認し`labstop16`で協調停止を要求。**施工の再実行はしない**。停滞したらCSVまたは画像を送る。

`COPY OK`が出ない場合、同じフォルダに生成された`PASTE_THIS_P16.ts`をエディターで開いて全文コピーできる。コード全文のSHA256照合と、ファイル・クリップボード読戻しチェックを実装済み。

コマンド：

- `labauto16`：標準65,536ブロック分割施工。
- `labstatus16`：現在の処理と進捗をチャット表示。
- `labstop16`：協調停止要求。重いMinecraft API処理の実行中は即時停止できない可能性あり。
- `labprobe16`：標準成功後の任意1命令上限探索（追加の変更あり）。
- `labplan16`：読み取り専用で分割・命令サイズ案を表示。

## 検証方法

ローカルのプログラムチェック（Minecraft実機ではない）：

```sh
tsc --target es5 --module none --lib es5 --skipLibCheck --outFile build/limitlab_p1_6.js tests/makecode_p16_stub.d.ts makecode/limitlab_p1_6.ts
node tests/test_p16.js
python -m unittest discover -s tests -p test_p16_tools.py -v
python tools/analyze_p16.py /path/to/USER_UPLOAD_THIS_P16_STATUS.csv
```

GitHub ActionsではLinuxのTypeScript+Minecraft APIスタブ・模擬操作試験・CSV解析・P1.0ソースSHA保全に加え、Windows PowerShell 5.1の`-PrepareOnly`と構文チェックを実施する。**これらのPASSはMinecraft実機PASSを意味しない。**

## 安全・開発方針

- MinecraftAIBuilder等の既存ワールドやGitHubリポジトリは操作しない。
- P1.0〜P1.5の実績・ソース・結果は保持する。
- Public GitHubへユーザーの実測CSVやPC固有のログを公開しない。
- 元のワールド内のブロックを消したり、試験に失敗したとき自動で再実行する機能はない。
- Chat主体で作業し、Workへ移す場合は事前のユーザー承認が必要。
