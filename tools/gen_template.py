import pathlib, html
from playwright.sync_api import sync_playwright
F="file:///home/claude/social-build/node_modules/@fontsource"
CSS=f"""
@font-face{{font-family:'SG';font-weight:700;src:url('{F}/space-grotesk/files/space-grotesk-latin-700-normal.woff2')}}
@font-face{{font-family:'PS';font-weight:400;src:url('{F}/ibm-plex-sans/files/ibm-plex-sans-latin-400-normal.woff2')}}
@font-face{{font-family:'PS';font-weight:600;src:url('{F}/ibm-plex-sans/files/ibm-plex-sans-latin-600-normal.woff2')}}
@font-face{{font-family:'PM';font-weight:600;src:url('{F}/ibm-plex-mono/files/ibm-plex-mono-latin-600-normal.woff2')}}
*{{box-sizing:border-box;margin:0}}
body{{background:#fff;font-family:'PS';color:#4A5478;position:relative;overflow:hidden}}
.wrap{{position:absolute;left:80px;right:80px;display:flex;flex-direction:column}}
.head{{display:flex;align-items:center;gap:20px;padding-bottom:26px;border-bottom:2px solid #EEF0F8}}
.mark{{width:76px;height:76px}}
.wm{{font-family:'SG';font-weight:700;font-size:56px;color:#0C1633;line-height:1}}
.sub{{font-family:'PM';font-weight:600;font-size:15px;letter-spacing:.32em;color:#FF2E5B;margin-top:8px}}
.cnt{{margin-left:auto;font-family:'PM';font-weight:600;font-size:24px;letter-spacing:.2em;color:#7079A0}}
.eye{{display:flex;align-items:center;gap:18px;margin-top:64px;font-family:'PM';font-weight:600;font-size:24px;letter-spacing:.3em;color:#4A5478;text-transform:uppercase}}
.eye i{{display:block;width:48px;height:4px;background:#FF2E5B}}
h1{{font-family:'SG';font-weight:700;letter-spacing:-.02em;color:#0C1633;margin-top:30px;line-height:1.04}}
h1 em{{font-style:normal;color:#FF2E5B}}
p{{font-size:38px;line-height:1.45;margin-top:30px}}
.soft{{background:#F4F6FC;border-radius:34px;padding:46px 52px;margin-top:44px}}
.soft p{{margin-top:0;font-size:40px;color:#0C1633;font-weight:600;line-height:1.4}}
.soft small{{display:block;font-family:'PM';font-weight:600;font-size:20px;letter-spacing:.25em;color:#FF2E5B;margin-bottom:18px;text-transform:uppercase}}
.num{{font-family:'SG';font-weight:700;font-size:260px;line-height:.9;color:#FF2E5B;margin-top:34px;letter-spacing:-.04em}}
.card{{margin-top:auto;border-radius:34px;background:#0C1633;position:relative;overflow:hidden;display:flex;align-items:center;padding:0 52px;gap:46px}}
.card:after{{content:'';position:absolute;right:0;top:0;bottom:0;width:70px;background:repeating-linear-gradient(to bottom,rgba(255,46,91,.28) 0 3px,transparent 3px 8px)}}
.lab{{font-family:'PM';font-weight:600;font-size:20px;letter-spacing:.3em;color:#FF6E8E;text-transform:uppercase}}
.big{{font-family:'SG';font-weight:700;color:#fff;line-height:.95}}
.card .t{{color:#C9D0EC;font-size:30px;line-height:1.4}}
.pill{{margin-top:auto;align-self:flex-start;background:#0C1633;color:#fff;font-family:'PM';font-weight:600;font-size:26px;letter-spacing:.28em;padding:30px 48px;border-radius:100px}}
.pill b{{color:#FF2E5B;font-weight:600}}
"""
def mark():
    s=''.join(f'<rect y="{i*10}" width="100" height="5" fill="#FF2E5B"/>' for i in range(10))
    return f'<svg class="mark" viewBox="0 0 100 100"><defs><clipPath id="c"><rect width="100" height="100" rx="30"/></clipPath></defs><g clip-path="url(#c)"><rect width="100" height="100" fill="#0E2156"/>{s}</g></svg>'
def head(cnt=""):
    return f'<div class="head">{mark()}<div><div class="wm">Reagenta</div><div class="sub">CLINICAL SOLUTIONS</div></div><div class="cnt">{cnt}</div></div>'
def page(w,h,top,bottom,inner):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS} body{{width:{w}px;height:{h}px}} .wrap{{top:{top}px;bottom:{bottom}px}}</style></head><body><div class="wrap">{inner}</div></body></html>'
def stand_card(h, extra):
    return f'<div class="card" style="height:{h}px"><div><div class="lab">Stand</div><div class="big" style="font-size:170px">574</div></div><div class="t">{extra}</div></div>'

