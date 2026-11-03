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


### 節17補足 — native検証のやり直し（正確なCI状態）

最初の専用CI [#41422123251](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41422123251) は、新v2真正BLENDの作成までは成功したが、独立再読込ゲート実行中に診断改訂を行ったため **CANCELLED**。**独立再読込とアーカイブのSUCCESSとは扱わない**。

処理が長引いたため、別プロセス再読込ゲートに150秒の子プロセス実行上限・80秒経過時のfaulthandlerダンプ・段階進捗出力を追加した。ワークフロー更新コミット `46a1d98f4824bc128a732a596f037b4943059f2b`。新版 [#41422705862](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41422705862) は最後の確認で **QUEUED、全体未検証**。新v2 `.blend` のGitHubアーカイブ確定は、CIが実際にファイルをpushし、改めて存在・manifest SHAを確認するまで保留。

本工程は空の編集器の整備であり、ART HOLD/正式採用0、331/993 NOT RUN、Minecraft施工禁止の固定判定は不変。

---

## 18. M37-P2：単一ファイル直接造形・3真正視点レビュー可能な空Blender原本v2の保存確認（2026-11-02 JST）

**専用Actions [#41423413754](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41423413754) はcompleted/SUCCESS**。真正Blender bpy4.5での別保存、新規の独立再読込、埋込3Python原文SHA照合、実メッシュ0・暫定3カメラ、ART/正式採用/安全/施工の不変、GUIアドオンregister/unregister、**空の原本からARTレビューを試みると正しく拒否する負例**が成立。追記GitHub commit `5eefbe16210faee1bbd22516625b6daa8ecdf28d` で真原本一式を保存。

- [真正保存済みの単一BLEND v2](../artifacts/g4c7-m37p2-standalone-artist-workspace-v2-NOT-ART/M37P2_SINGLE_FILE_DIRECT_AUTHOR_AND_REVIEW_NOT_ART.blend)：**526,911 bytes**、SHA256 `a772fc0bc1d1d2b23a33a14154ca5bcd08fcb1ced05ea5c9eb009aa02b19f99e`。
- [manifest](../artifacts/g4c7-m37p2-standalone-artist-workspace-v2-NOT-ART/M37P2_V2_NATIVE_WORKSPACE_MANIFEST.json) と [直接造形／審査の操作説明](../artifacts/g4c7-m37p2-standalone-artist-workspace-v2-NOT-ART/README_JA.md) を同じ保存フォルダに保管。
- 最初の[#41422123251](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41422123251) は新版への入替でCANCELLED。診断付き[#41422705862](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41422705862) は**FAIL**。ログではnativeBLEND再読込と GUI登録自体は成功したが、CI側で登録済みOperatorを `hasattr(bpy.types, ...)` で判定した誤ったassertに失敗したことを確認。更新コミット `264733ea43c8e2acbb07d7409550c8241582f493` でクラス同一性の確認に変更し、[#41423413754](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41423413754) で再読込・実登録／解除・負例／追記保存まで確認。失敗を成果と混同しない。
- 先行v1空原本SHAは `6ca727def08cce9220dbde59f5836248cb5d0def39c7f375c9308af1461ee904` のまま不変。旧M37-L/N/O1/P1不採用BLENDも一切変更していない。
- **絶対的制限：** CIで真正BLENDのテキスト登録・空原本拒否を確認しただけで、実BlenderデスクトップGUI上の二画面操作、制作途中の作者実3D、3枚の実シーンCycles画像・住居/製造断面の美術的価値はNOT TESTED。都市アート自体は**NOT CREATED**。ART HOLD／正式採用0、331/993・G0/S1/G1/G2/G3 NOT RUN、MakeCode費用未評価、Minecraft施工禁止。manifest内の`G0_S1_G2_G3`という項目名にはG1表記漏れがあるが、G1を含む正式審査の実施・合格の意味ではなく、すべてNOT RUN。
- 次工程はこれ以上の空エディタ生成ではない。**新しい作者が同一保存真正BLENDで都市粗3Dと来訪者・工場職員・研究・文化・住宅の生活断面を直接造形し、早期3視点を画像として絶対ART評価**。未許可Workは使わず、旧プリミティブの第三作を禁止。main変更・Draft PR #53状態維持。

---

## 19. M37-P2：実メッシュ正常系3視点・v3修正原本検証（2026-11-02 JST）

**工程判定：研究用技術レビュー経路は前進。ただし「都市美術」はNOT CREATED、ART HOLD、正式採用0件。** v2までのCIでは「空スタジオから誤ART出力できない」という負例は成立していたが、実際に非空の真正BLENDを再読込し、3枚のCycles画像を生成できるという**正常系は未検証**だった。今回の工程で初めて実試験し、2件の実不具合を修正した。

### 実際に検出した不良

1. Blender 4.5 の `bpy_prop_collection.__contains__` はObjectオブジェクトではなく名前文字列を要求するため、元の `ob in coll.all_objects` 判定は、実メッシュを入れたとき `TypeError` を発生させた。実ログは[初回正常系CI #41428130552 FAIL](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41428130552)。[修正ソース](../tools/g4c7_m37p2_author_native_early_review.py)で `ob.name in coll.all_objects` へ修正。
2. Blender wheelのヘッドレス実行では `open_mainfile` 後の `bpy.data.is_dirty` がTrueとなり、直前のファイルが保存・再読込済みでもレビュー入口で誤停止した。[初回正常系CI #41427642212 FAIL](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41427642212)。[GUI入口修正](../tools/g4c7_m37p2_one_file_early_art_review_gui.py)では、**実GUI内の未保存原本は従来どおり拒否**し、CIのヘッドレスでのみこの誤検出を除外する。

### 真正Blenderでの技術正常系PASS

- [CI #41428422529 SUCCESS](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41428422529)：保護済み元v2をハッシュ照合し、**CI専用の一時ディレクトリ内だけに**修正済みPythonを組み込んだBlenderコピーと5つの単純四面体試験メッシュを作成。保存・別プロセス相当の再読込後、GUI入口と同じ`run_review`関数経路から、AERIAL・PUBLIC_EYE・HABITAT_EYEの**3真正Cycles PNG**を生成。PNG署名・画像SHA・保存マスターハッシュ不変、ART HOLD／施工禁止を確認。試験用3D・画像は一時ディレクトリから削除。**これは新しい都市案ではないし、公開・Minecraft施工・正式美術合格を意味しない**。
- 技術テストソース [`g4c7_m37p2_ephemeral_positive_native_review_smoke.py`](../tools/g4c7_m37p2_ephemeral_positive_native_review_smoke.py) はCI環境かつBlenderバックグラウンド時だけ動作し、CITY ARTへ一切昇格しない。
- 従来v2は古い埋込コードを含むため、固定の原本上書き禁止を守って、新しく[真正v3作者スタジオ（修正済み）](../artifacts/g4c7-m37p2-patched-native-author-editor-v3-NOT-ART/M37P2_DIRECT_AUTHOR_NATIVE_EDITOR_FIXED_REVIEW_V3_NOT_ART.blend)を追記保存。**528,408 bytes、SHA256 `536e451c763c4326421b13285abf1056a3a11d755028f8ff20b54b99b08a0249`**。[保存監査manifest](../artifacts/g4c7-m37p2-patched-native-author-editor-v3-NOT-ART/M37P2_V3_PATCH_MANIFEST.json)、[CI #41428982047 SUCCESS](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41428982047) は独立再読込、2埋込スクリプトSHA、空原本の拒否、旧v2 SHA不変、GitHub追記保存まで成立。旧原本v1/v2/O1/P1は未変更。
- 注意：旧v2のアーカイブ作成専用CIはコード改修後の再実行で失敗する場合がある。v2を上書き・再生成して整合を偽装せず、修正済みの**v3を唯一の次回作者編集入口**として指定する。
- CIはBlenderの**デスクトップGUIでの実操作・本当の都市全景と居住/製造/文化/研究断面・人間視点の美術的評価**を行っていない。空v3の実都市メッシュ数0。正式331人体／993足元、G0/S1/G1/G2/G3 NOT RUN、MakeCode実費未測定、Minecraft施工禁止、正式採用0、main変更禁止、Draft PR #53未merge。

**次の制作工程はこれ以上の空エディタ開発ではない。** v3真正BLENDをBlenderで直接編集し、都市全体の異なる密度と、来訪者／製造職員・研究・文化・居住の本当の生活断面を同時に造形すること。それを同じ保存原本で3視点から絶対ART批評する。旧P1の`patch/wall/bridge`を用いた第三の擬似美術は禁止。未承認のWorkは使用しない。

---

## 20. M37-P2：真正BlenderデスクトップGUI二画面編集・実視点切替の初PASS（2026-11-02 JST）

**研究進捗は編集GUIの限定TECH PASSであり、作品制作ARTは未着手。全体ART HOLD／正式採用0件不変。**

- [正式検証レポート](../research/g4c7-b11-r5-d56/p2/d3s26/M37P2_ACTUAL_DISPLAY_GUI_DUAL_AUTHOR_EDITOR_PASS_20261102_JA.md) と [成功した真正GUI Actions #41431524480](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41431524480)。Blender公式GUI実行ファイル4.5.15を上流SHA256で照合し、Xvfb実ディスプレイで`bpy.app.background=False`の**非ヘッドレス**状態を確認。v3真正原本を読み込んでGUIコマンド`g4c7.p2_parallel_split`を発行し、`VIEW_3D`の2編集エリアを実測。公共視点／住宅視点を切替・`g4c7.p2_parallel_refresh`が`FINISHED`。保存元SHA256 `536e451c763c4326421b13285abf1056a3a11d755028f8ff20b54b99b08a0249`は前後不変。新メッシュ0。
- [新GUI実測コード](../tools/g4c7_m37p2_real_gui_dual_editor_smoke.py)／[専用read-onlyワークフロー](../.github/workflows/g4c7-m37p2-actual-display-gui-dual-views.yml) を研究ブランチへ保存。JSON証拠はActions artifact（保持21日）に記録、原本やMinecraftワールドへ書込みなし。
- 初回の [#41431366117 FAIL](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41431366117) はBlender 4.5.15で無効な`--noaudio`オプションが原因。commit `6a634ebc2c02ac7404fb1619d69c3ce7ecac68e5`で削除し、上記成功CIを確認。原因を造形ARTやBlender製品不良と誤分類しない。
- **実都市の3D作者造形や真の居住・製造・研究・文化の生活断面は依然ゼロ、3視点ART画像を作る工程は未実施。** GUIの2編集エリアが正しく動く技術成功を、完成した都市美術や正式採用へ格上げしない。ART HOLD／正式採用0件。331人体・993足元、G0/S1/G1/G2/G3 NOT RUN、MakeCode費用未評価、Minecraft施工禁止、main変更禁止、PR #53 Open/Draft/未merge、Work事前明示承認制。
- **次の工程は実際の新都市作品を、v3原本で人の営みを含めて作者が3D直接造形すること。** 旧P1の自動プリミティブ第三作、空原本追加、未許可Workは避ける。

---

## 21. M37-P2：本当の都市美術へ向けた作者造形の具体的な初回構想（2026-11-02 JST）

**段階：未採用の具体的ART DIRECTIONのみ。新3D原本は未制作、ART HOLD、正式採用0件。**

- 2026-11-02最新の研究HEAD `8631178e7531955c108f7e98716b0b0899e9c539` から引き継ぎ、通常Verify [#41431909686](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41431909686) completed/SUCCESS、PR #53 Open/Draft/unmergedを確認した。
- [新規作者構想「街を織り込む造船都市」](../research/g4c7-b11-r5-d56/p2/d3s26/M37P2_FIRST_DIRECT_AUTHOR_ART_DIRECTION_CITY_AND_LIVED_SECTION_20261102_JA.md) を研究原本へ追加。旧M37-O1/P1の形状／生成器は変更せず、**建物が暮らしと製造に侵食される密な連続街区**を新たな作者主導の対象として明文化。工場実設備／公衆と職員を隔てる奥行ある見学室／研究文化の自然光を入れる共有中庭／私的玄関・深い居室・都市へ向く窓を**同じ本当の3D原本で同時に造形**するという形態上の決定を記述。
- 過去の「検査済み空スタジオ」整備をこれ以上追加するのでなく、次の実行が**どの画面に何を真正3Dで見せなければART REJECTなのか**を全景・公共眼高・住宅眼高の3視点ごとに具体化。箱・板・道路・チューブ・低層パビリオンへの回帰を禁止。これは手順の再列挙ではなく、**表現したい都市の空間的内容の仮説**。
- **厳格に未達を記録：** 現Chat環境には作者用Blender GUIの対話操作がなく、Workは事前明示承認制で未承認。GitHub Actions上のGUI技術試験は済んだが、人間に代わる真正都市の直接編集・保存・3視点美術評価は本工程で実施していない。コード上の第三の`patch/wall/bridge`型プリミティブ都市を生成して完成扱いしない。
- R0〜R5、美術第一・正式採用本人限定、正式331人体／993足元とG0/S1/G1/G2/G3 NOT RUN、MakeCode未測定、Minecraft施工禁止、旧真正原本不変、main未変更、PR #53 Draft、Work事前許可を維持。

**次の実美術制作に必要なもの：** 新しい直接造形の作業権限・アクセスと、その実体としてのBLENDメッシュ＋同一シーンの都市全景/公共眼高/住宅内観。次回「工程番号」だけを進めたり、空の編集用ファイル・QAツールを再生成して実際の美術制作に替えたりしない。

---

## 22. M37-P2：Work無し／ローカルBlenderを直接作者編集するためのWindows起動経路（2026-11-02 JST）

**工程分類：真の作者3Dへのローカル到達経路。作品自体は依然NOT CREATED。ART HOLD、正式採用0を維持。**

ユーザーからWorkの使用量枯渇、できればGPT-6 Lunaまたは6.1 Terraで継続希望があった。現在のChatにはローカルWindowsデスクトップを対話的に操作する権限・接続がなく、モデルの実行選択やTerraへの直接委譲も不可能。**Workは起動せず、Luna/Terraが自動で制作したとは報告しない**。

- [Windows単一PowerShell起動スクリプト](../tools/g4c7_m37p2_launch_local_author.ps1) と [日本語使い方](../tools/G4C7_M37P2_LOCAL_AUTHOR_LAUNCH_README_JA.md) を研究ブランチに実際に保存。GitHub ZIPや過去チャットのZIPは不要。正本v3の固定コミット `3c05ba86814443bb3b6d44718dae50a855fea083` から、元SHA256 `536e451c763c4326421b13285abf1056a3a11d755028f8ff20b54b99b08a0249` を保持する編集用別ファイルをWindowsのユーザー文書セッションフォルダに置く。もとのGitHub保護原本は絶対上書きしない。
- Blenderの既設二画面/直接作者監査/真正3視点レビューをセッション起動時に読み込むGUI初期化スクリプトを生成し、インストール済みBlenderを起動し、作業フォルダをExplorerで開く。**幾何形状の自動生成、元Blenderの保存変更、Minecraft world write、main変更はしない**。これで、本当に作者が立体編集を始める最後のWindowsローカル起動操作が短縮できた。
- [Windows実検証CI #41447267350 SUCCESS](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41447267350) はPowerShellの真正Windows解析、v3 SHA固定原本のローカル複写、フォルダ・manifest・埋込GUIブートストラップPython構文、世界・GitHub原本変更0を検証。テストは`-PrepareOnly`で実行したため、Windowsデスクトップ上のBlender実モデル編集・Windows 5.2 GUI表示は**未検証**。[既存の実GUI CI #41431524480](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41431524480)はLinux Xvfb/Blender 4.5.15による限定的な非ヘッドレスGUI操作の証拠であって、Windows実作者造形の代用にはしない。
- **アート前進の計数を虚偽にしない：** M37-P2都市メッシュ0、実住宅室0、実製造工程0、3真正都市ART画像0、技術GUIの操作だけPASS。旧P1/O1の不採用形状を流用した第三自動プリミティブ案は禁止。新しい空BLENDをGitHubへ作り増したわけではない。
- 固定R0〜R5、正式331人体／993足元＋G0/S1/G1/G2/G3 NOT RUN、MakeCodeコスト未評価、Minecraft施工禁止、PR #53 Open/Draft/未merge、main保護、Work事前明示承認制を再確認した。

**本当の次工程**：ユーザーのローカルBlender、またはデスクトップGUIを本当に操作できるローカル作者エージェントが、既存v3コピーを元に「都市全域粗形状」と「工場・見学・研究・文化・住宅生活断面」を**直接同時造形**して保存する。3保存実視点をART-firstで審査し、低品質ならすぐREJECT。その作者操作が実施されるまではモデル、CI、計画書の完了を作品の完成と表現しない。

---

## 23. M37-P2：Work無しのローカルモデル直接頂点造形（未採用METHOD実験／2026-11-02 JST）

**実験コードをGitHubへ実装。ただし生成された新たな真正都市BLEND／美術3画像の実作者成果はまだゼロ。ART HOLD／正式採用0件。**

- スクリーンショットでBlender **5.2.1 LTSの実起動**、左右2つの編集ViewとP2用5コレクションがユーザーWindows上に実在することを確認。初回Windows起動障害は解消したが、Chatから直接Blender GUIを操作する権限はない。Work使用量枯渇のためWorkは使用しない。モデル切替はユーザー側設定の範囲。
- [詳しい実験の根拠と否認事項](../research/g4c7-b11-r5-d56/p2/d3s26/M37P2_LOCAL_LLM_VERTEX_AUTHOR_BRIDGE_NOT_ART_20261102_JA.md)。新しいPythonはローカルOllama/Qwen等から、実メッシュの**明示的な頂点＋面JSON**を受け取る。モデル生成の任意Pythonコードは実行しない。5用途、非退化面、3軸の空間的厚み、単純8頂点6面キューブの多用を拒否して、危険な旧`patch/wall/bridge`第三自動プリミティブ都市として扱わない。品質保証ではなく、**不適切なAI出力を初期に捨てるための経路**。
- JSONが形式検証を通ったときだけ、**v3不変空原本から分岐した新しい未採用ローカルBLEND**と真正Blender3視点PNGを生成する。元のGUIを編集せず、ローカルAIは人間のGUI作者編集と異なると記録。正式ARTの昇格禁止、偽のカメラ作者承認禁止、原本SHAを必ず再確認。合格が得られない場合は**新都市に正式採用しない**。
- [実装コード](../tools/g4c7_m37p2_local_vertex_author.py)、[Windows省操作PowerShell](../tools/g4c7_m37p2_run_local_ai_vertex_trial.ps1)、[真正Blender非都市一時検証CI](../.github/workflows/g4c7-m37p2-local-llm-explicit-vertex-first-art-tech-smoke.yml)、[Windows準備検証CI](../.github/workflows/g4c7-m37p2-windows-local-vertex-ai-first-art-prepare.yml) を追加。**専用CIが成功するまでは実運用PASSとは呼ばない**。
- 全体のR0〜R5とART-FIRST、美術の最終採否はユーザー本人、331人体・993足元/正式G0/S1/G1/G2/G3 NOT RUN、MakeCode未評価、Minecraft施工禁止、main無変更、PR #53 Open/Draft未merge、Work事前承認制は不変。

**引き継ぎの重要な停止条件**：このLLM JSON試作を第三の箱／板／橋量産都市に変質させない。スクリーンショット実絶対審査で薄壁・黒画面・空白や用途の断絶が見えたらEARLY ART REJECTを維持し、都市全景と本当の製造／研究／住居生活断面を同時制作する直接作者法へ戻す。

---

## 24. M37-P2：Ollama出力検証と3真正ビューの自動レビュー（2026-11-02 JST）

**作業実装済み、専用CI未実行／ART HOLD／正式採用0。新都市の真正3Dはまだ作成・美術審査していない。**

- 現研究HEADは作業中の最新ブランチ参照とPR #53を再確認する。前工程で確認済みの通常Verify `2dee1cc...` はSUCCESS。ただし**現在のローカルLLM用PythonとWindows起動器の専用CIはGitHub APIで長くqueued／pendingとなっており、成功扱い禁止**。後続更新でconcurrencyによって前の同名ジョブがcancelledされたものもある。原因を根拠なくGitHub障害と断定しない（GitHub公開Statusの2026-11-02月間履歴にはこの時点で現行障害の情報が無い）。
- [ローカルLLMの3D明示的頂点検査と真正Blenderレンダ](../tools/g4c7_m37p2_local_vertex_author.py)に、Ollama公式`/api/generate`の`think=false`、応答バイト上限、`done`および`done_reason=length/error`の拒否、モデルJSONが配列など異常でも記録して停止する保護を追加。設計意図の文字数不足も拒否。不採用候補は`.validation.json`と`.REJECTED_NEVER_ART.json`（上限内）の診断用ファイルとして残し、**不適合メッシュをBlenderへ渡さない**。
- 5用途に関する明示的頂点案が形式検査を通り、**実際にBlenderで3枚のPNG生成に成功した場合だけ**、`OPEN_THREE_REAL_BLENDER_VIEWS_ART_HOLD.html`をローカル生成するよう改修。全景、公共・製造、住居の**同じ真正Blender 3Dから撮影した3枚**を並べ、旧不合格の板・壁・空白・黒画像、実製造・境界・採光・住居の不在をART-FIRSTで見て判断できる。HTMLも未審査、採用0、安全未実施を明示。これは画像を人工的に生成・修正する機能でもなく、正式美術認定機能でもない。
- [Windows PowerShellワンコマンド本体](../tools/g4c7_m37p2_run_local_ai_vertex_trial.ps1)は最新固定Python `13193a41b99e59c87a9475024d4340becb74833d` を参照し、成功後は評価HTMLを自動で開く。[WindowsワンクリックCMD](../tools/G4C7_P2_AI_Trial_Start.cmd)は固定PS1 `f7feec03dfb8a2214ea11d4c9c7be8c212878851` を参照。GitHubから**固定の正しい版を実際に取得できることはコネクタの参照照合で確認したが、Windows 5.2.1／Ollama実機での統合成功は未確認**。
- 正規安全331人体・993足元、G0/S1/G1/G2/G3 NOT RUN、MakeCodeコスト未測定、Minecraft施工禁止、main保護、PR #53 Open/Draft/未merge、Work無しの方針は不変。従来O1/P1の大量プリミティブ生成や旧形状流用に戻ることは禁止。

**次の必要な証拠：** 新Python専用CIとWindows専用CIの実行結果をまず確認する。技術経路の検証成功後、ユーザー既存ローカルOllamaで**1つだけ**候補試験を行い、真正3D／3枚の実レンダを早期絶対評価する。複数案を機械的に量産せず、失格なら拒否・診断する。実行していないローカルモデル試験を実行済みとして報告しない。

---

## 25. M37-P2：初回実ローカルQwen頂点試作の厳格ART REJECT（2026-11-02）

ユーザーのWindowsから`qwen3:14b`による**1回の実Ollama試行**が成立し、旧PowerShell起動エラーを越えてJSON出力された。ただし厳格な形式検査で `P2_AUTHOR_ART_FIRST_PLAN_REJECT` / `SAFE_STOP_ART_HOLD`。実3Dモデル／真正3視点画像の制作成功ではない。

[実測のART REJECT証拠](../research/g4c7-b11-r5-d56/p2/d3s26/M37P2_QWEN14B_FIRST_LOCAL_VERTEX_ART_REJECT_20261102_JA.md)：提出11メッシュ、頂点総数297、面配列総数12、**正しい面0/12**（18/25/56頂点の巨大N-gon）、頂点配列が同一の再使用メッシュ5件、10/11メッシュの面数1件、面インデックス範囲外5件。実都市の新しいCycles画像0枚。ログと付属検証レポートでは正式ART HOLD、採用0、Minecraft FORBIDDEN、安全QA NOT RUN。

同じ不正面が繰り返されたのは**一括で全市の明示頂点・面をQwen14Bに要求する方法が本試験では実用に達していない**ことの証拠。全LLM不可とは断定しない。第三の固定プリミティブ自動都市を再作成して置換しない。ユーザーに同じワンクリックファイルの再試行やBlender手作業を強制しない。

検証器`tools/g4c7_m37p2_local_vertex_author.py`は、形状を変更せず、**不正な面数で早期除外されるメッシュにも完全同一の頂点配列がないか調べる**よう修正した。対応する`tests/test_g4c7_m37p2_vertex_first_art_reject.py`を追加。添付された本物の不採用JSONへの再評価は、従来14種類の不採用理由に加えて5件の頂点複製を独立検出した（計19種類のエラー）。正しい構造の非美術QAフィクスチャは引き続き受理。専用CIでの結果は**成功を確認するまでPASSとしない**。

R0〜R5/ART-FIRST絶対評価、公式採用0、正式331人体/993足元、G0/S1/G1/G2/G3 NOT RUN、MakeCode費用未評価、Minecraft施工禁止、main不変更、PR #53 Draft、Work事前明示許可を維持。

---

## 26. M37-P2：一括頂点方式をRETIRED、制限付きBlenderネイティブ編集Operator研究へ

**2026-11-02 JST。** 実験コード追加／正式ART採用0／都市美術未完成／ART HOLD。

- 先のユーザー実機Qwen3:14B全市一括頂点試作は、有効面0/12・同一頂点配列5件の厳格ART REJECT。これをさらにローカル実行させるのはユーザー負担・ART-FIRST両方に反するので、`tools/G4C7_P2_AI_Trial_Start.cmd`と`tools/g4c7_m37p2_run_local_ai_vertex_trial.ps1`を**通常実行の入口として廃止し、安全STOP**する。旧コミットのファイルはGitHub履歴に残るので、ユーザーには旧ダウンロードを再実行させない。
- [M37-P2新研究方式とMCP安全監査](../research/g4c7-b11-r5-d56/p2/d3s26/M37P2_NATIVE_EDITOR_ACTION_BRIDGE_STUDY_20261102_JA.md)を作成。Blender開発元の公式Lab MCP、Blender 5.2サードパーティ型付きMCP、LM Studio MCP、Ollama Qwenツール呼出し機能を現行情報として調べた。**公式Blender Lab MCPでLLM生成コード実行に保護がないという警告を確認したため、ユーザーWindowsに無制限のMCPをインストールしない。** Workも使用しない。
- `tools/g4c7_m37p2_native_operator_author.py`を新規実装。AIの任意コードや全市頂点データを処理せず、小さな2役割（都市マクロ＋住居）の`begin_surface/extrude_face/inset_face/translate_selection`に限定し、実BlenderネイティブEdit Modeオペレータを**元v3とは別の技術研究BLEND**に適用する。コード内で建物配置や完成した都市の姿を固定生成しない。試験の最小面は一回の編集起点に過ぎず、都市美術として認めない。
- `tools/g4c7_m37p2_ollama_paired_native_action_proposal.py`はOllama `/api/chat` tool callingで**短い操作データのみ**1回提案させる。tool呼出し失敗や未承認パラメータ、API応答異常を全て安全HOLD。今回この新方式でのローカル実モデル呼出しは**未実施**。
- `tests/test_g4c7_m37p2_paired_operator_native.py`、`tests/test_g4c7_m37p2_ollama_paired_operator_proposal.py`、`.github/workflows/g4c7-m37p2-paired-operator-native-blender-smoke.yml`で、正規の2役割ネイティブ編集、未許可コード拒否、実Blender別名保存を技術検証する。**当該新HEADのCI結果がcompleted/successと確認されない限り新ルートの技術PASSは未確認。**
- **本質的な制約を残す：** 本研究はGUIを操作して作者が美術の質を作った証明ではない。実都市全景・実工場と見学者の物理隔壁・研究文化・玄関から内室の奥行の5領域・3真正ART画像は未完成。これらがART絶対評価に出るまでは第三自動プリミティブ都市を増産せず、安全QA（331/993・G0/S1/G1/G2/G3）、MakeCode評価、Minecraft施工を行わない。PR #53 Draft、main保護、正式採用0を維持。

**後工程は本物のペア都市・住居造形、実工場／研究文化の実在と、3視点の早期ART判定。** 技術CIや資料作成だけでは完成数を増やさない。

---

## 27. M37-P2：実Blender 3視点技術画像とWindows省操作起動（2026-11-03）

**ネイティブ編集保存・再読込はCI #41467002875 実測SUCCESS。3視点追加CIおよび新Windows統合CIは本追記時点ではqueued、結果が出るまでPASSと称さない。正式都市ARTは未制作、ART HOLD・正式採用0。**

- [新研究正本](../research/g4c7-b11-r5-d56/p2/d3s26/M37P2_NATIVE_PAIRED_THREE_VIEW_LOCAL_ENTRY_20261103_JA.md)
- [真正同一BLENDの3視点Cyclesレンダ＋SHA検証](../tools/g4c7_m37p2_paired_operator_three_view_evidence.py)を実装。2役割の実際の編集済みメッシュのみを読み込み、別のメモリ上のカメラ仮配置で撮影。保存済み原本を書き換えず、PNG 3枚とレポート、オフライン閲覧HTMLを生成。公式作者カメラ審査・都市美術とは完全に区別。
- [真正Blender CI #41471988900](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41471988900)：実画像・同一BLEND SHA・3 PNG・ART HOLD・原本不変を確認し、撮影成果物をGitHub Actionsにアップロードする新工程を追加。**この新CIの結果は確認待ち**。
- [Windows向け統合PowerShell](../tools/g4c7_m37p2_run_native_operator_first_pair.ps1)は固定コミットから3つのPythonのみ取得し、ユーザーが既に持つSHA固定v3コピーと既存Ollamaモデル・Blender5.2を利用する。1回の型付きOllama Tool Callで小さい2領域の編集命令を取り、別名Blender試作`.blend`と3真正画像を作り、HTMLと保存フォルダを開く。元のBlender GUIを直接操作せず、main／Minecraftは不変更。失敗したらHOLD。
- [1ダブルクリックCMD](../tools/G4C7_P2_Native_Operator_Trial_Start.cmd)を追加。ZIP不要、通常利用者はコード編集・PowerShell入力不要。ただし**実ローカルOllama＋Blender統合テストは未実施**。[新Windows検証CI #41472380173](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41472380173)でWindows PowerShell構文、固定PS1と3Pythonの取得、SHA、PrepareOnly安全停止、元のBLEND不変を確認するまでユーザーに実行させない。
- **実作品の認定ではない**：二つの仮Edit Mode形状は学習用フィクスチャ。都市全体の密度、工場・見学区切り、研究文化、室内住居の実物、本当の3視点ART提出は未完成。旧Qwen一括JSON・固定巨大板、Box群ジェネレータへ戻らない。旧ランチャーはRETIREDを維持。
- 固定規約：main変更禁止、Draft PR #53未merge、Work不使用・事前許可、正式331人体/993足元＆G0/S1/G1/G2/G3未実施、MakeCode未測定、Minecraft施工禁止、正式採用0。

---

## 28. M37-P2：3真正Cyclesの実画像評価で技術PASS・ART REJECT（2026-11-03）

[実画像による独立ART REJECT正本](../research/g4c7-b11-r5-d56/p2/d3s26/M37P2_NATIVE_OPERATOR_3REAL_CYCLES_VISUAL_ART_REJECT_20261103_JA.md)。

[本物のBlender3視点撮影CI #41471988900](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41471988900)で`SUCCESS`。実artifact `g4c7-p2-paired-native-true-three-views-tech-only-not-art`に保存済みのCycles3 PNG／JSON／HTMLをこのチャットで取得・**3枚すべて直接目視**。同じ保存済みBlenderのSHA256 `2ee1f2592084e75b041c8e1bc36fb9fd5e73581b1959caf42f8658d759f8a456`、`city_macro`と`habitat`の実メッシュはそれぞれ**8頂点6面**。画面は互いに離れた無装飾の灰色直方体2つのみ。

**ART REJECT**：街並み・造船設備・研究文化・住居の実在が確認できず、全景／人間目線すべてで美術の絶対基準未達。これはアートを作ったという報告ではない。前回Qwen3:14b一括頂点失敗とは別に、単純なネイティブ編集操作の技術経路の限界が視覚的に判明。旧P1/O1と同じ仮都市を無限に増産しない。

- [新Windows PowerShell](../tools/g4c7_m37p2_run_native_operator_first_pair.ps1)は通常起動時の新たな`VISUAL_ART_REJECT`停止ガードを持つ。`-PrepareOnly`でのチェックだけ可能であり、本体のAIモデル呼出しを行いたい研究者のみ別途明示的`-ExplicitTechOnly`が必要。初心者用CMDも停止版の固定コミットを参照し、**ユーザーへ無駄なモデル再実行を指示しない**。
- **新ガードのWindows CI #41473665867は実行結果確認まで未検証**。先行ガードなしWindows準備CI #41472380173はSUCCESSだが、安全停止の最新版の成功と混同しない。
- 本物の次の制作要件は「同一Blender原本を実画面で見ながら作者が直接造形・修正する閉ループ」。技術フィクスチャや少数オペレータの追加ではART PASSにできない。公式ART採用0、ART HOLD、正式331人体993足元/G0/S1/G1/G2/G3 NOT RUN、MakeCode未評価、Minecraft施工禁止、main保護、PR #53 Draft未merge、Work不使用を継承。

---

## 29. M37-P2：実Cycles 3視点のART-FIRSTフィードバックゲート成立（2026-11-03）

- [新しい実画像フィードバック報告](../research/g4c7-b11-r5-d56/p2/d3s26/M37P2_VISUAL_FEEDBACK_GATE_20261103_JA.md)を保存。
- [CI #41552562056 SUCCESS](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41552562056)：実際に保存した同じネイティブBlenderから3枚の真正Cycles PNGを撮影し、PNGのSHA256／原本メタデータから**EARLY_ART_REJECT**と明示的に判定した。都市・工場・研究文化・住居内観が未実体、2メッシュは各8頂点6面であるため。**技術CI成功と美術REJECTは同時成立**。新ゲート回帰テスト5件成功。
- [実装](../tools/g4c7_m37p2_visual_feedback_gate.py)は検証済み3枚と参照JSONを読み取るだけでBlender原本・Minecraft・GitHub mainに書き込まない。フィードバックJSON、携帯可能な同一3画像HTMLを出力。[同一CI](../.github/workflows/g4c7-m37p2-paired-operator-native-blender-smoke.yml)のartifactに含めて保存。**ART PASSを自動発行するコードは存在しない**。構造上明らかに不足ならEARLY_ART_REJECT、それ以外はART HOLD（作者・ユーザーの実画面審査必須）。
- 追加の`--vision-model gemma4:26b`は**ユーザーが明示的に選んだ場合だけ**ローカルOllamaの画像入力へ3枚を送る。モデルはインストールしない／画像解析は推奨コメントに限定／任意Pythonコードや形状を生成・実行しない。ユーザー実機でのGemma画像評価は**未実施**。ビジュアルAIが不足を見逃しても正式美術を承認できない。
- **本質的なARTの未解決点**：作者が実Blender画面を見て3D形状を継続修正する閉ループはまだ未成立。直方体2つの再実行・無制限プリミティブ生成・旧Qwen全市一括頂点の再試行は禁止。現状の技術PASSは作品採用とは無関係。
- 固定：全体ART HOLD、正式採用0、正式331人体・993足元／G0/S1/G1/G2/G3 NOT RUN、MakeCode費用未評価、Minecraft施工禁止、main保護、Draft PR #53未merge、Work不使用と事前承認制維持。

---

## 30. M37-P2：実Cycles不採用フィードバックから同一Blenderメッシュの修正→再撮影まで1往復の技術検証（2026-11-03）

[実証と厳密な美術REJECTの研究正本](../research/g4c7-b11-r5-d56/p2/d3s26/M37P2_TRUE_FEEDBACK_NATIVE_REVISION01_20261103_JA.md)へ記録。

- [Blender実CI #41554510076 SUCCESS](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41554510076)で、実Cycles3視点→EARLY_ART_REJECT→そのレポートと保存済みBLEND両方のSHA256に結びつく**1回の安全な修正アクション**→本物のbmesh選択面編集→別名`.blend`→実Cycles3視点を再撮影→EARLY_ART_REJECT、という技術ループ全体を証明した。**ローカルOllama/Gemma/Qwenが実画像から自分で修正案を生成したわけではない**（CI上は明示的な2操作の技術フィクスチャ）。
- 元実測：`city_macro` 8頂点6面→12頂点10面、`habitat` 8頂点6面→12頂点11面。元の保存済みBLEND SHA `5f9e9b82eb952cdb4b32bab03e59dbe973c90ab80e5c9598750ea134a9d396ab`、修正後別名BLEND SHA `6edc310147b35e2acaac4f5b7928eda577f1d50053a532dfe3c7f9694994cd78`、実画像のフィードバックSHA `0471ac6632485cdcc1fa7299d191f358489d0903f645ea01158bc093de84a2af`。原本上書き0・新オブジェクト0・正式作品採用0。
- 修正後の3 PNGも**実際に画面確認済み**。依然として離れた箱状2形状で、街並み・造船設備・研究文化・住居内部が存在しない。黒い面が見えるが、その技術原因は未調査なので憶測で断定しない。**芸術的改善なし／EARLY ART REJECT維持**。面数の増加を美術の採用に使わない。
- [実装](../tools/g4c7_m37p2_feedback_to_native_revision.py)は既存の2つのメッシュの正しい向きの1面を選択し、boundedな`bmesh.ops.inset_region` / `bmesh.ops.extrude_face_region` / `bmesh.ops.translate`のみ許可。モデル生成コードや新規箱の作成・Minecraftの書き込み禁止。元`.blend`と実際の3PNG・JSONのSHAを変更直前に再照合し、**1回の研究修正だけ**許可し、`ART HOLD`のまま別名保存。[回帰テスト](../tests/test_g4c7_m37p2_feedback_to_native_revision.py)にはSHA改変・画像改変・無許可Python・world write・二役割欠落等の拒否を含む。
- [CI保存物](../.github/workflows/g4c7-m37p2-paired-operator-native-blender-smoke.yml)に、本物の修正済み別名`.blend`もartifactへ含める変更を実施。[追加ガードの最終CI #41555143899 SUCCESS](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41555143899) は3枚のPNGバイト列SHA改変拒否と修正後BLENDのartifact保存まで実証と明示。前回の全ループCI成功とは区別。
- **本来のアート制作の欠落は解消していない**。モデルが見栄えを自ら判断して形を作り込む能力・実Blender GUIを見て作者操作する経路・5用途を伴う巨大街並みの独創的造形は未成立。第三の単純箱都市を反復しない。Work使用量枯渇・事前許可制を守り、ユーザーに新たなローカル試行を求めない。
- 固定：全体ART HOLD、正式採用0、331人体/993足元・正式G0/S1/G1/G2/G3 NOT RUN、MakeCode費用未評価、Minecraft施工禁止、main保護、PR #53 Draft未merge。

---

## 31. M37-P2：実Cycles前後比較で自動箱編集を停止し、直接作者造形へ戻す品質ゲート（2026-11-03）

[実施した根拠と固定判断](../research/g4c7-b11-r5-d56/p2/d3s26/M37P2_ART_GAP_AUTHOR_CAPABILITY_GATE_20261103_JA.md)。

- [技術CI #41556855447 completed/SUCCESS](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41556855447)：**本物の保存Blender→真正Cycles3画像→EARLY ART REJECT**の元・1回修正後それぞれに新ゲートを実行し、両方`REQUIRE_NEW_DIRECT_AUTHOR_3D_CONTENT`、モデル追加実行0を確認。修正前にあった2直方体8頂点6面という失格要素は、面を増やしても本当の都市全景・工場・住居内部等の欠落を解消しない。新ゲート回帰7件PASS。
- [実装](../tools/g4c7_m37p2_art_gap_authoring_gate.py)と[検査7件](../tests/test_g4c7_m37p2_art_gap_authoring_gate.py)。実BLEND SHA・3 PNG SHA・不採用フィードバックの一致確認、`true_city=false`・工場見学隔壁／研究文化／住居の`NOT_AUTHORED`など根本的な不足を確認した時点で`REQUIRE_NEW_DIRECT_AUTHOR_3D_CONTENT`を出し、旧2箱の自動補修とモデル呼出しを許可しない。正式美術を自動PASSする分岐は存在しない。
- CI artifact `g4c7-p2-one-true-feedback-native-revision-before-after-not-art` ID `13195277229`に旧2箱BLEND、前後のPNG、編集結果、前後の停止判断JSONを保存した。**技術PASSは美術作成成功ではない。**
- **次工程は既存の「街を織り込む造船都市」美術方針どおり作者が同一Blender原本へ都市マクロ＋工場／厚い見学隔壁＋研究文化＋玄関・前室・居間・窓の実居住断面を直接造形することのみ**。現ChatはWindows Blender GUIにアクセスできずWork不使用のため、今時点でその制作自体を実行したとは報告できない。コード生成の第三箱都市／同じ薄い板やブロックの自動形状増殖へ戻らない。
- R0〜R5、ART HOLD・正式採用0、331人体／993足元とG0/S1/G1/G2/G3 NOT RUN、MakeCode未測定、Minecraft施工禁止、main保護、PR #53 Draft・未merge、Work事前承認制の方針は維持。
