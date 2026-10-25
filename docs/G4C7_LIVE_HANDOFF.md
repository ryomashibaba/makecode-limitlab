# MakeCode LimitLab — G4-C7 継続開発・LIVE HANDOFF

最終確認：2026-10-25 JST。これは新規開発ではない。**常にGitHubの現在のHEAD/QA/CIを実際に再確認**してから次に進む。下のSHAは文書作成時点の確定成果であり、この文書自体の後続コミットによってブランチHEADは進む。

## 最上位原則

- Repository: https://github.com/ryomashibaba/makecode-limitlab
- G4-C7は既存MakeCode LimitLab内の**B文化地区「Orbital Commons」の独立したART-FIRST建築研究**。A/C/D/全都市への統合をまだ許可しない。
- 現時点の判定：**ART HOLD / NO MINECRAFT CONSTRUCTION / NO CITY INTEGRATION**。教育版実機に制作・Fill・Clone・ワールド更新をしていない。過去のG4-C6実機成果やワールド、USEDラッチ、CSV/ZIPは保存し、上書き・再実行をしない。
- 対象寸法の旧歴史基準は188×178/高さ-4～66概念単位。G4-C7のART-FIRST美術研究はこれを超え、A11/A12実験の最高Y約94、A13-A/B約106へ拡大した。GLBは**Y-up・概念単位**でありMinecraftブロックへ直結する値ではない。
- **幾何学的数値PASS ≠ 通路完成 ≠ 美術PASS ≠ Minecraft Educationでの歩行/施工PASS**。厳格に区別。大規模アトリウム、厚い都市断崖、上下公共空間が遠景から読み取れることが美術上の中心目標。
- 細かい差分と保守的なGitHubコミットを好みつつ、1工程は美術上意味のある実装＋実3D GLB/OBJ＋固定4視点＋同条件QA＋日本語監査＋独立Draft PR＋GitHub成果保存までまとめる。段階を微細化してQAだけ増やさない。専用CIはpath-filtered/push-only/concurrency制御し、従来の安全ゲートの無断停止はしない。
- 作業はChatからGitHub connector / GitHub Actions中心に進め、ユーザーが手元でZIPやCMD操作をしなくて済むようにする。Blender等のリアルな本格3D表現で美術評価が著しく向上する場合にはWork/ローカル利用を合理的に検討するが、利用自体を目的にしない。

## 正本・最新確定

最新A13研究：Draft PR **#49** (https://github.com/ryomashibaba/makecode-limitlab/pull/49)。
ブランチ：dev/g4c7-a13-unified-megafold-comparative-study。
研究コード/既存基点：tools/g4c7_a13_megafold_comparative.py。
A13の研究記録：docs/G4C7_A13_UNIFIED_MEGAFOLD_ART_HOLD_JA.md。
検証：.github/workflows/verify_g4c7_a13_megafold.yml。
最新全ジョブSUCCESS：https://github.com/ryomashibaba/makecode-limitlab/actions/runs/40159363403。
A/B/C三案のGLB・OBJ・数量QA・四視点の4列比較画像が**GitHubへ恒久コミット済み**：
artifacts/g4c7-a13/。
モデル検証・保存後の確定コミットは **153a7c494651db910fd6afa0ef550782726bbecd**（このLIVE HANDOFFを加える前）。以後は最新HEADを照合すること。

## 過去の重要な研究工程・失敗から得たこと

