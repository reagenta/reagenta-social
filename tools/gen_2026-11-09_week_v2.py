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


def tl(a,b):
    return f'<div style="display:flex;align-items:center;gap:30px;background:rgba(255,255,255,.07);border-radius:30px;padding:26px 36px"><div style="font-family:SG;font-weight:700;font-size:84px;color:#FF2E5B;line-height:1;width:110px">{a}</div><div style="font-family:SG;font-weight:700;font-size:52px;color:#fff;line-height:1.1">{b}</div></div>'
def dots(i,n,on='#FF2E5B',off='#C9D0EC'):
    return '<div style="display:flex;gap:10px;margin-top:28px">'+''.join(f'<span style="width:{70 if j==i else 26}px;height:14px;border-radius:8px;background:{on if j<=i else off}"></span>' for j in range(1,n+1))+'</div>'
def step(name,i,N,theme,lab,num,title,body,tsz=118,nsz=300,dk=False):
    add(f'{name}-{i}',POST,theme,head(f"{i}/{N}")+eye(lab)+f'<div class="num" style="font-size:{nsz}px;margin-top:26px">{num}</div><h1 style="font-size:{tsz}px;margin-top:0">{title}</h1><div class="cardx" style="margin-top:auto"><p style="font-size:36px">{body}</p></div>'+dots(i-1,N-1))

# ============ FEED ============
# F1 Lun10 carosello preanalitica 5 punti (navy)
n='feed-lun-10-preanalitica'
add(f'{n}-1',POST,'navy',head("1/6")+eye("Il caso del bancone")+'<h1 style="font-size:150px;margin-top:50px">Il campione può peggiorare. <em>Dove?</em></h1><p style="font-size:42px">5 punti della preanalitica da tenere d\'occhio.</p>'+scorri('m'))
pa=[("01","Identificazione","Un errore di etichetta non si corregge in laboratorio."),("02","Prelievo","Stasi prolungata e tecnica di prelievo possono alterare il campione."),("03","Conservazione","Tempi e temperature: quelli del produttore e del tuo laboratorio."),("04","Centrifugazione","Tempi e giri secondo le istruzioni della provetta."),]
for i,(a,b,c) in enumerate(pa,2):
    add(f'{n}-{i}',POST,'navy',head(f"{i}/6")+eye("Punto "+a)+f'<div class="num" style="font-size:300px;margin-top:26px">{a}</div><h1 style="font-size:122px;margin-top:0">{b}</h1><div class="cardx" style="margin-top:auto"><p style="font-size:36px">{c}</p></div>')
add(f'{n}-6',POST,'navy',head("6/6")+eye("Punto 05")+'<div class="num" style="font-size:300px;margin-top:26px">05</div><h1 style="font-size:118px;margin-top:0">Controllo visivo</h1><p style="font-size:38px">Emolisi, lipemia, ittero: guarda il campione prima di analizzarlo.</p><div class="pill m" style="margin-top:auto">QUAL È IL TUO PUNTO CRITICO?</div>')
# F2 Lun18 domanda (magenta)
add('feed-lun-18-centrifuga',POST,'mag',head()+eye("Domanda di mestiere")+'<h1 style="font-size:132px;margin-top:50px">Dopo il prelievo, quanto aspetti prima di <em>centrifugare?</em></h1><div style="display:flex;flex-wrap:wrap;gap:16px;margin-top:40px">'+pillrow(["Subito","Entro un\'ora","Dipende dall'analita","Dipende dal turno"],'#fff')+'</div><div class="pill" style="margin-top:auto">RISPONDI NEI COMMENTI</div>')
# F3 Mar10 mito/fatto FOB vs calprotectina (half)
add('feed-mar-10-fob-calpro','half','half','')
# F4 Mar18 carosello AVE-562 in 7 passi (bianco)
n='feed-mar-18-ave562'
add(f'{n}-1',POST,'white',head("1/5")+eye("Parassitologia e feci")+'<h1 style="font-size:136px">L\'esame delle feci in <em>7 passi.</em></h1><div style="display:flex;justify-content:center;margin-top:30px">'+ph('ave562',520,400,'#F4F6FC')+'</div>'+scorri())
av=[("01–03","Prepara","Fino a 40 campioni a bordo, barcode, diluizione, omogeneizzazione e filtrazione automatiche."),("04–05","Osserva","Microscopia digitale ed elaborazione iA: riconoscimento e conteggio di eritrociti, leucociti, strutture parassitarie, lieviti. L'operatore rivede le immagini."),("06","Misura","Test immunochimici compatibili: sangue occulto, calprotectina, transferrina, antigeni gastrointestinali, secondo configurazione.")]
for i,(a,b,c) in enumerate(av,2):
    add(f'{n}-{i}',POST,'white',head(f"{i}/5")+eye("Passi "+a)+f'<div class="num" style="font-size:230px;margin-top:30px;white-space:nowrap">{a}</div><h1 style="font-size:128px;margin-top:0">{b}</h1><div class="cardx" style="margin-top:auto;background:#F4F6FC"><p style="font-size:34px">{c}</p></div>')
