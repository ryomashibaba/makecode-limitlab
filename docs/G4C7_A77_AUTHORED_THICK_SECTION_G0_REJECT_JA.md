# G4-C7 Orbital Commons / A77 — 3つの居住厚層を直接造形した真正VTK G0、ART REJECT

**2026年10月27日 JST／A76基準HEAD `be2774dee47792fab9e29cefa09b8f0430cae043`／正式美術採用0・全体ART HOLD・Minecraft Education施工/都市統合禁止**

## 何を実際に変えたか
A76では4棟の形式を数千の浮いた小室に拡大したため、遠景が塔状の反復棚だった。今回は「小室の数」から形を決める生成器を廃止し、**研究、工房、住宅を内包する大きな3建築断面の平面ポリゴンを作者が個別に指定**。各断面に5枚ずつ、合計15枚の実三角形床を作り、上下の建築表皮も各断面から接続した。地上には小規模の市場、制作、閲覧、屋外公共床を別の実形状として作った。

[A77 SHA固定再現Python](../artifacts/g4c7-a77-thick-sections/a77_spatial_section.py.gz)の展開元SHA-256は`f20da46403b51c107196f1215c270629bf8d3fdc85b2f447d9e11e7c95578740`。専用Actionsが凍結原本を展開し、実VTK/OpenGL 3画像・OBJ/MTL・マニフェスト・局所断裂監査を生成する。GitHub保存を実際に確認するまで、再現ActionsのTECH PASSを宣言しない。

## ローカルで直接実行・画像目視したG0結果
- 真正OBJ/MTL、1280×800の3画像を生成。形状バウンディングボックス**(-320,-219,-12)〜(320,291,300)m**、水平約640×510m、上端300m。
- **281構成メッシュ／2,036三角形／OBJ頂点1,680**、形状正本は人が選んだ3建築断面×各5階の**15の異なる実床ポリゴン**。実床の存在は確認できるが、人口が居住・通行できる実証ではない。
- **斜視：G0 ART REJECT。** 3つの高さの違う巨大な「縦型本棚・厚い開放棚」に見える。A68で失敗した厚板の複数階化と同じ形態。高所の活動部品は散発的な小片で、都市全景として魅力的な生活密度や未来文明の空間はない。
- **人間目線：G0 ART REJECT。** 暗い巨大壁、むき出しの骨格と小規模な市場が見えるのみで、住みたくなる近景ではない。同一真正3Dのinside追加画像も同様。
- **設計上の明確な通行断絶**：段高0.18mの各20段は描画されたが、第一階段の末端 `(-4,-25.6,3.6)` と第二の始点 `(-4,-17,3.6)` は同じ高さで**8.6m離隔**。第二の終点 `(2.4,-17,7.2)` と閲覧実床の最南縁y=15との差が**32m**。橋・踊り場の接続床を作っていない。全15実床への上下アクセスはない。これは**既知欠陥のG0幾何再現**であり、正式歩行・避難のQAではない。
- 「床上1.7mの人間目線」のカメラは `(0,-112,1.7)` だが、基壇上面との相対高さの意図に限る。**VTK raycastによる支持・床接触実証は行っていない**。

## 新しい根本反省（A68との厳密な比較）
部屋を量産しなくても、**各階の大きな多角形床を水平に積み、その外縁同士を垂直の連続壁でつなぐ設計命令そのもの**が棚状の建築を生む。形を決めるのが小部屋か巨大床かという違いは本質ではない。都市の生活する空間を十分にデザインせず、15の「フロア」という機能名を外形に置き換えても魅力は生まれない。

## A77保存後の厳格な方針
- A77全体は**G0 ART REJECT**。改修・大型化・Minecraft施工・正式美術採用禁止。写真やPNGに意味のない成功ラベルを描かない。
- A73で確認した「公共床と入口を同一データから作る方式」はまだA77に接続しておらず、その技術PASSをA77の動線として転用しない。
- 次工程A78では「複数の水平床」「開放した棚」「曲面の外皮」を改良して進めない。**地上・高所の活動空間、必要な空洞、非反復の主要厚みと外形を作者が同時に決める実際の構成方法**を根本から調べる。完全な用途・経路の対応を見せるまでは同型試作を量産しない。
- 旧331人体／993足元、半幅0.65、足元+0.15〜+3.25、身体干渉45以下、未支持0、故意負対照の正式G2/G3契約を変更せず、**S1/G1/G2/G3はすべてNOT RUN**。Minecraft Education施工/都市統合禁止。歴史原本はappend-only保護。Work利用はユーザーの事前許可が必要。通常CI既知の`build/g4c4_access_baseline.json`欠落を偽データで修復しない。

**実制作の結論：美術的突破なし。A77の唯一の有用な成果は、「小部屋反復でなくても大きな階床反復が同じ棚状形態を生む」ことを、真正3Dで確かめたこと。**

## A77 GitHub独立再現・真正ファイルの保存確認（2026-10-27 JST）
- [専用VTK Actions #40506547138](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/40506547138) **SUCCESS**。完全固定gzipをPythonへ戻し、原本SHA-256 `f20da46403b51c107196f1215c270629bf8d3fdc85b2f447d9e11e7c95578740`を独立照合。1280×800の同一VTK3視点、OBJ 1680頂点/2036面、15床を再生成。故意に保持した階段8.6m・閲覧床まで32mの設計欠陥も自動確認。
- botのappend-only原本保存コミット [`cba9802decd91bd8b914ed5ed49bfacb170db4fc`](https://github.com/ryomashibaba/makecode-limitlab/commit/cba9802decd91bd8b914ed5ed49bfacb170db4fc)。[再現Python](../artifacts/g4c7-a77-thick-sections/a77_spatial_section.py)、[実3D OBJ](../artifacts/g4c7-a77-thick-sections/output/a77_authored_real_section.obj)、[MTL](../artifacts/g4c7-a77-thick-sections/output/a77_authored_real_section.mtl)、[遠景](../artifacts/g4c7-a77-thick-sections/output/oblique.png)、[眼高](../artifacts/g4c7-a77-thick-sections/output/public_eye.png)、[内観](../artifacts/g4c7-a77-thick-sections/output/inside.png)、[manifest](../artifacts/g4c7-a77-thick-sections/output/a77_manifest.json)、[事故/美術判定JSON](../artifacts/g4c7-a77-thick-sections/output/a77_rejection_evidence.json)を保持。
- **ローカル原本とのGit blob SHAは7/7完全一致**（Python、OBJ、MTL、PNG3枚、manifest）。設計不良JSONはGitHub上で独立再計算されており、ローカルJSONと文字列が若干異なるが判定値は同一。出力先だけの付け替え、PNGの合成図を「真正3D」と偽る操作はなし。
- [A77通常CI #40506546937](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/40506546937) は最後に確認した時点で**queued**。合格とは主張しない。直前A76の[通常CI #40504025279](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/40504025279) はFAILで、既知の`build/g4c4_access_baseline.json`欠落が継続。偽baseline追加・skipは禁止。
- **結論**：技術の真正再現PASSは美術PASSではない。三つの巨大な「居住厚層」は見た目が棚建築でREJECT、生活経路も断絶。正式美術採用0、全体ART HOLD、S1/G1/G2/G3 NOT RUN、Minecraft施工・都市統合禁止は不変。
