# MakeCode LimitLab P2.0 — 単一clone 196,608 → 262,144の境界調査

## 実機で確認済みの記録

- P1.6：単一fill・clone各32,768ブロックPASS、分割施工65,536ブロックPASS。
- P1.7：単一fill32,800ブロックNO_WRITE、単一clone32,800ブロックPASS。
- P1.8：単一fill32,775ブロックNO_WRITE、単一clone65,536ブロックまでPASS。
- P1.9：単一clone **98,304と131,072ブロックが全域一致でPASS**。
- **P2.0はMinecraft Education実機未検証。** GitHub CIを通過しても実機結果とは別です。

P2.0は未測定の**196,608 → 262,144ブロック**を段階的に検証。131,072以下の単一clone成功試験は繰り返さず、fill境界研究は別テーマとして維持します。

## 実験の流れ

| 段階 | 操作・寸法 | ブロック数 | 条件 |
| --- | --- | ---: | --- |
| 事前安全検査 | 64³のコピー元・64³の複製先とAIR/GOLD基準 | 524,288＋1,024 | 最大6候補を全域AIR検査 |
| コピー元作成 | GOLD 64×64×64 | 262,144 | 一命令4,096のfill×64。512タイル照合 |
| 一命令clone 1 | 64×48×64 | **196,608** | 全域一致＋対象外の上部16層がAIRか検証 |
| 複製先の初期化 | 自分で書いた48層のみ | 196,608 | clone 1完全PASSのときだけ小分けAIR fill×48 |
| 一命令clone 2 | 64×64×64 | **262,144** | 再検査後に一度だけ実行、512タイル照合 |

**最初の196,608ブロック試験で拒否・部分施工・不一致・返り値の矛盾があれば262,144へ進みません。** 成功時にのみ自分が作った複製先をリセットします。ソースは残し、終了時の自動清掃や失敗後の自動再試行はしません。

## 安全性

**破棄可能なLimitLab専用Minecraft Educationテストワールドでのみ使用**。コピー元・複製先は合計最大524,288ブロック、GOLD参照キューブが512ブロック。重要な建築物やMinecraftAIBuilderのワールドで実行しないでください。

- X/Z方向へ分散した6候補について、書込み前にコピー元・複製先・2つの参照領域すべてをAIRで照合。使えない場所はCSVに理由を記録して回避し、全候補が不適ならSTOP。
- コピー元は一命令4,096以下の安全なfillを使用。単一fill 262,144ブロックは試しません。
- clone返り値と全512ブロックタイルの一致を両方確認。指定領域外の変化や部分施工も別に記録。
- 途中のloops.pause(1)は停止チェック用。実時間が1msという意味ではありません。
- 巨大なMinecraft API命令がハングした場合、コードによる強制キャンセルや終了チャット通知は保証できません。未読み込み領域の実機挙動にも制約があり、事前AIR検査も完全な安全保証ではありません。

## Windows + Minecraftでの実機操作

1. [GitHub mainのZIP](https://github.com/ryomashibaba/makecode-limitlab/archive/refs/heads/main.zip)を解凍。
2. makecode/COPY_P20.cmd をダブルクリックして **COPY OK** を確認（失敗時はPASTE_THIS_P20.tsの内容を手動コピー）。
3. Minecraft Education MakeCodeのJavaScript欄を Ctrl+A → Ctrl+V で貼替え、**File Read & Write拡張機能**を維持。エラー0件で再生する。
4. **破棄可能な専用テストワールド**のチャットで **labauto20 を1回だけ**入力する。
5. **TEST FINISHED / TEST STOPPED** の終了メッセージが出たら Downloads\MakeCode_LimitLab\results\USER_UPLOAD_THIS_P20_STATUS.csv をアップロードする。

補助コマンド：labstatus20（工程と理由）、labreport20（最終結果の再表示のみ）、labstop20（協調停止）、labplan20（説明表示のみ）。どれも再施工しません。

成功時の想定表示（これは実測ではありません）：

    LimitLab P2.0 ========== TEST FINISHED ==========
    LimitLab P2.0 Result ALL_PASS: 262144_single_clone_verified_not_universal_maximum
    LimitLab P2.0 Verified one-call clone at least 262144 blocks
    LimitLab P2.0 Send USER_UPLOAD_THIS_P20_STATUS.csv

## 継続方針

P1.0〜P1.9のソースを保持し、個人のCSVやローカルログを公開GitHubにアップロードしません。単純なブロック数拡張だけが研究目的ではないため、P2.0の実機結果後は汎用の巨大建築・分割施工・検証・部分修正エンジンの研究へ移る判断をします。

[方針監査の全文](../docs/P20_DIRECTION_AUDIT_JA.md)
