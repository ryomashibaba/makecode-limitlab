# D3S26 M27 — 室内先行研究室に公開見学ギャラリーを実際に接続
2026-11-01 JST。TECH LIMITED PASS、ART HOLD、正式採用0、Minecraft Education施工禁止。

## 正本と今回の実作業
ryomashibaba/makecode-limitlab の研究ブランチ dev/g4c7-a17-monolithic-rift-fold-art-study、PR #53 Draft/Open。前回M26Bの室内は正式ART PASSではなく比較用の技術研究であり、その編集可能原本 M26B_EDITED_HUMAN_RESEARCH_ROOM.blend をSHA256 aae03e6af71a6acca1da740d73f12e4e8db6cceff457debe93aa299c2f7a241f で固定し、同原本を上書きせず新しいBlender研究に使用。M23～M25の不採用巨大建築は流用していない。

M17ネットワークの公開U0南側ギャラリー(-24,13,9.6)、公開U1研究見学(-29,30,9.6)、制限付きR0研究室(-43,37,9.6)を出発点に、M26B東側ガラス1面を非表示として制御開口、上階のU0→U1公開見学床、しきい、展示機材・植栽・実採光の外構を制作。内部研究室カメラを一切移動せず、外部の見学者眼高2カメラを追加。研究用途が既存ガラス越しに見えることを目指した。

## 真正Blender実行
制作コード tools/g4c7_m27_native_research_visitor_gallery.py、独立検証 tools/g4c7_m27_independent_gallery_readback.py、GitHub Actions .github/workflows/g4c7-m27-native-gallery.yml。初回run #41274311544は編集可能BLEND・3枚画像の撮影まで成功したが、独立検証が厚さ0.5の床をゼロ厚と仮定したためFAIL。検査を正し、手前の展示物が床の外へ浮く配置も修正。最新[GitHub Actions #41274393708](https://github.com/ryomashibaba/makecode-limitlab/actions/runs/41274393708)はBlender制作、3視点Cycles、保存後GLB独立再読込、画像・バイナリSHA256検査まで**全工程SUCCESS**。同HEAD通常Verify LimitLabもSUCCESS。

成果物：GitHub Artifact ID 13070294786。ZIP D3S26_M27_NATIVE_FINAL_GALLERY_EVIDENCE.zip、3,219,140 bytes、SHA256 64a92c1b7e398236973c6e301c0df3104ca15a8a2bbd5df8efb7bfe8ee4c70d6、ZIP CRC PASS。保存BLEND SHA256 b39af3481a003ad6eef0e844310be8d7abce0af5616489f8514d1db3d3860efb、保存GLB SHA256 8403aa9a7d0704731361dfc51b080b23d473968bbeb49407bd9aa55a31c2934a。実Cycles PNGは gallery_arrival_eye、controlled_threshold_eye、original_research_eye の1080×680で3枚、全SHA manifest一致。新制作Blenderオブジェクト56、GLB新規メッシュ55個。

## 実GLBの独立接続監査
元M26B GLBとM27 GLBの両方をtrimeshで読み込み、元の157メッシュ中、公開口として取り除いた東ガラス M26_east_large_daylight_glazing_32 だけが非表示となり、ほか**156メッシュのワールド頂点・面配列はすべて一致**。旧M22道路は元BLEND内部で不変だが、以前から非表示のため、M27の見学ギャラリーGLBで全都市道路を検査したとは主張しない。

独立Shapely検査:
- 公開上階ギャラリー実床上面 306.8700研究単位²、実厚0.5。U0(-24,13)・U1(-29,30)・中間1点の3か所はそれぞれ半径0.65円の範囲がこの公開床に収まる。ただしこれは限定3中心のみ。
- 実床→しきいの交差面積 5.9280研究単位²（正）。
- しきい→元研究室木床の交差面積 5.1350研究単位²（正）。
- ギャラリー床上面 z9.643、しきい上面 z9.664、差0.021研究単位。
- ガラス壁1面を実際に抜いて開口を作った。設計上の幅2.60、高さ3.2研究単位。ただし正式な障害物3D掃引検査や実際のドア/ガラス衝突の証明ではない。

## 実画像での厳しい美術判定
公開見学通路の壁を通してM26B研究室の測定機器が認識でき、中央の出入口も視覚上開いている。室内human-eyeは旧M26Bカメラと家具を維持。室内一室から公開見学へ発展できる技術的方向性を確認。ただし公開ギャラリーは長い白い通路と反復した庇梁が支配し、展示の面白さ・人間の活動・外界と未来都市を感じさせる奥行きが不足。手前の低ポリ植栽が視界を大きく遮るカメラもある。**ART HOLD / 正式採用0件**。画像を見ずに材質やメッシュ数で美術PASSを宣言しない。

## M28の優先作業
M27の既存室内と公開経路を保持しながら、公開通路を単調な白い廊下から活動の見える体験型研究ギャラリーに直接美術修正。カメラ位置からの植栽遮蔽と展示の弱さを改善し、入館導線と見学実験が両方見える本物の眼高比較を作成。室内・公開見学の意味が画像から読めない場合は早期美術REJECT。M17全体ネットワークを結線したと主張せず、地上アクセス・縦動線は後の独立検査とする。

**安全・施工境界**：公式331人体・993足元、G0/S1/G1/G2/G3はNOT RUN、正式安全認定なし。M27のルート座標・床重なりは建物通行安全を証明しない。Minecraft Education書込み/都市統合0、施工禁止。MakeCodeのみで最終施工する従来方針を維持。main無変更、PR #53 Draft/Open、Work無断使用なし、ユーザーPC操作0。
