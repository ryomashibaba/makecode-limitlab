# M37-P2｜Windowsから本物のBlender作者編集を開始する（Work不使用）

**位置付け：Windowsローカル作者操作の入口。都市美術ではない。ART HOLD／正式採用0。**

GitHubには真正Blender 4.5.15ベースの **v3空編集原本** があるが、チャット内でWindowsのBlenderを代わりに動かすことはできない。6 Luna／6.1 Terraを使用できる環境なら、そのエージェントに**画面上で作者編集を行わせることは別途可能性がある**ものの、このランチャーがAIによる直接造形を実行するわけではない。

## 準備と最短操作（ZIP不要、元原本上書きなし）

1. [`g4c7_m37p2_launch_local_author.ps1`](g4c7_m37p2_launch_local_author.ps1) をGitHubの「Raw」から単独ファイルとしてダウンロードする。GitHub研究ブランチの該当ファイルであり、古い版への変更・mainへの切替はしない。
2. Windows PowerShellで、保存したファイルがあるフォルダーを開いて次の1行を実行：

   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File .\g4c7_m37p2_launch_local_author.ps1
   ```

3. ローカルに正しいSHAのv3原本があればコピーし、なければ固定コミット `3c05ba86814443bb3b6d44718dae50a855fea083` から取得する。**SHA256 `536e451c763c4326421b13285abf1056a3a11d755028f8ff20b54b99b08a0249` と一致しなければ起動を中止**する。Blenderが見つからなければエラーで停止。
4. `ドキュメント\G4C7\P2_Author_Sessions\P2_DIRECT_ART_...` 内に一意のセッションを新規作成する。原本は決して上書きせず、`P2_DIRECT_AUTHOR_UNAPPROVED.blend` という**編集用コピー**をBlenderで開き、そのセッションフォルダもエクスプローラーで表示する。
5. 既存v3原本に埋め込まれた「都市全景と人間目線の並行編集」「作者レビュー提出」「3真正視点のレンダリング」GUIパネルを起動スクリプトで登録する。**新しい3D形状は1つも自動生成しない**。

## モデリング実作業の固定条件

作者はBlender GUIで、街区全景と同一街区の宇宙機製造・公衆見学隔壁・研究文化・本当の住居内観を**同時に**制作する。旧P1/O1の`patch/wall/bridge`自動生成と不採用形態の転用は禁止。制作前に完成を主張せず、五つのコレクションへ実メッシュを直接作成。3カメラを実際に確認・移動して初回ART提出段階へ進めたら、別名保存・再読込し、P2 Early Art Reviewから**同じ真正BLENDの3視点**を撮影する。技術上のPNG生成成功をART PASSと扱わない。

## 確認済みと未確認の区別

- [Windowsランチャー基礎検証CI #41447267350](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41447267350) は SUCCESS：Windows PowerShell構文、原本コピーSHA一致、一時作業フォルダ、JSON固定属性、起動用Python構文を確認。**PrepareOnlyモードで実行したためWindowsのBlender GUI自体は起動していない。**
- [Blender 4.5.15実GUI二画面CI #41431524480](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41431524480) と [真正3視点の技術CI #41428422529](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41428422529) は先行して成功。ただしWindowsのBlender 5.2.xでの実操作・本物の美術完成はまだ未検証。
- [Windowsダウンロード専用経路CI #41447810957 SUCCESS](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41447810957)：GitHubのローカルクローンが**一切ない別フォルダ**へスクリプト1本だけを置き、raw.githubusercontent.comからSHA固定の真正v3原本をダウンロード、保存コピーのSHA・セッションを検証した。ZIPやGitクローン不要。ただし実際のユーザーPC固有のネットワーク制限・WindowsのBlender起動可否までは保証しない。
- Run後の実セッション、見栄え、居住・製造機能、331人体・993足元とG0/S1/G1/G2/G3は未実施。MakeCode費用未測定。Minecraft施工禁止、PR #53 Draft、main変更禁止、Work事前許可を維持。

**ランチャーで準備できても、本当の次工程は本人または許可済みのローカル作家エージェントがGUIで造形した保存BLENDを提示すること。** 空の編集機能を作品完成と混同しない。
