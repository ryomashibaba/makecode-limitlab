# G4-C7 M37-P1：真正7視点絶対審査／EARLY ART REJECT／制作方法の再切替

**2026-11-02 JST。限定METHOD TECH PASS／都市美術EARLY ART REJECT／全体ART HOLD／正式採用0／Minecraft施工禁止。**

## A. 実物GitHub正本とCI結果

- M37-P1は新規Pythonで一体の工場・公共・研究・住宅・文化・高所を作家決定の4変数で編集する真正Blender作者研究。**M37-O1の低層独立パビリオン・M37-L/Nのチューブ外殻をコピーしていない**。
- 初回 [M37-P1 CI #41351611157](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41351611157) は `bpy`前に`mathutils`をimportしたため初期化で停止（FAIL）。輸入順を修正した [#41351764632](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41351764632) は **completed/success**（モデル生成・本物の7Cycles画像・独立Blender再読込/負例・GitHubアーカイブまで全ステップ成功）。
- 真正[アーカイブ](../../../../artifacts/g4c7-m37p1-verified-native-interlocked-urban-author-art-hold/)にBLEND・7PNG・manifest・独立監査JSON・ソース2本・READMEが実在。
- 真正 `M37P1_ONE_COUPLED_NATIVE_CITY_ART_HOLD.blend` **1,005,323 bytes**、manifest記録SHA256 **`ca402f8e58269535bd6838cc8e5201000e9bc137dc578f0751f76bcb0d3b262d`**。同値が独立再読込監査にも記録。保存GitHubのBLENDバイナリの現物と検査結果を示すが、Chat側でBlender GUIの手作業をしたとは主張しない。
- 4つの作者判断（宇宙機搬送/見学に係るクリアランス、研究の採光、住居の段階的私的境界、文化/高所接続）が、複数の実Blenderメッシュへ伝播し、9つの実頂点整合式を独立再検証した。**6負例**（製造側の幾何関係解除、研究採光の幾何関係解除、住居境界の幾何関係解除、文化高所接続解除、工場/公衆の隔壁属性消去、住宅境界属性消去）検出。
- これは **LIMITED_M37P1_NATIVE_SHARED_AUTHOR_METHOD_REOPEN_PASS** に限る。ソースからの形状連動が存在しても、視覚美術・実安全・通行・建築の支持・施工可能性を認定しない。

## B. GitHub実画像7枚に対する絶対美術審査

| 同一保存BLENDの真正Cycles画像 | 実際に見えたこと | 判定 |
|---|---|---|
| [AERIAL](../../../../artifacts/g4c7-m37p1-verified-native-interlocked-urban-author-art-hold/M37P1_AERIAL.png) | 人工的な巨大平面壁・床板と細い帯状橋が主体。真ん中の宇宙機形状も都市生活を説明しない。低密度、空白背景、持続する都市のスケール/地区密度が読めない。M37-D/F/GやP1以前の板/壁優位の根本再発。 | **EARLY ART REJECT** |
| [PUBLIC_EYE](../../../../artifacts/g4c7-m37p1-verified-native-interlocked-urban-author-art-hold/M37P1_PUBLIC_EYE.png) | 巨大な未分割の青灰壁と不自然な床/橋が大きな視野を占め、人間が実際に暮らす街路の入口・活動・連続する賑わいがない。 | **REJECT** |
| [MAKER_EYE](../../../../artifacts/g4c7-m37p1-verified-native-interlocked-urban-author-art-hold/M37P1_MAKER_EYE.png) | 大きな単純なロケット状輪郭・青い三角形面・一枚の帯が主役。製造工程・宇宙機の台座・運搬・整備設備・人と研究をつなぐ実活動の密度がなく、工場らしさが不足。 | **REJECT** |
| [RESEARCH_EYE](../../../../artifacts/g4c7-m37p1-verified-native-interlocked-urban-author-art-hold/M37P1_RESEARCH_EYE.png) | ほぼ全面黒。カメラ遮蔽・照明・配置のどれが支配的かは追加の幾何学的独立検査なしには断定しない。保存固定視点で研究空間の実在を見せられないことが重大問題。 | **REJECT** |
| [HABITAT_EYE](../../../../artifacts/g4c7-m37p1-verified-native-interlocked-urban-author-art-hold/M37P1_HABITAT_EYE.png) | 壁の薄い断片と開放された床の先に空白が広がり、居住できる深い室・実玄関・プライバシー/採光や繋がる街並みを視覚的に示していない。 | **REJECT** |
| [CULTURE_EYE](../../../../artifacts/g4c7-m37p1-verified-native-interlocked-urban-author-art-hold/M37P1_CULTURE_EYE.png) | 巨大な床面と不自然に独立した板/梁で覆われており、文化施設の活動・入口・都市との連続空間が読めない。 | **REJECT** |
| [UPPER_EYE](../../../../artifacts/g4c7-m37p1-verified-native-interlocked-urban-author-art-hold/M37P1_UPPER_EYE.png) | 広い空白デッキと巨大板・帯を眺めるのみ。未来都市の地区密度と生活の高所からの眺望が不成立。 | **REJECT** |

**7視点総合絶対判定：M37-P1 EARLY ART REJECT（アシスタント審査）。正式ユーザーART採用0、全体ART HOLD継続。**

旧M37-O1の不採用も変更しない。「両案とも実3Dで成立する」わけではない。M37-P0の構造的な入力契約では、単純な幾何生成を禁止しても実際の作者コードが`patch`・`wall`・`bridge`を反復し、**外観の決定権は巨大な壁/板/帯へ戻った**。幾何の連動数やCI成功は美術の前進ではない。

## C. 「同方式で第三案」停止とP2への作者方法切替

これまでのM37-O1（独立多角形施設）とM37-P1（部位が連動しても巨大板・壁が残る）は**方向を変えた2つの真正3D不合格例**。2026-10-28固定R0〜R5戦略の「2案失敗で方法を変える」を適用する。

**M37-P1の壁を削る／橋を増やす／色を変更する／居室を大量コピーする追試禁止。第三の`patch/wall/bridge`プリミティブ組み合わせ生成は禁止。**

次段階P2では、実都市形態の一次ソースを**便利なコード生成プリミティブから作者が編集する3D造形判断と使用体験**へ戻す。最初に必要な真正作家入力は、次の各条件を一体の都市造形で満たすこと：

1. 空港/造船所で訪問者が実作業の大きさを見て、工場職員専用動線とは隔壁で分離される実体のある見学断面（巨大な空白工場や単純なロケット模型を主役にしない）。
2. 研究と文化の公共空間が、造船の視線・採光・実縦移動と共有壁/共用床によって相互に**都市外形を変更**する。単なる別の平板渡り廊下では不可。
3. 住宅は独立した小箱でも薄い仕切りだけでもなく、奥行・私的入口・窓・上階生活・街並みを一体で備える。高所から本当に住民の生活する多層都市が見える。
4. **都市全体の粗い外観と代表生活断面を同時**に編集する。遠景を完成してから部屋を詰め込む/一室を完成してから施設をつなぐ、両方禁止。
5. 固定9視点を保持しつつ、本物のBLENDを保存して読戻す。**大規模レンダリング前に**少数の同一3Dで全景・公共眼高・代表居住内観の早期資格を確認し、箱/壁/棚/帯がまた支配するなら停止。

P2では新しい研究案を生成する前に、現在の形状生成コードがなぜこのような壁・帯・空白へ戻ったか、作者の手編集原本が最低何を物理的に含むべきかを確定する。**チャットでGUI編集を実施したと偽らず、WorkでのBlender GUI制作を行う場合もユーザー事前明示承認が必須**。抽象画像や2Dコンセプトを真正3Dと呼ばない。

## D. 生活・安全・MakeCodeと絶対停止条件

- P1の実路面とバリアが存在することは、**自由連続歩行・支持/避難・設備運用・工場公開/職員分離・住宅プライバシー**の認証でない。路面の連続幅・高さ差・踏面/頭上・人体掃引は未試験。
- 正式 **331人体/993足元、人体半幅0.65m・足元相対+0.15〜+3.25m、旧干渉上限45/331・足元未支持0/993** の条件不変、正規331/993は**NOT RUN**。正規G0/S1/G1/G2/G3も**NOT RUN**。
- 新都市のMinecraft Education施工・旧都市統合は**禁止**、ワールド書込み0。Blender原本は研究資料であり、最終施工手段はMakeCodeのみ。現案のFill/Clone/Place・階段換算/処理量は**NOT EVALUATED**。
- main変更禁止、Draft PR #53のReady/merge禁止、旧原本上書き禁止、Work事前承認制・Chat中心を維持。

**結論：M37-P1限定METHOD TECH PASS／EARLY ART REJECT。次は新しい同型モデルの作り増しではなく、作者造形入力の根本再設計。**
