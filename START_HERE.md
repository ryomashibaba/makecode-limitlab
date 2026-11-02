# START HERE — MakeCode LimitLab / G4-C7 Orbital Commons

**チャットを移ってもここから再開する。GitHubの現在の研究ブランチが正本。2026-11-02 JST更新。**
旧チャット全文・古いZIP・長い引き継ぎ文をユーザーへ要求しない。前工程をやり直さず、前の方針や不採用を再決定しない。

## 最優先で読む新しい統合引き継ぎ

**[M37-P1完了／M37-P2継続の完全統合引き継ぎ](docs/G4C7_M37P2_COMPLETE_INTEGRATED_HANDOFF_20261102_JA.md)**

これはM37-Nまでの全履歴を引き継いだうえで、最新M37-O1／P0／P1、2つの絶対美術REJECT、反省点、R0〜R5固定戦略、QA/施工禁止と正当な次工程を統合した**現行の第一正本**。必ず最初に確認する。

併せて以下を必要に応じて参照する：
- [2026-10-28確定R0〜R5制作戦略](docs/G4C7_POST_B10_CRITICAL_STRATEGY_REVISION_JA.md)
- [M37-P1 7真正視点の絶対ART不採用審査](research/g4c7-b11-r5-d56/p2/d3s26/M37P1_NATIVE_SEVEN_VIEW_EARLY_ART_REJECT_AND_P2_AUTHOR_METHOD_RESET_JA.md)
- [M37-P1真正BLEND／7 PNG／manifest／独立監査／コード](artifacts/g4c7-m37p1-verified-native-interlocked-urban-author-art-hold/)
- [M37-O1真正BLEND／5 PNG／独立監査](artifacts/g4c7-m37o1-verified-native-activity-author-art-hold/)と[EARLY ART REJECT](research/g4c7-b11-r5-d56/p2/d3s26/M37O1_SAVED_NATIVE_FIVE_VIEW_EARLY_ART_REJECT_AND_AUTHOR_INPUT_RESET_JA.md)
- [M37-P0共有作者判断の入力原本](research/g4c7-b11-r5-d56/p2/d3s26/M37P0_SHARED_AUTHOR_DECISION_SOURCE_OF_FORM_V1.json)、[M37-K](artifacts/g4c7-m37k-verified-native-authoring-method-art-hold/)、[M37-M](artifacts/g4c7-m37m-verified-native-review-workspace-art-hold/)、[M37-N](artifacts/g4c7-m37n-verified-native-maker-exposure-art-hold/)の技術資産
- [M37-N時点の以前の統合引き継ぎ](docs/G4C7_M37N_FULL_HANDOFF_20261102_JA.md)と[過去の長期研究履歴](docs/G4C7_LIVE_HANDOFF.md)。**これらの古い書類の「次工程M37-O」や履歴先頭D3S20は現在の次工程ではない。**

## 現在の確定状態：正本は M37-P1 完了 → M37-P2