- A5 Draft PR #41: Blender基点の二重大アーチ文化地区。436 GLBメッシュ、BLEND/GLB、四視点比較。ART HOLD。模型は見られるが建築内部の使い方、足元の経路、魅力的な重層都市の印象が弱い。
- A6 Draft PR #42: A5を元に上空スラブを開放したロフト・リボン案。579メッシュ。建築的に空が開いたが、見せかけの門や実際の移動接続が未完成。
- A7 Draft PR #43: SOUTH主アーチの殻・床を実ブーリアンで切り抜き、橋床・地盤支持・上空スロットを追加。587メッシュ。308/308の中心足元サンプル支持。検査は全身干渉でもMinecraft歩行でもなかった。
- A8 Draft PR #44: 旧ランプと回廊の中心線距離約3.354概念単位を実接続床・4支持柱で補完。592メッシュ。3レイ×331=993の足元支持を検査。992/993支持、67/331の人体包絡表面交差を発見。保守的なSATは三角形と検査BOXの表面交差であって、全面的な立体内含有と実歩行を証明しない。
- A9 Draft PR #45: 南主アーチ外殻とガラス帯の実切除、地上のアプローチ湾曲と乗換床を修正。590メッシュ。**67→45**地点の人体BOX表面干渉、支持不足1→0（当時のin-memory測定）。4視点で既存建築の質量・空間がほぼ変わらず美術HOLD。なお、**コミットされたA9 GLBを別工程で再読込すると端部の支持不足1/993**が検出された。メモリ上と保存GLB再読込の差を明確にして、A10で実床を伸ばして再読込後0/993へ修正した。検査許容差のごまかしは禁止。
- A10 Draft PR #46: 本物の中空をもつ非対称二重居住バンク、内部床・開口4・地盤支持6・2横断デッキ。602メッシュ。モデル高層化の後、既存45地点の干渉・0支持不足を維持。ただし遠景ではアーチの下に小さなポッド2つに見え、美術不合格。
- A11 Draft PR #47: 二つの非対称な巨大人工断崖を追加。613メッシュ（B2改修）。旧A10比、最高Y約94。実空洞、左右合計8実切欠き、両岸6段丘・2空中大路・中央高さ45概念単位上昇の大公共スパイン。GitHubモデル保存・CI成功、既存経路45表面干渉/0支持不足を維持。美術は壁面が単調で大きな彫刻に見える。
- A12 Draft PR #48: コミット済A11-B2 GLBの実断崖から、楕円球近似カッターで西16,307.93/東17,770.98概念体積単位を追加で削り、5巨大アトリウムと5実床・1上部公共体積を追加。**613→619**メッシュ、4視点、45/331と0/993維持、GitHub全保存成功。側面・斜視は向上する一方、旧大アーチと断崖がバラバラに見える。
- A13 Draft PR #49: A12 619メッシュを基点に、構造全体の主従を探る三案を同じCIで比較。すべてGLB再読込・QA SUCCESS、出力一式GitHubに永続保存。
  - **A案**: 旧アーチを全保存＋上空大フォールド＋斜め4リンク。624メッシュ、最高Y106.163。**ART REJECT/HOLD**：都市の上の「浮遊屋根」に見える。
  - **B案**: Aで旧innerは残したまま、旧outer load shellを2メッシュだけ研究コピーで省略。622メッシュ、Y106.163。**ART REJECT/HOLD**：上空屋根感が大きく改善しない。
  - **C案**: 旧inner/outer shell計4メッシュを**研究コピー内のみ**省略し、大フォールドを上空ではなく中層Y31～51.99へ置き直す。616メッシュ、全体最高Y94.063。都市層が見やすくなったが、**あくまで次研究の参考候補・ART HOLD**。load shellの省略は構造安全証明ではなく、実施工への解体指示でもない。
  - A/B/Cとも既存歩行経路**331人体検査地点、993足元サンプル、身体半幅0.65、高さ0.15～3.25、意図的障害物の負の対照を変更せず**、**45/331の未解決表面干渉**と**0/993未支持**。QA緑と機能合格を混同しない。

## 次にやるべきこと（新チャットの担当AIへの指示）

