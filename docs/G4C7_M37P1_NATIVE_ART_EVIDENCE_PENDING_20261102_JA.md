# G4-C7 M37-P1 — 共有作者断面のネイティブ制作・現物審査待ち

**2026-11-02 JST。段階判定：SOURCE COMMITTED／ART UNREVIEWED／全体ART HOLD。**

## 目的と着手した実物

M37-O1は真正5画像の審査でEARLY ART REJECT。再発した「用途別に独立多角形建物を作りあとから道路板で繋ぐ」方式を使用しない。M37-P0の確定した4つの作者判断（製造クリアランス、研究採光、住居プライバシー、文化高所接続）を入力に、新しい一体Blender作者シーンを試作する。

研究ブランチへ実コードをコミットした：
- [M37-P1新規本物のBlender作者プログラム](../tools/g4c7_m37p1_coupled_civic_shipyard_native.py)：工場を開放し、周辺の公共見学、研究、居住、文化、高所の実床・ガード形状・壁・非一様公共路面を同じ原本として作る。旧M37-O1の7施設・M37-L/Nチューブ美術はインポートしない。
- [M37-P1独立ネイティブ再読込・実頂点依存・6負例監査](../tools/g4c7_m37p1_independent_native_section_audit.py)：実BLENDを別Blenderプロセスで再読込し、4作者判断が複数のメッシュ頂点に対応するか確認する。本人の美術合格・331/993・実歩行の認定とは全く別。
- [M37-P1専用GitHub Actions](../.github/workflows/g4c7-m37p1-shared-section-native-art-gate.yml)：真Blender 4.5、真正7視点、再読込監査、SHA一致、6負例、採用0と禁止条件を通った場合のみ研究ブランチにBLEND/PNG/manifest/監査をappend-only保存する。

## CIは未完了なら成功を名乗らない

初回専用 [#41351611157](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41351611157) は、Blenderの導入と原本照合は成功したが、実モデル生成の冒頭に `ModuleNotFoundError: No module named 'mathutils'`。Blenderの`bpy`初期化前のimport順が原因で**FAIL**。修正コミット `860f0337930113f5853af50303a65b9dc7beb58f` により `bpy`を先にインポートするよう修正。

再実行専用 [#41351764632](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41351764632) の結果、次のアーカイブ原本の実在およびSHA・真正7視点は**再開時点で改めて確認する**。この文書作成時には最新結果を未確定とする。専用CI SUCCESS後も**ART PASSではない**。

## 視点審査で不採用にする条件

- 全域：再び浮いた床板・帯・一枚板や巨大空洞、巨大抽象彫刻が主役で、人間の生活する高密度都市が読めない。
- 公共眼高：街路・室内・研究の行先より暗い壁・天井・行き止まりが主役。
- 工場：単なる棒状宇宙機とガントリー模型が主役で、製造・運搬・見学の人間スケールが読めない。
- 研究／住居／文化／高所：本当の採光、用途と私的・公的境界、共有空間、高所の眺望が同じ3Dで成立していない。
- 実床・公開路面が作られていても傾斜・支持・人体連続掃引・工場の立入防護は未認証。幾何の因果性テストやCIは美術の主観絶対評価を置換しない。

旧M37-O1を復活・延命しない。新M37-P1が失格なら、**同じ生成規則で床やリブを増やさずEARLY ART REJECTし、制作の作者性に戻る**。

## 不変契約

全体ART HOLD／正式ART採用0。331人体・993足元、人体半幅0.65m、足元相対+0.15〜+3.25m、旧干渉許容45/331、未支持0/993の条件不変。正式G0/S1/G1/G2/G3はNOT RUN。Minecraft Education新都市施工と都市統合、world writes禁止。MakeCodeは後段の唯一の最終施工経路で現案は未換算・未試験。main不変更、PR #53 Open/Draft/未merge、Work事前承認制。旧モデル原本・既存ZIP・CSV・USED一回ラッチ保護。

この文書はソース・失敗の記録であり、美しい3D都市を完成させたという報告ではない。
