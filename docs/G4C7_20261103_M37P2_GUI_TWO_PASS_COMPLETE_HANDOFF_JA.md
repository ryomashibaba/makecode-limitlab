# MakeCode LimitLab / G4-C7 Orbital Commons — 2026-11-03 完全統合引き継ぎ（GUI 2回継続編集TECH実証後）

**本書は2026-11-03 JST時点での最新版の追加引き継ぎ正本。過去の歴史正本を置換・破棄せず、最新状態と旧不採用からの教訓を重ねる。** 逐語的な全チャットの複製ではなく、意思決定・不変憲章・工程・検査・成果物・未達成事項・次の行動を復元するための資料。

## 0. 新しいチャットの起動条件と正本の優先順位

- リポジトリ：**ryomashibaba/makecode-limitlab**。
- 研究ブランチ：**dev/g4c7-a17-monolithic-rift-fold-art-study**。**main変更禁止**。
- Draft PR：**#53**、Open/Draft/未merge。Ready for reviewやmergeの無断実行は禁止。
- 本書作成前の確認済みHEAD：**d66b71bee0a01d90fd2a7fc0ef321e301cc38cfc**。本書とSTART_HERE更新コミットの後は変わるため**このSHAにリセットしてはいけない**。
- 最新Verify LimitLab CI（上記HEAD）：**#41605731484 completed/SUCCESS**。
- 新チャット開始時は必ず研究ブランチの実HEAD、PR #53、最新CI、Artifacts、保護原本を改めて照合。旧CIのQUEUEDや旧文書の未完了表示を最新の事実として無批判に繰り返さない。
- 参照順：研究ブランチの [START_HERE.md](../START_HERE.md) → **本書** → [2026-11-03クラウド第一・モデル費用・品質方針](G4C7_20261103_CLOUD_FIRST_MODEL_COST_COMPLETE_HANDOFF_JA.md) → [2026-11-02 M37-P1〜P2完全統合引き継ぎ](G4C7_M37P2_COMPLETE_INTEGRATED_HANDOFF_20261102_JA.md) → [B10後の根本戦略/R0〜R5](G4C7_POST_B10_CRITICAL_STRATEGY_REVISION_JA.md) → [全歴史](G4C7_LIVE_HANDOFF.md)と個別証拠。
- 資料内の過去HEAD、当時のQueued、過去時点の「GUI実証不可」「Cycles画像未取得」は**歴史的時点の記録**。この文書の後述する現在の限定TECH成果と区別する。

## 1. 何を作るか：最終目標は「美しい本当の巨大未来都市」＋MakeCodeのみで施工

Minecraft Educationの**MakeCodeのみを最終施工経路**として、G4-C7 Orbital Commonsを巨大・高密度・独創的で実際に都市生活が成立する一体型未来都市にする。住居、日常的商業、公共交通/歩行、芸術・研究文化、**現役の宇宙機・衛星・ロケット関連の製造/組立/検査/搬送/揚重**、見学者と作業員の物理分離、都市全域の歴史性・都市的密度と地形対応を必要とする。

**一つの保存された真正3D都市**の中で、マクロ全景の街区構成と、実入口→街路→前室→生活室→外の窓、公開公共空間→工場見学/立入境界→実製造設備、研究/文化活動と立体動線を**並行して作者設計する**。外観だけ先に美しくして内部を後で加える、単体室内だけ造って大屋根で覆う、形の違う箱を橋で接ぐ、巨大な彫刻や低層キャンパスを都市と呼ぶことは禁止。

Blenderは現段階の真正作者原本であって**最終施工方式ではない**。ART候補が成立してから建築の作者判断と設計規則を抽出し、MakeCodeへの変換、施工費用、安全、異なる地形での再生成を別々に検証する。MinecraftAIBuilder・CELESTIAL HALO-9・東京CityGen・Skytreeとは別プロジェクトであり、各プロジェクトの縮尺・憲章・施工許可を流用しない。

## 2. 絶対に変更しない運用・安全・証拠の憲章