POST=(1080,1350,72,72); STORY=(1080,1920,250,250)
out={}
# ---- carousel 1..5
out['carosello-1']=(POST,head("1/5")+'<div class="eye"><i></i>Per la farmacia</div><h1 style="font-size:112px"><em>3 domande</em> prima di portare un laboratorio da banco in farmacia.</h1><div class="pill">SCORRI<svg width="34" height="26" viewBox="0 0 34 26" style="margin-left:14px;vertical-align:-3px"><path d="M2 13h28M20 3l10 10-10 10" fill="none" stroke="#FF2E5B" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg></div>')
qs=[("Chi forma il tuo personale?","Formazione","Il personale va formato su come usare lo strumento, non lasciato da solo con un manuale."),
    ("Chi interviene se serve assistenza?","Assistenza","Un referente tecnico e tempi chiari: da noi l'assistenza tecnica arriva in 24–48 ore."),
    ("Come avviene l'installazione?","Installazione","L'avvio va seguito da chi conosce lo strumento: installazione e messa in funzione con il nostro team.")]
for i,(q,lab,a) in enumerate(qs,1):
    out[f'carosello-{i+1}']=(POST,head(f"{i+1}/5")+f'<div class="num">0{i}</div><h1 style="font-size:92px;margin-top:10px">{html.escape(q)}</h1><div class="soft" style="margin-top:auto;height:340px;display:flex;flex-direction:column;justify-content:center"><small>{lab}</small><p>{html.escape(a)}</p></div>')
out['carosello-5']=(POST,head("5/5")+'<div class="eye"><i></i>Ci vediamo a Pharmexpo</div><h1 style="font-size:112px">Ne parliamo <em>di persona.</em></h1><p style="max-width:860px">Mostra d\'Oltremare, Napoli · 23–25 ottobre</p>'+stand_card(300,"081 8045042<br>ordini@reagenta.it<br>reagenta.it"))
# ---- countdown post 18:00
out['post-domani-pharmexpo']=(POST,head()+'<div class="eye"><i></i>Pharmexpo 2026 · Napoli</div><div class="num" style="font-size:150px;margin-top:40px;color:#0C1633">DOMANI</div><h1 style="font-size:96px;margin-top:6px">Apriamo lo stand <em>alle 10:00.</em></h1><p>Mostra d\'Oltremare, Napoli. Dal 23 al 25 ottobre.</p>'+stand_card(300,"Ven 23 e Sab 24<br>10:00 – 18:00<br>Dom 25 · 10:00 – 15:00"))
# ---- stories
out['story-1-numeri']=(STORY,head()+'<div class="eye"><i></i>Il tuo partner per la diagnostica</div><h1 style="font-size:150px;margin-top:40px"><em>5.700+</em> referenze.</h1><p style="font-size:46px">Strumenti, reagenti e materiale di consumo per laboratori, ospedali e professionisti.</p><div class="card" style="height:280px"><div><div class="big" style="font-size:96px">60+</div><div class="lab" style="margin-top:12px">Produttori</div></div><div><div class="big" style="font-size:96px">24/48h</div><div class="lab" style="margin-top:12px">Spedizione tracciata</div></div></div>')
out['story-2-servizi']=(STORY,head()+'<div class="eye"><i></i>Reagenta Pro in farmacia</div><h1 style="font-size:130px;margin-top:40px">Non solo uno strumento. <em>Un servizio.</em></h1><div class="soft" style="margin-top:50px"><small>Con lo strumento</small><p>Installazione<br>Assistenza tecnica in 24–48 ore<br>Formazione del personale</p></div><div class="pill" style="margin-top:auto">SCRIVICI <b>IN DM</b></div>')
out['story-3-countdown']=(STORY,head()+'<div class="eye"><i></i>Pharmexpo 2026</div><div class="num" style="font-size:190px;margin-top:50px;color:#0C1633">DOMANI</div><h1 style="font-size:120px;margin-top:10px">Ci trovi allo <em>stand 574.</em></h1>'+stand_card(340,"Mostra d'Oltremare<br>Viale Kennedy 54<br>Napoli · dalle 10:00"))
with sync_playwright() as p:
    b=p.chromium.launch()
    for name,((w,h,t,bo),inner) in out.items():
        pg=b.new_page(viewport={"width":w,"height":h})
        fn=pathlib.Path(f"out/2026-10-22/{name}.html"); fn.write_text(page(w,h,t,bo,inner))
        pg.goto("file://"+str(fn.resolve())); pg.wait_for_timeout(500)
        pg.screenshot(path=f"out/2026-10-22/{name}.png"); pg.close()
    b.close()
# contact sheet for QA
from PIL import Image
names=list(out)
ims=[Image.open(f"out/2026-10-22/{n}.png").convert("RGB") for n in names]
th=[im.resize((int(im.width*600/im.height),600)) for im in ims]
W=sum(i.width for i in th[:5])+60; sheet=Image.new("RGB",(W,1240),"#888")
x=10
for im in th[:5]: sheet.paste(im,(x,10)); x+=im.width+10
x=10
for im in th[5:]: sheet.paste(im,(x,620)); x+=im.width+10
sheet.save("out/2026-10-22/_sheet.png"); print(names)