add(f'{n}-5',POST,'white',head("5/5")+eye("Passo 07")+'<div class="num" style="font-size:230px;margin-top:30px">07</div><h1 style="font-size:110px;margin-top:0">Validazione e <em>refertazione.</em></h1><p style="font-size:36px">Risultati integrati, immagini archiviate, trasmissione al LIS. AVE-562: 90 campioni/ora.</p><div class="nav" style="margin-top:auto"><small>Vuoi vederlo dal vivo?</small><p>Scrivici in DM<br>081 8045042 · reagenta.it</p></div>')
# F5 Mer10 carosello IVDR (soft)
n='feed-mer-10-ivdr'
add(f'{n}-1',POST,'soft',head("1/5")+eye("Qualità e norme")+'<h1 style="font-size:132px;margin-top:40px">IVDR: cosa cambia per chi <em>compra</em> diagnostici?</h1><p style="font-size:40px">Le scadenze, in parole semplici.</p>'+scorri())
iv=[("Regolamento (UE) 2017/746","Più dispositivi passano da un <b>organismo notificato</b>. Sostituisce la vecchia direttiva IVD.",96),("31/12/2027 · 2028 · 2029","Dispositivi «legacy» sul mercato fino al <b>31/12/2027</b> (classe D), <b>31/12/2028</b> (C), <b>31/12/2029</b> (B e A sterile).",84),("A condizioni precise","Sistema qualità IVDR, domanda a un organismo notificato e accordo scritto, entro le date previste per ogni classe.",96)]
for i,(a,b,s) in enumerate(iv,2):
    add(f'{n}-{i}',POST,'soft',head(f"{i}/5")+eye("IVDR")+f'<h1 style="font-size:{s}px;margin-top:40px">{a}</h1><div class="nav" style="margin-top:auto"><small>In sintesi</small><p style="font-size:36px">{b}</p></div>')
add(f'{n}-5',POST,'soft',head("5/5")+eye("Cosa fare")+'<h1 style="font-size:104px;margin-top:40px">Chiedi al fornitore <em>marcatura e documenti.</em></h1><p style="font-size:30px">Sintesi da Reg. (UE) 2024/1860, in vigore dal 9/7/2024. Sono indicazioni generali: vale il testo ufficiale.</p><div class="cardx" style="margin-top:auto;background:#fff"><p>Documentazione tecnica: richiedila a reagenta.it o allo 081 8045042.</p></div>')
# F6 Mer18 ELISA colore / CLIA luce (split verticale navy | magenta)
add('feed-mer-18-colore-luce','split','split','')
# F7 Gio10 carosello HIL (navy)
n='feed-gio-10-siero'
add(f'{n}-1',POST,'navy',head("1/5")+eye("Il caso del bancone")+'<h1 style="font-size:132px;margin-top:40px">Il campione ti parla: <em>emolisi, lipemia, ittero.</em></h1><p style="font-size:40px">Cosa significano, in 3 colori.</p>'+scorri('m'))
hl=[("Rosso","Emolisi","Rottura dei globuli rossi: rilascia componenti intracellulari (es. potassio, LDH, AST) e può alterare i valori."),("Lattescente","Lipemia","Siero torbido: può interferire con i metodi ottici e fotometrici."),("Giallo intenso","Ittero","Bilirubina elevata: il colore giallo-arancio può interferire con alcuni metodi.")]
for i,(c,b,t) in enumerate(hl,2):
    add(f'{n}-{i}',POST,'navy',head(f"{i}/5")+eye(c)+f'<h1 style="font-size:150px;margin-top:40px">{b}</h1><div class="cardx" style="margin-top:auto"><small>Cosa succede</small><p style="font-size:36px">{t}</p></div>'+dots(i-1,4))
