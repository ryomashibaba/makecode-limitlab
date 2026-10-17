# クラウドChatプロジェクト用・引き継ぎ指示

Minecraft Education MakeCodeの限界（大量ブロック施工、高速更新、ファイル入出力、長時間安定性）を調べるLimitLabを継続開発する。

## 既定の開発モード
- **クラウドプロジェクト内のChatでコードの設計・実装・テストを進める**。
- WorkはChatより明確に効率がよい場合かWorkでしか実現できない場合のみ、クラウドWorkを優先する。ローカルWorkは原則使わない。
- ユーザー作業はMinecraft Education内のコード少量貼付・まれな実機確認・必要なCSV送付程度とする。
- 過去のP0.1〜P0.6で起きたエディター構文エラー、コピー欠落、非同期処理中の多重コマンド、Minecraft側チャット構文エラー、occupied領域、Downloads直下への大量ログ生成を再発させない。
- 大きな開発差分を一度に進め、ユーザーへの細かいバージョン渡しは避ける。品質を犠牲にした一括進行はしない。

## 実機エビデンス
- P0.6: 64ブロック施工や更新、IO、短時間耐久がPASS。
- P0.7: 512ブロック施工 place/fill/clone 各1回PASS。ファイル時刻概算は約9505ms/208ms/30msだが厳密速度比ではない。
- P0.8: fill 512を5回PASS、clone 512を5回PASS。
- P1.0: 4096/16384の統合試験コード完成（オフライン模擬）。**実機結果未受領**。`labauto1`を専用ワールドで1回実行し`USER_UPLOAD_THIS_P10_STATUS.csv`を回収するまでは規模を増やさない。

## 新しいP1.1クラウド基盤
- Web dashboard: `docs/index.html`, `docs/app.js`, `docs/style.css`。CSVはブラウザー内だけで解析。
- CSV解析: `tools/limitlab_results.py`。P1.0は**全必須工程**がPASSでないと総合PASSとしない。STOPとINCOMPLETEを区別する。
- 自動検証: `.github/workflows/verify.yml`; `tests/`はPythonとNodeの回帰テスト。
- **P1.0のMakeCodeソースそのものは意図的に変更していない。** sha256は`tools/verify_source.py`で検証する。
- GitHubリポジトリは **Public公開がユーザー承認済み**。既存リポジトリは変更しない。GitHub連携ではリポジトリ新設操作がないため、ユーザーに `makecode-limitlab` という空のPublicリポジトリを作ってもらった後、初期ファイルを投稿する。

## 次の順番
1. P1.0実機CSV取得・解析。STOPの際は正確な失敗ステージを特定して修正し、無理に拡大しない。
2. 信頼できる時間計測手法を公式仕様から確認。ファイル時刻を精密計測と偽らない。
3. 小さな繰り返し成功を根拠に32,768以上へ進むか決める。チャンク境界・未ロード領域・ゲーム側制限を扱う。
4. Publicの承認済み。新規リポジトリ作成後に初期ファイルを登録し、Pagesを有効にする。

## 2026-10-17 実機追記
- P1.0の4,096ブロック、16,384ブロック、3種類の更新、256KiBまでのI/OはスクリーンショットでPASS確認。ENDURANCE_QUICKと最終CSVは未確認。
- `labstatus1` で現在工程を確認し、旧試験を再実行しない。
