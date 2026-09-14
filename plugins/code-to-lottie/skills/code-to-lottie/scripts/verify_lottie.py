#!/usr/bin/env python3
"""verify_lottie — prove a Lottie JSON matches its SVG+CSS source.

Stage 1 (always): TIMING — re-parse the source's @keyframes/animation rules
with svg2lottie's parser and assert every layer's keyframes (times, values,
easing) match the expected model.
Stage 2 (always): GEOMETRY — re-derive each part's curves fresh from the
source SVG, sample both source and Lottie beziers, map Lottie points back to
SVG space, and assert max deviation <= 0.05px (build rounds to 0.01px).
Stage 3 (--diff): DIFF PAGE — write a self-contained diff.html (inline
lottie.min.js + JSON + source SVG) that pixel-diffs the paused Lottie against
the source rendering and prints the match % in the page title.

Usage:
  python3 verify_lottie.py source.svg anim.json
  python3 verify_lottie.py source.html anim.json --diff [--lottie-js lottie.min.js]

Exit 0 = stages 1-2 PASS. Stage 3 pass bar: >= 99% pixels within tolerance
(antialiasing differences between rasterizers eat the rest).
"""
import json, math, os, re, sys, argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import svg2lottie as S

DIFF_TPL = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>lottie diff</title>
<script>__LOTTIE_JS__</script>
<style>body{font:13px monospace;margin:16px}.row{margin-bottom:20px}
canvas{outline:1px solid #ddd}.chip{padding:3px 10px;border-radius:99px;background:#eef8e8;display:inline-block}</style>
</head><body>
<div>__TITLE__</div>
<div class="row"><div>source (svg) vs lottie (paused @__FRAME__)</div>
<div>__ORIG__</div><div id="box"></div></div>
<p class="chip" id="chip">diffing…</p>
<script>
const DATA = __DATA__;
const SRC = __SRC__;
const FRAME = __FRAME__, SCALE = 3, TOL = 32;
function drawOrig() {
  return new Promise(res => {
    const img = new Image();
    img.onload = () => {
      const c = document.createElement('canvas');
      c.width = DATA.w * SCALE; c.height = DATA.h * SCALE;
      c.getContext('2d').drawImage(img, 0, 0, c.width, c.height); res(c);
    };
    img.src = URL.createObjectURL(new Blob([SRC], {type: 'image/svg+xml'}));
  });
}
function drawLottie() {
  return new Promise(res => {
    const el = document.createElement('div');
    el.style.width = DATA.w * SCALE + 'px'; el.style.height = DATA.h * SCALE + 'px';
    document.getElementById('box').appendChild(el);
    const a = lottie.loadAnimation({container: el, renderer: 'canvas', loop: false, autoplay: false, animationData: DATA});
    a.goToAndStop(FRAME, true);
    setTimeout(() => res(el.querySelector('canvas')), 250);
  });
}
(async () => {
  const [c1, c2] = await Promise.all([drawOrig(), drawLottie()]);
  const d1 = c1.getContext('2d').getImageData(0, 0, c1.width, c1.height).data;
  const d2 = c2.getContext('2d').getImageData(0, 0, c2.width, c2.height).data;
  let bad = 0, total = c1.width * c1.height, sum = 0;
  for (let i = 0; i < d1.length; i += 4) {
    const dd = Math.max(Math.abs(d1[i]-d2[i]), Math.abs(d1[i+1]-d2[i+1]), Math.abs(d1[i+2]-d2[i+2]));
    if (dd > TOL) bad++; sum += dd;
  }
  const match = 100 * (1 - bad / total);
  document.getElementById('chip').textContent = (match >= 99 ? '\\u2713 ' : '\\u2717 ') +
    match.toFixed(2) + '% pixel match (mean \\u0394' + (sum / total).toFixed(2) + ')';
  document.title = 'DIFF ' + match.toFixed(2) + '%';
})();
</script></body></html>"""

def sample_sub(s, n=16):
    v, i_, o = s['v'], s['i'], s['o']
    pts = []
    segs = list(range(len(v) - 1)) + ([len(v) - 1] if s['c'] else [])
    for k in segs:
        p0, p3 = v[k][:2], v[(k + 1) % len(v)][:2]
        c1 = [v[k][j] + o[k][j] for j in (0, 1)]
        c2 = [p3[j] + i_[(k + 1) % len(v)][j] for j in (0, 1)]
        for t in [j / n for j in range(n)]:
            mt = 1 - t
            pts.append(tuple(mt**3 * p0[j] + 3 * mt**2 * t * c1[j] + 3 * mt * t**2 * c2[j] + t**3 * p3[j]
                             for j in (0, 1)))
    return pts

def dedupe(pairs):
    """same clamp-dedupe the builder applies: a stop clamped onto an earlier
    frame replaces it (keep latest value)"""
    out = []
    for t, v in pairs:
        if out and out[-1][0] >= t:
            out[-1] = (t, v)
        else:
            out.append((t, v))
    return out

def check_timing(comp, kf_stops, anim, fps):
    N = int(anim['duration'] * fps)
    assert comp['op'] == N and comp['fr'] == fps, 'comp duration/fps mismatch'
    for L in comp['layers']:
        im = re.search(r'(\d+)$', L['nm'])
        idx = int(im.group(1)) if im else 0
        d0 = idx * anim['stagger'] * fps
        def stop_t(pct):
            t = round(pct / 100 * N + d0, 2)
            return round(pct / 100 * N, 2) if t > N else t   # tail stops go global

        o_pairs = [(stop_t(pct), st['opacity']) for pct, st in kf_stops if 'opacity' in st]
        s_pairs = [(stop_t(pct), st['scale']) for pct, st in kf_stops if 'scale' in st]
        o_exp = dedupe(o_pairs)
        s_exp = dedupe(s_pairs)
        if o_exp:
            got = [(k['t'], k['s'][0]) for k in L['ks']['o']['k']] if L['ks']['o'].get('a') else None
            assert got is not None, (L['nm'], 'opacity should be animated')
            assert got == o_exp, (L['nm'], 'opacity', got, o_exp)
        if s_exp:
            got = [(k['t'], k['s'][0]) for k in L['ks']['s']['k']] if L['ks']['s'].get('a') else None
            assert got is not None, (L['nm'], 'scale should be animated')
            assert got == s_exp, (L['nm'], 'scale', got, s_exp)
        for seq in ('o', 's', 'p'):
            prop = L['ks'][seq]
            if prop.get('a'):
                for k in prop['k'][:-1]:
                    e = S.EASINGS.get(anim['easing'], S.EASINGS['ease-out'])
                    assert k['o'] == e[0] and k['i'] == e[1], (L['nm'], seq, 'easing')
    return 'timing OK (%ss loop, %sms stagger, %d stops, %s)' % (
        anim['duration'], anim['stagger'] * 1000, len(kf_stops), anim['easing'])

def check_geometry(comp, parts):
    worst = 0.0
    assert len(comp['layers']) == len(parts), 'layer count != part count'
    for L, p in zip(comp['layers'], parts):
        c = S.bbox(p['subs'])                     # svg-space bbox (parts unshifted)
        cx, cy = (c[0] + c[2]) / 2, (c[1] + c[3]) / 2
        shs = [it for it in L['shapes'][0]['it'] if it['ty'] == 'sh']
        assert len(shs) == len(p['subs']), (L['nm'], 'subpath count')
        for sh, os_ in zip(shs, p['subs']):
            got = sample_sub(sh['ks']['k'])
            want = sample_sub(os_)
            assert len(got) == len(want)
            for (gx, gy), (wx, wy) in zip(got, want):
                sx, sy = gx + cx, gy + cy         # local verts = svg verts - center
                worst = max(worst, math.hypot(sx - wx, sy - wy))
    assert worst <= 0.05, 'geometry deviation %.4fpx > 0.05' % worst
    return 'geometry OK (max deviation %.4fpx)' % worst

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('source', help='.svg/.html the animation was converted from')
    ap.add_argument('json', help='the generated lottie json')
    ap.add_argument('--css', help='css file if not embedded in source')
    ap.add_argument('--fps', type=int, default=60)
    ap.add_argument('--diff', action='store_true', help='also write diff.html')
    ap.add_argument('--lottie-js', default='lottie.min.js',
                    help='lottie-web player to inline (download from cdnjs if absent)')
    ap.add_argument('--out', default='diff.html')
    a = ap.parse_args()
    src_text = open(a.source, encoding='utf-8').read()
    css = open(a.css, encoding='utf-8').read() if a.css else ''
    comp = json.load(open(a.json))

    parts, kf_stops, anim = S.extract_parts(src_text, css)
    if kf_stops and '<style' not in src_text and not css:
        raise SystemExit('source has no keyframes — pass --css')
    print('STAGE 1:', check_timing(comp, kf_stops, anim, a.fps))
    print('STAGE 2:', check_geometry(comp, parts))
    print('PASS: lottie matches source (timing + geometry)')

    if a.diff:
        # source svg cropped to the comp frame (same pad the builder used) for the pixel diff
        x0 = min(S.bbox(p['subs'])[0] for p in parts) - 4
        y0 = min(S.bbox(p['subs'])[1] for p in parts) - 4
        w, h = comp['w'], comp['h']
        m = re.search(r'<svg\b[^>]*>', src_text)
        stag = m.group(0)
        new_tag = re.sub(r'viewBox="[^"]*"', 'viewBox="%g %g %g %g"' % (x0, y0, w, h), stag)
        if 'viewBox' not in new_tag:
            new_tag = new_tag[:-1] + ' viewBox="%g %g %g %g">' % (x0, y0, w, h)
        new_tag = re.sub(r'width="[^"]*"', 'width="%g"' % (w * 3), new_tag)
        new_tag = re.sub(r'height="[^"]*"', 'height="%g"' % (h * 3), new_tag)
        src_crop = src_text.replace(stag, new_tag, 1)
        # an <img>-rasterized svg RUNS its css animation — freeze parts at the
        # "all in" state the paused lottie frame shows (scale-1/translate-0 hold)
        src_crop = src_crop.replace('</svg>',
            '<style>.lottie-part{animation:none!important;opacity:1!important;'
            'transform:none!important}</style></svg>')
        ljs = ''
        for cand in (a.lottie_js, os.path.join(os.path.dirname(os.path.abspath(a.json)), 'lottie.min.js'),
                     os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lottie.min.js')):
            if os.path.exists(cand):
                ljs = open(cand, encoding='utf-8').read(); break
        if not ljs:
            raise SystemExit('lottie.min.js not found — download from '
                             'https://cdnjs.cloudflare.com/ajax/libs/bodymovin/5.12.2/lottie.min.js')
        page = (DIFF_TPL.replace('__LOTTIE_JS__', ljs)
                .replace('__TITLE__', os.path.basename(a.json))
                .replace('__FRAME__', str(int(0.8 * comp['op'])))
                .replace('__ORIG__', src_crop)
                .replace('__DATA__', json.dumps(comp))
                .replace('__SRC__', json.dumps(src_crop)))
        open(a.out, 'w').write(page)
        print('STAGE 3: wrote %s — open it (or headless-chromium --dump-dom) and read the '
              'match %% in the title/chip; >= 99%% passes' % a.out)

if __name__ == '__main__':
    main()