1. **ART-FIRST / QUALITY-FIRST**。美術的な完成を最優先。CI SUCCESS、レンダ枚数、Blenderの起動・操作、頂点/メッシュ数、局所歩行数字、テスト数、Pythonコード量はART PASSではない。**美術の正式採用を決めるのはユーザー本人のみ**。
2. **全体ART HOLD、正式美術採用0件。真正な新R1高品質都市候補0件。** 現工程はR1真正作者都市に未到達。技術PASSを美術採用へ昇格しない。
3. **Minecraft Educationの新都市施工・既存都市統合禁止、world write 0。** 安全・正式ART採用・MakeCodeとユーザー承認が成立するまで解除しない。旧一回USEDラッチの再利用も不可。
4. **main禁止、研究ブランチ限定、PR #53 Draft維持。** 旧原本/ワールド、BLEND・GLB・OBJ・PNG、ZIP、CSV、USEDラッチ、旧実機成功証拠、失敗証拠を保護。変更は別名/append-only、強制push/reset/旧HEADへの巻き戻し禁止。GitHub CI botの自動コミットを考慮し、各書込み前に実HEAD確認。
5. **正式安全QA契約：331人体サンプル／993足元サンプル、人体半幅0.65、足元相対+0.15〜+3.25、旧干渉上限45/331、未支持0/993。** 絶対に数値を緩めない。実人体掃引/頭上/支持床/階段/双方向通路/工場の公衆隔離/荷重/避難/防火/住居プライバシーは別々の独立検証。単なる接触や旧QA数値を全面安全と呼ばない。
6. **G0/S1/G1/G2/G3、正式331/993、MakeCode Fill/Clone/Place・地形・実機施工の新都市検証はNOT RUN/NOT EVALUATED。** Blender研究単位を無断で1m=1Minecraftブロックに換算しない。
7. **Chat＋GitHub主体。Workは事前の明示承認必須。** 無断でWork/クラウドPC/有料API/有料GPU/外注/新アカウントを使用しない。Solも本人の事前明示承認が必要。実機PCの勝手な操作、架空の操作・レンダ・保存・コストを宣言しない。
8. **ユーザー操作最小限。** ZIP往復、毎回のローカル実行、手動スクリーンショット、長い引継ぎの再提出を要求しない。ブラウザで見られるGitHubの画像・真正ファイルを優先。
9. **無意味なCI・工程番号の増殖禁止。** 失敗原因がわかった時だけ少数の修正をまとめて実行、完走/Artifactを検証してから次の工程。技術試験Suzanneを延々と追加しない。
10. 真正Cycles/Blender原本の画像、VTK等の「メッシュ形状代理」画像、AI画像・参考アート、GUIスクリーンショットを混同しない。GUIスクリーンショットで実変換を見た事実と、ネイティブ保存ファイルの独立再読込は別の証拠。

## 3. R0〜R5の固定工程（変更・再決定禁止）

- **R0 過去失敗の体系化**：真の保存原本/多視点/負例から、巨大板・箱・帯・壁・橋・チューブ・巨屋根・彫刻・薄い街区・反復塔がなぜ都市と生活を壊したかを記録。既存の限定TECHのみを継承する。
- **R1 真の作者による高品質な真正3D**：最大2方向の**質的に異なる**一体型都市を、実際の「都市遠景」と「住居/公共/工場/研究の生活断面」を**同一ネイティブ3Dで同時設計**。コードで作りやすい図形を主形態にしない。視点・用途ラベルだけでごまかさず、人が体験する場所の実物を作者編集する。
- **R2 厳格な絶対ART審査**：保存BLEND由来のAERIAL / PUBLIC_EYE / HABITAT_EYEの真正Cycles3視点で早期判定。不合格なら止める。有望作だけ地区密度、研究文化、工場の実製造、公共眼高、室内、高所等を追加する。2方向とも不採用なら第三の同型モデルは禁止し、作者方法/設計ブリーフを根本から修正。本人以外は正式採用しない。
- **R3 機能と安全**：美術的に本気で進める作品だけに、現実の入り口/床/階段/連続双方向人流、工場隔壁、住宅私界、全人体・足元支持・負例を適用し、正式331/993とG0/S1/G1/G2/G3へ進む。
- **R4 MakeCode変換・非施工コスト検証**：作者の構成法を生成規則に整理し、材料、方向付き階段、Fill/Clone/Place数、処理時間/メモリ、地形/形態劣化を独立検証。未計測時間・上限を推測でPASSにしない。ワールドへ書かない。
- **R5 正式ART・安全・施工方針が本人承認後に限るMinecraft Education施工**。現時点で必要条件は未達。

