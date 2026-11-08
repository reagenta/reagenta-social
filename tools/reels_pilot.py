import sys, pathlib
from reels_engine import *
OUT = sys.argv[2] if len(sys.argv) > 2 else "/home/claude/reagenta-social/reels-pilota"
DISC = '<p style="font-size:26px;margin-top:0;opacity:.85">Contenuto informativo · Prodotti CE-IVD per uso professionale</p>'

def dots(n, on):
    return '<div style="display:flex;gap:16px;align-items:center">' + "".join(f'<div class="dot{" on" if i == on else ""}"></div>' for i in range(n)) + '</div>'
def cnt(to, pad=True, suffix="", size=300, color="var(--em)"):
    return f'<div class="e" data-k="count" data-in="0" data-d="0.8" data-from="{max(0,to-1) if to<10 else 0}" data-to="{to}"{" data-pad=1" if pad else ""} data-suffix="{suffix}"><div class="num" style="font-size:{size}px;color:{color}">0</div></div>'
def card(small, text, d=0.9):
    return f'<div class="cardx" style="margin-top:50px;padding:60px 56px"><small style="font-size:24px">{small}</small><p style="font-size:54px">{text}</p></div>'
def cta_btn(t, cls="m"):
    return f'<div class="pill {cls}" style="font-size:30px">{t}</div>'

# ---------- REEL 1 ----------
def reel1():
    sc = []
    s = Scene(0, 4, 'navy')
    s.add(eye("Il caso del bancone"), "fade", 0.1)
    s.words("Il campione può peggiorare. Dove?", 150, d0=0.3, step=0.15, em=(4,), mt=40)
    s.add(f'<div class="pill m" style="margin-top:70px;font-size:28px">5 punti da tenere d\'occhio</div>', "pop", 1.8)
    sc.append(s)
    pts = [("Identificazione", "Etichetta e provetta devono coincidere. Un errore qui si porta dietro tutto il resto.", ""),
           ("Prelievo", "Provetta giusta, ordine di prelievo corretto, tempi di stasi ridotti al minimo.", ""),
           ("Conservazione", "Temperatura e tempi di attesa seguono le istruzioni del produttore.", ""),
           ("Centrifugazione", "Parametri costanti: tempo, velocità e bilanciamento dei rotori.", ""),
           ("Controllo visivo", "Prima di analizzare, guarda il campione.", "pills")]
    for i, (t, x, k) in enumerate(pts):
        a = 4 + i * 3.8
        s = Scene(a, a + 3.8, 'white' if i % 2 == 0 else 'soft')
        s.add(eye(f"Punto {i+1} di 5"), "fade", 0.1)
        s.add(f'<div style="margin-top:40px">{cnt(i+1)}</div>'.replace('data-in="0"', f'data-in="{a+0.2:.2f}"'), "fade", 0.0, 0.1)
        s.words(t, 112, d0=0.5, step=0.12, mt=10)
        body = card("Cosa controllare", x)
        if k:
            body += '<div class="row" style="margin-top:34px">' + "".join(f'<div class="pill{" m" if j==0 else ""}" style="font-size:24px;padding:24px 34px">{w}</div>' for j, w in enumerate(["Emolisi", "Lipemia", "Ittero"])) + '</div>'
        s.add(body, "up", 1.1)
        s.add(dots(5, i), "fade", 1.3, style="margin-top:auto")
        sc.append(s)
    a = 4 + 5 * 3.8
    s = Scene(a, a + 3.2, 'mag')
    s.add(eye("Parliamone"), "fade", 0.1)
    s.words("Qual è il tuo punto critico?", 140, d0=0.3, step=0.14, mt=40)
    s.add(cta_btn("Rispondi nei commenti", "w"), "pop", 1.5, style="margin-top:auto")
    s.add(DISC, "fade", 1.8, style="margin-top:36px")
    sc.append(s)
    return "reel1-preanalitica", a + 3.2, sc

