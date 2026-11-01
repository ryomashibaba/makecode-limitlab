# G4-C7 / M37-M — 人間目線の直接レビュー・Blender実メッシュ編集スタジオ

**2026-11-01 JST。限定METHOD TECH PASS。新規都市美術は未制作、旧M37-L ART REJECT継続。全体ART HOLD・正式採用0。Minecraft Education施工と都市統合禁止、main不変、PR #53 Draft/Open・未merge。**

## (a) 実物のモデルと美術評価

長期間のA/B不採用、M37-Lの湾曲した巨大チューブ構造のART REJECTを受け、**M37-Lの曲面形状を自動改良した新都市は作成していない**。

真正M37-LのSHA256 `85397f2ddc41cff6ef53d26813c7c57b1420318de840e78b5f7ec5ec3762bfc4` を開き、旧199実メッシュ＋9固定カメラを保存する不変参照シーンに維持したまま、新しい `M37M_DIRECT_AUTHORING_REVIEW_STUDIO_ART_HOLD` という**別シーン**に深いメッシュコピー199個・カメラコピー9台を作成。局所的な作者の検討（実オブジェクト選択、固定視点変更、2メッシュ試験移動、復元）に利用できる作業台にした。

4枚の比較用画像は**M37-Lの保存実Blenderモデルから以前に撮った真正Cycles参照画像のSHAピンコピー**。M37-Mとして新規に再レンダリングした画像ではない。旧M37-Lと編集開始時のM37-Mは同じ実形状・同じカメラであり、これを画像の根拠とする。**未完成の都市を制作・美術改善したとは判定しない**。既存の湾曲した外形に対する美術REJECTは解除せず、ART評価は「新候補なし」。

## (b) 実Blender作者レビューの機能と検査

Blender4.5.15上の実BLENDへ文字テキスト `M37M_RUN_ONCE_TO_ENABLE_REVIEW_PANEL.py` を埋め込み、明示的なRun Scriptで有効化するNサイドバー `M37-M Review` を作成。自動実行は許可せずBlenderのセキュリティ仕様に従う。

- **RESEARCH**：研究区床と関連する殻パッチの現物を選択し、RESEARCH_EYE固定カメラへ切替え。
- **HABITAT**：居住床と関連する殻パッチ、HABITAT_EYE。
- **MAKER**：製造見学側研究床と殻パッチ、MAKER_EYE。
- 限定プレビュー：2つの実メッシュデータブロックの頂点Xを0.1〜1の研究単位だけ一緒に移動。3問題箇所すべてで**実頂点が変わり、復元後に完全に一致すること**を別Blenderプロセスで確認。
- 編集スコープ：オリジナルの199メッシュと独立した編集コピー199を比較し、指定2メッシュ以外の変更は**FAIL CLOSED**。試験中に予想外の局所座標が混入しても監査で検出可能。
- 構造的な壁・床の接合や人体の自由歩行まで保証する機能ではない。現プレビューは**編集検証用の2メッシュ試験移動だけ**で、完全な連動設計や美術改善とは別。

独立再読込のネガティブチェックは `RESEARCH/HABITAT/MAKER` 各2件＋対象外メッシュ変更1件＝**7件**で、すべて検出・復元を実確認。また構築段階では認識不能の問題、過大な移動、ART誤昇格、別メッシュ変更、二重プレビュー、二重ロールバックの**6負例**を確認した。

> 重要：実行したのは**Blender headless上の編集ロジック／保存・再読込試験**であり、Blender GUIの人間操作テストはまだ実施していない。パネルコード自体はBLENDへ埋め込み済み。Blenderの実画面で手作業の彫刻を完了したという意味ではない。

## (c) Minecraft安全とコスト

331人体・993足元、人体半幅0.65m、頭上相対+0.15〜+3.25m、旧干渉上限45・未支持0、負の対照、G0/S1/G1/G2/G3は**正式NOT RUN**。原本の到達可能性、広域支持、避難、階段の連続歩行、MakeCodeブロック変換やFill/Clone/Placeのコストも**NOT RUN**。Minecraftワールド書込0。Blender座標は抽象研究単位で、Minecraft1ブロックと同一とは認めない。

## (d) ネイティブ原本とCI証拠

専用Actions **[#41317346178](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41317346178) SUCCESS**。最初のActions #41316498016 は保存済BLENDの実シーン名不一致でFAIL。元の制作草稿のオブジェクト名が実原本と異なることも修正し、最終CIは実名と本物のネイティブ保存ファイルを基準にしている。重い不採用3Dの再レンダリングは無駄なので中止し、既存SHA一致4PNGを再利用した。

- 新しい真正BLEND `M37M_DIRECT_AUTHORING_REVIEW_STUDIO_ART_HOLD.blend`：**2,832,487 bytes**、SHA256 `8671733deccbeb8ea0e911fc4b8411734df4158c928e1ebe2f5ebf1d0cc1a57c`。
- CI再読込監査：`M37M_INDEPENDENT_REOPEN_SCOPE_AUDIT.json`、`PASS_BOUNDED_GUI_AUTHORING_REVIEW_METHOD_ONLY`。保存された旧M37-Lの199メッシュ全件が別ファイルのSHAピン原本と一致。
- 編集UI・保存生成・独立監査のPython原文3本：`tools/g4c7_m37m_blender_review_panel.py`・`tools/g4c7_m37m_build_native_review_studio.py`・`tools/g4c7_m37m_independent_reopen_review_audit.py`。
- 実BLEND、4既存真正参考PNG、報告・原文・READMEを [研究ブランチ保存先](https://github.com/ryomashibaba/makecode-limitlab/tree/dev/g4c7-a17-monolithic-rift-fold-art-study/artifacts/g4c7-m37m-verified-native-review-workspace-art-hold) にappend-only保管。初回の失敗CIと取消した古い重いCIは履歴保持。
- 古いM35/M36/M37-K/L原本と旧Minecraftワールド、mainは全く上書きせず。

## (e) 絶対評価と次の工程の資格

**M37-Mは「編集によって元の構造を壊さず、現物を複数視点で確認しながら試作・復元する方法」の限定TECH PASS**。しかしM37-Lのチューブ都市の美術は以前どおりREJECTであり、新都市の完成度は上がっていない。次工程で今回の2メッシュ移動を大規模化して再び奇妙な箱・棚・連続チューブを生成してはならない。

続行には真正Blender内のユーザーがレビューする**特定の空間体験問題**（市民が何を見てどこへ行くか、製造を安全に見られるか、住民の動線を確保できるか）を1件ずつ、実室と外形の両方に結び付けて形状として提案し、同一モデルの遠景・眼高・内部・高所を検証する。**新しい3Dデザインの候補資格を得る前に、今回の編集操作や対象数を単純にスケールさせない**。GUI手編集を行う場合はBlenderアプリ上でツールパネルの実操作を確認し、メッシュの範囲外編集はFAILする。

**最終：M37-M限定制作環境 TECH PASS／都市ART REJECT継続／全体ART HOLD・正式採用0／331/993 NOT RUN／Minecraft施工禁止。**
