# M37-P2：Blenderネイティブ編集の実3視点とWindows統合入口（2026-11-03 JST）

**TECH ONLY／ART HOLD／正式採用0件。新都市・住宅のART作品はまだ完成していない。**

## 今回の直接実装

前工程で`Blender Edit Mode`の`begin_surface`、`extrude_face`、`inset_face`、`translate_selection`を保護v3の別名ファイルへ書き込む技術CI #41467002875 が**SUCCESS**。Pythonの厳格操作ゲート7件、Ollama Tool Calling模擬応答5件、実bpy 4.5.15で1つの保存済み`.blend`に都市外形・住居2メッシュ（それぞれ面数2超）を作成し、再読み込みしたことを確認した。**これは一時テスト形状。正規の都市美術ではない。**

- [真正3 Cycles視点の証拠出力実装](../../../../tools/g4c7_m37p2_paired_operator_three_view_evidence.py)。直前の**実際に保存された同じ`.blend`を再読み込み**し、実メッシュ2領域・ART HOLD・作者カメラ未承認を検査したあと、都市遠景・公共側・住居側の3カメラ位置をメモリ上だけで仮配置して真正Cycles PNGを保存。保存原本SHA不変。各PNGのSHA・面数・非美術宣言をJSONに残し、ローカル`OPEN_REAL_THREE_VIEW_NON_ART.html`で3枚を並べて表示する。画像の生成・加工による見せかけではない。
- [3視点を実際にレンダ・保存するCI](../../../../.github/workflows/g4c7-m37p2-paired-operator-native-blender-smoke.yml)。本物のCycles3 PNG・JSON・HTMLをGitHub Actionsのartifactとして保存し、SHA・各視点の独立画像・同一BLENDのSHA一致を検証。最新ワークフローのCIが**完了SUCCESSになるまでは今回の3視点についてPASSと呼ばない**。前回のCI PASSとは明確に区別する。
- [Windows PowerShell 1回実行](../../../../tools/g4c7_m37p2_run_native_operator_first_pair.ps1)と[単独CMDの起動ファイル](../../../../tools/G4C7_P2_Native_Operator_Trial_Start.cmd)を新設。ユーザーはBlender 5.2.1 LTSでv3原本を開くことに成功済み。ローカルOllamaのQwen3:14bは旧試験で実応答あり。新統合では元のv3コピーがSHA一致することを最初に検査し、固定GitHubコミットの3つの監査済みPythonを固有の`LOCAL_AI_NATIVE_PAIRED_OPERATOR_*`フォルダに取得、**Ollama Tool Callは1回のみ**、動作可能な許可済み操作だけを隔離Blenderプロセスへ渡し、真正別名`.blend`と3視点Cyclesを生成し、HTMLとフォルダを自動表示。失敗時にHOLD、モデルコード・Minecraft書込を実行せず、既存GUIや原本は上書きしない。
- [専用Windows PrepareOnly検証CI](../../../../.github/workflows/g4c7-m37p2-paired-operator-windows-local-preflight.yml)。WindowsのPowerShellパーサー、固定PS1/CMD連結、原本SHA、3つのPythonダウンロードと構文、Ollama未実行・Blender未起動を検査する。**これがSUCCESSになるまでは利用者へ実行を勧めない。** 公開GitHubのコードを単独で固定コミットから取得する方式でZIPや手動フォルダ作成不要。

## 状態を混同しない

- **確認済み**：ネイティブEdit Modeの保存／再読込、5+7のモデル模擬・構文/操作安全テスト。旧全市一括頂点試作がART REJECT、旧ランチャーはRETIRED、main変更なし。
- **未確認**：新CIの3視点CyclesまでのSUCCESS、新Windows準備CIのSUCCESS、実ローカルQwen3:14bによる新ツール呼出しとBlender5.2.1との統合、技術試験形状の美術価値、生活室・工場・研究文化の実体、**作品としての3真正ART審査**。2つの操作試験形状はART採用0。
- **固定制限**：全体ART HOLD、正式331人体/993足元＆G0/S1/G1/G2/G3 NOT RUN、MakeCode費用未評価、Minecraft施工禁止、Work不使用／事前承認、main保護、Draft PR #53未merge。技術画像でART早期審査を代替しない。

**次の判断**：まず2本のCIを完了まで確認し、失敗したら修正する。成功した場合のみ、ユーザーの手操作1回（起動ファイルのダブルクリック）で**1回の本物のOllamaツール呼出し**を試す。失敗なら原因がわかるレポートを残して停止。見栄えが低品質ならEARLY ART REJECTしてプリミティブの量産をしない。
