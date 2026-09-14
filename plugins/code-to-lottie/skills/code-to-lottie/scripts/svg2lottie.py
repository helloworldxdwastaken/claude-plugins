#!/usr/bin/env python3
"""svg2lottie — convert a tagged SVG + CSS-keyframe animation to Lottie JSON.

Source contract (the tagging the SKILL.md describes):
  - Each animated piece is an element (path/g/rect/circle/ellipse/text) with
    class "lottie-part" and style "--i: <n>" giving its stagger order.
  - A CSS block (in the file, or passed via --css) defines ONE keyframes rule
    used by the parts, plus a .lottie-part animation rule:
        .lottie-part { opacity: 0; animation: part-in 5s ease-out infinite;
                       animation-delay: calc(var(--i, 0) * 100ms); }
        @keyframes part-in { 0% {opacity:0; transform:scale(.6)} ... }
  - Supported transform functions: scale(), translate(). opacity supported.
  - Path commands: M/L/H/V/C/S/Q/T/Z (arc 'A' is not supported — flatten
    arcs to cubics first; shape_to_parts already emits cubics for rects).
  - <text> is NOT a Lottie shape: run text_to_paths() (fontTools) and splice
    the returned path parts in, like SKILL.md shows.

Known-correct invariants (each was a real render-breaking bug once):
  - tangents (i/o) are RELATIVE: never translate them when repositioning;
  - shape vertices are stored RELATIVE to the layer anchor; layer position =
    the part's bbox center, so scale() pops around the part's own center;
  - delayed parts clamp hold/fade into the global loop window so the seam
    doesn't pop (CSS staggers the fade too; imperceptible, keeps loops clean).
"""
import json, math, re, sys

NUM = re.compile(r'[-+]?(?:\d+\.\d+|\.\d+|\d+)(?:[eE][-+]?\d+)?')
ARGN = {'M': 2, 'L': 2, 'H': 1, 'V': 1, 'C': 6, 'S': 4, 'Q': 4, 'T': 2, 'Z': 0}
EASINGS = {  # css timing function -> lottie cubic-bezier control points
    'ease-out': ({'x': 0, 'y': 0}, {'x': 0.58, 'y': 1}),
    'ease-in-out': ({'x': 0.42, 'y': 0}, {'x': 0.58, 'y': 1}),
    'ease-in': ({'x': 0.42, 'y': 0}, {'x': 1, 'y': 1}),
    'linear': ({'x': 0, 'y': 0}, {'x': 1, 'y': 1}),
    'ease': ({'x': 0.25, 'y': 0.1}, {'x': 0.25, 'y': 1}),
}

# ---------- svg path -> lottie beziers ----------
def tokenize(d):
    toks, i = [], 0
    while i < len(d):
        c = d[i]
        if c.isalpha():
            if c.upper() not in ARGN:
                raise ValueError('unsupported path cmd %r' % c)
            toks.append(c); i += 1
        elif c in ' \t\r\n,':
            i += 1
        else:
            m = NUM.match(d, i)
            if not m:
                raise ValueError('path syntax at %d: %r' % (i, d[i:i + 12]))
            toks.append(float(m.group())); i = m.end()
    return toks

