# M15 — ネイティブBlender 3D可視制作の実行契約

ユーザーが選択した**ローカル**Codex + Blender MCP から、AIが本物のBlender画面と3Dシーンを観察し、**実際に造形を2回以上修正した前後差分**を残す。接続未成立ならNOT RUNで停止。第三者製プラグイン導入はユーザーの判断による。

- 正本 `ryomashibaba/makecode-limitlab`、ブランチ `dev/g4c7-a17-monolithic-rift-fold-art-study`、PR #53 Draft。main編集/force push/merge禁止。
- ART HOLD、正式採用0、Minecraft Education施工/統合禁止。正規331人体/993足元・G0/S1/G1/G2/G3はNOT RUN。LimitLabに別プロジェクトの10km級規模条件を持ち込まない。
- M11〜M14のART REJECT形状（板、箱、棚、彫刻高層塊、リボン外殻）を流用しない。M13真正.blendは参照用のみ、SHA256 `0950a2bb166e5db302ca100638e3aab7764ca702babd842aae193e2417d6b319`、原本上書き不可。
- 新規の `M15_AUTHORING_01.blend` を用意。第一対象は巨大都市全体ではなく、一人の市民が**公共街路→実開口→製造ホール→採光アトリウム→階段と踊り場→研究ギャラリー→住居アプローチ**と体験できる一つの建築空間。
- 非反復的な都市美術は、実室・光・視線・人の活動・構造厚み・上下移動を同時に観察して導く。巨大外殻のコード生成と装飾後付け禁止。
- 最初に3D GUIのscreenshotが取得でき、assistantが見ていることを実証。シーン情報だけ、Pythonが動いただけでは不十分。スクリーンショット→直接造形→次のスクリーンショットを少なくとも2回。
- 8視点 `south,north,oblique,district,street_eye,maker_eye,research_eye,resident_eye` を同じ保存シーンから撮影。画像・見える用途・厚み・採光・実開口・反復性で厳格な美術不合格判定を行う。
- 保存した.blendの再オープン、8画像、比較スクショ、短い監査・SHA一覧を作成。少数の軽い成果物ZIPを会話に添付。美術採用はユーザー判断。正式安全QAとMakeCode施工はまだ行わない。
- Blender MCPはlocalhost限定、`DISABLE_TELEMETRY=true`、外部アセット/オンライン3D生成と第三者データ送信を避ける。CodexのAIがアクセスできるPC範囲で作業するためファイル削除・プラグイン追加インストール・重要リポジトリ書込みは禁止。

この指示だけではM15実3Dが作成されたことにならない。実画面/モデル/画像/差分が残って初めて制作工程を実施済みとする。
