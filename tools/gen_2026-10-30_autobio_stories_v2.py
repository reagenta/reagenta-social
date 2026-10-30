"""Set 1 stories "Arrivati i kit Autobio" v2 - foto a tutto schermo, testo minimo in basso.
Nessun riferimento al tipo di kit (ne abbiamo diversi). 1080x1920, safe zone 250px.
Foto: /home/claude/assets/{box,fila,mano}.jpg (la foto 'mano' ha lotto/QR sfumati).
"""
import pathlib, base64
from playwright.sync_api import sync_playwright

FB = "/home/claude/social-build/node_modules/@fontsource"
ASSETS = "/home/claude/assets"
OUT = pathlib.Path("/home/claude/reagenta-social/img/2026-10-30")
TMP = pathlib.Path("/home/claude/assets/html"); TMP.mkdir(exist_ok=True)


def jpg(n):
    return "data:image/jpeg;base64," + base64.b64encode(open(f"{ASSETS}/{n}.jpg", "rb").read()).decode()


BOX, FILA, MANO = jpg("box"), jpg("fila"), jpg("mano")

CSS = f"""
@font-face{{font-family:'SG';font-weight:700;src:url('file://{FB}/space-grotesk/files/space-grotesk-latin-700-normal.woff2')}}
@font-face{{font-family:'PS';font-weight:400;src:url('file://{FB}/ibm-plex-sans/files/ibm-plex-sans-latin-400-normal.woff2')}}
@font-face{{font-family:'PM';font-weight:500;src:url('file://{FB}/ibm-plex-mono/files/ibm-plex-mono-latin-500-normal.woff2')}}
*{{box-sizing:border-box;margin:0}}
body{{width:1080px;height:1920px;position:relative;overflow:hidden;font-family:'PS';background:#0C1633}}
.bg{{position:absolute;inset:0}}
.bg img{{width:100%;height:100%;object-fit:cover;display:block}}
.shade{{position:absolute;left:0;right:0;bottom:0;height:760px;background:linear-gradient(to top,rgba(12,22,51,.97) 0,rgba(12,22,51,.93) 42%,rgba(12,22,51,.55) 72%,rgba(12,22,51,0) 100%)}}
.shade.tall{{height:1000px;background:linear-gradient(to top,rgba(12,22,51,.97) 0,rgba(12,22,51,.95) 62%,rgba(12,22,51,.86) 76%,rgba(12,22,51,0) 100%)}}
.logo{{position:absolute;left:72px;top:250px;height:112px;background:#fff;border-radius:56px;padding:0 40px 0 26px;display:flex;align-items:center;gap:22px;box-shadow:0 14px 36px rgba(12,22,51,.25)}}
.logo svg{{width:64px;height:64px}}
.wm{{font-family:'SG';font-weight:700;font-size:48px;line-height:1;color:#0C1633;letter-spacing:-.01em}}
.cs{{font-family:'PM';font-weight:500;font-size:14px;letter-spacing:.26em;color:#FF2E5B;margin-top:7px}}
.eye{{position:absolute;left:72px;font-family:'PM';font-weight:500;font-size:26px;letter-spacing:.22em;text-transform:uppercase;color:#FF6E8E;display:flex;align-items:center;gap:20px}}
.eye:before{{content:'';width:44px;height:5px;background:#FF2E5B;border-radius:3px}}
h1{{position:absolute;left:72px;right:72px;font-family:'SG';font-weight:700;letter-spacing:-.025em;font-size:90px;line-height:1.04;color:#fff}}
h1 em{{font-style:normal;color:#FF4D78}}
.sticker{{position:absolute;background:#FF2E5B;color:#fff;font-family:'SG';font-weight:700;font-size:44px;line-height:1.05;padding:22px 32px;border-radius:30px;box-shadow:0 16px 36px rgba(255,46,91,.45)}}
.chips{{position:absolute;left:72px;right:72px;display:grid;grid-template-columns:1fr 1fr;gap:16px}}
.chip{{background:rgba(18,34,74,.92);border:2px solid #2c4080;border-radius:26px;height:96px;padding:0 28px;display:flex;align-items:center;gap:20px;font-family:'SG';font-weight:700;font-size:38px;color:#fff;white-space:nowrap}}
.chip b{{font-family:'PM';font-weight:500;font-size:26px;color:#FF2E5B}}
.ct{{position:absolute;left:72px;right:72px;display:grid;grid-template-columns:1fr 1.25fr;gap:16px}}
.ct div{{background:rgba(18,34,74,.92);border:2px solid #2c4080;border-radius:26px;height:92px;display:flex;align-items:center;justify-content:center;font-family:'PM';font-weight:500;font-size:32px;color:#fff}}
.btn{{position:absolute;left:72px;right:72px;height:112px;background:#FF2E5B;color:#fff;font-family:'SG';font-weight:700;font-size:46px;border-radius:30px;display:flex;justify-content:space-between;align-items:center;padding:0 44px;box-shadow:0 18px 40px rgba(255,46,91,.4)}}
"""

