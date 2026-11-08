import pathlib, html, sys
from playwright.sync_api import sync_playwright
F="file:///home/claude/social-build/node_modules/@fontsource"
P="file:///home/claude/social-build/prod"
OUT=pathlib.Path("/home/claude/reagenta-social/img/2026-11-09"); OUT.mkdir(parents=True,exist_ok=True)
TMP=pathlib.Path("/home/claude/social-build/out"); 
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

# ============ FEED ============
# F1 Lun 10 carosello checklist prelievo (soft)
n='feed-lun-10-checklist'
add(f'{n}-1',POST,'soft',head("1/6")+eye("Per il laboratorio")+'<h1 style="font-size:136px">Prima del prelievo: <em>4 controlli.</em></h1><div style="display:flex;justify-content:center;margin-top:30px">'+ph('vacumed',520,470)+'</div>'+scorri())
chk=[("01","Identità","Etichetta e richiesta corrispondono. Si parte da qui."),("02","Provetta giusta","Colore del tappo e additivo adatti all'esame richiesto."),("03","Scadenza","Data di scadenza e confezione integra, ogni volta."),("04","Riempimento","Volume indicato e miscelazione come da istruzioni del produttore.")]
for i,(a,b,c) in enumerate(chk,2):
    dots=''.join(f'<span style="width:{70 if j==i-1 else 26}px;height:14px;border-radius:8px;background:{"#FF2E5B" if j<=i-1 else "#C9D0EC"}"></span>' for j in range(1,5))
    add(f'{n}-{i}',POST,'soft',head(f"{i}/6")+eye("Controllo "+a)+f'<div class="num" style="font-size:340px;margin-top:30px">{a}</div><h1 style="font-size:128px;margin-top:0">{b}</h1><div class="cardx" style="margin-top:auto"><p>{c}</p></div><div style="display:flex;gap:10px;margin-top:30px">{dots}</div>')
