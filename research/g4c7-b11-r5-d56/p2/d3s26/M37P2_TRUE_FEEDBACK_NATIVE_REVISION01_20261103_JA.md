# M37-P2：実Cyclesフィードバックから保存済みBlenderを1回編集し、3視点で再判定した研究結果

2026-11-03 JST。**TECH PASS / ART REJECT / ART HOLD / 正式作品採用0**。

## この工程で本当に実行したこと

[CI #41554510076 SUCCESS](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41554510076) により、仮の2役割ネイティブBlenderシーンを相手にして初めて次の一連の処理が成立した。

1. **実シーン→実画像**：一つの保存済み `.blend` から本当のCyclesでAERIAL／PUBLIC_EYE／HABITAT_EYEを生成し、3 PNGとSHAを照合。
2. **実画像→不採用根拠**：`tools/g4c7_m37p2_visual_feedback_gate.py`で `EARLY_ART_REJECT`、`TWO_CUBOIDS_8_VERTICES_6_FACES_EACH` などの不足を判定。偽のART PASSを許さない。
3. **不採用根拠→1回の編集案**：CIで**明示的に書いたテスト用JSON**に、元のネイティブBLEND SHA256、実画像フィードバックJSON SHA256、該当不足コードを埋め込む。**ローカルAIが自律的にこの編集案を考案した証拠ではない。**
4. **編集案→Blenderの真の頂点・面変更**：`tools/g4c7_m37p2_feedback_to_native_revision.py`が元の保存済み`.blend`とフィードバックのSHA一致を検査して、元メッシュの指定方向の**1つの面だけ**をBlender `bmesh`で`inset` / `extrude`し、元とは**別の**ネイティブ`.blend`へ保存。新しい立方体オブジェクトを追加しない。
5. **修正後の再撮影・再審査**：別名保存の修正版を読み込み、真正Cycles 3視点を改めて撮影、同じART-FIRSTゲートへ送信し、再び**`EARLY_ART_REJECT`**を取得した。合否に関わらず自動ART昇格しない。

## 構造と真正な証拠

| 項目 | 実測 |
|---|---|
| 変更前`city_macro` | 8頂点／6面 |
| 変更後`city_macro` | **12頂点／10面** |
| 変更前`habitat` | 8頂点／6面 |
| 変更後`habitat` | **12頂点／11面** |
| 元の保存済み試験BLEND SHA256 | `5f9e9b82eb952cdb4b32bab03e59dbe973c90ab80e5c9598750ea134a9d396ab` |
| 参照した実視点フィードバック SHA256 | `0471ac6632485cdcc1fa7299d191f358489d0903f645ea01158bc093de84a2af` |
| 新しい別名保存BLEND SHA256 | `6edc310147b35e2acaac4f5b7928eda577f1d50053a532dfe3c7f9694994cd78` |
| 編集操作 | 2件、既存メッシュのみ |
| 新しい3 PNG撮影 | 成功、AERIAL／PUBLIC_EYE／HABITAT_EYE |
| 最終美術判定 | **EARLY_ART_REJECT** |
| オリジナル上書き | **なし** |
| モデルが修正案を自律生成 | **まだなし** |

真正な修正後3画像を直接閲覧した結果は、**孤立した箱状の2形状**のままで、居住内部、街の連続性、工場の実作業、見学境界、研究文化を示すものではなかった。暗い面があるが光源や法線の原因は未特定。**美術改善の証拠はゼロ**。面数が増えたという技術指標を美術的成功として扱わない。

[CI実際の技術証拠artifact](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41554510076#artifacts)：`g4c7-p2-one-true-feedback-native-revision-before-after-not-art`。SHAを持つ修正証拠JSON、修正後の3真正Cycles画像、不採用フィードバック、HTMLレビュー。[最終追加保護CI #41555143899 SUCCESS](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41555143899) で、実3PNGのバイトSHA再照合・改変拒否の回帰テストが通過し、**本物の別名修正版`.blend`をGitHub artifactに保存した**。artifact名 `g4c7-p2-one-true-feedback-native-revision-before-after-not-art`、ID `13194850787`。

## この工程で追加した安全契約

- 提案アクションは`source_sha256`と`feedback_sha256`に厳密に結び付く。実ユーザーの保存Blenderへ不用意な操作をしない。
- `responds_to`は実際の`EARLY_ART_REJECT`理由コードだけ。自由Python、生成スクリプト、任意パス、`begin_surface`新規オブジェクト追加、無制限操作数は拒否。
- **同じ`.blend`には1回だけ**研究修正。既存メッシュ2領域を両方編集する条件。操作は最大8件で最大移動量・インセット量を制限。
- 元BLEND、3枚の実PNG、フィードバックJSONが変化していないか、操作の直前にSHA256を再照合する新安全ガードを追加。実画像のバイト列まで読む形で、JSONだけの判定に依存しない。
- 同じ保存済み試験BLENDを新しい都市として正式採用せず、ART HOLD／公式採用0／Minecraft施工禁止。

## 制作方針に対する率直な判定

本工程によって**フィードバック→本物のBlenderメッシュ修正→実画像再撮影→フィードバック**のメカニズムは成立。ただし試験では編集案は人が明示的に記述した小規模フィクスチャであり、**AI自身が実画像を解釈し、本格的な都市・生活断面を設計し直す閉ループは依然未成立**。この試験を単純な直方体修正だけで無限反復しても目標に到達しない。

次の美術工程に進む条件は、元の技術フィクスチャから離れ、同じBlender原本に都市全景・真正の生きた住居・製造・見学境界・研究文化が**本当に存在する作者造形**を準備し、実3視点ART-FIRSTで判断できること。脚本で作った板や箱の別案を「世界的都市」に偽装するのは禁止。

**固定**：ART HOLD、正式採用0、331人体/993足元＆G0/S1/G1/G2/G3 NOT RUN、MakeCode未評価、Minecraft施工禁止、main保護、PR #53 Draft、Work不使用／事前承認制。
