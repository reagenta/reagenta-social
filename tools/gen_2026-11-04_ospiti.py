"""Post + storia "Ospiti internazionali in sede" (04/11/2026).
Foto: /mnt/user-data/uploads/FullSizeRender.jpeg  -> testo a schermo del monitor sfumato.
Post 1080x1350, storia 1080x1920 (safe zone 250px). Stile reagenta.it (navy + magenta).
"""
import pathlib, base64, io
from PIL import Image, ImageFilter, ImageDraw
from playwright.sync_api import sync_playwright

FB = "/home/claude/social-build/node_modules/@fontsource"
SRC = "/mnt/user-data/uploads/FullSizeRender.jpeg"
OUT = pathlib.Path("/home/claude/reagenta-social/img/2026-11-04"); OUT.mkdir(parents=True, exist_ok=True)
TMP = pathlib.Path("/home/claude/assets/html"); TMP.mkdir(parents=True, exist_ok=True)

# --- foto: cancello il messaggio "Nessun segnale" del monitor (fondo sfumato, esclude la giacca) ---
im = Image.open(SRC).convert("RGB")
cx0, cy0, cx1, cy1 = 1040, 640, 1320, 830
ctx = im.crop((cx0, cy0, cx1, cy1))
smooth = ctx.resize((14, 10), Image.BOX).resize(ctx.size, Image.BICUBIC).filter(ImageFilter.GaussianBlur(10))
mask = Image.new("L", ctx.size, 0)
poly = [(1058 - cx0, 650 - cy0), (1250 - cx0, 650 - cy0), (1250 - cx0, 822 - cy0), (1090 - cx0, 822 - cy0),
        (1088 - cx0, 790 - cy0), (1082 - cx0, 720 - cy0), (1062 - cx0, 700 - cy0)]
ImageDraw.Draw(mask).polygon(poly, fill=255)
mask = mask.filter(ImageFilter.GaussianBlur(5))
im.paste(smooth, (cx0, cy0), mask)
buf = io.BytesIO(); im.save(buf, "JPEG", quality=95)
PHOTO = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
im.save("/home/claude/assets/ospiti.jpg", quality=95)

CSS = f"""
@font-face{{font-family:'SG';font-weight:700;src:url('file://{FB}/space-grotesk/files/space-grotesk-latin-700-normal.woff2')}}
@font-face{{font-family:'PS';font-weight:400;src:url('file://{FB}/ibm-plex-sans/files/ibm-plex-sans-latin-400-normal.woff2')}}
@font-face{{font-family:'PM';font-weight:500;src:url('file://{FB}/ibm-plex-mono/files/ibm-plex-mono-latin-500-normal.woff2')}}
*{{box-sizing:border-box;margin:0}}
body{{position:relative;overflow:hidden;font-family:'PS';background:#0C1633}}
.bg{{position:absolute;inset:0}}
.bg img{{position:absolute;display:block}}
.shade{{position:absolute;left:0;right:0;bottom:0}}
.logo{{position:absolute;left:72px;height:104px;background:#fff;border-radius:52px;padding:0 38px 0 24px;display:flex;align-items:center;gap:20px;box-shadow:0 14px 36px rgba(12,22,51,.28)}}
.logo svg{{width:60px;height:60px}}
.wm{{font-family:'SG';font-weight:700;font-size:44px;line-height:1;color:#0C1633;letter-spacing:-.01em}}
.cs{{font-family:'PM';font-weight:500;font-size:13px;letter-spacing:.26em;color:#FF2E5B;margin-top:6px}}
.eye{{position:absolute;left:72px;font-family:'PM';font-weight:500;font-size:25px;letter-spacing:.22em;text-transform:uppercase;color:#FF6E8E;display:flex;align-items:center;gap:20px}}
.eye:before{{content:'';width:44px;height:5px;background:#FF2E5B;border-radius:3px}}
h1{{position:absolute;left:72px;right:72px;font-family:'SG';font-weight:700;letter-spacing:-.025em;color:#fff;line-height:1.04}}
h1 em{{font-style:normal;color:#FF4D78}}
p.sub{{position:absolute;left:72px;right:72px;font-family:'PS';font-size:32px;line-height:1.38;color:#D5DCF2}}
.sticker{{position:absolute;background:#FF2E5B;color:#fff;font-family:'SG';font-weight:700;font-size:44px;line-height:1.05;padding:22px 32px;border-radius:30px;box-shadow:0 16px 36px rgba(255,46,91,.45)}}
"""
LOGO = '''<div class="logo" style="top:%dpx"><svg viewBox="0 0 168 168"><defs><clipPath id="c"><rect width="168" height="168" rx="48"/></clipPath></defs>
<g clip-path="url(#c)"><rect width="168" height="168" fill="#FF2B59"/>''' + "".join(
    f'<rect y="{i*19.82:.2f}" width="168" height="9.4" rx="4.7" fill="#11245A"/>' for i in range(9)) + '''</g></svg>
<div><div class="wm">Reagenta</div><div class="cs">CLINICAL SOLUTIONS</div></div></div>'''

POST = f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}body{{width:1080px;height:1350px}}</style></head><body>
<div class="bg"><img src="{PHOTO}" style="width:1080px;left:0;top:-30px"></div>
<div class="shade" style="top:700px;height:650px;background:linear-gradient(to bottom,rgba(12,22,51,0) 0,rgba(12,22,51,.88) 38%,rgba(12,22,51,.97) 100%)"></div>
{LOGO % 64}
<div class="eye" style="top:930px">Sede Reagenta · Monte di Procida</div>
<h1 style="top:992px;font-size:76px">Incontro con un<br><em>partner internazionale.</em></h1>
<p class="sub" style="top:1176px">Qualità, affidabilità e cooperazione: le basi<br>di una diagnostica in vitro al servizio dei laboratori.</p>
</body></html>"""

STORY = f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}body{{width:1080px;height:1920px}}</style></head><body>
<div class="bg"><img src="{PHOTO}" style="height:1920px;width:auto;left:-190px;top:0"></div>
<div class="shade" style="top:1080px;height:840px;background:linear-gradient(to bottom,rgba(12,22,51,0) 0,rgba(12,22,51,.9) 34%,rgba(12,22,51,.97) 100%)"></div>
{LOGO % 250}
<div class="eye" style="top:1380px">Sede Reagenta · Monte di Procida</div>
<h1 style="top:1440px;font-size:80px">Incontro con un<br><em>partner internazionale.</em></h1>
<p class="sub" style="top:1690px;font-size:32px">Diagnostica in vitro: qualità e affidabilità.</p>
</body></html>"""

with sync_playwright() as p:
    b = p.chromium.launch()
    for name, html, w, h in (("post-partner-internazionale", POST, 1080, 1350), ("story-partner-internazionale", STORY, 1080, 1920)):
        f = TMP / f"{name}.html"; f.write_text(html)
        pg = b.new_page(viewport={"width": w, "height": h})
        pg.goto("file://" + str(f)); pg.wait_for_timeout(800)
        pg.screenshot(path=str(OUT / f"{name}.png")); pg.close()
    b.close()
print("ok")
