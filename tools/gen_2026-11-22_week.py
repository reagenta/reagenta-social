import pathlib, html, sys
from playwright.sync_api import sync_playwright
F="file:///home/claude/social-build/node_modules/@fontsource"
P="file:///home/claude/social-build/prod"
OUT=pathlib.Path("/home/claude/reagenta-social/img/2026-11-22"); OUT.mkdir(parents=True,exist_ok=True)
TMP=pathlib.Path("/home/claude/social-build/out"); TMP.mkdir(exist_ok=True)
TH={
 'white':dict(bg='#fff',fg='#4A5478',h='#0C1633',em='#FF2E5B',eye='#4A5478',wm='#0C1633',sub='#FF2E5B',line='#EEF0F8',cnt='#7079A0',card='#F4F6FC',cardfg='#0C1633'),
 'soft':dict(bg='#F4F6FC',fg='#4A5478',h='#0C1633',em='#FF2E5B',eye='#4A5478',wm='#0C1633',sub='#FF2E5B',line='#E1E5F3',cnt='#7079A0',card='#fff',cardfg='#0C1633'),
 'navy':dict(bg='#0C1633',fg='#C9D0EC',h='#fff',em='#FF2E5B',eye='#C9D0EC',wm='#fff',sub='#FF6E8E',line='rgba(255,255,255,.18)',cnt='#C9D0EC',card='#fff',cardfg='#0C1633'),
 'mag':dict(bg='#FF2E5B',fg='#0C1633',h='#fff',em='#0C1633',eye='#0C1633',wm='#0C1633',sub='#0C1633',line='rgba(12,22,51,.25)',cnt='#0C1633',card='#fff',cardfg='#0C1633'),
}
CSS=f"""
@font-face{{font-family:'SG';font-weight:700;src:url('{F}/space-grotesk/files/space-grotesk-latin-700-normal.woff2')}}
@font-face{{font-family:'PS';font-weight:400;src:url('{F}/ibm-plex-sans/files/ibm-plex-sans-latin-400-normal.woff2')}}
@font-face{{font-family:'PS';font-weight:600;src:url('{F}/ibm-plex-sans/files/ibm-plex-sans-latin-600-normal.woff2')}}
@font-face{{font-family:'PM';font-weight:600;src:url('{F}/ibm-plex-mono/files/ibm-plex-mono-latin-600-normal.woff2')}}
*{{box-sizing:border-box;margin:0}}
body{{background:var(--bg);font-family:'PS';color:var(--fg);position:relative;overflow:hidden}}
.wrap{{position:absolute;left:80px;right:80px;display:flex;flex-direction:column}}
.head{{display:flex;align-items:center;gap:20px;padding-bottom:26px;border-bottom:2px solid var(--line)}}
.mark{{width:76px;height:76px}}
.wm{{font-family:'SG';font-weight:700;font-size:56px;color:var(--wm);line-height:1}}
.sub{{font-family:'PM';font-weight:600;font-size:15px;letter-spacing:.32em;color:var(--sub);margin-top:8px}}
.cnt{{margin-left:auto;font-family:'PM';font-weight:600;font-size:24px;letter-spacing:.2em;color:var(--cnt)}}
.eye{{display:flex;align-items:center;gap:18px;margin-top:50px;font-family:'PM';font-weight:600;font-size:24px;letter-spacing:.3em;color:var(--eye);text-transform:uppercase}}
.eye i{{display:block;width:48px;height:4px;background:var(--em)}}
h1{{font-family:'SG';font-weight:700;letter-spacing:-.02em;color:var(--h);margin-top:26px;line-height:1.04}}
h1 em{{font-style:normal;color:var(--em)}}
p{{font-size:38px;line-height:1.42;margin-top:26px}}
.num{{font-family:'SG';font-weight:700;line-height:.9;color:var(--em);letter-spacing:-.04em}}
.cardx{{background:var(--card);border-radius:34px;padding:42px 50px;color:var(--cardfg)}}
.cardx small{{display:block;font-family:'PM';font-weight:600;font-size:20px;letter-spacing:.25em;color:#FF2E5B;margin-bottom:14px;text-transform:uppercase}}
.cardx p{{margin-top:0;font-size:38px;font-weight:600;line-height:1.38;color:var(--cardfg)}}
.ph{{background:#fff;border-radius:34px;display:flex;align-items:center;justify-content:center;overflow:hidden}}
.ph img{{max-width:100%;max-height:100%;object-fit:contain}}
.nav{{border-radius:34px;background:#0C1633;position:relative;overflow:hidden;padding:42px 56px;color:#C9D0EC}}
.nav:after{{content:'';position:absolute;right:0;top:0;bottom:0;width:70px;background:repeating-linear-gradient(to bottom,rgba(255,46,91,.28) 0 3px,transparent 3px 8px)}}
.pill{{align-self:flex-start;background:#0C1633;color:#fff;font-family:'PM';font-weight:600;font-size:26px;letter-spacing:.24em;padding:28px 44px;border-radius:100px;text-transform:uppercase}}
.pill.w{{background:#fff;color:#0C1633}} .pill.m{{background:#FF2E5B;color:#fff}}
.chip{{display:inline-block;border-radius:100px;padding:18px 28px;font-family:'PM';font-weight:600;font-size:23px;letter-spacing:.1em;text-transform:uppercase}}
.lab{{font-family:'PM';font-weight:600;font-size:22px;letter-spacing:.28em;text-transform:uppercase;color:var(--eye)}}
"""
def mark():
    s=''.join(f'<rect y="{i*10}" width="100" height="5" fill="#FF2E5B"/>' for i in range(10))
    return f'<svg class="mark" viewBox="0 0 100 100"><defs><clipPath id="c"><rect width="100" height="100" rx="30"/></clipPath></defs><g clip-path="url(#c)"><rect width="100" height="100" fill="#0E2156"/>{s}</g></svg>'
