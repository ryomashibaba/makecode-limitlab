# M37-P2：AI作者が「本物のBlender編集画面」を見るための最初のネイティブ経路

2026-11-03 JST。**G4-C7の正式美術作品ではない／ART HOLD／採用0。**

## なぜ必要なのか

前工程の技術試験は「保存済み2箱→Cycles撮影→不足の判定→面を修正→再撮影」を成立させたが、実作者が画面の立体・街並み・部屋を見て意図を判断し直接編集した訳ではない。実都市自体は未制作。特に、過去のP1/O1の板・箱・橋の形式を修正し続ける路線へ戻らない。

ここでは**Blender本体の実GUI**の2つの`VIEW_3D`領域とその瞬間の本物のシーンを扱う。その画像はCycles・別ファイルのレンダ・2Dの想像画像ではない。3Dオブジェクトの所属コレクション・本当の頂点数/面数/位置を画像と同じ時点で得る。

## 今回実際に追加した実装

- [実GUI撮影ツール](../../../../tools/g4c7_m37p2_live_gui_context_capture.py)：Blenderの`bpy.ops.screen.screenshot_area`を、`VIEW_3D`の領域コンテキストで使用。実2画面を`P2_ACTUAL_GUI_MACRO_EDITOR.png`と`P2_ACTUAL_GUI_LIVED_EDITOR.png`に保存し、同時に`P2_ACTUAL_GUI_CONTEXT_HOLD.json`を作成する。画像SHA/本物の画面位置・サイズ、5コレクションのメッシュ数/頂点数/面数、保存済みBLEND SHAを収める。
- 対象は正式P2の安全状態`P2_ART=HOLD`、`P2_OFFICIAL_ADOPTIONS=0`、`P2_MINECRAFT=FORBIDDEN`、`P2_FORMAL_331_993=NOT_RUN`のみ。GUI本体に新メッシュ・新カメラ・新レンダ・新Blender保存を行わない。画像は新しい別フォルダにだけ保存する。
- 本ツールの現段階では**Ollamaの画像AIを呼び出すことも、AIにBlenderの造形操作を送ることもできない**。直接作者の造形能力は**未成立**。ここが次の本当の技術課題である。
- [真正Blender GUI CI](../../../../.github/workflows/g4c7-m37p2-genuine-live-gui-context-capture.yml)：公式SHAを検証したBlender 4.5.15 GUIとXvfb上で、本物の2領域があるときのみ撮影し、画像実バイトSHA・元Blender SHA不変・ART HOLDを検査。Linuxの技術成功はWindows上の実現や作者造形の美術完成を意味しない。

## 初回CIの不具合と対応

[初回CI #41558995077](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41558995077) は失敗。理由は原本v3をGUIで開いた**だけ**では2画面分割が有効にならず、`TWO_REAL_VIEW_3D_GUI_AREAS_REQUIRED`を検出して安全停止したから。後続では、**SHA固定v3に内蔵され、過去の実GUIテストで成功した専用画面分割オペレーター**をCI内で実行してから撮影する。画面分割はGUI上だけで、`.blend`を保存し直したり都市メッシュを作ったりしない。

本工程は必要な入口の提供であり、進捗数を増やすための独立した箱・板・都市生成を行わない。Work不使用／Minecraft施工禁止／main保護／PR #53 Draft、正式安全331人体・993足元ほか全QA NOT RUN、MakeCode費用未評価、ART HOLD正式採用0を維持。
