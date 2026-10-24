import pathlib, html, sys
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path('/home/claude/social-build')
F = f"file://{ROOT}/node_modules/@fontsource"
P = f"file://{ROOT}/photos"
OUT = ROOT / 'out'

# ---------- photos: trim 3px edge, keep as-is ----------
for f in (ROOT / 'photos').glob('*.png'):
    im = Image.open(f)
    if not f.stem.endswith('_t'):
        pass

CSS = """
@font-face{font-family:'SG';font-weight:700;src:url('@@F@@/space-grotesk/files/space-grotesk-latin-700-normal.woff2')}
@font-face{font-family:'PS';font-weight:400;src:url('@@F@@/ibm-plex-sans/files/ibm-plex-sans-latin-400-normal.woff2')}
@font-face{font-family:'PS';font-weight:600;src:url('@@F@@/ibm-plex-sans/files/ibm-plex-sans-latin-600-normal.woff2')}
@font-face{font-family:'PM';font-weight:600;src:url('@@F@@/ibm-plex-mono/files/ibm-plex-mono-latin-600-normal.woff2')}
*{box-sizing:border-box;margin:0}
body{font-family:'PS';position:relative;overflow:hidden}
.wrap{position:absolute;display:flex;flex-direction:column}
.eye{display:flex;align-items:center;gap:18px;font-family:'PM';font-weight:600;font-size:24px;letter-spacing:.28em;text-transform:uppercase}
.eye i{display:block;width:48px;height:4px;background:var(--acc)}
h1{font-family:'SG';font-weight:700;letter-spacing:-.02em;line-height:1.04;color:var(--title)}
h1 em{font-style:normal;color:var(--acc)}
p.lead{color:var(--text);line-height:1.42}
.panel{background:#fff;border-radius:34px;position:relative;overflow:hidden;display:flex;align-items:center;justify-content:center;gap:18px;padding:26px;box-shadow:0 14px 40px rgba(12,22,51,.10)}
.panel .ph{position:absolute;left:26px;right:26px;top:26px;bottom:26px;display:flex;gap:18px;align-items:center;justify-content:center}
.panel .ph img{flex:1 1 0;min-width:0;height:100%;object-fit:contain}
.panel.cover-fit .ph{left:0;right:0;top:0;bottom:0}
.panel.cover-fit .ph img{object-fit:cover}
.stats{display:flex;gap:16px}
.stat{flex:1;background:var(--chip);border-radius:26px;padding:26px 28px 24px}
.stat b{display:block;font-family:'SG';font-weight:700;font-size:62px;line-height:1;color:var(--statc);letter-spacing:-.02em;white-space:nowrap}
.stat span{display:block;font-family:'PM';font-weight:600;font-size:15px;letter-spacing:.16em;text-transform:uppercase;color:var(--statl);margin-top:12px;line-height:1.35}
.foot{display:flex;align-items:center;gap:16px}
.mk{width:56px;height:56px}
.wm{font-family:'SG';font-weight:700;font-size:38px;line-height:1;color:var(--title)}
.sb{font-family:'PM';font-weight:600;font-size:11px;letter-spacing:.3em;color:var(--acc);margin-top:6px}
.cnt{margin-left:auto;font-family:'PM';font-weight:600;font-size:22px;letter-spacing:.2em;color:var(--text)}
.pill{display:inline-flex;align-items:center;gap:14px;background:var(--pillbg);color:var(--pillfg);font-family:'PM';font-weight:600;font-size:24px;letter-spacing:.2em;padding:24px 42px;border-radius:100px;text-transform:uppercase;align-self:flex-start}
.pill b{color:var(--acc);font-weight:600}
.logo{position:absolute;left:72px;display:flex;align-items:center;gap:20px;background:#fff;border-radius:34px;padding:20px 30px 20px 26px;box-shadow:0 10px 30px rgba(12,22,51,.14)}
.logo .mk{width:64px;height:64px}
.logo .wm{font-size:48px;color:#0C1633}
.logo .sb{font-size:13px}
.chip{display:inline-block;background:var(--chip);color:var(--title);border-radius:100px;font-weight:600;font-size:28px;padding:14px 26px;margin:0 10px 12px 0}
.row{display:flex;align-items:center;gap:26px;background:var(--chip);border-radius:28px;padding:22px 30px}
.row b{font-family:'SG';font-weight:700;color:var(--title);font-size:46px;line-height:1.05}
.row span{color:var(--text);font-size:30px;line-height:1.3}
.num{font-family:'SG';font-weight:700;color:var(--acc);font-size:60px;min-width:84px}
table{border-collapse:separate;border-spacing:0 12px;width:100%}
td,th{padding:34px 14px;text-align:center;background:var(--chip);font-size:42px;color:var(--title);font-family:'SG';font-weight:700}
th{background:transparent;font-size:30px;vertical-align:bottom}
td:first-child{text-align:left;border-radius:24px 0 0 24px;font-family:'PM';font-weight:600;font-size:17px;letter-spacing:.16em;text-transform:uppercase;color:var(--statl);width:210px;padding-left:26px}
td:last-child{border-radius:0 24px 24px 0}
th img{height:150px;display:block;margin:0 auto 10px;object-fit:contain;background:#fff;border-radius:22px;padding:8px;width:100%}
"""