add(f'{n}-5',POST,'navy',head("5/5")+eye("Cosa fare")+'<h1 style="font-size:110px;margin-top:40px">Guarda il campione, <em>poi analizza.</em></h1><div class="nav" style="margin-top:36px"><p>Segui la procedura del tuo laboratorio: indici HIL, commento al referto, nuovo prelievo se serve.</p></div><div class="pill m" style="margin-top:auto">SALVA E CONDIVIDI</div>')
# F8 Gio18 carosello test rapido o laboratorio (soft)
n='feed-gio-18-rapido-lab'
add(f'{n}-1',POST,'soft',head("1/5")+eye("Appropriatezza")+'<h1 style="font-size:132px;margin-top:40px">Test rapido o laboratorio? <em>Non è una gara.</em></h1>'+scorri())
rl=[("Rapido","Il test rapido risponde in pochi minuti: utile al punto di cura, vicino al paziente."),("Laboratorio","Il laboratorio dà risultati quantitativi, controlli di qualità e tracciabilità su volumi maggiori."),("Attenzione","Un risultato negativo non sempre basta: può servire una conferma, secondo il quadro clinico.")]
for i,(a,b) in enumerate(rl,2):
    add(f'{n}-{i}',POST,'soft',head(f"{i}/5")+eye("Da sapere")+f'<h1 style="font-size:136px;margin-top:40px">{a}</h1><div class="nav" style="margin-top:auto"><small>In sintesi</small><p style="font-size:38px">{b}</p></div>'+dots(i-1,4))
add(f'{n}-5',POST,'soft',head("5/5")+eye("In breve")+'<h1 style="font-size:112px;margin-top:40px">Strumenti <em>complementari.</em></h1><p style="font-size:38px">Test rapidi e analisi di laboratorio rispondono a bisogni diversi. L\'interpretazione spetta al medico.</p><div class="cardx" style="margin-top:auto;background:#fff"><p>Quale usi di più, e per cosa? Raccontacelo nei commenti.</p></div>')
# F9 Ven10 checklist manutenzione (bianco)
def ck(i,t): return f'<div style="display:flex;align-items:center;gap:26px;border-bottom:2px solid #EEF0F8;padding:22px 0"><div style="font-family:SG;font-weight:700;font-size:64px;color:#FF2E5B;width:90px">{i}</div><div style="font-family:SG;font-weight:700;font-size:44px;color:#0C1633;line-height:1.1">{t}</div></div>'
add('feed-ven-10-manutenzione',POST,'white',head()+eye("Checklist del tecnico")+'<h1 style="font-size:104px;margin-top:24px">Manutenzione preventiva: <em>5 controlli.</em></h1><div style="margin-top:20px">'+ck("01","Pulizia e decontaminazione")+ck("02","Controllo di qualità interno")+ck("03","Verifiche secondo il produttore")+ck("04","Registro degli interventi")+ck("05","Scorte e scadenze dei consumabili")+'</div><p style="font-size:28px;margin-top:20px">Indicazioni generali: valgono le istruzioni del produttore.</p>')
# F10 Ven18 domanda (magenta)
add('feed-ven-18-automatizzare',POST,'mag',head()+eye("Domanda del venerdì")+'<h1 style="font-size:100px;margin-top:50px">Qual è la prima cosa che <em>automatizzeresti?</em></h1><div style="display:flex;flex-wrap:wrap;gap:16px;margin-top:40px">'+pillrow(["Preanalitica","Parassitologia","Refertazione","Magazzino"],'#fff')+'</div><div class="pill" style="margin-top:auto">SCRIVICI IN DM</div>')