1. このLIVE HANDOFFより先に、GitHubのA13 PR #49、HEAD、artifacts/g4c7-a13/a13_comparative_geometry_qa.json と4枚のA12/A13-A/B/C同カメラ比較画像、Actions #40159363403を必ず読み、事実を更新。
2. **ART-FIRSTの方向性を再評価**：Cをそのまま採用・Minecraftで施工してはいけない。A/Bの浮遊屋根の失敗を繰り返さず、既存大アーチ・左右の巨大人工断崖・公共階層を一体の都市の巨大負空間として整理する。本当に壮大で、遠景でも複層都市が読み取れる造形を優先。単に窓を増やす、再度上に屋根を載せる、箱を反復、同じ曲面を太くするだけの小修正を避ける。形態・素材・アーチ/リング等を固定的に禁止せず、芸術目標に従って自由に造形してよい。
3. 次工程はA14などの独立した美術研究ブランチ＋Draft PRを適切に設け、**明確に異なる実GLB形態**を制作。4視点すべてでA12/A13-Cと同縮尺比較し、幾何QA/負の対照と美術の採否を別々に記録。構造上重要そうな旧殻を外す案は「未検証」と明示し、後工程で本当の荷重支持・接合・内部からの公共経路を設計する。
4. 一度の工程で実体制作・四視点画像・再現ソース・QA JSON・Actions・GitHubへの自動アーカイブまでまとめて作業。CIの成功後は**保存ジョブもSUCCESS、GitHubブランチに全ファイルが存在するか**確認。古いActionsの成功を最新HEADのPASSと取り違えない。
5. **永久HOLD条件**：Minecraft Educationの施工、ワールド書換え、USED・古い実機QA証拠の上書き、都市統合は行わない。A5～A13原本を保護する。構造・内部歩行・手すり・建築防火等が未検証でも「達成」と呼ばない。
6. 可能ならこのLIVE HANDOFFを工程完了ごとに簡潔に更新し、新チャット移動のたびに長大な文書を再作成する負担を減らす。

## A14 研究中（2026-10-25 JST、ART HOLD）

- 独立研究ブランチ：dev/g4c7-a14-tectonic-civic-braid-art-study。起点HEAD fd86ec4f2a62e788fb26b0e1f59efb4bbe96041b。A13 PR #49とA5～A13原本は未マージ・原形維持。
- 造形仮説：研究コピーのA13-C（616メッシュ）から旧A12上空クレセントとA13-C中層横断フォールドだけを省略し、断崖を上下に縫う一つの大きな立体的都市フォールドに置換。旧殻4メッシュの省略はA13-C研究コピー由来であって撤去・荷重安全証明ではない。
- 再現コード tools/g4c7_a14_tectonic_civic_braid.py。監査 docs/G4C7_A14_TECTONIC_BRAID_ART_HOLD_JA.md。専用CI .github/workflows/verify_g4c7_a14_tectonic_braid.yml。
- CIにて実GLB/OBJ、固定四視点のA12/A13-C/A14同縮尺比較画像、QA JSON・provenanceを生成し、成功後に artifacts/g4c7-a14/ へ自動アーカイブ。CIと保存両方のSUCCESSを確認するまで成果完了とは呼ばない。
- QAの人体331地点/足元993点/半幅0.65/高さ0.15～3.25/意図的負の対照は変更禁止。45地点の既存表面干渉を悪化させず支持不足0を保つ。緑の幾何CIは歩行証明・美術PASSではない。
- ART HOLD、Minecraft施工禁止、都市統合禁止、未検証の荷重支持・内部歩行・避難・接合。旧Minecraft World・USED・CSV・ZIP・過去の実機証拠を触らない。画像確認後、蛇状の孤立構造に見えたらREJECTしてさらに形態修正。

### A14 美術試作の追加監査（2026-10-25 JST）

- A13専用Actions成功run 40159363403から実A13-C GLBと比較PNG、A12専用Actions成功run 40156977781から実A12 GLBを取得。GitHub上の実バイナリと4視点画像を直接確認した。A13-Cにも前面旧大アーチが強く残る。
- A14の新連続帯状立体を同一の実A13-Cモデルへ適用し、独立のローカルGLB再読込・front/oblique/side/aerial比較を行った。単体メッシュは1128頂点/2252面、watertight・正体積約56,052概念体積単位。候補全体は615メッシュのGLBとして再読込できた。
- 【美術暫定判定：REJECT / ART HOLD】新しい帯が分離した蛇状の付加物に見える。旧前面アーチが相変わらず主役。美術的な大幅改善を達成したとは言えない。単体の幾何PASSは美術採用に一切使わない。
- 専用GitHub Actions run 40161602783 は2026-10-25 JSTの確認時点でqueued。旧幾何経路331/993点・negative controlの実行結果は未取得、専用CIのarchiveジョブも未成功。GitHubに完成モデルと比較画像が恒久保存されたと主張しないこと。
- 追加の大きな双翼試作もローカルで四方向検分したが、別々の巨大塔に見えるためGitHub本案には未採用。未来都市の立体的な一体感を優先し、次は前面旧アーチ自体の主従も抜本的に再設計すること。
- 関連の一次監査はDraft PR #50のConversationコメントを参照。禁止事項（Minecraft施工・都市統合・旧原本書換え）は継続。

