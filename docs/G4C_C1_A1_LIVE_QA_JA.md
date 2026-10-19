# MakeCode LimitLab — G4-C C1 A1（2×2地区の実機施工候補）

## 経緯・証拠の区別
- 前提：G4-C C0 `dev/g4c-c0-pedestrian-grade` / Draft PR #22 / `a0b36cf...`。Minecraft Education実機サンプルCSVは386 Fill、5 Clone、118 checks、8棟、`FAST_COMPLETED_SAMPLED_NOT_EXACT`でPASS。目視で横断歩道の凸状段差が改善。
- A0：Draft PR #23 `dev/g4c-c1-district-tiling-a0` の非施工検証。ピッチ180と共有12幅道路、2×2地区の正当性を12件CIで検証。
- **A1のこのブランチは実機Minecraft未実行。CIと現実の動作は区別する。** Private CSV・スクリーンショット・USEDラッチはコミットしない。

## 本工程の実装
- **372×372×高さ84**、2×2地区、36区画＝32棟＋4公共広場。セル間隔60、区画幅48、道路幅12、地区間ピッチ180。
- 元の完成済みC0 192×192から、先頭180×180の構造を **180×180×6＝194,400 ブロック**に分割し、3地区に42 Clone。右端・下端の12幅道路と角をさらに5 Clone。元の建物Clone 5回を含み、**計52 Clone**。
- 建物の3ファミリー、現行の白・シアン・灰色配色、街路樹16本×4地区、路面・横断帯Y+1、C0の原型品質を維持。**景観完成版ではない**（同じ地区の技術的複製）。後工程で地区ごとに建物高さ、景観、施設構成を変える。
- 元地区は既存の386 Fillを再利用。拡張後は **386 Fill＋52 Clone** 計画。
- P1.6/P2.0の実機成功範囲を守り、Fill上限32768、Clone上限262144。全てのタイル・外縁道路のCloneは上限内、境界内、元ソースと宛先が不交差、互いの宛先も不交差。
- **事前300点AIR検査**（4地区×75点、Y+0/36/80）を、最初のCSV書き込み・一回限りラッチ消費・施工より前に実施。ただしこの試験は疎サンプルであり、対象全域のAIRを保証しない。
- 施工段階：PLAN → PREFLIGHT → ROADS → PROTOTYPES → CLONE → PLAZA → DETAIL → SAMPLE（元地区28点）→ TILE（新47 Clone）→ DISTRICT_SAMPLE（新地区・外縁道路18点）。
- 検査予定合計 **361点＝事前300＋建物Clone15＋元地区28＋拡張後18**。結果 `FAST_COMPLETED_SAMPLED_NOT_EXACT` は全域一致ではない。
- 新しく独立した `G4C1_ONCE.txt` と `USER_UPLOAD_THIS_G4C1_STATUS.csv` を使用。既存C0/G4Bの成果には書き込まない。
- 実行時、47タイルCloneの7/14/21/.../47回で進捗ログを保存し、失敗時に自動再施工・世界の自動復旧を行わない。大領域のCloneが実機で遅い・失敗する可能性は未知。

## 実機試験はCIが全PASSした後のみ

1. OMEN上の既存Gitリポジトリから新A1専用のworktree（ローカルの変更を保持）を取得する。手順はChat側で最終合格SHAを指定する。
2. **新規の破棄可能な専用Minecraft Educationワールド**だけで使う。重要ワールドや既存建築のある地点に施工しない。
3. `RUN_G4C1_A1.cmd` を1回起動して `COPY OK` を確認。独自ランダムRunディレクトリとSHA固定の完全ソースが自動生成・コピーされる。
4. MakeCodeのJavaScriptにCtrl+A→Ctrl+V、File Read & Write拡張を保持、**エディタエラー0件**を確認。
5. `labareag4c1` で372角の予定範囲を目視、問題なければ `labcityg4c1` を一度だけ実行。進捗は `labstatusg4c1`、協調停止は `labstopg4c1`。**重いCloneがネイティブ処理中の場合は即停止できない可能性がある**。
6. 終了時の非公開ZIPは `Downloads/MakeCode_LimitLab/G4C1_A1/runs/<新ID>/private_results/USER_UPLOAD_THIS_G4C1_....zip`。観測用Pythonは古い結果・使用済みラッチを書き換えない。ZIPと斜め俯瞰・道路連結・公共広場スクリーンショットをChatに添付。**公開GitHubへCSVや個人情報は出さない**。

## 品質ゲートとC1 A2
- Linux/Windows CI、MakeCodeスタブコンパイル、372平方のボクセル模擬実装、座標安全性、300点preflight、失敗時停止、CSV真正性、SHAピンと排他的Runフォルダが**すべて合格**することが実機QAに進む前提。
- 実機完了後は実際の所要時間をユーザーから取得し、C0と比較する。CSVのサンプル合格は全ブロック完全一致を証明しない。
- C1 A2では**巨大都市らしい非反復の地区デザイン**（建築用途・高さ構成・公共施設・内部動線）と性能効率を優先する。52 Clone の反復都市で最終完成にしない。

**固定方針：OMEN Windows一台、Chat主体、Work原則不使用。結果CSV/旧ラッチ保存、ユーザー操作最小化、品質と開発速度両立。**