def head(cnt=""):
    return f'<div class="head">{mark()}<div><div class="wm">Reagenta</div><div class="sub">CLINICAL SOLUTIONS</div></div><div class="cnt">{cnt}</div></div>'
def eye(t): return f'<div class="eye"><i></i>{t}</div>'
ARROW='<svg width="34" height="26" viewBox="0 0 34 26" style="margin-left:14px;vertical-align:-3px"><path d="M2 13h28M20 3l10 10-10 10" fill="none" stroke="#FF2E5B" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def scorri(cls=''): return f'<div class="pill {cls}" style="margin-top:auto">SCORRI{ARROW}</div>'
def ph(n,w,h,bg='#fff',pad=14,extra=''):
    return f'<div class="ph" style="width:{w}px;height:{h}px;background:{bg};{extra}"><img src="{P}/{n}.png" style="padding:{pad}px"></div>'
def big(t,sz=140,mt=60): return f'<h1 style="font-size:{sz}px;margin-top:{mt}px">{t}</h1>'
POST=(1080,1350,72,72); STORY=(1080,1920,250,250)
items={}
def add(name,size,theme,inner): items[name]=(size,theme,inner)
def S(name,theme,inner): add(name,STORY,theme,inner)

# ================= FEED =================
# F1 Lun 10:00 carosello 6 slide - navy - titolo gigante + checklist numerata
n='feed-lun-10-provetta-viola'
add(f'{n}-1',POST,'navy',head("1/6")+eye("Preanalitica")+'<h1 style="font-size:128px;margin-top:34px"><em>4 errori</em> da evitare con la provetta viola.</h1><div style="display:flex;justify-content:center;margin-top:30px">'+ph('vacumed',400,400,'#fff',10)+'</div>'+scorri('m'))
errs=[("01","Riempi fino al segno","Il volume di sangue deve essere quello previsto: segui il livello indicato sulla provetta."),
      ("02","Inverti subito, con delicatezza","Dopo il prelievo mescola come indicato dal produttore. Niente agitazione energica."),
      ("03","Rispetta l'ordine di prelievo","Segui il protocollo del tuo laboratorio: l'ordine delle provette evita contaminazioni tra additivi."),
      ("04","Conserva con tempi e temperature giusti","Quelli indicati dal produttore e dal tuo protocollo, non a memoria.")]
