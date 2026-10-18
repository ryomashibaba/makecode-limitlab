# MakeCode LimitLab

Minecraft Education MakeCodeの実際の技術的限界を、破棄可能な専用テストワールドで調べる独立研究プロジェクトです。対象はブロック施工・複製・更新、ファイル入出力、安定性、実用的な大規模建築の実現性です。

**最新版：P2.1 — 汎用分割施工・clone・全域検証・部分変更（Minecraft実機未検証）。** P2.0はユーザー提供CSVで単一clone 196,608・262,144の全域ALL_PASSを確認。最大値更新から実用的な巨大建築の施工研究へ進みます。

- **[P2.1 日本語の実行手順・安全ガイド](makecode/README_P21_JA.md)**
- **[P2.1 方針・計画・効率監査](docs/P21_DIRECTION_AUDIT_JA.md)**
- [P2.1 MakeCodeソース](makecode/limitlab_p2_1.ts) / [P2.1 GitHub Actions](https://github.com/ryomashibaba/makecode-limitlab/actions/workflows/verify_p21.yml)
- **[P2.0 日本語の実行手順・安全ガイド](makecode/README_P20_JA.md)**
- **[P2.0 方針監査・次の汎用施工開発ゲート](docs/P20_DIRECTION_AUDIT_JA.md)**
- **[GitHub最新版ZIP](https://github.com/ryomashibaba/makecode-limitlab/archive/refs/heads/main.zip)** — makecode/COPY_P21.cmd でWindowsクリップボードへコピー（P2.1を含む版）
- [P2.0 MakeCodeソース](makecode/limitlab_p2_0.ts) / [P2.0 GitHub Actions](https://github.com/ryomashibaba/makecode-limitlab/actions/workflows/verify_p20.yml)
- [実測ダッシュボード](https://ryomashibaba.github.io/makecode-limitlab/)
- 過去のソース：[P1.0](makecode/main.ts) / [P1.3](makecode/endurance_p1_3.ts) / [P1.4](makecode/limitlab_p1_4.ts) / [P1.5](makecode/limitlab_p1_5.ts) / [P1.6](makecode/limitlab_p1_6.ts) / [P1.7](makecode/limitlab_p1_7.ts) / [P1.7.1](makecode/limitlab_p1_7_1.ts) / [P1.8](makecode/limitlab_p1_8.ts) / [P1.9](makecode/limitlab_p1_9.ts)

## Minecraft Education実機で確認できた結果（2026-10-18）

| 版 | 実機結果 |
| --- | --- |
| P0.6–P0.8 | 小規模のplace/fill/cloneがPASS |
| P1.0 | 4,096・16,384ブロックの施工、更新3方式、256KiBファイルI/O成功。QUICK耐久は中断 |
| P1.3 | QUICK24回＋SOAK300回PASS |
| P1.4 | 512ブロックのfill/cloneが各4回PASS。PAUSE150は106/150で手動停止 |
| P1.5 | 32,768ブロックの分割SOURCE/FILL/CLONEが全PASS |
| P1.6 | 65,536ブロックの分割SOURCE/FILL/CLONE全PASS。単一fill/clone32,768もPASS |
| P1.7 | 単一fill32,800はNO_WRITE、単一clone32,800は全域PASS |
| P1.7.1 | 施工候補を6地点へ分散した安全検査の修正。単独の実機再試験は未実施 |
| P1.8 | 単一fill32,775はNO_WRITE、単一clone33,024・40,960・65,536全PASS |
| **P1.9** | **単一clone 98,304・131,072がMinecraft実機で全域PASS** |
| **P2.0** | **ユーザー提供CSVで単一clone196,608・262,144の全域PASS、最終ALL_PASSを確認。個人CSVは非公開** |
| **P2.1** | **開発・オフライン検証段階。Minecraft実機は未検証** |

P2.0は64×64×64のコピー元と複製先（各262,144ブロック）を専用テストワールドで全域AIR検査します。コピー元を4,096ブロック以下の小分けfillで作り、単一cloneの196,608が全域一致した場合だけ262,144へ進みます。最初の試験では**指定した範囲の外側16層がAIRのまま**かも監査します。

MinecraftのAPI自体が固まった場合、スクリプトからの強制キャンセルや終了チャット表示は保証できません。結果が得られた場合だけ実機PASSと呼び、特定形状の成功をAPIの普遍的な上限とは断言しません。

## 安全・公開方針

個人の実測CSV・PCローカルログ・ワールドデータ・スクリーンショットはPublic GitHubへ公開しません。MinecraftAIBuilderなどほかのプロジェクトや重要ワールドには触れません。実験は1回限り、失敗後の自動再実行・自動消去はしません。

開発はChat主体、Work利用は事前相談。今回のP2.1はユーザー了承のもとで開発します。P2.1は82×49×77の建築を小分け施工し、36回の分割cloneと16³の部分変更を全域検証します。全域AIR検査・失敗時停止・永続一回記録・CSV読戻し・終了チャットを備えます。Minecraft実機成功とは主張しません。
