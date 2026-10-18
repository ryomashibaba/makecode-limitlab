# MakeCode LimitLab

Minecraft Education MakeCodeの施工・複製・更新・ファイルI/Oの限界を実機で調査し、**将来の巨大都市の高速生成に応用する**研究プロジェクトです。

**最新版：P2.2 — 事前計算型の高速施工エンジン。** P2.1で約31万ブロックのSOURCE施工は実機PASSしたものの、分割clone 9/36で極端に時間がかかりユーザーが停止しました。P2.2では施工命令と途中検証を再設計し、`FAST`と`VERIFY`を分離しました。**P2.2のMinecraft実機動作は未確認**です。

- **[P2.2 日本語の実行・安全ガイド](makecode/README_P22_JA.md)**
- **[P2.2 方針・計画・効率監査](docs/P22_DIRECTION_AUDIT_JA.md)**
- [P2.2 MakeCode本体](makecode/limitlab_p2_2.ts) / [P2.2 CI](https://github.com/ryomashibaba/makecode-limitlab/actions/workflows/verify_p22.yml) / [マージ済みPR #12](https://github.com/ryomashibaba/makecode-limitlab/pull/12)
- **[GitHub main最新版ZIP](https://github.com/ryomashibaba/makecode-limitlab/archive/refs/heads/main.zip)**：Windowsでは`makecode/COPY_P22.cmd`でコードをコピー
- [P2.1 日本語ガイド](makecode/README_P21_JA.md) / [P2.1 ソース](makecode/limitlab_p2_1.ts)
- [P2.0 日本語ガイド](makecode/README_P20_JA.md) / [実測ダッシュボード](https://ryomashibaba.github.io/makecode-limitlab/)
- 旧版：[P1.0](makecode/main.ts) / [P1.3](makecode/endurance_p1_3.ts) / [P1.4](makecode/limitlab_p1_4.ts) / [P1.5](makecode/limitlab_p1_5.ts) / [P1.6](makecode/limitlab_p1_6.ts) / [P1.7](makecode/limitlab_p1_7.ts) / [P1.7.1](makecode/limitlab_p1_7_1.ts) / [P1.8](makecode/limitlab_p1_8.ts) / [P1.9](makecode/limitlab_p1_9.ts)

## Minecraft Education実機の確定記録（2026-10-18）

| フェーズ | 実機結果 |
| --- | --- |
| P0.6〜P0.8 | 小規模のplace/fill/clone PASS |
| P1.0 | 4,096・16,384の施工、更新3方式、File Read & Write 256KiB成功 |
| P1.3 | QUICK24回、SOAK300回PASS |
| P1.4 | 512のfill/clone各4回PASS。待機工程は106/150で手動停止 |
| P1.5 | 32,768ブロック分割SOURCE/FILL/CLONE PASS |
| P1.6 | 65,536ブロック分割施工PASS。単一fill/clone 32,768 PASS |
| P1.7 | 単一fill 32,800はNO_WRITE、単一clone 32,800 PASS |
| P1.7.1 | 安全候補探索の修正版。単独実機未検証 |
| P1.8 | 単一fill 32,775はNO_WRITE、単一clone 65,536までPASS |
| P1.9 | 単一clone 98,304・131,072 PASS |
| **P2.0** | **単一clone 196,608・262,144まで実機全域PASS** |
| **P2.1** | **309,386ブロックのSOURCE構築・全域検証PASS、分割clone 9/36でUSER_STOP。PATCH/最終検証は未実施** |
| **P2.2** | **オフライン18件模擬＋16件CSV判定＋Windows準備PASS。Minecraft実機は未検証** |

## P2.2の高速化戦略

- P2.1と同じ**82×49×77＝309,386ブロック／領域**のモデル。素材を3Dで結合してから命令を作る。
- 既定プランの**SOURCE fillは68命令・非AIR施工体積208,010**。P2.1のSOURCE施工前記録約572件から約88%の命令削減。PATCH fillは別途1命令。
- 分割cloneを**36→2命令**へ集約。混在材質での巨大cloneは実機未検証。
- 速度重視の`labfast22`はサンプル検証のみで、**全域一致を保証しない**。
- 全域一致を調べたい場合は`labverify22`。同じ施工を行った後に、SOURCEとPATCH済みTARGETを全タイル照合する。**FASTからVERIFYへの同一ラン中の切替は不可**。
- ファイル書込みは工程の節目に限定し、永続の一回ラッチ・異常停止・終了表示を維持する。

**安全上の重要な変更：P2.2の施工前AIR検査は全域ではなく代表点のみです。** 必ず**新しく作った破棄可能なLimitLab専用ワールド**で使用してください。既存のP2.1試験ワールド、MinecraftAIBuilder、重要な建築ワールドでは実行しないでください。VERIFYでも実行前のAIR確認は限定的です。

## 実測・公開ポリシー

GitHub Actionsの模擬PASSはMinecraft実機PASSではありません。高速化率（実時間）は未計測であり、命令数削減と区別します。実測CSV・個人PCログ・ワールド・スクリーンショットはPublic GitHubへ公開しません。失敗時の自動再試行・自動清掃はしません。

開発はChat主体。Work利用を検討する場合は必ず事前に「必須／できれば使いたい／不要」と希望モデル（GPT-6.1 Sol／GPT-6 Luna／Astra）を示し、ユーザーへ相談します。
