import pathlib
from playwright.sync_api import sync_playwright
F="file:///home/claude/social-build/node_modules/@fontsource"
P="file:///home/claude/social-build/photos"
CSS=f"""
@font-face{{font-family:'SG';font-weight:700;src:url('{F}/space-grotesk/files/space-grotesk-latin-700-normal.woff2')}}
@font-face{{font-family:'PS';font-weight:400;src:url('{F}/ibm-plex-sans/files/ibm-plex-sans-latin-400-normal.woff2')}}
@font-face{{font-family:'PM';font-weight:600;src:url('{F}/ibm-plex-mono/files/ibm-plex-mono-latin-600-normal.woff2')}}
*{{box-sizing:border-box;margin:0}}
body{{position:relative;overflow:hidden;background:#0C1633;font-family:'PS'}}
.ph{{position:absolute;inset:0;background-size:cover}}
.shade{{position:absolute;inset:0}}
.logo{{position:absolute;left:72px;display:flex;align-items:center;gap:20px;background:#fff;border-radius:34px;padding:22px 32px 22px 28px}}
.mark{{width:64px;height:64px}}
.wm{{font-family:'SG';font-weight:700;font-size:50px;color:#0C1633;line-height:1}}
.sub{{font-family:'PM';font-weight:600;font-size:13px;letter-spacing:.3em;color:#FF2E5B;margin-top:7px}}
.txt{{position:absolute;left:72px;right:72px}}
.eye{{display:flex;align-items:center;gap:18px;font-family:'PM';font-weight:600;font-size:24px;letter-spacing:.3em;color:#FF6E8E;text-transform:uppercase}}
.eye i{{display:block;width:48px;height:4px;background:#FF2E5B}}
h1{{font-family:'SG';font-weight:700;letter-spacing:-.02em;color:#fff;line-height:1.03;margin-top:26px}}
h1 em{{font-style:normal;color:#FF6E8E}}
.pill{{display:inline-block;margin-top:38px;background:#fff;color:#0C1633;font-family:'PM';font-weight:600;font-size:24px;letter-spacing:.2em;padding:24px 44px;border-radius:100px;text-transform:uppercase}}
.pill b{{color:#FF2E5B;font-weight:600}}
.card{{border-radius:34px;background:#0C1633;position:relative;overflow:hidden;display:flex;align-items:center;padding:0 52px;gap:46px;margin-top:38px;height:250px}}
.card:after{{content:'';position:absolute;right:0;top:0;bottom:0;width:70px;background:repeating-linear-gradient(to bottom,rgba(255,46,91,.28) 0 3px,transparent 3px 8px)}}
.lab{{font-family:'PM';font-weight:600;font-size:20px;letter-spacing:.3em;color:#FF6E8E;text-transform:uppercase}}
.big{{font-family:'SG';font-weight:700;color:#fff;line-height:.95;font-size:140px}}
.t{{color:#C9D0EC;font-size:30px;line-height:1.45}}
"""
def mark():
    s=''.join(f'<rect y="{i*10}" width="100" height="5" fill="#FF2E5B"/>' for i in range(10))
    return f'<svg class="mark" viewBox="0 0 100 100"><defs><clipPath id="c"><rect width="100" height="100" rx="30"/></clipPath></defs><g clip-path="url(#c)"><rect width="100" height="100" fill="#0E2156"/>{s}</g></svg>'
LOGO=lambda top:f'<div class="logo" style="top:{top}px">{mark()}<div><div class="wm">Reagenta</div><div class="sub">CLINICAL SOLUTIONS</div></div></div>'
def page(w,h,photo,pos,shade,inner):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS} body{{width:{w}px;height:{h}px}}</style></head><body><div class="ph" style="background-image:url({P}/{photo});background-position:{pos}"></div><div class="shade" style="background:{shade}"></div>{inner}</body></html>'
G="linear-gradient(to bottom,rgba(12,22,51,0) 0%,rgba(12,22,51,0) {a}%,rgba(12,22,51,.88) {b}%,#0C1633 100%)"
out={}
# POST 4:5 - stand
out['post-giorno2-stand']=(1080,1350,page(1080,1350,'stand.jpg','50% 20%',G.format(a=38,b=70),
  LOGO(56)+'<div class="txt" style="bottom:72px"><div class="eye"><i></i>Pharmexpo 2026 · Stand 574</div><h1 style="font-size:104px">Secondo giorno. <em>Vieni a trovarci.</em></h1><div class="pill">Mostra d\'Oltremare · <b>Sab 24 ott</b></div></div>'))
# STORY 1 - close-up CITEST Pro
out['story-citest-pro']=(1080,1920,page(1080,1920,'citest.jpg','50% 40%',G.format(a=48,b=76),
  LOGO(250)+'<div class="txt" style="bottom:250px"><div class="eye"><i></i>Pharmexpo · Stand 574</div><h1 style="font-size:106px">Toccalo <em>con mano.</em></h1><p style="font-size:42px;line-height:1.4;color:#C9D0EC;margin-top:26px">Il CITEST Pro ti aspetta.</p></div>'))
# STORY 2 - stand + orari
out['story-orari-stand']=(1080,1920,page(1080,1920,'stand.jpg','88% 50%',G.format(a=34,b=66),
  LOGO(250)+'<div class="txt" style="bottom:250px"><div class="eye"><i></i>Siamo in fiera</div><h1 style="font-size:100px">Oggi fino alle <em>18:00.</em></h1><div class="card"><div><div class="lab">Stand</div><div class="big">574</div></div><div class="t">Mostra d\'Oltremare<br>Viale Kennedy 54, Napoli<br>Domani 10:00 – 15:00</div></div></div>'))
pathlib.Path('out').mkdir(exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch()
    for n,(w,h,html) in out.items():
        pg=b.new_page(viewport={'width':w,'height':h}); f=pathlib.Path(f'out/{n}.html'); f.write_text(html)
        pg.goto('file://'+str(f.resolve())); pg.wait_for_timeout(600); pg.screenshot(path=f'out/{n}.png'); pg.close()
    b.close()
print(list(out))
