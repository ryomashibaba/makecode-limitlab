#!/usr/bin/env python3
"""Build an inspectable GitHub Markdown gallery from three REAL Blender renders.

Requires the EXISTING native author early-review manifest and three PNGs.
Never generates geometry, upgrades ART, certifies safety, or runs Minecraft.
Never uses X11 screenshot/camera renders from prior two-box technical studies.
"""
import argparse
import base64
import hashlib
import html
import json
from pathlib import Path

from PIL import Image

VIEWS = ('AERIAL', 'PUBLIC_EYE', 'HABITAT_EYE')
MANIFEST = 'M37P2_EARLY_REVIEW_UNAPPROVED_MANIFEST.json'
README = 'README_ART_HOLD.md'
HTML = 'OPEN_GENUINE_THREE_VIEW_ART_HOLD.html'
SUMMARY = 'M37P2_CANDIDATE_GALLERY_AUDIT.json'
MAX_IMAGE_BYTES = 8_000_000


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as file:
        for data in iter(lambda: file.read(1024 * 1024), b''):
            h.update(data)
    return h.hexdigest()


def verify(directory, blend):
    directory = Path(directory).resolve()
    raw = directory / MANIFEST
    if not raw.is_file() or raw.stat().st_size > 250000:
        raise ValueError('AUTHORED_BLEND_NATIVE_REVIEW_MANIFEST_REQUIRED')
    manifest = json.loads(raw.read_text('utf-8'))
    if (not isinstance(manifest, dict) or
            manifest.get('schema') != 'g4c7-m37p2-artist-native-early-review-v1' or
            manifest.get('official_adoption') != 0 or
            manifest.get('Minecraft') != 'FORBIDDEN' or
            manifest.get('formal_331_993') != 'NOT_RUN' or
            manifest.get('G0_S1_G1_G2_G3') != 'NOT_RUN' or
            manifest.get('absolute_art') != 'NOT_ASSESSED_HUMAN_ABSOLUTE_REVIEW_REQUIRED'):
        raise ValueError('SOURCE_ART_CHARTER_OR_NATIVE_REVIEW_INCOMPLETE')
    source = manifest.get('source_sha256_before_and_after')
    if not isinstance(source, str) or len(source) != 64:
        raise ValueError('INVALID_AUTHOR_SOURCE_HASH')
    blend = Path(blend).resolve()
    if not blend.is_file() or blend.suffix.lower() != '.blend':
        raise ValueError('ACTUAL_SAVED_BLEND_SOURCE_REQUIRED')
    if blend.name != manifest.get('source_blend') or digest(blend) != source:
        raise ValueError('ART_AUTHOR_BLEND_SOURCE_CHANGED_OR_MISSING')
    images = manifest.get('early_native_three_view_renders')
    if not isinstance(images, dict) or set(images) != set(VIEWS):
        raise ValueError('THREE_GENUINE_BLENDER_VIEWS_REQUIRED')
    evidence = {}
    for name in VIEWS:
        entry = images[name]
        if not isinstance(entry, dict):
            raise ValueError('INVALID_VIEW_MANIFEST_' + name)
        fn = 'M37P2_' + name + '.png'
        if entry.get('name') != fn:
            raise ValueError('VIEW_NAME_CHANGED_' + name)
        path = directory / fn
        if not path.is_file() or not 200 <= path.stat().st_size <= MAX_IMAGE_BYTES:
            raise ValueError('VIEW_PNG_MISSING_OR_TOO_LARGE_' + name)
        if digest(path) != entry.get('sha256'):
            raise ValueError('VIEW_PNG_SHA_MISMATCH_' + name)
        with Image.open(path) as img:
            img.load()
            if img.format != 'PNG' or img.width < 320 or img.height < 240 or img.width * img.height > 5000000:
                raise ValueError('VIEW_NOT_GENUINE_SIZED_PNG_' + name)
            pic = img.convert('RGB').resize((128, 96))
            pixels = pic.get_flattened_data() if hasattr(pic, 'get_flattened_data') else pic.getdata()
            visible = sum(max(px) >= 20 for px in pixels) / (128 * 96)
        evidence[name] = dict(file=fn, sha256=digest(path),
                              visible_fraction=round(visible, 6),
                              early_black_view_reject=visible < .035)
    return source, evidence