## 4. 大量の歴史から残す具体的失敗と反省

- **G4-C1 A1-R1** 約5分38秒・**G4-C6** 19工程はMakeCode現物施工の限定TECH PASS。旧成功を壊さないが、32同型建物・薄板の新都市美術は不採用。
- **A1〜A32**：峡谷/アーチ/巨大外殻と市民生活が分断。**A33〜A65**：採石場/倉庫/大屋根/彫刻/低層キャンパス回帰。**A66〜A83**：開口・床/階段・幾何と4視点が進歩しても棚塔・卵・小室列・板・道路として都市ART REJECT。
- **B0〜B11 / D3S**：線・用途ラベル・接触/経路スコアが高くても空白だらけの箱・リング・道路・長壁。D3S25で店舗入口11/11逆向き、階段頭上34/126干渉、工場階段とギャラリーに約13.75抽象単位の高さ差。このような実アクセス不成立を見逃すな。
- **M30〜M36**：室内外の連動・真正Blender・多視点・ファイルQAの限定技術成果。しかし巨大屋根、棚、外殻、薄い室、離れたキャンパスを都市としてART REJECT。真の全体密度と生活する局所空間を同時に設計しなかった。
- **M37-A〜J**：メッシュや機能の名前、頭上・通路の数字を増やしても区画間に「都市」が生まれない。M37-Jは実室/開口があっても板状工業団地、工場境界・住宅階段干渉でREJECT。
- **M37-K〜N**：保存Blenderの直接メッシュ編集、室⇄外観連動、原本保護、負例などTECHは一部有効。しかし**Lの長チューブ/Nのチューブ延命はART REJECT**。本命作者形態へ流用しない。
- **M37-O1・M37-P1**：本物のBlenderモデルとCyclesでも、巨大板・帯・壁・橋・暗い研究視点・暮らしの欠落でEARLY ART REJECT。パッチ/スラブ/壁押出しを繰り返す同種の第三案を禁止。
- **M37-P2ローカルLLM頂点大量生成**：Qwenの無効面/トポロジー、生成しやすい形へ退化。高価なクラウド品質を少額節約のため低品質ローカルLLMに置換しない。
- **M37-P2 cloud bpy統合作者実験**：本物のBLEND、Cycles4枚、CI成立でも、低密度の同型12塔・箱・筒状工場・机/棚中心。真正メッシュ227、2,576頂点、4,244三角、204/227が単純8頂点、12塔同形45頂点。**限定TECH PASS、当該案EARLY ART REJECT**。色調/照明の変更、塔やブロック追加で延命禁止。
- **M37-P2 Chat内独立GLB試験**：1,562メッシュ/55,526三角形へ増やしても彫刻/孤立キャンパス、巨大外殻が住戸/研究眼高を遮蔽。8視点VTK形状代理でEARLY ART REJECT。GLB/VTKはネイティブBlender/Cyclesと混同しない。
- **本質的反省**：「ART-FIRST」と言いつつ、実際には制作権を自動の簡単な図形生成器へ戻し続けた。**街を連続的に歩き、働き、住み、研究できる高密度建築都市そのものを直接作者制作する必要がある**。技術診断だけやって「進めた」と報告するのを止める。
- **CI連続pushの弊害**：PendingのBlender取得・GPU/GUI実行を大量の追随コミットでキャンセル・渋滞させ、品質進展を妨げた。コード改善・負例・証拠保管を一括処理し、実行を最後まで観測してから次を作る。

## 5. 2026-11-03：本チャット中に実際に到達した最新の限定TECH

### 5.1 保存真正Blender＋4枚Cycles（作品は失格）