# ============ STORIES ============
def S(name,theme,inner): add(name,STORY,theme,inner)
def big(t,sz=140,mt=60): return f'<h1 style="font-size:{sz}px;margin-top:{mt}px">{t}</h1>'
S('story-lun-0850','white',head()+eye("Domanda del giorno")+big('Il campione può peggiorare. <em>Dove?</em>',140,70)+'<p style="font-size:48px">Alle 10:00 i 5 punti da tenere d\'occhio.</p><div class="pill m" style="margin-top:auto">DETTAGLI NEL POST</div>')
S('story-lun-1310','navy',head()+eye("Lo sapevi?")+big('L\'emolisi rilascia <em>potassio, LDH e AST</em> dalle cellule.',112,60)+'<p style="font-size:44px">Per questo un campione emolizzato può alterare i valori.</p><div class="pill m" style="margin-top:auto">SALVA PER DOPO</div>')
S('story-lun-1730','soft',head()+eye("Alle 18:00")+big('Quanto aspetti prima di <em>centrifugare?</em>',130,70)+'<p style="font-size:48px">Una domanda per i tecnici. Rispondi nel post.</p><div class="pill m" style="margin-top:auto">DETTAGLI NEL POST</div>')
S('story-mar-0850','mag',head()+eye("Mito o fatto?")+big('FOB e calprotectina misurano <em>la stessa cosa?</em>',120,70)+'<p style="font-size:48px;font-weight:600">Il fatto, alle 10:00.</p><div class="pill" style="margin-top:auto">DETTAGLI NEL POST</div>')
S('story-mar-1310','navy',head()+eye("Numero del giorno")+'<div class="num" style="font-size:420px;margin-top:40px">7</div><h1 style="font-size:96px;margin-top:0">passi per l\'esame <em>delle feci.</em></h1><div style="margin-top:34px;display:flex;justify-content:center">'+ph('ave562',480,340,'#fff')+'</div>')
S('story-mar-1730','soft',head()+eye("Alle 18:00")+big('Parassitologia con <em>elaborazione iA.</em>',130,70)+'<p style="font-size:48px">Un carosello da scorrere.</p><div class="pill m" style="margin-top:auto">SCORRI IL CAROSELLO</div>')
S('story-mer-0850','white',head()+eye("Qualità e norme")+big('IVDR: lo sai cosa cambia per chi <em>compra?</em>',120,70)+'<p style="font-size:48px">Alle 10:00 le scadenze in parole semplici.</p><div class="pill m" style="margin-top:auto">DETTAGLI NEL POST</div>')
S('story-mer-1310','navy',head()+eye("Numero del giorno")+'<div class="num" style="font-size:230px;margin-top:60px;white-space:nowrap">31/12/27</div><h1 style="font-size:92px;margin-top:10px">Classe D: scadenza della transizione <em>IVDR.</em></h1><p style="font-size:38px">Per i dispositivi legacy, a condizioni precise.</p>')
S('story-mer-1730','mag',head()+eye("Alle 18:00")+big('ELISA: il segnale è colore. CLIA: <em>luce.</em>',112,70)+'<p style="font-size:48px;font-weight:600">Stesso principio, lettura diversa.</p><div class="pill" style="margin-top:auto">DETTAGLI NEL POST</div>')
S('story-gio-0850','soft',head()+eye("Domanda del giorno")+big('Che colore ha <em>il tuo siero?</em>',150,70)+'<p style="font-size:48px">Rosso, lattescente, giallo intenso: alle 10:00 cosa significano.</p><div class="pill m" style="margin-top:auto">DETTAGLI NEL POST</div>')
S('story-gio-1310','white',head()+eye("Consiglio rapido")+big('Test rapido o laboratorio? <em>Non è una gara.</em>',120,70)+'<p style="font-size:46px">Sono strumenti complementari: scegli in base al bisogno.</p><div class="pill m" style="margin-top:auto">SALVA PER DOPO</div>')
S('story-gio-1730','navy',head()+eye("Alle 18:00")+big('Un negativo <em>basta sempre?</em>',150,70)+'<p style="font-size:48px">Il carosello su rapido e laboratorio.</p><div class="pill m" style="margin-top:auto">SCORRI IL CAROSELLO</div>')
S('story-ven-0850','white',head()+eye("Checklist")+big('Manutenzione preventiva: <em>5 controlli.</em>',130,70)+'<p style="font-size:48px">Alle 10:00 la checklist del tecnico.</p><div class="pill m" style="margin-top:auto">DETTAGLI NEL POST</div>')
S('story-ven-1310','mag',head()+eye("Servizio")+'<div class="num" style="font-size:230px;margin-top:50px;color:#fff;white-space:nowrap">24–48h</div><h1 style="font-size:92px;margin-top:10px">Assistenza tecnica: <em>intervento in 24–48 ore.</em></h1><p style="font-size:40px;font-weight:600">Hotline lun–ven 8:30–18:00 · 081 8045042</p>')
S('story-ven-1730','soft',head()+eye("Buon weekend")+big('Qual è la prima cosa che <em>automatizzeresti?</em>',98,70)+'<p style="font-size:48px">Rispondi nel post delle 18:00.</p><div class="pill m" style="margin-top:auto">DETTAGLI NEL POST</div>')

