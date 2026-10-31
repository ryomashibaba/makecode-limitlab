# D3S26-M02 — Windows起動引数の安全修正 / ZIP確定値（2026-10-31 JST）

この記録は、同工程で作成した `D3S26_M02_NATIVE_BLENDER_AUTHORING_STUDIO_PREPARATION_JA.md` の**配布ZIP情報のみを訂正**するappend-only追記である。過去の研究原本は編集していない。

初期配布スクリプトのWindowsコマンドで、末尾のバックスラッシュを含む引用付きディレクトリ引数が壊れる可能性があったため、`M02_make_studio.py` が `__file__` の親ディレクトリから相対参照する方式へ変更し、バッチから不要なディレクトリ引数を削除した。

**確定配布ZIP:** `D3S26_M02_VISUAL_AUTHORING_STUDIO.zip`、**17,622 bytes**、CRC PASS、SHA256 **`65952d11c479c4c6cd675c94ec6a6d2d3900db9c5bc986cab616528bf27546e3`**。前記文書のサイズ17,679 bytes・SHA `c7edf...` は旧配布版であり、**使用すべき正本ではない**。

Python構文再検査PASS、M01原本SHA一致。**Blender本体実行・.blend実生成・8視点実画像はNOT RUN**。ART HOLD、採用0、正式QA NOT RUN、Minecraft Education施工禁止のまま。

ZIP/GLBをGitHubへ保存済みとは主張しない。main/PR #53の状態は維持。