add(f'{n}-6',POST,'soft',head("6/6")+eye("Da salvare")+'<h1 style="font-size:104px">La checklist <em>in 4 righe.</em></h1><div class="nav" style="margin-top:40px"><p>1. Identità<br>2. Provetta e additivo<br>3. Scadenza e integrità<br>4. Riempimento e miscelazione</p></div><p style="font-size:30px">Indicazioni generali: valgono sempre le istruzioni d\'uso del produttore.</p><div class="pill m" style="margin-top:auto">SALVA E CONDIVIDI</div>')
# F2 Lun 18 numero eroe assistenza (magenta)
add('feed-lun-18-assistenza',POST,'mag',head()+eye("Assistenza tecnica")+'<div class="num" style="font-size:250px;margin-top:70px;color:#fff;white-space:nowrap">24–48h</div><h1 style="font-size:98px;margin-top:20px">Quando serve, l\'intervento arriva <em>in 24–48 ore.</em></h1><p style="font-size:38px;font-weight:600">Hotline tecnica 081 8045042<br>Lun–Ven 8:30–18:00</p><div class="pill" style="margin-top:auto">CHIAMA LO 081 8045042</div>')
# F3 Mar 10 AutoLumo S900 (navy) foto grande + callout
add('feed-mar-10-autolumo',POST,'navy',head()+eye("Strumento in uso · CLIA")+'<h1 style="font-size:92px;margin-top:20px">Un analizzatore CLIA compatto <em>per laboratori di medie dimensioni.</em></h1><div style="margin-top:26px;display:flex;justify-content:center">'+ph('autolumo',700,380)+'</div><div class="row" style="margin-top:26px">'+chip("180","test / ora")+chip("19 min","primo risultato")+chip("51","campioni a bordo")+'</div><p style="font-size:25px;margin-top:16px;line-height:1.3">AutoLumo S900 · random access, 3 posizioni STAT. Analiti e condizioni secondo i reagenti compatibili.</p>')
# F4 Mar 18 carosello combo respiratorio (bianco)
n='feed-mar-18-combo'
add(f'{n}-1',POST,'white',head("1/5")+eye("Per la farmacia")+'<h1 style="font-size:128px">Un solo tampone, <em>6 target</em> respiratori.</h1><div style="display:flex;justify-content:center;margin-top:30px">'+ph('combo',520,380,'#F4F6FC')+'</div>'+scorri())
add(f'{n}-2',POST,'white',head("2/5")+eye("Cosa rileva")+'<h1 style="font-size:112px">6 antigeni in un <em>unico test.</em></h1><div style="display:flex;flex-wrap:wrap;gap:16px;margin-top:40px">'+pillrow(["SARS-CoV-2","Influenza A","Influenza B","RSV","Adenovirus","Mycoplasma pneumoniae"],'#F4F6FC')+'</div><div class="cardx" style="margin-top:auto;background:#F4F6FC"><small>Campione</small><p>Tampone nasofaringeo, test immunocromatografico a cassetta.</p></div>')
add(f'{n}-3',POST,'white',head("3/5")+eye("Tempi")+'<div class="num" style="font-size:300px;margin-top:60px;white-space:nowrap">15 min</div><h1 style="font-size:100px;margin-top:10px">Esito <em>in 15 minuti.</em></h1><div class="cardx" style="margin-top:auto;background:#F4F6FC"><p>Kit completo, pronto all\'uso, senza strumentazione aggiuntiva.</p></div>')
add(f'{n}-4',POST,'white',head("4/5")+eye("Dove si usa")+'<h1 style="font-size:112px">Per chi lavora <em>in prima linea.</em></h1><div class="nav" style="margin-top:44px"><p>Farmacie<br>Laboratori di analisi<br>Ambulatori e poliambulatori<br>Strutture sanitarie</p></div>')
add(f'{n}-5',POST,'white',head("5/5")+eye("Da ricordare")+'<h1 style="font-size:106px">Uso professionale, <em>lettura al medico.</em></h1><p>Dispositivo diagnostico in vitro per uso professionale: l\'interpretazione del risultato spetta al medico.</p><div class="nav" style="margin-top:auto"><small>Richiedi una quotazione</small><p>reagenta.it<br>081 8045042</p></div>')
# F5 Mer 10 carosello Farmacia Verdi Mercatale (soft)
n='feed-mer-10-verdi'
add(f'{n}-1',POST,'soft',head("1/5")+eye("Sul campo · Salerno")+'<h1 style="font-size:112px">Una farmacia, un open day, <em>un laboratorio da banco.</em></h1><div style="display:flex;justify-content:center;margin-top:24px">'+ph('reagpro',500,420)+'</div>'+scorri())
vs=[("01","Open day","Una giornata intera di test, plaque test compresi."),("02","Dal vivo","Dimostrazione dal vivo dello strumento, direttamente in farmacia."),("03","Nuovi servizi","Il laboratorio da banco affianca i servizi già attivi in farmacia.")]
for i,(a,b,c) in enumerate(vs,2):
    add(f'{n}-{i}',POST,'soft',head(f"{i}/5")+eye("Farmacia Verdi Mercatale")+f'<div class="num" style="font-size:300px;margin-top:30px">{a}</div><h1 style="font-size:128px;margin-top:0">{b}</h1><div class="cardx" style="margin-top:auto"><p>{c}</p></div>')
