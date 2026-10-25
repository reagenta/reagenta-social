"""Chiusura Pharmexpo 2026 (domenica 25/10): post di ringraziamento + storia.
Output in img/2026-10-25/. Font da /home/claude/social-build/node_modules/@fontsource.
"""
import pathlib, html
from playwright.sync_api import sync_playwright

F = "file:///home/claude/social-build/node_modules/@fontsource"
CSS = f"""
@font-face{{font-family:'SG';font-weight:700;src:url('{F}/space-grotesk/files/space-grotesk-latin-700-normal.woff2')}}
@font-face{{font-family:'PS';font-weight:400;src:url('{F}/ibm-plex-sans/files/ibm-plex-sans-latin-400-normal.woff2')}}
@font-face{{font-family:'PS';font-weight:600;src:url('{F}/ibm-plex-sans/files/ibm-plex-sans-latin-600-normal.woff2')}}
@font-face{{font-family:'PM';font-weight:600;src:url('{F}/ibm-plex-mono/files/ibm-plex-mono-latin-600-normal.woff2')}}
*{{box-sizing:border-box;margin:0}}
body{{font-family:'PS';color:#4A5478;position:relative;overflow:hidden}}
.wrap{{position:absolute;left:80px;right:80px;display:flex;flex-direction:column}}
.head{{display:flex;align-items:center;gap:20px;padding-bottom:26px;border-bottom:2px solid var(--line)}}
.mark{{width:76px;height:76px}}
.wm{{font-family:'SG';font-weight:700;font-size:56px;color:var(--ink);line-height:1}}
.sub{{font-family:'PM';font-weight:600;font-size:15px;letter-spacing:.32em;color:#FF2E5B;margin-top:8px}}
.cnt{{margin-left:auto;font-family:'PM';font-weight:600;font-size:24px;letter-spacing:.2em;color:var(--muted)}}
.eye{{display:flex;align-items:center;gap:18px;font-family:'PM';font-weight:600;font-size:24px;letter-spacing:.3em;color:var(--muted);text-transform:uppercase}}
.eye i{{display:block;width:48px;height:4px;background:#FF2E5B}}
h1{{font-family:'SG';font-weight:700;letter-spacing:-.02em;color:var(--ink);line-height:1.04}}
h1 em{{font-style:normal;color:#FF2E5B}}
p{{font-size:36px;line-height:1.45;color:var(--body)}}
.soft{{background:#fff;border-radius:34px;padding:40px 48px}}
.soft small{{display:block;font-family:'PM';font-weight:600;font-size:20px;letter-spacing:.25em;color:#FF2E5B;margin-bottom:16px;text-transform:uppercase}}
.soft p{{color:#0C1633;font-weight:600;font-size:36px;line-height:1.4}}
.card{{border-radius:34px;background:#0C1633;position:relative;overflow:hidden;display:flex;align-items:center;padding:0 52px;gap:46px}}
.card:after{{content:'';position:absolute;right:0;top:0;bottom:0;width:70px;background:repeating-linear-gradient(to bottom,rgba(255,46,91,.28) 0 3px,transparent 3px 8px)}}
.lab{{font-family:'PM';font-weight:600;font-size:20px;letter-spacing:.3em;color:#FF6E8E;text-transform:uppercase}}
.big{{font-family:'SG';font-weight:700;color:#fff;line-height:.95}}
.card .t{{color:#C9D0EC;font-size:30px;line-height:1.45}}
.pill{{align-self:flex-start;font-family:'PM';font-weight:600;font-size:26px;letter-spacing:.28em;padding:30px 48px;border-radius:100px}}
.pill b{{color:#FF2E5B;font-weight:600}}
"""
LIGHT = "--ink:#0C1633;--body:#4A5478;--muted:#7079A0;--line:#E1E5F3;background:#F4F6FC"
DARK = "--ink:#fff;--body:#C9D0EC;--muted:#9AA3CC;--line:rgba(255,255,255,.14);background:#0C1633"


