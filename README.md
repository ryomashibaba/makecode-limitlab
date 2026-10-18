# MakeCode LimitLab

Minecraft Education MakeCodeの施工・動的更新・ファイル入出力・安定性の技術的限界を、専用テストワールドで実測する独立研究プロジェクトです。

**最新版：P1.7.1 — 施工場所の探索修正版（Minecraft実機は未検証）。** P1.7での単一命令境界結果を維持し、空き候補をX/Zに分散させ、不合格理由をCSVへ記録する改良版です。

- **[P1.7.1 安全候補の探索改善と実機結果](makecode/README_P171_JA.md)**
- [P1.7元版の手順・実験仕様](makecode/README_P17_JA.md)
- **[GitHub最新版ZIP](https://github.com/ryomashibaba/makecode-limitlab/archive/refs/heads/main.zip)** （必要な場合は`makecode/COPY_P171.cmd`からコピー）
- [P1.7.1 MakeCodeソース](makecode/limitlab_p1_7_1.ts) / [P1.7.1 CI](https://github.com/ryomashibaba/makecode-limitlab/actions/workflows/verify_p171.yml)
- [P1.7実機で使った元ソース](makecode/limitlab_p1_7.ts)
- [結果ダッシュボード](https://ryomashibaba.github.io/makecode-limitlab/)
- 旧版：[P1.0](makecode/main.ts) / [P1.3](makecode/endurance_p1_3.ts) / [P1.4](makecode/limitlab_p1_4.ts) / [P1.5](makecode/limitlab_p1_5.ts) / [P1.6](makecode/limitlab_p1_6.ts)

## Minecraft Education実機で確かめられた成果（2026-10-18）

| 版 | 実機検証結果 |
| --- | --- |
| P0.6–P0.8 | 小規模のplace/fill/cloneがPASS |
| P1.0 | 4,096・16,384ブロック施工、更新3方式、256KiB I/OがPASS。QUICK耐久は手動停止 |
| P1.3 | 独立24回＋300回の耐久試験PASS |
| P1.4 | 512ブロックfill/clone各4回PASS。待機工程は106/150で手動停止 |
| P1.5 | 32,768ブロックの分割SOURCE/FILL/CLONEすべてPASS |
| **P1.6** | **65,536ブロックの分割SOURCE/FILL/CLONEすべてPASS。単一fill/clone各32,768ブロックも8/8実機PASS** |
| **P1.7** | **実機：単一fill 32,800ブロックはNO_WRITE、単一clone 32,800ブロックはPASS。33,024未実施** |
| **P1.7.1** | **探索候補をX/Zに6地点へ分散し、理由を記録。GitHub CIはPASS、実機未検証** |

P1.7では **32,800（20×40×41）ブロックの単一fillがNO_WRITE、単一cloneがPASS** しました。**33,024（24×32×43）ブロックは未実施**です。P1.7.1は同じ試験機能を維持し、安全な空き領域候補を6地点に拡大します。容量が拒否されても、APIから処理が戻ってくれば`TEST FINISHED`と診断結果をMinecraftチャットに表示します。安全停止時は`TEST STOPPED`です。

初期施工はコピー元・fill先・clone先の各最大41,280ブロックを**すべて空気か検査**してから開始。計最大123,840ブロックの領域に対応します。再試行や終了後の自動削除はありません。

**注意：** 32,769ブロックぴったりは実施せず、コンパクトな直方体で調べるため32,800を第一段階に採用しています。失敗したサイズをもって、Minecraft APIの絶対上限を断言しません。Minecraftの実行スレッドがハングした場合、チャットの終了表示も保証できません。`labstatus17` / `labstop17` で状態を確認してください。

## 公開・安全

ユーザーの実測CSV、スクリーンショット、ワールドデータ、PCローカルログはPublic GitHubへアップロードしません。MinecraftAIBuilderや他ワールドへの変更はありません。開発はChat主体です。
