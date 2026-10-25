"""Aggiunge la slide GastroPanel / Istituto Varelli al carosello Linea Gastro (27/10): 6 -> 7 slide."""
import pathlib, shutil, sys
from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright
HERE = pathlib.Path(__file__).resolve().parent
src = (HERE / 'gen_2026-10-26_week.py').read_text().split('def build')[0]
exec(src)
D = HERE.parent / 'img' / '2026-10-27'
TMP = pathlib.Path('/tmp/gp'); TMP.mkdir(exist_ok=True)

def row(a, b):
    return f'<div class="row" style="margin-top:16px"><div><b style="font-size:42px">{a}</b><br><span>{b}</span></div></div>'
inner = ('<div class="eye" style="color:var(--text)"><i></i>GastroPanel · BioHit</div>'
  '<h1 style="font-size:96px;margin-top:26px">GastroPanel, <em>all\'Istituto Varelli.</em></h1>'
  '<p class="lead" style="font-size:34px;margin-top:20px;font-weight:600;color:var(--acc)">Il lettore GP Reader è installato in un centro di eccellenza.</p>'
  '<div style="height:26px"></div>'
  + row('GastroPanel Quick Test NT', 'BioHit · REF 602410')
  + row('GP Reader', 'Il lettore del sistema, installato presso il centro')
  + row('Installazione e formazione', 'Corso per il personale, in sede')
  + '<div style="flex:1"></div>'
  '<div class="pill" style="background:var(--chip);color:var(--title);font-size:22px;padding:22px 34px;align-self:flex-start;text-transform:none;letter-spacing:.04em;font-family:PS;font-weight:600">Istituto Diagnostico Varelli · Soccavo, Napoli</div>'
  '<div style="height:26px"></div>' + foot('6 / 7', 'gp6'))
html6 = page(CW, CH, 'navy', 72, 56, inner)

def shot(b, html, path, w=1080, h=1350, omit=False):
    f = TMP / (pathlib.Path(path).stem + '.html'); f.write_text(html)
    pg = b.new_page(viewport={'width': w, 'height': h}); pg.goto('file://' + str(f)); pg.wait_for_timeout(500)
    pg.screenshot(path=str(path), omit_background=omit); pg.close()

if not (TMP / 'orig_c1.png').exists():
    for i in range(1, 7): Image.open(D / f'c{i}.png').convert('RGB').save(TMP / f'orig_c{i}.png')
orig = {i: Image.open(TMP / f'orig_c{i}.png').convert('RGB') for i in range(1, 7)}

def ink_bbox(im, box, bg):
    c = im.crop(box); diff = ImageChops.difference(c, Image.new('RGB', c.size, bg)).convert('L').point(lambda v: 255 if v > 40 else 0)
    bb = diff.getbbox()
    return None if bb is None else (bb[0] + box[0], bb[1] + box[1], bb[2] + box[0], bb[3] + box[1])

CNT_HTML = ("<!doctype html><html><head><meta charset='utf-8'><style>%s body{background:transparent;margin:0}</style></head><body style='--text:#C9D0EC'>"
            "<div class='cnt' style='position:absolute;left:20px;top:20px;margin:0'>%s</div></body></html>")
with sync_playwright() as p:
    b = p.chromium.launch()
    shot(b, html6, TMP / 'c6new.png')
    out = {1: orig[1]}
    for i in range(2, 7):
        im = orig[i].copy(); n_new = i if i < 6 else 7
        bg = im.getpixel((1050, 1300))
        bb = ink_bbox(im, (860, 1250, 1020, 1345), bg)
        assert bb, i
        # render new counter
        cs = TMP / f'cnt{i}.png'; shot(b, CNT_HTML % (CSS.replace('@@F@@', F), f'{n_new} / 7'), cs, 300, 80, omit=True)
        cim = Image.open(cs).convert('RGBA'); cb = cim.getbbox(); cim = cim.crop(cb)
        pad = 6
        draw_bg = Image.new('RGB', (bb[2] - bb[0] + 2 * pad + 20, bb[3] - bb[1] + 2 * pad), bg)
        im.paste(draw_bg, (bb[2] + pad - draw_bg.width, bb[1] - pad))
        x = bb[2] - cim.width; y = (bb[1] + bb[3]) // 2 - cim.height // 2
        im.paste(cim, (x, y), cim)
        out[i if i < 6 else 7] = im
    b.close()
out[6] = Image.open(TMP / 'c6new.png').convert('RGB')
for i in range(1, 8):
    out[i].save(D / f'c{i}.png')
print('ok')
