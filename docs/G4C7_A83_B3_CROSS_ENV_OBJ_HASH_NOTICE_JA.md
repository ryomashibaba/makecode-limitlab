# A83-B3 — ローカルとGitHub Actions間のOBJバイトハッシュ不一致に関する追補（append-only）

2026-10-28 JST。対象：G4-C7 A83-B3 G0 ART REJECT。旧監査・3D・PNG・コードは**不変更**で保護。

## 実際の相違
- ローカルで保存したOBJ `output/a83_b3_integrated_civic_study.obj`：SHA256 `59c81993160704697a696845e331510e822338a93839f2f8006f9bf7cf821725`。
- GitHub Actions #40630143320が**保存した別途再生成OBJ**：SHA256 `7e9ac811afb3b8b1ebe3b71751676e5f6ed09915ad0ac4970812884884bf8b12`。
- どちらもソースの圧縮tar.gz原本SHA256 `bf19cd10e045a5b10825575b464bdad7d06a44ef1a52bcb4f0f65a3ed1e03ee2` に基づく。Actionsはソース4ファイルの個別SHA256を実際に検査してSUCCESS。
- いずれも335部材／3972三角形／11916 OBJ頂点として監査された。GitHub自身のOBJ⇄manifestのSHA一致、独立実三角形レイ6開口、共有床3、階段3、故意破損5/5、4視点PNGの実生成は成功。
- GitHubの`oblique.png`と`public_eye.png`を再取得し、**画像を実際に開いて視覚観察**。ローカルと同じ「3つの低層箱型施設／無地巨大壁」のG0 ART REJECTで、採用する余地なし。

## 証明できていないこと
**二つのOBJの完全な頂点配列・面順序・法線・三角形集合が数学的に同一かは未証明**。原因も未特定。可能性としてShapely/GEOS、数値処理の実装環境による三角形順序差などは考えられるが、断定しない。したがって「ローカルとCIがバイト単位で同一モデルを再現した」と主張しない。

Github上で各結果の真のメッシュを再読込した狭いTECH G0のPASSと、跨環境でバイト同一性の保証がない状態を明確に分離する。次回同様のモデルを作る際は、環境固定またはソート済み三角形の正規化ダイジェストを設け、ローカル⇄Actionsの一致条件を追加する。今回の不採用モデルの装飾・大規模化をこの検証のために再開しない。

**総合はG0 ART REJECT／ART HOLD／正式美術採用0／正式S1/G1/G2/G3 NOT RUN／Minecraft Education施工禁止。**