THEMES = {
 'light': dict(bg='#F4F6FC', title='#0C1633', text='#4A5478', acc='#FF2E5B', chip='#FFFFFF', statc='#0C1633', statl='#7079A0', pillbg='#0C1633', pillfg='#fff'),
 'navy':  dict(bg='#0C1633', title='#FFFFFF', text='#C9D0EC', acc='#FF6E8E', chip='#16224A', statc='#FFFFFF', statl='#FF9DB4', pillbg='#fff', pillfg='#0C1633'),
 'pink':  dict(bg='#FFF1F4', title='#0C1633', text='#5A4A64', acc='#E8184A', chip='#FFFFFF', statc='#E8184A', statl='#7C6A86', pillbg='#0C1633', pillfg='#fff'),
 'blue':  dict(bg='linear-gradient(165deg,#0E2156 0%,#1D3F9E 100%)', title='#FFFFFF', text='#D5DCF5', acc='#FF8FA9', chip='rgba(255,255,255,.12)', statc='#FFFFFF', statl='#FFC2D0', pillbg='#fff', pillfg='#0C1633'),
 'white': dict(bg='#FFFFFF', title='#0C1633', text='#4A5478', acc='#FF2E5B', chip='#F4F6FC', statc='#FF2E5B', statl='#7079A0', pillbg='#0C1633', pillfg='#fff'),
}

def vars_(t):
    th = THEMES[t]
    return ';'.join(f'--{k}:{v}' for k, v in th.items() if k != 'bg')

def mark(uid):
    s = ''.join(f'<rect y="{i*10}" width="100" height="5" fill="#FF2E5B"/>' for i in range(10))
    return f'<svg class="mk" viewBox="0 0 100 100"><defs><clipPath id="c{uid}"><rect width="100" height="100" rx="30"/></clipPath></defs><g clip-path="url(#c{uid})"><rect width="100" height="100" fill="#0E2156"/>{s}</g></svg>'

def foot(cnt='', uid='f'):
    return f'<div class="foot">{mark(uid)}<div><div class="wm">Reagenta</div><div class="sb">CLINICAL SOLUTIONS</div></div><div class="cnt">{cnt}</div></div>'

def logo_card(top, uid='l'):
    return f'<div class="logo" style="top:{top}px">{mark(uid)}<div><div class="wm">Reagenta</div><div class="sb">CLINICAL SOLUTIONS</div></div></div>'

def imgs(names, style=''):
    return ''.join(f'<img src="{P}/{n}.png" style="{style}">' for n in names)

PHOTO_BG = {'ave661': '#A0A0A0'}
def panel(names, h=None, flex=True, cover=False, extra=''):
    cover = False
    st = 'flex:1;' if flex else ''
    if len(names) == 1 and names[0] in PHOTO_BG:
        st += f'background:{PHOTO_BG[names[0]]};'
    if h: st += f'height:{h}px;'
    cls = 'panel cover-fit' if cover else 'panel'
    return f'<div class="{cls}" style="{st}{extra}"><div class="ph">{imgs(names)}</div></div>'

def page(w, h, theme, top, bottom, inner, left=72, extra_abs=''):
    bg = THEMES[theme]['bg']
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS.replace("@@F@@", F)}'
            f'body{{width:{w}px;height:{h}px;background:{bg}}} '
            f'.wrap{{left:{left}px;right:{left}px;top:{top}px;bottom:{bottom}px}}</style></head>'
            f'<body style="{vars_(theme)}">{extra_abs}<div class="wrap">{inner}</div></body></html>')

ARROW = '<svg width="34" height="26" viewBox="0 0 34 26"><path d="M2 13h28M20 3l10 10-10 10" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>'

# ----------------- carousel slide builders (1080x1350) -----------------
CW, CH = 1080, 1350

