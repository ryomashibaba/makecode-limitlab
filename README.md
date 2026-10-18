# MakeCode LimitLab

Minecraft Education MakeCodeの施工・動的更新・ファイル入出力・安定性の技術的限界を、専用テストワールドで調べる独立研究プロジェクトです。

**最新版：P1.5 — 32,768ブロック分割施工研究（実機確認待ち）。** 長時間待機実験を本筋から切り離して、実際の建築能力を調査します。

- **[P1.5 日本語の実行・安全ガイド](makecode/README_P15_JA.md)**
- **[最新版ダウンロード（GitHub ZIP）](https://github.com/ryomashibaba/makecode-limitlab/archive/refs/heads/main.zip)**
- **[P1.5 MakeCodeソース](makecode/limitlab_p1_5.ts)**
- **[P1.5 GitHub Actions](https://github.com/ryomashibaba/makecode-limitlab/actions/workflows/verify_p15.yml)**
- **[既存の計測ダッシュボード](https://ryomashibaba.github.io/makecode-limitlab/)**
- **[既存のP1.0コード](makecode/main.ts)** / **[P1.3](makecode/endurance_p1_3.ts)** / **[P1.4](makecode/limitlab_p1_4.ts)**
- **[Cloud Chat開発・安全上の引き継ぎ](CLOUD_CHAT_HANDOFF.md)**

## 実機で確かめたこと（2026-10-18時点）

| 段階 | 実機で確定できたこと | 備考 |
| --- | --- | --- |
| P0.6〜P0.8 | place/fill/clone各種の小規模試験PASS | CSVで確認 |
| P1.0 | 4,096/16,384ブロック施工、更新3方式、最大256KiBの入出力がPASS | 耐久QUICKは長時間化し USER_STOP、全工程PASSではない |
| P1.3 | 24回QUICK・300回SOAKがPASS | 独立診断 |
| P1.4 | 512ブロックのfill/cloneを各4回PASS | PAUSE150を106/150で手動停止、長時間化の原因未特定 |
| **P1.5** | **GitHub CIによる検証PASS** | **32,768ブロックのMinecraft実機施工は未実施** |

**P1.5が検証するのは「32,768ブロックを小分けにして構築・複製できるか」です。1命令で32,768個を処理できると主張するものではありません。** 安全な空き領域確認が成功した場合、コピー元・fill先・clone先の最大計98,304ブロックを書き換えます。施工は専用の破棄可能なテストワールド限定です。

P1.5での実機所要時間は不明です。Minecraftの実行環境は極端に遅くなることがあるため、見積時間を保証しません。異常時には `labstatus15`・`labstop15` を使用し、失敗後の無条件再実行は避けてください。

## 公開・プライバシー

実際のユーザーCSV、ローカルログ、ワールド、スクリーンショットはリポジトリに公開しません。`tests/fixture_p*.csv` は合成データです。ダッシュボードへのCSV取込みはブラウザ内で処理し、自動送信しません。

既存のMinecraftAIBuilder等の他プロジェクトには触れません。開発はChat主体、Workは事前許可がある場合のみ。
