import pathlib, html, sys
from playwright.sync_api import sync_playwright
F="file:///home/claude/social-build/node_modules/@fontsource"
P="file:///home/claude/social-build/prod"
OUT=pathlib.Path("/home/claude/reagenta-social/img/2026-11-02"); OUT.mkdir(parents=True,exist_ok=True)
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

# ===== F1 Lun 10:00 carosello tappi (navy)
n='feed-lun-10-tappi'
add(f'{n}-1',POST,'navy',head("1/5")+eye("Per il laboratorio")+'<h1 style="font-size:132px">Tappo viola o azzurro? <em>Non confonderli.</em></h1><div class="row" style="margin-top:44px">'+img('vacumed',440,440)+img('citrato',440,440)+'</div>'+scorri('m'))
add(f'{n}-2',POST,'navy',head("2/5")+eye("Tappo viola")+'<h1 style="font-size:150px">Ematologia.</h1><p style="font-size:42px">K3 EDTA: la provetta per gli esami ematologici, come l\'emocromo.</p><div style="margin-top:auto">'+img('vacumed',None,430).replace('style="width:Nonepx;','style="width:100%;')+'</div>')
add(f'{n}-3',POST,'navy',head("3/5")+eye("Tappo azzurro")+'<h1 style="font-size:132px">Coagulazione.</h1><p style="font-size:42px">Sodio citrato 3,2%: per PT, aPTT, fibrinogeno, INR e D-dimero.</p><div style="margin-top:auto">'+img('citrato',None,430).replace('style="width:Nonepx;','style="width:100%;')+'</div>')
add(f'{n}-4',POST,'navy',head("4/5")+eye("Il dettaglio che conta")+'<h1 style="font-size:150px">Proporzione.</h1><p style="font-size:42px">Le provette sottovuoto sono progettate per la corretta proporzione sangue/additivo. Rispetta sempre il volume di riempimento.</p><div class="cardx" style="margin-top:auto"><small>Prima del prelievo</small><p>Tappo · additivo · livello di riempimento</p></div>')
add(f'{n}-5',POST,'navy',head("5/5")+eye("Da salvare")+'<h1 style="font-size:104px">3 controlli, <em>5 secondi.</em></h1><div class="nav" style="margin-top:40px"><p>1. Colore del tappo<br>2. Additivo giusto per l\'esame<br>3. Volume di riempimento</p></div><p style="font-size:30px">Indicazioni generali: valgono sempre le istruzioni d\'uso del produttore.</p><div class="pill m" style="margin-top:auto">SALVA E CONDIVIDI</div>')
# ===== F2 Lun 18:00 domanda (magenta)
add('feed-lun-18-domanda',POST,'mag',head()+eye("Domanda di mestiere")+'<h1 style="font-size:138px;margin-top:60px">Dove perde più tempo il tuo <em>laboratorio?</em></h1><p style="font-size:44px;font-weight:600">Preanalitica, analisi o refertazione?</p><div class="pill" style="margin-top:auto">RISPONDI NEI COMMENTI</div>')
# ===== F3 Mar 10:00 5 min (bianco)
add('feed-mar-10-5min',POST,'white',head()+eye("Per la farmacia")+'<div class="num" style="font-size:360px;margin-top:40px">5 min</div><h1 style="font-size:100px;margin-top:10px">Il tempo <em>di un caffè.</em></h1><div class="cardx" style="margin-top:auto;display:flex;align-items:center;gap:36px;padding:28px 40px">'+img('strep',270,270,'#fff')+'<div><small>Test rapido Strep A CiTest</small><p style="font-size:32px;font-weight:400">Tempo di lettura su tampone faringeo. Dispositivo CE-IVD per uso professionale.</p></div></div>')
# ===== F4 Mar 18:00 carosello Reagenta Pro 3 passi (soft)
n='feed-mar-18-3passi'
add(f'{n}-1',POST,'soft',head("1/5")+eye("Come funziona")+'<h1 style="font-size:128px">Dal campione al risultato: <em>3 passi.</em></h1><div style="margin-top:36px;display:flex;justify-content:center">'+img('reagpro',500,430,'#fff')+'</div>'+scorri())
steps=[("01","Prepara","Campione e cassetta dedicata, secondo le istruzioni del test."),("02","Incuba","Fino a 12 canali indipendenti, con incubazione a 37 °C a bordo."),("03","Leggi","Lettura a fluorescenza in meno di 20 secondi. Risultato su touchscreen e stampa.")]
for i,(a,b,c) in enumerate(steps,2):
    dots=''.join(f'<span style="width:{70 if j==i-1 else 26}px;height:14px;border-radius:8px;background:{"#FF2E5B" if j<=i-1 else "#C9D0EC"}"></span>' for j in range(1,4))
    add(f'{n}-{i}',POST,'soft',head(f"{i}/5")+eye("Passo "+a)+f'<div class="num" style="font-size:300px;margin-top:30px">{a}</div><h1 style="font-size:130px;margin-top:0">{b}</h1><div class="cardx" style="margin-top:auto"><p>{c}</p></div><div style="display:flex;gap:10px;margin-top:30px">{dots}</div>')