## A15「天裂双流殻」継続研究（2026-10-25 JST）

- A14 PR #50は実制作自体と継承331/993幾何QAの専用Actionsを成功させたが、成果保存pushがLIVE HANDOFF更新と競合して失敗した。Actions #40161602783のbuild-and-qa=SUCCESS、persist-a14-research=FAILURE（non-fast-forward）。A14専用workflowのアーカイブをrebase-safeへ変更。美術は暫定REJECT。
- A15独立ブランチ dev/g4c7-a15-split-tide-sculpted-urban-shells。基点はA14の保存処理修正後のHEAD。A15は不合格の追加蛇状帯を一切使わず、GitHub保存済みA13-CのA11/A12左右大断崖・中空・公共段丘など**23メッシュをそれぞれの実3D表面ごと変形**する2方向比較。
- A15-Aは内側へ巻き込む巨大都市双殻（上端約141）。A15-Bは空へ外側に開花する裂け目形の巨大殻（上端約158）。両方地面近傍Y<=14は変形しない。A/Bとも約610メッシュ。数値はローカル予備検証でありGitHub Actions確定値はCI成功後に確認。
- ソース tools/g4c7_a15_split_tide_urban_shells.py、文書 docs/G4C7_A15_SPLIT_TIDE_ART_HOLD_JA.md、専用CI .github/workflows/verify_g4c7_a15_split_tide.yml。成果予定 artifacts/g4c7-a15/（A/B実GLB+OBJ、A12/A13-C/A15-A/Bのfront/oblique/side/aerial固定4列比較、QA JSON）。
- 元の331人体サンプル／993足元／半幅0.65／高さ+0.15〜3.25／負の対照を一切緩めない。既存45表面干渉より悪化不可、0未支持維持。成功しても通路安全・荷重・自己交差検証・美術承認は別物。
- **ART HOLD、NO MINECRAFT CONSTRUCTION、NO CITY INTEGRATION、原本・ワールド・USED・CSV・ZIP・実機証拠保護**。旧A13-Cコピーで省略した歴史的load shellの撤去を承認するものではない。4視点の実画像と専用Actions/保存のSUCCESSが揃うまで完成を主張しない。

## A16「Living Oculi — 生きた空洞都市」美術研究開始（2026-10-25 JST）

- A15独立Draft PR #51、起点HEAD d15f0f2cf22bb5c75c0a7d3596e0c94a02f13744。A15-A/Bローカル実GLBは再読込実測A610メッシュ最高Y約141、B610メッシュ最高Y約158だがART HOLD。A15専用Actions run 40164110635は前回の確認時queuedでGitHubへの実GLB恒久保存は未確認。正本の状態は必ず再確認。
- A16独立研究ブランチ dev/g4c7-a16-living-oculi-void-city-art-study。既存A13-C実GLBをread-only再読込→A15-Bの本体変形（610メッシュ）→A16 A/Bの**巨大な実Boolean空洞を両岸2か所ずつ計4か所削る**。A15の二本の壁にしか見えない問題への次の実体美術仮説であり、単なる小窓追加ではない。
- A16-Aは大きな非対称Tidal Oculi、A16-Bはさらに偏ったOpen Crown Abyss。中空の左右都市外殻から実体積を減らす設計。歴史的A5-A15は改変せず、Minecraft Construction/City Integrationは禁止。旧A13-Cで既に省略されたload shell4メッシュは新たに壊さず構造検証未実施。
- 実装 tools/g4c7_a16_living_oculi_void_city.py、設計と安全 docs/G4C7_A16_LIVING_OCULI_ART_HOLD_JA.md、専用CI .github/workflows/verify_g4c7_a16_living_oculi.yml、完成後の成果予定 artifacts/g4c7-a16/（A/B実GLB/OBJ、A15-B参照GLB、同視点比較front/oblique/side/aerial PNG、QA JSON/provenance）。
- A16は**実物をBoolean差分で切り抜いた体積・閉体積・GLB再読込**を必須とし、モデル用の見かけだけの穴は不可。旧331人体包絡/993足元/半幅0.65/体高さ0.15~3.25と故意障害物負対照の閾値を絶対緩めない。45人体干渉/0未支持以上に悪化したらCI失敗。ART PASSではない。
- A14の保存時push競合を反省し、専用CI保存ジョブにはgit fetch→rebase→push（force無し）を実装。GitHub上に成果物全ての実在・CIの保存ジョブSUCCESSを確認するまで完了宣言禁止。
- **美術判定は未審査ART HOLD**。巨大な開口でも単なる壁面の4窓に見えればREJECTし、さらに一体の立体都市へ根本設計する。人体通行・多層階接続・構造・自己交差・避難・防災はNOT VERIFIED。旧World、USED、CSV、ZIP、実機証拠の完全保護。

