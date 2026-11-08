import sys
from reels_engine import *
import reels_art as A
OUT = sys.argv[2] if len(sys.argv) > 2 else "/home/claude/reagenta-social/reels-pilota"
DISC = '<p style="font-size:26px;margin-top:0;opacity:.85">Contenuto informativo · Prodotti CE-IVD per uso professionale</p>'

def dots(n, on):
    return '<div style="display:flex;gap:16px;align-items:center">' + "".join(f'<div class="dot{" on" if i == on else ""}"></div>' for i in range(n)) + '</div>'
def cta_btn(t, cls="m"):
    return f'<div class="pill {cls}" style="font-size:30px">{t}</div>'
def cap(s, text, d=1.2):
    s.add(f'<p style="font-size:50px;margin-top:0;font-weight:600;color:var(--h);line-height:1.3">{text}</p>', "up", d, style="margin-top:40px")

def step(a, dur, theme, eye_t, art, title, caption, n, i, tsize=104):
    s = Scene(a, a + dur, theme)
    s.add(eye(eye_t), "fade", 0.3)
    svg, js = art
    s.ill(svg, js, d=0.35, dur=0.5, style="margin-top:34px")
    s.words(title, tsize, d0=0.6, step=0.12, mt=36)
    cap(s, caption)
    s.add(dots(n, i), "fade", 1.4, style="margin-top:auto")
    return s

def reel1():
    sc = []
    s = Scene(0, 4.4, 'navy')
    s.add(eye("Il caso del bancone"), "fade", 0.2)
    s.words("Il campione può peggiorare. Dove?", 118, d0=0.4, step=0.14, em=(4,), mt=30)
    s.ill(*A.r1_hook(), d=0.3, style="margin-top:20px")
    sc.append(s)
    P = [(A.ident(), "white", "Identificazione", "Etichetta e provetta devono coincidere."),
         (A.r1_prelievo(), "soft", "Prelievo", "Provetta giusta, ordine corretto, stasi minima."),
         (A.r1_conserv(), "navy", "Conservazione", "Temperatura e tempi come da istruzioni."),
         (A.r1_centrifuga(), "white", "Centrifugazione", "Parametri costanti, rotore bilanciato."),
         (A.r1_visivo(), "soft", "Controllo visivo", "Prima di analizzare, guarda il campione.")]
    a = 4.4
    for i, (art, th, t, c) in enumerate(P):
        sc.append(step(a, 4.4, th, f"Punto {i+1} di 5", art, t, c, 5, i)); a += 4.4
    s = Scene(a, a + 3.4, 'mag')
    s.add(eye("Parliamone"), "fade", 0.3)
    s.ill(*A.r1_cta(), d=0.35, style="margin-top:10px")
    s.words("Qual è il tuo punto critico?", 118, d0=0.7, step=0.14, mt=20)
    s.add(cta_btn("Rispondi nei commenti", "w"), "pop", 1.6, style="margin-top:auto")
    s.add(DISC, "fade", 1.9, style="margin-top:30px")
    sc.append(s)
    return "reel1-preanalitica", a + 3.4, sc

def reel2():
    sc = []
    s = Scene(0, 3.4, 'mag')
    s.add(eye("Laboratorio"), "fade", 0.3)
    s.ill(*A.r2_hook(), d=0.3, style="margin-top:30px")
    s.words("Mito o fatto?", 190, d0=0.7, step=0.2, mt=40)
    sc.append(s)
    s = Scene(3.4, 8.2, 'navy')
    s.add(eye("Il mito"), "fade", 0.3)
    s.ill(*A.r2_mito(), d=0.35, style="margin-top:20px")
    s.words("FOB e calprotectina fanno la stessa cosa?", 84, d0=0.6, step=0.1, mt=20)
    sc.append(s)
    sc.append(step(8.2, 4.6, 'white', "Test 1 · FOB", A.r2_fob(), "FOB", "Cerca tracce di sangue occulto.", 4, 0, 130))
    sc.append(step(12.8, 4.6, 'soft', "Test 2 · Calprotectina", A.r2_calpro(), "Calprotectina", "Marcatore di infiammazione intestinale.", 4, 1, 104))
    s = Scene(17.4, 21.6, 'navy')
    s.add(eye("Il confronto"), "fade", 0.3)
    s.ill(*A.r2_confronto(), d=0.35, style="margin-top:20px")
    s.words("Domande diverse, risposte diverse.", 96, d0=1.3, step=0.1, em=(2, 3), mt=20)
    sc.append(s)
    s = Scene(21.6, 25.4, 'mag')
    s.add(eye("Fatto"), "fade", 0.3)
    s.ill(*A.r2_close(), d=0.35, style="margin-top:20px")
    s.words("Non sono intercambiabili.", 128, d0=0.8, step=0.14, mt=20)
    s.add('<p style="font-weight:600;color:#0C1633;font-size:42px;margin-top:0">L\'interpretazione spetta al medico.</p>', "up", 1.8, style="margin-top:24px")
    s.add(cta_btn("Quale usi di più?", "w"), "pop", 2.4, style="margin-top:auto")
    sc.append(s)
    return "reel2-mito-fob-calprotectina", 25.4, sc

