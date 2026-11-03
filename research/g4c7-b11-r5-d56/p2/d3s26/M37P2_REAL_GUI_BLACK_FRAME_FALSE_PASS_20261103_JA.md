# M37-P2｜実Blender GUI PNGの黒画面偽陽性：実画素まで確認して修正

2026-11-03 JST。**本事象はBlender GUI技術検証の問題であって、美術作品の作成ではない。ART HOLD・採用0。**

## 実測した反証

- [CI #41559389596](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41559389596) は`completed/success`。SHA固定のBlender 4.5.15をXvfb上で真正GUI起動、公式v3に組み込まれた2画面分割を適用し、`screenshot_area`から2 PNGが保存された、という**ファイル・形状整合の技術結果**に過ぎない。
- [同CI artifact](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41559389596#artifacts) ID `13196718022` を**実際にダウンロードし、双方のPNGの全画素をPillowで検査・直接画像を開いて目視**した。
- `P2_ACTUAL_GUI_MACRO_EDITOR.png`：**657×783=514,431画素**、RGB色は**(0,0,0)のみ**、非黒画素0、平均輝度0。
- `P2_ACTUAL_GUI_LIVED_EDITOR.png`：**661×783=517,563画素**、RGB色は**(0,0,0)のみ**、非黒画素0、平均輝度0。
- 2枚の画像はPNG構文・SHA・3D表示領域の存在テストを通っていたが、**視覚的な3D情報は0**。従って**「Blender実編集画面を視覚AIへ渡せる」はまだ未実証**。以前の技術PASS表記は限定し直す必要がある。
- 真っ黒になった根本原因は現段階で**未確定**。実GPU画面描画前のcaptureやXvfbのフレームバッファなどが候補だが、いずれも証明されていない。根拠なく断定しない。

## 今回実施したコード修正

- `tools/g4c7_m37p2_live_gui_context_capture.py`：`bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=4)`を撮影前に実行する候補対策を追加。**Blenderが再読込した各PNGの実RGB成分をサンプリング**し、十分な明るさの画素がなければ`REAL_GUI_SCREENSHOT_BLACK_OR_UNDRAWN_REJECT`で停止する。技術CIのPNGマジック/SHA確認とは独立に画素品質を確認する。
- 同スクリプトの正しい出力だけに`content_not_blank_black=true`と`visible_bright_pixel_ratio`を持たせる。
- `tools/g4c7_m37p2_local_gui_vision_review.py`は、後段のローカルGemma画像認識でこの画素検査が成立していない写真を`GUI_BLACK_SCREENSHOT_REJECT_UNREADABLE`として拒否する。メッシュ0ではモデル呼出ししない。
- `tests/test_g4c7_m37p2_local_gui_vision_review.py`に、「正しいPNGヘッダとSHAでも黒画像」ゲートを通さない回帰を追加。
- [GUI CI](../../../../.github/workflows/g4c7-m37p2-genuine-live-gui-context-capture.yml)も実画素の可視性割合 >=0.035 がなければFAILとする。CIのSUCCESS≠実際の画像有用性、という失敗を繰り返さない。

**新しい再撮影CIが成功し、本人が画像の実内容を直接確認するまではGUI視覚入力経路はART/HOLDのみ。** 修正前の2枚の黒PNGは今後の美術・AI判断のソースとして使わない。

## 変わらない基準

都市全体と生活断面、造船設備、厚い公共・職員境界、研究文化を同一Blender原本へ作者が実造形する。本工程は新都市や新しい仮モデリングを生成していない。今あるのは空スタジオと旧不採用2箱試験だけ。Work未使用、main変更禁止、PR #53 Draft、Minecraft施工禁止、正式331人体/993足元・G0/S1/G1/G2/G3未実施、正式ART採用0。
