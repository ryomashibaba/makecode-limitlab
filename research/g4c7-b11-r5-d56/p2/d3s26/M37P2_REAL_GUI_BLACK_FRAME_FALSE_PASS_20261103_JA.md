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

---

## 2026-11-03 JST：独立X11フレームバッファ診断を追加

- 旧CI #41559389596 のPNGを改めて現物確認し、`MACRO_EDITOR` 657×783、`LIVED_EDITOR` 661×783 は両方とも全画素RGB=(0,0,0)だった。PNGとSHAが正常でも視覚的な有用性は**0**。
- `tools/g4c7_m37p2_live_gui_context_capture.py`の**CI専用**実GUIタイマーで、`bpy.ops.wm.redraw_timer`によるBlender内部の再描画・実PNGの明るさ検査に加え、XvfbのX11 root framebufferをImageMagick `import -window root`で**別経路**から撮影する診断処理を追加。X11側の画像は **`P2_X11_ROOT_DIAGNOSTIC_ONLY.png`**。これは表示障害の切り分け専用で、Blenderの各VIEW_3D画像への置換やART証拠としての採用は**絶対にしない**。
- [.github/workflows/g4c7-m37p2-genuine-live-gui-context-capture.yml](../../../../.github/workflows/g4c7-m37p2-genuine-live-gui-context-capture.yml) にImageMagick/Pillowを導入。実GUI試験がFAILでも`if: always()`で双方のネイティブGUI PNGとX11 root画像の**非黒画素率・全黒フラグ・サイズ・色数**を独立取得する。証拠は`P2_INDEPENDENT_PIXEL_DIAGNOSTIC.json`へ保存し、Actions artifactへ同梱。GUI実キャプチャ自体は画素条件を満たさなければFAILのまま。
- 新CI **#41562899937** はこの文章の時点でqueued。原因判定は**未確定**であり「再描画が直った」「X11側が直った」「AIがBlender画面を認識できる」いずれも未確認。成功した場合もartifactの画像自体を見てから認定する。
- GUIは空のv3のまま。ローカルGemmaは呼ばない。作品の直接造形・密度・生活断面・製造と公開境界・研究文化については**未制作**。ART HOLD／正式採用0／正式安全QA NOT RUN、Minecraft施工禁止、main変更なし、Work不使用を維持。

---

## 2026-11-03：ローカル画像AI入力側でPNG自体を独立デコードして検査

- 前工程の画素可視率`content_not_blank_black`と`visible_bright_pixel_ratio`は、Blenderが書き込んだ**レポートの数値**であり、画像ファイル本体の独立検証ではなかった。これをAIの唯一の入力ゲートとして信頼すると、古い誤ったレポートや改ざんされたメタデータで**黒いPNGをモデルへ渡す可能性**が残る。
- [ローカルモデル入力ゲート](../../../../tools/g4c7_m37p2_local_gui_vision_review.py)に`independently_verify_png_pixels`を実装。**Python標準ライブラリのみ**でPNGのチャンクCRC、IHDRの実寸、8bitグレースケール/RGB/RGBAの非インターレース画像を読み、PNGフィルタ0〜4を逆変換して全画素の可視輝度を再計算する。明るい画素が3.5%未満なら`REAL_GUI_PNG_ACTUAL_PIXELS_BLACK_OR_UNDRAWN`でAI画像入力前に拒否。CRC不正／実PNG寸法不一致／壊れた圧縮列／未知の形式も安全拒否。標準ライブラリ以外のPython環境インストールは不要。対応しないPNG形式は**正常扱いせずHOLD**。
- [回帰テスト](../../../../tests/test_g4c7_m37p2_local_gui_vision_review.py)を**11件**に拡張。署名だけの偽PNGではなく、テスト内で本物の8bit PNGとCRCを標準ライブラリで組み立てる。特に、黒PNGのSHAまで一致させ、レポートでは`content_not_blank_black=true`／明るさ60%と偽ったケースを拒否する。PNG CRC破損も別途拒否。正常PNGの実輝度を認識するケースも検査。
- [GUI CI](../../../../.github/workflows/g4c7-m37p2-genuine-live-gui-context-capture.yml)は、11件のPNG安全テストを**GUI/Blenderダウンロード前**に実行する順序へ変更した。コードの実装・GitHub保存は完了。ただし**最新版のCI成功は未確認**であり、表示内容のあるBlender GUI取得成功と混同しない。
- さらにX11 rootとBlender native 2VIEW_3D双方のPNG画像を独立診断する経路は維持。**X11 root画像は証拠の切り分けのみで、本物の編集領域キャプチャ・都市ARTの代わりではない。**
- 本工程はユーザーのPCやOllamaへアクセスしておらず、Blenderで街を作成していない。ART HOLD／正式採用0／331人体993足元とG0/S1/G1/G2/G3 NOT RUN、Minecraft施工禁止、main保護、Draft PR #53未merge、Work不使用を維持。
