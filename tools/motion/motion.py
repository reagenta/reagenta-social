#!/usr/bin/env python3
"""Motion-graphics reel engine for Reagenta (voice-over by Susi, scenes synced to ASR word times).
usage: motion.py <spec_id> [preview_t ...]
"""
import numpy as np, math, subprocess, sys, json, functools, difflib, re, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from scipy.io import wavfile
from scipy.signal import butter, lfilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
A = '/tmp/reagenta_assets/'
WD = '/home/claude/work/'
W, H, FPS = 1080, 1920, 30
NAVY = (10, 26, 87); MAG = (255, 46, 99); WHITE = (255, 255, 255); SKY = (120, 190, 255); SOFT = (200, 214, 255)
IB = '/usr/share/fonts/opentype/inter/InterDisplay-Black.otf'
IX = '/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf'
IM = '/usr/share/fonts/opentype/inter/Inter-Medium.otf'
IS = '/usr/share/fonts/opentype/inter/Inter-SemiBold.otf'
COL = {'white': WHITE, 'mag': MAG, 'sky': SKY, 'soft': SOFT, 'navy': NAVY}


@functools.lru_cache(None)
def font(p, s): return ImageFont.truetype(p, s)


logo_l = Image.open(A + 'logo_light.png').convert('RGBA')
@functools.lru_cache(None)
def logo_w(w): return logo_l.resize((w, int(w * logo_l.height / logo_l.width)), Image.LANCZOS)


def ease(x): x = max(0, min(1, x)); return 1 - (1 - x) ** 3
def eio(x): x = max(0, min(1, x)); return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2
def back(x):
    x = max(0, min(1, x)); c = 1.70158; return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2


def over(im, L, x, y):
    x, y = int(x), int(y)
    sx = max(0, -x); sy = max(0, -y); ex = min(L.width, W - x); ey = min(L.height, H - y)
    if ex <= sx or ey <= sy: return
    im.alpha_composite(L.crop((sx, sy, ex, ey)), (x + sx, y + sy))


def fadeL(L, a):
    if a >= 0.999: return L
    r, g, b, al = L.split(); al = al.point(lambda v: int(v * a)); return Image.merge('RGBA', (r, g, b, al))


yy, xx = np.mgrid[0:H, 0:W]

# ---------- themes ----------
THEMES = {
    'ecm':      dict(c0=(7, 16, 58),  c1=(18, 40, 120), acc=(255, 46, 99),  sec=(120, 190, 255), o2=(40, 100, 255), ink=(255, 255, 255), bg='orbs',    trans='wipe',    txt='rise',  card='right', row='left',  rc=48, rr=40, chip=34, rs=50, accpos='left'),
    'prean':    dict(c0=(4, 34, 44),  c1=(8, 92, 98),   acc=(255, 176, 32), sec=(120, 240, 200), o2=(0, 170, 160),  ink=(20, 30, 40),    bg='grid',    trans='push',    txt='slide', card='left',  row='right', rc=20, rr=18, chip=16, rs=22, accpos='top'),
    'ves':      dict(c0=(44, 6, 28),  c1=(112, 18, 62), acc=(0, 222, 255),  sec=(255, 170, 190), o2=(210, 40, 90),  ink=(10, 20, 40),    bg='rings',   trans='iris',    txt='zoom',  card='zoom',  row='zoom',  rc=70, rr=59, chip=34, rs=50, accpos='bottom'),
    'resp':     dict(c0=(14, 18, 30), c1=(44, 54, 80),  acc=(70, 226, 190), sec=(190, 205, 235), o2=(90, 110, 170), ink=(10, 24, 30),    bg='stripes', trans='blinds',  txt='drop',  card='up',    row='left',  rc=16, rr=14, chip=12, rs=16, accpos='left'),
    's900':     dict(c0=(18, 6, 56),  c1=(64, 26, 150), acc=(190, 255, 60), sec=(150, 220, 255), o2=(140, 60, 255), ink=(20, 14, 50),    bg='beams',   trans='zoom',    txt='zoom',  card='right', row='up',    rc=40, rr=34, chip=34, rs=50, accpos='top'),
    'assist':   dict(c0=(6, 10, 22),  c1=(18, 32, 56),  acc=(255, 96, 52),  sec=(255, 205, 120), o2=(255, 96, 52),  ink=(255, 255, 255), bg='radar',   trans='push_up', txt='slide', card='up',    row='right', rc=30, rr=26, chip=22, rs=30, accpos='left'),
    'rischio':  dict(c0=(24, 6, 10),  c1=(86, 14, 24),  acc=(255, 214, 0),  sec=(255, 150, 90),  o2=(220, 30, 40),  ink=(30, 10, 10),    bg='hazard',  trans='wipe',    txt='drop',  card='zoom',  row='left',  rc=14, rr=12, chip=10, rs=14, accpos='bottom'),
    'hp':       dict(c0=(5, 34, 24),  c1=(14, 92, 62),  acc=(255, 112, 92), sec=(170, 255, 150), o2=(30, 190, 110), ink=(255, 255, 255), bg='bubbles', trans='iris',    txt='rise',  card='left',  row='up',    rc=64, rr=55, chip=34, rs=50, accpos='top'),
    'campania': dict(c0=(2, 30, 72),  c1=(8, 112, 170), acc=(255, 204, 40), sec=(150, 225, 255), o2=(0, 170, 230),  ink=(8, 30, 60),     bg='waves',   trans='push',    txt='fade',  card='zoom',  row='right', rc=36, rr=30, chip=34, rs=40, accpos='left'),
    'turni':    dict(c0=(34, 20, 8),  c1=(104, 58, 20), acc=(80, 214, 255), sec=(255, 205, 150), o2=(220, 120, 40), ink=(10, 24, 40),    bg='diamonds', trans='blinds', txt='slide', card='right', row='zoom',  rc=24, rr=20, chip=18, rs=24, accpos='bottom'),
}
TH = THEMES['ecm']
RC, RR, CHR, RS, ACCPOS, INK = 48, 40, 34, 50, 'left', (255, 255, 255)
TXT, CARDIN, ROWIN, TRANS, BGSTYLE = 'rise', 'right', 'left', 'wipe', 'orbs'