def s_cover(theme, eyebrow, title, sub, photos, n, N):
    inner = (f'<div class="eye" style="color:var(--text)"><i></i>{eyebrow}</div>'
             f'<h1 style="font-size:104px;margin-top:30px">{title}</h1>'
             f'<p class="lead" style="font-size:36px;margin-top:26px;max-width:900px">{sub}</p>'
             f'<div style="height:34px"></div>' + panel(photos) +
             f'<div style="height:34px"></div><div class="foot">{mark("c"+str(n))}<div><div class="wm">Reagenta</div><div class="sb">CLINICAL SOLUTIONS</div></div>'
             f'<div class="pill" style="margin-left:auto;padding:18px 32px;font-size:20px;gap:12px">Scorri {ARROW}</div></div>')
    return page(CW, CH, theme, 72, 72, inner)

def s_product(theme, n, N, brand, name, tag, stats, text, photo, cover=False, name_size=92):
    st = ''.join(f'<div class="stat"><b>{a}</b><span>{b}</span></div>' for a, b in stats)
    inner = (f'<div class="eye" style="color:var(--text)"><i></i>{brand}</div>'
             f'<h1 style="font-size:{name_size}px;margin-top:22px">{name}</h1>'
             f'<p class="lead" style="font-size:34px;margin-top:14px;font-weight:600;color:var(--acc)">{tag}</p>'
             f'<div style="height:28px"></div>' + panel([photo], cover=cover) +
             f'<div style="height:26px"></div><div class="stats">{st}</div>'
             f'<p class="lead" style="font-size:28px;margin-top:22px">{text}</p>'
             f'<div style="height:22px"></div>' + foot(f'{n} / {N}', 'p' + str(n)))
    return page(CW, CH, theme, 64, 56, inner)

def s_compare(theme, n, N, title, cols, rows):
    head = '<tr><th></th>' + ''.join(f'<th><img src="{P}/{ph}.png">{nm}</th>' for ph, nm in cols) + '</tr>'
    body = ''.join('<tr><td>' + r[0] + '</td>' + ''.join(f'<td>{c}</td>' for c in r[1:]) + '</tr>' for r in rows)
    inner = (f'<div class="eye" style="color:var(--text)"><i></i>A confronto</div>'
             f'<h1 style="font-size:88px;margin-top:26px">{title}</h1><div style="height:24px"></div>'
             f'<table>{head}{body}</table><div style="flex:1"></div>' + foot(f'{n} / {N}', 'q' + str(n)))
    return page(CW, CH, theme, 72, 64, inner)

def s_chips(theme, n, N, title, groups, photo):
    g = ''
    for lab, items in groups:
        g += (f'<div style="font-family:PM;font-weight:600;font-size:20px;letter-spacing:.26em;color:var(--acc);text-transform:uppercase;margin:30px 0 16px">{lab}</div>'
              + '<div>' + ''.join(f'<span class="chip">{i}</span>' for i in items) + '</div>')
    inner = (f'<div class="eye" style="color:var(--text)"><i></i>AVE-562</div>'
             f'<h1 style="font-size:84px;margin-top:24px">{title}</h1>{g}<div style="flex:1"></div>'
             + panel([photo], h=330, flex=False) + '<div style="height:26px"></div>' + foot(f'{n} / {N}', 'k' + str(n)))
    return page(CW, CH, theme, 72, 56, inner)

def s_duo(theme, n, N, brand, title, photos, items):
    it = ''.join(f'<div class="row" style="margin-top:16px"><div><b>{a}</b><br><span>{b}</span></div></div>' for a, b in items)
    inner = (f'<div class="eye" style="color:var(--text)"><i></i>{brand}</div>'
             f'<h1 style="font-size:92px;margin-top:24px">{title}</h1><div style="height:26px"></div>'
             + panel(photos) + f'<div style="height:10px"></div>{it}<div style="height:26px"></div>' + foot(f'{n} / {N}', 'd' + str(n)))
    return page(CW, CH, theme, 72, 56, inner)

def s_guide(theme, n, N, title, rows, photos=None):
    r = ''.join(f'<div class="row" style="margin-top:16px;align-items:flex-start"><div class="num" style="font-size:48px;min-width:0;width:40px">›</div><div><b>{a}</b><br><span>{b}</span></div></div>' for a, b in rows)
    inner = (f'<div class="eye" style="color:var(--text)"><i></i>La guida</div>'
             f'<h1 style="font-size:92px;margin-top:26px">{title}</h1><div style="height:18px"></div>{r}<div style="height:24px"></div>' + (panel(photos) if photos else '<div style="flex:1"></div>') + '<div style="height:26px"></div>'
             + foot(f'{n} / {N}', 'g' + str(n)))
    return page(CW, CH, theme, 72, 64, inner)