for i,(a,b,c) in enumerate(errs,2):
    add(f'{n}-{i}',POST,'navy',head(f"{i}/6")+eye("Errore "+a)+f'<div class="num" style="font-size:300px;margin-top:24px">{a}</div><h1 style="font-size:100px;margin-top:0">{b}</h1><div class="cardx" style="margin-top:auto"><p style="font-size:42px">{c}</p></div>')
add(f'{n}-6',POST,'navy',head("6/6")+eye("Provetta K3 EDTA")+'<h1 style="font-size:104px;margin-top:34px">3 ml, 13×75 mm, tappo viola. <em>Conf. da 100.</em></h1><div class="nav" style="margin-top:34px;background:#0E2156"><p style="margin:0;color:#fff;font-weight:600;font-size:38px;line-height:1.38;padding-right:50px">Vacumed® sottovuoto per esami ematologici. Prodotto per uso professionale.</p></div><div class="pill m" style="margin-top:auto">SALVA IL POST PER DOPO</div>')

# F2 Lun 18:00 domanda grande - magenta
add('feed-lun-18-domanda-preanalitica',POST,'mag',head()+eye("Domanda di mestiere")+'<h1 style="font-size:138px;margin-top:44px">Quale errore di preanalitica vi fa <em>rifare più prelievi?</em></h1><div style="display:flex;flex-wrap:wrap;gap:16px;margin-top:44px"><span class="chip" style="background:#fff;color:#0C1633">Identificazione</span><span class="chip" style="background:#fff;color:#0C1633">Volume</span><span class="chip" style="background:#fff;color:#0C1633">Emolisi</span><span class="chip" style="background:#fff;color:#0C1633">Tempi di consegna</span></div><div class="pill" style="margin-top:auto">RISPONDI NEI COMMENTI</div>')

# F3 Mar 10:00 foto grande + callout - soft
chp=''.join(f'<span class="chip" style="background:#0C1633;color:#fff">{t}</span>' for t in ["SARS-CoV-2","Influenza A+B","RSV","Adenovirus","M. pneumoniae"])
add('feed-mar-10-test-respiratorio',POST,'soft',head()+eye("Per la farmacia e l'ambulatorio")+'<h1 style="font-size:96px;margin-top:26px">Stagione respiratoria: <em>un tampone, più target.</em></h1><div style="display:flex;justify-content:center;margin-top:28px">'+ph('combo',760,440,'#fff',6)+'</div><div style="display:flex;flex-wrap:wrap;gap:12px;margin-top:26px">'+chp+'</div><p style="font-size:30px;margin-top:22px;margin-bottom:0">Esito in 15 minuti · uso professionale CE-IVD · interpretazione al medico.</p>')

# F4 Mar 18:00 card navy con righe magenta + foto - white
add('feed-mar-18-geneye-30-target',POST,'white',head()+eye("Il laboratorio al punto di cura")+'<h1 style="font-size:100px;margin-top:26px">Un campione, fino a <em>30 target.</em></h1><div class="nav" style="margin-top:34px;display:flex;align-items:center;gap:30px;padding:36px 80px 36px 36px">'+ph('geneye',420,420,'#fff',8)+'<div style="color:#fff"><div style="font-family:PM;font-weight:600;font-size:20px;letter-spacing:.3em;color:#FF6E8E">GENEYE GCP-30</div><div style="font-family:SG;font-weight:700;font-size:150px;line-height:.95;letter-spacing:-.04em;margin-top:10px">20<span style="font-size:60px"> min</span></div><div style="font-size:28px;line-height:1.35;color:#C9D0EC;margin-top:10px">Sistema multiplex POCT molecolare, rilevazione in fluorescenza in tempo reale.</div></div></div><p style="font-size:30px;margin-top:24px">Target e interpretazione dipendono dal kit utilizzato. Uso professionale.</p><div class="pill m" style="margin-top:auto">DETTAGLI SU REAGENTA.IT</div>')

