# MakeCode LimitLab

Minecraft Education MakeCodeの実際の技術的限界を、安全な専用テストワールドで調査する研究プロジェクトです。対象はブロック施工・複製・更新・File Read & Write・安定性です。

**最新版：P1.9 — 1命令の `clone` を98,304→131,072ブロックへ拡張（Minecraft Education実機は未検証）。** `fill`はこれまでの実機結果を保存し、重複試験しません。

- **[P1.9 日本語の安全な実行手順](makecode/README_P19_JA.md)**
- **[P1.9 方針監査](docs/P19_DIRECTION_AUDIT_JA.md)**
- **[GitHub最新版ZIP](https://github.com/ryomashibaba/makecode-limitlab/archive/refs/heads/main.zip)**（Windowsでは `makecode/COPY_P19.cmd` を使用）
- [P1.9 MakeCodeソース](makecode/limitlab_p1_9.ts) / [P1.9 自動検証](https://github.com/ryomashibaba/makecode-limitlab/actions/workflows/verify_p19.yml)
- [測定ダッシュボード](https://ryomashibaba.github.io/makecode-limitlab/)
- 過去のソース：[P1.0](makecode/main.ts) / [P1.3](makecode/endurance_p1_3.ts) / [P1.4](makecode/limitlab_p1_4.ts) / [P1.5](makecode/limitlab_p1_5.ts) / [P1.6](makecode/limitlab_p1_6.ts) / [P1.7](makecode/limitlab_p1_7.ts) / [P1.7.1](makecode/limitlab_p1_7_1.ts) / [P1.8](makecode/limitlab_p1_8.ts)

## Minecraft Education実機で確認できた成果（2026-10-18）

| 版 | 実機結果 |
| --- | --- |
| P0.6〜P0.8 | 小規模のplace/fill/cloneがPASS |
| P1.0 | 4,096・16,384ブロックの施工、更新3方式、256KiB I/OがPASS。QUICK耐久は停止 |
| P1.3 | 24回QUICKと300回SOAKがPASS |
| P1.4 | 512ブロックのfill/cloneが各4回PASS。待機工程は106/150で手動停止 |
| P1.5 | 32,768ブロックの分割SOURCE/FILL/CLONEがすべてPASS |
| P1.6 | 65,536ブロックの分割SOURCE/FILL/CLONEがすべてPASS、単一fill/cloneも各32,768までPASS |
| P1.7 | 単一fill 32,800がNO_WRITE、単一clone 32,800がPASS |
| P1.7.1 | 安全候補の6地点探索を実装、CI PASS。修正版自身のMinecraft実機検証は未実施 |
| **P1.8** | **単一fill 32,775がNO_WRITE、単一clone 33,024・40,960・65,536が実機PASS** |
| **P1.9** | **TypeScript・Minecraft模擬・CSV判定・Windows準備のCIがPASS。実機はまだ未検証** |

**P1.9は単一clone 98,304→131,072を段階的に検証**します。最初の命令が完全一致でPASSした場合だけ次の131,072を実施し、その間にP1.9自身の複製先だけを安全な小分け操作でAIRに戻します。

2領域×131,072ブロック＋2参照キューブを事前AIR検査し、使える候補がなければ書き込みません。Minecraft側のAPI処理が停止した場合に強制キャンセルできる保証はありません。最終チャット表示は制御が戻った場合に限ります。専用の破棄可能なテストワールドでのみ実行してください。

**測定した体積・形状・環境で成功/不成功を確認できたという意味であり、Minecraft APIの普遍的な上限を断定していません。** CIの成功を実機の成功と混同せず、P1.9の結果CSVが得られるまで未検証とします。

## 安全とプライバシー

ユーザー個人のCSV、PCログ、ワールドデータ、スクリーンショットはPublic GitHubへアップロードしません。MinecraftAIBuilderその他のリポジトリやワールドは操作しません。コマンドは一度限りで、失敗時の自動再実行・無断清掃は行いません。Chat主体の開発を継続します。