def build(directory, blend):
    directory = Path(directory).resolve()
    for name in (README, HTML, SUMMARY):
        if (directory / name).exists():
            raise FileExistsError('APPEND_ONLY_ART_GALLERY_EXISTS_' + name)
    source, views = verify(directory, blend)
    black = [name for name in VIEWS if views[name]['early_black_view_reject']]
    state = 'EARLY_ART_REJECT_BLACK_VIEW' if black else 'ART_HOLD_HUMAN_CRITIQUE_REQUIRED'
    labels = {'AERIAL': '都市全景', 'PUBLIC_EYE': '公共・製造者目線', 'HABITAT_EYE': '住宅・私界目線'}
    markdown = [
        '# M37-P2 真正Blender早期ART審査 — 未採用', '',
        f'**判定: {state}／正式ART採用0件。**', '',
        '同じ保存済み作者Blender原本をBlender/Cyclesで撮影した3視点です。',
        'これは正式ART合格ではなく、造船設備・都市密度・玄関からの生活断面などを人が絶対評価するための証拠です。',
        f'原本SHA-256: `{source}`', '',
    ]
    sections = []
    for name in VIEWS:
        file = views[name]['file']
        label = labels[name]
        reject = '（画像黒／EARLY ART REJECT）' if views[name]['early_black_view_reject'] else '（人間審査待ち）'
        markdown += [f'## {label}{reject}', '', f'![Blender {label}]({file})', '',
                     f'PNG SHA-256: `{views[name]["sha256"]}`', '']
        data = base64.b64encode((directory / file).read_bytes()).decode('ascii')
        sections.append(f'<section><h2>{html.escape(label)} {html.escape(reject)}</h2>'
                        f'<img alt="{html.escape(label)}" src="data:image/png;base64,{data}"></section>')
    markdown += ['---', '', 'ART HOLD／正式採用0件／331人体・993足元とG0/S1/G1/G2/G3未実施。',
                 'MakeCode未評価／Minecraft施工禁止／main・Draft PR変更なし。',
                 '**画像枚数・形状数・CI成功は美術品質の代理指標ではありません。**', '']
    page = ('<!doctype html><html lang="ja"><meta charset="utf-8"><meta name="viewport"'
            ' content="width=device-width,initial-scale=1"><title>G4C7 M37P2 ART HOLD</title>'
            '<style>body{background:#141923;color:#f3f4f6;font:16px system-ui;margin:auto;'
            'max-width:1180px;padding:24px}section{padding:14px;background:#262d39;'
            'margin:18px 0;border-radius:12px}img{width:100%;height:auto;display:block}'
            'code{word-break:break-all}</style><h1>M37-P2／真3D早期美術レビュー</h1>'
            f'<p><strong>{html.escape(state)}・正式採用0</strong>／人間の絶対評価が必要</p>'
            f'<p>保存済み原本SHA <code>{html.escape(source)}</code></p>'
            + ''.join(sections) + '<p>331/993未実施、Minecraft施工禁止、作品採用なし。</p></html>')
    result = dict(schema='g4c7-m37p2-author-candidate-visual-gallery-v1',
                  result=state, source_blend_sha256=source, images=views,
                  human_accepted_art=False, official_adoptions=0, art='HOLD',
                  formal_331_993='NOT_RUN', G0_S1_G1_G2_G3='NOT_RUN',
                  minecraft='FORBIDDEN', makecode='NOT_EVALUATED',
                  geometry_generated=False, model_calls=0,
                  on_disk_original_blend_changed=False)
    (directory / README).write_text('\n'.join(markdown), encoding='utf-8')
    (directory / HTML).write_text(page, encoding='utf-8')
    (directory / SUMMARY).write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--review-dir', required=True)
    ap.add_argument('--blend', required=True)
    args = ap.parse_args()
    result = build(args.review_dir, args.blend)
    print('P2_GENUINE_CYCLES_GALLERY_READY_ART_HOLD', result['result'])


if __name__ == '__main__':
    main()
