# M37-P2 真正Blender原本の独立バイナリ監査（2026-11-03）

結論：**ネイティブ保存・別Blenderプロセスでの読込を実証。SOURCE TECH限定。実4視点Cyclesと美術認定は未確認。ART HOLD／正式採用0。**

## 一次証拠
- GitHub Actions [#41577380073](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41577380073)（旧source commit `abba4c018064c95cbd51f375d1a51f644e00c7e7`）はcompleted/failure。ただし新規BLEND保存後、Blender 4.5.15 LTSの別プロセスが `Read blend:` を出力した。後段の旧reviewで `from PIL import Image` → `ModuleNotFoundError: No module named 'PIL'` のため停止した。
- Actions Artifact **13208845765** のZIPを取得し、単一の `M37P2_CLOUD_AI_NATIVE_INTEGRATED_STUDY_ART_HOLD.blend`（198,887 bytes）を独立に取り出した。
- 原本SHA-256：`ac6c322e1f4a957281ca5a7f2d9633ce4d602b7254cb1717735feb6ed02e9bd6`。
- 原本はzstd圧縮。`zstd -d`展開後2,081,462 bytes、先頭は `BLENDER-v405`（64-bit little-endian）。独立したBLENDデータブロックの歩査で`ENDB`がファイル末尾と完全一致。
- 実測内部ブロック：`OB=235`、`ME=227`、`MA=10`、`GR=6`、`CA=4`、`LA=4`、`SC=1`、`ENDB=1`。`P2_CITY_MACRO_DIRECT_AUTHOR`、`P2_HABITAT_PRIVATE_DIRECT_AUTHOR`、`HOME_ACTUAL_LIVING_SOFA`、`SPACECRAFT_HULL_IN_ACTIVE_ASSEMBLY`、`RESEARCH_REAL_BENCH_0`、`PUBLIC_CULTURE_REAL_BOOKSHELF_0`、`P2_CLOUD_AUTHOR_NOT_GUI` の文字列が存在。

## 限界と次工程
- これは**真正Blender保存・再読込・バイナリ整合の限定証拠**。命名やオブジェクト数は美術的品質、都市景観、動線、居住、製造能力、安全性を保証しない。
- 本命R1の作者方法は依然METHOD HOLD。共通`tower()`の12棟反復、`room()`／`walkway()`依存という以前の作者方法監査を解除しない。AIのBlender GUI手操作をしたと主張しない。
- 修正後cloud-native [#41577471323](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41577471323)は照合時queued。そこから真正4枚のCycles画像、原本、manifestを取得し**現物を直接目視**するまでART評価は未実施。安易な定型反復と空疎な街路はEARLY ART REJECT対象。
- CI Verify [#41584052963](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41584052963) はPython3.12用Pillow修復後もqueued、全体PASS未確認。
- R0–R5、ART HOLD／採用0、正式331人体・993足元・G0/S1/G1/G2/G3 NOT RUN、MakeCode未評価、Minecraft施工禁止、保護v3とmain変更禁止、PR #53 Draft維持、Work／Sol事前承認は不変。