def page(size,theme,inner):
    w,h,t,b=size
    th=TH[theme]
    v=';'.join(f'--{k}:{x}' for k,x in th.items())
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS} body{{width:{w}px;height:{h}px;{v}}} .wrap{{top:{t}px;bottom:{b}px}}</style></head><body><div class="wrap">{inner}</div></body></html>'
def page_half():
    th=TH['navy']; v=';'.join(f'--{k}:{x}' for k,x in th.items())
    top=f'''<div style="position:absolute;left:0;right:0;top:0;height:690px;background:#0C1633;{v}"><div class="wrap" style="top:60px;bottom:0">{head()}{eye("Mito")}<h1 style="font-size:92px;margin-top:30px">«FOB e calprotectina misurano <em>la stessa cosa.</em>»</h1></div></div>'''
    w=TH['white']; v2=';'.join(f'--{k}:{x}' for k,x in w.items())
    bot=f'''<div style="position:absolute;left:0;right:0;top:690px;bottom:0;background:#fff;{v2}"><div class="wrap" style="top:50px;bottom:60px">{eye("Fatto")}<h1 style="font-size:58px;margin-top:20px;line-height:1.1">Il FOB cerca <em>sangue occulto</em> nelle feci. La calprotectina è una proteina legata all'<em>infiammazione intestinale.</em></h1><p style="font-size:34px;margin-top:22px">Due domande diverse, due test diversi. L'interpretazione spetta al medico.</p></div></div>'''
    sep='<div style="position:absolute;left:0;right:0;top:690px;height:8px;background:#FF2E5B"></div>'
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS} body{{width:1080px;height:1350px;background:#fff}}</style></head><body>{top}{bot}{sep}</body></html>'
def page_split():
    n=TH['navy']; vn=';'.join(f'--{k}:{x}' for k,x in n.items())
    m=TH['mag']; vm=';'.join(f'--{k}:{x}' for k,x in m.items())
    left=f'<div style="position:absolute;left:0;top:0;bottom:0;width:540px;background:#0C1633;{vn}"><div style="position:absolute;left:60px;right:40px;top:72px;bottom:72px;display:flex;flex-direction:column"><div class="head" style="gap:14px"><div class="wm" style="font-size:44px">Reagenta</div></div>{eye("ELISA")}<div class="num" style="font-size:140px;margin-top:70px;color:#fff;letter-spacing:-.04em">Colore</div><p style="font-size:34px;color:#C9D0EC">La reazione enzimatica cambia colore: si misura l\'assorbanza.</p></div></div>'
    right=f'<div style="position:absolute;right:0;top:0;bottom:0;width:540px;background:#FF2E5B;{vm}"><div style="position:absolute;left:60px;right:60px;top:72px;bottom:72px;display:flex;flex-direction:column"><div class="head" style="border:0;height:76px"></div>{eye("CLIA")}<div class="num" style="font-size:170px;margin-top:70px;color:#fff;letter-spacing:-.04em">Luce</div><p style="font-size:34px;color:#0C1633;font-weight:600">La reazione chemiluminescente emette luce: si misura il segnale luminoso.</p></div></div>'
    foot='<div style="position:absolute;left:0;right:0;bottom:72px;text-align:center;font-family:PM;font-weight:600;font-size:22px;letter-spacing:.25em;color:#fff;z-index:5"><span style="background:#0C1633;padding:22px 34px;border-radius:100px">STESSO PRINCIPIO IMMUNOLOGICO</span></div>'
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS} body{{width:1080px;height:1350px}}</style></head><body>{left}{right}{foot}</body></html>'
only=sys.argv[1:]
with sync_playwright() as p:
    b=p.chromium.launch()
    for name,(size,theme,inner) in items.items():
        if only and not any(name.startswith(o) for o in only): continue
        w,h=(1080,1350) if size in('half','split') else (size[0],size[1])
        pg=b.new_page(viewport={"width":w,"height":h})
        fn=TMP/f"{name}.html"; fn.write_text(page_half() if theme=='half' else page_split() if theme=='split' else page(size,theme,inner))
        pg.goto("file://"+str(fn)); pg.wait_for_timeout(400)
        pg.screenshot(path=str(OUT/f"{name}.png")); pg.close()
    b.close()
print(len(items))