LOGO = '''<div class="logo"><svg viewBox="0 0 168 168"><defs><clipPath id="c"><rect width="168" height="168" rx="48"/></clipPath></defs>
<g clip-path="url(#c)"><rect width="168" height="168" fill="#FF2B59"/>''' + "".join(
    f'<rect y="{i*19.82:.2f}" width="168" height="9.4" rx="4.7" fill="#11245A"/>' for i in range(9)) + '''</g></svg>
<div><div class="wm">Reagenta</div><div class="cs">CLINICAL SOLUTIONS</div></div></div>'''

ARROW = '<svg width="48" height="40" viewBox="0 0 48 40"><path d="M4 20h36M26 5l15 15-15 15" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def page(photo, pos, inner, tall=False, img=None, shade=None):
    """img: stile libero per posizionare/ingrandire la foto; shade: stile libero della sfumatura."""
    s = '<div class="shade tall"></div>' if tall else '<div class="shade"></div>'
    if shade:
        s = f'<div class="shade" style="{shade}"></div>'
    ist = img if img else f"object-position:{pos}"
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>'
            f'<div class="bg"><img src="{photo}" style="{ist}"></div>{s}{LOGO}{inner}</body></html>')


# foto 'box': i kit stanno nella metà bassa -> la foto viene alzata cosi' che i kit finiscano a meta' schermo
BOX_S1 = "position:absolute;width:1452px;height:auto;left:-186px;top:-583px"   # bordo basso foto a y=1330
BOX_S5 = "position:absolute;width:1320px;height:auto;left:-120px;top:-589px"   # bordo basso foto a y=1150
SH_S1 = "top:1050px;height:870px;background:linear-gradient(to bottom,rgba(12,22,51,0) 0,rgba(12,22,51,.97) 32%,rgba(12,22,51,.97) 100%)"
SH_S5 = "top:900px;height:1020px;background:linear-gradient(to bottom,rgba(12,22,51,0) 0,rgba(12,22,51,.97) 25%,rgba(12,22,51,.97) 100%)"


# 1 - Sono arrivati
S1 = page(BOX, "50% 50%", '''
<div class="sticker" style="left:690px;top:430px;transform:rotate(6deg)">Appena<br>aperto!</div>
<div class="eye" style="top:1400px">Autobio · nuovo arrivo</div>
<h1 style="top:1458px">Sono arrivati i kit <em>Autobio.</em></h1>''', img=BOX_S1, shade=SH_S1)

# 2 - La fila
S2 = page(FILA, "50% 50%", '''
<div class="eye" style="top:1400px">Magazzino Reagenta</div>
<h1 style="top:1458px">Una <em>bella fila</em><br>di kit.</h1>''')

# 3 - Piccoli ma potenti
S3 = page(MANO, "52% 50%", '''
<div class="sticker" style="left:690px;top:420px;transform:rotate(6deg)">Sta in una<br>mano!</div>
<div class="eye" style="top:1400px">Guarda che dimensioni</div>
<h1 style="top:1458px">Piccoli,<br>ma <em>potenti.</em></h1>''')

# 4 - Sondaggio
chips = "".join(f'<div class="chip"><b>{n}</b>{t}</div>' for n, t in (("A", "Ormoni"), ("B", "Tiroide"), ("C", "Marker tumorali"), ("D", "Altro")))
S4 = page(FILA, "50% 40%", f'''
<div class="sticker" style="left:700px;top:430px;transform:rotate(7deg);font-size:92px;padding:4px 40px 10px">?</div>
<div class="eye" style="top:1230px">Sondaggio</div>
<h1 style="top:1288px;font-size:82px">Quale marker<br><em>ti serve di più?</em></h1>
<div class="chips" style="top:1496px">{chips}</div>''', tall=True)

# 5 - CTA
S5 = page(BOX, "50% 42%", f'''
<div class="eye" style="top:1196px">Autobio · Reagenta</div>
<h1 style="top:1254px;font-size:82px">Ti serve un kit<br><em>Autobio?</em></h1>
<div class="ct" style="top:1448px"><div>081 8045042</div><div>ordini@reagenta.it</div></div>
<div class="btn" style="top:1550px"><span>Link in bio</span>{ARROW}</div>''', img=BOX_S5, shade=SH_S5)

FRAMES = (("autobio-v2-s1-arrivati", S1), ("autobio-v2-s2-fila", S2), ("autobio-v2-s3-piccoli-potenti", S3),
          ("autobio-v2-s4-sondaggio", S4), ("autobio-v2-s5-cta", S5))

with sync_playwright() as p:
    b = p.chromium.launch()
    for n, h in FRAMES:
        f = TMP / f"{n}.html"; f.write_text(h)
        pg = b.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto("file://" + str(f)); pg.wait_for_timeout(700)
        pg.screenshot(path=str(OUT / f"{n}.png")); pg.close()
    b.close()
print("ok")