def make_base(c0, c1):
    yy, xx = np.mgrid[0:H, 0:W]
    g = (yy / H)[..., None]
    c0 = np.array(c0, np.float32); c1 = np.array(c1, np.float32)
    base = c0 * (1 - g) + c1 * g
    dots_ = ((xx % 54 < 3) & (yy % 54 < 3)).astype(np.float32)[..., None]
    dotfade = np.clip(1 - np.abs(yy - H * 0.45) / (H * 0.5), 0, 1)[..., None]
    base = base + dots_ * dotfade * 30
    return Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert('RGBA')


def orb(sz, col, al):
    yy2, xx2 = np.mgrid[0:sz, 0:sz]; r = np.hypot(xx2 - sz / 2, yy2 - sz / 2) / (sz / 2)
    a = np.clip(1 - r, 0, 1) ** 2 * al
    arr = np.zeros((sz, sz, 4), np.uint8); arr[..., 0], arr[..., 1], arr[..., 2] = col; arr[..., 3] = a.astype(np.uint8)
    return Image.fromarray(arr)


prng = np.random.default_rng(11)
PART = [(prng.uniform(0, W), prng.uniform(0, H), prng.uniform(0.04, 0.12), prng.uniform(2, 5), prng.uniform(0, 6.28)) for _ in range(46)]
BASE = None; ORB_M = None; ORB_B = None
_bgc = {}


def apply_theme(name):
    global TH, MAG, SKY, COL, BASE, ORB_M, ORB_B, RC, RR, CHR, RS, ACCPOS, INK, TXT, CARDIN, ROWIN, TRANS, BGSTYLE
    TH = THEMES[name]
    MAG = TH['acc']; SKY = TH['sec']; INK = TH['ink']
    COL = {'white': WHITE, 'mag': MAG, 'sky': SKY, 'soft': SOFT, 'navy': NAVY}
    BASE = make_base(TH['c0'], TH['c1'])
    ORB_M = orb(1000, TH['acc'], 80 if name != 'ecm' else 95); ORB_B = orb(1100, TH['o2'], 85)
    RC, RR, CHR, RS, ACCPOS = TH['rc'], TH['rr'], TH['chip'], TH['rs'], TH['accpos']
    TXT, CARDIN, ROWIN, TRANS, BGSTYLE = TH['txt'], TH['card'], TH['row'], TH['trans'], TH['bg']
    _bgc.clear()


apply_theme('ecm')


