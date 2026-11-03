# G4-C7 M37-P2：真正Blender/Cycles4視点・最終早期美術審査（2026-11-03）

**判定：クラウドbpy研究案を EARLY ART REJECT（真正Cyclesによる実画面評価）。全体ART HOLD、正式採用0件。R0–R5の基本方針を変更しない。**

## 検証の由来
- GitHub Actions [成功run #41577471323](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41577471323) ：Blender 4.5.15 LTSによる保護v3のコピーを実際にbpy編集・保存。新保存BLENDを別Blenderプロセスで再読込、**真正Cycles 16 samplesで4視点各960×600 PNG**を出力。
- 新BLEND SHA256：`7b4fb821e75946ad763692d3887fb9f8e5d63dda61221c18c2def160f1e3bc71`。保護v3 SHA256：`536e451c763c4326421b13285abf1056a3a11d755028f8ff20b54b99b08a0249`。
- GitHub Actions Artifact ID `13210103003`、7ファイル約2.88MB。成功runが研究ブランチHEAD `238ff83cf5917d025ac030422d9a726a0fec56ab`へappend-onlyでBLEND・4PNG・manifest・READMEをアーカイブ保存。
- アーカイブ [JSON検証manifest](artifacts/g4c7-m37p2-cloud-native-integrated-art-hold/6077fc44b78a7cacc94c68a67a7ebe2d3baebcb0/M37P2_CLOUD_AUTHOR_EVIDENCE_ART_HOLD.json) の4つのPNG SHA-256と、**ZIPから独立ダウンロードした実PNG4枚の計算ハッシュ・ピクセル寸法が全件一致**。技術的な保存・レンダリング成立は限定TECHとして確定。ただしGUIマウス直接編集実績ではない。

## 真正Cycles4枚と絶対美術評価
### AERIAL
![AERIAL TRUE CYCLES ART HOLD](../../../artifacts/g4c7-m37p2-cloud-native-integrated-art-hold/6077fc44b78a7cacc94c68a67a7ebe2d3baebcb0/M37P2_AERIAL.png)
- [GitHubの本物のPNGを見る](https://github.com/ryomashibaba/makecode-limitlab/blob/dev/g4c7-a17-monolithic-rift-fold-art-study/artifacts/g4c7-m37p2-cloud-native-integrated-art-hold/6077fc44b78a7cacc94c68a67a7ebe2d3baebcb0/M37P2_AERIAL.png)
- 960×600、711751 bytes、SHA256 `a5888a85217ea512738085467603a78bb453a358013a36d80b3a271fa9cbc08b`。
- **目視評価：** 真の街区・異なる建築構成・公共街路の細部が見えない。ほぼ同一の低分割灰白色塔、2枚の平板状の土地と細長い水路が大部分を占める。

### PUBLIC_EYE
![PUBLIC_EYE TRUE CYCLES ART HOLD](../../../artifacts/g4c7-m37p2-cloud-native-integrated-art-hold/6077fc44b78a7cacc94c68a67a7ebe2d3baebcb0/M37P2_PUBLIC_EYE.png)
- [GitHubの本物のPNGを見る](https://github.com/ryomashibaba/makecode-limitlab/blob/dev/g4c7-a17-monolithic-rift-fold-art-study/artifacts/g4c7-m37p2-cloud-native-integrated-art-hold/6077fc44b78a7cacc94c68a67a7ebe2d3baebcb0/M37P2_PUBLIC_EYE.png)
- 960×600、695825 bytes、SHA256 `fd1df875e40a0bb522a252032adc1352477d8c12163b2522fb364229da10d9d6`。
- **目視評価：** 隔壁・ガントリー・筒状船体は見えるが、来訪者の滞留・都市の公共顔・実製造設備の細部が不足。

### HABITAT_EYE
![HABITAT_EYE TRUE CYCLES ART HOLD](../../../artifacts/g4c7-m37p2-cloud-native-integrated-art-hold/6077fc44b78a7cacc94c68a67a7ebe2d3baebcb0/M37P2_HABITAT_EYE.png)
- [GitHubの本物のPNGを見る](https://github.com/ryomashibaba/makecode-limitlab/blob/dev/g4c7-a17-monolithic-rift-fold-art-study/artifacts/g4c7-m37p2-cloud-native-integrated-art-hold/6077fc44b78a7cacc94c68a67a7ebe2d3baebcb0/M37P2_HABITAT_EYE.png)
- 960×600、608965 bytes、SHA256 `706edbc85226050896887bfa11da0e6dd65a1e9cdc1df69db221d10dc3033dac`。
- **目視評価：** 直方体家具、大板天井、窓パネルのみが支配的で、住戸の開口・外壁・通行・居住の建築統合が成立していない。

### CULTURE_EYE
![CULTURE_EYE TRUE CYCLES ART HOLD](../../../artifacts/g4c7-m37p2-cloud-native-integrated-art-hold/6077fc44b78a7cacc94c68a67a7ebe2d3baebcb0/M37P2_CULTURE_EYE.png)
- [GitHubの本物のPNGを見る](https://github.com/ryomashibaba/makecode-limitlab/blob/dev/g4c7-a17-monolithic-rift-fold-art-study/artifacts/g4c7-m37p2-cloud-native-integrated-art-hold/6077fc44b78a7cacc94c68a67a7ebe2d3baebcb0/M37P2_CULTURE_EYE.png)
- 960×600、659487 bytes、SHA256 `1a97b1b841d4214db13e6ba8b51ae6fc75cb68d0d50ebc6516d5d470899a456c`。
- **目視評価：** 裸の平台・机・パネル・棚が中心で、文化/研究施設ならではの屋内空間、立体的活動、採光の構成が欠ける。

## 判断と次の制作への拘束
- これは前回のVTK代理幾何画像と異なり、**Blender原本の元マテリアル・実照明を含んだ真正Cycles**を直接確認した判定。形態・都市密度・公共生活・居住・製造・研究文化の全方面で要求を満たさない。現段階の色調も一様な灰白・青銅系の単純面が目立つが、配色だけの改修では根本問題は解消しない。
- 既往の真正BLEND実データ227メッシュ／2,576頂点／204個が8頂点／12塔が同じ45頂点という警告は、真正Cycles画像の実情と整合する。**この案のソースと形状はR1本命候補として打ち切り**、同型塔のパラメータ変更・板・箱の増殖・AI用ラベル追加で再試行しない。
- **本プロジェクトのR1作者制作は依然未達**。次は実際の制作者が同じ3D保存原本を見て編集と批評を繰り返せる経路で、都市全域と住戸・工場・文化施設を同時に設計する。今回のBlender bpy + GitHub Actions + TRUE Cycles + Chatによる画像批評という**非GUIの非同期1ループは実証済み**だが、GUI直接操作するクラウドAI経路は未証明であり、当該低品質作品の「手直し」は進めない。
- R1の2つの作者候補は**都市体験・都市構造・社会活動の構成原理が実質的に異なる**必要があり、同じジェネレーターの種や係数違いは不可。2案とも不合格の場合は設計ブリーフに戻る（第三の同型プリミティブ禁止）。2Dイメージだけを真正3Dの証明と扱わない。
- **安全性：331人体／993足元、G0/S1/G1/G2/G3 NOT RUN**。MakeCode実装・コスト NOT EVALUATED。Minecraft Education施工0／禁止、正式ART採用0／ART HOLD、main保護・v3上書き禁止、PR #53 Draft未merge、Workは事前承認制・Solは事前許可制・ローカルLLMにクラウド美術を置換しない。
