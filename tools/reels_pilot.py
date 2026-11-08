import sys
from reels_engine import *
import reels_art as A
import reels_audio as AU
import pathlib
OUT = sys.argv[2] if len(sys.argv) > 2 else "/home/claude/reagenta-social/reels-pilota"
DISC = '<p style="font-size:26px;margin-top:0;opacity:.85">Contenuto informativo · Prodotti CE-IVD per uso professionale</p>'


FX = {
 'r1_hook': [(0.3+.15*i, 'tick') for i in range(5)] + [(1.7, 'pop')],
 'ident': [(.35, 'beep'), (.95, 'beep'), (1.55, 'beep'), (2.15, 'beep'), (2.5, 'ding')],
 'r1_prelievo': [(.25+.18*i, 'tick') for i in range(5)] + [(1.1+.25*i, 'pop') for i in range(5)] + [(2.3, 'swish')],
 'r1_conserv': [(.3, 'rise', .5)] + [(.5+.5*i, 'tock' if i%2 else 'tick') for i in range(6)],
 'r1_centrifuga': [(.0, 'whir', .8), (3.1, 'ding', .7)],
 'r1_visivo': [(.3+(i-.3)*.95+.3, 'pop') for i in range(4)],
 'r1_cta': [(.2, 'pop')] + [(.9+.52*i, 'tick') for i in range(3)],
 'r2_hook': [(.3, 'pop'), (.5, 'pop'), (.9, 'boing')],
 'r2_mito': [(.9, 'swish'), (1.8, 'thud')],
 'r2_fob': [(.5+.55*i+.55, 'plip') for i in range(3)] + [(1.6, 'beep'), (2.4, 'beep'), (2.6, 'ding', .6)],
 'r2_calpro': [(.2, 'swish', .8), (1.5, 'thud', .6), (2.2, 'bubble', .6), (2.7, 'bubble', .6)],
 'r2_confronto': [(.2, 'swish'), (.5, 'swish')],
 'r2_close': [(.5, 'swish'), (1.1, 'thud', .6)],
 'r3_carica': [(.3, 'swish', .8)] + [(1.5+.35*i, 'beep') for i in range(3)],
 'r3_prepara': [(.8+.6*i, 'plip') for i in range(3)] + [(2.3+.35*i, 'bubble') for i in range(3)],
 'r3_osserva': [(.1, 'beep'), (2.4, 'shutter')],
 'r3_riconosci': [(.8+.35*i, 'tick') for i in range(6)] + [(.8+.35*i, 'beep', .4) for i in range(6)],
 'r3_misura': [(.4+.18*i, 'pop', .6) for i in range(6)] + [(1.6, 'beep')],
 'r3_referta': [(.3+.2*i, 'tick') for i in range(6)] + [(1.9, 'ding')],
 'r3_close': [(.3, 'rise', .8), (2.25, 'ding')],
}

def K(fn):
    a, b = fn(); return (a, b, fn.__name__)

def dots(n, on):
    return '<div style="display:flex;gap:16px;align-items:center">' + "".join(f'<div class="dot{" on" if i == on else ""}"></div>' for i in range(n)) + '</div>'
def cta_btn(t, cls="m"):
    return f'<div class="pill {cls}" style="font-size:30px">{t}</div>'
def cap(s, text, d=1.2):
    s.add(f'<p style="font-size:50px;margin-top:0;font-weight:600;color:var(--h);line-height:1.3">{text}</p>', "up", d, style="margin-top:40px")

def step(a, dur, theme, eye_t, art, title, caption, n, i, tsize=104):
    s = Scene(a, a + dur, theme)
    s.add(eye(eye_t), "fade", 0.3)
    svg, js, key = art
    s.ill(svg, js, d=0.35, dur=0.5, style="margin-top:34px")
    s.fx(FX[key], 0.35)
    s.words(title, tsize, d0=0.6, step=0.12, mt=36)
    cap(s, caption)
    s.add(dots(n, i), "fade", 1.4, style="margin-top:auto")
    return s