# ---------- REEL 2 ----------
def reel2():
    sc = []
    s = Scene(0, 3, 'mag')
    s.add(eye("Laboratorio"), "fade", 0.1)
    s.words("Mito o fatto?", 190, d0=0.3, step=0.2, mt=60)
    sc.append(s)
    s = Scene(3, 7, 'navy')
    s.add(eye("Il mito"), "fade", 0.1)
    s.add('<div style="position:relative;margin-top:50px"><h1 style="font-size:104px;margin-top:0">«FOB e calprotectina fanno la stessa cosa.»</h1>'
          '<div class="e" data-k="wipe" data-in="4.6" data-d="0.7" style="position:absolute;left:0;right:0;top:44%;height:12px;background:#FF2E5B"></div></div>', "up", 0.3)
    s.add('<div class="pill m" style="margin-top:80px">Mito</div>', "pop", 1.8)
    sc.append(s)
    drop = '<svg width="150" height="190" viewBox="0 0 60 76"><path d="M30 2C30 2 4 34 4 50a26 26 0 0052 0C56 34 30 2 30 2z" fill="#FF2E5B"/></svg>'
    s = Scene(7, 11.5, 'white')
    s.add(eye("Test 1 · FOB"), "fade", 0.1)
    s.add(f'<div style="margin-top:50px">{drop}</div>', "pop", 0.3)
    s.words("FOB: cerca sangue occulto", 108, d0=0.5, step=0.12, mt=24)
    s.add(card("In sintesi", "Rileva tracce di sangue nelle feci, anche non visibili a occhio nudo."), "up", 1.6)
    sc.append(s)
    bars = "".join(f'<div class="e" data-k="grow" data-in="{11.7+i*0.15:.2f}" data-d="0.7" style="width:90px;height:{h}px;background:{"#FF2E5B" if i==4 else "#0C1633"};border-radius:18px 18px 0 0"></div>' for i, h in enumerate([90, 150, 120, 230, 300]))
    s = Scene(11.5, 16, 'soft')
    s.add(eye("Test 2 · Calprotectina"), "fade", 0.1)
    s.add(f'<div style="display:flex;gap:24px;align-items:flex-end;height:310px;margin-top:50px">{bars}</div>', "fade", 0.2)
    s.words("Calprotectina: segnala infiammazione", 100, d0=0.5, step=0.1, mt=24)
    s.add(card("In sintesi", "Marcatore di infiammazione intestinale, non di sanguinamento."), "up", 1.8)
    sc.append(s)
    s = Scene(16, 20, 'navy')
    s.add(eye("Il confronto"), "fade", 0.1)
    s.add('<div class="row" style="margin-top:50px;gap:30px">'
          '<div class="cardx" style="flex:1"><small>FOB</small><p>Sangue occulto</p></div>'
          '<div class="cardx" style="flex:1"><small>Calprotectina</small><p>Infiammazione</p></div></div>', "up", 0.4)
    s.words("Domande diverse, risposte diverse.", 104, d0=1.2, step=0.1, em=(2, 3), mt=60)
    sc.append(s)
    s = Scene(20, 23.4, 'mag')
    s.add(eye("Fatto"), "fade", 0.1)
    s.words("Non sono intercambiabili.", 128, d0=0.3, step=0.14, mt=40)
    s.add('<p style="font-weight:600;color:#0C1633;font-size:40px">L\'interpretazione spetta al medico.</p>', "up", 1.4)
    s.add(cta_btn("Quale usi di più?", "w"), "pop", 2.0, style="margin-top:60px")
    sc.append(s)
    return "reel2-mito-fob-calprotectina", 23.4, sc

# ---------- REEL 3 ----------
def reel3():
    sc = []
    s = Scene(0, 4, 'white')
    s.add(eye("AVE-562"), "fade", 0.1)
    s.words("L'esame delle feci in 7 passi", 118, d0=0.3, step=0.13, em=(4, 5), mt=30)
    s.add(f'<div class="ph" style="height:560px;margin-top:44px;background:#F4F6FC"><img src="{P}/ave562.png" style="padding:10px"></div>', "up", 1.2)
    sc.append(s)
    steps = [("Carica", "Il campione viene caricato nello strumento."), ("Identifica", "Codice a barre: ogni provetta ha la sua identità."),
             ("Prepara", "Diluizione e preparazione automatiche."), ("Osserva", "Acquisizione automatica delle immagini."),
             ("Riconosci", "Il software classifica gli elementi osservati."), ("Misura", "Conteggio e quantificazione degli elementi."),
             ("Referta", "Dati pronti per la verifica e la validazione.")]
    for i, (t, x) in enumerate(steps):
        a = 4 + i * 2.7
        s = Scene(a, a + 2.7, 'soft' if i % 2 == 0 else 'white')
        s.add(eye(f"Passo {i+1} di 7"), "fade", 0.1)
        s.add(f'<div style="margin-top:30px">{cnt(i+1, size=260)}</div>'.replace('data-in="0"', f'data-in="{a+0.15:.2f}"'), "fade", 0, 0.1)
        s.words(t, 128, d0=0.4, step=0.12, mt=10)
        s.add(card("Cosa succede", x), "up", 0.9)
        s.add(dots(7, i), "fade", 1.0, style="margin-top:auto")
        sc.append(s)
    a = 4 + 7 * 2.7
    s = Scene(a, a + 4.2, 'navy')
    s.add(eye("Risultato"), "fade", 0.1)
    s.add(f'<div style="margin-top:30px">{cnt(90, pad=False, size=330, color="#FF2E5B")}</div>'.replace('data-in="0"', f'data-in="{a+0.3:.2f}"'), "fade", 0, 0.1)
    s.words("campioni/ora", 120, d0=0.9, mt=0)
    s.add(cta_btn("Scrivici in DM · 081 8045042"), "pop", 1.8, style="margin-top:auto")
    s.add(DISC, "fade", 2.2, style="margin-top:36px")
    sc.append(s)
    return "reel3-ave562-7-passi", a + 4.2, sc

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    for k, f in (("1", reel1), ("2", reel2), ("3", reel3)):
        if which in ("all", k):
            n, T, sc = f(); render(n, T, sc, OUT)
