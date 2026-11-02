# MakeCode LimitLab / G4-C7 Orbital Commons
## M37-P1 完了時点・M37-P2継続用 完全統合引き継ぎ正本

**作成日：2026-11-02 JST。これまでの決定事項・研究履歴・失敗・反省・技術証拠・安全契約・次工程を一体化したGitHub正本。過去の全チャットの逐語転記ではない。既存の歴史資料を上書きせず、最新優先順位を明示する。**

**重要：これは引き継ぎであって、美術の採用・新都市の施工・Workの実行承認ではない。**

## 0. 最短の再開結論と優先順位

- **新しいチャットの入口**は研究ブランチのルート [START_HERE.md](../START_HERE.md)。正本は [ryomashibaba/makecode-limitlab](https://github.com/ryomashibaba/makecode-limitlab) の **\`dev/g4c7-a17-monolithic-rift-fold-art-study\`**。mainに移らない。
- **直近完成工程＝M37-P1**。新規本物Blender原本、7真正Cycles画像、独立保存原本再読込・6負例・ハッシュアーカイブ。専用 [GitHub Actions #41351764632 SUCCESS](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41351764632)。旧の失敗 [#41351611157](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41351611157) は修正済み。
- **M37-P1は限定METHOD TECH PASS／絶対美術 EARLY ART REJECT**。巨大な板・壁・帯、ほぼ黒い研究視点、実生活の不在。前段のM37-O1もEARLY ART REJECT。**方向が異なる2つの真正3D不合格により、同種の自動プリミティブの第三案は禁止**。
- **次工程＝M37-P2、都市3Dを作る際の作者の形態決定権の再設計**。P1案の修繕・拡大は禁止。M37-P2の新しい真3D成果は本書作成時点で **NOT CREATED**。恣意的に「M37-P2完成」と記載しない。
- **全体ART HOLD／正式ユーザーART採用0件／正式331人体・993足元およびG0/S1/G1/G2/G3 NOT RUN／自由歩行・支持・構造・避難 NOT CERTIFIED／新都市Minecraft Education施工・都市統合は禁止／main不変更／Draft PR #53 Open・未merge／Workは事前明示承認制**。
- 最終照合した研究HEAD（新引き継ぎコミットより前）：\`50285ae9b7948d2404b223437c73efe88b4b8cab\`。**保存後HEADは必ず変わる。作業時はGitHub PR headとCIを読み直し、旧SHAへのリセット禁止。** この旧HEADの通常 Verify [#41352198482](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41352198482) は最初の調査時はQUEUED、その後の再照合で **completed/SUCCESS** を確認した。最新引き継ぎコミットのVerifyは別実行なので、次チャットで状態を再確認する。

## 1. 最終目的 — 何を作るプロジェクトか

Minecraft Education内で**最終的にはMakeCodeだけ**を施工経路として、人間が訪れ、歩き、学び、居住し、宇宙機を製造・研究し、芸術文化を育てられる、**巨大・高密度・独創的な一体型未来都市「G4-C7 Orbital Commons」**を実現する。

これは建物の寄せ集め、低層キャンパス、独立オブジェ群、巨大な彫刻、断面実験集合、道路模型ではない。遠景の密度差、公共入口眼高、街区、宇宙機製造、研究、住宅、文化、代表室内、高所眺望が**1つの真正3D原本で有機的に整合**し、人の活動が見える必要がある。

3D作者モデルそのものも最終成果ではない。美術的に有望な原本の作者判断を抽出し、地形・用途変化でも破綻しない再生成規則を後で実証し、さらにMakeCodeへの変換・安全施工を独立評価する。**施工容易性のため美術品質を犠牲にしない。**

## 2. 運用の固定指示（チャット移行でも解除しない）

1. **ART-FIRST / QUALITY-FIRST**。技術テストやメッシュ数の成果を美術採用と混同しない。美術の質は本当の3D画像の絶対評価によって厳しく判断。技術PASSでART PASSにはならない。正式ユーザーART採用の宣言者はユーザー本人のみ。
2. **ChatとGitHub正本を中心**とする。Work使用はChatより具体的な利益があり、ユーザーから**明確な事前承認があった場合のみ**。外注、無断ローカルPC操作、新しいアカウント作成を前提にしない。過去のZIP・長文・全履歴の再提出を求めず、GitHubを読み書きして引き継ぐ。
3. **mainへの変更、Draft PR #53のReady・merge、旧BLEND・過去研究ZIP/CSV・保護原本・旧USED一回ラッチ・Minecraft既存ワールドの上書き禁止**。原本はappend-only。研究ブランチ内でも作業前に現在HEADと同時開発の競合を確認。CI botの自動コミットを考慮し、古いSHAへ強制戻ししない。
4. **Minecraft Education新都市world write 0を維持**。正式アート・独立安全・施工計画・明示的な本人承認が成立するまで施工/旧都市統合を解禁しない。試験でも「既存一回施工ラッチ使い回し」をしない。
5. Blender bpy headless/CIによる制作は真正の保存3Dとして扱えるが、**GUIで手作業したと偽らない**。イメージ生成画像・2D説明図を保存BLEND由来の実写真と混同しない。
6. 成果が見えないなら工程番号だけ進めない。価値の低い試作は**少数の実カメラで早期ART REJECT**。深いQAや重いレンダリングを無駄な形に投入しない。必要な独立監査や負例は省略しない。
7. 他プロジェクト（MinecraftAIBuilder、CELESTIAL HALO-9、Tokyo CityGen等）の縮尺・方針・素材を無断流用しない。

## 3. 変更禁止の安全QA・施工契約

- **331人体サンプル／993足元サンプル、人体半幅0.65m、足元相対高さ+0.15〜+3.25m、旧人体干渉許容上限45/331、足元未支持0/993**。この数値の意味を緩めず維持。許容45は真の安全を自動保証する数でない。
- 正式G0/S1/G1/G2/G3と、床接触、局所レイ、メッシュwatertight、自由歩行、全身掃引、踏面/頭上、工場立入制限、荷重強度、避難、防火は**異なる検査領域**。名前をすり替えてPASSにしない。
- 閉塞、床抜き、支持断絶、階段破損、工場隔壁除去、プライバシー境界の消去などの**故意の負例**を独立監査と共に保存し、原本は一切変更しない。
- 現行M37-P1では正規331/993、G0/S1/G1/G2/G3、自由歩行、連続掃引、工場の防護性能、構造・避難が**未実行・未認証**。メッシュの見た目上の接続から認定しない。
- Blenderで使った**抽象研究単位を1m=1blockと勝手に換算しない**。現在案のMakeCode Fill/Clone/Place/向き付き階段コスト・時間・現実機能は **NOT EVALUATED/NOT RUN**。最終施工経路はMakeCodeのみ。

## 4. R0〜R5の正規全体計画（2026-10-28固定）

- **R0｜不採用と証拠の体系化**：箱、棚、キャンパス、彫刻、巨殻、道路、チューブを本物の固定カメラ画像と失格原因ごとに整理。既存Blender/安全/施工技術を造形の美術採用と切り離して再利用。
- **R1｜真に異なる最大2つの作者形態方向**：人間の活動・公共→工場見学/研究→文化/住居→高所への体験を決め、**全市街の粗い実3Dと代表生活断面の実入口/床/境界を同じ原本で並行制作**。最初に外殻だけ完成させて室内を後詰めするのも、一室だけ作って独立施設を橋でつなぐのも不可。
- **R2｜真正3Dの絶対美術審査**：全市街遠景/地区密度/公共眼高/製造・研究・居住・文化/内部/高所を同一保存原本から固定カメラで見る。場所と活動が実際に見えなければEARLY ART REJECT。2案とも失格なら**第三の同種プリミティブを自動生成せず制作方法の前提へ戻す**。
- **R3｜美術候補に限定した実機能・安全QA**：本物の室・扉開口・縦移動・工場スタッフ/見学者隔壁・居住の私界・実支持/連続人体掃引・独立負例、続いて正式331/993とG0/S1/G1/G2/G3。現段階では未実施。
- **R4｜MakeCodeへの可逆変換・非施工コスト**：Fill/Clone/Place・材料/階段向き・ブロック境界・地形干渉・処理上限を検査する。美術不採用形態を施工容易さで救済せず、未測定時間を推定値として断定しない。
- **R5｜本人正式採用後の実機安全施工と統合**：美術と安全とMakeCodeが全て実証され、ユーザーが明示的に許可して初めてMinecraft Educationで施工する。現在R5条件は満たされていない。

## 5. これまでの成果と不採用歴 — 何を繰り返してはいけないか

### 初期実機・A/Bライン
- **旧G4-C1 A1-R1**：Minecraft Educationの実施工約5分38秒。**G4-C6**：19工程、863 Fill/49 Clone/264向き付き階段/455点サンプルなどの限定技術実績。しかし32同型建築と巨大薄板などの美術は**不採用**。これは現都市の施工許可ではない。
- **A1〜A32**：アーチ、谷、外殻と実都市生活の分断。A32の公共主導仮説が実3Dへ定着せず。
- **A33〜A65**：採石場、大屋根、巨大彫刻、低層キャンパス、モール等へ反復。設計改革を宣言しても実体は簡単なプリミティブへ戻った。
- **A66〜A83**：Blender/Cycles、VTK/Trimesh、実扉/床/階段/レイが向上。A73/A75/A81/A82の局所技術は残るが、棚塔・卵彫刻・小室列・長壁/道路など都市ARTは不合格。
- **B0〜B11 / D3S**：占有マスク、支持意図、境界、実3D・QAを加えても箱、リング、巨壁、道路帯に回帰。D3S25の市場側入口11/11逆向き、階段頭上干渉34/126、製造階段とギャラリー高さ差約13.75研究単位など。詳細は[歴史原本](G4C7_LIVE_HANDOFF.md)。**歴史ファイル先頭のD3S20は最新ではない**。

### M30〜M36 — 技術は増えても都市美術は不採用
- **M30**：2案とも押出し箱と道路板、ART REJECT。M31：実入口・橋・斜路があっても低層キャンパス。M32：室⇄屋根連動でも巨大壁と棚。M33：用途5種でも街区が分断。いずれもART REJECT。
- **M34**：保存真正Blenderの頂点直接編集法、限定TECH。**M35**：208実メッシュ・9真正視点でも巨大屋根の4地区独立キャンパス、ART REJECT。**M36**：保護シーン/編集シーン各208の真正BLEND SHA256 \`be8d6eb0c37f58de4d677c12c4382f4f254ce51fe36e022946d4d9315301dc06\`、編集METHOD限定PASS、都市ART未制作。
- メッシュ数/工程/CIを品質の代理指標にしないことを確定。

### M37-A〜J — 順番や局所QAだけでは改善しない
- **A/B**：682反復メッシュや巨大帯87,721セル切削、EARLY ART REJECT。
- **C**：真正BLENDの旧シーン保持・直接編集METHOD PASS、ART HOLD。
- **D**：1,163メッシュ/名目113入口/72階段・9視点があっても棚と巨大空白、ART REJECT。
- **E**：363床の実接触を監査し180床接触成分、公共ゲート5床、113名目入口で公共床と直結する室3。**V1カメラ未評価matrix_worldバグにより無効、V2のみ有効**。
- **F**：公共床21枚の接触成分、106踏面など限定TECH PASS。黒い帯・棚でART REJECT、連続実歩行未認証。
- **G**：24箱・374装飾・実室0・真正ドア0。眼高492中43地点に体積重複。外形先行→内部空白の失敗。
- **H**：CIVIC BRAID A/Bの2D設計、Bのドア/重複/経路干渉。2D整合は実3D美術でない。
- **I**：10実室/164踏面でも共有壁0の分離キャンパスでEARLY ART REJECT。
- **J**：19実室・22共有壁・18真正開口でも板状工業団地、工場見学境界3欠陥、住宅階段頭上15干渉、ART REJECT。**A/Bの2方向失格を受け同じやり方の第三案禁止**。

### M37-K〜N — 保護する真正作者技術と、流用禁止の旧都市形状
- **K**：[原本](../artifacts/g4c7-m37k-verified-native-authoring-method-art-hold/)：室⇄外形を同一編集トランザクションで変化させる35実Blenderメッシュ、開口/吹抜/隔壁/負例。局所METHOD TECH PASS、全都市ARTではない。初期V1のbase64文字欠落修正の履歴も残す。
- **L**：[原本](../artifacts/g4c7-m37l-verified-native-city-master-art-hold/)：9作者断面から199メッシュ/13室、真正9視点。でも連続した巨大チューブと白い空洞でART REJECT。
- **M**：[原本](../artifacts/g4c7-m37m-verified-native-review-workspace-art-hold/)：M37-L199＋編集コピー199・9カメラ・巻き戻し・SHA監査。編集環境限定METHOD PASS。GUI手操作は未確認。初回保存シーン/実メッシュ名と草稿名不一致を修正した。
- **N**：[原本](../artifacts/g4c7-m37n-verified-native-maker-exposure-art-hold/)：本物のM37-Lコピー外殻10実メッシュを直接切除、工場の物理隔壁維持、見学床/ガード/支持5実物、固定9+補助2視点。専用[CI #41318630617 SUCCESS](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41318630617)。BLEND **4,120,845 bytes**／SHA256 \`0817bf8a9681e9380b8167e75ddc236dbcab18920b01298c5e405ed46752bdff\`。技術限定PASSだが巨大チューブの空洞が見えるだけで**ART REJECT**。外殻の切除/装飾による延命を停止。

### M37-O1〜P1 — このチャットで完了した最新研究
- **O1**：[真正原本](../artifacts/g4c7-m37o1-verified-native-activity-author-art-hold/) / [厳格審査](../research/g4c7-b11-r5-d56/p2/d3s26/M37O1_SAVED_NATIVE_FIVE_VIEW_EARLY_ART_REJECT_AND_AUTHOR_INPUT_RESET_JA.md)。旧チューブをコピーせず、到着/公共/工場/研究/住宅/文化/高所7用途を独立多角形の床/屋根/壁/実ドアで表現、6経路板、保存BLEND・5真正画像・9カメラ・3負例。専用[CI #41321512829 SUCCESS](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41321512829)。BLEND **1,091,100 bytes**／SHA256 \`7845343514b79067835ddbbd18aabf93439a391f4a2c0983227475b18331b2f1\`。**低密度の分離パビリオン群、公共/住宅が真っ暗でEARLY ART REJECT**。失敗原因：独立7用途の平面外形を押し出して橋で結ぶ設計入力が都市外観を支配。
- **P0**：[入力正本](../research/g4c7-b11-r5-d56/p2/d3s26/M37P0_SHARED_AUTHOR_DECISION_SOURCE_OF_FORM_V1.json) / [ガード](../tools/g4c7_m37p0_author_source_contract_guard.py)。工場クリアランス/研究採光/住宅私界/文化高所を複数用途の共同決定事項へ。6負例と公私・工場スタッフ経路の意図分離。専用[CI #41350862339 SUCCESS](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41350862339)。**これは形態の意図契約であり新BLEND/ARTではない**。
- **P1最新**：[真正原本](../artifacts/g4c7-m37p1-verified-native-interlocked-urban-author-art-hold/) / [7視点の詳細ART REJECT報告](../research/g4c7-b11-r5-d56/p2/d3s26/M37P1_NATIVE_SEVEN_VIEW_EARLY_ART_REJECT_AND_P2_AUTHOR_METHOD_RESET_JA.md)。P0の4作者判断が複数の本物メッシュへ伝播。Blender保存・再開/7真正画像/9カメラ/9幾何係数整合・6負例は専用[CI #41351764632 SUCCESS](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41351764632)。初回[#41351611157 FAIL](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41351611157)は\`mathutils\`を\`bpy\`前にimportしたため、後に修正。BLEND **1,005,323 bytes**／SHA256 \`ca402f8e58269535bd6838cc8e5201000e9bc137dc578f0751f76bcb0d3b262d\`。**限定METHOD TECH PASS／EARLY ART REJECT**。俯瞰は巨大平板壁・床・細帯橋、公共は巨大青灰壁、工場は単純ロケットと青い三角形板、研究はほぼ真っ黒、住宅・文化・高所も空白板。人間生活する高密度都市として失格。
- **M37-O1とM37-P1の2案は両方不合格**。ここで2026-10-28の「2案失格なら方法を変えろ」を発動した。**M37-P1へ壁の穴・窓・装飾・床・階段追加して再採用しない。同じ\`patch/wall/bridge\`主導の第三形態は禁止。**

## 6. 重要な因果診断 — 何故同じ失敗を百回以上繰り返したか

- **失敗の核心：「ART-FIRST」と言いながら、コードで作りやすいbox / extrude / plate / slab / bridge / band / ring / shell / SDF primitiveが外形を先に決めること。** 用途ラベル・室数・床面・安全メトリクスを増やしても、最終ARTは巨大壁/棚/キャンパス/空洞へ退化する。
- **外形→室内の順**では箱の中身が空白、**室内→外形の順**では複数低層施設のキャンパス。順序だけ逆転しても解決しない。全市街粗形態と人の代表実断面を1原本で**同時に作者判断**する。
- **用途と形態の連動だけでも不十分**。P0のグラフ整合とP1の数値からメッシュへの伝播が成立しても、美術は板・壁・帯。作者の**3D造形と生活体験の実体**が決定権を持つ必要がある。室の数や開口の数は、室の深さ・採光・意味・人の移動を保証しない。
- 3D原本の真正ハッシュ、9カメラ、独立QA、負例は**改竄や技術欠陥を検出するための資産**で、美しい都市を作る自動機構ではない。ソースの偽り・V1の視点行列・base64破損・名前違い・CI失敗は記録して再発防止する。
- 人間の眼高画像が真っ黒、巨大無地壁、何もない広大デッキなら、カメラを都合よく動かして失敗を隠さず、画面に露出した欠陥自体を不採用根拠にする。
- 質的に違う2案でも不合格なら**同じジェネレータに異なるパラメータを与えた第三案を作らない**。美術上の前提と作者への入力を改める。
- GitHub正本を使うメリットを守り、チャット移行ごとに古いZIPを作り直す、長文を逐語貼る、ユーザーへ大量操作を求める運用へ戻らない。

## 7. 次の正当な工程 M37-P2 — 創作方法を変える（新3Dは未制作）

**現段階は新たな単純幾何の制作ではなく、美術作品の作者性・人間活動を根本入力とする造形方法の実証へ移る。**

必須の結果と手順：

1. **造形設計の権限を書き直す**：旧P1の\`patch/wall/bridge\`生成規則やP0の用途ノードだけでは外形を決めさせない。作者が3D形態と実生活断面を同時に編集する原本を主とし、コードは保存・監査・再現/施工検証の補助へ格下げする。Work/GUIなど許可が必要な手段は**先にユーザーの明示承認を得る**。Chatだけでできる方法検証やGitHub保存は実行可能。
2. **作者編集する1つの一体都市断面の必須内容**：来訪者が宇宙機製造の実作業/機器密度を見られ、物理的に工場職員専用域から分離。研究と文化は自然採光・本当の床/吹抜・縦動線・共有壁で結ばれる。住居は奥行ある生活室と私的玄関、街並みに開く窓を持つ。公共到着から高所の都市眺望まで、同じ街区で体験がつながる。
3. **マクロと生活断面を同時制作する**：都市の遠景の地区密度差と、代表的な居住/工場/研究の実床を同じ原本に保持。外観完成→後詰め内部、局所完成→橋で施設追加、どちらも禁止。単独高層オブジェ、巨大彫刻、巨大殻、道路板を都市として採用しない。
4. **まず最小の美術資格検査**：既存の固定失敗視点を基準に全景・公共眼高・住宅内観を同じ保存3Dから直接確認し、制作する価値があるか判断。品質が上がらなければ即停止し「何が原因か」を原本とともに記録。追加の細部量産はしない。
5. **品質が有望な場合のみ**：製造・研究・文化・高所を含む全9尺度真正カメラから画像レビューし、保護BLEND・再読込SHA・独立編集/戻し/負例を記録。その後にだけ正規安全QAとMakeCode非施工コストへ進む。アシスタントは正式ART採用宣言をしない。
6. **ソースの可再生成性**：もし真に美しい都市が作者編集で成立したら、何が造形の中核判断だったかを取り出して、別地形/用途への再生成が美術を壊さないかを後に試す。「手作りBlender完成」でプロジェクト成功としない。
7. **作業の停止条件**：P1型巨大壁/板/帯が再発、実生活見えず、代表視点黒、原本とレンダが違う、正式QAを走らせないまま安全と主張、未許可Work/施工に踏み出す場合は必ずSTOP/HOLD。

**引き継ぎ時の優先**：GitHubの原本と最新状態を読み、P2の「方法変更」と実際に品質が改善する制作を進める。次チャットで再び方針の再決定や、未制作P2を完成扱いしない。

## 8. GitHub証拠索引（正本優先）

- [ルート START_HERE](../START_HERE.md) ／ [2026-10-28固定戦略](G4C7_POST_B10_CRITICAL_STRATEGY_REVISION_JA.md) ／ [M37-Nまでの旧統合引き継ぎ](G4C7_M37N_FULL_HANDOFF_20261102_JA.md) ／ [研究歴史12万字超](G4C7_LIVE_HANDOFF.md)
- [M37-P1真正BLEND/7視点/検査原本](../artifacts/g4c7-m37p1-verified-native-interlocked-urban-author-art-hold/) ／ [M37-P1 ART REJECT詳報](../research/g4c7-b11-r5-d56/p2/d3s26/M37P1_NATIVE_SEVEN_VIEW_EARLY_ART_REJECT_AND_P2_AUTHOR_METHOD_RESET_JA.md)
- [M37-O1真正BLEND/5視点](../artifacts/g4c7-m37o1-verified-native-activity-author-art-hold/) ／ [M37-O1 ART REJECT詳報](../research/g4c7-b11-r5-d56/p2/d3s26/M37O1_SAVED_NATIVE_FIVE_VIEW_EARLY_ART_REJECT_AND_AUTHOR_INPUT_RESET_JA.md)
- [M37-P0作者意思決定入力](../research/g4c7-b11-r5-d56/p2/d3s26/M37P0_SHARED_AUTHOR_DECISION_SOURCE_OF_FORM_V1.json) ／ [ガード](../tools/g4c7_m37p0_author_source_contract_guard.py)
- [M37-N真正実外殻切除アーカイブ](../artifacts/g4c7-m37n-verified-native-maker-exposure-art-hold/) ／ [M37-M編集/巻き戻し](../artifacts/g4c7-m37m-verified-native-review-workspace-art-hold/) ／ [M37-K室/外形作者連動](../artifacts/g4c7-m37k-verified-native-authoring-method-art-hold/)
- [PR #53](https://github.com/ryomashibaba/makecode-limitlab/pull/53) ／ [専用P1 Actions](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41351764632) ／ [専用P0 Actions](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41350862339)

**注意：M37-G/H/I/Jの主GLB/PNG/検査パッケージは過去チャットのZIP主体のものがあり、GitHubに本体全点があると偽らない。GitHubで存在を確認できたアーカイブを優先。**

## 9. 新しいチャットで必ず行う確認と報告方式

1. [START_HERE](../START_HERE.md) → **本統合引き継ぎ全体** → 固定R0〜R5 → M37-P1不採用審査と真正アーカイブを取得。
2. 研究ブランチ最新HEAD、PR #53のhead SHA・Open/Draft/未merge、最新専用Actionsと通常Verifyを**再取得**。この文書中の旧SHAを現在のHEADとして誤認しない。
3. ART HOLD／正式採用0／正式331/993・G0/S1/G1/G2/G3 NOT RUN／Minecraft書込み禁止／main保護／Work事前承認を先に固定。
4. 次の実作業はM37-P2。出来る部分のGitHub・コード・原本検証を行い、実行できないGUI作業を成功と詐称しない。Workはユーザーに**事前承認**を得る。長文/ZIP再提出なし。
5. 毎工程報告は **(a)絶対ART評価、(b)本当に成立した活動/実室/接続/支持、(c)MakeCodeコストと未測定、(d)GitHub実原本/CIとSHA、(e)今の方法を続けるかSTOPか** を区別する。
6. 新しい結果が出たら、**本書をappend-only追補、START_HEREを最新入口として更新**。旧資料・過去ART REJECT・検査失敗は消さず、別案の成果と混同しない。

---

## 新チャットへ送る短い引き継ぎ指示

> **MakeCode LimitLab / G4-C7をGitHub研究ブランチのSTART_HERE.mdとリンク先のM37-P2完全統合引き継ぎから再開してください。最新HEAD・Draft PR #53・CI・M37-P1の真正Blender原本/7画像を確認し、全方針と失敗記録を継承してください。M37-O1/P1はEARLY ART REJECT、全体ART HOLD・正式採用0・安全QA未実施です。M37-P2の作者造形方法切替へ進み、旧板/壁/橋の第三案、Minecraft施工、main変更、未承認Work、長文/ZIPの再提出は禁止です。**

---

## 10. 2026-11-02 JST M37-P2 初回実行追補（美術モデル未制作／全体ART HOLD）

**新しいM37-P2真正都市BLENDは依然NOT CREATED。これは美術制作の達成報告ではない。** 旧研究の第三プリミティブ案を生成せず、GitHub正本を読み直し、M37-P1の真正PNGと現行作者ソースを再精査した。

### 新しく実測した負例：研究カメラが既存厚壁の内部にある

- 保存P1真正画像 `M37P1_RESEARCH_EYE.png` はほぼ全面黒。生成コード中、カメラ `RESEARCH_EYE=(40,-3,37)`、閉じた厚壁 `EAST_RESEARCH_MAKER_WING` の中心線 `(54,-69)→(41,0)`、厚さ `3.5`、垂直範囲 `z=3..62`。
- カメラから壁中心線への水平最短距離は `1.538155688...` 研究単位、半厚 `1.75` より短く、線分への垂線係数 `0.960649...` は0..1以内。z=37も壁内。**保存ソースにおいてカメラが閉じた実壁の体積内部に存在することを幾何で確定**。黒画像の主要原因をこれが説明する可能性は非常に高いが、実レンダ全要因の鑑別は未実施。
- 直接確認したP1 AERIAL、PUBLIC_EYE、RESEARCH_EYE、HABITAT_EYEは、巨大板壁・開放空白・黒視点を示す。旧EARLY ART REJECTは維持。P1のカメラを修正してP1美術を救済する操作はしない。
- その根因とは別に、P1作者コードの幾何作成主要API `patch()` / `wall()` / `bridge()` が外形の選択肢を大型平板・厚壁・帯状連結へ縮退させていた。数値連動は作者3D美術の決定権の回復ではない。

### GitHubへ追加した再発防止の実物（**ARTではない**）

- [`tools/g4c7_m37p2_native_camera_inside_solid_audit.py`](../tools/g4c7_m37p2_native_camera_inside_solid_audit.py)：保存Blenderの真正カメラと閉じた実メッシュに対する三方向ray parity検査。純PythonでP1の具体的な既知不良を再現する `--self-test` を実装。非watertightの開いた面は認証対象外と明示。画像美術・実歩行・安全を認証しない。コミット `3981db2306bed2da7df5afa5b4699214feac3eb7`。
- [`g4c7-m37p2-camera-solid-negative-control.yml`](../.github/workflows/g4c7-m37p2-camera-solid-negative-control.yml)：不変のP1真正BLEND SHA256 `ca402f8e...` を確認し、bpyで原本を再開、既知の壁内カメラを**期待される負例として検出**する独立read-onlyジョブ。原本・main・Minecraftには書き込まない。追加コミット `6d9ca1b122bf1af55ba4a398ceee80df1d0471db`。
- 専用 [Actions #41353940198](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41353940198) は作成直後の照合で **QUEUED / NOT YET VERIFIED**。成功と断定せず次回再照合する。

**次工程の有効条件は変わらない。** 旧patch/wall/bridgeを少し替えてもう一都市出さず、作者が真正BLEND上で都市全体の粗い姿と代表的な生活・製造断面を同時に編集した原本を必要とする。GUI/Workは明示的事前承認がないので実施していない。未制作のP2を完成やART合格と呼ばない。全体ART HOLD、正式採用0、331/993・G0/S1/G1/G2/G3 NOT RUN、Minecraft world writes 0、PR #53 Draft維持、main変更禁止。

---

## 11. M37-P2 非生成型Blender作者原本レビュー経路の実装（2026-11-02 JST）

**開発進捗分類：制作方法の実装。新しい造形原本・真正3D美術作品は依然NOT CREATED、ART HOLD／正式採用0。** 旧P1のpatch/wall/bridge補修や第三の自動プリミティブ都市を作らない方針を継続した。

- [`tools/g4c7_m37p2_author_native_early_review.py`](../tools/g4c7_m37p2_author_native_early_review.py) を新規保存。**Blender側にすでに直接編集・保存された新しい作者BLENDを入力**し、同じ保存原本から `P2_CAMERA_AERIAL` / `P2_CAMERA_PUBLIC_EYE` / `P2_CAMERA_HABITAT_EYE` の3真正Cycles画像を生成し、画像SHAと原本SHAを記録する。**このスクリプト自身にはbpyメッシュを作る処理・形を決めるプリミティブ生成処理・.blend保存処理がない。** 同一の作者原本内に市街全域と実生活断面を並行で制作する実作業は今後必要。
- 実施前提：直接作者入力の宣言、旧不採用造形未流用、ART HOLD、正式採用0、正規331/993 NOT_RUN、MakeCode NOT_EVALUATED、Minecraft FORBIDDENの各シーン属性。宣言は本人の実造形由来の証明ではなく、**実際の原本・画像を人間が検証する必要がある**。入力メッシュ・3カメラ欠落は拒否する。
- 禁止入力：M37-O1/P1/Nの既知SHA原本、旧M37L/N/O/P1メッシュ命名を含む原本。P1の複製を単に別名にしてP2と称してはならない。既存の非空レビュー出力ディレクトリへの上書きも拒否。
- 前回実装した閉じた実メッシュへのカメラ埋没検出を**先行ゲートとして再利用**。壁内埋没があれば3視点描画を開始しない。開いたメッシュは陰性証明にならない旨をレポートへ記載。
- [P2独立負例Workflow](../.github/workflows/g4c7-m37p2-camera-solid-negative-control.yml) に本ツールの純Python self-test（9拒否条件）と非生成ソース静的検査、既存P1の壁内カメラ再読込負例を追加。**このCIはMETHODの回帰検査だけでありARTの採用・新規美術原本制作を行わない**。
- 主要コミット：`e8d32d61f699e2a3fd0cbdfd449218e802eac0b4`（新審査経路）、`dcd78b3e03b3516d3b3f7230788b780b6c5f4317`（旧原本SHA・メッシュ接頭辞拒否、レビュー上書き防止）、`def0b9efe23324208fc66e6ba8f9352ef72fd284`（CIテスト統合）。
- [最新版専用Actions #41354779183](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41354779183) は初回確認でQUEUED、**SUCCESS未確認**。旧 #41353940198 はconcurrencyによるCANCELLEDであり成功と書かない。

**この方法は必要条件の整備であって、十分条件の達成ではない。** P2の実都市・生活形態の入力には、Blenderで本人/承認された作者が実3Dを直接編集する必要がある。このチャットではBlender GUI・Work・外注・Minecraft操作を実行していない。Workは従前どおり事前明示承認が必要。新3D未制作の段階で安全QA、MakeCode施工コスト、R3〜R5への昇格はしない。

---

## 12. M37-P2直接作者Blender空スタジオの実装・真正保存試験（2026-11-02 JST）

**重大な区別：これは美術作品ではなく新規作者が直接3D編集できる「空」の制作原本用技術。M37-P2新都市の真正メッシュと美術画像は依然NOT CREATEDであり、ART HOLD／正式採用0のまま。**

- [`tools/g4c7_m37p2_direct_author_studio.py`](../tools/g4c7_m37p2_direct_author_studio.py) を新規実装。既存M37-L/N/O1/P1の拒否された造形・コレクション・メッシュをコピーしない。Blenderの空シーンに6つの制作・カメラ用コレクション、全景・公共眼高・住宅眼高の**暫定**3カメラ、ART/Safety/Minecraft固定属性、埋込のBlender操作パネルを持たせる。都市形態のメッシュ生成関数を持たず、初期の本物のメッシュ数は意図的に0。これは品質の達成ではない。
- 作家本人のGUI直接編集では都市全域粗形と製造・研究・住居・文化を含む代表生活断面を**同時**に同原本で造形する。新規独立原本の実メッシュを5内容別コレクションに置き、人の体験を表現する。カメラを作者が確認するまでレビュー準備を許可しない。レビュー提出に成功しても正式ART PASSには一切ならない。旧形態を換名コピーしてP2にしない。
- 先の[非生成型真正3視点審査](../tools/g4c7_m37p2_author_native_early_review.py)と連結。新作者の原本だけ受け取るよう、カメラの作者承認・作品制作段階・同一原本内の都市全景／公共製造分離／研究文化／住宅を示す**別々の実メッシュの存在**を必須とする。ただし形状品質、実支持、避難、歩行、独立した制作者履歴をこの属性だけで証明できない。
- [.github/workflows/g4c7-m37p2-empty-direct-author-studio-native.yml](../.github/workflows/g4c7-m37p2-empty-direct-author-studio-native.yml) で真正bpy4.5を用いた空Blender原本の作成、別bpyでの保存原本再読込、0メッシュ／3カメラ／ART HOLDの独立確認、**ARTとしてでなく空スタジオとしてappend-only保存**を設定した。
- 初回CI [#41359593395](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41359593395) は空Blender `scene.world=None` の背景色設定が原因で **FAIL**。新規原本は保存前に停止した。ソースに明示的World初期化を加え[再試行 #41359669304](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41359669304) を開始。**追補作成時点ではQUEUEDでありSUCCESSと断定しない**。今回追加のコミット `9716d86f8b72bd4e320544bf3009bdd4b4affbf0`、`f055e739c7226250b1c09e5647c9fca01946f666`、`9534896a59653ea76c7ae0c15f22c4dc3d7dfc0d`、`415efeb049dc26e3fcc7c368be0e3fe4a906547b`。
- **次工程の正当性**：空原本ではなく、Blender GUI/直接編集による都市粗3D＋実生活断面の作者造形を現物として成立させ、同一保存BLENDから全景／公共／住宅の真正画像を先に批評しなければARTの前進はない。未承認Workは使わない。旧P1自動プリミティブの第三の試案を作らない。

固定安全契約331/993（人体半幅0.65、足元+0.15〜3.25、干渉上限45/331、未支持0）、G0/S1/G1/G2/G3未実施、Minecraft書込み0、MakeCode未評価、main保護、Draft PR #53維持、ART採用0。

---

## 13. M37-P2 直接作者スタジオの視点証明抜け道を修正（2026-11-02 JST）

**美術成果：未制作、ART HOLD、正式採用0。** 保存空スタジオ（真正BLEND 429,824 bytes／0実メッシュ）は[専用CI #41359859014](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41359859014)でSUCCESS。M37-P2の既存負例CI [#41354779183](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41354779183)もSUCCESS。これは前段の正確な再照合であり、都市ARTの前進と同一視しない。

### 修正したレビュー入力不正

- 空スタジオに保存されている3つのカメラは **PROVISIONAL（位置暫定）** で、デザインした市街と住宅・公共入口に対応する保証がない。一方、前版の真正早期レビューは `P2_CAMERA_VIEWS_AUTHOR_APPROVED=true` という宣言を受け取るだけで、初期位置のままでも審査へ進める危険があった。
- [`tools/g4c7_m37p2_author_native_early_review.py`](../tools/g4c7_m37p2_author_native_early_review.py) に、初期全景・公共・住宅のカメラ位置と保存された実位置を比較するゲートを実装した。**各カメラが空スタジオの暫定位置から少なくとも1抽象研究単位移動していなければ拒否**。カメラ位置だけを変更したことが良質な視点・美術や直接作者編集の証明になるわけではなく、正式ART判定は必ず真正画像で行う。
- Pure Python self-testで、全カメラ暫定位置・公共カメラだけ暫定位置の負例と3カメラ移動例を検証。GitHubコミット `cfe8a8ba548c8bfd1c349203d6a5b792628f20b6`。
- [専用CI #41374480855](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41374480855) **completed/success**。通常Verifyも [#41374480896](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41374480896) **completed/success**。これらは限定METHODの検査に過ぎない。

**次に必要な工程は新しいGUI直接編集の作者原本で都市粗形と代表生活断面を並行制作し、実際のAERIAL／PUBLIC_EYE／HABITAT_EYEの絶対美術を審査すること。** 本チャットではBlender GUIもWorkも実行していない。新しい第三の自動プリミティブ都市は作らず、M37-O1/P1のEARLY ART REJECT固定。331人体／993足元、正式G0/S1/G1/G2/G3未実施。MakeCodeコスト未測定、Minecraft施工禁止、main変更禁止、PR #53 Draft/未merge、Work事前承認制は不変。

---

## 14. M37-P2：都市全景と生活断面の「同時直接編集」GUI（2026-11-02 JST）

**分類：作者編集環境の機能実装。新しい真正3D都市美術の制作ではない。ART HOLD／正式採用0件は不変。**

- [`tools/g4c7_m37p2_parallel_author_view.py`](../tools/g4c7_m37p2_parallel_author_view.py) を保存。真正BlenderのGUI 3D View内で、同一シーンを都市全景（AERIAL）と人間視点（PUBLIC_EYEまたはHABITAT_EYE）の2つの編集ペインに分割し、保存カメラを参照して編集ビューだけを並行設定できる。両ペインは同じ編集可能な真正Blender原本を参照する。カメラ・メッシュ自体の自動変更はしない。
- この機能は旧P1の`patch/wall/bridge`生成コードを延命せず、P2の核心「外観を先行完成させる／内部を後詰めするのではなく、全市街と生活断面を同じ原本で同時に作者造形」の作業方法を直接支援する。使う側が本物の3Dを制作しない限り作品はゼロである。
- 固定ART HOLD／正式採用0／正式QA未実施／Minecraft禁止のシーン属性、真正P2保存カメラの存在をGUI操作の前提条件として検査。空スタジオ原本を変更しない。GUI操作の成功はヘッドレスでは検証できないため、**実際の編集二画面挙動・美術はNOT TESTED**と分離する。
- [専用Actions](https://github.com/ryomashibaba/makecode-limitlab/actions/workflows/g4c7-m37p2-parallel-native-author-ui.yml) は保存済み空真正BLEND SHAを確認したうえで、Blender Python 4.5でアドオンの登録・解除、固定条件の故意改変検出、メッシュ0／原本不変を独立確認する読取り専用ジョブ。作成時は**未完了**、後続で結果を確認する。
- 最新作業コミット：`50a82c89ac32d2ead8cc70e60c66b7a5613b0d4c`（GUIアドオン）と`6062ca0ddb37628072901d1548f326c6cd0e302c`（専用検証）。原本・main・PRのDraft状態を変更しない。

**直近の制作ブロッカー：** GitHub ActionsのBlenderはヘッドレスで、作者が3Dを視覚的に直接造形するBlender GUIをChatの現行環境では操作できない。Workは事前明示承認制であり未承認のまま使わない。「Pythonで生成しやすい都市」を第三案として作らず、本人または承認された実GUI作者編集を待つ。これまでの同型案を増やすのでなく、次に必要なのは一つの新規真正BLENDの**美術そのもの**である。

---

## 15. M37-P2：空作者スタジオを「単一真正BLEND GUI作業原本」に統合（2026-11-02 JST）

**成果分類：作者作業環境。都市美術そのものではない。ART HOLD／正式採用0、正規331/993・G0/S1/G1/G2/G3未実施、Minecraft施工禁止。**

- [`tools/g4c7_m37p2_bundle_direct_author_workspace.py`](../tools/g4c7_m37p2_bundle_direct_author_workspace.py)：固定SHA `d13e17fb59763a0719b5a91ed80043dade0f40ea65b7a29eba4e5bbfb9545041` の真正空作者BLENDを読み取る。既存原本を上書きせず、GUI二画面編集用Pythonと3視点レビュー用PythonをBlender Textとして埋込んだ別の**新しい保存BLEND**を作る。全新規都市メッシュ数は0のまま。
- [専用CI](https://github.com/ryomashibaba/makecode-limitlab/actions/workflows/g4c7-m37p2-integrated-native-editor-workspace.yml)：Blender 4.5で新たな原本を保存し、別プロセスで読み直して埋込Text原文SHA、空の実メッシュ、固定3カメラ、原BLEND不変、ART/安全/施工禁止を検査。成功した場合に限り `artifacts/g4c7-m37p2-integrated-native-author-workspace-NOT-ART/` へ追記保存する。**初回調査時はActions #41390131345 QUEUED、技術完了と誤報しない**。
- GUI自動起動・GUIでの真正立体造形・人間の活動の美術的完成・レンダリングは一切実施しない。この統合原本は「同じ作品を全景と人間眼高で直接編集する作者の作業効率を高める器」であって、実際の高密度都市そのものではない。
- 主コードコミット `3a6557f7f67a014006286ea3705e760cbdce4aad`、CIコミット `3ce8b21439f3dca1ca2c845b8e96252061ec9143`。GUI/Work使用事前明示承認制、main禁止、PR #53 Draft・未merge、ART FIRSTを維持。

**次のブロッカー／実制作：** 作者が直接Blender GUIで市街マクロ・造船活動/見学と職員隔壁・研究文化共有断面・生活室を一体原本に並行編集する。現環境でGUI操作が未許可のため、勝手に旧`patch/wall/bridge`主導の第三作品を生成して代行しない。真正3画像が揃うまでは美術候補へ昇格させない。

---

## 16. M37-P2 統合真正Blender GUI作者作業原本を保存済み（2026-11-02 JST）

前節15のQUEUED段階から更新：**専用GitHub Actions [#41390131345](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41390131345) はcompleted/SUCCESS**。実保存と別Blenderプロセスによる再読込、埋込ソースSHA、原本不変、ART HOLD、都市メッシュ0、カメラ3、負例検査を満たした。CIが追記コミットした真正原本は以下のとおり。

- [新しい統合空作者原本](../artifacts/g4c7-m37p2-integrated-native-author-workspace-NOT-ART/M37P2_INTEGRATED_EMPTY_ARTIST_WORKSPACE_NOT_ART.blend)：491,214 bytes、manifest SHA256 `6ca727def08cce9220dbde59f5836248cb5d0def39c7f375c9308af1461ee904`。
- [manifest](../artifacts/g4c7-m37p2-integrated-native-author-workspace-NOT-ART/M37P2_WORKSPACE_BUILD_MANIFEST.json)：元の空原本 `d13e17fb59763a0719b5a91ed80043dade0f40ea65b7a29eba4e5bbfb9545041` の不変を保存。GUI二画面用Textと作者3視点レビュー用Textを別の真正BLENDに埋め込んだ。
- **作品としての成功ではない**。新原本の実都市メッシュは0、実公共入口・実居室・実工場設備・同一城市の生活活動・美術画像は未制作。元のテンプレートも書き換えていない。**GUI上の実2画面操作・直接モデリングはまだNOT TESTED**。

今後の正当な次工程は、作者がその同じ真正BLENDを直接編集し、都市マクロと代表生活断面の美術実体を同時に制作し、3真正視点で絶対品質を評価すること。コードによる第三の旧`patch/wall/bridge`美術を作って代行しない。Workは事前明示承認、main変更禁止、PR #53 Draft/未merge、ART HOLD、正式採用0、331/993・G0/S1/G1/G2/G3 NOT RUN、Minecraft world writes 0を維持。

---

## 17. M37-P2 単一BLENDでの真正3視点レビュー実行経路を修正（2026-11-02 JST）

**現時点の美術判定：ART HOLD、正式採用0。新市街の直接造形未実施、都市メッシュ0の空編集スタジオである。**

前節16で保存した単一真正BLENDは二画面GUI用Pythonと3視点レビュースクリプトを内蔵していたが、**内蔵レビューのCLIソースは原則として隣接Pythonファイルを検索し、Blender Text Editorから直接起動することも不適切**という実操作上の欠陥があった。

修正・実装は以下。

- [`g4c7_m37p2_author_native_early_review.py`](../tools/g4c7_m37p2_author_native_early_review.py)を変更。サイドカーの監査.pyが存在しない場合、BLEND内の`M37P2_CAMERA_INSIDE_SOLID_AUDIT.py` Blender Textから同じカメラ実メッシュ埋没判定をロードできる。
- [`g4c7_m37p2_one_file_early_art_review_gui.py`](../tools/g4c7_m37p2_one_file_early_art_review_gui.py)を新規作成。作者が別名保存・再読込済みの真正BLENDから、GUI専用ボタンで3枚のCycles真正画像を審査用に描画し、独立ART判定に提出可能にする。旧空原本・元メッシュの上書きは行わない。保存されていない編集、空テンプレート、レビュー用コード欠落、元ソース改変は明示拒否。
- [`g4c7_m37p2_integrate_standalone_review_workspace_v2.py`](../tools/g4c7_m37p2_integrate_standalone_review_workspace_v2.py)：v1真BLEND SHA `6ca727def08cce9220dbde59f5836248cb5d0def39c7f375c9308af1461ee904` を固定し、新たなv2真正BLENDに旧コード修正版・監査・GUIボタンを全て同梱する。旧原本は保存・再読込のための入力のみで、一切上書きしない。都市造形・ART画像・世界書込みは行わない。
- [専用native CI #41422123251](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41422123251) は真正Blender v2**生成工程はSUCCESS**、追補確認時は独立再読込と空原本からのレンダ誤実行拒否検査が**IN_PROGRESS**であり、全体成功はまだ未確定。完了が確認できた場合にのみ `artifacts/g4c7-m37p2-standalone-artist-workspace-v2-NOT-ART/` をGitHub原本として扱う。
- 保存コミット `0b92cc487ff35746cadf1398fee69069f33b675b`、`c04878dd4064817afaa126ba4b371ff977833b45`、`f35fa37d77f750a8e0f8064a9170036bc497e08d`、`a7d6f60e0127f9df423a12d18d8845aa09af2140`。

**重要な未達：** このCIは実際の新しい都市形態が存在しないため、GUIの真正3視点ART画像、住居・公共入口・工場の実空間、331/993安全QA、MakeCode費用を評価していない。P2の本当の進展には作者が同一Blender原本上で市街粗3Dと実生活断面を並行して直接編集する必要がある。Workは事前明示承認制。第三のプログラム生成プリミティブ都市は作らない。main変更禁止、PR #53 Draft/未merge、Minecraft施工禁止。
