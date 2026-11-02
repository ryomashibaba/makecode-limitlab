# G4-C7 M37-P2 — 実際のBlender GUI二画面作者編集の技術検証（2026-11-02 JST）

**判定：限定GUI METHOD TECH PASS／ART HOLD／正式美術採用0件。都市の新規3Dは未制作。**

## 何を本当に実行したか

1. [専用GitHub Actions #41431524480](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41431524480) の Ubuntu 24.04 Xvfb実ディスプレイで、公式 Blender **4.5.15 Linux GUI実行ファイル**をダウンロードし、公式公開SHA256表でバイナリ整合を検証して起動した。**Python `bpy`モジュールのヘッドレスだけの試験ではない**。`bpy.app.background=False` と実画面DISPLAY `:99` をログに記録した。
2. 固定SHA256 `536e451c763c4326421b13285abf1056a3a11d755028f8ff20b54b99b08a0249` の真正v3空Blender原本を読み込んだ。2つの実`VIEW_3D`編集エリアへ分割する **`g4c7.p2_parallel_split`** をGUIコンテキストから呼び、実際に **2つの3D編集エリア** が成立した。
3. `PUBLIC_EYE` 配置と、その後に`HABITAT_EYE`を選択して **`g4c7.p2_parallel_refresh`** が`FINISHED`となることを確認。どちらも同一Blenderシーンでの操作で、3Dカメラや既存メッシュの保存変更はしない。
4. 終了後、原本SHAは初回と一致。メッシュ0件、`P2_ART=HOLD`／正式採用0／正式331/993 NOT RUN／Minecraft FORBIDDENを維持。変更の保存は一切実行せず、GUI実行エビデンスJSONだけをCI artifactに保存（21日保存）。

CI JSONの内容：`outcome=PASS_ACTUAL_DISPLAY_SPLIT`, `headless=false`, `native_viewport_split=true`, `real_3d_view_area_count=2`, `public_eye=true`, `habitat_eye=true`, `geometry_art=NOT_CREATED`。

### 初回失敗と修正

- [初回 #41431366117](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41431366117) はBlender 4.5.15のCLIが`--noaudio`を認識しなかったため、原本を開く前にFAIL。
- 不正オプションを削除したcommit `6a634ebc2c02ac7404fb1619d69c3ce7ecac68e5`で再実行し、[成功 #41431524480](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41431524480) を確認。

### 未検証・誇張禁止

- **直接GUIで都市メッシュを制作する操作、実住宅の室内、工場見学／職員動線、文化研究活動、真正美術3視点審査は一切実施していない。** ウィンドウ分割・2視点切替の限定TECH PASSは美術的品質を保証しない。
- 完成済みの原本は「作者が直接3D造形を始めるための空の編集スタジオ」であり、都市作品ではない。
- M37-O1/P1は引き続きEARLY ART REJECT。旧形状の再利用・プログラム上の第三の`patch/wall/bridge`都市は禁止。
- **全体ART HOLD、正式採用0、正式331人体／993足元とG0/S1/G1/G2/G3 NOT RUN、MakeCodeコスト未評価、Minecraft施工禁止、main変更禁止、Draft PR #53維持、Work事前明示承認制**。

**次の唯一の制作工程は、新しい都市粗3Dと実生活断面を同じv3 Blender原本に直接作者造形し、保存3Dから3真正視点を絶対美術審査すること。** アシスタントが実行できない作者造形を、空スタジオの追加やコード自動形状生成で代用しない。