def bg_overlay(style, tt, d, L):
    a_ = TH['acc']; s_ = TH['sec']
    if style == 'grid':
        for k in range(-1, 24):
            y = int((k * 96 - tt * 36) % (H + 96)) - 96
            d.line([0, y, W, y], fill=s_ + (34,), width=2)
        for k in range(0, 13): d.line([k * 90, 0, k * 90, H], fill=s_ + (20,), width=2)
        for k in range(3):
            y = int((tt * 150 + k * 640) % (H + 200)) - 100
            d.rectangle([0, y, W, y + 6], fill=a_ + (40,))
    elif style == 'rings':
        for k in range(8):
            r = (tt * 110 + k * 170) % 1360
            al = int(max(0, 1 - r / 1360) * 90)
            d.ellipse([W / 2 - r, 1250 - r, W / 2 + r, 1250 + r], outline=a_ + (al,), width=4)
        for k in range(3):
            r = 140 + k * 70; d.ellipse([W / 2 - r, 330 - r, W / 2 + r, 330 + r], outline=s_ + (26,), width=2)
    elif style == 'stripes':
        off = (tt * 40) % 240
        for k in range(-4, 16):
            x0 = k * 240 + off
            d.polygon([(x0, 0), (x0 + 80, 0), (x0 - 520 + 80, H), (x0 - 520, H)], fill=(255, 255, 255, 12))
        d.rectangle([0, 1650, W, 1654], fill=a_ + (90,)); d.rectangle([0, 100, 140, 106], fill=a_ + (160,))
    elif style == 'beams':
        for k in range(6):
            x = 90 + k * 180 + 60 * math.sin(tt * 0.7 + k * 1.3); w = 70 + 40 * math.sin(tt * 0.9 + k)
            d.polygon([(x, 0), (x + w, 0), (x + w * 2.4 - 120, H), (x - 120, H)], fill=(a_ if k % 2 else s_) + (22,))
    elif style == 'radar':
        cx, cy = W / 2, 1000
        for k in range(1, 6): d.ellipse([cx - k * 200, cy - k * 200, cx + k * 200, cy + k * 200], outline=s_ + (30,), width=2)
        d.line([cx - 1100, cy, cx + 1100, cy], fill=s_ + (24,), width=2); d.line([cx, cy - 1100, cx, cy + 1100], fill=s_ + (24,), width=2)
        ang = (tt * 70) % 360
        for j in range(18): d.pieslice([cx - 1100, cy - 1100, cx + 1100, cy + 1100], ang - j * 2 - 2, ang - j * 2, fill=a_ + (int(48 * (1 - j / 18)),))
    elif style == 'hazard':
        off = (tt * 60) % 120
        for k in range(-2, 12):
            x0 = k * 120 + off
            d.polygon([(x0, 0), (x0 + 60, 0), (x0 + 20, 96), (x0 - 40, 96)], fill=a_ + (150,))
            d.polygon([(x0, H - 96), (x0 + 60, H - 96), (x0 + 20, H), (x0 - 40, H)], fill=a_ + (150,))
        for k in range(6): d.line([0, 300 + k * 210, W, 300 + k * 210 - 160], fill=(255, 255, 255, 12), width=2)
    elif style == 'bubbles':
        for k in range(18):
            x = (k * 193) % W + 30 * math.sin(tt * 0.8 + k); r = 24 + (k * 37) % 70
            y = (H + 100) - ((tt * (40 + (k * 13) % 50) + k * 211) % (H + 200))
            d.ellipse([x - r, y - r, x + r, y + r], outline=s_ + (60,), width=3, fill=s_ + (12,))
    elif style == 'waves':
        for k in range(7):
            pts = [(x, 1250 + k * 70 + 28 * math.sin(x / 150 + tt * 1.3 + k * 0.8)) for x in range(0, W + 30, 30)]
            d.line(pts, fill=(a_ if k == 3 else s_) + (70 if k == 3 else 38,), width=4 if k == 3 else 3)
        for k in range(4):
            pts = [(x, 330 + k * 50 + 18 * math.sin(x / 120 - tt + k)) for x in range(0, W + 30, 30)]
            d.line(pts, fill=s_ + (22,), width=2)
    elif style == 'diamonds':
        off = (tt * 28) % 160
        for r_ in range(-1, 14):
            for c_ in range(-1, 8):
                cx = c_ * 160 + (80 if r_ % 2 else 0) + off - 80; cy = r_ * 150 + 40
                d.polygon([(cx, cy - 60), (cx + 60, cy), (cx, cy + 60), (cx - 60, cy)], outline=s_ + (22,))


def bg(t, off=0.0):
    k = (int((t + off) * 15), off)
    if k in _bgc: return _bgc[k].copy()
    tt = k[0] / 15.0
    im = BASE.copy()
    over(im, ORB_M, -300 + 90 * math.sin(tt * 0.5), 1050 + 120 * math.cos(tt * 0.4))
    over(im, ORB_B, 400 + 80 * math.cos(tt * 0.45), -250 + 90 * math.sin(tt * 0.35))
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    bg_overlay(BGSTYLE, tt, d, L)
    im.alpha_composite(L)
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for x, y, v, r, ph in PART:
        py = (y - tt * v * H * 0.6) % H; px = x + 14 * math.sin(tt + ph); a = int(90 * (0.5 + 0.5 * math.sin(tt * 1.5 + ph)))
        d.ellipse([px - r, py - r, px + r, py + r], fill=(255, 255, 255, a))
    im.alpha_composite(L)
    if len(_bgc) > 6: _bgc.clear()
    _bgc[k] = im
    return im.copy()