# F5 Mer 10:00 carosello 5 - soft - timeline
n='feed-mer-10-dopo-installazione'
add(f'{n}-1',POST,'soft',head("1/5")+eye("Sul campo")+'<h1 style="font-size:122px;margin-top:34px">Dopo l\'installazione, <em>cosa succede?</em></h1><div style="display:flex;justify-content:center;margin-top:30px">'+ph('reagentapro',430,430,'#fff',8)+'</div>'+scorri('m'))
steps=[("Installazione","Messa in funzione dello strumento, con il nostro team."),("Validazione","Verifica del sistema presso la tua struttura."),("Formazione","Corso di formazione per il personale che lo userà."),("Assistenza","Assistenza tecnica in 24–48 ore.")]
def tline(k):
    r=''
    for j,(t,d) in enumerate(steps):
        if j==k:
            r+=f'<div style="display:flex;gap:26px;align-items:stretch;margin-top:34px"><div style="width:96px;height:96px;border-radius:50%;background:#FF2E5B;color:#fff;font-family:SG;font-weight:700;font-size:48px;display:flex;align-items:center;justify-content:center;flex:none">{j+1}</div><div class="nav" style="flex:1;padding:26px 90px 26px 40px"><div style="font-family:SG;font-weight:700;font-size:68px;color:#fff;line-height:1">{t}</div><div style="font-size:36px;line-height:1.3;color:#C9D0EC;margin-top:12px">{d}</div></div></div>'
        else:
            r+=f'<div style="display:flex;gap:26px;align-items:center;margin-top:34px"><div style="width:96px;height:96px;border-radius:50%;background:#fff;border:3px solid #C9D0EC;color:#7079A0;font-family:SG;font-weight:700;font-size:48px;display:flex;align-items:center;justify-content:center;flex:none">{j+1}</div><div style="font-family:SG;font-weight:700;font-size:60px;color:#7079A0;line-height:1">{t}</div></div>'
    return r
for i,k in enumerate(range(4),2):
    extra='<div class="pill m" style="margin-top:auto">CHIAMA LO 081 8045042</div>' if k==3 else ''
    add(f'{n}-{i}',POST,'soft',head(f"{i}/5")+eye(f"Passo {k+1} di 4")+f'<h1 style="font-size:84px;margin-top:22px">{["Si parte dall\'<em>installazione.</em>","Poi la <em>validazione.</em>","Poi la <em>formazione.</em>","E il servizio <em>continua.</em>"][k]}</h1><div style="margin-top:14px">{tline(k)}</div>{extra}')

# F6 Mer 18:00 numero eroe a tutta pagina - magenta
add('feed-mer-18-480-installazioni',POST,'mag',head()+eye("Sul campo, ogni giorno")+'<div class="num" style="font-size:370px;margin-top:40px;color:#0C1633">480+</div><h1 style="font-size:96px;margin-top:6px">installazioni <em style="color:#fff;font-style:normal">attive.</em></h1><p style="font-size:42px;font-weight:600;color:#0C1633;max-width:880px">24 tecnici certificati. Oltre 25 anni di esperienza del team nella diagnostica.</p><div class="pill" style="margin-top:auto">RICHIEDI UNA QUOTAZIONE SU REAGENTA.IT</div>')

