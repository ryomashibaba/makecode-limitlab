# D34 原本復元・真正GLB再検証
このフォルダーの `d34_source_part1.b64` と `d34_source_part2.b64` を **この順番に連結**すると、Brotli 圧縮されたPython作者生成器・独立GLB監査の可逆アーカイブになる。

- 結合後のASCII長さ: `7532`
- 結合後のSHA256: `7bd15bb49d5681c774fde1e48e91da79b97fcf7dd3bfd1391dcbec6336266ab1`
- 形式: Base64(Brotli(4バイトの生成器長 + AST整形されたPython生成器 + 独立監査Python))
- アーカイブに含まれる生成器: `d34_civic_section.py`
- 独立監査: `d34_independent_audit.py`
- これらのAST整形版をローカルで実行し、元の保存GLB3件とJSON2件のSHA256が**すべて完全一致**することを確認済み。

専用ワークフローは圧縮ソースを復元して、3ケースの真正GLBを再生成・再読込した6視点をレンダリングし、独立保存GLB監査を実行する。

**D34: PRE-G0 ART REJECT。美術採用0／正式G0 S1 G1 G2 G3 NOT_RUN／Minecraft Education施工・都市統合禁止。** CI SUCCESSは美術や安全の合格ではない。