def beziers(d, mat=(1, 0, 0, 1, 0, 0)):
    """svg path 'd' -> list of subpaths {'v','i','o','c'} in Lottie form
    (absolute vertices, tangents relative to each vertex), matrix-transformed."""
    a, b, c, dm, e, f = mat
    tp = lambda x, y: (a * x + c * y + e, b * x + dm * y + f)
    td = lambda x, y: (a * x + c * y, b * x + dm * y)
    toks = tokenize(d)
    subs, cur = [], None
    newsub = lambda: {'v': [], 'i': [], 'o': [], 'c': False}

    def flush():
        nonlocal cur
        if cur and cur['v']:
            subs.append(cur)
        cur = newsub()

    def seg_v(x, y, iin=(0.0, 0.0)):
        vx, vy = tp(x, y)
        ix, iy = td(*iin)
        cur['v'].append([vx, vy, 0]); cur['o'].append([0, 0, 0]); cur['i'].append([ix, iy, 0])

    def seg_out(cp):
        tox, toy = td(cp[0] - cx, cp[1] - cy)
        cur['o'][-1] = [tox, toy, 0]

    cur = newsub()
    cx = cy = sx = sy = 0.0
    px = py = None
    cmd = None
    pos = 0
    while pos < len(toks):
        t = toks[pos]
        if isinstance(t, str):
            cmd = t; pos += 1
        elif cmd and cmd.upper() == 'M':
            cmd = 'L' if cmd == 'M' else 'l'   # implicit lineto after moveto
        if cmd is None:
            raise ValueError('path starts with a number')
        up = cmd.upper()
        args = [float(v) for v in toks[pos:pos + ARGN[up]]]; pos += ARGN[up]
        if len(args) < ARGN[up]:
            raise ValueError('truncated path')
        R = (lambda x, y: (cx + x, cy + y)) if cmd.islower() else (lambda x, y: (x, y))
        if up == 'M':
            flush()
            cx, cy = R(args[0], args[1]); sx, sy = cx, cy; px = py = None
            seg_v(cx, cy)
        elif up == 'L':
            x, y = R(args[0], args[1])
            seg_v(x, y); cx, cy = x, y
        elif up == 'H':
            x, _ = R(args[0], 0)
            seg_v(x, cy); cx = x
        elif up == 'V':
            _, y = R(0, args[0])
            seg_v(cx, y); cy = y
        elif up == 'C':
            x1, y1 = R(args[0], args[1]); x2, y2 = R(args[2], args[3]); x, y = R(args[4], args[5])
            seg_out((x1, y1)); seg_v(x, y, (x2 - x, y2 - y))
            cx, cy = x, y; px, py = x2, y2
        elif up == 'S':
            x2, y2 = R(args[0], args[1]); x, y = R(args[2], args[3])
            cp1 = (2 * cx - px, 2 * cy - py) if px is not None else (cx, cy)
            seg_out(cp1); seg_v(x, y, (x2 - x, y2 - y))
            cx, cy = x, y; px, py = x2, y2
        elif up == 'Q':
            qx, qy = R(args[0], args[1]); x, y = R(args[2], args[3])
            cp1 = (cx + 2 / 3 * (qx - cx), cy + 2 / 3 * (qy - cy))
            cp2 = (x + 2 / 3 * (qx - x), y + 2 / 3 * (qy - y))
            seg_out(cp1); seg_v(x, y, (cp2[0] - x, cp2[1] - y))
            cx, cy = x, y; px, py = cp2
        elif up == 'T':
            x, y = R(args[0], args[1])
            qx, qy = 2 * cx - (px or cx), 2 * cy - (py or cy)
            cp1 = (cx + 2 / 3 * (qx - cx), cy + 2 / 3 * (qy - cy))
            cp2 = (x + 2 / 3 * (qx - x), y + 2 / 3 * (qy - y))
            seg_out(cp1); seg_v(x, y, (cp2[0] - x, cp2[1] - y))
            cx, cy = x, y; px, py = cp2
        elif up == 'Z':
            cur['c'] = True; cx, cy = sx, sy; px = py = None
    flush()
    return subs

def shape_to_parts(elem_text, tag):
    """rect/circle/ellipse -> path 'd' so ordinary shapes work as parts."""
    at = dict(re.findall(r'([\w-]+)="([^"]*)"', elem_text))
    if tag == 'rect':
        x, y = float(at.get('x', 0)), float(at.get('y', 0))
        w, h = float(at['width']), float(at['height'])
        rx = min(float(at.get('rx', 0) or 0), w / 2, h / 2)
        if rx <= 0:
            return 'M%g %gH%gV%gH%gZ' % (x, y, x + w, y + h, x)
        k = 0.5522847498 * rx
        return ('M%g %gH%gC%g %g %g %g %g %gV%gC%g %g %g %g %g %g'
                'H%gC%g %g %g %g %g %gV%gC%g %g %g %g %g %gZ'
                % (x + rx, y, x + w - rx,
                   x + w - rx + k, y, x + w, y + rx - k, x + w, y + rx,
                   y + h - rx,
                   x + w, y + h - rx + k, x + w - rx + k, y + h, x + w - rx, y + h,
                   x + rx,
                   x + rx - k, y + h, x, y + h - rx + k, x, y + h - rx,
                   y + rx,
                   x, y + rx - k, x + rx - k, y, x + rx, y))
    if tag in ('circle', 'ellipse'):
        cx, cy = float(at['cx']), float(at['cy'])
        rx = float(at['r']) if tag == 'circle' else float(at['rx'])
        ry = rx if tag == 'circle' else float(at['ry'])
        k = 0.5522847498
        return ('M%s %sC%s %s %s %s %s %sC%s %s %s %s %s %sC%s %s %s %s %s %sC%s %s %s %s %s %sZ'
                % (cx + rx, cy,
                   cx + rx, cy + ry * k, cx + rx * k, cy + ry, cx, cy + ry,
                   cx - rx * k, cy + ry, cx - rx, cy + ry * k, cx - rx, cy,
                   cx - rx, cy - ry * k, cx - rx * k, cy - ry, cx, cy - ry,
                   cx + rx * k, cy - ry, cx + rx, cy - ry * k, cx + rx, cy))
    return None

