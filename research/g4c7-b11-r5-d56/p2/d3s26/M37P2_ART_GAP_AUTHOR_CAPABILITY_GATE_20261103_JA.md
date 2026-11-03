# G4-C7 / M37-P2 — 実Blender 3視点に基づく「作者造形必須」判定

2026-11-03 JST。**作品完成ではない。技術検証PASS／ART REJECT・HOLD／正式採用0。**

## なぜこの工程に変えたか

前工程の真正Blenderは2メッシュの各8頂点6面を、1回の面編集で12頂点10面・12頂点11面へ変更できた。しかし、AERIAL／PUBLIC_EYE／HABITAT_EYEで本当に見える建築は依然として孤立した箱状2体であり、住居の玄関→前室→居間→窓、造船製造、物理的見学隔壁、研究文化、都市の密集した連続街区が全くない。**頂点数やCIの成功は、都市美術の改善指標ではない。**

既に確定した方針「街を織り込む造船都市」は、直接作者が同じ真正Blender原本の中へ都市全景と人間の生活断面を同時制作することを要求する。箱編集の自動反復や新しい第三プリミティブ都市の生成はその方針に反する。

## 実際に実装・検証したもの

- [ART-FIRSTの作者造形能力ゲート](../../../../tools/g4c7_m37p2_art_gap_authoring_gate.py)と[7件の回帰テスト](../../../../tests/test_g4c7_m37p2_art_gap_authoring_gate.py)を研究ブランチに保存。
- [GitHub Actions #41556855447](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41556855447)：**completed/success**。本物のBlender 4.5.15で元・修正後の保存済みネイティブBLENDを各3視点Cycles撮影し、SHA固定の美術フィードバックを得た。その前後で新ゲートを実行した。
- 実行ログの根拠：
  - 修正前：`ART_FIRST_AUTHOR_DIRECT_CONTENT_REQUIRED_NO_ANOTHER_TWO_BOX_AUTO_GENERATION`
  - 修正後：`AFTER_EXTRA_FACES_ART_STILL_REJECT_MUST_CHANGE_AUTHORING_METHOD`
  - 両方とも`REQUIRE_NEW_DIRECT_AUTHOR_3D_CONTENT`／`model_calls=0`／`official_adoptions=0`
  - 回帰テスト7件はPASS。
- 証拠artifact：`g4c7-p2-one-true-feedback-native-revision-before-after-not-art`、ID **13195277229**。新ゲートの修正前／修正後の判定JSON、真正3視点PNG、旧修正BLEND（未採用）の技術データを保存。
- この新ゲートは**写真の美しさをAIが採点するものではない**。真正Blender SHA、3画像SHA、`true_city=false`や`NOT_AUTHORED`、2形状8頂点6面などの**構造的・来歴上の確実な不足**を照合し、無駄な簡易編集再試行を拒否する。不十分なデータや不一致ならSAFE STOP。すべて揃っていてもART PASSは発行しない。

## 次の作者造形でしか解消できない欠落

実際の作者作業で、同じ保存済みBlender原本に以下を実物として同時に制作する必要がある。

1. 店先／住戸入口／異なる軒や中庭を持つ**連続した高密度の都市全景**。
2. **玄関→前室→内扉→居間・机→街並みと空の見える窓**という本当に深さのある住居生活断面。
3. 複数の製造段階の搬送・治具・検査足場・揚重・収納を伴う**宇宙機工場の実作業**。
4. 工場職員専用の床・扉と分かれ、窓台と厚みを持つ**公衆見学空間と物理隔壁**。
5. **研究の机・装置、文化滞在域、採光中庭、実階段／昇降**と都市街路の連続。

AERIAL、PUBLIC_EYE、HABITAT_EYEを必ず**同じ実際に編集・保存したBLEND**から撮影し、失格なら早期にART REJECT。美術が承認される前に7〜9正式視点や安全QAは進めない。

**現環境の障害**：ChatからユーザーWindowsのBlender GUIを直接操作できず、Workも使用しないため、直接作者造形の自律実行環境はまだ成立していない。これを「今回のCITY ART完成」と言い換えない。新たな箱モデルや追加の自動押出しで穴埋めしたと主張しない。

## 変更しない固定契約

R0〜R5、ART-FIRST／品質優先、ART HOLD、正式採用0、331人体／993足元とG0/S1/G1/G2/G3 NOT RUN、MakeCode未評価、Minecraft施工禁止、保護v3原本SHA不変、main変更なし、PR #53 Draft・未merge、Workは事前明示承認制（今回は未使用）。