# F7 Gio 10:00 carosello 5 - navy - mito/fatto + GastroPanel
n='feed-gio-10-gastropanel'
add(f'{n}-1',POST,'navy',head("1/5")+eye("Mito o fatto?")+'<h1 style="font-size:104px;margin-top:30px">«Un test rapido sostituisce <em>la gastroscopia.»</em></h1><div style="display:flex;justify-content:center;margin-top:34px">'+ph('gastroquick',860,560,'#fff',20)+'</div>'+scorri('m'))
add(f'{n}-2',POST,'navy',head("2/5")+'<div style="display:flex;flex-direction:column;gap:22px;margin-top:40px;flex:1"><div style="background:#0E2156;border-radius:34px;padding:36px 48px;border:2px solid rgba(255,255,255,.18)"><div class="lab" style="color:#FF6E8E">Mito</div><div style="font-family:SG;font-weight:700;font-size:72px;line-height:1.08;color:#fff;margin-top:12px">GastroPanel sostituisce gli esami di approfondimento.</div></div><div style="background:#fff;border-radius:34px;padding:36px 48px;flex:1"><div class="lab" style="color:#FF2E5B">Fatto</div><div style="font-family:SG;font-weight:700;font-size:72px;line-height:1.08;color:#0C1633;margin-top:12px">Aiuta il medico a individuare chi ha bisogno di <span style="color:#FF2E5B">ulteriori approfondimenti</span>, come gastroscopia o biopsia.</div></div></div>')
bm=''.join(f'<div style="background:#fff;border-radius:30px;padding:44px 34px;flex:1 1 44%"><div style="font-family:SG;font-weight:700;font-size:{sz}px;color:#0C1633;line-height:1.05">{a}</div><div class="lab" style="margin-top:14px;font-size:22px;color:#FF2E5B">{b}</div></div>' for a,b,sz in [("PGI","Pepsinogeno I",110),("PGII","Pepsinogeno II",110),("G-17","Gastrina-17",110),("Anti-H. pylori","Anticorpi",64)])
add(f'{n}-3',POST,'navy',head("3/5")+eye("Cosa misura")+'<h1 style="font-size:104px;margin-top:26px">Quattro <em>biomarcatori,</em> un solo test.</h1><div style="display:flex;flex-wrap:wrap;gap:22px;margin-top:40px">'+bm+'</div><p style="font-size:34px;margin-top:auto">Su plasma EDTA. Il medico valuta il quadro nel suo insieme.</p>')
st=''.join(f'<div style="display:flex;align-items:center;gap:26px;background:rgba(255,255,255,.07);border-radius:28px;padding:22px 32px;margin-top:16px"><div style="font-family:SG;font-weight:700;font-size:68px;color:#FF2E5B;line-height:1;width:70px">{a}</div><div style="font-size:33px;line-height:1.28;color:#fff;font-weight:600">{b}</div></div>' for a,b in [("1","Plasma EDTA del paziente, secondo le istruzioni del test."),("2","Il campione si dispensa sul test: risultato in circa 15 minuti."),("3","Il GP Reader NT legge in automatico la cassetta.")])
add(f'{n}-4',POST,'navy',head("4/5")+eye("In 3 passi")+'<div style="display:flex;justify-content:center;margin-top:26px">'+ph('gpreader',640,430,'#fff',8)+'</div>'+st)
add(f'{n}-5',POST,'navy',head("5/5")+eye("Sul campo")+'<h1 style="font-size:100px;margin-top:30px">Installato a Caserta e a Soccavo, <em>con formazione del personale.</em></h1><div class="nav" style="margin-top:30px;background:#0E2156"><p style="margin:0;color:#fff;font-weight:600;font-size:36px;line-height:1.38;padding-right:50px">Casa di Cura San Michele e Istituto Diagnostico Varelli. Dispositivo per uso professionale CE-IVD: l\'interpretazione spetta al medico.</p></div><div class="pill m" style="margin-top:auto">RICHIEDI UNA QUOTAZIONE SU REAGENTA.IT</div>')

# F8 Gio 18:00 foto grande + callout - white
cl=''.join(f'<span class="chip" style="background:#0C1633;color:#fff">{t}</span>' for t in ["Sterile (EO)","Monouso","Teli con bordo adesivo","Universale"])
add('feed-gio-18-kit-chirurgico',POST,'white',head()+eye("Per ospedali e cliniche")+'<h1 style="font-size:92px;margin-top:26px">Il campo operatorio in <em>un\'unica confezione sterile.</em></h1><div style="margin-top:30px">'+ph('kit',920,380,'#F4F6FC',16)+'</div><div style="display:flex;flex-wrap:wrap;gap:12px;margin-top:26px">'+cl+'</div><div class="pill m" style="margin-top:auto">RICHIEDI UNA QUOTAZIONE SU REAGENTA.IT</div>')

