# START HERE — MakeCode LimitLab / G4-C7 Orbital Commons

**チャット移行の唯一の入口。2026-11-02 JST更新。GitHub研究ブランチが正本。** 長い引き継ぎ文の再コピー、ZIP再添付、過去の計画の再決定は不要。

## M37-P1 実体制作へ移行（2026-11-02 JST／最新CI要再照合）

- **[M37-P1真正Blender作者原本の制作工程・CI修正履歴・未確認事項](docs/G4C7_M37P1_NATIVE_ART_EVIDENCE_PENDING_20261102_JA.md)**。旧M37-O1の不採用施設とM37-L/Nのチューブ美術を再利用せず、M37-P0の4共有作者判断を実メッシュへ結びつける研究コード・独立再読込監査・7視点レンダリングCIを研究ブランチへコミット。
- 初回 [#41351611157](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41351611157) はBlenderの`mathutils`読込順で**FAIL**。コード修正済み。再実行 [#41351764632](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41351764632) は**再開時に現在状態を確認**。CI成功とGitHubアーカイブの実在・SHA・真正7視点・厳格な美術批評の完了前に**M37-P1のMETHOD PASSやART改善を主張しない**。
- **M37-O1 EARLY ART REJECT／全体ART HOLD／正式採用0／正式331/993・G0/S1/G1/G2/G3 NOT RUN／Minecraft施工・統合禁止／main変更禁止／PR #53 Draft／Work事前承認制**をそのまま継承。

## 最新：M37-O1の美術不採用とM37-P0の作者入力ゲート（2026-11-02 JST）

- **[M37-O1真正5視点によるEARLY ART REJECTと根本原因の固定](research/g4c7-b11-r5-d56/p2/d3s26/M37O1_SAVED_NATIVE_FIVE_VIEW_EARLY_ART_REJECT_AND_AUTHOR_INPUT_RESET_JA.md)**。実BLEND＋5枚のGitHub保存真正画像を確認。俯瞰は独立した低層押出しパビリオン、公共・住宅・高所眼高は暗い/遮蔽された空間で、**都市の美術として明白に不採用**。M37-N旧チューブもART REJECTのまま。M37-O1を拡大・改装・装飾して延命しない。
- **[M37-P0 作者が共同決定する生活断面の新入力正本](research/g4c7-b11-r5-d56/p2/d3s26/M37P0_SHARED_AUTHOR_DECISION_SOURCE_OF_FORM_V1.json)**。各用途の独立した建築輪郭を押し出して接続する入力を禁止し、製造/見学/研究・公共/住宅私界・文化/上層が**都市外形と実床・実境界を一緒に変える**意思決定を定義。これは**形態の意図データのみ、新BLEND・新ART候補ではない**。
- **[M37-P0入力契約ガード](tools/g4c7_m37p0_author_source_contract_guard.py)**と[専用CI #41350862339](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41350862339) **SUCCESS**。6件の故意不正を拒否し、公開ルートが工場作業域・住居私域を意図の上で横断しないことを検査。ただし**安全な実歩行・本物の共有壁・美しさは未検証**で、入力ガード成功をART PASSへ昇格しない。
- **次の実体工程**：旧M37-O1の7独立建物を流用せず、共有意思決定が実3Dの都市外観と内部をどう同時変更するかを作家判断で新作者シーンに落とし込み、早期に真正全域/公共/製造/居住/文化/高所の固定視点で厳しく審査。見た目が悪ければ早期停止。**全体ART HOLD・正式採用0・正規331/993とS1/G1/G2/G3 NOT RUN・Minecraft施工禁止・main変更禁止・PR #53 Draft・Workは事前承認制**を絶対維持。

## M37-O1追補（2026-11-02 JST／最新状態は常にActionsで再照合）

**[M37-O1作者ソース・CI確認待ち・早期ARTゲートの記録](docs/G4C7_M37O1_AUTHOR_SOURCE_AND_CI_PENDING_20261102_JA.md)**。M37-Nまでの下記完全統合正本は引き続き有効。

M37-Oの新規実験AのBlender作者コード・独立監査コード・[専用Actions #41321512829](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41321512829) を研究ブランチに追加した。初回記載時点はCI QUEUEDで、**真正M37-O BLEND・PNGの完成やMETHOD PASSは未確認**。ランの結果／アーカイブ原本／最新HEADを再取得するまで成功と報告しない。旧チューブ・箱群・独立キャンパスの再発は実画像で即不採用。**全体ART HOLD・正式採用0・正式安全QA NOT RUN・Minecraft施工禁止・main変更禁止・PR #53 Draft・Work事前承認制**を維持。

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