def s_cta(theme, n, N, title, photos):
    aud = ''.join(f'<span class="chip" style="font-size:30px">{a}</span>' for a in ['Laboratori', 'Distributori', 'Farmacie'])
    card = ('<div style="background:var(--pillbg);border-radius:34px;padding:40px 48px;color:var(--pillfg);display:flex;gap:40px;align-items:center">'
            '<div><div style="font-family:PM;font-weight:600;font-size:18px;letter-spacing:.28em;color:#FF2E5B;text-transform:uppercase">Richiedi la tua offerta</div>'
            '<div style="font-family:SG;font-weight:700;font-size:46px;margin-top:10px">reagenta.it/quotazione</div></div>'
            '<div style="font-size:26px;line-height:1.5;opacity:.8;margin-left:auto;text-align:right">081 8045042<br>ordini@reagenta.it</div></div>')
    inner = (f'<div class="eye" style="color:var(--text)"><i></i>Offerte dedicate</div>'
             f'<h1 style="font-size:98px;margin-top:26px">{title}</h1>'
             f'<p class="lead" style="font-size:32px;margin-top:18px">Prezzi riservati ai clienti: condizioni dedicate per</p>'
             f'<div style="margin-top:18px">{aud}</div><div style="height:16px"></div>' + panel(photos) +
             f'<div style="height:26px"></div>{card}<div style="height:26px"></div>' + foot(f'{n} / {N}', 'z' + str(n)))
    return page(CW, CH, theme, 72, 56, inner)

# ----------------- story builders (1080x1920) -----------------
SW, SH = 1080, 1920

def st_hero(theme, eyebrow, title, sub, photo, cover=False, extra_bottom=''):
    inner = (f'<div style="height:190px"></div>' + panel([photo], cover=cover) +
             f'<div style="height:44px"></div><div class="eye" style="color:var(--text)"><i></i>{eyebrow}</div>'
             f'<h1 style="font-size:108px;margin-top:22px">{title}</h1>'
             f'<p class="lead" style="font-size:40px;margin-top:20px">{sub}</p>{extra_bottom}')
    return page(SW, SH, theme, 250, 250, inner, extra_abs=logo_card(250))

def st_quiz(theme, eyebrow, title, photo, opts, cta):
    o = ''.join(f'<div class="row" style="margin-top:18px"><div class="num" style="font-size:54px">{a}</div><div><b style="font-size:42px">{b}</b><br><span style="font-size:28px">{c}</span></div></div>' for a, b, c in opts)
    inner = (f'<div style="height:190px"></div><div class="eye" style="color:var(--text)"><i></i>{eyebrow}</div>'
             f'<h1 style="font-size:100px;margin-top:22px">{title}</h1><div style="height:30px"></div>'
             + panel([photo], h=360, flex=False) + f'<div style="height:10px"></div>{o}<div style="flex:1"></div>'
             f'<div class="pill" style="font-size:22px;padding:22px 36px">{cta}</div>')
    return page(SW, SH, theme, 250, 250, inner, extra_abs=logo_card(250))

def st_tech(theme, eyebrow, title, items, cta):
    o = ''.join(f'<div class="row" style="margin-top:18px;padding:16px 24px"><img src="{P}/{ph}.png" style="width:210px;height:150px;object-fit:contain;background:#fff;border-radius:20px;padding:6px"><div><b style="font-size:54px;color:var(--acc)">{a}</b><br><span style="font-size:32px;font-weight:600;color:var(--title)">{b}</span></div></div>' for ph, a, b in items)
    inner = (f'<div style="height:190px"></div><div class="eye" style="color:var(--text)"><i></i>{eyebrow}</div>'
             f'<h1 style="font-size:104px;margin-top:22px">{title}</h1><div style="height:24px"></div>{o}<div style="flex:1"></div>'
             f'<div class="pill" style="font-size:22px;padding:22px 36px">{cta}</div>')
    return page(SW, SH, theme, 250, 250, inner, extra_abs=logo_card(250))

def st_offer(theme, eyebrow, title, sub, photos, cta, aud=True):
    a = ''
    if aud:
        a = ''.join(f'<div class="row" style="margin-top:14px;padding:18px 28px"><b style="font-size:42px">{x}</b><span style="margin-left:auto;font-size:28px">{y}</span></div>' for x, y in [('Laboratori', 'prezzi riservati'), ('Distributori', 'condizioni dedicate'), ('Farmacie', 'offerte dedicate')])
    inner = (f'<div style="height:190px"></div>' + panel(photos, h=(520 if len(photos)==1 else 440), flex=False) +
             f'<div style="height:40px"></div><div class="eye" style="color:var(--text)"><i></i>{eyebrow}</div>'
             f'<h1 style="font-size:98px;margin-top:20px">{title}</h1>'
             f'<p class="lead" style="font-size:36px;margin-top:16px">{sub}</p><div style="height:14px"></div>{a}<div style="flex:1"></div>'
             f'<div class="pill" style="font-size:22px;padding:22px 36px">{cta}</div>')
    return page(SW, SH, theme, 250, 250, inner, extra_abs=logo_card(250))