def reel3():
    sc = []
    s = Scene(0, 4.4, 'white')
    s.add(eye("AVE-562"), "fade", 0.3)
    s.words("L'esame delle feci in 7 passi", 118, d0=0.4, step=0.13, em=(4, 5), mt=30)
    s.add(f'<div class="ph" style="height:640px;margin-top:40px;background:#F4F6FC"><img src="{P}/ave562.png" style="padding:10px"></div>', "up", 1.2)
    s.add('<div style="display:flex;gap:14px;justify-content:center">' + ''.join(f'<div class="e" data-k="pop" data-in="{2.2+i*.2:.2f}" data-d="0.4" style="width:70px;height:70px;border-radius:50%;background:#0C1633;color:#fff;font-family:SG;font-weight:700;font-size:38px;display:flex;align-items:center;justify-content:center">{i+1}</div>' for i in range(7)) + '</div>', None, style="margin-top:36px")
    sc.append(s)
    P3 = [(A.r3_carica(), "soft", "Carica", "Il campione entra nello strumento."),
          (A.ident(), "white", "Identifica", "Il codice a barre lega provetta e risultato."),
          (A.r3_prepara(), "soft", "Prepara", "Diluizione e miscelazione automatiche."),
          (A.r3_osserva(), "white", "Osserva", "Acquisizione automatica delle immagini."),
          (A.r3_riconosci(), "soft", "Riconosci", "Il software individua gli elementi."),
          (A.r3_misura(), "white", "Misura", "Conteggio e quantificazione."),
          (A.r3_referta(), "soft", "Referta", "Dati pronti per verifica e validazione.")]
    a = 4.4
    for i, (art, th, t, c) in enumerate(P3):
        sc.append(step(a, 3.6, th, f"Passo {i+1} di 7", art, t, c, 7, i, 124)); a += 3.6
    s = Scene(a, a + 4.6, 'navy')
    s.add(eye("Risultato"), "fade", 0.3)
    s.ill(*A.r3_close(), d=0.35, style="margin-top:30px")
    s.add('<p style="color:#fff;font-weight:600;font-size:48px;margin-top:10px">Il referto, senza attese inutili.</p>', "up", 1.6, style="margin-top:24px")
    s.add(cta_btn("Scrivici in DM · 081 8045042"), "pop", 2.2, style="margin-top:auto")
    s.add(DISC, "fade", 2.5, style="margin-top:30px")
    sc.append(s)
    return "reel3-ave562-7-passi", a + 4.6, sc

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which == "snap":
        import pathlib
        from playwright.sync_api import sync_playwright
        out = pathlib.Path("/tmp/claude-0/chk2"); out.mkdir(parents=True, exist_ok=True)
        with sync_playwright() as p:
            b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
            for f in (reel1, reel2, reel3):
                n, T, sc = f(); h = build(n, T, sc, out); pg.goto("file://" + str(h)); pg.wait_for_timeout(700)
                for k, x in enumerate(sc):
                    pg.evaluate(f"seek({x.start+ (x.end-x.start)*0.82})")
                    pg.screenshot(path=str(out / f"{n}-{k:02d}.png"))
            b.close()
    else:
        for k, f in (("1", reel1), ("2", reel2), ("3", reel3)):
            if which in ("all", k):
                n, T, sc = f(); render(n, T, sc, OUT)