# F9 Ven 10:00 split orizzontale navy/bianco - CLI1000
def page_split_h():
    n=TH['navy']; vn=';'.join(f'--{k}:{x}' for k,x in n.items())
    w=TH['white']; vw=';'.join(f'--{k}:{x}' for k,x in w.items())
    top=f'<div style="position:absolute;left:0;right:0;top:0;height:620px;background:#0C1633;{vn}"><div class="wrap" style="top:60px;bottom:0">{head()}{eye("Per il laboratorio")}<h1 style="font-size:92px;margin-top:24px">CLIA in laboratorio: <em>reagente monotest da 24.</em></h1></div></div>'
    st=''.join(f'<div style="display:flex;align-items:baseline;gap:18px;margin-top:20px"><span style="font-family:SG;font-weight:700;font-size:78px;color:#FF2E5B;line-height:1;letter-spacing:-.03em">{a}</span><span style="font-size:28px;line-height:1.2;color:#0C1633;font-weight:600">{b}</span></div>' for a,b in [("24","test per reagente monotest"),("8″","touchscreen per gestire l'analisi"),("LIS","collegamento e stampa integrata")])
    bot=f'<div style="position:absolute;left:0;right:0;top:620px;bottom:0;background:#fff;{vw}"><div class="wrap" style="top:44px;bottom:54px;flex-direction:row;gap:30px;align-items:center"><div style="flex:none;width:470px;height:470px;background:#F4F6FC;border-radius:34px;display:flex;align-items:center;justify-content:center"><img src="{P}/cli1000.png" style="width:100%;border-radius:34px"></div><div style="flex:1"><div class="lab" style="color:#4A5478">Lumicision CLI1000 · Assure Tech</div>{st}</div></div></div>'
    sep='<div style="position:absolute;left:0;right:0;top:620px;height:8px;background:#FF2E5B"></div>'
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS} body{{width:1080px;height:1350px;background:#fff}}</style></head><body>{top}{bot}{sep}</body></html>'
add('feed-ven-10-cli1000','split','split','')

# F10 Ven 18:00 griglia 3 servizi - soft
def icon(k):
    s={'tool':'<path d="M14 54 40 28M34 14a14 14 0 0 0 18 18l8 8a6 6 0 0 1-8 8l-8-8a14 14 0 0 1-10-26z" fill="none" stroke="#FF2E5B" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>',
       'cap':'<path d="M4 26 32 12l28 14-28 14zM16 34v14c8 8 24 8 32 0V34" fill="none" stroke="#FF2E5B" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>',
       'clock':'<circle cx="32" cy="32" r="24" fill="none" stroke="#FF2E5B" stroke-width="5"/><path d="M32 18v15l10 6" fill="none" stroke="#FF2E5B" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'}[k]
    return f'<svg width="84" height="84" viewBox="0 0 64 64">{s}</svg>'
def svc(k,t,d):
    return f'<div style="flex:1;min-width:0;background:#fff;border-radius:30px;padding:26px 22px;display:flex;flex-direction:column;gap:14px">{icon(k)}<div style="font-family:SG;font-weight:700;font-size:40px;color:#0C1633;line-height:1.05">{t}</div><div style="font-size:26px;line-height:1.3;color:#4A5478">{d}</div></div>'
add('feed-ven-18-tre-servizi',POST,'soft',head()+eye("Reagenta Pro in farmacia")+'<h1 style="font-size:86px;margin-top:24px">Reagenta Pro non arriva da solo: <em>arrivano 3 servizi.</em></h1><div style="display:flex;justify-content:center;margin-top:26px">'+ph('reagentapro',920,250,'#fff',2)+'</div><div style="display:flex;gap:18px;margin-top:22px">'+svc('tool','Installazione','Messa in funzione con il nostro team.')+svc('cap','Formazione','Corso per il personale.')+svc('clock','Assistenza','Intervento in 24–48 ore.')+'</div><div class="pill m" style="margin-top:auto">CHIAMA LO 081 8045042</div>')

# ================= STORIES =================
# LUN
S('story-lun-0850','navy',head()+eye("Domanda del giorno")+big('La provetta viola è riempita <em>al segno?</em>',112,34)+'<div style="display:flex;justify-content:center;margin-top:34px">'+ph('vacumed',440,440,'#fff',8)+'</div><p style="font-size:44px;margin-top:34px">Alle 10:00: 4 errori da evitare con la K3 EDTA.</p><div class="pill m" style="margin-top:auto">DETTAGLI NEL POST</div>')
S('story-lun-1310','white',head()+eye("Consiglio rapido")+'<div class="num" style="font-size:330px;margin-top:70px">01</div>'+big('Etichetta la provetta <em>al letto del paziente.</em>',112,20)+'<p style="font-size:46px">Un errore di identificazione non si corregge in laboratorio.</p><div class="pill m" style="margin-top:auto">SALVA PER DOPO</div>')
S('story-lun-1730','mag',head()+eye("Alle 18:00")+big('Quale errore vi fa <em>rifare più prelievi?</em>',130,70)+'<p style="font-size:48px;font-weight:600">Una domanda per chi lavora in laboratorio. Rispondi nel post.</p><div class="pill" style="margin-top:auto">DETTAGLI NEL POST</div>')
# MAR
S('story-mar-0850','soft',head()+eye("Domanda del giorno")+big('Quale test rapido vi chiedono di più <em>in questo periodo?</em>',120,70)+'<p style="font-size:48px">Scrivici in DM: ti rispondiamo con quello che abbiamo a catalogo.</p><div class="pill m" style="margin-top:auto">SCRIVICI IN DM</div>')
S('story-mar-1310','navy',head()+eye("Numero del giorno")+'<div class="num" style="font-size:270px;margin-top:40px;white-space:nowrap">5 min</div>'+big('lettura del test rapido <em>FOB.</em>',100,6)+'<div style="display:flex;justify-content:center;margin-top:34px">'+ph('fob',700,460,'#fff',10)+'</div><p style="font-size:38px;margin-top:30px">25 test per confezione · uso professionale.</p><div class="pill m" style="margin-top:auto">DETTAGLI SU REAGENTA.IT</div>')
S('story-mar-1730','mag',head()+eye("Alle 18:00")+big('Fino a <em>30 target</em> in un\'analisi.',120,40)+'<div style="display:flex;justify-content:center;margin-top:36px">'+ph('geneye',640,640,'#fff',8)+'</div><p style="font-size:44px;font-weight:600;margin-top:34px">GenEye GCP-30, POCT molecolare.</p><div class="pill" style="margin-top:auto">DETTAGLI NEL POST</div>')
# MER
S('story-mer-0850','white',head()+eye("Domanda del giorno")+big('Dopo l\'installazione, chi forma <em>il tuo personale?</em>',120,70)+'<p style="font-size:48px">Alle 10:00 i 4 passi che seguiamo.</p><div class="pill m" style="margin-top:auto">DETTAGLI NEL POST</div>')
def tl(a,b):
    return f'<div style="display:flex;align-items:center;gap:30px;background:rgba(255,255,255,.07);border-radius:30px;padding:24px 36px;margin-top:18px"><div style="font-family:SG;font-weight:700;font-size:80px;color:#FF2E5B;line-height:1;width:90px">{a}</div><div style="font-size:40px;line-height:1.2;color:#fff;font-weight:600">{b}</div></div>'
S('story-mer-1310','navy',head()+eye("Dietro le quinte")+big('Reagenta Pro, <em>in struttura.</em>',120,34)+'<div style="display:flex;justify-content:center;margin-top:30px">'+ph('reagentapro',420,420,'#fff',8)+'</div><div style="margin-top:14px">'+tl("1","Installazione")+tl("2","Validazione")+tl("3","Formazione")+'</div>')
S('story-mer-1730','mag',head()+eye("Alle 18:00")+'<div class="num" style="font-size:340px;margin-top:70px;color:#0C1633">480+</div>'+big('installazioni <em style="color:#fff;font-style:normal">attive.</em>',110,6)+'<p style="font-size:46px;font-weight:600">Dove? Nel post delle 18:00.</p><div class="pill" style="margin-top:auto">DETTAGLI NEL POST</div>')
# GIO
S('story-gio-0850','soft',head()+eye("Mito o fatto?")+big('GastroPanel sostituisce <em>la gastroscopia?</em>',112,34)+'<div style="display:flex;justify-content:center;margin-top:34px">'+ph('gastroquick',920,613,'#fff',18)+'</div><p style="font-size:44px;margin-top:34px">La risposta alle 10:00.</p><div class="pill m" style="margin-top:auto">DETTAGLI NEL POST</div>')
S('story-gio-1310','navy',head()+eye("FAQ")+big('Che campione serve? <em>Plasma EDTA.</em>',112,34)+'<div style="display:flex;justify-content:center;margin-top:30px">'+ph('gpreader',760,560,'#fff',8)+'</div><p style="font-size:38px;margin-top:30px">GastroPanel Quick Test NT: risultato in circa 15 minuti, letto dal GP Reader NT.</p><div class="pill m" style="margin-top:auto">SALVA PER DOPO</div>')
S('story-gio-1730','white',head()+eye("Alle 18:00")+big('Kit chirurgico <em>KUNIV PLUS.</em>',120,34)+'<div style="display:flex;justify-content:center;margin-top:34px">'+ph('kit',920,600,'#F4F6FC',24)+'</div><p style="font-size:44px;margin-top:34px">Sterile, monouso, in un\'unica confezione.</p><div class="pill m" style="margin-top:auto">DETTAGLI NEL POST</div>')
# VEN
S('story-ven-0850','mag',head()+eye("Spunto")+big('Ogni strumento ha un <em>referente tecnico</em> nel tuo laboratorio?',112,70)+'<p style="font-size:48px;font-weight:600">Raccontaci come lavorate: scrivici in DM.</p><div class="pill" style="margin-top:auto">SCRIVICI IN DM</div>')
S('story-ven-1310','navy',head()+eye("Servizio")+'<div class="num" style="font-size:240px;margin-top:60px;white-space:nowrap">24–48h</div>'+big('Assistenza tecnica: intervento in <em>24–48 ore.</em>',92,10)+'<p style="font-size:40px;font-weight:600;color:#fff">Hotline lun–ven 8:30–18:00 · 081 8045042</p><div class="pill m" style="margin-top:auto">CHIAMA LO 081 8045042</div>')
S('story-ven-1730','white',head()+eye("Alle 18:00")+big('Reagenta Pro non arriva <em>da solo.</em>',120,34)+'<div style="display:flex;justify-content:center;margin-top:34px">'+ph('reagentapro',620,620,'#F4F6FC',10)+'</div><p style="font-size:44px;margin-top:34px">Installazione, formazione, assistenza. Buon weekend dal team Reagenta.</p><div class="pill m" style="margin-top:auto">DETTAGLI NEL POST</div>')

def page(size,theme,inner):
    w,h,t,b=size
    th=TH[theme]
    v=';'.join(f'--{k}:{x}' for k,x in th.items())
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS} body{{width:{w}px;height:{h}px;{v}}} .wrap{{top:{t}px;bottom:{b}px}}</style></head><body><div class="wrap">{inner}</div></body></html>'
only=sys.argv[1:]
with sync_playwright() as p:
    b=p.chromium.launch()
    for name,(size,theme,inner) in items.items():
        if only and not any(name.startswith(o) for o in only): continue
        w,h=(1080,1350) if size=='split' else (size[0],size[1])
        pg=b.new_page(viewport={"width":w,"height":h})
        fn=TMP/f"{name}.html"; fn.write_text(page_split_h() if theme=='split' else page(size,theme,inner))
        pg.goto("file://"+str(fn)); pg.wait_for_timeout(400)
        pg.screenshot(path=str(OUT/f"{name}.png")); pg.close()
    b.close()
print(len(items))