### A16 造形の最低実体量チェック（2026-10-25 JST）

- 初版の『4個の切削を実施した』だけではA12と似た小開口の量産になり得るため、A16 Python・専用CIに**各開口で600超の実体積除去、各巨大断崖の元体積比3.5%以上の除去**を追加した。数値のみで美術PASSにしない。未達の場合は正常な不合格として扱い、閾値の緩和ではなく根本的に造形を変える。
- 最終アーカイブ先 artifacts/g4c7-a16/、CIのbuild/QAとpersistの双方のSUCCESS、完成ファイル存在、4視点での美術審査をすべて別々に確認すること。未確認ならART HOLDを維持。


## A17一体断層都市の独立形態研究（2026-10-25 JST、ART HOLD）

- A16 PR #52（ブランチ `dev/g4c7-a16-living-oculi-void-city-art-study`）のActions run **40165116192** は前回再確認時 **queued**（build/QA・persistとGitHub実成果物は未確認）。**A16の不合格は未確定**。保存済み`artifacts/g4c7-a16/`の存在を確認するまで成功扱い禁止。
- A17はA16を不合格と決めつけた置換ではなく、空き工程で始めた独立した対抗形態研究。独立ブランチ `dev/g4c7-a17-monolithic-rift-fold-art-study`、Draft PR **#53**（https://github.com/ryomashibaba/makecode-limitlab/pull/53）。
- A17実装 `tools/g4c7_a17_monolithic_rift_fold.py`、専用CI `.github/workflows/verify_g4c7_a17_monolithic_rift.yml`、日本語監査 `docs/G4C7_A17_MONOLITHIC_RIFT_FOLD_ART_HOLD_JA.md`。
- A17-AはAscending Sky-Wound、BはCascading Civic Caldera。既存A13-C実GLBとA15-Bを研究コピーとして再構築し、**新研究コピーの2断崖包絡を一つの巨大な閉体積の折れた人工大地に置換**。ボクセルの空間占有格子と実iso-surfaceにより本当の3D負空間を作る。Boolean切削の実測と偽らず、占有格子除去量と実閉体積を別に報告。歴史的ソース、A5〜A16原本・Minecraft実機には書き込まない。
- 限定的なローカル形態試作で、A/B各単一連結の真のwatertight GLB単体が生成された。**ただし市街地608メッシュとの結合モデル・本来の331/993ルートQA・Actionsのモデル保存は未確認**。2候補とも単独形状は巨大スラブ状で都市の魅力には未達の疑いが強いため、**ART HOLD**。未検証を美術PASSとしない。
- Actions成功後、`artifacts/g4c7-a17/`に実A/B GLB/OBJ、参照A15-B GLB、front/oblique/side/aerialの4列比較、QA JSON・provenanceが揃い、archiveジョブのSUCCESSまで確認する。旧331人体・993足元、半幅0.65、足元+0.15〜+3.25、負の対照、45表面干渉上限と未支持0を**絶対緩めない**。欠ければ失敗として原因を修正。
- **ART HOLD / NO MINECRAFT CONSTRUCTION / NO CITY INTEGRATION**。古いworld、USED、CSV、ZIP、過去の実機・モデルは完全保護。新人工大地と旧階層都市の荷重接合、内部経路、柵・避難・歩行は全て未証明。