add(f'{n}-5',POST,'soft',head("5/5")+eye("Reagenta Pro")+'<h1 style="font-size:118px"><em>12 canali,</em> 144 test/h.</h1><p>Touchscreen, stampante integrata e collegamento LIS. Analiti e modalità dipendono dal test compatibile.</p><div class="nav" style="margin-top:auto"><small>Prenota una demo</small><p>Scrivici in DM<br>081 8045042 · reagenta.it</p></div>')
# ===== F5 Mer 10:00 carosello Campanialab (bianco)
n='feed-mer-10-campanialab'
add(f'{n}-1',POST,'white',head("1/5")+eye("Sul campo · Camposano")+'<h1 style="font-size:104px">Il giorno dell\'installazione: <em>cosa succede?</em></h1><div class="row" style="margin-top:40px">'+img('reagpro',440,380,'#F4F6FC')+img('ave562',440,380,'#F4F6FC')+'</div>'+scorri())
st=[("01","Installazione","Gli strumenti vengono installati dal nostro team presso il centro Campanialab di Camposano."),("02","Validazione","Dopo l'installazione si valida il sistema, prima di usarlo nella routine."),("03","Formazione","Corso e conferenza: AVE-562 per automazione e parassitologia, Reagenta Pro per FOB, calprotectina e H. pylori.")]
for i,(a,b,c) in enumerate(st,2):
    add(f'{n}-{i}',POST,'white',head(f"{i}/5")+eye("Passo "+a)+f'<div class="num" style="font-size":"300px">'.replace('style="font-size":"300px"','style="font-size:300px;margin-top:30px"')+f'{a}</div><h1 style="font-size:124px;margin-top:0">{b}</h1><div class="cardx" style="margin-top:auto"><p>{c}</p></div>')
