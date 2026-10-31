# D3S26-M15 — 視覚的ネイティブ3D作者ワークフローへの切替（制作準備／接続未実施）
**2026-11-01 JST / Visual Authoring Toolchain: PREPARED ONLY / ART HOLD / adopted 0**

## 従来方式の停止
M11とM12はGitHub Actionsで真正Blender.blend/8視点制作成功、しかし低層の箱や孤立彫刻としてART REJECT。M13は市場→工房→研究→住居の36段の実階段と限定接続を含むものの低層箱としてART REJECT、CIは書式ミスと記録用変数衝突でFAIL（本物の.blendと画像は回収済み）。M14はVTK事前実画像で2本の巨大外殻とランプ勾配問題を発見、PRE-BLENDER ART REJECT。**次の巨大外殻・箱・棚の新候補をPythonで無限生成しない**。

## M15で実行した具体的作業
1. 公式READMEを再確認。MakeCode LimitLabの本目的はMinecraft Education MakeCodeによる巨大都市の安全/高速施工研究。別プロジェクトHALO-9に固有の10km規模・80/20美術憲章を引き継がない。過去研究記録にある10km表現をLimitLabの正式設計根拠と扱わない。
2. Chat側の利用可能ツールを検査したが**現在のチャットにローカルBlender画面操作コネクタはない**。既存GitHub ActionsはBlenderをバッチ実行できるが、制作中に3D GUIを観察・直接編集する能力は与えない。
3. 代替のネイティブ可視編集経路として第三者製 **MCP for Blender** (https://github.com/ahujasid/mcp-for-blender) とCodexのローカルMCP接続を調査。addonからviewport/camera画像、scene情報、直接Blender操作が可能と文書に記載あり。**実Windows接続PASSは未実施**。依存するのはユーザーが明示的に選択して導入したローカル環境のみで、Work、リモート通信やpublic portは不要。インストーラーはChat側で勝手に起動していない。
4. Chat会話には `D3S26_M15_NATIVE_VISUAL_AUTHORING_HANDOFF.zip` を作成（**292,236 bytes、SHA256 `0b926a5cc506dbba0ecbca1aed482d5d73c96da850d704d61f830c70352b31b1`**、ZIP CRC PASS）。内容6件：M13真正編集可能.blend参照、M13実8視点JPEG、M15のGUI直接制作プロンプト、Windows setup手順、検査専用Python、保護契約JSON。M13参照.blendは **SHA256 `0950a2bb166e5db302ca100638e3aab7764ca702babd842aae193e2417d6b319`** 完全一致。ローカル診断コードをChatコンテナで実行、SHA一致、読み取り専用動作PASS。
5. インストール時は原則PowerShell `winget install --id=astral-sh.uv -e`（uvがないときだけ）、`uvx mcp-for-blender install-addon`、未登録のCodexに限り `codex mcp add blender --env DISABLE_TELEMETRY=true -- uvx mcp-for-blender`。これは案内であり**ユーザーPCで実行した事実ではない**。MCPはlocalhostのみを許可し、テレメトリー・外部3D/asset自動取得を禁止。第三者製addonがPythonを実行できるため、未信頼.blendを扱わず、データ送信/個人ログの公開禁止。
6. 制作プロンプトは、原本はART REJECTの参照に限定し、**新しい**空シーンから公共街路→製造→採光アトリウム→研究→住居アプローチを、スクリーンショットで観察しながらネイティブ3Dで少なくとも2回直接編集。8視点と初期/修正1/修正2を保存する。別の形状コード生成を唯一の作者方法にしない。

## 次に実行すべきこと
- ユーザーが必要と判断した場合のみ、ローカルBlender 5.2.1 LTSとCodexをMCPで接続して**実際のviewport screenshotとオブジェクト一覧を取得できること**を最初のGateにする。スクショなしに造形を開始しない。
- 同じシーンを2回以上視覚観察→直接変更→再観察して前後比較し、一つの生活体験から非反復的な建築と都市形態が生じるか評価する。M13に対する見た目の修正を新採用としない。
- その場で実Blenderの編集済み.blend/8視点/ハッシュ付きmanifestを保存し、Chatで独立監査。真の歩行/人体の331/993とG0/S1/G1/G2/G3は正式ゲート前にPASSとは呼ばない。
- Chat側からPCのBlenderを直接操作できた、またはM15の3D美術が改善した、とは現段階で主張しない。

**保護：** main変更なし、既存PR #53 Draft/Open保持、ART HOLD、正式採用0。Minecraft Education施工・都市統合禁止。本施工はMakeCodeのみ。今回のGitHub追加はテキスト資料で、M13.blendをGitHubに再アップロードしたとは主張しない。