add(f'{n}-5',POST,'soft',head("5/5")+eye("Anche per la tua farmacia")+'<h1 style="font-size:108px">Formazione del personale e <em>assistenza in 24–48 ore.</em></h1><div class="nav" style="margin-top:auto"><small>Parliamone</small><p>Scrivici in DM<br>081 8045042 · reagenta.it</p></div>')
# F6 Mer 18 GenEye GCP-30 (magenta, foto su card bianca)
add('feed-mer-18-geneye',POST,'mag',head()+eye("POCT molecolare")+'<div class="num" style="font-size:300px;margin-top:20px;color:#fff;line-height:.85">30</div><h1 style="font-size:84px;margin-top:6px">target per pannello, <em>circa 20 minuti.</em></h1><div style="margin-top:24px;display:flex;justify-content:center">'+ph('gcp30',600,360)+'</div><p style="font-size:27px;font-weight:600;margin-top:16px;line-height:1.3">GenEye GCP-30 · tecnologia ERA, touchscreen 7". Target e interpretazione dipendono dai reagenti compatibili.</p>')
# F7 Gio 10 mito/fatto (due metà)
add('feed-gio-10-mito','half','half','')
# F8 Gio 18 carosello ordinare su reagenta.it (soft)
n='feed-gio-18-ordine'
add(f'{n}-1',POST,'soft',head("1/5")+eye("Per acquisti ed enti")+'<h1 style="font-size:140px;margin-top:50px">Prima di ordinare: <em>4 cose</em> da sapere.</h1><p style="font-size:42px">Quello che trovi su reagenta.it.</p>'+scorri())
oq=[("01","Un catalogo per area","Test rapidi, strumenti, monouso e prelievi, kit chirurgici, biologia molecolare, immunofluorescenza."),("02","Un account su misura","Cliente finale, laboratorio, distributore, ospedale o ente: scegli il profilo giusto."),("03","Spedizione tracciata","Evasione media in 48 ore, spedizione tracciata 24/48h dal magazzino di Monte di Procida.")]
for i,(a,b,c) in enumerate(oq,2):
    add(f'{n}-{i}',POST,'soft',head(f"{i}/5")+f'<div class="num" style="font-size:240px;margin-top:50px">{a}</div><h1 style="font-size:112px;margin-top:6px">{b}</h1><div class="nav" style="margin-top:auto"><small>Su reagenta.it</small><p style="font-size:36px">{c}</p></div>')
add(f'{n}-5',POST,'soft',head("5/5")+eye("CE-IVD · uso professionale")+'<div class="num" style="font-size:240px;margin-top:40px">04</div><h1 style="font-size:104px;margin-top:6px">Documentazione <em>prima dell\'acquisto.</em></h1><div class="cardx" style="margin-top:auto;background:#fff"><p>Documentazione tecnica sempre disponibile. Richiedi una quotazione su reagenta.it.</p></div>')
# F9 Ven 10 webinar (navy, timeline)
tl=lambda a,b:f'<div style="display:flex;align-items:center;gap:30px;background:rgba(255,255,255,.07);border-radius:30px;padding:26px 36px"><div style="font-family:SG;font-weight:700;font-size:84px;color:#FF2E5B;line-height:1;width:110px">{a}</div><div style="font-family:SG;font-weight:700;font-size:52px;color:#fff;line-height:1.1">{b}</div></div>'
add('feed-ven-10-webinar',POST,'navy',head()+eye("Formazione · prossimamente")+'<h1 style="font-size:104px">Dal campione al referto: <em>il webinar in arrivo.</em></h1><div style="display:flex;flex-direction:column;gap:18px;margin-top:36px">'+tl("01","Il campione")+tl("02","Metodiche CLIA")+tl("03","Il referto")+'</div><p style="font-size:32px;margin-top:26px">Un percorso pratico sui flussi del laboratorio moderno, con domande dal vivo. Iscrizioni in apertura.</p>')
# F10 Ven 18 Lumicision CLI1000 (bianco, specifiche)
def spec(a,b): return f'<div style="display:flex;justify-content:space-between;align-items:baseline;border-bottom:2px solid #EEF0F8;padding:16px 0"><span style="font-family:PM;font-weight:600;font-size:22px;letter-spacing:.16em;text-transform:uppercase;color:#7079A0">{a}</span><span style="font-family:SG;font-weight:700;font-size:40px;color:#0C1633">{b}</span></div>'
add('feed-ven-18-lumicision',POST,'white',head()+eye("CLIA da banco")+'<h1 style="font-size:92px;margin-top:20px">Analizzatore CLIA <em>a reagente monotest.</em></h1><div class="row" style="margin-top:22px;align-items:center;gap:30px">'+ph('cli1000',400,330,'#F4F6FC')+'<div style="flex:1">'+spec("Test/ora","32")+spec("Monotest","24 test")+spec("Campioni","8 a bordo")+spec("Incubazione","37 °C")+'</div></div><p style="font-size:30px;margin-top:18px;line-height:1.35">Lumicision CLI1000 · touchscreen 8", stampa integrata, collegamento LIS. Pannello secondo i reagenti compatibili.</p><div class="pill" style="margin-top:auto">RICHIEDI UNA QUOTAZIONE</div>')

