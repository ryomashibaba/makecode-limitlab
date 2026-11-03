# M37-P2：本物のBlender 3視点からART-FIRSTの失格証拠を抽出し、次の作者修正へ返す

2026-11-03 JST。**新しい完成都市の作成ではなく、実画像と3D構造を照合するフィードバック経路の追加。**

## 実際の検証結果

- [新CI #41552562056 SUCCESS](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41552562056)。既存の2メッシュの非美術試験を保護されたv3から別名保存した真正Blenderに再生し、3つのCycles PNGを**同一の保存済みBLEND**から再生成した。
- 新スクリプト `tools/g4c7_m37p2_visual_feedback_gate.py` は、3枚のPNGのSHA256をJSONと突き合わせ、原本改変・Minecraft書込・正式安全QA実施なし・ユーザーART採用0を確認する。P2の試験はメッシュが各8頂点6面、`true_city=false`、製造境界・研究文化・居住内観が`NOT_AUTHORED`であるため、自動判定は**`EARLY_ART_REJECT`**。これはAIによる美術合格ではなく、不足が確実に分かる内容を正しく拒否した証拠。
- CIで`P2_GENUINE_VISUAL_ART_GATE EARLY_ART_REJECT official_adoptions=0`と`TRUE_CYCLES_THREE_IMAGES_ART_FIRST_EARLY_REJECT_TECH_NO_ART_PASS`が出力された。構造ゲートの独立回帰テスト5件成功。GitHub artifact `g4c7-p2-paired-native-true-three-views-tech-only-not-art`に3真正PNG／旧レンダレポート／新フィードバックJSON／持ち運び可能な比較HTMLを保存。
- `--vision-model gemma4:26b`（任意）のときだけ、**既存のOllama 127.0.0.1:11434**に3枚を画像入力し、日本語でAERIAL、PUBLIC_EYE、HABITAT_EYEの見える物・欠ける実体・次の造形判断を短く求める。モデルを自動インストール・ダウンロードしない。Gemma 4のOllama画像入力は公式ドキュメントでサポートされている。ただしこのチャットでは**ユーザーのPCのGemmaをまだ実行していない**ので視覚LLMの精度は未検証。
- どんな場合も結果は`EARLY_ART_REJECT`か`ART_HOLD_VISUAL_JUDGMENT_REQUIRED`だけで、コード上**ART PASSに到達できない**。画像モデルの解釈は参考情報であり、ユーザーの正式採用・安全確認の代替不可。コードや自由なbpyスクリプトをモデル生成させたり、Minecraftを書き換えたりしない。

## 明確になった次の作者造形への要求

初回ネイティブ編集試験で、保存・編集・実3視点描画の機構は成立しているが、`city_macro`＋`habitat`の各直方体では現実の都市の証拠が何一つ無い。画像フィードバックに基づき、**実際の作者が**一体の街並みと住居内部・工場見学境界・研究文化の実建築を同じBlender原本で彫刻的に編集する工程へ移る必要がある。単純なEdit操作を増やす、座標JSONを再び一括出力させる、画像だけを未来都市風に加工してBlender作品と称する代替は不可。

## 守る状態

ART-FIRST／全体ART HOLD／正式採用0／331人体・993足元とG0/S1/G1/G2/G3 NOT RUN／MakeCode未評価／Minecraft施工禁止／main保護／PR #53 Draft／Work事前承認制（今回は不使用）。実美術作品の正式採用やMinecraft施工を許可する文書ではない。