@functools.lru_cache(None)
def glass(w, h, r, fill=(255, 255, 255, 30), outline=(255, 255, 255, 80), accent=None, accpos='left'):
    S = 2; L = Image.new('RGBA', (w * S, h * S), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rounded_rectangle([0, 0, w * S - 1, h * S - 1], radius=r * S, fill=fill, outline=outline, width=2 * S)
    d.rounded_rectangle([r * S * 0.6, 3 * S, w * S - r * S * 0.6, 6 * S], radius=3 * S, fill=(255, 255, 255, 40))
    if accent:
        if accpos == 'left': d.rounded_rectangle([0, r * S * 0.5, 8 * S, h * S - r * S * 0.5], radius=4 * S, fill=accent)
        elif accpos == 'top': d.rounded_rectangle([r * S * 0.5, 0, w * S - r * S * 0.5, 9 * S], radius=4 * S, fill=accent)
        else: d.rounded_rectangle([r * S * 0.5, h * S - 9 * S, w * S - r * S * 0.5, h * S], radius=4 * S, fill=accent)
    return L.resize((w, h), Image.LANCZOS)


_tmpd = ImageDraw.Draw(Image.new('RGBA', (10, 10)))
def tw_(txt, f): return _tmpd.textlength(txt, font=f)


@functools.lru_cache(None)
def text_layer(parts, fp, fs, w=W, pad=8):
    f = font(fp, fs)
    tws = [tw_(t, f) for t, c in parts]; tw = sum(tws); h = int(fs * 1.6)
    L = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(L); x = (w - tw) / 2
    for (t, c), twi in zip(parts, tws):
        d.text((x, pad), t, font=f, fill=c + (255,)); x += twi
    return L


def parse(txt, base_col):
    out = []
    for i, seg in enumerate(txt.split('*')):
        if seg: out.append((seg, MAG if i % 2 else base_col))
    return tuple(out)


def fit_size(lines, fp, size, maxw=960):
    s = size
    for ln in lines:
        w = sum(tw_(t, font(fp, s)) for t, c in ln)
        if w > maxw: s = min(s, int(s * maxw / w))
    return s


def reveal(im, parts, y, fp, fs, t, t0, dur=0.6, idx=0):
    k = ease((t - t0) / dur)
    if k <= 0: return
    L = text_layer(parts, fp, fs); h = L.height
    if TXT == 'rise':
        tmp = Image.new('RGBA', (W, h), (0, 0, 0, 0)); tmp.paste(L, (0, int((1 - k) * h * 0.9)))
        over(im, fadeL(tmp, min(1, k * 1.6)), 0, y)
    elif TXT == 'drop':
        tmp = Image.new('RGBA', (W, h), (0, 0, 0, 0)); tmp.paste(L, (0, -int((1 - k) * h * 0.9)))
        over(im, fadeL(tmp, min(1, k * 1.6)), 0, y)
    elif TXT == 'slide':
        dx = int((1 - k) * 360) * (1 if idx % 2 == 0 else -1)
        over(im, fadeL(L, min(1, k * 1.6)), dx, y)
    elif TXT == 'zoom':
        sc = 1 + 0.45 * (1 - k); Lr = L.resize((int(W * sc), int(h * sc)), Image.BILINEAR)
        over(im, fadeL(Lr, min(1, k * 1.6)), -(Lr.width - W) / 2, y - (Lr.height - h) / 2)
    else:
        over(im, fadeL(L, k), 0, y + int((1 - k) * 18))


def enter(pl, L, x, y, mode, t, t0, dist=520):
    k = back((t - t0) / 0.5)
    if k <= 0: return
    a = ease((t - t0) / 0.3); kk = min(1.0, k)
    if mode == 'right': over(pl, fadeL(L, a), x + (1 - kk) * dist, y)
    elif mode == 'left': over(pl, fadeL(L, a), x - (1 - kk) * dist, y)
    elif mode == 'up': over(pl, fadeL(L, a), x, y + (1 - kk) * 420)
    else:
        sc = max(0.3, 0.55 + 0.45 * min(k, 1.06)); Lr = L.resize((int(L.width * sc), int(L.height * sc)), Image.BILINEAR)
        over(pl, fadeL(Lr, a), x + (L.width - Lr.width) / 2, y + (L.height - Lr.height) / 2)


# ---------- items ----------
def it_height(it):
    t = it['t']
    if t == 'chip': return 68 + 34
    if t == 'title':
        n = len(it['text'].split('|')); return n * int(it.get('size', 92) * 1.12) + 22
    if t == 'sub':
        n = len(it['text'].split('|')); return n * int(it.get('size', 44) * 1.35) + 14
    if t == 'stamp': return 100 + 40
    if t == 'card':
        n = len(it['label'].split('|')); nf = it.get('size', 140)
        return int(nf * 1.2) + 18 + n * 50 + 34 + 30
    if t == 'row': return 118 + 22
    if t == 'gap': return it['h']
    return 0


def draw_chip(pl, it, t, t0, y):
    a = ease((t - t0) / 0.4)
    if a <= 0: return
    f = font(IS, 32); txt = it['text']; tw = tw_(txt, f)
    gl = glass(int(tw + 72), 68, CHR, fill=(255, 255, 255, 34)); L = Image.new('RGBA', gl.size); L.alpha_composite(gl)
    ImageDraw.Draw(L).text((36, 15), txt, font=f, fill=WHITE + (255,))
    over(pl, fadeL(L, a), W / 2 - gl.width / 2, y + int((1 - a) * 20))


def draw_title(pl, it, t, t0, y):
    col = COL[it.get('col', 'white')]; lines = [parse(l, col) for l in it['text'].split('|')]
    size = fit_size(lines, IB, it.get('size', 92))
    for i, ln in enumerate(lines):
        reveal(pl, ln, y + i * int(size * 1.12), IB, size, t, t0 + i * 0.16, idx=i)


def draw_sub(pl, it, t, t0, y):
    col = COL[it.get('col', 'soft')]; lines = [parse(l, col) for l in it['text'].split('|')]
    size = fit_size(lines, IM if it.get('w', 'm') == 'm' else IX, it.get('size', 44))
    for i, ln in enumerate(lines):
        reveal(pl, ln, y + i * int(size * 1.35), IM if it.get('w', 'm') == 'm' else IX, size, t, t0 + i * 0.14, idx=i)


def draw_stamp(pl, it, t, t0, y):
    k = back((t - t0) / 0.5)
    if k <= 0: return
    fill = COL[it.get('fill', 'mag')]; tcol = TH['c0'] if it.get('fill') == 'sky' else INK
    f = font(IB, it.get('size', 46)); tw = tw_(it['text'], f); w = int(tw + 90)
    L = Image.new('RGBA', (w, 100), (0, 0, 0, 0)); L.alpha_composite(glass(w, 100, RS, fill=fill + (235,), outline=(255, 255, 255, 150)))
    ImageDraw.Draw(L).text((45, 24), it['text'], font=f, fill=tcol + (255,))
    sc = max(0.2, min(k, 1.05)); L = L.resize((int(L.width * sc), int(L.height * sc)), Image.LANCZOS)
    over(pl, fadeL(L, ease((t - t0) / 0.3)), W / 2 - L.width / 2, y + 50 - L.height // 2)


@functools.lru_cache(None)
def card_img(num, label, nf, accent):
    lines = label.split('|'); h = int(nf * 1.2) + 18 + len(lines) * 50 + 34
    while tw_(num, font(IB, nf)) > 760: nf -= 6
    L = Image.new('RGBA', (860, h), (0, 0, 0, 0)); L.alpha_composite(glass(860, h, RC, accent=accent, accpos=ACCPOS))
    d = ImageDraw.Draw(L); d.text((52, 14), num, font=font(IB, nf), fill=WHITE + (255,))
    ly = 14 + int(nf * 1.2) + 4
    for i, l in enumerate(lines): d.text((56, ly + i * 50), l, font=font(IM, 40), fill=SOFT + (255,))
    return L


def draw_card(pl, it, t, t0, y):
    L = card_img(it['num'], it['label'], it.get('size', 140), COL[it.get('accent', 'mag')] + (255,))
    enter(pl, L, 110, y, CARDIN, t, t0)


@functools.lru_cache(None)
def row_img(n, text):
    L = Image.new('RGBA', (860, 118), (0, 0, 0, 0)); L.alpha_composite(glass(860, 118, RR))
    d = ImageDraw.Draw(L)
    if RR >= 30: d.ellipse([28, 24, 98, 94], fill=MAG + (255,))
    else: d.rounded_rectangle([28, 24, 98, 94], radius=14, fill=MAG + (255,))
    fn = font(IB, 46); d.text((63 - tw_(n, fn) / 2, 27), n, font=fn, fill=INK + (255,))
    s = 40
    while tw_(text, font(IS, s)) > 700: s -= 2
    d.text((126, 59 - int(s * 0.64)), text, font=font(IS, s), fill=WHITE + (255,))
    return L


def draw_row(pl, it, t, t0, y):
    L = row_img(it['n'], it['text'])
    enter(pl, L, 110, y, ROWIN, t, t0, dist=620)


DRAW = {'chip': draw_chip, 'title': draw_title, 'sub': draw_sub, 'stamp': draw_stamp, 'card': draw_card, 'row': draw_row}


# ---------- wipes ----------
U = {
    'diag': ((xx + 0.35 * yy) / (W + 0.35 * H)).astype(np.float32),
    'up': (1 - yy / H).astype(np.float32),
    'left': (xx / W).astype(np.float32),
    'diag_r': ((W - xx + 0.35 * yy) / (W + 0.35 * H)).astype(np.float32),
}
STYLES = ['diag', 'up', 'left', 'diag_r']
def wipe(out, inn, p, style):
    Uf = U[style]; bw = 0.14; q = -bw + (1 + bw) * eio(p)
    o = np.asarray(out.convert('RGB')).astype(np.float32); n = np.asarray(inn.convert('RGB')).astype(np.float32)
    m_in = (Uf < q)[..., None]; band = ((Uf >= q) & (Uf < q + bw))[..., None]
    res = np.where(m_in, n, o)
    mag = np.array(MAG, np.float32); edge = (((Uf >= q) & (Uf < q + 0.012))[..., None])
    res = np.where(band, mag, res); res = np.where(edge, 255.0, res)
    return Image.fromarray(res.astype(np.uint8))



def _clip(x): return max(0.0, min(1.0, x))
def trans(kind, out, inn, p, style):
    q = eio(p)
    if kind == 'wipe': return wipe(out, inn, p, style)
    out = out.convert('RGB'); inn = inn.convert('RGB')
    if kind in ('push', 'push_up'):
        cv = Image.new('RGB', (W, H)); d = ImageDraw.Draw(cv)
        if kind == 'push':
            sh = int(q * W); cv.paste(out, (-sh, 0)); cv.paste(inn, (W - sh, 0)); d.rectangle([W - sh - 5, 0, W - sh + 5, H], fill=MAG)
        else:
            sh = int(q * H); cv.paste(out, (0, -sh)); cv.paste(inn, (0, H - sh)); d.rectangle([0, H - sh - 5, W, H - sh + 5], fill=MAG)
        return cv
    if kind == 'iris':
        r = q * 1250; m = Image.new('L', (W, H), 0); d = ImageDraw.Draw(m); d.ellipse([W / 2 - r, H / 2 - r, W / 2 + r, H / 2 + r], fill=255)
        cv = Image.composite(inn, out, m)
        if 0 < q < 1: ImageDraw.Draw(cv).ellipse([W / 2 - r, H / 2 - r, W / 2 + r, H / 2 + r], outline=MAG, width=12)
        return cv
    if kind == 'blinds':
        nb = 12; bh = H / nb; m = Image.new('L', (W, H), 0); d = ImageDraw.Draw(m); cv_edges = []
        for i in range(nb):
            lp = _clip(q * 1.7 - i * 0.06)
            if lp > 0: d.rectangle([0, i * bh, W, i * bh + lp * bh], fill=255)
        cv = Image.composite(inn, out, m); d2 = ImageDraw.Draw(cv)
        for i in range(nb):
            lp = _clip(q * 1.7 - i * 0.06)
            if 0 < lp < 1: d2.rectangle([0, i * bh + lp * bh - 4, W, i * bh + lp * bh], fill=MAG)
        return cv
    # zoom
    so = 1 + 0.10 * q; si = 1.14 - 0.14 * q
    o2 = out.resize((int(W * so), int(H * so)), Image.BILINEAR).crop((int(W * (so - 1) / 2), int(H * (so - 1) / 2), int(W * (so - 1) / 2) + W, int(H * (so - 1) / 2) + H))
    i2 = inn.resize((int(W * si), int(H * si)), Image.BILINEAR).crop((int(W * (si - 1) / 2), int(H * (si - 1) / 2), int(W * (si - 1) / 2) + W, int(H * (si - 1) / 2) + H))
    cv = Image.blend(o2, i2, q); fl = math.sin(math.pi * q) * 0.28
    return Image.blend(cv, Image.new('RGB', (W, H), MAG), fl) if fl > 0.01 else cv


# ---------- timing ----------
def norm(w): return re.sub(r"[^a-zàèéìòù0-9]", '', w.lower())
def find_anchor(words, text, cursor):
    toks = [norm(x) for x in text.split() if norm(x)]
    for i in range(cursor, len(words)):
        if difflib.SequenceMatcher(None, norm(words[i][0]), toks[0]).ratio() >= 0.72:
            ok = True
            if len(toks) > 1 and i + 1 < len(words):
                ok = difflib.SequenceMatcher(None, norm(words[i + 1][0]), toks[1]).ratio() >= 0.55
            if ok: return i
    raise SystemExit(f'anchor not found: "{text}" after word {cursor}: {" ".join(w[0] for w in words[cursor:cursor+8])}')


def build(spec):
    words = json.load(open(spec['asr']))
    scenes = []; cur = 0
    for sc in spec['scenes']:
        a = find_anchor(words, sc['at'], cur if scenes else 0) if sc['at'] else 0
        cur = max(cur, a)
        st = 0.0 if not scenes else max(0.0, words[a][1] - 0.05)
        its = []; icur = a; ioff = {}
        total = sum(it_height(x) for x in sc['items'])
        y = sc.get('y', max(330, int(900 - total / 2) + sc.get('dy', 0)))
        for it in sc['items']:
            if it['t'] == 'gap': y += it['h']; continue
            if 'at' in it:
                j = find_anchor(words, it['at'], icur); icur = j; t0 = words[j][1] + it.get('dt', 0.0)
            else:
                t0 = st + 0.25 + len(its) * 0.5 if not scenes or True else 0
                if sc['at']:
                    t0 = words[a][1] + 0.1 + sum(1 for x in its if 'at' not in x) * 0.45
            its.append((it, t0, y)); y += it_height(it)
        scenes.append({'st': st, 'items': its, 'foot': sc.get('foot', spec.get('foot')), 'style': STYLES[len(scenes) % 4]})
    vend = words[-1][2]
    ostart = vend + 0.7
    END = ostart + 3.8
    return scenes, ostart, END, words


# ---------- scene frames ----------
def make_renderer(spec, scenes, ostart, END):
    def base_frame(t, hdr=True):
        im = bg(t)
        if hdr: over(im, fadeL(logo_w(340), ease(t / 0.5)), (W - 340) // 2, 150)
        return im

    def foot(im, lines, t):
        if t > 1.0 and lines:
            fs = 25
            while max(tw_(x, font(IM, fs)) for x in lines) > 980: fs -= 1
            for j, txt in enumerate(lines):
                L = text_layer(((txt, (190, 205, 255)),), IM, fs)
                over(im, fadeL(L, ease((t - 1.0) / 0.5) * 0.9), 0, (1506, 1546)[j])

    def scene_img(i, t):
        sc = scenes[i]; im = base_frame(t); pl = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        for it, t0, y in sc['items']:
            if t >= t0: DRAW[it['t']](pl, it, t, t0, y)
        im.alpha_composite(pl); foot(im, sc['foot'], t)
        pw = int(W * (t / END)); ImageDraw.Draw(im).rounded_rectangle([0, 1596, pw, 1604], radius=4, fill=MAG + (255,))
        return im.convert('RGB')

    def outro_img(t):
        lt = max(0, t - ostart); im = bg(t, 20)
        s = 0.75 + 0.25 * back(lt / 0.8); lw = int(820 * s); lg = logo_w(lw); a = ease(lt / 0.4)
        G = Image.new('RGBA', (lw + 300, lg.height + 300), (0, 0, 0, 0)); ImageDraw.Draw(G).ellipse([40, 100, G.width - 40, G.height - 100], fill=MAG + (60,))
        over(im, fadeL(G.filter(ImageFilter.GaussianBlur(60)), a), (W - G.width) // 2, 690 + lg.height // 2 - G.height // 2)
        over(im, fadeL(lg, a), (W - lw) // 2, 690)
        reveal(im, (('Soluzioni per la', WHITE),), 960, IX, 56, lt, 0.6)
        reveal(im, (('diagnostica di laboratorio', WHITE),), 1030, IX, 56, lt, 0.75)
        k = back((lt - 1.3) / 0.5)
        if k > 0:
            f = font(IS, 40); tw = tw_('reagenta.it', f)
            pl = Image.new('RGBA', (int(tw + 110), 84), (0, 0, 0, 0)); ImageDraw.Draw(pl).rounded_rectangle([0, 0, pl.width - 1, 83], radius=42, fill=MAG + (255,))
            ImageDraw.Draw(pl).text((55, 16), 'reagenta.it', font=f, fill=INK + (255,))
            over(im, fadeL(pl, min(1, k)), (W - pl.width) // 2, 1190)
        if lt > 1.8:
            L = text_layer((('Voce generata con IA', (190, 205, 255)),), IM, 28)
            over(im, fadeL(L, ease((lt - 1.8) / 0.5) * 0.9), 0, 1330)
        return im.convert('RGB')

    n = len(scenes)
    starts = [s['st'] for s in scenes] + [ostart]

    def frame(t):
        # find current segment
        seg = 0
        for j in range(1, n + 1):
            if t >= starts[j] - 0.15: seg = j
        if seg == n:
            if t < ostart + 0.30:
                p = (t - (ostart - 0.15)) / 0.45
                return trans(TRANS, scene_img(n - 1, t), outro_img(ostart), p, STYLES[n % 4])
            return outro_img(t)
        if seg > 0 and t < starts[seg] + 0.30:
            p = (t - (starts[seg] - 0.15)) / 0.45
            return trans(TRANS, scene_img(seg - 1, t), scene_img(seg, starts[seg]), p, scenes[seg]['style'])
        return scene_img(seg, t)
    return frame


# ---------- audio ----------
SR = 44100
rg = np.random.default_rng(7)
def whoosh(dur=0.5):
    n = int(dur * SR); noise = rg.standard_normal(n); out = np.zeros(n); seg = 16
    for s in range(0, n, n // seg):
        e = s + n // seg; fc = 400 + 3500 * (s / n) ** 1.5
        b, a = butter(2, [fc * 0.6 / (SR / 2), min(0.95, fc * 1.4 / (SR / 2))], 'band'); out[s:e] = lfilter(b, a, noise[s:e])
    env = np.sin(np.linspace(0, np.pi, n)) ** 2; out *= env; return out / np.max(np.abs(out)) * 0.5
def pop(f0=700):
    n = int(0.12 * SR); t = np.arange(n) / SR; f = f0 * np.exp(-t * 18) + 200
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 30) * 0.6
def ding():
    n = int(1.2 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 1320 * t) + 0.5 * np.sin(2 * np.pi * 1980 * t)) * np.exp(-t * 4) * 0.3


def make_audio(spec, scenes, ostart, END):
    N = int(END * SR); aud = np.zeros(N)
    def add(t0, x, gn=1.0):
        i = int(t0 * SR); j = min(N, i + len(x)); aud[i:j] += gn * x[:j - i]
    k = 0
    for i, sc in enumerate(scenes):
        if i > 0: add(sc['st'] - 0.15, whoosh(0.45), 0.7)
        for it, t0, y in sc['items']:
            add(t0, pop(520 + 30 * (k % 5)), 0.55); k += 1
    add(ostart - 0.15, whoosh(0.45), 0.7); add(ostart + 0.8, ding(), 0.8)
    aud = np.tanh(aud * 1.1); sfx = aud / max(1e-6, np.max(np.abs(aud))) * 0.55
    p = WD + f"out/{spec['id']}_sfx.wav"
    wavfile.write(p, SR, (sfx * 32767).astype(np.int16))
    mix = WD + f"out/{spec['id']}_mix.wav"
    fc = ('[0:a]aresample=44100,aformat=channel_layouts=mono,highpass=f=80,aecho=0.85:0.5:25|48:0.10|0.06,loudnorm=I=-16:TP=-1.5:LRA=7,apad=whole_dur=%s[v];'
          '[1:a]aformat=channel_layouts=mono,volume=0.40[s];[v][s]amix=inputs=2:duration=first:normalize=0,aformat=channel_layouts=stereo[m]') % END
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', spec['voice'], '-i', p, '-filter_complex', fc, '-map', '[m]', '-t', str(END), mix], check=True)
    return mix


def main():
    from specs import SPECS
    spec = SPECS[sys.argv[1]]; only = [float(x) for x in sys.argv[2:]]
    apply_theme(spec.get('theme', 'ecm'))
    scenes, ostart, END, words = build(spec)
    json.dump({'scenes': [s['st'] for s in scenes], 'outro': ostart, 'end': END}, open(WD + f"out/{spec['id']}.times.json", 'w'))
    print(spec['id'], 'scenes at', [round(s['st'], 1) for s in scenes], 'outro', round(ostart, 1), 'END', round(END, 1), flush=True)
    frame = make_renderer(spec, scenes, ostart, END)
    if only:
        for o in only: frame(o).save(WD + f"out/{spec['id']}_{o}.png")
        return
    mix = make_audio(spec, scenes, ostart, END)
    outp = WD + f"out/{spec['id']}.mp4"
    nf = int(END * FPS)
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-i', mix, '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '24', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k',
                          '-shortest', '-movflags', '+faststart', outp], stdin=subprocess.PIPE)
    for i in range(nf): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('done', outp, nf, flush=True)


if __name__ == '__main__':
    main()
