# D55-A2専用GitHub Actions SUCCESSと証拠境界（2026-10-29 JST）

[GitHub Actions実行 #40868614075](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/40868614075) は **completed / success**。Run HEAD `62d8a20996b246c707c61dfd7e54df4ebef1b31b`。次の実行Stepを確認した。

- `Run author section and numeric failure controls only`: SUCCESS
- `Check shared-section path interference and notch falsification`: SUCCESS
- `Preserve reproducible source and PRE-3D result`: SUCCESS
- 正常終了のartifact `g4c7-d55-pre3d-only-no-art-pass`、ID 12894719895、サイズ17,325バイトが存在（ただし30日保持の一時資料）。

### CIログに実際に残った数値

| 項目 | 本物の実行結果 |
|---|---:|
| 各候補の離散足元・体内サンプル数 | 6,777 |
| A1の共有境界との干渉 | 55（制作研究7、研究生活48、三者共有0） |
| A2の予約切り欠きを考慮した干渉 | 0 |
| A2の通路予約楕円体内の最大スコア | 0.66999 |
| 階段算術 | 120段（20/50/50） |

4種類の故意破損（上階着床不一致、入口空洞極小化、三者共有所有権除去、採光方向の一致）をすべてREJECTED。さらにA2の開口予約を取り除くとA1の干渉を再現し、**故意破損を捕まえる陰性試験の存在**を確認した。

### どこまで合格したのか

数値のPRE-3D契約と離散サンプルのA2切り欠きによる交差低減は**限定PASS**。しかし実GLB・穴の開いた三角形・人間の連続掃引・構造強度・室内生活・日照・魅力的な遠景と内観・正式G0/S1/G1/G2/G3・331/993は、すべてNOT RUN。

したがって **D55-A2を美術採用してよい証拠はない**。3つの有限な材料パッチを巨大化・フィン化して過去の失敗を繰り返さない。形状の開発は [D55-A2 SOURCE-GAP審査](./D55_A2_SOURCE_GAP_PREART_JA.md) に従い停止。続きは [D56美術先行の研究方針](../g4c7-b11-r5-d56/D56_ART_FIRST_SPATIAL_BRIEF_JA.md) を適用。

**ART HOLD／正式美術採用0／旧331・993未実行／G0/S1/G1/G2/G3 NOT RUN／Minecraft施工・都市統合禁止／main変更禁止／PR #53 Draft保持／Work事前承認。**