# ---------- text -> paths (fontTools; variable fonts pinned by weight) ----------
def text_to_paths(text, x, y, size, weight=400, spacing=0.0, font_path=None):
    """-> [(char, subs)] with each char's subpaths in final coordinates.
    macOS: /System/Library/Fonts/SFNS.ttf (variable, wght axis)."""
    from fontTools.ttLib import TTFont
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.misc.transform import Transform
    from fontTools.varLib import instancer
    if not font_path:
        for cand in ('/System/Library/Fonts/SFNS.ttf',):
            if os.path.exists(cand):
                font_path = cand
                break
        else:
            raise SystemExit('no system SF font found; pass font_path')
    f = TTFont(font_path)
    if 'fvar' in f:
        instancer.instantiateVariableFont(f, {'wght': weight}, inplace=True)
    s = size / f['head'].unitsPerEm
    cmap = f.getBestCmap(); gs = f.getGlyphSet()
    out, penx = [], x
    for ch in text:
        g = gs[cmap[ord(ch)]]
        spen = SVGPathPen(gs)
        g.draw(TransformPen(spen, Transform(s, 0, 0, -s, penx, y)))
        d = spen.getCommands()
        if d:
            out.append((ch, beziers(d)))
        penx += g.width * s + spacing
    return out

import os  # noqa: E402  (used by text_to_paths default font search)

# ---------- css parsing ----------
def parse_css(css):
    """-> (keyframes: {name: [(pct, {opacity?, scale?, translate?})]},
            part_anim: {duration_s, easing, stagger_s})"""
    kfs = {}
    for m in re.finditer(r'@keyframes\s+([\w-]+)\s*\{((?:[^{}]|\{[^}]*\})*)\}', css):
        name, body = m.group(1), m.group(2)
        stops = []
        for sel, blk in re.findall(r'([\d.]+(?:\s*,\s*[\d.]+)*)%\s*\{([^}]*)\}', body):
            st = {}
            op = re.search(r'opacity:\s*([\d.]+)', blk)
            if op:
                st['opacity'] = float(op.group(1)) * 100
            sc = re.search(r'scale\(([\d.]+)\)', blk)
            if sc:
                st['scale'] = float(sc.group(1)) * 100
            tr = re.search(r'translate\(([-\d.]+)(px)?(?:\s*,\s*([-\d.]+)(px)?)?\)', blk)
            if tr:
                st['translate'] = (float(tr.group(1)), float(tr.group(3) or 0))
            for pct in sel.split(','):
                stops.append((float(pct.strip()), dict(st)))
        stops.sort(key=lambda s: s[0])
        kfs[name] = stops
    anim = {'duration': 5.0, 'easing': 'ease-out', 'stagger': 0.1}
    am = re.search(r'animation:\s*([\w-]+)\s+([\d.]+)s\s+([\w-]+)', css)
    if am:
        anim['duration'] = float(am.group(2))
        anim['easing'] = am.group(3)
    sm = re.search(r'animation-delay:\s*calc\(var\(--i,\s*0\)\s*\*\s*([\d.]+)(ms|s)\)', css)
    if sm:
        anim['stagger'] = float(sm.group(1)) / (1000 if sm.group(2) == 'ms' else 1)
    return kfs, anim

# ---------- lottie assembly ----------
def hexrgb(h):
    h = {'black': '000000', 'white': 'ffffff'}.get(h, h)
    h = h.lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    return [round(int(h[i:i + 2], 16) / 255, 4) for i in (0, 2, 4)]

def bbox(subs):
    xs, ys = [], []
    for s in subs:
        for v, o, i in zip(s['v'], s['o'], s['i']):
            xs += [v[0], v[0] + o[0], v[0] + i[0]]
            ys += [v[1], v[1] + o[1], v[1] + i[1]]
    return min(xs), min(ys), max(xs), max(ys)

def shift(subs, dx, dy):
    for s in subs:
        for p in s['v']:          # vertices only — i/o tangents are relative
            p[0] = round(p[0] + dx, 2); p[1] = round(p[1] + dy, 2)

