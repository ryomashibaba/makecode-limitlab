# GitHub 公開準備 — 新規Publicリポジトリ

このパッケージは、既存プロジェクトを一切変更せず、専用リポジトリを**新規**作成するためのものです。

## ユーザーの最小操作

1. <https://github.com/new> を開く。
2. `Repository name` に **makecode-limitlab** を入力し、`Public` を選択。
3. `Add a README file`、`.gitignore`、`Choose a license` は**設定しない**（初回ファイル登録はこちらで行う）。
4. `Create repository` を押し、できたリポジトリのURLをChatGPTに送信。

新規リポジトリにファイルを追加できるGitHub連携が有効なら、ChatGPTがこのパッケージを投稿できます。新規リポジトリが連携権限の対象外のときはGitHubのインテグレーション設定からこのリポジトリへのアクセスを許可する必要があります。

## 公開してよいファイル

`README.md`、`README_JA.md`、`CLOUD_CHAT_HANDOFF.md`、`PUBLISH_JA.md`、`makecode/`、`docs/`、`tools/`、`tests/`、`.github/workflows/verify.yml`、`.gitignore`、`MANIFEST.json`。

`tests/fixture_p*.csv` は合成データ。利用者からアップロードされた実験CSV、Minecraftワールド、ZIP、ログ、画像、個人パス付きファイルは含めません。

## GitHub Pages

ファイル投稿後に GitHub リポジトリの `Settings → Pages` で `Deploy from a branch` を選び、`main` ブランチの `/docs` を指定すると静的ダッシュボードを公開できます。GitHub側の設定変更は、実際のリポジトリにファイルが存在してから行います。

**公開完了を確認するまでは、サイトURLが稼働していると主張しません。**