def build():
    out = {}
    CTA = 'Richiedi la tua offerta'
    # ===================== LUN 26 — VES (light) =====================
    d = '2026-10-26'; N = 6
    out[f'{d}/c1'] = (CW, CH, s_cover('light', 'Famiglia VES · ALCOR', 'VES da sangue intero in <em>15–20 secondi.</em>', 'miniiSED, iSED e iSED PRO: tre analizzatori, tre modi di lavorare.', ['miniised', 'ised', 'isedpro'], 1, N))
    out[f'{d}/c2'] = (CW, CH, s_product('light', 2, N, 'ALCOR · VES', 'miniiSED', 'Il VES compatto, sempre pronto sul banco.', [('15 s', 'per risultato'), ('180', 'test / ora'), ('1', 'campione a bordo')], 'Sangue intero in provetta EDTA primaria, senza preparazione. 100 µL aspirati per test.', 'miniised'))
    out[f'{d}/c3'] = (CW, CH, s_product('light', 3, N, 'ALCOR · VES', 'iSED', 'Accesso casuale e caricamento continuo.', [('~20 s', 'per campione'), ('180', 'test / ora'), ('20', 'posizioni campione')], 'Provette caricabili anche tappate. Collegamento al LIS via LAN e RS232.', 'ised'))
    out[f'{d}/c4'] = (CW, CH, s_product('light', 4, N, 'ALCOR · VES', 'iSED PRO', 'Per il laboratorio che non può rallentare.', [('275', 'test / ora'), ('120', 'campioni a bordo'), ('1–130', 'mm/h range')], 'LIS bidirezionale con lettore barcode integrato. Risultato in mm/h correlato con il Westergren.', 'isedpro'))
    out[f'{d}/c5'] = (CW, CH, s_compare('light', 5, N, 'Quale scegliere? <em>Dipende dai campioni.</em>', [('miniised', 'miniiSED'), ('ised', 'iSED'), ('isedpro', 'iSED PRO')], [('Test / ora', '180', '180', '275'), ('Campioni a bordo', '1', '20', '120'), ('Risposta', '~15 s', '~20 s', '~20 s'), ('Volume aspirato', '100 µL', '100 µL', '100 µL')]))
    out[f'{d}/c6'] = (CW, CH, s_cta('light', 6, N, 'Il VES giusto <em>per il tuo volume.</em>', ['miniised', 'ised', 'isedpro']))
    out[f'{d}/s1'] = (SW, SH, st_hero('light', 'VES · ALCOR', 'Il VES che sta <em>sul banco.</em>', 'miniiSED: 15 secondi a risultato, 180 test l\'ora.', 'miniised'))
    out[f'{d}/s2'] = (SW, SH, st_quiz('light', 'Quiz', 'Quanti VES <em>al giorno?</em>', 'isedpro', [('A', 'Meno di 50', 'miniiSED'), ('B', '50–150', 'iSED'), ('C', 'Oltre 150', 'iSED PRO · 275 test/ora')], 'Rispondi in DM: ti consigliamo il modello'))
    out[f'{d}/s3'] = (SW, SH, st_offer('light', 'Test rapidi CiTest', 'Test rapidi: <em>offerte per chi ordina.</em>', 'Sangue occulto fecale e molti altri: scegli dal catalogo.', ['tfob'], CTA))
    # ===================== MAR 27 — Linea Gastro (navy) =====================
    d = '2026-10-27'; N = 6
    out[f'{d}/c1'] = (CW, CH, s_cover('navy', 'Linea Gastro', 'Il laboratorio feci, <em>automatizzato.</em>', 'Microscopia con intelligenza artificiale, test rapidi integrati e lettori quantitativi.', ['ave562', 'ave661'], 1, N))
    out[f'{d}/c2'] = (CW, CH, s_product('navy', 2, N, 'Ave · Linea Gastro', 'AVE-562', 'Microscopia, IA e test rapidi in un unico flusso.', [('90', 'test / ora'), ('40', 'campioni a bordo'), ('200', 'cuvette')], 'Posizione STAT per le urgenze, memoria da 200.000 record, integrazione LIS e HIS.', 'ave562'))
    out[f'{d}/c3'] = (CW, CH, s_chips('navy', 3, N, 'Cosa riconosce <em>e cosa legge.</em>', [('Elementi corpuscolati', ['Eritrociti', 'Leucociti', 'Cellule epiteliali', 'Cristalli', 'Lieviti', 'Funghi', 'Granuli di amido', 'Globuli di grasso', 'Uova di parassiti']), ('Test rapidi integrati', ['Sangue occulto', 'Transferrina', 'Calprotectina', 'Lattoferrina', 'H. pylori', 'Rotavirus', 'Adenovirus'])], 'ave562'))
    out[f'{d}/c4'] = (CW, CH, s_product('navy', 4, N, 'Ave · Microscopia con IA', 'AVE-661', 'Oltre 78 tipi di elementi. Tu validi.', [('60', 'test / ora'), ('78+', 'tipologie'), ('&lt;3 ml', 'di campione')], 'Urine, feci, secrezioni vaginali e liquidi biologici. Ingrandimenti 10x, 20x, 40x, immagini multilayer da 5 Mpx.', 'ave661', cover=True))
    out[f'{d}/c5'] = (CW, CH, s_duo('navy', 5, N, 'Eurospital · Linea Gastro', 'Calprotectina, elastasi, <em>FOB.</em>', ['euturbo', 'eufast'], [('Eu-Turbo Analyzer', 'Calprotectina, elastasi pancreatica e FOB'), ('Eu-Fast Reader', 'Lettore automatico di test rapidi quantitativi')]))
    out[f'{d}/c6'] = (CW, CH, s_cta('navy', 6, N, 'Automatizza <em>il tuo laboratorio feci.</em>', ['ave562', 'ave661', 'euturbo']))
    out[f'{d}/s1'] = (SW, SH, st_hero('navy', 'AVE-661 · Microscopia con IA', 'Oltre 78 tipi <em>di elementi.</em>', 'Lo strumento riconosce, tu validi le immagini.', 'ave661', cover=True))
    out[f'{d}/s2'] = (SW, SH, st_hero('navy', 'AVE-562 · Linea Gastro', '90 test l\'ora. <em>Un solo flusso.</em>', 'Microscopia, IA e test rapidi: FOB, calprotectina, H. pylori.', 'ave562'))
    out[f'{d}/s3'] = (SW, SH, st_offer('navy', 'Kit chirurgici completi', 'Il campo operatorio, <em>già pronto.</em>', 'Kit universale sterile monouso: teli, salviette e sacco mayo.', ['kitchir'], 'Richiedi la quotazione', aud=False))
    # ===================== MER 28 — Breath test (pink) =====================
    d = '2026-10-28'; N = 7
    out[f'{d}/c1'] = (CW, CH, s_cover('pink', 'Breath test', 'Un respiro. <em>Molte risposte.</em>', 'Lattosio, SIBO e H. pylori: quattro strumenti per il tuo ambulatorio.', ['gastroplus', 'wld500'], 1, N))
    out[f'{d}/c2'] = (CW, CH, s_product('pink', 2, N, 'Bedfont · Breath test', 'Gastro+ Gastrolyzer', 'Portatile, a idrogeno, pronto in un attimo.', [('60', 'test / ora'), ('10', 'profili paziente'), ('24–48h', 'assistenza tecnica')], 'H₂ per intolleranza al lattosio e SIBO. Boccagli SteriBreath, CE-IVD.', 'gastroplus', name_size=80))
    out[f'{d}/c3'] = (CW, CH, s_product('pink', 3, N, 'FAN · Breath test', 'LactoFAN 2', 'Touchscreen che si usa anche con i guanti.', [('1–6', 'pazienti a bordo'), ('4×AA', 'batterie'), ('0 min', 'di preriscaldamento')], 'H₂ per lattosio, fruttosio, sorbitolo, saccarosio, SIBO e transito oro-cecale. Autoreset e calibrazione semiautomatica.', 'lactofan2'))
    out[f'{d}/c4'] = (CW, CH, s_product('pink', 4, N, 'Bedfont · Breath test', 'GastroCH4ECK', 'H₂, CH₄ e O₂ nello stesso respiro.', [('80', 'test / ora'), ('≤45 s', 'risposta'), ('±10%', 'accuratezza')], 'Per SIBO e malassorbimento di lattosio e fruttosio. Sensore CH₄ laser da 0 a 200 ppm.', 'gastroch4eck'))
    out[f'{d}/c5'] = (CW, CH, s_product('pink', 5, N, 'Wanlianda · Breath test', 'WLD500', 'H. pylori con ¹³C-urea, senza radiazioni.', [('25', 'coppie / ora'), ('~140 s', 'per coppia'), ('NDIR', 'tecnologia')], 'Rapporto isotopico 13CO₂/12CO₂ su campione basale e post-somministrazione. USB, LAN e COM.', 'wld500'))
    out[f'{d}/c6'] = (CW, CH, s_guide('pink', 6, N, 'Quale strumento <em>per quale quesito?</em>', [('Lattosio e SIBO', 'Gastro+ · LactoFAN 2 · GastroCH4ECK'), ('SIBO con metano', 'GastroCH4ECK: H₂, CH₄ e O₂'), ('H. pylori', 'WLD500 con ¹³C-urea'), ('Hai dubbi?', 'Scrivici: scegliamo insieme')], ['gastroplus', 'lactofan2', 'gastroch4eck', 'wld500']))
    out[f'{d}/c7'] = (CW, CH, s_cta('pink', 7, N, 'Porta il breath test <em>nel tuo ambulatorio.</em>', ['gastroplus', 'lactofan2', 'wld500']))
    out[f'{d}/s1'] = (SW, SH, st_hero('pink', 'Gastro+ · Bedfont', 'Lattosio e SIBO, <em>in un respiro.</em>', 'Portatile, 60 test l\'ora, boccagli SteriBreath.', 'gastroplus'))
    out[f'{d}/s2'] = (SW, SH, st_hero('pink', 'WLD500 · Wanlianda', 'H. pylori senza <em>radiazioni.</em>', '¹³C-urea, NDIR, 25 coppie l\'ora.', 'wld500'))
    out[f'{d}/s3'] = (SW, SH, st_offer('pink', 'Test rapido CiTest', 'H. pylori: <em>lettura in 5 minuti.</em>', 'Kit da 25 test su feci, conservazione 2–30 °C.', ['tphylori'], CTA))
    # ===================== GIO 29 — Immunodiagnostica (blue) =====================
    d = '2026-10-29'; N = 7
    out[f'{d}/c1'] = (CW, CH, s_cover('blue', 'Immunodiagnostica', 'Dal monotest all\'<em>accesso casuale.</em>', 'CLIA, CLEIA, ECLIA ed ELISA: cinque analizzatori per ogni volume di lavoro.', ['autolumo', 'cobas', 'lumipulse'], 1, N))
    out[f'{d}/c2'] = (CW, CH, s_product('blue', 2, N, 'Autobio · CLIA', 'Autolumo S900', 'CLIA ad accesso casuale.', [('180', 'test / ora'), ('150+', 'parametri'), ('19 min', 'al primo risultato')], '51 posizioni campione di cui 3 STAT, fino a 16 test simultanei per campione.', 'autolumo', name_size=88))
    out[f'{d}/c3'] = (CW, CH, s_product('blue', 3, N, 'Fujirebio · CLEIA', 'Lumipulse G1200', 'CLEIA con cartucce monotest.', [('120', 'test / ora'), ('100', 'campioni a bordo'), ('24', 'saggi per campione')], 'Separazione magnetica e caricamento continuo: un risultato ogni 30 secondi dopo il primo.', 'lumipulse', name_size=88))
    out[f'{d}/c4'] = (CW, CH, s_product('blue', 4, N, 'Roche · ECLIA', 'cobas e 411', 'ECLIA con priorità STAT.', [('86', 'test / ora'), ('100+', 'metodiche'), ('9 min', 'alcune applicazioni')], '30 campioni (Disk) o 75 (Rack), 18 posizioni reagenti, rilevamento di livello e coaguli.', 'cobas'))
    out[f'{d}/c5'] = (CW, CH, s_product('blue', 5, N, 'Diesse · ELISA monotest', 'Chorus Trio', 'ELISA monotest per l\'autoimmunità.', [('30', 'test / ora'), ('30', 'saggi per seduta'), ('150+', 'test disponibili')], 'Dispositivi da 12 o 36 con reagenti già inclusi, riconosciuti da barcode. ANA, ENA, anti-CCP, anti-dsDNA.', 'chorus'))
    out[f'{d}/c6'] = (CW, CH, s_product('blue', 6, N, 'Assure Tech · CLIA monotest', 'Lumicision CLI1000', 'CLIA monotest, multidisciplinare.', [('CLIA', 'monotest'), ('Multi', 'disciplinare'), ('Pronta', 'consegna')], 'Chiedi il menu dei test disponibili e il pannello dedicato Lumicision.', 'lumicision', name_size=84))
    out[f'{d}/c7'] = (CW, CH, s_cta('blue', 7, N, 'Scegli l\'analizzatore <em>giusto per te.</em>', ['autolumo', 'lumipulse', 'cobas']))
    out[f'{d}/s1'] = (SW, SH, st_hero('blue', 'Autolumo S900 · CLIA', '19 minuti al <em>primo risultato.</em>', '180 test l\'ora e oltre 150 parametri.', 'autolumo'))
    out[f'{d}/s2'] = (SW, SH, st_tech('blue', 'Quiz', 'ECLIA, CLEIA <em>o CLIA?</em>', [('cobas', 'ECLIA', 'cobas e 411'), ('lumipulse', 'CLEIA', 'Lumipulse G1200'), ('autolumo', 'CLIA', 'Autolumo S900')], 'Scrivici in DM: scegliamo insieme'))
    out[f'{d}/s3'] = (SW, SH, st_offer('blue', 'Per i distributori', 'Rivendi sul territorio? <em>Condizioni dedicate.</em>', '60+ produttori, 5.700+ referenze, spedizione tracciata 24/48h.', ['tfob', 'tphylori'], 'Apri il conto B2B su reagenta.it', aud=False))
    # ===================== VEN 30 — HbA1c / elettroforesi (white) =====================
    d = '2026-10-30'; N = 5
    out[f'{d}/c1'] = (CW, CH, s_cover('white', 'Diabetologia ed emoglobinopatie', 'HbA1c ed emoglobine: <em>HPLC</em> ed elettroforesi.', 'Due analizzatori HPLC Lifotronic e l\'elettroforesi automatica Futurlab.', ['h8', 'h100', 'fe26'], 1, N))
    out[f'{d}/c2'] = (CW, CH, s_product('white', 2, N, 'Lifotronic · HPLC', 'Lifotronic H8', 'HPLC per HbA1c e varianti emoglobiniche.', [('130 s', 'per HbA1c'), ('10', 'posizioni campione'), ('≤1,5%', 'CV dichiarato')], 'HbA1c 3–18%, HbF, HbA2 e varianti HbE, HbD, HbS, HbC. NGSP e IFCC dichiarate dal produttore.', 'h8'))
    out[f'{d}/c3'] = (CW, CH, s_product('white', 3, N, 'Lifotronic · HPLC · da esposizione', 'Lifotronic H100', 'Nuovo da esposizione, mai utilizzato.', [('96 s', 'per HbA1c'), ('110', 'campioni (o 50)'), ('10,1″', 'touchscreen')], 'Modalità HbA1c e β-talassemia, memoria da 20.000 risultati, USB, LAN e COM. Chiedi la quotazione.', 'h100'))
    out[f'{d}/c4'] = (CW, CH, s_product('white', 4, N, 'Futurlab · Elettroforesi', 'FE26 Agarose Gel', 'Elettroforesi su agarosio, tutto automatico.', [('26', 'campioni per ciclo'), ('45 min', 'per ciclo (sieroproteine)'), ('6', 'frazioni')], 'Applicazione, migrazione, colorazione ed essiccazione automatiche, densitometria integrata, software GEMINI.', 'fe26', name_size=82))
    out[f'{d}/c5'] = (CW, CH, s_cta('white', 5, N, 'Dal diabete alle talassemie, <em>un solo partner.</em>', ['h8', 'h100', 'fe26']))
    out[f'{d}/s1'] = (SW, SH, st_hero('white', 'Lifotronic H100 · da esposizione', 'Mai utilizzato, <em>da esposizione.</em>', 'HPLC per HbA1c: 96 secondi a test.', 'h100'))
    out[f'{d}/s2'] = (SW, SH, st_hero('white', 'FE26 · Futurlab', '26 campioni, <em>un solo ciclo.</em>', 'Elettroforesi su agarosio completamente automatica.', 'fe26'))
    out[f'{d}/s3'] = (SW, SH, st_offer('white', 'Buon weekend da Reagenta', 'Offerte per <em>tutti i profili.</em>', 'Test rapidi, strumenti e kit chirurgici: scrivici.', ['tfob', 'tphylori', 'kitchir'], 'reagenta.it/quotazione'))
    return out


if __name__ == '__main__':
    only = sys.argv[1:]
    items = build()
    with sync_playwright() as p:
        b = p.chromium.launch()
        for key, (w, h, html_) in items.items():
            if only and not any(key.startswith(o) or key == o for o in only):
                continue
            d, name = key.split('/')
            (OUT / d).mkdir(parents=True, exist_ok=True)
            f = OUT / d / f'{name}.html'
            f.write_text(html_)
            pg = b.new_page(viewport={'width': w, 'height': h})
            pg.goto('file://' + str(f)); pg.wait_for_timeout(500)
            pg.screenshot(path=str(OUT / d / f'{name}.png')); pg.close()
            print(key)
        b.close()
