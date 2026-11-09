"""Copertine per la griglia Instagram (1080x1920, contenuto nella zona centrale 3:4 = y 240-1680)."""
import pathlib, sys
from reels_engine import *
import reels_art as A, reels_art2 as B
from reels_pilot import K
OUT = pathlib.Path("/home/claude/reagenta-social/covers"); OUT.mkdir(exist_ok=True)

def cover(theme, eye_t, title, tsize, em, art, zoom=1.0, extra=None):
    s = Scene(0, 10, theme); svg, js = art
    s.add(eye(eye_t), "fade", 0.0)
    s.words(title, tsize, d0=0.1, step=0.02, em=em, mt=30)
    s.ill(svg, js, d=0.35, dur=0.1, style=f"margin-top:30px;zoom:{zoom};align-self:center")
    if extra: s.add(extra, "fade", 0.0, 0.1)
    return s

photo = f'<div class="ph" style="height:640px;margin-top:40px;background:#F4F6FC"><img src="{P}/ave562.png" style="padding:10px"></div>'
nums = '<div style="display:flex;gap:14px;justify-content:center;margin-top:36px">' + ''.join(f'<div style="width:70px;height:70px;border-radius:50%;background:#0C1633;color:#fff;font-family:SG;font-weight:700;font-size:38px;display:flex;align-items:center;justify-content:center">{i+1}</div>' for i in range(7)) + '</div>'
def a(fn): return fn()
COVERS = [
 ("01-preanalitica", cover('navy', "Il caso del bancone", "Il campione può peggiorare. Dove?", 124, (4,), a(A.r1_hook), .9)),
 ("02-mito-fob-calprotectina", cover('mag', "Laboratorio", "Mito o fatto?", 190, (2,), a(B.r2_hook), .9)),
 ("03-ave562-7-passi", cover('white', "AVE-562", "L'esame delle feci in 7 passi", 124, (4, 5), (photo + nums, ""), 1.0)),
 ("04-centrifugazione", cover('mag', "Domanda di mestiere", "Quanto aspetti prima di centrifugare?", 112, (4,), a(B.r4_timer), .9)),
 ("05-ivdr", cover('white', "Qualità e norme", "IVDR: le scadenze", 150, (1,), a(B.r5_timeline), 1.0)),
 ("06-elisa-clia", cover('mag', "Immunodiagnostica", "Colore o luce?", 190, (2,), a(B.r6_vs), 1.0)),
 ("07-hil", cover('soft', "Preanalitica", "Emolisi, lipemia, ittero.", 128, (2,), a(B.r7_hook3), 1.0)),
 ("08-rapido-laboratorio", cover('soft', "Appropriatezza", "Test rapido o laboratorio?", 128, (2, 3), a(B.r8_scale), 1.0)),
 ("09-manutenzione", cover('white', "Checklist del tecnico", "5 controlli di manutenzione", 128, (0,), a(B.r9_gear), .95)),
 ("10-automatizzare", cover('navy', "Domanda del venerdì", "Cosa automatizzeresti?", 104, (1,), a(B.r10_gears), .95)),
]
if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    work = pathlib.Path("/tmp/claude-0/covwork"); work.mkdir(exist_ok=True)
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
        for name, sc in COVERS:
            h = build("c" + name, 10, [sc], work)
            t = h.read_text()
            t = t.replace("</style>", "#pbw{display:none}#gh{top:290px!important}.sc .wrap{top:290px!important;bottom:240px!important}</style>", 1)
            h.write_text(t)
            pg.goto("file://" + str(h)); pg.wait_for_timeout(800)
            pg.evaluate("seek(4.2)"); pg.wait_for_timeout(100)
            pg.screenshot(path=str(OUT / f"cover-{name}.png"))
        b.close()
    from PIL import Image
    fs = sorted(OUT.glob("cover-*.png")); W = Image.new("RGB", (360 * 5 + 40, 480 * 2 + 10), "#fff")
    for i, f in enumerate(fs):
        im = Image.open(f).convert("RGB").crop((0, 240, 1080, 1680)).resize((360, 480)); W.paste(im, ((i % 5) * 370, (i // 5) * 490))
    W.save("/tmp/claude-0/grid-preview.png")
    print(len(fs))