# ============ STORIES ============
def S(name,theme,inner): add(name,STORY,theme,inner)
def big(t,sz=140,mt=60): return f'<h1 style="font-size:{sz}px;margin-top:{mt}px">{t}</h1>'
# LUN
S('story-lun-0850','white',head()+eye("Domanda del giorno")+big('Cosa controlli <em>prima</em> di ogni prelievo?',150,70)+'<p style="font-size:48px">Alle 10:00 la checklist da salvare.</p><div class="pill m" style="margin-top:auto">DETTAGLI NEL POST</div>')
S('story-lun-1310','navy',head()+eye("Consiglio rapido")+big('Data di scadenza: <em>sempre.</em>',130,60)+'<div style="margin-top:44px;display:flex;justify-content:center">'+ph('vacumed',560,520)+'</div><p style="font-size:40px;margin-top:30px">Controllala prima di usare la provetta, poi segui le istruzioni del produttore.</p>')
S('story-lun-1730','soft',head()+eye("Alle 18:00")+big('Lo strumento si ferma. <em>Quanto aspetti?</em>',130,70)+'<p style="font-size:48px">Alle 18:00 la nostra risposta.</p><div class="pill m" style="margin-top:auto">DETTAGLI NEL POST</div>')
# MAR
S('story-mar-0850','mag',head()+eye("Domanda del giorno")+big('Quanti campioni passa il tuo laboratorio <em>in un\'ora?</em>',120,70)+'<p style="font-size:48px;font-weight:600">Alle 10:00 un analizzatore CLIA compatto.</p><div class="pill" style="margin-top:auto">DETTAGLI NEL POST</div>')
S('story-mar-1310','navy',head()+eye("Numero del giorno")+'<div class="num" style="font-size:270px;margin-top:40px;white-space:nowrap">15 min</div><h1 style="font-size:84px;margin-top:0">per l\'esito del test <em>combo respiratorio.</em></h1><div style="margin-top:36px;display:flex;justify-content:center">'+ph('combo',560,400)+'</div>')
S('story-mar-1730','white',head()+eye("Alle 18:00 · Farmacie")+big('1 tampone, <em>6 target.</em>',170,70)+'<p style="font-size:48px">Un carosello da scorrere.</p><div class="pill" style="margin-top:auto">SCORRI IL CAROSELLO</div>')
# MER
S('story-mer-0850','white',head()+eye("Oggi sul campo")+big('Un open day <em>in farmacia.</em>',150,60)+'<div style="margin-top:40px;display:flex;justify-content:center">'+ph('reagpro',560,420,'#F4F6FC')+'</div><p style="font-size:42px;margin-top:28px">Alle 10:00 il caso Salerno.</p>')
S('story-mer-1310','navy',head()+eye("Dietro le quinte")+big('Installazione. <em>Formazione.</em> Assistenza.',130,60)+'<div style="display:flex;flex-direction:column;gap:18px;margin-top:50px">'+tl("01","Installiamo")+tl("02","Formiamo")+tl("03","24–48 ore")+'</div><div class="pill m" style="margin-top:auto">SCRIVICI IN DM</div>')
S('story-mer-1730','soft',head()+eye("Alle 18:00")+'<div class="num" style="font-size:380px;margin-top:30px">30</div><h1 style="font-size:96px;margin-top:0">target in circa <em>20 minuti.</em></h1><div style="margin-top:34px;display:flex;justify-content:center">'+ph('gcp30',520,330)+'</div>')
# GIO
S('story-gio-0850','navy',head()+eye("Mito o fatto?")+big('«Il test rapido <em>basta per decidere.</em>»',130,70)+'<p style="font-size:48px">Il fatto, alle 10:00.</p><div class="pill m" style="margin-top:auto">DETTAGLI NEL POST</div>')
S('story-gio-1310','mag',head()+eye("FAQ clienti")+big('Quando arriva <em>l\'ordine?</em>',150,60)+'<div class="num" style="font-size:260px;margin-top:40px;color:#fff">24/48h</div><p style="font-size:44px;font-weight:600">Spedizione tracciata dal magazzino di Monte di Procida.</p><div class="pill" style="margin-top:auto">REAGENTA.IT</div>')
S('story-gio-1730','white',head()+eye("Alle 18:00")+big('Prima di ordinare: <em>4 cose.</em>',150,70)+'<p style="font-size:48px">Per laboratori, enti e ospedali.</p><div class="pill m" style="margin-top:auto">SALVA IL CAROSELLO</div>')
# VEN
S('story-ven-0850','soft',head()+eye("In arrivo")+big('Dal campione <em>al referto.</em>',160,70)+'<p style="font-size:48px">Alle 10:00 il webinar sulle metodiche CLIA.</p><div class="pill m" style="margin-top:auto">DETTAGLI NEL POST</div>')
S('story-ven-1310','navy',head()+eye("Numero del giorno")+'<div class="num" style="font-size:420px;margin-top:50px">60+</div><h1 style="font-size:96px;margin-top:0">produttori <em>selezionati.</em></h1><p style="font-size:42px">Un solo referente, dal preventivo all\'assistenza.</p>')
S('story-ven-1730','white',head()+eye("Alle 18:00 · CLIA da banco")+big('32 test/ora, <em>reagente monotest.</em>',120,50)+'<div style="margin-top:44px;display:flex;justify-content:center">'+ph('cli1000',560,440,'#F4F6FC')+'</div><div class="pill m" style="margin-top:auto">DETTAGLI NEL POST</div>')

