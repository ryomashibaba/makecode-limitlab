# START HERE — MakeCode LimitLab / G4-C7 Orbital Commons

**チャット移行の唯一の入口。2026-11-02 JST更新。GitHub研究ブランチが正本。** 長い引き継ぎ文の再コピー、ZIP再添付、過去の計画の再決定は不要。

## まず読む（この順番）

1. **[M37-Nまでの全計画・全体方針・ユーザー指示・失敗・技術/安全契約・次工程を統合した日本語引き継ぎ](docs/G4C7_M37N_FULL_HANDOFF_20261102_JA.md)**。最初に全文を読む。
2. **[2026-10-28制定のR0〜R5固定戦略](docs/G4C7_POST_B10_CRITICAL_STRATEGY_REVISION_JA.md)**。同時に全市街の粗い3Dと代表生活断面を作ること、ART-FIRST/QUALITY-FIRST、2案失敗時の方法変更は絶対方針。
3. **[M37-Nの最新絶対美術不採用・独立安全未確認報告](research/g4c7-b11-r5-d56/p2/d3s26/M37N_REAL_NATIVE_SHIPYARD_CARVE_FIXED_VIEW_ART_REJECT_JA.md)**。
4. **[M37-Nの真正Blender原本・5新画像・manifest・独立監査・制作コード](artifacts/g4c7-m37n-verified-native-maker-exposure-art-hold/)**、[M37-M編集ワークスペース](artifacts/g4c7-m37m-verified-native-review-workspace-art-hold/)、[M37-K室⇄外形連動技術](artifacts/g4c7-m37k-verified-native-authoring-method-art-hold/) を必要な範囲で照合する。
5. 必要な場合に限り **[昔からの大規模研究履歴](docs/G4C7_LIVE_HANDOFF.md)** を辿る（ファイルの先頭は旧D3S20であり、現在の最新ではない）。

## いま最も重要な確定状態

| 区分 | 状態 |
|---|---|
| G4-C7全体美術 | **ART HOLD** |
| 正式ユーザーART採用 | **0件** |
| 直近M37-N | 既存外殻10メッシュを真正BLENDで直接切除した**限定METHOD TECH PASS**、都市美術は**ART REJECT** |
| 現行正式331人体/993足元QAとS1/G1/G2/G3 | **NOT RUN** |
| 新都市Minecraft Education施工・既存都市統合 | **禁止／今回までworld writes 0** |
| mainへの変更 | **禁止** |
| Draft PR [#53](https://github.com/ryomashibaba/makecode-limitlab/pull/53) | **Open/Draft/未merge**（再開時に再確認） |
| 継続ブランチ | **dev/g4c7-a17-monolithic-rift-fold-art-study** |
| 直近専用CI | [M37-N #41318630617 SUCCESS](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41318630617) |
| 引き継ぎ前HEAD | **42b38673acf43de4016a26241d1d66d5d567449d**（この引き継ぎコミットより前。**固定せず現在HEADを読め**） |

**絶対安全契約**：331人体、993足元、人体半幅0.65m、足元+0.15〜+3.25m、旧干渉上限45/331、未支持0/993、負の対照。条件を緩めず、局所レイ・面重複・実メッシュ数・CI SUCCESSから正式安全を認定しない。Blender/GLBは研究表現であり、最終施工手段は**MakeCodeのみ**。

**根本的反省**：何度も制作方法を変えても、箱・棚・低層キャンパス・巨殻・チューブ・巨大な空白という「簡単に自動生成できる形」が美術を支配してしまった。M37-Hの2案A/Bはいずれも美術失格。M37-Kの室/外形連動・M37-Mの直接編集環境・M37-Nの外殻切除は技術の実証であり、**新しい美しい都市を完成させたわけではない**。M37-L/Nのチューブをさらに切る/飾ることを**停止**。詳細は上記全文。

## 次工程 — M37-Oの方向（方針再決定はしない）

- 「市民が何を見る／どこへ行く」「宇宙機の実製造」「研究観察」「住宅の私的境界」「文化と高所の公共空間」が、**都市の全域立体造形と同じ作者決定で互いに形を変える**制作手順へ移る。遠景だけ/小部屋だけを先に完成させない。
- 旧技術ライブラリK/M/Nは保持し、旧チューブ美術は流用しない。単純な第三の自動プリミティブの生成やテスト件数だけの前進は禁止。**品質に明確な価値がある真正3D**を少数・厳格に審査し、弱ければ早期停止して制作の根本原因を訂正。
- 正式美術採用0、全体ART HOLD、正式安全QA未実施、Minecraft施工禁止・都市統合禁止、main保護、PR Draft、Work事前許可という固定条件は**新チャットでもそのまま継承**。

## これからの各チャットの必須操作

1. このSTART_HERE、詳細ハンドオフ、根本戦略、最新M37-N原本を**GitHubから直接取得**する。ユーザーへZIP/長文資料の再提出を求めない。
2. 同時並行開発との競合回避のためPR #53 **現在のHEAD**、最新専用Actions・通常Verify、必要な実ファイルとSHAを照合。古い引き継ぎSHAから開発しない。
3. ユーザーが「次の工程」と指示したら、R0〜R5の正当な次工程を**実際に**進め、見た目が悪ければREJECT。計画書/メッシュ/CIの数を成果と呼ばない。Chat中心、Workは事前明示許可のみ。
4. 毎回報告は **(a)ART絶対評価 (b)実生活・経路・支持 (c)MakeCodeコスト/未確認 (d)GitHub原本・CI (e)続行/停止**。美術結果とTECH/S1/施工を混同しない。
5. 新しい根拠と工程の進歩が確定したらGitHubの詳細ハンドオフに日付付き補遺を追加し、この入口の現行状態・次工程を更新。**旧長大LIVE_HANDOFF、過去成果、main、旧世界は保護**。

---

### 新しいChatGPTチャットに送る一文

> **MakeCode LimitLab / G4-C7を、GitHubの研究ブランチにあるSTART_HERE.mdとリンク先の完全引き継ぎから継承してください。最新HEAD・PR #53・CI・実Blender原本を自分で照合し、これまでの固定方針と反省を一切変えず、M37-Nから次の正当な開発工程へ進めてください。旧チューブ案の延命、Minecraft施工・都市統合、main変更、無断Workはしないでください。**
