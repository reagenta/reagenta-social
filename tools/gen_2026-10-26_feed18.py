import pathlib, html
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path('/home/claude/social-build')
F = f"file://{ROOT}/node_modules/@fontsource"
OUT = pathlib.Path(__file__).resolve().parent.parent / 'img' / '2026-10-26'
OUT.mkdir(parents=True, exist_ok=True)

CSS = f"""
@font-face{{font-family:'SG';font-weight:700;src:url('{F}/space-grotesk/files/space-grotesk-latin-700-normal.woff2')}}
@font-face{{font-family:'PS';font-weight:400;src:url('{F}/ibm-plex-sans/files/ibm-plex-sans-latin-400-normal.woff2')}}
@font-face{{font-family:'PS';font-weight:600;src:url('{F}/ibm-plex-sans/files/ibm-plex-sans-latin-600-normal.woff2')}}
@font-face{{font-family:'PM';font-weight:600;src:url('{F}/ibm-plex-mono/files/ibm-plex-mono-latin-600-normal.woff2')}}
*{{box-sizing:border-box;margin:0}}
body{{width:1080px;height:1350px;font-family:'PS';position:relative;overflow:hidden;background:var(--bg);color:var(--text)}}
.wrap{{position:absolute;left:72px;right:72px;top:72px;bottom:72px;display:flex;flex-direction:column}}
.eye{{display:flex;align-items:center;gap:18px;font-family:'PM';font-weight:600;font-size:24px;letter-spacing:.28em;text-transform:uppercase;color:var(--text)}}
.eye i{{display:block;width:48px;height:4px;background:var(--acc)}}
h1{{font-family:'SG';font-weight:700;letter-spacing:-.02em;line-height:1.04;color:var(--title)}}
h1 em{{font-style:normal;color:var(--acc)}}
p{{line-height:1.42;color:var(--text)}}
.foot{{display:flex;align-items:center;gap:16px;margin-top:auto}}
.mk{{width:56px;height:56px}}
.wm{{font-family:'SG';font-weight:700;font-size:38px;line-height:1;color:var(--title)}}
.sb{{font-family:'PM';font-weight:600;font-size:11px;letter-spacing:.3em;color:var(--acc);margin-top:6px}}
.contact{{margin-left:auto;font-family:'PM';font-weight:600;font-size:22px;letter-spacing:.12em;color:var(--text)}}
.head{{display:flex;align-items:center;gap:20px;padding-bottom:24px;border-bottom:2px solid var(--line);margin-bottom:46px}}
.head .mk{{width:64px;height:64px}} .head .wm{{font-size:46px}}
"""
THEMES = {
 'white': dict(bg='#FFFFFF', title='#0C1633', text='#4A5478', acc='#FF2E5B', line='#EEF0F8'),
 'soft':  dict(bg='#F4F6FC', title='#0C1633', text='#4A5478', acc='#FF2E5B', line='#E1E5F2'),
 'navy':  dict(bg='#0C1633', title='#FFFFFF', text='#C9D0EC', acc='#FF6E8E', line='rgba(255,255,255,.14)'),
 'pink':  dict(bg='#FF2E5B', title='#FFFFFF', text='#FFFFFF', acc='#0C1633', line='rgba(255,255,255,.35)'),
}
def mark(uid, dark=False):
    s = ''.join(f'<rect y="{i*10}" width="100" height="5" fill="#FF2E5B"/>' for i in range(10))
    return f'<svg class="mk" viewBox="0 0 100 100"><defs><clipPath id="c{uid}"><rect width="100" height="100" rx="30"/></clipPath></defs><g clip-path="url(#c{uid})"><rect width="100" height="100" fill="#0E2156"/>{s}</g></svg>'
def head(uid):
    return f'<div class="head">{mark(uid)}<div><div class="wm">Reagenta</div><div class="sb">CLINICAL SOLUTIONS</div></div></div>'
