# M37-P2：全市一括頂点を廃止し、Blenderネイティブ編集操作へ（新METHOD・技術研究）

2026-11-02 JST、**ART HOLD／正式採用0／真正な都市美術の完成0**。

## 根拠と選定理由

先のQwen3:14B実実行は11メッシュ中の全12面が不正、5メッシュで同じ頂点配列を流用。旧方式を繰り返すのはART-FIRSTに反する。11メッシュの頂点座標と面インデックスをモデルに一括記述させる工程は**正式にRETIRED**。GitHubの既存コマンドランチャーとPowerShell経路は安全停止する。

調査した別経路：
- Blender Lab MCP（Blender Foundation管理プロジェクト）: https://www.blender.org/lab/mcp-server/ 、 https://projects.blender.org/lab/blender_mcp 。GUIのBlenderをMCPから操作でき、スクリーンショットとオブジェクト概要も取得可能。しかし公式ページの警告通り、**LLM生成コードの実行にデータ保護ガードがない**。ユーザーの実PCで現段階の無制限導入はしない。
- Blender 5.2用 typed MCP候補 `ceeyang/blender_mcp`（2026-09-08の調査時HEAD `d3bfbcc751d398d2ae6436a72a1ee901a700aa37`）: 一部にGUIスクリーンショット・undo・モデル編集・オブジェクト検索のtyped tools。ただし `execute_code` があり、localhost TCPの実装にもアクセス制御の検証を要する。無条件採用禁止。
- LM Studioは0.3.17以降MCPホストに対応： https://lmstudio.ai/docs/app/mcp 。Ollamaの`/api/chat`によるtool calling、`qwen3:14b`のtool対応は公開ドキュメントで確認できた： https://docs.ollama.com/capabilities/tool-calling 、 https://ollama.com/library/qwen3:14b 。

**採用した技術研究の方向：** 外部の無制限コード実行MCPを入れずに、標準Ollama APIでモデルが許可済みの**少数のBlenderネイティブ編集操作**を選ぶ。こちらのPythonはその操作のみ実行し、都市形状を固定のbox/plate/wall/bridgeジェネレータで決めない。原本SHAを検査して**隔離した別名`.blend`へ保存**する。作業単位は全景と住居の厚みを同時に見る**1ペア**。正式な美術作品でなく実ツール能力研究として扱う。

## GitHubに実装したもの

- `tools/g4c7_m37p2_native_operator_author.py`：アート方向を宣言する小規模`actions`の検証器、`begin_surface`、`extrude_face`、`inset_face`、`translate_selection`の4許可済みBlender Edit Mode操作の再生。Pythonコード・自由なbpy API・path指定・Minecraft書込コマンドをモデルから受け付けない。**両役割同時必須、同じ役割で複数seed禁止、編集の実際の変形量上限、ART HOLD固定**。1役割あたりのseedは試験用の起点であり、固定形状を反復して都市を量産する許可ではない。
- `tools/g4c7_m37p2_ollama_paired_native_action_proposal.py`：ユーザーの既存Ollamaに`tools`スキーマを渡し、1回の短い関数呼出しから**編集命令データだけを得る**研究経路。失敗時はHOLDレポート、成功時も**レビュー前の操作データ**のみ保存する。モデル生成の任意Pythonは実行しない。実Ollamaモデル実行はまだ**行っていない**。
- `tests/test_g4c7_m37p2_paired_operator_native.py`：正常構造の仮手順、巨大データ・未許可operator・複製seed・ロール不足・Minecraft/action ART昇格を拒否。仮試験は**都市美術ではない**。
- `tests/test_g4c7_m37p2_ollama_paired_operator_proposal.py`：Ollamaの模擬tool応答をチェック。未完了、別tool名、toolなし、JSON形式を安全に区別する。
- `.github/workflows/g4c7-m37p2-paired-operator-native-blender-smoke.yml`：GitHub上の本物のbpy Blenderで、2ペア操作を**一つの別名保存BLEND**に入れられるか技術だけ調べる。ART評価ではなく、当該CIのSUCCESSを実確認するまでPASSと表現しない。

**何も「完全な未来都市」に昇格しない。** この操作方式はツールの研究であり、今後の本物の作者によるART品質を保証しない。第一ペアの屋根・室内の実寸関係も未証明。一次技術フィクスチャは保護v3本体や公開本番都市にはコピー禁止。

## 現状および必要な次の判定

1. **WindowsやOllamaでの新方式の実作者運用は未実施**。GUIライブ直接造形ではなく、将来のライブGUIへ拡張できるbpyネイティブoperator再生の範囲。GPT-6 Luna/Terraへの遠隔委任、ChatからユーザーPCへのアクセス、Work使用は行っていない。
2. CIが技術PASSなら、同じ元v3原本から分岐する**隔離試作**でモデルが編集命令を1回提案し、実BLEND・同一シーンの3真正レンダを取得し、絶対美術評価。不採用なら即停止。外観先行の大量プリミティブ生成・条件緩和は禁止。
3. 正式331人体／993足元、G0/S1/G1/G2/G3未実施、MakeCode未評価、Minecraft施工禁止、main変更禁止、PR #53 Draft維持、ユーザー正式ART採用0。

この経路が安全性または美術を満たせなければ、認定0のまま拒否し**真正直接GUI作者編集への復帰**を最優先する。