def kfs_list(vals, ease):
    o, i = EASINGS.get(ease, EASINGS['ease-out'])
    ks = []
    for j, (t, v) in enumerate(vals):
        kf = {'t': t, 's': v}
        if j < len(vals) - 1:
            kf['o'] = dict(o); kf['i'] = dict(i)
        ks.append(kf)
    return {'a': 1, 'k': ks}

def build_comp(name, parts, kf_stops, duration, easing, stagger, fps=60, pad=4):
    """parts: [{'nm','subs','fill','i'}]; kf_stops: [(pct, {opacity?,scale?,translate?})]"""
    N = int(duration * fps)
    for p in parts:
        p.setdefault('bb', bbox(p['subs']))
    gx0 = min(p['bb'][0] for p in parts); gy0 = min(p['bb'][1] for p in parts)
    gx1 = max(p['bb'][2] for p in parts); gy1 = max(p['bb'][3] for p in parts)
    dx, dy = pad - gx0, pad - gy0
    w, h = math.ceil(gx1 - gx0) + 2 * pad, math.ceil(gy1 - gy0) + 2 * pad
    has_scale = any('scale' in st for _, st in kf_stops)
    has_tr = any('translate' in st for _, st in kf_stops)
    layers = []
    for n, p in enumerate(parts, 1):
        shift(p['subs'], dx, dy)                     # svg space -> comp space
        c = ((p['bb'][0] + p['bb'][2]) / 2 + dx, (p['bb'][1] + p['bb'][3]) / 2 + dy)
        shift(p['subs'], -c[0], -c[1])               # recenter: vertices local to anchor
        d0 = p['i'] * stagger * fps
        ovals, svals, pvals = [], [], []

        def add(vals, t, v):
            if vals and vals[-1][0] >= t:      # clamped onto the same frame: keep latest
                vals[-1] = (t, v)
            else:
                vals.append((t, v))

        for pct, st in kf_stops:
            t = round(pct / 100 * N + d0, 2)
            if t > N:
                # loop seam: a delayed stop past the loop end snaps to its
                # GLOBAL (undelayed) time — clamping to N + dedupe would stretch
                # the hold into a slow full-length fade
                t = round(pct / 100 * N, 2)
            if 'opacity' in st:
                add(ovals, t, [st['opacity']])
            if 'scale' in st:
                s = st['scale']; add(svals, t, [s, s, 100])
            if 'translate' in st:
                tx, ty = st['translate']
                add(pvals, t, [round(c[0] + tx, 2), round(c[1] + ty, 2), 0])
        ks = {'o': kfs_list(ovals, easing) if ovals else {'a': 0, 'k': 100},
              'r': {'a': 0, 'k': 0},
              'p': kfs_list(pvals, easing) if pvals else {'a': 0, 'k': [round(c[0], 2), round(c[1], 2), 0]},
              'a': {'a': 0, 'k': [0, 0, 0]},
              's': kfs_list(svals, easing) if svals else {'a': 0, 'k': [100, 100, 100]}}
        shapes = [{'ty': 'sh', 'ks': {'a': 0, 'k': {'c': s['c'], 'v': s['v'], 'i': s['i'], 'o': s['o']}}}
                  for s in p['subs']]
        grp = {'ty': 'gr', 'nm': p['nm'], 'it': shapes + [
            {'ty': 'fl', 'c': {'a': 0, 'k': hexrgb(p['fill']) + [1]}, 'o': {'a': 0, 'k': 100}, 'r': 1, 'nm': 'fill'},
            {'ty': 'tr', 'p': {'a': 0, 'k': [0, 0]}, 'a': {'a': 0, 'k': [0, 0]},
             's': {'a': 0, 'k': [100, 100]}, 'r': {'a': 0, 'k': 0}, 'o': {'a': 0, 'k': 100},
             'sk': {'a': 0, 'k': 0}, 'sa': {'a': 0, 'k': 0}}]}
        layers.append({'ddd': 0, 'ind': n, 'ty': 4, 'nm': p['nm'], 'sr': 1, 'ks': ks,
                       'ao': 0, 'shapes': [grp], 'ip': 0, 'op': N, 'st': 0, 'bm': 0})
    return {'v': '5.7.4', 'fr': fps, 'ip': 0, 'op': N, 'w': w, 'h': h,
            'nm': name, 'ddd': 0, 'assets': [], 'layers': layers, 'markers': []}