add(f'{n}-5',POST,'white',head("5/5")+eye("Il tuo laboratorio")+'<h1 style="font-size:112px">Vuoi lo stesso <em>percorso?</em></h1><p>Installazione, validazione e formazione del personale: parliamone sul tuo flusso di lavoro.</p><div class="nav" style="margin-top:auto"><small>Contatti</small><p>Scrivici in DM<br>081 8045042<br>reagenta.it</p></div>')
# ===== F6 Mer 18:00 San Michele (navy)
add('feed-mer-18-sanmichele',POST,'navy',head()+eye("Caserta · 2026")+'<h1 style="font-size:116px">Installare non basta: <em>si forma il personale.</em></h1><p style="font-size:40px">Casa di Cura San Michele: installazione e formazione con il sistema GastroPanel GP Reader.</p><div class="row" style="margin-top:auto;align-items:center;gap:36px">'+img('gastropanel',430,290,'#fff')+'<div class="pill m" style="align-self:center;padding:28px 34px">SCRIVICI<br>IN DM</div></div>')
# ===== F7 Gio 10:00 mito/fatto due meta
add('feed-gio-10-mito-fob',POST,'half','')
# ===== F8 Gio 18:00 FAQ test rapidi (soft)
n='feed-gio-18-faq-test-rapidi'
add(f'{n}-1',POST,'soft',head("1/5")+eye("Test rapidi · FAQ")+'<h1 style="font-size:130px">4 domande sui test rapidi, <em>con risposta.</em></h1><div class="row" style="margin-top:40px">'+img('hpylori',440,380)+img('calpro',440,380)+'</div>'+scorri())
qa=[("Quanto serve per leggerli?","Per Strep A, H. pylori e calprotectina CiTest: 5 minuti di lettura."),("Serve uno strumento?","H. pylori e calprotectina CiTest: lettura visiva, senza strumentazione aggiuntiva. Per i quantitativi c'è Reagenta Pro."),("Che campione serve?","Dipende dal test: tampone faringeo per Strep A, feci per H. pylori, FOB e calprotectina."),("Chi interpreta il risultato?","Sono dispositivi CE-IVD per uso professionale: l'interpretazione spetta al medico.")]
for i,(q,a) in enumerate(qa,2):
    add(f'{n}-{i}',POST,'soft',head(f"{i}/5")+eye(f"Domanda {i-1}")+f'<h1 style="font-size:118px;margin-top:36px">{q}</h1><div class="nav" style="margin-top:auto"><small>Risposta</small><p>{a}</p></div>')
# slide 5 as separate (4 Q + cover = 5 slides: so 2..5 are Qs)
# ===== F9 Ven 10:00 KUNIV (magenta)
add('feed-ven-10-kuniv',POST,'mag',head()+eye("Per ospedali e cliniche")+'<h1 style="font-size:106px">Quanti pezzi prepari prima di <em>ogni intervento?</em></h1><div style="margin-top:34px">'+img('kuniv',920,430)+'</div><p style="font-size:34px;font-weight:600;margin-top:24px">KUNIV PLUS di MABE Medical: teli con bordo adesivo, salviette e sacco Mayo in un set sterile monouso.</p>')
# ===== F10 Ven 18:00 carosello 3 cose (navy)
n='feed-ven-18-fornitore'
add(f'{n}-1',POST,'navy',head("1/5")+eye("Prima di scegliere")+'<h1 style="font-size:138px;margin-top:50px">Chiedi al fornitore <em>queste 3 cose.</em></h1><p style="font-size:42px">Valgono per laboratori, farmacie ed enti.</p>'+scorri('m'))
fq=[("01","Chi installa e forma il personale?","Installazione e formazione fanno parte del servizio."),("02","In quanto tempo interviene l'assistenza?","Da noi: assistenza tecnica in 24–48 ore."),("03","Ho un referente unico?","Un referente per ordini e documentazione.")]
for i,(a,q,r) in enumerate(fq,2):
    add(f'{n}-{i}',POST,'navy',head(f"{i}/5")+f'<div class="num" style="font-size:260px;margin-top:50px">{a}</div><h1 style="font-size:112px;margin-top:6px">{q}</h1><div class="cardx" style="margin-top:auto"><small>La nostra risposta</small><p>{r}</p></div>')
def tile(svg,t): return f'<div class="cardx" style="flex:1;text-align:center;padding:36px 14px"><div style="height:110px;display:flex;justify-content:center">{svg}</div><div style="font-family:SG;font-weight:700;font-size:34px;margin-top:18px;line-height:1.1;color:#0C1633">{t}</div></div>'
wr='<svg width="110" height="110" viewBox="0 0 24 24" fill="none" stroke="#FF2E5B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.4 2.4-2.6-.6-.6-2.6z"/></svg>'
bk='<svg width="110" height="110" viewBox="0 0 24 24" fill="none" stroke="#FF2E5B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 5h7a2 2 0 0 1 2 2v13a2 2 0 0 0-2-2H3zM21 5h-7a2 2 0 0 0-2 2v13a2 2 0 0 1 2-2h7z"/></svg>'
ck='<svg width="110" height="110" viewBox="0 0 24 24" fill="none" stroke="#FF2E5B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>'
add(f'{n}-5',POST,'navy',head("5/5")+eye("Tutto in un servizio")+'<h1 style="font-size:104px">Installazione, formazione, <em>assistenza.</em></h1><div class="row" style="margin-top:44px">'+tile(wr,"Installazione")+tile(bk,"Formazione")+tile(ck,"Assistenza<br>24–48 h")+'</div><div class="pill m" style="margin-top:auto">CHIAMA LO 081 8045042</div>')

