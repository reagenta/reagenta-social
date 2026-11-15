import pathlib, html, sys
from playwright.sync_api import sync_playwright
F="file:///home/claude/social-build/node_modules/@fontsource"
P="file:///home/claude/social-build/prod"
OUT=pathlib.Path("/home/claude/reagenta-social/img/2026-11-15"); OUT.mkdir(parents=True,exist_ok=True)
TMP=pathlib.Path("/home/claude/social-build/out")
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
.eye{{display:flex;align-items:center;gap:18px;margin-top:56px;font-family:'PM';font-weight:600;font-size:24px;letter-spacing:.3em;color:var(--eye);text-transform:uppercase}}
.eye i{{display:block;width:48px;height:4px;background:var(--em)}}
h1{{font-family:'SG';font-weight:700;letter-spacing:-.02em;color:var(--h);margin-top:28px;line-height:1.04}}
h1 em{{font-style:normal;color:var(--em)}}
p{{font-size:38px;line-height:1.42;margin-top:28px}}
.num{{font-family:'SG';font-weight:700;line-height:.9;color:var(--em);letter-spacing:-.04em}}
.cardx{{background:var(--card);border-radius:34px;padding:44px 50px;color:var(--cardfg)}}
.cardx small{{display:block;font-family:'PM';font-weight:600;font-size:20px;letter-spacing:.25em;color:#FF2E5B;margin-bottom:16px;text-transform:uppercase}}
.cardx p{{margin-top:0;font-size:40px;font-weight:600;line-height:1.38;color:var(--cardfg)}}
.ph{{background:#fff;border-radius:34px;display:flex;align-items:center;justify-content:center;overflow:hidden}}
.ph img{{max-width:100%;max-height:100%;object-fit:contain}}
.nav{{border-radius:34px;background:#0C1633;position:relative;overflow:hidden;padding:44px 56px;color:#C9D0EC}}
.nav:after{{content:'';position:absolute;right:0;top:0;bottom:0;width:70px;background:repeating-linear-gradient(to bottom,rgba(255,46,91,.28) 0 3px,transparent 3px 8px)}}
.nav p{{margin-top:0;color:#fff;font-weight:600;font-size:40px;line-height:1.38;padding-right:50px}}
.nav small{{display:block;font-family:'PM';font-weight:600;font-size:20px;letter-spacing:.3em;color:#FF6E8E;margin-bottom:14px;text-transform:uppercase}}
.pill{{align-self:flex-start;background:#0C1633;color:#fff;font-family:'PM';font-weight:600;font-size:26px;letter-spacing:.26em;padding:30px 46px;border-radius:100px;text-transform:uppercase}}
.pill.w{{background:#fff;color:#0C1633}} .pill.m{{background:#FF2E5B;color:#fff}}
.row{{display:flex;gap:28px}}
.lab{{font-family:'PM';font-weight:600;font-size:22px;letter-spacing:.28em;text-transform:uppercase;color:var(--eye)}}
"""
def mark():
    s=''.join(f'<rect y="{i*10}" width="100" height="5" fill="#FF2E5B"/>' for i in range(10))
    return f'<svg class="mark" viewBox="0 0 100 100"><defs><clipPath id="c"><rect width="100" height="100" rx="30"/></clipPath></defs><g clip-path="url(#c)"><rect width="100" height="100" fill="#0E2156"/>{s}</g></svg>'
def head(cnt=""):
    return f'<div class="head">{mark()}<div><div class="wm">Reagenta</div><div class="sub">CLINICAL SOLUTIONS</div></div><div class="cnt">{cnt}</div></div>'
def eye(t): return f'<div class="eye"><i></i>{t}</div>'
def img(n,w=None,h=None,bg='#fff',extra=''):
    return f'<div class="ph" style="width:{w}px;height:{h}px;background:{bg};{extra}"><img src="{P}/{n}.png" style="padding:16px"></div>'
ARROW='<svg width="34" height="26" viewBox="0 0 34 26" style="margin-left:14px;vertical-align:-3px"><path d="M2 13h28M20 3l10 10-10 10" fill="none" stroke="#FF2E5B" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def scorri(cls=''): return f'<div class="pill {cls}" style="margin-top:auto">SCORRI{ARROW}</div>'
POST=(1080,1350,72,72); STORY=(1080,1920,250,250)
items={}  # name -> (size, theme, inner, rawpage or None)
def add(name,size,theme,inner): items[name]=(size,theme,inner)


def ph(n,w,h,bg='#fff',pad=10):
    return f'<div class="ph" style="width:{w}px;height:{h}px;background:{bg}"><img src="{P}/{n}.png" style="padding:{pad}px"></div>'
def chip(t,sub,bg='#fff',fg='#0C1633'):
    return f'<div style="flex:1;background:{bg};border-radius:28px;padding:26px 22px;text-align:center"><div style="font-family:SG;font-weight:700;font-size:64px;line-height:1;color:#FF2E5B;letter-spacing:-.03em">{t}</div><div style="font-family:PM;font-weight:600;font-size:17px;letter-spacing:.14em;text-transform:uppercase;color:{fg};margin-top:12px;line-height:1.35">{sub}</div></div>'
def pillrow(items,bg='#fff',fg='#0C1633'):
    return ''.join(f'<div style="background:{bg};color:{fg};border-radius:100px;padding:20px 30px;font-family:PM;font-weight:600;font-size:25px;letter-spacing:.1em;text-transform:uppercase">{i}</div>' for i in items)


def tl(a,b):
    return f'<div style="display:flex;align-items:center;gap:30px;background:rgba(255,255,255,.07);border-radius:30px;padding:26px 36px"><div style="font-family:SG;font-weight:700;font-size:84px;color:#FF2E5B;line-height:1;width:110px">{a}</div><div style="font-family:SG;font-weight:700;font-size:52px;color:#fff;line-height:1.1">{b}</div></div>'
def dots(i,n,on='#FF2E5B',off='#C9D0EC'):
    return '<div style="display:flex;gap:10px;margin-top:28px">'+''.join(f'<span style="width:{70 if j==i else 26}px;height:14px;border-radius:8px;background:{on if j<=i else off}"></span>' for j in range(1,n+1))+'</div>'
def step(name,i,N,theme,lab,num,title,body,tsz=118,nsz=300,dk=False):
    add(f'{name}-{i}',POST,theme,head(f"{i}/{N}")+eye(lab)+f'<div class="num" style="font-size:{nsz}px;margin-top:26px">{num}</div><h1 style="font-size:{tsz}px;margin-top:0">{title}</h1><div class="cardx" style="margin-top:auto"><p style="font-size:36px">{body}</p></div>'+dots(i-1,N-1))


def ckd(i,t): return f'<div style="display:flex;align-items:center;gap:26px;border-bottom:2px solid rgba(255,255,255,.18);padding:16px 0"><div style="font-family:SG;font-weight:700;font-size:64px;color:#FF2E5B;width:100px">{i}</div><div style="font-family:SG;font-weight:700;font-size:42px;color:#fff;line-height:1.1">{t}</div></div>'
def stp(i,t,b,bg='#0C1633'):
    return f'<div style="display:flex;align-items:center;gap:34px;background:{bg};border-radius:34px;padding:34px 40px"><div style="font-family:SG;font-weight:700;font-size:110px;color:#FF2E5B;line-height:1;width:96px">{i}</div><div><div style="font-family:SG;font-weight:700;font-size:46px;color:#fff;line-height:1.1">{t}</div><div style="font-size:30px;color:#C9D0EC;margin-top:10px;line-height:1.35">{b}</div></div></div>'
def photo(n,w,h,bg='#fff',pad=14,center=True):
    d=f'<div class="ph" style="width:{w}px;height:{h}px;background:{bg};flex:none"><img src="{P}/{n}.png" style="padding:{pad}px"></div>'
    return f'<div style="display:flex;justify-content:center">{d}</div>' if center else d

# ===== FEED =====
# F1 Lun10 carosello VES miniiSED (soft)
n='feed-lun-10-ves-miniised'
add(f'{n}-1',POST,'soft',head("1/5")+eye("Per i laboratori")+'<h1 style="font-size:150px;margin-top:30px">VES in <em>15 secondi.</em></h1><p style="font-size:40px;margin-top:14px">Direttamente dalla provetta EDTA.</p><div style="margin-top:26px">'+photo('mini',560,430,'#fff',10)+'</div>'+scorri('m'))
for i,(lab,num,t,b,tsz,nsz) in enumerate([
 ("Cosa misura","01","Misura l'aggregazione dei globuli rossi",'Reologia fotometrica in ambiente chiuso. Il valore in mm/ora è correlato al metodo Westergren.',104,230),
 ("Campione","02","Nessuna preparazione del campione",'Analizza direttamente le provette primarie EDTA, da un\'unica posizione di caricamento.',104,230),
 ("Produttività","180","test all\'ora, dichiarati",'Dato dichiarato dal produttore, in un ingombro ridotto: pensato per chi ha poco spazio.',112,260)],2):
    step(n,i,5,'soft',lab,num,t,b,tsz,nsz)
add(f'{n}-5',POST,'soft',head("5/5")+eye("ALCOR miniiSED")+'<h1 style="font-size:96px;margin-top:40px">VES in 15 secondi? <em>Vediamolo insieme.</em></h1><div style="margin-top:20px">'+photo('mini',360,270,'#fff',10)+'</div><div class="nav" style="margin-top:auto"><small>Prenota una dimostrazione</small><p>Scrivici in DM<br>081 8045042 · reagenta.it</p></div>')
# F2 Lun18 checklist prima del prelievo (navy)
add('feed-lun-18-checklist-prelievo',POST,'navy',head()+eye("Checklist · da salvare")+'<h1 style="font-size:92px;margin-top:24px">Prima del prelievo: <em>5 controlli.</em></h1><div style="margin-top:16px">'+ckd("01","Identità e etichetta")+ckd("02","Provetta giusta per l\'esame")+ckd("03","Tecnica di prelievo")+ckd("04","Miscelazione e tempi")+ckd("05","Condizioni di invio")+'</div><p style="font-size:28px;margin-top:22px;color:#C9D0EC">Indicazioni generali: valgono le procedure del tuo laboratorio.</p>')
# F3 Mar10 LactoFAN (magenta, foto grande + callout)
add('feed-mar-10-lactofan2',POST,'mag',head()+eye("Strumento in ambulatorio")+'<h1 style="font-size:104px;margin-top:30px">LactoFAN 2: l\'<em>idrogeno</em> nel respiro.</h1><div style="margin-top:26px">'+photo('lacto',920,450,'#fff',12,False)+'</div><div style="display:flex;flex-wrap:wrap;gap:14px;margin-top:30px">'+pillrow(["Portatile","Touchscreen","Export USB","A batterie"],'#0C1633','#fff')+'</div>')
# F4 Mar18 Strep A (bianco, numero eroe)
add('feed-mar-18-strep-a-5-minuti',POST,'white',head()+eye("Test rapido Strep A")+'<div style="display:flex;align-items:flex-end;gap:30px;margin-top:20px"><div class="num" style="font-size:420px;margin-top:0">5</div><div style="font-family:SG;font-weight:700;font-size:96px;color:#0C1633;line-height:1;padding-bottom:30px">minuti</div></div><p style="font-size:38px;margin-top:6px">Antigene dello Streptococco di gruppo A da tampone faringeo. Lettura visiva.</p><div style="margin-top:24px">'+photo('strep',920,430,'#F4F6FC',10,False)+'</div><p style="font-size:26px;margin-top:16px">Uso professionale CE-IVD. Risultato da interpretare secondo le istruzioni per l\'uso.</p>')
# F5 Mer10 carosello case study Campanialab (navy)
n='feed-mer-10-case-campanialab'
add(f'{n}-1',POST,'navy',head("1/5")+eye("Case study · Camposano 2026")+'<h1 style="font-size:132px;margin-top:36px">Due sistemi, <em>un solo flusso.</em></h1><p style="font-size:38px;margin-top:10px">Il caso del Consorzio Campanialab.</p><div style="display:flex;justify-content:center;gap:24px;margin-top:30px">'+photo('rpro',420,340,'#fff',8,False)+photo('ave562',420,340,'#fff',20,False)+'</div>'+scorri('m'))
for i,(lab,num,t,b) in enumerate([("Fase 1","01","Installazione e validazione","Messa in funzione e validazione dei sistemi presso il Consorzio Campanialab di Camposano."),("Fase 2","02","Formazione e conferenza","Il corso ha presentato AVE-562 per l'automazione e la parassitologia, e il sistema da banco Reagenta Pro."),("Fase 3","03","Soluzioni quantitative integrate","Reagenta Pro integra la lettura quantitativa automatica di FOB, calprotectina ed H. pylori.")],2):
    step(n,i,5,'navy',lab,num,t,b,104,230)
add(f'{n}-5',POST,'navy',head("5/5")+eye("Il tuo laboratorio")+'<h1 style="font-size:112px;margin-top:40px">Vuoi un percorso <em>simile?</em></h1><p style="font-size:38px">Installazione, validazione e formazione del personale, con il nostro team.</p><div class="pill m" style="margin-top:44px">SCRIVICI IN DM</div><div class="nav" style="margin-top:auto"><small>Contatti</small><p>081 8045042<br>reagenta.it</p></div>')
# F6 Mer18 Open day Verdi (bianco, foto in alto)
add('feed-mer-18-openday-verdi',POST,'white',head()+'<div style="margin-top:34px">'+photo('rpro',920,560,'#F4F6FC',10,False)+'</div>'+eye("Caso sul campo · Salerno")+'<h1 style="font-size:92px;margin-top:20px">Open day in farmacia: una giornata <em>di test.</em></h1><p style="font-size:34px;margin-top:16px">Farmacia Verdi Mercatale: dimostrazione dal vivo di Reagenta Pro, formazione del personale, assistenza in 24–48 ore.</p>')
# F7 Gio10 mito/fatto H. pylori (sopra magenta, sotto bianco con foto)
add('feed-gio-10-mito-hpylori','raw','mf','')
# F8 Gio18 carosello FAQ Reagenta Pro (soft)
n='feed-gio-18-faq-reagenta-pro'
add(f'{n}-1',POST,'soft',head("1/5")+eye("Domande frequenti")+'<h1 style="font-size:140px;margin-top:30px">Reagenta Pro: <em>4 domande</em> prima di sceglierlo.</h1><div style="margin-top:20px">'+photo('rpro',480,340,'#fff',6)+'</div>'+scorri('m'))
for i,(lab,num,t,b,nsz) in enumerate([("Domanda 1","12","Quanti test insieme?","12 canali indipendenti con incubazione a 37 °C: puoi gestire test diversi contemporaneamente.",300),("Domanda 2","<20s","E il tempo di lettura?","Meno di 20 secondi per lettura, con tecnologia a microsfere di Europio. Fino a 144 test/ora.",250),("Domanda 3","10.000","Dove finiscono i risultati?","Touchscreen, stampa termica, memoria da 10.000 record e trasmissione al LIS, secondo configurazione.",210)],2):
    step(n,i,5,'soft',lab,num.replace('<','&lt;'),t,b,112,nsz)
add(f'{n}-5',POST,'soft',head("5/5")+eye("Domanda 4")+'<h1 style="font-size:112px;margin-top:40px">E dopo l\'installazione? <em>Ci siamo.</em></h1><p style="font-size:38px">Formazione del personale e assistenza tecnica con intervento in 24–48 ore.</p><div class="nav" style="margin-top:auto"><small>Parliamone</small><p>Scrivici in DM<br>081 8045042 · reagenta.it</p></div>')
# F9 Ven10 CLI1000 (navy, foto grande + chip)
add('feed-ven-10-cli1000',POST,'navy',head()+eye("Analizzatore CLIA")+'<h1 style="font-size:112px;margin-top:26px">CLIA anche in <em>poco spazio.</em></h1><div style="margin-top:24px">'+photo('cli',920,470,'#fff',10,False)+'</div><div class="row" style="margin-top:26px">'+chip("32","test/ora")+chip("8","campioni a bordo")+chip("12 kg","circa")+'</div><p style="font-size:30px;margin-top:20px">Lumicision CLI1000: reagenti monotest, touchscreen da 8", collegamento LIS.</p>')
# F10 Ven18 timeline assistenza (magenta)
add('feed-ven-18-assistenza-3-passi',POST,'mag',head()+eye("Assistenza tecnica")+'<h1 style="font-size:96px;margin-top:26px">Strumento fermo? <em>Ecco cosa succede.</em></h1><div style="display:flex;flex-direction:column;gap:20px;margin-top:34px">'+stp("1","Chiami o apri un ticket","081 8045042 · reagenta.it/assistenza · lun–ven 8:30–18:00")+stp("2","Presa in carico","Ricevi l'email con la tua richiesta e la priorità indicata.")+stp("3","Intervento in 24–48 ore","Con un contratto attivo, coda prioritaria con SLA.")+'</div>')

# ===== STORIES =====
def S(name,theme,inner): add(name,STORY,theme,inner)
def big(t,sz=140,mt=60): return f'<h1 style="font-size:{sz}px;margin-top:{mt}px">{t}</h1>'
def pl(t,c='m'): return f'<div class="pill {c}" style="margin-top:auto">{t}</div>'
S('story-lun-0850','white',head()+eye("Domanda del giorno")+big('Quanti secondi per un risultato di <em>VES?</em>',140,70)+'<p style="font-size:48px">Alle 10:00 la risposta, con il carosello.</p>'+pl('DETTAGLI NEL POST'))
S('story-lun-1310','navy',head()+eye("Numero del giorno")+'<div class="num" style="font-size:420px;margin-top:40px">180</div><h1 style="font-size:100px;margin-top:0">test/ora dichiarati, per la <em>VES.</em></h1><div style="margin-top:34px">'+photo('mini',720,440,'#fff',10)+'</div><p style="font-size:30px;margin-top:20px">ALCOR miniiSED · dato dichiarato dal produttore</p>')
S('story-lun-1730','mag',head()+eye("Alle 18:00")+big('Prima di prelevare: <em>5 controlli.</em>',140,70)+'<p style="font-size:48px;font-weight:600">La checklist da salvare e girare al tuo team.</p>'+pl('SALVA IL POST','w'))
S('story-mar-0850','soft',head()+eye("Lo sapevi?")+big('Nel respiro si misura <em>l\'idrogeno.</em>',140,70)+'<p style="font-size:48px">Alle 10:00 LactoFAN 2: come funziona lo strumento.</p>'+pl('DETTAGLI NEL POST'))
S('story-mar-1310','white',head()+eye("Dietro lo strumento")+'<div style="margin-top:36px">'+photo('lacto',920,640,'#F4F6FC',14,False)+'</div>'+big('Portatile. A batterie. <em>Export USB.</em>',104,40)+'<p style="font-size:40px">LactoFAN 2, per ambulatori e centri di gastroenterologia.</p>')
S('story-mar-1730','navy',head()+eye("Alle 18:00")+'<div style="display:flex;align-items:flex-end;gap:24px;margin-top:20px"><div class="num" style="font-size:360px">5</div><div style="font-family:SG;font-weight:700;font-size:96px;color:#fff;padding-bottom:36px">minuti</div></div><h1 style="font-size:100px;margin-top:0">Test rapido <em>Strep A.</em></h1><div style="margin-top:34px">'+photo('strep',820,520,'#fff',10)+'</div>'+pl('DETTAGLI NEL POST'))
S('story-mer-0850','mag',head()+eye("Caso sul campo")+big('Camposano: due sistemi, <em>un flusso.</em>',130,70)+'<p style="font-size:48px;font-weight:600">Alle 10:00 il caso del Consorzio Campanialab.</p>'+pl('SCORRI IL CAROSELLO','w'))
S('story-mer-1310','soft',head()+eye("Numero del giorno")+'<div class="num" style="font-size:360px;margin-top:20px">12</div><h1 style="font-size:100px;margin-top:0">canali indipendenti, <em>37 °C a bordo.</em></h1><div style="margin-top:34px">'+photo('rpro',780,520,'#fff',8)+'</div><p style="font-size:30px;margin-top:20px">Reagenta Pro CTA-FAG</p>')
S('story-mer-1730','navy',head()+eye("Alle 18:00")+big('Open day a Salerno, in <em>farmacia.</em>',120,60)+'<p style="font-size:44px">Farmacia Verdi Mercatale: un giorno di test e dimostrazione dal vivo.</p><div style="margin-top:30px">'+photo('rpro',760,480,'#fff',8)+'</div>'+pl('DETTAGLI NEL POST'))
S('story-gio-0850','mag',head()+eye("Mito o fatto?")+big('Per un test rapido H. pylori serve <em>uno strumento?</em>',112,70)+'<p style="font-size:48px;font-weight:600">Il fatto, alle 10:00.</p>'+pl('DETTAGLI NEL POST','w'))
S('story-gio-1310','white',head()+eye("Domanda frequente")+big('Dove finiscono i risultati? <em>Stampa, memoria, LIS.</em>',104,50)+'<div style="margin-top:34px">'+photo('rpro',800,600,'#F4F6FC',8)+'</div><p style="font-size:38px;margin-top:24px">Reagenta Pro, secondo configurazione.</p>')
S('story-gio-1730','navy',head()+eye("Alle 18:00")+big('Reagenta Pro: <em>4 domande</em> prima di sceglierlo.',110,60)+'<div style="margin-top:30px">'+photo('rpro',760,520,'#fff',8)+'</div><p style="font-size:42px;margin-top:20px">Il carosello da scorrere e salvare.</p>'+pl('SCORRI IL CAROSELLO'))
S('story-ven-0850','white',head()+eye("Strumenti")+big('CLIA in poco spazio: <em>circa 12 kg.</em>',120,60)+'<div style="margin-top:30px">'+photo('cli',760,540,'#F4F6FC',8)+'</div><p style="font-size:42px;margin-top:20px">Alle 10:00 Lumicision CLI1000.</p>'+pl('DETTAGLI NEL POST'))
S('story-ven-1310','navy',head()+eye("Servizio")+'<div class="num" style="font-size:168px;margin-top:60px;white-space:nowrap">8:30–18:00</div><h1 style="font-size:100px;margin-top:20px">Hotline tecnica <em>081 8045042.</em></h1><p style="font-size:44px">Lun–ven. Intervento in 24–48 ore.</p>'+pl('SCRIVICI IN DM'))
S('story-ven-1730','soft',head()+eye("Buon weekend")+big('Strumento fermo? Ecco <em>come funziona l\'assistenza.</em>',104,70)+'<p style="font-size:48px">Alle 18:00 i 3 passi, nel post.</p>'+pl('DETTAGLI NEL POST'))

def page(size,theme,inner):
    w,h,t,b=size
    th=TH[theme]
    v=';'.join(f'--{k}:{x}' for k,x in th.items())
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS} body{{width:{w}px;height:{h}px;{v}}} .wrap{{top:{t}px;bottom:{b}px}}</style></head><body><div class="wrap">{inner}</div></body></html>'
def page_mf():
    m=TH['mag']; vm=';'.join(f'--{k}:{x}' for k,x in m.items())
    w=TH['white']; vw=';'.join(f'--{k}:{x}' for k,x in w.items())
    top=f'<div style="position:absolute;left:0;right:0;top:0;height:640px;background:#FF2E5B;{vm}"><div class="wrap" style="top:60px;bottom:0">{head()}{eye("Mito")}<h1 style="font-size:88px;margin-top:26px">«Per un test rapido H. pylori serve <em>uno strumento.</em>»</h1></div></div>'
    bot=f'<div style="position:absolute;left:0;right:0;top:640px;bottom:0;background:#fff;{vw}"><div class="wrap" style="top:56px;bottom:50px;flex-direction:row;gap:30px"><div style="flex:1;display:flex;flex-direction:column">{eye("Fatto")}<h1 style="font-size:58px;margin-top:20px;line-height:1.08">È una cassetta: lettura visiva in 5 minuti, <em>nessuna strumentazione.</em></h1><p style="font-size:26px;margin-top:20px;line-height:1.4">Test su feci per uso professionale CE-IVD. Il risultato va interpretato da personale qualificato e, se necessario, confermato in laboratorio.</p></div><div style="width:360px;display:flex;align-items:center">{photo("hp",360,300,"#F4F6FC",8,False)}</div></div></div>'
    sep='<div style="position:absolute;left:0;right:0;top:640px;height:8px;background:#0C1633"></div>'
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS} body{{width:1080px;height:1350px;background:#fff}}</style></head><body>{top}{bot}{sep}</body></html>'
only=sys.argv[1:]
with sync_playwright() as p:
    b=p.chromium.launch()
    for name,(size,theme,inner) in items.items():
        if only and not any(name.startswith(o) for o in only): continue
        w,h=(1080,1350) if size=='raw' else (size[0],size[1])
        pg=b.new_page(viewport={"width":w,"height":h})
        fn=TMP/f"{name}.html"; fn.write_text(page_mf() if theme=='mf' else page(size,theme,inner))
        pg.goto("file://"+str(fn)); pg.wait_for_timeout(500)
        pg.screenshot(path=str(OUT/f"{name}.png")); pg.close()
    b.close()
print(len(items))
