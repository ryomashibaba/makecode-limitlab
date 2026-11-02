# M37-P2 ローカルLLMの直接頂点造形データを真正Blenderで検証する非採用METHOD試験

**2026-11-02 JST｜研究ツール実装。真正AI都市ART作品は未生成／ART HOLD／正式採用0。**

## 目的と旧失敗との差

- 前回までにWindows Blender 5.2.1実GUI、v3空原本、左右2つの3D編集画面の表示が**ユーザー本人のスクリーンショットで確認済み**。ただしChatからこのGUIへクリックや3D編集操作は送れない。Workは使用量枯渇のため使用しない。
- 従来のP1/O1の `patch/wall/bridge` や箱・板・巨大壁を固定関数で繰り返す方式で**第三の自動プリミティブ都市を作らない**。
- 新しい実験経路では、ユーザーのローカルOllamaで動くQwen3:14b等が、各メッシュの**明示的な頂点座標・面インデックス・用途・作者意図のJSON**を直接提案する。**モデルが生成したPythonコードは一切実行しない**。専用バリデータが五つの制作領域・各面の有効面積・複雑なメッシュ・シーン3軸の厚み・キューブ多数の拒否条件を検証する。違反があれば実3Dファイルを作成せず保留する。
- JSONが機械検査を通った場合のみ、**GitHubと元のBlender GUIを変更せず**、SHA固定のv3空原本からローカルAIにより提案された別名保存の真正`.blend`と、同じBlenderネイティブシーンの真正3視点Cycles PNGを生成する。結果は**独立の未承認試作**、美術PASSではない。AIが実際にGUIで手造形した／人が操作したとは呼ばない。旧正本のGUI直接編集作品と同等にも認定しない。

## GitHubで実際に追加したコード

- [モデルから安全な頂点面データを受け取り、Blenderで実3Dにする標準Python／bpy実装](../../../../tools/g4c7_m37p2_local_vertex_author.py)
- [PowerShellからOllama・Blenderを最小操作で開始する起動器](../../../../tools/g4c7_m37p2_run_local_ai_vertex_trial.ps1)
- [固定の検証用非都市サンプルだけを使用した真正Blenderの3視点CI](../../../../.github/workflows/g4c7-m37p2-local-llm-explicit-vertex-first-art-tech-smoke.yml)
- [WindowsのPrepareOnly安全検証CI](../../../../.github/workflows/g4c7-m37p2-windows-local-vertex-ai-first-art-prepare.yml)
- 作業機での操作をさらに削減するため、チャット成果物として単一クリック式CMDランチャーも生成したが、実行可能性の確認はCIとユーザーのPC固有環境に依存する。

**厳密な未検証事項：** Pythonの静的実行／GitHub Actionsの本テストが成功するまでは「Windows統合完成」と呼ばない。Qwen3:14bが実際に五領域の信頼できる本物メッシュを出せるか、現実的な都市生活密度を作れるか、ユーザーのWindows Blender 5.2.1でCyclesが動くか、モデルを自動起動できるかは**未検証**。モデルの出力が物理空間を満たすことや美しいこともバリデータで保証しない。画面を見た絶対評価が必須。

**次の真の美術目標は変わらない。** 一体都市の全景と、製造／見学／研究文化／住居の本当の生活断面を含む、作者が編集した3D原本。自動モデル結果が不合格なら即REJECTし、単に板を増やして修復しない。

## 保存済み禁止事項

ART HOLD／正式ユーザー採用0件／331人体・993足元とG0/S1/G1/G2/G3未実施／MakeCode費用未評価／Minecraft world write 0／main不変更／PR #53 Draft未merge／Work事前明示承認制。ローカルAIが作る全提案は`LOCAL_LLM_EXPLICIT_VERTICES_NOT_GUI_DIRECT_AUTHOR`と記録し、`P2_CAMERA_VIEWS_AUTHOR_APPROVED=false`、作者直接GUI造形の偽装を禁止する。