# ================= STORIES
def S(name,theme,inner): add(name,STORY,theme,inner)
def big(t,sz=140,mt=60): return f'<h1 style="font-size:{sz}px;margin-top:{mt}px">{t}</h1>'
S('story-lun-0850','navy',head()+eye("Domanda del giorno")+big('Cosa controlli <em>prima</em> di prelevare?',150,70)+'<p style="font-size:48px">Alle 10:00 la guida ai tappi: viola o azzurro?</p><div class="pill m" style="margin-top:auto">DETTAGLI NEL POST</div>')
S('story-lun-1310','white',head()+eye("In una riga")+big('Viola: <em>ematologia.</em><br>Azzurro: <em>coagulazione.</em>',120,70)+'<div class="row" style="margin-top:60px">'+img('vacumed',440,440,'#F4F6FC')+img('citrato',440,440,'#F4F6FC')+'</div><div class="pill" style="margin-top:auto">SALVA IL POST</div>')
S('story-lun-1730','mag',head()+eye("Alle 18:00")+big('Una domanda <em>per voi.</em>',160,70)+'<p style="font-size:50px;font-weight:600">Dove perde più tempo il tuo laboratorio?</p><div class="pill" style="margin-top:auto">RISPONDI NEL POST</div>')
S('story-mar-0850','soft',head()+eye("Indovinello")+big('Il tempo <em>di un caffè.</em>',170,70)+'<p style="font-size:50px">Alle 10:00 scopri a cosa ci riferiamo.</p><div class="pill m" style="margin-top:auto">DETTAGLI NEL POST</div>')
S('story-mar-1310','navy',head()+eye("Numero del giorno")+'<div class="num" style="font-size:420px;margin-top:50px">12</div><h1 style="font-size:96px;margin-top:0">canali <em>indipendenti.</em></h1><p style="font-size:42px">Reagenta Pro: 144 test/h, lettura in meno di 20 secondi.</p><div style="margin-top:auto">'+img('reagpro',420,300,'#fff')+'</div>')
S('story-mar-1730','white',head()+eye("Alle 18:00")+big('Dal campione al risultato: <em>3 passi.</em>',140,70)+'<p style="font-size:48px">Un carosello da scorrere.</p><div class="pill" style="margin-top:auto">SCORRI IL CAROSELLO</div>')
S('story-mer-0850','mag',head()+eye("Oggi sul campo")+big('Cosa succede <em>il giorno dell\'installazione?</em>',104,70)+'<p style="font-size:46px;font-weight:600">Alle 10:00 il caso Campanialab, Camposano.</p><div class="pill" style="margin-top:auto">DETTAGLI NEL POST</div>')
S('story-mer-1310','white',head()+eye("Dietro le quinte")+big('Installazione. <em>Validazione.</em> Formazione.',130,70)+'<div class="cardx" style="margin-top:60px;background:#F4F6FC"><p>Tre passi, un solo referente.</p></div><div class="pill" style="margin-top:auto">SCRIVICI IN DM</div>')
S('story-mer-1730','navy',head()+eye("Alle 18:00 · Caserta")+big('Installare non basta: <em>si forma il personale.</em>',120,60)+'<div style="margin-top:50px">'+img('gastropanel',600,400,'#fff')+'</div><div class="pill m" style="margin-top:auto">DETTAGLI NEL POST</div>')
S('story-gio-0850','soft',head()+eye("Mito o fatto?")+big('«Un test positivo basta <em>per la diagnosi.</em>»',120,70)+'<p style="font-size:48px">Il fatto, alle 10:00.</p><div class="pill m" style="margin-top:auto">DETTAGLI NEL POST</div>')
S('story-gio-1310','navy',head()+eye("FAQ clienti")+big('Quando arriva <em>l\'ordine?</em>',150,60)+'<div class="num" style="font-size:250px;margin-top:40px">24/48h</div><p style="font-size:44px">Spedizione tracciata sugli ordini dal catalogo online.</p><div class="pill m" style="margin-top:auto">REAGENTA.IT</div>')
S('story-gio-1730','mag',head()+eye("Alle 18:00")+big('4 domande sui <em>test rapidi.</em>',150,70)+'<p style="font-size:48px;font-weight:600">Tempi, campione, lettura, interpretazione.</p><div class="pill" style="margin-top:auto">SALVA IL CAROSELLO</div>')
S('story-ven-0850','white',head()+eye("Domanda del giorno")+big('Quanti pezzi prepari prima <em>di un intervento?</em>',120,70)+'<p style="font-size:48px">Alle 10:00 una soluzione per ospedali e cliniche.</p><div class="pill m" style="margin-top:auto">DETTAGLI NEL POST</div>')
S('story-ven-1310','navy',head()+eye("Chi siamo")+'<div class="num" style="font-size:380px;margin-top:50px">1998</div><h1 style="font-size:90px;margin-top:0">Professionisti nella <em>diagnostica dal 1998.</em></h1><p style="font-size:40px">CE-IVD · Uso professionale</p>')
S('story-ven-1730','soft',head()+eye("Buon weekend")+big('Lunedì si riparte <em>dal tuo flusso.</em>',130,70)+'<p style="font-size:46px">Raccontaci cosa rallenta il tuo laboratorio.</p><div class="pill" style="margin-top:auto">CHIAMA 081 8045042</div>')

