import sys, pathlib
from playwright.sync_api import sync_playwright
F = "file:///home/claude/social-build/node_modules/@fontsource"
html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:'SG';font-weight:700;src:url('{F}/space-grotesk/files/space-grotesk-latin-700-normal.woff2')}}
@font-face{{font-family:'SG';font-weight:500;src:url('{F}/space-grotesk/files/space-grotesk-latin-500-normal.woff2')}}
@font-face{{font-family:'PS';font-weight:400;src:url('{F}/ibm-plex-sans/files/ibm-plex-sans-latin-400-normal.woff2')}}
@font-face{{font-family:'PS';font-weight:600;src:url('{F}/ibm-plex-sans/files/ibm-plex-sans-latin-600-normal.woff2')}}
@font-face{{font-family:'PM';font-weight:600;src:url('{F}/ibm-plex-mono/files/ibm-plex-mono-latin-600-normal.woff2')}}
*{{box-sizing:border-box;margin:0}}
body{{width:1080px;height:1350px;background:#fff;font-family:'PS';color:#4A5478;position:relative;overflow:hidden}}
.wrap{{position:absolute;left:80px;right:80px;top:72px;bottom:72px;display:flex;flex-direction:column}}
.head{{display:flex;align-items:center;gap:20px;padding-bottom:26px;border-bottom:2px solid #EEF0F8}}
.mark{{width:76px;height:76px}}
.wm{{font-family:'SG';font-weight:700;font-size:56px;color:#0C1633;line-height:1}}
.sub{{font-family:'PM';font-weight:600;font-size:15px;letter-spacing:.32em;color:#FF2E5B;margin-top:8px}}
.eye{{display:flex;align-items:center;gap:18px;margin-top:70px;font-family:'PM';font-weight:600;font-size:24px;letter-spacing:.3em;color:#4A5478}}
.eye i{{display:block;width:48px;height:4px;background:#FF2E5B}}
h1{{font-family:'SG';font-weight:700;font-size:108px;line-height:1.02;letter-spacing:-.02em;color:#0C1633;margin-top:30px}}
h1 em{{font-style:normal;color:#FF2E5B}}
p{{font-size:36px;line-height:1.45;margin-top:34px;max-width:860px}}
.card{{margin-top:auto;height:300px;border-radius:34px;background:#0C1633;position:relative;overflow:hidden;display:flex;align-items:center;padding:0 52px;gap:46px}}
.card:after{{content:'';position:absolute;right:0;top:0;bottom:0;width:70px;background:repeating-linear-gradient(to bottom,rgba(255,46,91,.28) 0 3px,transparent 3px 8px)}}
.st b{{display:block;font-family:'SG';font-weight:700;font-size:78px;color:#fff;line-height:1}}
.st span{{display:block;font-family:'PM';font-weight:600;font-size:16px;letter-spacing:.2em;color:#FF6E8E;margin-top:14px;text-transform:uppercase}}
</style></head><body><div class="wrap">
<div class="head"><svg class="mark" viewBox="0 0 100 100"><defs><clipPath id="c"><rect width="100" height="100" rx="30"/></clipPath></defs><g clip-path="url(#c)"><rect width="100" height="100" fill="#0E2156"/>{''.join(f'<rect y="{i*10}" width="100" height="5" fill="#FF2E5B"/>' for i in range(10))}</g></svg>
<div><div class="wm">Reagenta</div><div class="sub">CLINICAL SOLUTIONS</div></div></div>
<div class="eye"><i></i>ESEMPIO DI GRAFICA</div>
<h1>Il tuo partner per la <em>diagnostica.</em></h1>
<p>Strumenti, reagenti e materiale di consumo per laboratori, ospedali e professionisti.</p>
<div class="card"><div class="st"><b>5.700+</b><span>Referenze</span></div><div class="st"><b>60+</b><span>Produttori</span></div><div class="st"><b>24/48h</b><span>Spedizione tracciata</span></div></div>
</div></body></html>"""
pathlib.Path("out/sample.html").write_text(html)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width":1080,"height":1350})
    pg.goto("file:///home/claude/social-build/out/sample.html"); pg.wait_for_timeout(600)
    pg.screenshot(path="out/esempio-post.png"); b.close()
