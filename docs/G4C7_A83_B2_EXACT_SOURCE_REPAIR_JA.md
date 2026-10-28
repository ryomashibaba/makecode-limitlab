# A83-B2 修復アーカイブ — 分割gzip+base64原本の一致確認を必須化

2026-10-28 JST。前コミット \`188641b70635c9bbc014e5a76da3168ee0b1bac7\` の単一ファイル \`g4c7_b2_prototype.py.gz.b64\` は伝送上の省略により原本バイト数が一致していないため、**正式なソース正本として使ってはならない**。旧ファイルはappend-onlyで残す。

こちらの \`g4c7_b2_prototype.py.b64.part0\` 〜 \`part3\` を番号順にバイト列連結し、\`base64.b64decode(...,validate=True)\`、\`gzip.decompress\`で解凍する。復元したPythonのSHA-256は必ず \`54a152007eda9693dd9f32506149b19d8547eb7c1e430b6ec29b61f5432f3c93\` となること。異なれば**SOURCE_INTEGRITY_FAIL**とし、その後のCI/生成は実行しない。生成した画像や完成都市の美術認定ではない。

原本はART REJECTの研究記録。G0の局所開口4か所は限定的に観測、上下に5.9mの非支持ギャップ、ランプと入口4m分離。正式331/993、S1/G1/G2/G3はNOT RUN。全体ART HOLD、美術採用0、Minecraft施工禁止。