| 項目 | 状態 |
|---|---|
| 最終制作目標 | Minecraft Educationで最終MakeCode施工する、居住・研究・文化・宇宙機製造が一体化した巨大未来都市 |
| **全体ART** | **HOLD** |
| **正式ユーザー美術採用** | **0件** |
| **M37-O1** | 5真正視点、限定METHOD成立だが分離低層パビリオン・暗い公共/住居で **EARLY ART REJECT** |
| **M37-P0** | 作者の4共有判断のソース意図契約、[CI #41350862339 SUCCESS](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41350862339)。真3D ART成果ではない |
| **M37-P1最新** | 4共有決定→実メッシュ、真正BLEND・7画像・独立再読込・6負例 [CI #41351764632 SUCCESS](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41351764632)。**限定TECH PASS／EARLY ART REJECT** |
| 次工程 | **M37-P2：形態生成の決定権を単純プリミティブから作者の3D造形・人の体験へ戻す制作方法変更**。新BLEND未制作 |
| 331人体／993足元、正式G0/S1/G1/G2/G3 | **NOT RUN** |
| 自由歩行・工場隔壁/住宅私界の安全・構造・避難 | **NOT CERTIFIED** |
| 新都市Minecraft Education施工・都市統合 | **禁止、world writes 0** |
| MakeCodeの新都市施工時間/Fill/Clone/Place | **NOT EVALUATED** |
| main | **変更禁止** |
| [PR #53](https://github.com/ryomashibaba/makecode-limitlab/pull/53) | **Open／Draft／未mergeを維持**（次のChatでは再照合） |
| Work | **ユーザー事前明示承認制、Chat中心** |

研究ブランチ：**\`dev/g4c7-a17-monolithic-rift-fold-art-study\`**。
新統合文書作成前に照合したHEAD：\`50285ae9b7948d2404b223437c73efe88b4b8cab\`。**引き継ぎ保存でHEADは変わった。決してこのSHAにリセットせず、毎回現在のPR headを確認する。** 前HEADの通常 Verify [#41352198482](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41352198482) は再照合で**SUCCESS**。本引き継ぎコミットのVerifyは別実行なので次チャットで再照合。専用P1成功は確定。

## 変更禁止の重要な方針

- **ART-FIRST／QUALITY-FIRST**：遠景の地区密度・実生活・公共入口眼高・製造・研究・住宅・文化・代表室内・高所を同一真正3Dで作る。全都市粗3Dと代表の実生活断面は**同じ作者原本で同時制作**。一方だけ先行完成しない。
- **繰り返し禁止**：箱、棚板、巨壁、アーチだけの彫刻、長いチューブ、独立キャンパス、巨大テント、道路帯、空洞模型。形状自体を一般的に禁止するのではなく、これらが都市を支配する**安易な反復・第三案生成**を禁止する。
- **直近の2つの本物の失敗**：M37-O1は7独立多角形用途押出し＋板橋、M37-P1は共有判断を実メッシュへ伝播させても\`patch/wall/bridge\`を反復し巨大板・壁・帯へ。**同じ方式で第三の試案を作らず、P2の作者方法からやり直す。**
- **安全契約厳守**：人体331・足元993・人体半幅0.65m・足元+0.15〜+3.25m・干渉上限45/331・未支持0/993。負例検査を伴う独立監査。局所TECH PASSからARTやS1の合格を推定しない。Blender研究単位をMinecraft 1block=1mに勝手に対応させない。
- **禁止**：main更新、PR #53 Ready化/merge、旧BLEND/ZIP/CSV/USEDラッチ/世界の上書き、未承認のWork・外注・Minecraft world write。本人が正式ART採用を宣言するまでアシスタントは正式採用扱いしない。

## 新しいチャットの再開手順

1. GitHub Connectorでこの入口と**上の完全統合引き継ぎ**を読み、現行ブランチHEAD、PR #53のDraft状態、最新CIと真正BLEND・manifest・画像を確認。
2. M37-O1/P1のART REJECTを固定。原本の保存/ハッシュ・技術PASSと美術失格を区別。安全331/993・G0/S1/G1/G2/G3は全て未実施。
3. **次にM37-P2の正当な制作方法切替を実際に進める**。出来ることはGitHubとChatで実行し、Blender GUI等Workが必要なら事前にユーザーの明示承認を得る。旧チューブ・巨大壁・板/帯・第三の自動プリミティブの延命をしない。
4. 真正3Dの全景・公共・住宅の早期美術審査を最優先。価値がなければ早期にART REJECTし、メッシュ数やCIを品質と誤認しない。美術候補になってから機能/安全/MakeCodeへ。
5. 結果を新統合引き継ぎへ追補し、このSTART_HEREを最新に保つ。ユーザーに長文やZIPの再提出を求めない。

---

### 新しいチャットに送る最短の一文

> MakeCode LimitLab / G4-C7を、GitHub研究ブランチのSTART_HERE.mdとリンク先のM37-P2完全統合引き継ぎから継承してください。最新HEAD・Draft PR #53・CI・真正Blender原本を照合し、M37-O1/P1のEARLY ART REJECTと全固定方針を守って次のM37-P2工程を実際に進めてください。ART HOLD・正式採用0・安全QA未実施・Minecraft施工禁止・main変更禁止・Work事前承認制。過去の失敗形態の第三案やZIP/長文再提出は禁止です。


## M37-P2実作業追補（2026-11-02 JST）

- P2の**新しい真正都市3D／Blender原本はまだ未制作**。ART HOLD／正式採用0に変化なし。
- P1保存ソースと真正画像の再検証で、黒い`RESEARCH_EYE`カメラが厚壁`EAST_RESEARCH_MAKER_WING`内に配置されている幾何欠陥を特定（距離1.538研究単位、壁半厚1.75）。
- [P2カメラ実メッシュ内埋没診断ツール](tools/g4c7_m37p2_native_camera_inside_solid_audit.py) と[既存P1 BLEND読み取り専用負例CI](.github/workflows/g4c7-m37p2-camera-solid-negative-control.yml)を追加。専用[Actions #41353940198](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41353940198) は初回照合でQUEUED。**技術前提の不良発見であり、都市美術の改善・採用を意味しない。**
- 続きと固定条件は[現行統合引き継ぎの節10](docs/G4C7_M37P2_COMPLETE_INTEGRATED_HANDOFF_20261102_JA.md)。第三の`patch/wall/bridge`都市生成ではなく、作者が同一真正BLENDで都市粗形と生活断面を同時に直接編集する段階へ。Workは明示的事前承認まで使わない。



## M37-P2 直接作者原本レビュー経路（2026-11-02 JST追補）

- [非生成型Blender作者原本・全景/公共眼高/住宅眼高の真正3視点レビュー](tools/g4c7_m37p2_author_native_early_review.py)を研究ブランチへ実装。旧P1の`patch/wall/bridge`自動造形の第三案を作る仕組みではない。**新P2真正BLENDはまだNOT CREATED、ART HOLD・正式採用0**。
- 新しい作者編集済み保存BLENDが入力になった場合のみ、旧不採用原本を拒否し、原本SHA不変とカメラ実壁埋没負例を確認して、3枚の真正画像へ進む。シーンの作者宣言は美術品質・製作者の独立証明ではない。
- [専用P2の限定METHOD/負例Actions](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41354779183) は最新照合時QUEUEDでPASS未確認。詳細は[統合引き継ぎ節11](docs/G4C7_M37P2_COMPLETE_INTEGRATED_HANDOFF_20261102_JA.md)。
- 次の美術制作は「全都市粗3Dと実生活・製造断面を一つの新しい直接作者原本で同時編集し、3視点を早期ART審査」。原本未制作なのに工程完了やART合格を宣言しない。main・Draft PR #53・Minecraft禁止・Work事前承認は不変。


## M37-P2 真正Blender「空の直接作者スタジオ」進行（2026-11-02 JST）

- [新しい直接Blender制作スタジオの実装](tools/g4c7_m37p2_direct_author_studio.py) と [真正ネイティブ空原本生成＋別プロセス再読込のActions](.github/workflows/g4c7-m37p2-empty-direct-author-studio-native.yml) を導入。旧不採用造形を複製せず、全市街＋代表生活断面の**直接編集**に使う。都市生成メッシュは **0** であり、**ART作品はまだ未制作**。
- 3真正早期レビューも[作者が編集したマクロ／製造公私境界／研究文化／住宅の実メッシュ](tools/g4c7_m37p2_author_native_early_review.py)と作者確認済み3視点を必須に強化。虚偽のP2美術認定禁止。
- 初回空スタジオCI [#41359593395](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41359593395) はWorld欠落でFAIL、次の[#41359669304](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41359669304) は圧縮形式ヘッダーの独立監査でFAIL。原因を修正し、再試行[#41359859014](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41359859014) は本追補時点で**QUEUED／未確定**。SUCCESSと断定しない。
- 以前からの固定条件は[最新統合引き継ぎの節12](docs/G4C7_M37P2_COMPLETE_INTEGRATED_HANDOFF_20261102_JA.md)参照。次は**空のテンプレートではなく、同一保存原本に都市と人の生活が実際に見える真正3D美術の制作**。Workには事前明示承認が必要。main変更、Minecraft施工、正式ART採用は禁止のまま。


## M37-P2 2026-11-02：暫定カメラの虚偽承認を検出（限定METHOD）

- 最新の作者レビュー入力では**全景・公共・住宅の各カメラが初期空スタジオの暫定位置から最低1抽象研究単位移動**していなければ拒否する。[ソース](tools/g4c7_m37p2_author_native_early_review.py)、[専用CI #41374480855 SUCCESS](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41374480855)、[統合引き継ぎ節13](docs/G4C7_M37P2_COMPLETE_INTEGRATED_HANDOFF_20261102_JA.md)。
- **限界**：カメラ移動だけでは良質な視点・造形を証明しない。P2新真正都市美術は未制作。空真正BLEND・0実メッシュのまま、全体ART HOLD／正式採用0、331/993・G0/S1/G1/G2/G3未実施、MakeCode未測定、Minecraft施工禁止、main保護・Draft PR #53維持。
- **次工程**：新しい同型の自動生成を繰り返さず、同一作者編集Blender原本に全市街粗3Dと代表製造・研究・住宅・文化の生活断面を実造形し、3真正視点を絶対美術審査。Work/GUIの承認制は不変。


## M37-P2 同一Blender原本の全景＋人間視点・並行直接編集機能

- [真正Blender GUI用並行編集アドオン](tools/g4c7_m37p2_parallel_author_view.py)を研究ブランチへ追加。都市全景＋公共または住宅の人間視点を2画面にし、**同じ作者原本の直接造形**を可能にする。新都市のメッシュは自動生成しない。
- [Blender実原本を使う登録・負例の独立CI](.github/workflows/g4c7-m37p2-parallel-native-author-ui.yml) を追加。GUI二画面の実操作自体はヘッドレスでは未確認。詳細は[統合引き継ぎ節14](docs/G4C7_M37P2_COMPLETE_INTEGRATED_HANDOFF_20261102_JA.md)。
- **ARTではない**。新P2都市美術未制作、ART HOLD／正式採用0、正式331/993・G0/S1/G1/G2/G3未実施、MakeCodeコスト未評価、Minecraft施工禁止、main変更禁止、PR Draft維持。次は直接3D造形の現物が必要。Workは事前明示承認なしでは使用不可。


## M37-P2 2026-11-02：真正Blender統合作者作業原本の保存成功（ART未制作）

- [新規保存した真正Blender作業原本](artifacts/g4c7-m37p2-integrated-native-author-workspace-NOT-ART/M37P2_INTEGRATED_EMPTY_ARTIST_WORKSPACE_NOT_ART.blend) は独立再読込に成功。491,214 bytes、SHA256 `6ca727def08cce9220dbde59f5836248cb5d0def39c7f375c9308af1461ee904`。作者の全景＋人間視点GUI編集支援と真正3視点レビュー用Pythonを同一BLENDへ埋込んだ。元の空原本・旧拒否モデルは不変。
- [専用Actions #41390131345](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41390131345) completed/SUCCESS。[マニフェスト](artifacts/g4c7-m37p2-integrated-native-author-workspace-NOT-ART/M37P2_WORKSPACE_BUILD_MANIFEST.json)が保存済み。
- **これは美術ではなく実メッシュ0の空編集スタジオ。** GUI実操作、都市全景・生活室の直接造形・美術3視点は未実施。ART HOLD／正式採用0、正式331/993・G0/S1/G1/G2/G3 NOT RUN、MakeCode未評価、Minecraft施工禁止、main不変更、Draft PR #53維持、Work事前承認不変。
- 次の正当工程は都市粗3Dと居住・文化・研究・実造船の生活断面を**同じBlender原本で実造形**すること。旧P1のプリミティブ同型第三案を生成しない。全文は[統合引き継ぎ節16](docs/G4C7_M37P2_COMPLETE_INTEGRATED_HANDOFF_20261102_JA.md)。


## M37-P2 2026-11-02：単一真正BLENDの早期美術レビュー実行経路（節17）

- 既存の統合空原本で、内蔵3視点審査が外部.pyに依存しText Editorからそのまま実行できない欠陥を修正。[自己完結GUIレビューボタン](tools/g4c7_m37p2_one_file_early_art_review_gui.py)／[同梱カメラ監査を読める改修版](tools/g4c7_m37p2_author_native_early_review.py)／[真正BLEND新v2原本作成](tools/g4c7_m37p2_integrate_standalone_review_workspace_v2.py)。
- [専用native Actions #41422123251](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41422123251)：真正Blenderでの**新v2生成工程はSUCCESS**、独立再読込・「空原本をARTレビューできない」負例検証は直近で**IN_PROGRESS、全体SUCCESS未確定**。アーカイブが実際にGitHubへ現れるまでは保存済みと称さない。詳細は[現行統合引き継ぎ節17](docs/G4C7_M37P2_COMPLETE_INTEGRATED_HANDOFF_20261102_JA.md)。
- これは新市街美術ではない。P2新真正都市メッシュ0、ART HOLD、正式採用0、331/993・G0/S1/G1/G2/G3 NOT RUN、MakeCode未測定、Minecraft施工禁止、main変更禁止、PR #53 Draft維持。作者による全景と生活断面の同一BLEND直接3D造形が次の美術制作。Workは事前明示承認制、未承認利用禁止。