def foot(uid, txt='reagenta.it · 081 8045042'):
    return f'<div class="foot">{mark(uid)}<div><div class="wm" style="font-size:34px">Reagenta</div><div class="sb">CLINICAL SOLUTIONS</div></div><div class="contact">{txt}</div></div>'
def page(theme, inner, extra=''):
    t = THEMES[theme]
    v = ';'.join(f'--{k}:{x}' for k, x in t.items())
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body style="{v}">{extra}<div class="wrap">{inner}</div></body></html>'

posts = {}

# LUN - checklist numerata, sfondo bianco (biologo/tecnico)
items = [("Identificazione", "Etichetta e dati del campione coincidono con la richiesta."),
         ("Provetta corretta", "Tipo di provetta e anticoagulante giusti per l'esame."),
         ("Riempimento e miscelazione", "Volume corretto, inversioni come da istruzioni d'uso."),
         ("Tempi e conservazione", "Temperatura e tempi di trasporto rispettati.")]
rows = ''.join(f'<div style="display:flex;gap:28px;align-items:center;background:#F4F6FC;border-radius:28px;padding:18px 32px"><div style="font-family:SG;font-weight:700;font-size:60px;color:#FF2E5B;min-width:70px">{i}</div><div><div style="font-family:SG;font-weight:700;font-size:40px;color:#0C1633;line-height:1.1">{a}</div><div style="font-size:28px;line-height:1.3;margin-top:6px">{b}</div></div></div>' for i, (a, b) in enumerate(items, 1))
posts['lun-checklist-preanalitica'] = ('white', head('a') + '<div class="eye"><i></i>Preanalitica · checklist</div>'
  '<h1 style="font-size:92px;margin-top:26px"><em>4 controlli</em> prima di analizzare un campione.</h1>'
  f'<div style="display:flex;flex-direction:column;gap:16px;margin-top:40px">{rows}</div>'
  '<p style="font-size:24px;margin-top:18px;margin-bottom:26px;color:#7079A0">Indicazioni generali: seguire sempre le istruzioni d\'uso del produttore.</p>' + foot('a', 'Salva il post'))

# MAR - numero eroe a tutta pagina, navy con righe magenta (laboratori)
posts['mar-24-48-ore'] = ('navy', head('b') + '<div class="eye"><i></i>Assistenza tecnica</div>'
  '<div style="font-family:SG;font-weight:700;font-size:250px;line-height:.92;letter-spacing:-.04em;color:#FF6E8E;margin-top:50px">24–48</div>'
  '<h1 style="font-size:104px;margin-top:6px">ore. Il nostro tempo di <em>intervento.</em></h1>'
  '<p style="font-size:38px;margin-top:34px;max-width:820px">Per un laboratorio la continuità conta quanto lo strumento: un referente tecnico e tempi chiari.</p>' + foot('b'),
  '<div style="position:absolute;right:0;top:0;bottom:0;width:90px;background:repeating-linear-gradient(to bottom,rgba(255,46,91,.30) 0 4px,transparent 4px 11px)"></div>')

# MER - case study Salerno, magenta pieno con numeri (farmacia)
def tile(n, l):
    return f'<div style="flex:1;background:#fff;border-radius:30px;padding:34px 30px"><div style="font-family:SG;font-weight:700;font-size:120px;line-height:1;color:#0C1633;letter-spacing:-.03em">{n}</div><div style="font-family:PM;font-weight:600;font-size:20px;letter-spacing:.16em;text-transform:uppercase;color:#4A5478;margin-top:14px;line-height:1.35">{l}</div></div>'
posts['mer-open-day-salerno'] = ('pink', head('c') + '<div class="eye" style="color:#fff"><i></i>Sul campo · Salerno</div>'
  '<h1 style="font-size:96px;margin-top:26px">Open day alla <em>Farmacia Verdi Mercatale.</em></h1>'
  '<p style="font-size:36px;margin-top:26px;color:#fff">Una giornata di test, plaque test compresi, con Reagenta Pro.</p>'
  f'<div style="display:flex;gap:20px;margin-top:44px">{tile("12","canali in contemporanea")}{tile("136","test disponibili")}</div>'
  '<p style="font-size:28px;margin-top:24px;color:#fff">Incubazione a bordo. Installazione, formazione e assistenza in 24–48 ore.</p>' + foot('c'))
