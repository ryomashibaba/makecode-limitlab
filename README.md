# MakeCode LimitLab

Minecraft Education MakeCodeの施工・動的更新・ファイル入出力・安定性の技術的限界を、独立した専用テストワールドで実測する研究プロジェクトです。

**最新版：P1.6 — 65,536ブロックの分割施工・複製と、任意の単一命令限界探索。** 長時間の耐久ループは含めません。

- **[P1.6 日本語セットアップ・安全ガイド](makecode/README_P16_JA.md)**
- [P1.6 実行用ソース](makecode/limitlab_p1_6.ts) ／ [Windowsコピー補助](makecode/COPY_P16.cmd)
- [P1.6 自動検証](https://github.com/ryomashibaba/makecode-limitlab/actions/workflows/verify_p16.yml)
- [GitHub最新版ZIP](https://github.com/ryomashibaba/makecode-limitlab/archive/refs/heads/main.zip)
- [結果ダッシュボード](https://ryomashibaba.github.io/makecode-limitlab/)
- 旧版：[P1.0](makecode/main.ts) ／ [P1.3](makecode/endurance_p1_3.ts) ／ [P1.4](makecode/limitlab_p1_4.ts) ／ [P1.5](makecode/limitlab_p1_5.ts)

## 実機で確かめられた成果

| 版 | 実機検証結果 |
|---|---|
| P0.6–P0.8 | 小規模のplace/fill/cloneが成功 |
| P1.0 | 4,096・16,384ブロック施工、更新3方式、256KiB I/O成功。QUICK耐久は手動停止 |
| P1.3 | 独立24回＋300回の耐久試験に成功 |
| P1.4 | 512ブロックfill/clone各4回PASS。待機中心の試験は106/150で手動停止 |
| **P1.5** | **32,768ブロックの分割SOURCE/FILL/CLONEが全PASS（計98,304ブロックを検証）** |
| **P1.6** | **TypeScript・Minecraft模擬14ケース・Python 9ケース・Windows CI成功。実機はまだ未検証** |

P1.6の標準試験は16×64×64の施工元・fill先・clone先の3領域に合計最大196,608ブロックを書き換えます。施工前に**全領域が空気か**を検査し、空いていなければ施工しません。

`labauto16` は **65,536ブロックを分割施工できるか**を検証するもので、1回のfillやcloneで65,536個を操作したという意味ではありません。`labprobe16` は主試験が成功した後の**任意**の追加試験で、4,096〜32,768ブロックまで単一命令で試し、結果を全域照合します。単一命令65,536ブロックの呼び出しは実装していません。

完走時間は保証できません。協調停止`labstop16`はありますが、Minecraft側の長いAPI呼び出し中に即時停止できる保証はありません。いずれも破棄可能なLimitLab専用テストワールドだけで実行してください。失敗後の無条件再実行や自動削除はしません。

## 開発と公開について

GitHubはPublic。実際のユーザーCSV、ワールド、ログなどはリポジトリに公開しません。ウェブ画面でのCSV読込みもブラウザー内のみです。

他のMinecraftAIBuilder等のリポジトリやワールドには触れません。開発はChat主体とし、Work利用は事前に相談します。