# ---------- source extraction ----------
def extract_parts(svg_text, css='', cls='lottie-part'):
    """-> (parts, kf_stops, anim) from an svg string (+ optional css)."""
    if '<style' in svg_text and not css:
        css = '\n'.join(re.findall(r'<style[^>]*>(.*?)</style>', svg_text, re.S))
    kfs, anim = parse_css(css)
    # one keyframes rule drives all parts: the one referenced by the part animation rule
    am = re.search(r'animation:\s*([\w-]+)', css or '')
    kf_name = am.group(1) if am and am.group(1) in kfs else (next(iter(kfs)) if kfs else None)
    kf_stops = kfs.get(kf_name, []) if kf_name else []
    parts = []
    # group blocks first (transform + inherited fill), then bare elements
    for gm in re.finditer(r'<g\b[^>]*>(.*?)</g>', svg_text, re.S):
        gtag, gbody = gm.group(0)[:gm.group(0).index('>') + 1], gm.group(1)
        if cls not in gtag:
            continue
        gat = dict(re.findall(r'([\w-]+)="([^"]*)"', gtag))
        gfill = gat.get('fill')
        gmat = (1, 0, 0, 1, 0, 0)
        tm = re.search(r'transform="translate\(([-\d.]+)[,\s]+([-\d.]+)\)(?:\s+scale\(([\d.]+)\))?"', gtag)
        if tm:
            s = float(tm.group(3) or 1)
            gmat = (s, 0, 0, s, float(tm.group(1)), float(tm.group(2)))
        im = re.search(r'--i:\s*(\d+)', gat.get('style', ''))
        subs = []
        fill = gfill or 'black'
        for pm in re.finditer(r'<(path|rect|circle|ellipse)\b[^>]*>', gbody):
            tag = pm.group(1)
            at = dict(re.findall(r'([\w-]+)="([^"]*)"', pm.group(0)))
            d = at.get('d') or shape_to_parts(pm.group(0), tag)
            if d:
                subs += beziers(d, gmat)
            fill = at.get('fill', fill)
        if subs:
            parts.append({'nm': 'part %s' % (im.group(1) if im else len(parts)),
                          'subs': subs, 'fill': fill, 'i': int(im.group(1)) if im else 0})
    # bare elements: blank out consumed lottie-part <g> blocks first so their
    # children aren't double-counted
    residue = re.sub(r'<g\b[^>]*%s[^>]*>.*?</g>' % cls, '', svg_text, flags=re.S)
    for em in re.finditer(r'<(path|rect|circle|ellipse)\b[^>]*>', residue):
        tag = em.group(1)
        tag_text = em.group(0)
        at = dict(re.findall(r'([\w-]+)="([^"]*)"', tag_text))
        full_cls = at.get('class', '')
        if cls not in full_cls.split():
            continue
        d = at.get('d') or shape_to_parts(tag_text, tag)
        if not d:
            continue
        im = re.search(r'--i:\s*(\d+)', at.get('style', ''))
        parts.append({'nm': 'part %s' % (im.group(1) if im else len(parts)),
                      'subs': beziers(d), 'fill': at.get('fill', 'black'),
                      'i': int(im.group(1)) if im else 0})
    parts.sort(key=lambda p: p['i'])
    return parts, kf_stops, anim

def convert(svg_text, css='', name='animation', fps=60, pad=4, cls='lottie-part'):
    parts, kf_stops, anim = extract_parts(svg_text, css, cls)
    if not parts:
        raise SystemExit('no .%s elements found — tag the animated pieces' % cls)
    if not kf_stops:
        raise SystemExit('no @keyframes found in source css')
    return build_comp(name, parts, kf_stops, anim['duration'], anim['easing'],
                      anim['stagger'], fps=fps, pad=pad)

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('source', help='.svg/.html file (or - for stdin)')
    ap.add_argument('--css', help='css file if keyframes are not in the source')
    ap.add_argument('--out', default='animation.json')
    ap.add_argument('--name', default='animation')
    ap.add_argument('--fps', type=int, default=60)
    ap.add_argument('--pad', type=int, default=4)
    ap.add_argument('--class', dest='cls', default='lottie-part')
    a = ap.parse_args()
    src = sys.stdin.read() if a.source == '-' else open(a.source, encoding='utf-8').read()
    css = open(a.css, encoding='utf-8').read() if a.css else ''
    comp = convert(src, css, a.name, a.fps, a.pad, a.cls)
    json.dump(comp, open(a.out, 'w'), separators=(',', ':'))
    print('%s: %dx%d, %d layers, %.1f KB' % (a.out, comp['w'], comp['h'],
          len(comp['layers']), __import__('os').path.getsize(a.out) / 1024))