- [クラウド本物Blender/Cycles run #41577471323](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41577471323) **SUCCESS**。Blender4.5.15によるBLEND生成、別プロセスでの再読込、真正Cycles4視点（AERIAL / PUBLIC_EYE / HABITAT_EYE / CULTURE_EYE）。
- GitHub研究ブランチへappend-only保存： [Cloud bpy保存真正原本と4画像](../artifacts/g4c7-m37p2-cloud-native-integrated-art-hold/6077fc44b78a7cacc94c68a67a7ebe2d3baebcb0/) 。原本SHA256：**7b4fb821e75946ad763692d3887fb9f8e5d63dda61221c18c2def160f1e3bc71**。
- [真正4視点美術審査](../research/g4c7-b11-r5-d56/p2/d3s26/M37P2_20261103_TRUE_CYCLES_FOUR_VIEW_FINAL_EARLY_ART_REJECT_JA.md)：大半が同型塔/単純地盤と水路、内部は棚/机/箱家具、工場設備は低密度。**当該作品EARLY ART REJECT**。TECHをARTへ昇格しない。

### 5.2 真正Blender GUI「読む」経路が成功

- [GUI X11読み取り専用CI #41597467506](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41597467506) **SUCCESS**。Blender内screenshot_areaは1×1黒だが、X11の実1600×900ウィンドウからBlender自身の領域座標を検査してMACRO657×783、LIVED661×783のピクセルを一致検証。初回Quick Setupは現時点の画面で解消。
- 関連コード：[X11 pixel bridge](../tools/g4c7_m37p2_x11_visual_context_bridge.py)、[11件の負例/改ざんテスト](../tests/test_g4c7_m37p2_x11_visual_context_bridge.py)、[読み取り回復監査](../research/g4c7-b11-r5-d56/p2/d3s26/M37P2_REAL_X11_GUI_PIXEL_RECOVERY_20261103_JA.md)。
- **GUIピクセルの取得TECH**でありAIの自主的作品編集やGUI内部APIの修復ではない。

### 5.3 真正Blender GUI「操作→別名保存→独立再読込」成功（1回目）

- [GUI入力CI #41599291594](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41599291594) **SUCCESS**、Artifact **13213069325**。実X11ウィンドウへxdotoolのF3 Add Monkey/GX8/S2を送信。Blender GUI Consoleは**メッシュ生成ではなくassertとsave_as_mainfileで保存**した。別Blenderプロセスで保存を確認。
- 1回目の真正BLEND：**139,802 bytes、SHA256 3279d909da13e5b09660dc170e8bb79b51a733611e4d1d1c02ea97f4f920ded8**。Suzanne **507頂点**、X=8、Scale XYZ=2。
- [成功の独立報告](../research/g4c7-b11-r5-d56/p2/d3s26/M37P2_REAL_GUI_SHORTCUT_EDIT_NATIVE_SAVE_INDEPENDENT_PASS_20261103_JA.md)。この1回目の原本はGitHub Actions Artifact保管であり、ブランチへ恒久保存したと虚偽主張しない。

### 5.4 同じ真正BLENDの**2回目**GUI視覚フィードバック・独立再保存も成功

- 最重要：[最終成功CI #41605230460](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41605230460) **completed/SUCCESS**。前回の保存済BLEND・実GUI画像をSHA固定して取得、BlenderのVIEW_3Dを開いて実マウスクリック+実キーボードで元のSuzanneを**X=8、Y=5、Z回転30°、Scale XYZ=1.3**へ更新。実画像で前後変化を目視。
- **失敗した途中run #41602792920、#41603430549、#41604040677、#41604589981**：GUIがConsole状態で再開、VIEW_3Dがアクティブでない、選択が失われる、Console keystroke saveに失敗、と原因を絞って修正。これらをPASS扱いしない。
- **成功への決定的修正**：保護元や前回原本ではなく**別の準備コピー**のエディタだけ事前にVIEW_3D復元し、メッシュはGUIでのみ変換。保存はGUI中のBlenderタイマーが変更値一致を検査してから新しい別名BLENDへ保存（メッシュをPythonが生成・変換していない）。
- 新たな保存BLEND：**M37P2_SECOND_REAL_GUI_NOT_ART.blend**、**140,135 bytes**、SHA256 **d0bf2c38bffd9684fe64aeb7890b37c29738610049212448738e67939a967472**。新BLENDを**別Blenderプロセス**で再読込し、Suzanne507頂点、X8/Y5/Z30°/Scale1.3、固定ART HOLD、安全未実施を確認。
- この4つの**本物の証拠は研究ブランチに恒久append-only保存済み**： [2回目のGUI原本/画像/JSON](../artifacts/g4c7-m37p2-gui-feedback-second-pass-TECH-NOT-ART/) 。内訳：M37P2_SECOND_REAL_GUI_NOT_ART.blend、GUI_BEFORE_SECOND_PASS.png、GUI_AFTER_SECOND_PASS.png、INDEPENDENT_GUI_STAGE2_RELOAD.json。
- 技術ファイル：[2回目GUI実操作](../tools/g4c7_m37p2_gui_feedback_second_pass.sh)、[独立再読込](../tools/g4c7_m37p2_gui_feedback_second_pass_verify.py)、[GUI変換観測後の保存](../tools/g4c7_m37p2_save_native_after_real_gui_edit.py)、[既存真正CI](../.github/workflows/g4c7-m37p2-gui-feedback-second-pass.yml)。
- **判定：同一ネイティブシーンを2回実GUIで編集・保存・再読込する「限定TECH閉ループ」が成立**。しかし**自律的にAIが画像を毎手理解して美術判断する能力、高品質都市の直接GUI造形、正式ART PASSは一切未証明**。Suzanneは単なるTECHの操作対象であって新R1都市候補ではない。これ以上Suzanne試験や空GUIの追加実験を続けない。

## 6. 保護対象、数値・仕様、証拠の取り扱い

- 最重要保護v3：artifacts/g4c7-m37p2-patched-native-author-editor-v3-NOT-ART/M37P2_DIRECT_AUTHOR_NATIVE_EDITOR_FIXED_REVIEW_V3_NOT_ART.blend
- 元v3 SHA256：**536e451c763c4326421b13285abf1056a3a11d755028f8ff20b54b99b08a0249**。この元ファイルは空の直接作者エディタ（新都市メッシュ0）。**絶対に上書きしない**。
- 旧G4-C1/G4-C6 Minecraft Educationワールド、実機成功証拠、A5〜A83/B/M37の歴史原本、保護ZIP/CSV、使用ラッチも残す。旧失敗美術を素材として無断採用しない。
- GitHub Actionsの一時Artifact（有効期限あり）と、研究ブランチの実ファイルを区別する。2回目保存原本のみ上述アーカイブに恒久保存した。
- 過去「BLENDが作れない」「GUIができない」という障害は限定的に解消された。しかし**本来の都市作品が作られたわけではない**。技術能力＝美術達成と解釈しない。

## 7. モデル、コスト、ユーザー負担の確定方針

- **品質優先／全クラウド第一候補**。美術の創作・本当の都市画像の批評をクラウドAI中心にする。**ローカルLLMに置換すると小幅な節約に対し大幅に作品品質を落とす可能性があるなら、全クラウドを選ぶ**。ローカルLLMは現状本都市美術の主作者にしない。
- **GPT-6 LunaまたはGPT-6.1 Terraが通常の第一選択**。美術構想/厳格な画像批評はLuna、通常のコード・GitHub/CI検証はTerraを基本とする（これはユーザー希望の使い分けであり、モデル品質の実測保証ではない）。
- **GPT-6.1 Solは高価なので、本当に不可欠と判断する工程だけ、具体的理由と期待できる美術改善、コストの不確実性を説明し、本人の明示事前許可を得た場合のみ使用**。モデル切替をこのChatが勝手にできると主張しない。
- Work、クラウドComputer Use、レンタルGPU、有料外部サービス、API従量課金、新規アカウントは**本人承認まで実行しない**。一方、既存GitHub Actions等で認められた無料/既存接続の研究開発はChat中心で進め、不要に毎回承認待ちで止まらない。
- ChatGPT Plusの制限/Work枠/外部GPU料金/API料金は混同しない。古い価格や未検証の節約率を断言しない。品質低下を伴う最適化は禁止。
- 作業の本当の成果は**GitHub正本に実ファイル・証拠・判断**を保存し、ユーザーはリンクから閲覧できる状態にする。スクショやZipを人間に毎回求めない。

## 8. 次チャットで行うべき「ただ一つの本当の開発の軸」

**R1の真の高品質都市を同一ネイティブ3Dで実際に作者造形し、真正Blender画像でEARLY ART判定を得ること**。2回目のSuzanne GUIテストは完了なので追加しない。

- **最初**：START_HERE・本書と歴史正本を読み、PR #53 HEADと最後の2回目GUIのGitHub保存実体があるか確認する。正式採用0、安全未実施を保持。
- **制作の着眼**：全体の市街地図/高密度街区/公共動線/居住の連続街並み、機能的で内部がある宇宙機製造工場・搬送と検査・見学者隔壁、研究文化施設と住宅の扉/前室/居間/窓を**1つの作者Blender原本で最初から統合**。高層・中層・低層の密度差、足元の店/看板だけでなく本物の立面、必要な上下アクセス。巨大彫刻の外殻や反復塔は最初から不採用。
- **制作方法**：既に証明済みの実GUI読み取り/キー入力/ネイティブ保存能力を、初めて意味のある建築造形とレビューに使う。小さなプリミティブ1個しか編集できないなら**高度な作者アート能力が未証明**と記録し、GUI技術テストを無意味に延命しない。Work/外部能力が必要なら承認を事前に得る。美術結果は真正保存原本と画像に必ず紐づける。
- **早期審査**：同一BLENDから最低AERIAL（都市と街区に見えるか）、PUBLIC_EYE（人が使う街路・工場公開部と境界）、HABITAT_EYE（玄関/室内/窓/生活）が写ることを確認。形が不合格なら即EARLY ART REJECT。そのあとで研究・文化・製造/工場の拡大視点や正式機能QAへ進む。
- **制作方向は最大2つ**。同じbox生成器のseed/係数違いを別案と呼ばない。2方向不合格なら制作方法/作者アクセスを見直す。未完成作品を「R1 PASS」「ART PASS」と呼ばない。
- **成果報告**：今回本当に変更したファイル/保存原本/画像/HEAD/CIに加え、①美術の絶対評価②街/公共/工場/研究文化/住宅の視認結果③正式QA・MakeCode・Minecraftの状態④次の大きな課題を簡潔に記載。「次工程へ」で計画だけ回答するのではなく、可能なら実ファイル/コードをGitHubへ保存して完了する。
- **コスト・質・負担**：CIの細分化、学習不要な長い空モック、ユーザーの毎回スクショ/ローカル操作を減らし、クラウド中心で質を上げる。Sol/Workの無断利用禁止は絶対。

## 9. 次チャットへの短い起動メッセージ

MakeCode LimitLab / G4-C7 Orbital CommonsをGitHubの最新正本から完全に引き継いで開発を再開してください。

リポジトリ：ryomashibaba/makecode-limitlab、研究ブランチ：dev/g4c7-a17-monolithic-rift-fold-art-study、Draft PR #53。まずルートSTART_HERE.md、2026-11-03の最新「M37P2_GUI_TWO_PASS_COMPLETE_HANDOFF_JA.md」、従来の2026-11-03統合方針・2026-11-02 M37完全統合引継ぎ・R0〜R5を読み、最新HEAD/CI/Artifactsを必ず照合してください。

2026-11-03には真正X11 BlenderのGUI取得・キーボード/マウス編集・同一原本の2回目GUI編集・別名保存・独立Blender再読込が実証され、最新証拠はartifacts/g4c7-m37p2-gui-feedback-second-pass-TECH-NOT-ARTに恒久保存済み（成功CI #41605230460）。ただしこれはSuzanne1個の限定TECHで都市美術の証明ではありません。これ以上空GUIやSuzanne試験を増やさず、R1の新規真正都市作者制作へ進んでください。

ART-FIRST/QUALITY-FIRST、R0〜R5固定、全体ART HOLD/正式採用0、正式331人体/993足元とG0/S1/G1/G2/G3 NOT RUN、MakeCode未評価、Minecraft Education施工・既存都市統合禁止、main/保護BLEND変更禁止、PR Draft/未merge、Chat＋GitHub中心、Work事前承認・GPT-6.1 Sol事前許可、基本はGPT-6 LunaまたはGPT-6.1 Terra、全クラウドと高品質優先・低品質ローカル置換禁止・ユーザー操作最小化を厳守。昔の箱・板・橋・チューブ・同型塔・低層キャンパス・巨大彫刻を再生産せず、真正BLENDの都市全景＋公共眼高＋住宅眼高、工場と研究文化と都市生活を同一3Dで作者制作して実画像審査してください。可能な限り実制作/保存まで進め、技術PASSをART PASSに格上げしないこと。
