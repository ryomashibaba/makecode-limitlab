# M37-P2｜ネイティブBlender 3視点実レンダリング — ART REJECT

2026-11-03 JST。**実Cycles 3視点に直接目を通した独立美術判定。**
本ファイルは架空のプレビューではなく、GitHub Actions実行 #41471988900 の保存artifactとレポート`P2_NATIVE_PAIRED_THREE_VIEW_REPORT.json`を根拠とする。

## 証拠と完成状態の区別

- [技術CI #41471988900 SUCCESS](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41471988900)
- [証拠ZIP (GitHub Actions artifact)](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41471988900#artifacts) — `g4c7-p2-paired-native-true-three-views-tech-only-not-art`。撮影日2026-11-02 UTC。原本は一つのネイティブ保存済み`.blend`、SHA256 `2ee1f2592084e75b041c8e1bc36fb9fd5e73581b1959caf42f8658d759f8a456`。
- AERIAL／PUBLIC_EYE／HABITAT_EYEの**実際のCycles PNG各1枚、計3枚**（各900×560）。カメラ位置はプログラムの自動仮フレームであり、作者正式承認0。
- 保存済みBlenderシーンの2メッシュはいずれも**8頂点・6面**。`city_macro`・`habitat`各1。再読込とレンダリングは本当に成功。ただし視認できるのは**互いに離れた単純な直方体2つ**と灰色背景だけ。
- **ART REJECT**：都市の連続した密度0、製造設備0、見学者と職員の物理隔壁0、研究文化0、住居入口・前室・居間・街並みが見える窓0。遠景でも人の目線でも住まいの実体がない。
- 技術CIでの`SUCCESS`は保存・再読み込み・実Cyclesレンダリングの証拠だけ。**美術作品の採用0、正式ART審査PASSED 0**。旧O1/P1の不採用条件に該当するため、作品としての継続利用不可。

## この結果から固定する次の制作判断

1. 4つの許可済み操作を単純なplane seedへ適用するだけでは、自動的に空間の意味・詳細・密度は生まれない。1回のTool Callと2つの直方体でART要件を満たすと見なさない。
2. **この短いペア編集命令モデルを、実都市の自動建築作業として無制限に繰り返さない**。モデル試行の発展は「実画面を見て補正する作者によるBlender編集」方式へ切り替えるまでART HOLD。
3. GitHubの初心者用`tools/g4c7_m37p2_run_native_operator_first_pair.ps1`の通常実行にART-FIRSTガードを追加：`-ExplicitTechOnly`がない実行はOllamaへの送信・Blender起動の前に安全停止する。`tools/G4C7_P2_Native_Operator_Trial_Start.cmd`もその新しい固定コミットを参照。**ユーザーに再実行を要求しない。**
4. GitHub CIによるWindows `-PrepareOnly`確認、実機AIによる新モードの外観評価は本証拠からは未確認とする。

## 制約・保存

一つの代表住戸と街全景を**同一真正Blender原本**で直接編集する方針は不変。無制限の外部MCPやLLM Python任意実行は安全確認なしに許可しない。ART-FIRST、正式採用0、正式331人体／993足元＆G0/S1/G1/G2/G3 NOT RUN、MakeCode費用未評価、Minecraft施工禁止、main変更禁止、PR #53 Draft未merge、Work不使用／事前承認制を維持。

**次の実際に必要な技術は単純なEdit操作の追加ではなく、Blender実画面・3D構造を取得し、作品を見て作者が継続修正できる閉ループ制作経路である。** その経路が未確立なまま箱状の「仮都市」を再生成しない。
