# G4-C7 R1 — 真正Blender負例画像に基づく視認性ゲート実証（2026-11-03）

## 今回の結果：限定TECH PASS、作品は美術不採用のまま

**Civic BraidはEARLY ART REJECT。全体ART HOLD・正式採用0。**
過去に繰り返した「GUI・レンダリング成功＝作品の品質改善」という誤認を防ぐため、**不合格側の兆候のみ検出する補助検査**を実装した。検査が問題を検出しなくてもART PASSにはならない。新都市メッシュ制作、既存BLEND修正、MakeCode施工はいずれも実施していない。

## 具体的な保存実装

- [負例ゲート本体](../../../../tools/g4c7_r1_negative_only_vision_gate.py)・[5件の負例テスト](../../../../tests/test_g4c7_r1_negative_only_vision_gate.py)・[専用GitHub CI](../../../../.github/workflows/g4c7-r1-negative-only-visibility-regression.yml)。
- [実行CI #41624336875](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41624336875)：completed/SUCCESS。実ネイティブBLEND/独立manifest/5枚Cycles画像のSHA256を照合、画像を読み取り、保存済みの不採用HABITAT_EYEを機械的にBLOCKした。
- [恒久保存の独立監査JSONとSHA256](../../../../artifacts/g4c7-r1-true-native-negative-only-visibility-20261103-NOT-ART/)：研究ブランチに実ファイルの存在を確認。
- 入力は既存不採用R1 Civic BraidのBlender原本（SHA256: 002618e89a93d28cab309392011e69b729d9cfefc469258e4d2a72177910e95b）を用いた。5画像の独立manifest（SHA256: 66f74f25f435ee6dbbe21af75a66e133fe631824c96facf473449a90d605763a）とPNG自体のSHA256を対応づけた。今回はBlenderを新しく実行しておらず、過去の独立再読込記録を検証対象とした。

## 実測した5視点の中心暗部率

暗部：RGB各画素の最大チャンネルが34/255以下。中央領域：画像の上下左右20%を除外した範囲を120×80画素で標本化。中央暗部率93%以上を視認性ブロックとする。

| 視点 | 全画面暗部率 | 中央暗部率 | 機械判定 |
|---|---:|---:|---|
| AERIAL | 0% | 0% | 深刻な暗部は検出されず（美術は不採用） |
| PUBLIC_EYE | 0.0875% | 0.0313% | 深刻な暗部は検出されず（美術は不採用） |
| HABITAT_EYE | **98.7938%** | **100%** | **BLOCK_VISUAL_OBSERVABILITY** |
| FACTORY_EYE | 0% | 0% | 深刻な暗部は検出されず（美術は不採用） |
| RESEARCH_EYE | 2.0563% | 2.875% | 深刻な暗部は検出されず（美術は不採用） |

これらの数値は色彩・露出の一部を検出するだけで、形態の単調さ、巨大壁、世界的都市密度、製造工程、研究活動、生活体験の成立を測れない。すでに目視で不合格とした他4視点のART REJECT判定は一切変更しない。暗い演出が意図的な場合は人間の確認が必要で、**このゲートだけで正式な美術不採用や合格を決めない**。

## 継続条件と絶対保護

本工程の限定価値は、**次に真のBlender作者作品が提出された場合に、同一ネイティブ・画像5枚の出所と重大な視認性欠落を先に見つけること**。コード式低品質都市の量産・追加GUI猿テスト・単発技術試験を再開しない。高品質の建築都市を直接造形する作者能力はいまだ未成立。Work/Sol/有料手段はユーザー事前明示承認なしで使わない。

R0〜R5固定、ART-FIRST、全体ART HOLD、正式採用0、331人体/993足元・人体半幅0.65/足元+0.15〜+3.25/干渉上限45/未支持0の安全契約不変、G0/S1/G1/G2/G3 NOT RUN、MakeCode未評価、Minecraft施工禁止、main/保護v3・旧不採用原本不変更、PR #53 Draft/未マージ、world writes 0を維持。