def page(size,theme,inner):
    w,h,t,b=size
    th=TH[theme]
    v=';'.join(f'--{k}:{x}' for k,x in th.items())
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS} body{{width:{w}px;height:{h}px;{v}}} .wrap{{top:{t}px;bottom:{b}px}}</style></head><body><div class="wrap">{inner}</div></body></html>'
def page_half():
    th=TH['navy']; v=';'.join(f'--{k}:{x}' for k,x in th.items())
    top=f'''<div style="position:absolute;left:0;right:0;top:0;height:690px;background:#0C1633;{v}"><div class="wrap" style="top:60px;bottom:0">{head()}{eye("Mito")}<h1 style="font-size:92px;margin-top:30px">Un FOB positivo ti dice <em>qual è la causa.</em></h1></div></div>'''
    w=TH['white']; v2=';'.join(f'--{k}:{x}' for k,x in w.items())
    bot=f'''<div style="position:absolute;left:0;right:0;top:690px;bottom:0;background:#fff;{v2}"><div class="wrap" style="top:50px;bottom:60px">{eye("Fatto")}<h1 style="font-size:74px;margin-top:24px">Rileva tracce di sangue occulto nelle feci. <em>Da solo non indica la causa.</em></h1><div style="margin-top:auto;display:flex;align-items:center;gap:30px"><div class="ph" style="width:270px;height:210px;background:#F4F6FC"><img src="{P}/fob.png" style="padding:10px"></div><p style="font-size:29px;margin-top:0;line-height:1.35">Test CE-IVD per uso professionale: l'interpretazione spetta al medico.</p></div></div></div>'''
    sep='<div style="position:absolute;left:0;right:0;top:690px;height:8px;background:#FF2E5B"></div>'
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS} body{{width:1080px;height:1350px;background:#fff}}</style></head><body>{top}{bot}{sep}</body></html>'
only=sys.argv[1:] 
with sync_playwright() as p:
    b=p.chromium.launch()
    for name,(size,theme,inner) in items.items():
        if only and not any(name.startswith(o) for o in only): continue
        w,h=size[0],size[1]
        pg=b.new_page(viewport={"width":w,"height":h})
        fn=TMP/f"{name}.html"; fn.write_text(page_half() if theme=='half' else page(size,theme,inner))
        pg.goto("file://"+str(fn)); pg.wait_for_timeout(500)
        pg.screenshot(path=str(OUT/f"{name}.png")); pg.close()
    b.close()
print(len(items))
