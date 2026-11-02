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


### 2026-11-02 M37-P2 v2 native Actions訂正

- 最初の[#41422123251](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41422123251) は真正BLEND生成工程まではPASS、独立再読込実行中に診断付き新ワークフローへ切り替え **CANCELLED**（全体SUCCESSではない）。
- [新版 #41422705862](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41422705862) は150秒の実行上限・診断出力を追加し、最後の照合で**QUEUED**。真正v2 `.blend` のGitHub追記保存は結果とmanifest実在を確認するまで未確定。全詳細は[統合引き継ぎ節17と補足](docs/G4C7_M37P2_COMPLETE_INTEGRATED_HANDOFF_20261102_JA.md)。
- 終始、P2新都市実造形0・ART HOLD・正式採用0、331/993・G0/S1/G1/G2/G3未実施、Minecraft施工禁止、main不変更、PR #53 Draft/未merge、Work明示承認制。


## M37-P2 2026-11-02：単一BLEND作者直接造形＋3視点審査v2成功（ART未制作）

- [新規真正Blender原本v2](artifacts/g4c7-m37p2-standalone-artist-workspace-v2-NOT-ART/M37P2_SINGLE_FILE_DIRECT_AUTHOR_AND_REVIEW_NOT_ART.blend) を保存済み。526,911 bytes／SHA256 `a772fc0bc1d1d2b23a33a14154ca5bcd08fcb1ced05ea5c9eb009aa02b19f99e`。新原本内に二画面作者編集・3真正視点のGUIレビューとカメラ埋没監査ソースを内蔵。旧真正原本・不採用ARTを変更しない。
- [専用Actions #41423413754](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41423413754) は **SUCCESS**：本物のBlenderで保存→別プロセスで再読込、埋込Text SHA一致、GUIアドオン登録・解除、空テンプレートのARTレビューボタン誤起動拒否、GitHub追記保存を確認。初回CANCELLEDと後の誤検証assertによるFAILは[統合引き継ぎ節18](docs/G4C7_M37P2_COMPLETE_INTEGRATED_HANDOFF_20261102_JA.md)に明記。
- **重要：これは空の作者編集スタジオであって、新しい都市造形ではない。都市実メッシュ0・真正美術3画像なし・BlenderデスクトップGUI実操作未確認。** ART HOLD／正式採用0、331/993・G0/S1/G1/G2/G3 NOT RUN、MakeCode未評価、Minecraft施工禁止、main不変更、Draft PR #53維持。
- 次工程はエディタ増設ではなく、**実際の都市マクロ＋居住・見学/製造・研究/文化の実生活断面を同じ作者BLENDで直接造形すること**。未承認Work禁止、旧P1のpatch/wall/bridge型第三生成案禁止。


## M37-P2 2026-11-02：真正3視点正常系PASS／修正済み作者原本v3

- **v3を現在の作者編集入口にする**：[真正Blender v3原本（修正済み、ART未制作）](artifacts/g4c7-m37p2-patched-native-author-editor-v3-NOT-ART/M37P2_DIRECT_AUTHOR_NATIVE_EDITOR_FIXED_REVIEW_V3_NOT_ART.blend)。528,408 bytes、SHA256 `536e451c763c4326421b13285abf1056a3a11d755028f8ff20b54b99b08a0249`。旧v1/v2/不採用原本は上書きせず保護。
- [一時技術メッシュを用いた正常系3真正Cycles PNG CI #41428422529 SUCCESS](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41428422529) でAERIAL/PUBLIC_EYE/HABITAT_EYEを実描画、保存原本不変とPNG/SHAを確認。一時メッシュ・画像は破棄し、**都市美術・正式ARTではない**。
- 実際の不具合は `bpy_prop_collection.__contains__` にObjectを渡す誤りと、ヘッドレス特有の`bpy.data.is_dirty`誤判定。[修正済みv3 native BLEND独立再読込/追記保存 CI #41428982047 SUCCESS](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41428982047)。
- 実都市原本の直接3D造形とデスクトップGUI実操作はまだ未実施。**ART HOLD・正式採用0、331人体/993足元とG0/S1/G1/G2/G3 NOT RUN、MakeCode未測定、Minecraft施工禁止、main変更禁止、Draft PR #53未merge、Work事前明示承認**を維持。
- 次は新しい空テンプレートを増やさず、作者がこのv3同一原本で全市街粗3Dと居住・造船/見学・研究・文化の実生活断面を同時造形し、3実視点の絶対美術審査。全文は[統合引き継ぎ節19](docs/G4C7_M37P2_COMPLETE_INTEGRATED_HANDOFF_20261102_JA.md)。


## M37-P2 2026-11-02：Blender実GUIで全景／公共・住宅の2編集画面 PASS

- [本物のBlender 4.5.15 GUIでの2画面分割／視点切替CI #41431524480 SUCCESS](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41431524480) を確認。Xvfb実ディスプレイ、`bpy.app.background=False`、v3原本の`VIEW_3D`実エリア2つ、公共→住宅の編集視点切替、元SHA不変を実測。[詳しい実行証拠と限界](research/g4c7-b11-r5-d56/p2/d3s26/M37P2_ACTUAL_DISPLAY_GUI_DUAL_AUTHOR_EDITOR_PASS_20261102_JA.md)／[統合引き継ぎ節20](docs/G4C7_M37P2_COMPLETE_INTEGRATED_HANDOFF_20261102_JA.md)。
- [v3真正作者原本](artifacts/g4c7-m37p2-patched-native-author-editor-v3-NOT-ART/M37P2_DIRECT_AUTHOR_NATIVE_EDITOR_FIXED_REVIEW_V3_NOT_ART.blend) は528,408バイト・SHA256 `536e451c763c4326421b13285abf1056a3a11d755028f8ff20b54b99b08a0249` のまま不変。実GUIで都市造形を行ったわけではない。ART HOLD、正式採用0、正式331/993・G0/S1/G1/G2/G3 NOT RUN、MakeCode未評価、Minecraft施工禁止。
- **次工程は唯一、GUIで都市マクロと製造・見学・研究・文化・住居を同時に実造形すること。** 旧不採用案の自動生成への復帰、空スタジオの追加、main変更、PR #53のmerge、未承認Workは禁止。


## M37-P2 2026-11-02：空スタジオ整備終了 → 直接作者都市美術の内容を具体化

- [作者主導の初回未採用構想「街を織り込む造船都市」](research/g4c7-b11-r5-d56/p2/d3s26/M37P2_FIRST_DIRECT_AUTHOR_ART_DIRECTION_CITY_AND_LIVED_SECTION_20261102_JA.md)を保存。旧P1/O1形式の同型自動第三案ではない。都市全体の密度と、実設備ある造船・隔てられた見学室・研究文化の採光中庭・私界のある住居を**同じ直接作者3D**に最初から組み込む方針の具体的な未採用ART方向。これは完成模型・美術採用・新Blenderメッシュではない。
- [統合引き継ぎ節21](docs/G4C7_M37P2_COMPLETE_INTEGRATED_HANDOFF_20261102_JA.md)に実行可否を追加。現真正編集入口は[v3空BLEND](artifacts/g4c7-m37p2-patched-native-author-editor-v3-NOT-ART/M37P2_DIRECT_AUTHOR_NATIVE_EDITOR_FIXED_REVIEW_V3_NOT_ART.blend)であり、SHA256 `536e451c763c4326421b13285abf1056a3a11d755028f8ff20b54b99b08a0249`。その都市メッシュは0。実GUI二画面TECH PASSと都市造形ART未着手を区別する。
- 新しい空テンプレート・CIを繰り返すより、作者による都市マクロ＋実居室＋製造研究文化の直接Blender 3D制作と真正3視点レビューを次工程の唯一の美術要件とする。Chatで直接Blender GUIの作者操作ができず、Workはユーザー事前明示承認制、未承認のまま代行・外注しない。
- **ART HOLD／正式採用0、331人体/993足元・G0/S1/G1/G2/G3 NOT RUN、MakeCodeコスト未測定、Minecraft world writes 0、main変更禁止、Draft PR #53未merge**を維持。


## M37-P2 2026-11-02｜Workなし・ZIPなしのWindows直接作者編集起動を整備

- [作者用PowerShell単一ファイル](tools/g4c7_m37p2_launch_local_author.ps1)／[日本語手順](tools/G4C7_M37P2_LOCAL_AUTHOR_LAUNCH_README_JA.md)：v3真正BLEND固定SHA `536e451c763c4326421b13285abf1056a3a11d755028f8ff20b54b99b08a0249` から保護原本を変えず、Windows文書フォルダへ**個別の編集用コピー**を作成し、既存の二画面・作者パネル・3視点レビューのGUI登録を行い、Blender・エクスプローラーを起動する。コードは都市メッシュを自動生成しない。
- [Windows実検証 #41447267350 SUCCESS](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41447267350)：本物のWindows PowerShell構文・原本SHA・コピー・セッションmanifest・GUI用Python構文チェック成功。[GitクローンがないWindowsでもrawから単一スクリプトで原本を取得した検証 #41447810957 SUCCESS](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41447810957)。両者は`-PrepareOnly`での**準備**テスト、ユーザーWindows実Blender GUIの起動・3D作者制作とは区別。
- Work使用量のためWorkは使用しない。現在のChatから6 Luna/6.1 Terraへ実行モデル切替・ローカルデスクトップ直接操作はできない。Luna/Terraを利用できるユーザー側のローカル環境があって初めて実作者操作が可能。
- 新Blender都市実メッシュ0、実3視点ART未取得、全体ART HOLD／正式採用0、331人体/993足元とG0/S1/G1/G2/G3 NOT RUN、MakeCode費用未評価、Minecraft施工禁止、PR #53 Draft未merge、main変更禁止。これは**都市美術の完成ではなく、実造形に着手できるWindows側入口の実装**。詳しくは[統合引き継ぎ節22](docs/G4C7_M37P2_COMPLETE_INTEGRATED_HANDOFF_20261102_JA.md)。


## M37-P2 2026-11-02：Blender実起動後、WorkなしでローカルAIが明示的頂点を編集する限定実験を準備

- Windows Blender **5.2.1 LTS**がユーザーPC上で実際に起動し、既存v3原本と左右2画面・5コレクションが表示されたことをユーザーの真正スクリーンショットから確認。ただし都市メッシュは0件。ChatからユーザーWindows/Blenderを直接編集する機能はない。
- [技術詳細・制約・未検証事項](research/g4c7-b11-r5-d56/p2/d3s26/M37P2_LOCAL_LLM_VERTEX_AUTHOR_BRIDGE_NOT_ART_20261102_JA.md)、[ローカルAI明示的頂点データの検査・実Blender書出しコード](tools/g4c7_m37p2_local_vertex_author.py)、[省操作Windows PowerShell](tools/g4c7_m37p2_run_local_ai_vertex_trial.ps1)、[1ファイルだけダウンロードして起動できるWindows CMD](tools/G4C7_P2_AI_Trial_Start.cmd) を追加。
- 旧P1/O1の`patch/wall/bridge`や固定箱形状生成器の第三都市は作らない。**LLMが各ポリゴンの本物の頂点面を直接JSONとして作者提案し、5用途や非退化形・キューブ多用を検査**する試験。任意のLLM生成Pythonコードは実行しない。成功候補は元のBlenderとは別の`.blend`＋真正3Cycles画像を自動生成し、必ず**「LOCAL_LLM」作者・非GUI手作業・未承認のART HOLD**と区別する。不合格なら即停止。作品の良否を形状数やテストPASSで代替しない。
- [専用Blenderテストワークフロー](.github/workflows/g4c7-m37p2-local-llm-explicit-vertex-first-art-tech-smoke.yml) と [Windows準備ワークフロー](.github/workflows/g4c7-m37p2-windows-local-vertex-ai-first-art-prepare.yml) を新設。ただしGitHub Actionsが**実際にcompleted/successと確認されるまでは当工程の技術PASSは未確認**。このチャットからローカルモデル実行はできず、実都市のAI造形・作者3D制作・正式3視点ART審査は未実施。
- 全体ART HOLD／正式採用0／331人体993足元とG0/S1/G1/G2/G3 NOT RUN／MakeCode未評価／Minecraft world writes 0／main保護／PR #53 Open/Draft未merge／Work使用なしを固定。
