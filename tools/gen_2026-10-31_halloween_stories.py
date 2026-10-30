import pathlib, base64
from playwright.sync_api import sync_playwright
FB="/tmp/claude-0/-home-claude/1d8364a1-3051-5239-bfb6-40e8b458227f/scratchpad/fb/node_modules/@fontsource"
def b64(p): return "data:image/png;base64,"+base64.b64encode(open(p,'rb').read()).decode()
LOGO=b64("/home/claude/assets/logo-light.png"); PHOTO=b64("/home/claude/assets/p17976-1791618336-e65dfd.png")
CSS=f"""
@font-face{{font-family:'SG';font-weight:700;src:url('file://{FB}/space-grotesk/files/space-grotesk-latin-700-normal.woff2')}}
@font-face{{font-family:'PS';font-weight:400;src:url('file://{FB}/ibm-plex-sans/files/ibm-plex-sans-latin-400-normal.woff2')}}
@font-face{{font-family:'PM';font-weight:400;src:url('file://{FB}/ibm-plex-mono/files/ibm-plex-mono-latin-400-normal.woff2')}}
*{{box-sizing:border-box;margin:0}}
body{{width:1080px;height:1920px;background:#0C1633;font-family:'PS';color:#C9D0EC;position:relative;overflow:hidden}}
.glow{{position:absolute;right:-300px;top:700px;width:1000px;height:1000px;background:radial-gradient(circle,rgba(255,46,91,.32),transparent 65%)}}
.bar{{position:absolute;left:0;top:0;bottom:0;width:8px;background:#FF2E5B}}
.wrap{{position:absolute;left:80px;right:80px;top:250px;bottom:250px;display:flex;flex-direction:column}}
.logo{{width:360px}}
.eye{{margin-top:70px;font-family:'PM';font-size:28px;letter-spacing:.22em;color:#FF2E5B;text-transform:uppercase}}
h1{{font-family:'SG';font-weight:700;letter-spacing:-.02em;color:#fff;font-size:128px;line-height:1.02;margin-top:26px}}
h1 em{{font-style:normal;color:#FF4D78}}
.sub{{font-size:44px;line-height:1.4;margin-top:34px}}
.chips{{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:50px}}
.chip{{background:#12224a;border:2px solid #1d2f63;border-radius:26px;padding:26px 28px;font-size:34px;color:#fff;display:flex;gap:20px;align-items:center}}
.chip b{{font-family:'PM';font-weight:400;color:#FF2E5B;font-size:34px}}
.btn{{margin-top:auto;background:#FF2E5B;color:#fff;font-family:'SG';font-weight:700;font-size:46px;padding:38px 48px;border-radius:30px;display:flex;justify-content:space-between;align-items:center;box-shadow:0 18px 40px rgba(255,46,91,.35)}}
.card{{margin-top:50px;background:#fff;border-radius:44px;padding:40px 44px;display:flex;align-items:center;gap:30px}}
.card img{{width:400px}}
.card .n{{font-family:'SG';font-weight:700;color:#0C1633;font-size:52px;line-height:1.1}}
.card .m{{font-family:'PM';color:#7079A0;font-size:26px;margin-top:12px}}
.web{{position:absolute;right:0;top:120px;width:300px;opacity:.5}}
.bat{{position:absolute;opacity:.5}}
"""
WEB='<svg class="web" viewBox="0 0 300 300" fill="none" stroke="#3a4a7e" stroke-width="3"><path d="M300 0 L0 0 M300 0 L300 300 M300 0 L40 120 M300 0 L110 250"/><path d="M230 0 Q215 70 300 80 M150 0 Q130 130 300 150 M80 0 Q60 190 300 230"/></svg>'
def bat(x,y,s=1): return f'<svg class="bat" style="left:{x}px;top:{y}px;width:{110*s}px" viewBox="0 0 110 50"><path d="M55 14 L42 4 L28 14 L2 8 L18 30 L32 26 L42 44 L55 28 L68 44 L78 26 L92 30 L108 8 L82 14 L68 4 Z" fill="#4a5a8e"/></svg>'
ARROW='<svg width="48" height="40" viewBox="0 0 48 40"><path d="M4 20h36M26 5l15 15-15 15" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def page(inner): return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="glow"></div><div class="bar"></div>{WEB}{inner}</body></html>'
S1=page(bat(700,1370,1.2)+f'''<div class="wrap"><img class="logo" src="{LOGO}">
<div class="eye">Halloween / Edizione Lab</div>
<h1>Quale ti ha fatto <em>venire i brividi?</em></h1>
<div class="chips"><div class="chip"><b>01</b>Campione emolizzato</div><div class="chip"><b>02</b>Etichetta illeggibile</div><div class="chip"><b>03</b>Reagente scaduto</div><div class="chip"><b>04</b>Calibratore fuori posto</div><div class="chip"><b>05</b>QC fuori limite</div><div class="chip"><b>06</b>Strumento fermo</div></div>
<div class="btn"><span>Scopri il post</span>{ARROW}</div></div>''')
S2=page(f'''<div class="wrap"><img class="logo" src="{LOGO}">
<div class="eye">Dopo la paura, la calma</div>
<h1>Strumento fermo? <em>La coda no.</em></h1>
<div class="sub">Il laboratorio non può fermarsi. Scrivici: rispondiamo noi.</div>
<div class="card"><img src="{PHOTO}"><div><div class="n">AutoLumo S900</div><div class="m">analizzatore CLIA</div></div></div>
<div class="btn"><span>Scrivici in DM</span>{ARROW}</div></div>''')
S0=page(bat(700,1560,1.2)+f'''<svg style="position:absolute;right:120px;top:1000px;width:330px" viewBox="0 0 120 140"><path d="M10 130V60C10 25 35 8 60 8s50 17 50 52v70l-14-12-12 12-12-12-12 12-12-12-12 12-12-12z" fill="#E8ECFA"/><ellipse cx="44" cy="58" rx="7" ry="11" fill="#0C1633"/><ellipse cx="76" cy="58" rx="7" ry="11" fill="#0C1633"/><ellipse cx="60" cy="86" rx="8" ry="11" fill="#0C1633"/></svg><div class="wrap"><img class="logo" src="{LOGO}">
<div class="eye">Halloween / Edizione Lab</div>
<h1>Domani <em>sei mostri</em> in laboratorio.</h1>
<div class="sub">Li conosci già. Alle 10:00 scopri chi sono.</div></div>''')
out=pathlib.Path("/home/claude/reagenta-social/img/2026-10-31"); 
with sync_playwright() as p:
    b=p.chromium.launch()
    for n,h in (("s0",S0),("s1",S1),("s2",S2)):
        f=pathlib.Path(f"/tmp/claude-0/-home-claude/1d8364a1-3051-5239-bfb6-40e8b458227f/scratchpad/{n}.html"); f.write_text(h)
        pg=b.new_page(viewport={"width":1080,"height":1920}); pg.goto("file://"+str(f)); pg.wait_for_timeout(600)
        pg.screenshot(path=str(out/f"{n}.png")); pg.close()
    b.close()
print("ok")
