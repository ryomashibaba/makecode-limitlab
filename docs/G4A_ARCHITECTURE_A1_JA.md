# MakeCode LimitLab — G4-A 建築ファミリー多様化（A1）

**基準：P2.4S R2はMinecraft Education実機で157 Fill＋5 Clone・サンプル108点PASS。** ユーザーの完成画像を受け、建物の骨組み感、8棟の類似、金・灰色のみの配色、都市スケール不足を課題として確定。今回は都市「建築品質」改善が目的。QAツールばかり増やすことはしません。

## 実装した差分

| 対象 | G4-A A1 |
|---|---|
| 街区 | P2.4S R2と同じ192×192の3×3構成、12幅道路と中央広場 |
| 原型1 | **SLENDER STEPPED**。24×24の細身、52m本体、張り出した白いバルコニー、シアンガラス、低い頂部タワー |
| 原型2 | **WIDE GLASS OFFICE**。36×36で68m、本物の外壁を四面、白い縦リブ、段状の上部・ガラスクラウン |
| 原型3 | **TWIN SKYBRIDGE**。離れた幅12の2翼と空中渡り廊下、56m、非対称の屋上 |
| 配置 | 原型3棟はそのまま施工、残り5棟を既存の高速Cloneでコピー |
| 個別化 | 残る5棟は立面の縦アクセント、バルコニー、ルーフトップ装飾を個別に重ねる（Cloneだけの同形ではない） |
| 外装 | WHITE_CONCRETE、LIGHT_GRAY_CONCRETE、BLACK_CONCRETE、CYAN_CONCRETE、CYAN_STAINED_GLASS、LIGHT_BLUE_STAINED_GLASS |
| 道路 | 交差点構造は不変、旧金縁・石を暗い舗装・白の区画線へ変更 |
| 中央広場 | 白/灰色の公共床・シアンの中央モニュメント |
| 境界/速度 | Fillは32,768ブロック、Cloneは262,144ブロックを超えない。75点AIR検査と一回ラッチを継続 |

MakeCodeブロック名はJavaScript参照の列挙にある既知のコンスタントのみ採用。実機での素材の描画結果はまだ未確認であり、CIはあくまでTypeScriptスタブ＋ボクセル模擬。

## なぜ原型は3種類のままか

8棟すべてを独立した大量のFillで施工すると、低コストで実証済みのClone速度を捨てる危険がある。そこで**3原型を本当に違うシルエットにし、5クローンを専用の少数Fillで仕上げる**方式を採った。3原型＋5差分で高い外観の違いを狙う。

この段階はまだ総合デザインの完成ではない。地下鉄、歩道、植栽、交差点、道路の曲線、建物密度と街区接続はG4-B / G4-Cの優先課題。

## 以前の試験を保持

- 旧P2.3/P2.4R/P2.4Sの実機結果、ラッチ、CSVは変更しない。
- G4-Aは固有の新しいコード、コマンド、出力フォルダーで試験する。
- 起動するたびUTC時刻＋GUIDで新しい `G4A_A1/runs` 内専用ディレクトリを作る。使用済みのディレクトリは再利用できない。
- ゲーム内 `g4aSiteSurvey()` は施工前に75点の空気確認。コケた段階ではラッチを消費しない。施工が始まったら同じRunを再試行しない。
- Minecraft外のクリップボード作業とCSV監視を1回の起動スクリプトでまとめ、Minecraft GUIだけ人手で動かす。
- 重要ワールドは一切対象にしない。破棄可能な専用ワールド内での試験は包括的に事前承認済み。

## OMENでの操作

現在のリポジトリに未コミットの変更がないことを確認してから：

```powershell
cd "$HOME\Documents\makecode-limitlab"
git status --short
git fetch origin dev/g4a-architecture-families
git switch --track origin/dev/g4a-architecture-families
.\RUN_G4A_A1.cmd
```

**COPY OK**ならMinecraft Educationの破棄可能なテスト用ワールドで、Cキー → Code Builder → JavaScriptタブ → Ctrl+A・Ctrl+V → 実行。File Read & Write拡張を保持し、エラー0件を確認する。

チャットコマンド：
- `labareag4a`：建築予定領域を表示。書き込まない。
- `labcityg4a`：新しい建物8棟を1回だけ施工。
- `labstatusg4a`：進行状態確認。
- `labstopg4a`：安全チェックポイントで協調停止。

結果ZIPの格納先：
`Downloads\MakeCode_LimitLab\G4A_A1\runs\<固有RunID>\private_results\USER_UPLOAD_THIS_G4A_...zip`

ZIPと**同一高度・同一方向からの全景／斜め俯瞰スクリーンショット**をこのチャットで共有すると、P2.4Sの2枚と比較して外観・見やすさ・密度を評価できる。

もし監視を閉じた後に結果を収集する場合、新しい施工を起動せず、出力ログの`Private output:`に表示された既存Runのパスを `--output-root` に指定して `python -B .\tools\g4a_capture.py --output-root "そのパス"` を使う。

## PASS判定

GitHub ActionsのテストPASSをMinecraft実機PASSと言わない。完走CSVの`FAST_COMPLETED_SAMPLED_NOT_EXACT`は**18点の最終サンプルを含む実機完走**のみを意味し、全ブロック完全一致ではない。見た目と速度も画像・時計で別途評価。

次はG4-B（歩道、植栽、交差点、密度、地面との接続）、G4-C（巨大複数街区生成）。
