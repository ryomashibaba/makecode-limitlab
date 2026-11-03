# M37-P2｜真正X11画面の実見でBlender Quick Setup障害を確認 — 最小修正

2026-11-03 JST。**CI実画面の独立監査／都市の美術制作ではない／ART HOLD・正式採用0件。**

## 1. 確認した一次証拠

- [完了済みCI #41566892238](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41566892238)：`completed/failure`。実行ジョブは`capture-two-real-native-viewports`。
- [Actions artifact 13202040183](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41566892238/artifacts/13202040183)を実際にダウンロードし、`P2_X11_ROOT_DIAGNOSTIC_ONLY.png`の実画像を直接確認した。これは1600×900のX11ルート画面で、Blender 4.5.15 LTS GUIに**左右2つのVIEW_3Dが実際に描画されている**。中央には**「Quick Setup」初回設定ダイアログとContinueボタン**が残っており、左右画面の一部を覆っていた。撮影物は空の作者スタジオで都市美術ではない。
- 同一artifactの`P2_INDEPENDENT_PIXEL_DIAGNOSTIC.json`の実数：`MACRO_EDITOR` は **1×1ピクセル／全黒／可視割合0**、`LIVED_EDITOR` はPNGなし、X11 rootは**1600×900／非黒可視割合0.971222／色数46,861**。
- Actionsログ：`FAIL_GENUINE_GUI_SCREENSHOT ValueError('REAL_VIEW_SCREENSHOT_FILE_SIZE_INVALID_MACRO_EDITOR')`、独立X11 rootは`CAPTURED_NEEDS_INDEPENDENT_PIXEL_INSPECTION`。Blender公式バイナリ取得とSHA検証はPASS、`P2_CI_ONLY_NATIVE_GUI_SPLIT_REQUESTED`もログ確認。
- **現時点で特定できたのは「初回設定モーダルが被さった状態で撮影が失敗した」ことであり、screenshot_areaの1×1失敗がQuick Setupだけで完全に説明できるかはまだ未証明。** 以前の「Xvfbは全黒かもしれない」は今回の真正X11画面については否定できる。

## 2. 最小修正と検証方針

- 正規GUI CIのみに一時的な`XDG_CONFIG_HOME=/tmp/g4c7-p2-isolated-xdg-config`を設定する。ユーザーのWindows/Blender設定や原本には一切触れない。
- 正式SHAを照合した同じBlender4.5.15を**背景実行**し、`bpy.ops.wm.save_userpref()`で隔離設定を保存。`userpref.blend`が実在し`BLENDER`マジックを持つことを確認した後、同じ隔離設定で真正GUIを起動する。
- Blender公式マニュアルによれば初回起動ではQuick Setupが表示され、ユーザー設定はBlender4.5のconfig内`userpref.blend`に保存される。今回はこの設定だけを先に準備し、modal回避が本当に実現するかをCIとartifactで実測する。**準備成功だけで画像成功としない**。
- 最後の視覚成功要件は、左右2つの真正Blender`VIEW_3D`画像が十分なサイズで独立に非黒ピクセルを含むこと。X11 root・X11 window・領域クロップは診断専用で代替ART証拠にしない。CI成功後も画像3ビューの実確認を要求する。

## 3. 開発・美術の固定状態

真正新都市メッシュ0、都市全景/公共/住居の新正式ART画像0、ART HOLD、正式採用0。R0〜R5、331人体993足元とG0/S1/G1/G2/G3 NOT RUN、MakeCode未評価、Minecraft施工禁止、PR #53 Draft、main保護、旧不採用形状再利用禁止、Work事前明示承認を堅持。X11障害だけを調査する空CIの量産には戻らない。