def page(size,theme,inner):
    w,h,t,b=size
    th=TH[theme]
    v=';'.join(f'--{k}:{x}' for k,x in th.items())
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS} body{{width:{w}px;height:{h}px;{v}}} .wrap{{top:{t}px;bottom:{b}px}}</style></head><body><div class="wrap">{inner}</div></body></html>'
def page_half():
    th=TH['navy']; v=';'.join(f'--{k}:{x}' for k,x in th.items())
    top=f'''<div style="position:absolute;left:0;right:0;top:0;height:690px;background:#0C1633;{v}"><div class="wrap" style="top:60px;bottom:0">{head()}{eye("Mito")}<h1 style="font-size:96px;margin-top:30px">«Il risultato del test rapido <em>basta per decidere.</em>»</h1></div></div>'''
    w=TH['white']; v2=';'.join(f'--{k}:{x}' for k,x in w.items())
    bot=f'''<div style="position:absolute;left:0;right:0;top:690px;bottom:0;background:#fff;{v2}"><div class="wrap" style="top:50px;bottom:60px">{eye("Fatto")}<h1 style="font-size:62px;margin-top:20px">È un supporto. <em>L'interpretazione spetta al medico,</em> con il quadro clinico.</h1><div style="margin-top:auto;display:flex;align-items:center;gap:30px"><div class="ph" style="width:220px;height:170px;background:#F4F6FC"><img src="{P}/combo.png" style="padding:6px"></div><p style="font-size:29px;margin-top:0;line-height:1.35">Test rapidi CE-IVD per uso professionale: li trovi su reagenta.it.</p></div></div></div>'''
    sep='<div style="position:absolute;left:0;right:0;top:690px;height:8px;background:#FF2E5B"></div>'
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS} body{{width:1080px;height:1350px;background:#fff}}</style></head><body>{top}{bot}{sep}</body></html>'
only=sys.argv[1:]
with sync_playwright() as p:
    b=p.chromium.launch()
    for name,(size,theme,inner) in items.items():
        if only and not any(name.startswith(o) for o in only): continue
        if size=='half': w,h=1080,1350
        else: w,h=size[0],size[1]
        pg=b.new_page(viewport={"width":w,"height":h})
        fn=TMP/f"{name}.html"; fn.write_text(page_half() if theme=='half' else page(size,theme,inner))
        pg.goto("file://"+str(fn)); pg.wait_for_timeout(400)
        pg.screenshot(path=str(OUT/f"{name}.png")); pg.close()
    b.close()
print(len(items))
