# MakeCode LimitLab

Minecraft Education MakeCodeの施工・動的更新・ファイル入出力・安定性の技術的限界を、専用テストワールドで実測する研究プロジェクトです。

**最新版：P1.8 — fillとcloneの単一命令境界を独立に調査（Minecraft実機は未検証）。** P1.7実機で観測したfill/cloneの違いを、重複実験を減らして追跡します。

- **[P1.8 日本語の実行・安全ガイド](makecode/README_P18_JA.md)**
- **[P1.8 方針ぶれ・計画・効率の監査](docs/P18_DIRECTION_AUDIT_JA.md)**
- **[GitHub最新版ZIP](https://github.com/ryomashibaba/makecode-limitlab/archive/refs/heads/main.zip)**：makecode/COPY_P18.cmdで1回コピー
- [P1.8 MakeCode本体](makecode/limitlab_p1_8.ts) / [P1.8 GitHub Actions](https://github.com/ryomashibaba/makecode-limitlab/actions/workflows/verify_p18.yml)
- [実測ダッシュボード](https://ryomashibaba.github.io/makecode-limitlab/)
- 旧版：[P1.0](makecode/main.ts) / [P1.3](makecode/endurance_p1_3.ts) / [P1.4](makecode/limitlab_p1_4.ts) / [P1.5](makecode/limitlab_p1_5.ts) / [P1.6](makecode/limitlab_p1_6.ts) / [P1.7](makecode/limitlab_p1_7.ts) / [P1.7.1](makecode/limitlab_p1_7_1.ts)

## Minecraft Educationで確認できた実機結果（2026-10-18）

| 版 | 観測できた成果 |
| --- | --- |
| P0.6–P0.8 | 小規模のplace/fill/cloneがPASS |
| P1.0 | 4,096・16,384ブロック施工、更新3方式、256KiB I/OがPASS。耐久QUICKは手動停止 |
| P1.3 | 24回QUICK＋300回SOAKの耐久試験PASS |
| P1.4 | fill/clone 512ブロック各4試行PASS。待機工程は106/150で手動停止 |
| P1.5 | 32,768ブロックの分割SOURCE/FILL/CLONEが全PASS |
| P1.6 | 65,536ブロックの分割SOURCE/FILL/CLONEが全PASS。単一fill/clone各32,768ブロックも8/8 PASS |
| **P1.7** | **単一fill 32,800ブロックはNO_WRITE、単一clone 32,800ブロックは全域PASS。33,024は未実施** |
| P1.7.1 | 六地点の安全検査を実装。GitHub CIはPASS、Minecraft実機で修正版は未検証 |
| **P1.8** | **GitHub CIはPASS、Minecraft実機は未検証** |

P1.8の新たな一命令テストは **fill 32,775（23×25×57）、clone 33,024 → 40,960 → 65,536**。fill結果によらずcloneを独立実施し、cloneの途中で失敗したら無条件に繰り返さず終了します。32,768や32,800の既存試験を繰り返しません。

書込み元・先の3領域と二つの参照領域を空気で事前検査し、X/Zに離れた6候補から一つを選びます。スクリプトの制御が戻ればMinecraftチャットに **TEST FINISHED / TEST STOPPED** を表示し、**labreport18** で後から再確認できます。Minecraft自体が長時間止まった場合の強制停止や完了通知は保証できません。

**重要：** 今回の結果からAPIの真の絶対上限を断定することはできません。形状・チャンク・ワールド環境も影響する可能性があります。Minecraft実機で未確認の試験をPASSと呼びません。

## 安全性と公開方針

Publicリポジトリへユーザー個人のCSV・ローカルログ・スクリーンショット・ワールドデータは公開しません。MinecraftAIBuilderなど他のプロジェクトには触れません。実験は破棄可能な専用ワールドのみ。自動削除や停止後の自動再試行はしません。

開発はChat主体。Workの利用をユーザーに強要せず、承認なしに切り替えません。