THEMES['pink']['title'] = '#FFFFFF'

# GIO - mito / fatto, mezzo e mezzo navy-bianco
posts['gio-mito-fatto'] = ('white', '', '')
half = (
 '<div style="position:absolute;left:0;right:0;top:0;height:675px;background:#0C1633"></div>'
 '<div style="position:absolute;left:72px;right:72px;top:72px;bottom:72px;display:flex;flex-direction:column">'
 f'<div style="display:flex;align-items:center;gap:20px">{mark("d1")}<div><div class="wm" style="color:#fff;font-size:46px">Reagenta</div><div class="sb">CLINICAL SOLUTIONS</div></div></div>'
 '<div style="font-family:PM;font-weight:600;font-size:26px;letter-spacing:.3em;color:#FF6E8E;margin-top:62px">MITO</div>'
 '<h1 style="font-size:76px;color:#fff;margin-top:14px">«Un test rapido in farmacia sostituisce la visita medica.»</h1>'
 '<div style="font-family:PM;font-weight:600;font-size:26px;letter-spacing:.3em;color:#FF2E5B;margin-top:auto">FATTO</div>'
 '<h1 style="font-size:76px;margin-top:14px;color:#0C1633">Sono dispositivi <em>CE-IVD</em> per uso professionale. L\'interpretazione spetta al medico.</h1>'
 '<p style="font-size:30px;margin-top:22px">Formazione e istruzioni d\'uso fanno parte del servizio.</p>'
 '</div>')
posts['gio-mito-fatto'] = ('white', '', half)

# VEN - griglia 3 servizi, soft (acquisti / enti)
svc = [("01", "Installazione", "Avvio e messa in funzione con il nostro team."),
       ("02", "Formazione", "Il personale impara a usare lo strumento."),
       ("03", "Assistenza", "Intervento tecnico in 24–48 ore.")]
cards = ''.join(f'<div style="flex:1;background:#fff;border-radius:30px;padding:34px 28px;box-shadow:0 10px 30px rgba(12,22,51,.07)"><div style="font-family:SG;font-weight:700;font-size:64px;color:#FF2E5B">{n}</div><div style="font-family:SG;font-weight:700;font-size:40px;color:#0C1633;margin-top:12px">{a}</div><div style="font-size:26px;line-height:1.35;margin-top:12px">{b}</div></div>' for n, a, b in svc)
posts['ven-tre-servizi'] = ('soft', head('e') + '<div class="eye"><i></i>Per laboratori, farmacie, enti</div>'
  '<h1 style="font-size:100px;margin-top:26px">Dopo la consegna, <em>comincia il servizio.</em></h1>'
  f'<div style="display:flex;gap:18px;margin-top:46px">{cards}</div>'
  '<div style="margin-top:36px;background:#0C1633;border-radius:100px;padding:28px 44px;align-self:flex-start;font-family:PM;font-weight:600;font-size:24px;letter-spacing:.2em;color:#fff">RICHIEDI UNA <span style="color:#FF2E5B">QUOTAZIONE</span></div>' + foot('e', 'reagenta.it/quotazione'))

with sync_playwright() as p:
    b = p.chromium.launch()
    for name, tup in posts.items():
        theme, inner, extra = (tup + ('',))[:3]
        h = page(theme, inner, extra)
        fn = pathlib.Path('/tmp') / f'{name}.html'
        fn.write_text(h)
        pg = b.new_page(viewport={'width': 1080, 'height': 1350})
        pg.goto('file://' + str(fn)); pg.wait_for_timeout(600)
        pg.screenshot(path=str(OUT / f'feed18-{name}.png')); pg.close()
    b.close()
print(list(posts))
