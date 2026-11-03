# G4-C7 / M37-P2：X11経由の実Blender GUI編集・ネイティブ保存・独立再読込の実証（2026-11-03）

**判定：GUI_INPUT_NATIVE_SAVE_INDEPENDENT_RELOAD = LIMITED TECH PASS。AI自律作者・新都市造形・正式ARTは未達。全体ART HOLD、正式採用0。**

## 真正CI・バイナリ証拠
- [GitHub Actions #41599291594](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41599291594) は `6cfa0152345dc670651faeb9cdf3343832102e6e` から起動、**completed/success**。ジョブの「Real GUI keyboard edit to distinct saved Blender copy, independent true Blender reload (TECH only)」が実際に成功した。
- Artifact ID **13213069325**（[ActionsのArtifacts](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41599291594)）に、真正Blender保存原本 `M37P2_X11_GUI_SHORTCUT_TECH_NOT_ART.blend`（139,802 bytes）、操作前後の実X11 PNG 2枚、独立再読込JSON、GUIログがある。GitHub Actions Artifactの保持は14日であり、**バイナリは研究ブランチに恒久保存したとは主張しない**。
- 新保存 `.blend` のSHA-256（GitHub Artifact取得後に隔離コンテナで独立再計算）：`3279d909da13e5b09660dc170e8bb79b51a733611e4d1d1c02ea97f4f920ded8`。CIの独立JSONに記録されたSHAと完全一致。保護元v3 SHA：`536e451c763c4326421b13285abf1056a3a11d755028f8ff20b54b99b08a0249`。
- 取得したGUI画像はそれぞれ**1600×900**。BEFORE PNG SHA-256：`8981ce4bcb24eedee46c710f8d9e7d71730514417c5d9d656f3d09e51851cba3`。AFTER PNG SHA-256：`f1b9d8edcf5fbc385f0cc9bf220fd999ba5be7c6308b307bc81397c3916ef71d`。画像は異なる実ピクセルを持つ。

## 観測された実GUI操作
- 新しいXvfb上でBlender **4.5.15** のネイティブGUIを起動し、`xdotool`で実ウィンドウにフォーカス・カーソル操作・キーボード操作を入力した。検索メニュー（F3）から **Add Monkey** を実行し、`G X 8 Enter` / `S 2 Enter` による移動・拡大を実施した。**メッシュ生成・変換をbpyで直接実行したのではない**。
- 操作後のX11スクリーンショットを直接目視すると、オレンジ色の選択外形を持つSuzanneメッシュと、BlenderのTransform欄 `Location X=8.00000`、`Scale X/Y/Z=2.000` が表示される。
- 実GUIのPython Consoleへ切替えた後、**メッシュの状態をassertで検証し、`bpy.ops.wm.save_as_mainfile()`で別名保存**した。保存自体はGUIのファイルメニューをマウスで操作したものではなく、GUI内Python Consoleからの保存である点を区別する。
- さらに**別のBlenderプロセス**が保存原本を再読込。`INDEPENDENT_REAL_BLENDER_REOPEN_TECH_ONLY.json` で `Suzanne`、**507頂点**、Location `[8.0, 0.0, 0.0]`、Scale `[2.0, 2.0, 2.0]`、元v3 SHAとART HOLDを確認。保存済みファイルを単に存在検査しただけではない。

## 成立した能力・未成立の能力
- **成立：** X11実画面取得・実GUIのキーボードとマウス入力・新メッシュのGUI追加と変換・GUI内Consoleを用いた別名ネイティブ保存・独立プロセスでの復元・原本不変性。
- **未成立：** 画面内容をAIが解釈しながら次の編集命令を決める視覚フィードバック閉ループ。高品質なR1作者モデル。都市遠景・街区・住居・工場・研究文化を同一3Dで美術的に成立させた作品。模型のSuzanneをCITY ART候補と扱うのは禁止。
- 今後は**AIの実画像批評 → 保存された同一ネイティブ3Dへの意図的GUI編集 → 新画像 → 早期ART絶対評価**の一貫した制作経路に集中。以前不採用になった `tower()` やパラメータ型のbox/slab/壁を量産して埋め合わせしない。R1は相互に質的に異なる最大2方向。新R1作品の正式ART採用には本人承認が必要。
- 研究ブランチ、Draft PR #53、main・保護v3不変更。Work、Solや追加有料課金は本人事前許可なしに使用しない。全体ART HOLD、正式採用0、331人体993足元/G0/S1/G1/G2/G3 NOT RUN、MakeCode NOT EVALUATED、Minecraft施工 FORBIDDEN を維持。