def reel1():
    sc = []
    s = Scene(0, 4.4, 'navy')
    s.add(eye("Il caso del bancone"), "fade", 0.2)
    s.words("Il campione può peggiorare. Dove?", 118, d0=0.4, step=0.14, em=(4,), mt=30)
    s.fx(FX['r1_hook'], 0.3 if 'r1_hook' in ('r1_hook','r2_hook') else 0.35); s.ill(*A.r1_hook(), d=0.3, style="margin-top:20px")
    sc.append(s)
    P = [(K(A.ident), "white", "Identificazione", "Etichetta e provetta devono coincidere."),
         (K(A.r1_prelievo), "soft", "Prelievo", "Provetta giusta, ordine corretto, stasi minima."),
         (K(A.r1_conserv), "navy", "Conservazione", "Temperatura e tempi come da istruzioni."),
         (K(A.r1_centrifuga), "white", "Centrifugazione", "Parametri costanti, rotore bilanciato."),
         (K(A.r1_visivo), "soft", "Controllo visivo", "Prima di analizzare, guarda il campione.")]
    a = 4.4
    for i, (art, th, t, c) in enumerate(P):
        sc.append(step(a, 4.4, th, f"Punto {i+1} di 5", art, t, c, 5, i)); a += 4.4
    s = Scene(a, a + 3.4, 'mag')
    s.add(eye("Parliamone"), "fade", 0.3)
    s.fx(FX['r1_cta'], 0.3 if 'r1_cta' in ('r1_hook','r2_hook') else 0.35); s.ill(*A.r1_cta(), d=0.35, style="margin-top:10px")
    s.words("Qual è il tuo punto critico?", 118, d0=0.7, step=0.14, mt=20)
    s.add(cta_btn("Rispondi nei commenti", "w"), "pop", 1.6, style="margin-top:auto")
    s.add(DISC, "fade", 1.9, style="margin-top:30px")
    sc.append(s)
    return "reel1-preanalitica", a + 3.4, sc

