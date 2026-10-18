# LimitLab P1.4 — cloud Chat handoff

- Canonical repo: https://github.com/ryomashibaba/makecode-limitlab (Public)
- P1.0 main.ts original SHA preserved by `tools/verify_source.py` CI.
- P1.0 real-world: B4096, B16384, three update modes, 1/64/256KiB I/O all PASS. ENDURANCE_QUICK incomplete; user stopped it successfully.
- P1.3 real-world: QUICK 24/24 PASS and SOAK30 300/300 PASS.
- P1.4 adds **standalone** `makecode/limitlab_p1_4.ts`, not replacement of main.ts. This is an independent program installed by replacing current MakeCode editor script; other versions remain in GitHub.
- `labauto14` one-time guarded quick suite: 512 fill/clone 4+4, PAUSE150, MIXED150, 256KiB IO, POSTIO60; CRC-free full-text I/O validation; CSV heartbeat every25 iterations.
- `labplan14` read-only 32,768 / 65,536 planned tessellation; **no large construction authorized**.
- Never upload private CSVs to public repository; synthetic test data only.
- Expected upload `USER_UPLOAD_THIS_P14_STATUS.csv`. If stopped, do not rerun without reasoning about partially written blocks.
- Source default output folder placeholder `__P14_ROOT__` is substituted by COPY_P14.ps1 and its source SHA must match. Copy from `makecode/PASTE_THIS_P14.ts` only if clipboard verification fails.
- P1.4 static/mocked testing does not prove real Minecraft performance; require real Minecraft Education evidence.
- Work policy: Cloud Chat default, Cloud Work only when obviously more efficient or required; local Work avoid. Minimal human copy/paste and infrequent field QA. Many development stages per handoff.
