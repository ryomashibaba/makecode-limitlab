# MakeCode LimitLab

Minecraft Education MakeCodeの技術的限界を、施工・動的更新・ファイル入出力・安定性の実験で調べる独立研究プロジェクトです。

- **日本語のセットアップと注意点:** [README_JA.md](README_JA.md)
- **計測結果ダッシュボード:** [docs/index.html](docs/index.html)（GitHub Pagesを有効にするまでローカル閲覧可能）
- **MakeCode P1.0 ソース:** [makecode/main.ts](makecode/main.ts)
- **クラウドChat開発の方針:** [CLOUD_CHAT_HANDOFF.md](CLOUD_CHAT_HANDOFF.md)
- **公開手順:** [PUBLISH_JA.md](PUBLISH_JA.md)

## 検証状態

P0.6〜P0.8の各段階はMinecraft Education実機でPASS。P1.0の4,096・16,384ブロック統合試験は**実機未確認**です。オフライン模擬テストの成功を、Minecraftでの成功と混同しません。

## 公開・プライバシー方針

実際の利用者CSV、ローカルのログ、ワールドデータ、スクリーンショットは公開リポジトリに含めません。`tests/fixture_p*.csv` は完全な**合成テストデータ**です。ダッシュボード上でCSVを読み込む際はブラウザー内のみで解析し、自動送信しません。

既存のMinecraftAIBuilderには影響を与えず、専用テストワールドで使用します。リポジトリがPublicであっても、再利用ライセンスを付与したという意味ではありません。