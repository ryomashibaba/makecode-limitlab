# MakeCode LimitLab P1.8 — fillとcloneの独立境界調査

## 実機で確定済みの出発点

P1.6：分割SOURCE/FILL/CLONE 65,536ブロック全PASS。単一fill / clone各32,768ブロックまでPASS。

P1.7：単一fill **32,800ブロックはLIMIT/NO_WRITE**、単一clone **32,800ブロックはPASS**。33,024は未実施。

P1.7.1は施工場所の選択肢と診断を改善した修正版で、既に取得したP1.7の実機結果を再計測する必要はありません。P1.4で問題になった長時間待機の耐久ループも追加しません。

**目的：fillとcloneの上限を独立に探る。単一の形状に対する失敗を、Minecraft APIの普遍的な最大値と断定しない。**

## 1回の実機操作で調べること

| API | 1命令のブロック数 | 寸法 | 開始条件 |
| --- | ---: | --- | --- |
| fill | **32,775** | 23×25×57 | ソース構築PASS後、1回だけ |
| clone | **33,024** | 24×32×43 | fillの結果と独立に実行 |
| clone | **40,960** | 32×32×40 | 33,024成功後 |
| clone | **65,536** | 32×32×64 | 40,960成功後 |

fill 32,775はP1.6の32,768とP1.7の32,800の間のサイズです。32,769ぴったりは細長い直方体を要求するため、チャンク負荷を抑える目的で**23×25×57の32,775**を使用。32,768や32,800のテストは繰り返しません。fillが失敗してもcloneは独立に続行します。

## 安全条件

**破棄可能なLimitLab専用テストワールドでのみ実行**してください。既存のMinecraftAIBuilder、他プロジェクトのワールド、重要な建築物がある場所では使わないでください。

- 最大書換え候補：GOLDソース32×32×64＝**65,536ブロック**、fill先23×25×57＝**32,775ブロック**、clone先32×32×64＝**65,536ブロック**。加えて基準キューブ8³が2つ。
- 施工前に**全3領域と両参照領域がAIRかチェック**。X/Z両方向へ離した6候補を検証。ひとつでも不一致ならその候補を使わず、CSVへ不合格理由を記録します。
- cloneの次サイズへ進む際は、**P1.8自身が書いたclone先だけ**を1024ブロック以下の小分けでAIRへ戻し、空気検証とソースの再検証を行います。これは次の実験のための初期化であり、失敗時の自動片づけはしません。
- 大きな1命令が失敗・拒否・部分施工となった場合、**同じ命令を自動再試行せず、それより大きなcloneへ進まない**。
- fillとcloneの施工結果は、全領域を最大8×8×8のタイルに分けて基準GOLDとの全域一致で比較。失敗はNO_WRITEとPARTIAL_OR_UNEXPECTED_BLOCKS、返り値の異常を区別。
- 停止要求に応答するのは短いloops.pause(1)チェックポイントのみ。API自身が止まった場合、時間制限や即時停止、終了メッセージは保証できません。施工物の自動削除はありません。
- **P1.8のMinecraft実機動作は未確認**。GitHub CIのPASSと実機PASSを混同しないでください。

## 操作（Minecraftチャットは1コマンド）

1. [GitHub mainのZIP](https://github.com/ryomashibaba/makecode-limitlab/archive/refs/heads/main.zip)を解凍し、makecode/COPY_P18.cmdをダブルクリックします。COPY OKを確認。失敗時には同じフォルダのPASTE_THIS_P18.tsからコピーします。
2. Minecraft EducationのMakeCode JavaScript欄にCtrl+A → Ctrl+Vで貼り付け、File Read & Write拡張機能を保持、エラー0件で再生します。
3. **破棄可能なLimitLab専用テストワールド**で、チャットに **labauto18** を1回だけ入力します。成功・LIMIT観測・安全停止の各終了時に目立つ通知を表示します。
4. TEST FINISHED / TEST STOPPEDが出たら、Downloads\MakeCode_LimitLab\results\USER_UPLOAD_THIS_P18_STATUS.csv をこの会話へ送ってください。

チャットの終了表示例（これは**想定例**であり実測ではありません）：

    LimitLab P1.8 ========== TEST FINISHED ==========
    LimitLab P1.8 Result LIMIT_OBSERVED: fill_NO_WRITE_clone_confirmed_65536
    LimitLab P1.8 Fill32775 NO_WRITE CloneBest 65536
    LimitLab P1.8 Send USER_UPLOAD_THIS_P18_STATUS.csv

コマンド：labstatus18（工程と進捗）、labstop18（協調停止）、labreport18（結果再表示のみ・再施工なし）、labplan18（読み取り専用）。

## 継続する開発方針

P1.0〜P1.7.1のソースはすべて保存。ユーザーの実測CSVやPC固有のログをPublic GitHubに公開しません。オフライン模擬試験はMinecraft Education実機の結果に代用しません。ユーザーのWindows操作回数を減らし、成果が出た試験を繰り返さない方針を維持します。

[方針監査と継続開発の判断](../docs/P18_DIRECTION_AUDIT_JA.md)