def reel2():
    sc = []
    s = Scene(0, 3.4, 'mag')
    s.add(eye("Laboratorio"), "fade", 0.3)
    s.fx(FX['r2_hook'], 0.3 if 'r2_hook' in ('r1_hook','r2_hook') else 0.35); s.ill(*A.r2_hook(), d=0.3, style="margin-top:30px")
    s.words("Mito o fatto?", 190, d0=0.7, step=0.2, mt=40)
    sc.append(s)
    s = Scene(3.4, 8.2, 'navy')
    s.add(eye("Il mito"), "fade", 0.3)
    s.fx(FX['r2_mito'], 0.3 if 'r2_mito' in ('r1_hook','r2_hook') else 0.35); s.ill(*A.r2_mito(), d=0.35, style="margin-top:20px")
    s.words("FOB e calprotectina fanno la stessa cosa?", 84, d0=0.6, step=0.1, mt=20)
    sc.append(s)
    sc.append(step(8.2, 4.6, 'white', "Test 1 · FOB", K(A.r2_fob), "FOB", "Cerca tracce di sangue occulto.", 4, 0, 130))
    sc.append(step(12.8, 4.6, 'soft', "Test 2 · Calprotectina", K(A.r2_calpro), "Calprotectina", "Marcatore di infiammazione intestinale.", 4, 1, 104))
    s = Scene(17.4, 21.6, 'navy')
    s.add(eye("Il confronto"), "fade", 0.3)
    s.fx(FX['r2_confronto'], 0.3 if 'r2_confronto' in ('r1_hook','r2_hook') else 0.35); s.ill(*A.r2_confronto(), d=0.35, style="margin-top:20px")
    s.words("Domande diverse, risposte diverse.", 96, d0=1.3, step=0.1, em=(2, 3), mt=20)
    sc.append(s)
    s = Scene(21.6, 25.4, 'mag')
    s.add(eye("Fatto"), "fade", 0.3)
    s.fx(FX['r2_close'], 0.3 if 'r2_close' in ('r1_hook','r2_hook') else 0.35); s.ill(*A.r2_close(), d=0.35, style="margin-top:20px")
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
    P3 = [(K(A.r3_carica), "soft", "Carica", "Il campione entra nello strumento."),
          (K(A.ident), "white", "Identifica", "Il codice a barre lega provetta e risultato."),
          (K(A.r3_prepara), "soft", "Prepara", "Diluizione e miscelazione automatiche."),
          (K(A.r3_osserva), "white", "Osserva", "Acquisizione automatica delle immagini."),
          (K(A.r3_riconosci), "soft", "Riconosci", "Il software individua gli elementi."),
          (K(A.r3_misura), "white", "Misura", "Conteggio e quantificazione."),
          (K(A.r3_referta), "soft", "Referta", "Dati pronti per verifica e validazione.")]
    a = 4.4
    for i, (art, th, t, c) in enumerate(P3):
        sc.append(step(a, 3.6, th, f"Passo {i+1} di 7", art, t, c, 7, i, 124)); a += 3.6
    s = Scene(a, a + 4.6, 'navy')
    s.add(eye("Risultato"), "fade", 0.3)
    s.fx(FX['r3_close'], 0.3 if 'r3_close' in ('r1_hook','r2_hook') else 0.35); s.ill(*A.r3_close(), d=0.35, style="margin-top:30px")
    s.add('<p style="color:#fff;font-weight:600;font-size:48px;margin-top:10px">Il referto, senza attese inutili.</p>', "up", 1.6, style="margin-top:24px")
    s.add(cta_btn("Scrivici in DM · 081 8045042"), "pop", 2.2, style="margin-top:auto")
    s.add(DISC, "fade", 2.5, style="margin-top:30px")
    sc.append(s)
    return "reel3-ave562-7-passi", a + 4.6, sc

STY = {"1": ['iris', 'wipeL', 'blinds', 'wipeU', 'slash', 'wipeR'],
       "2": ['wipeU', 'slash', 'blinds', 'iris', 'wipeL'],
       "3": ['wipeL', 'blinds', 'iris', 'slash', 'wipeU', 'wipeR', 'blinds', 'iris']}

def make(k):
    n, T, sc = {"1": reel1, "2": reel2, "3": reel3}[k]()
    for j, s in enumerate(sc[1:]): s.trans = STY[k][j % len(STY[k])]
    return n, T, sc

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    mode = sys.argv[3] if len(sys.argv) > 3 else "both"
    if which == "snap":
        from playwright.sync_api import sync_playwright
        out = pathlib.Path("/tmp/claude-0/chk2"); out.mkdir(parents=True, exist_ok=True)
        with sync_playwright() as pw:
            b = pw.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
            for k in "123":
                n, T, sc = make(k); h = build(n, T, sc, out); pg.goto("file://" + str(h)); pg.wait_for_timeout(700)
                for j, x in enumerate(sc):
                    pg.evaluate(f"seek({x.start+(x.end-x.start)*0.82})"); pg.screenshot(path=str(out / f"{n}-{j:02d}.png"))
                for j, x in enumerate(sc[1:]):
                    for q, tt in enumerate((0.15, 0.3, 0.45)):
                        pg.evaluate(f"seek({x.start-0.3+tt*1.0/1})"); pg.screenshot(path=str(out / f"{n}-tr{j}-{q}.png"))
            b.close()
    else:
        for k in "123":
            if which in ("all", k):
                n, T, sc = make(k)
                if mode in ("both", "video"): render_silent(n, T, sc)
                if mode in ("both", "audio"):
                    ev = [e for s in sc for e in s.ev]; tr = [(s.start, s.trans) for s in sc[1:]]
                    wav = pathlib.Path(f"/tmp/claude-0/{n}.wav"); AU.mix(T, ev, tr, wav); mux(n, wav, OUT)