def mark(light=True):
    s = ''.join(f'<rect y="{i*10}" width="100" height="5" fill="#FF2E5B"/>' for i in range(10))
    bg = "#0E2156"
    return (f'<svg class="mark" viewBox="0 0 100 100"><defs><clipPath id="c"><rect width="100" height="100" rx="30"/></clipPath></defs>'
            f'<g clip-path="url(#c)"><rect width="100" height="100" fill="{bg}"/>{s}</g></svg>')


def head(cnt=""):
    return (f'<div class="head">{mark()}<div><div class="wm">Reagenta</div><div class="sub">CLINICAL SOLUTIONS</div></div>'
            f'<div class="cnt">{cnt}</div></div>')


def page(w, h, top, bottom, theme, inner):
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS} body{{width:{w}px;height:{h}px;{theme}}} '
            f'.wrap{{top:{top}px;bottom:{bottom}px}}</style></head><body><div class="wrap">{inner}</div></body></html>')


POST = (1080, 1350, 72, 72)
STORY = (1080, 1920, 250, 250)
out = {}

# ---- POST 4:5 (sfondo chiaro, per variare rispetto alle card navy dei giorni scorsi)
out['ig-post-grazie-pharmexpo'] = (POST, LIGHT, head("PHARMEXPO 2026")
    + '<div class="eye" style="margin-top:48px"><i></i>Tre giorni a Napoli</div>'
    + '<h1 style="font-size:108px;margin-top:26px">Grazie a chi è passato <em>a trovarci.</em></h1>'
    + '<p style="margin-top:26px;max-width:900px">Tre giorni di confronto con farmacisti, professionisti e distributori su come portare analisi vere in farmacia.</p>'
    + '<div class="soft" style="margin-top:34px;padding:34px 48px"><small>Non ci hai incontrati?</small>'
      '<p>Scrivici o chiamaci: ti mostriamo Reagenta Pro e le soluzioni per la farmacia.</p></div>'
    + '<div class="card" style="margin-top:auto;height:210px"><div><div class="lab">Pharmexpo 2026</div>'
      '<div class="big" style="font-size:84px;margin-top:10px">23–25 OTT</div></div>'
      '<div class="t">081 8045042<br>ordini@reagenta.it<br>reagenta.it</div></div>')

# ---- STORY 9:16 (sfondo navy, zone sicure 250px sopra/sotto)
out['ig-story-grazie-pharmexpo'] = (STORY, DARK, head()
    + '<div class="eye" style="margin-top:70px"><i></i>Pharmexpo 2026 · è finita</div>'
    + '<div class="big" style="font-size:250px;margin-top:50px;letter-spacing:-.04em;line-height:.92">GRAZIE<span style="color:#FF2E5B">.</span></div>'
    + '<h1 style="font-size:96px;margin-top:40px">Tre giorni<br>allo <em style="white-space:nowrap">stand 574.</em></h1>'
    + '<p style="font-size:42px;margin-top:34px">Grazie a tutti quelli che sono passati a trovarci alla Mostra d\'Oltremare.</p>'
    + '<div class="card" style="margin-top:60px;height:270px;background:#0E2156"><div><div class="lab">Pharmexpo 2026</div><div class="big" style="font-size:84px;margin-top:12px">23–25 OTT</div></div><div class="t">Mostra d\'Oltremare<br>Napoli<br>Stand 574</div></div>'
    + '<div class="pill" style="margin-top:auto;background:#fff;color:#0C1633">SCRIVICI <b>IN DM</b></div>')

outdir = pathlib.Path('/home/claude/reagenta-social/img/2026-10-25')
tmp = pathlib.Path('/tmp/claude-0/-home-claude/69c6f0bb-3b0b-5e7e-b4a6-20175315735c/scratchpad/chiusura')
tmp.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch()
    for name, ((w, h, t, bo), theme, inner) in out.items():
        pg = b.new_page(viewport={"width": w, "height": h})
        fn = tmp / f"{name}.html"
        fn.write_text(page(w, h, t, bo, theme, inner))
        pg.goto("file://" + str(fn)); pg.wait_for_timeout(600)
        pg.screenshot(path=str(outdir / f"{name}.png")); pg.close()
    b.close()
print(list(out))
