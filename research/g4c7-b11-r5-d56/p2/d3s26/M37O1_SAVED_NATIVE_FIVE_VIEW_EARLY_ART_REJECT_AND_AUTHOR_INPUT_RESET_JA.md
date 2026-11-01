# G4-C7 M37-O1｜保存真正5視点の絶対美術審査・EARLY ART REJECT・作者入力の再設計

**2026-11-02 JST／固定方針に従いART-FIRSTで早期停止。** M37-Nを救済しない別Blender作者研究M37-O1（A_INHABITED_SHIPYARD_SEAM）を、GitHub保存済み真正5画像と実BLEND監査から独立評価した。

## 0. 真正ソースと判定の分離

- [M37-O1専用Actions #41321512829](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41321512829) は **completed/success**。ただしこれはネイティブ保存・限定METHODのCIでありART審査ではない。
- [真正アーカイブ](../../../../artifacts/g4c7-m37o1-verified-native-activity-author-art-hold/) は実在。BLEND `M37O_A_REAL_ACTIVITY_SILHOUETTE_AUTHOR_ART_HOLD.blend`、1,091,100 bytes、manifest記録SHA256 `7845343514b79067835ddbbd18aabf93439a391f4a2c0983227475b18331b2f1`。**manifest/独立監査の一致であり、本審査でBLENDバイナリを独自ダウンロード・再実行したとは主張しない。**
- 旧M37-NのソースSHA `0817bf8a9681e9380b8167e75ddc236dbcab18920b01298c5e405ed46752bdff` をCIが照合、旧チューブ美術メッシュのインポート0。7用途の実床・屋根と開口、6枚の公共ルート物理板、9保存カメラ、5真正Cycles画像をアーカイブ。3負例（工場隔壁除去、住宅ドア閉塞、公開経路欠落）を独立検査で検出。
- この**技術限定の成立は美術採用・歩行安全・施工可能性と無関係**。現地での実生活/物理エンジニアリングはNOT CERTIFIED。

## 1. 真正5視点・絶対美術判定（ユーザーの正式採用を代行しない）

| 画像（保存同一BLEND） | 実際に見えた問題 | ART判定 |
|---|---|---|
| [M37O_AERIAL.png](../../../../artifacts/g4c7-m37o1-verified-native-activity-author-art-hold/M37O_AERIAL.png) | 低密度の独立した多角形押出し室・似た水平屋根・開放大地。工場に簡素な先細りオブジェクトがあるが、巨大で高密度の未来都市と読めない。M37-I/J、M30、M33のキャンパス失敗と支配原理が同じ。 | **EARLY ART REJECT** |
| [M37O_PUBLIC_EYE.png](../../../../artifacts/g4c7-m37o1-verified-native-activity-author-art-hold/M37O_PUBLIC_EYE.png) | 画像のほぼ全面が暗く、巨大壁・天井で行先、公共活動、都市の奥行を読めない。原因の全量は照明・遮蔽を別測定しない限り区別しない。 | **REJECT** |
| [M37O_MAKER_EYE.png](../../../../artifacts/g4c7-m37o1-verified-native-activity-author-art-hold/M37O_MAKER_EYE.png) | 工場の対象物が単純な縦長多面体として見えるだけで、実製造活動、設備と人のスケール、見学導線が豊かに構成されていない。 | **REJECT** |
| [M37O_HABITAT_EYE.png](../../../../artifacts/g4c7-m37o1-verified-native-activity-author-art-hold/M37O_HABITAT_EYE.png) | 画面がほぼ暗く居住・窓・眺望・公共から私的玄関への関係を読み取れない。 | **REJECT** |
| [M37O_UPPER_EYE.png](../../../../artifacts/g4c7-m37o1-verified-native-activity-author-art-hold/M37O_UPPER_EYE.png) | 暗い単純な室内と四角開口。都市の文化・高所目的地・眺望に説得力がない。 | **REJECT** |

**結論：M37-O1はEARLY ART REJECT。全体ART HOLD維持、正式ART採用0件。** M37-NのART REJECTも取り消さない。美術不採用であり、M37-O1の旧外観へ窓・色・装飾・巨大屋根・階段・橋を追加して救済してはならない。

## 2. 失敗の根本原因

1. **作者入力自体が7個の「独立した平面外形＋z＋h」**で、各外形を同じまま床/屋根に押出し、残りを6接続板で結んでいる。用途ラベルと多角形頂点の違いだけで、巨大都市の造形の決定権は再び最も簡単な幾何へ戻った。
2. 「室と都市外形を同一BLENDで生成した」ことは、**製造・居住・研究の相互要求が外形と実内部を相互変更したことの証拠ではない**。床と屋根の輪郭一致は同時コピーであり双方向の作者判断とは違う。
3. 実入口やルートの存在は公共体験の成立を保証せず、眼高の厳格視点で失敗が見つかる。暗さ・遮蔽・立体移動・頭上/隔壁/プライバシーの未確認を別に扱う。
4. M37-Nの巨大殻の修正から離れた点はMETHOD上の前進。ただし作品の美術としてはM37-Iの**分離施設キャンパス**へ再発したため、高密度都市の候補へ進めない。

## 3. 次に認められる工程（形態生成前の作者入力再設計）

- M37-O1の**巨大化や追加レンダリングをしない**。M37-P0ではまず「市民が何を見てどの順で暮らし、宇宙機の製造とどのような壁/採光/高低差/実支持を共有するか」という同一の**相互作用の断面**から、外観・実床・実境界・実経路へ影響を及ぼす複数用途の**共有作者判断**を明文化する。
- **禁止された入力**：独立7用途の輪郭を各別に押出して後から床板で接続する、既存チューブ/箱/棚/キャンパスを再利用する、単純形状をアート評価の代わりに新規命名する。
- **必要な作者の実判断**：製造機の高さ/搬送の空間が市民見学と研究の断面を変え、研究の視線が外形開口を変え、住宅の私的境界が入口と都市立面を変え、文化/上層の公共接続が全体のボリューム配置を変えること。安全な人間動線や接続は意図データだけでは成立せず、後続の真正3D原本で実証する。
- 次案が真正3D化されても、全景＋人眼＋製造＋住宅＋高所の固定視点のうち一つでも旧失敗の重大な再発があれば大規模化前に止める。質的に異なる方向を最大2つだけ考え、2案不合格なら方法へ戻る。独立QAや施工見積りは美術候補に限り後段で行う。

## 4. 厳格な未実施・禁止契約

- 正規 **331人体／993足元**、人体半幅0.65m、足元高さ+0.15〜+3.25m、従来干渉上限45/331・未支持0/993＝旧契約不変、**現案ではNOT RUN**。
- 正規 **G0/S1/G1/G2/G3**、自由歩行、全身連続掃引、支持/構造/避難、現案のMakeCode Fill/Clone/Place非施工コストも **NOT RUN/NOT CERTIFIED**。研究単位をMinecraft 1m/1blockへ恣意換算しない。
- Minecraft Education施工・旧都市統合**禁止／world writes 0**、main変更禁止、[PR #53](https://github.com/ryomashibaba/makecode-limitlab/pull/53)をDraft/未mergeのまま保持、Workはユーザー事前承認なしには使用しない。

**M37-O1＝限定METHOD TECH PASS、絶対美術EARLY ART REJECT、全体ART HOLD、正式採用0、安全QA NOT RUN。**
