# G4-C7 / D3S26 M34 — 編集可能Blender原本TECH PASS・都市ART REJECT



**2026-11-01 JST。全体ART HOLD、正式採用0、Minecraft Education施工・都市統合禁止、main不変更、PR #53 Draft維持。**



## 目的と実施した制作

M30〜M33の箱・板・巨大壁・孤立施設の不採用反復を停止。M34は新しい巨大都市のART候補ではなく、Blenderのネイティブ原本を後から直接編集して別原本を保存可能にする「制作媒体の実証」を対象とした。

実GitHub Actions #41285017950（SUCCESS）でBlender 4.5.15による保存BASE.blend／BASE.glbと固定6視点PNGを制作。保存したBASE.blendをBlenderで再オープンし、**既存屋根メッシュの頂点2つだけを元形状からZ+2.25研究単位変更**して、DIRECT_EDIT.blend／DIRECT_EDIT.glbへ別保存、固定の同一6視点を再撮影。

独立監査で両GLB実27メッシュ・1,080三角形、**変更メッシュ1、不変26**、6×2=12枚の実PNG（760×460）、BLENDER/glTF/PNGヘッダー、保存SHA256、6編集可能なコレクション、Blender再オープン後の実頂点変更を確認。全工程SUCCESS。技術方法のPASSであり、GUIを手作業操作したとの主張ではない。



## 独立実画像／床支持ART監査

実保存GLBの南北・斜視では**離れた二つの低層室＋長い細い一本の連絡床**しかなく、都市の巨大スカイライン、2公共軸、生活・都市密度、居住区が存在しない。製造者眼高は設備の不透明面に視界を大きく遮られ、研究者眼高も無地壁が主体。頂点2個の変更、カメラ画像の差異を美術改善と認めない。**M34モデル ART REJECT／全体ART HOLD／正式採用0**。

独立Trimeshによる保存GLBの実三角支持検査で、元Blender座標 X=73・床Z=5.2 の上階研究室入口に、**Y=5.90公共床あり／Y=6.25支持床なし／Y=6.55研究室床あり**を確認。入口しきい値の未支持部分は残り、安全な通過を保証しない。床・壁の存在は全人体の連続通行や安全の証拠ではない。



## 正本保護・証拠

[M34制作ソース](https://github.com/ryomashibaba/makecode-limitlab/blob/dev/g4c7-a17-monolithic-rift-fold-art-study/tools/g4c7_m34_blender_native_authoring_gate.py)。

[M34全17ファイルのGitHub永続保存フォルダ](https://github.com/ryomashibaba/makecode-limitlab/tree/dev/g4c7-a17-monolithic-rift-fold-art-study/artifacts/g4c7-m34-verified-native-evidence)には、.blend 2、.glb 2、PNG 12、検査manifestを実在確認済みでappend-only記録。保存専用Actions #41285486454 全ステップSUCCESS。READMEを別途付記。期限付きGitHub ActionsのArtifactだけに依存しない。

取得済み一時ZIP M34_NATIVE_BLENDER_AUTHORING_ART_HOLD.zip は17ファイル・CRC PASS・SHA256 aee0cfedaa656c3bad2cc299be01febaeb3c25bd681fa9b3b4770cdfa72abc48。これはZIPハッシュでありGitツリー全体のハッシュではない。



## 次の工程

**METHOD TECH PASSとART REJECTを混同しない。** 今回の2施設試験体を拡張して都市にしない。M35では、証明済みのBlenderネイティブ編集方式を、都市外観と複数の実生活室・街路・上下接続を同じ作者シーンで同時に決定する真正美術制作へ適用。旧壁・棚・低層キャンパス型に戻れば早期停止する。単純な大量生成器をもう一度作らない。正式ART採用はユーザー判断。

正式331人体/993足元、身体半幅0.65、相対+0.15〜+3.25、歴史的45干渉上限、未支持0、正式負対照、G0/S1/G1/G2/G3、MakeCodeへの1m換算とFill/Clone/Place、Minecraft施工はすべてNOT RUN。Workは事前承認制。旧原本とmainは変更しない。