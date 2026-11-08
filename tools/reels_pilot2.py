"""Reel 4-10 (feed del 9-13 novembre 2026)."""
import sys, pathlib
from reels_engine import *
import reels_art as A, reels_art2 as B, reels_audio as AU
from reels_pilot import K, cap, dots, cta_btn, DISC, step, FX
OUT = "/home/claude/reagenta-social/reels"
FX.update({
 'r4_timer': [(i*.5, 'tick', .5) for i in range(7)] + [(.8, 'pop')],
 'r4_options': [(.25+.4*i, 'pop') for i in range(4)] + [(2.2+.45*i, 'tick') for i in range(4)],
 'r4_ifu': [(.3+.2*i, 'tick') for i in range(5)] + [(1.7, 'ding')],
 'r5_doc': [(.1, 'swish', .5), (1.2, 'thud')],
 'r5_timeline': [(.1, 'swish', .7)] + [(.9+.5*i, 'pop') for i in range(3)],
 'r5_checks': [(.5+.7*i, 'ding', .6) for i in range(3)],
 'r5_ce': [(.3, 'pop'), (1.0, 'swish', .5)],
 'r6_elisa': [(.3+.35*i, 'tick', .4) for i in range(6)] + [(1.8, 'beep')],
 'r6_clia': [(.3+.3*i, 'bubble', .5) for i in range(5)] + [(1.5, 'ding', .6)],
 'r6_vs': [(.2, 'swish'), (.4, 'swish'), (1.0, 'boing')],
 'r7_hook3': [(i*.25, 'tick') for i in range(3)] + [(1.0+.3*i, 'pop') for i in range(3)],
 'r7_emolisi': [(.8, 'thud', .6)] + [(1.4+.35*i, 'pop') for i in range(3)],
 'r7_lipemia': [(.6, 'swish', .5)] + [(.8+.3*i, 'bubble', .5) for i in range(4)],
 'r7_ittero': [(.5, 'rise', .5), (1.6, 'pop')],
 'r8_rapido': [(i*.4, 'tick', .5) for i in range(6)] + [(1.2, 'beep'), (1.6, 'ding', .7)],
 'r8_lab': [(.5+.3*i, 'beep', .5) for i in range(3)] + [(.3+.2*i, 'pop', .5) for i in range(4)] + [(1.4, 'ding')],
 'r8_attenzione': [(.3, 'boing', .7), (1.1, 'swish', .6), (2.0, 'ding')],
 'r8_scale': [(.2, 'thud', .6), (1.2, 'tock'), (1.7, 'tock'), (2.2, 'tock', .6)],
 'r9_gear': [(i*.35, 'tick', .5) for i in range(8)],
 'r9_clean': [(.2+.5*i, 'swish', .4) for i in range(5)] + [(1.4+.3*i, 'ding', .4) for i in range(4)],
 'r9_qc': [(.3+.25*i, 'tick') for i in range(7)] + [(2.2, 'ding')],
 'r9_log': [(.3+.45*i, 'tick') for i in range(5)] + [(.7+.45*i, 'pop', .5) for i in range(5)],
 'r9_stock': [(.2+.25*i, 'thud', .4) for i in range(4)] + [(1.2, 'pop'), (1.8, 'ding', .6)],
 'r9_bookmark': [(.2, 'swish'), (.9, 'thud', .5)] + [(.9+.25*i, 'ding', .35) for i in range(3)],
 'r10_gears': [(i*.3, 'tick', .5) for i in range(10)],
 'r10_options': [(.25+.4*i, 'pop') for i in range(4)] + [(2.2+.5*i, 'tick') for i in range(4)],
})
def ART(mod, name): fn = getattr(mod, name); a, b = fn(); return (a, b, name)

def hook(t0, dur, theme, eye_t, title, tsize, em, art, zoom=.8, mt=26):
    s = Scene(t0, t0 + dur, theme); svg, js, key = art
    s.add(eye(eye_t), "fade", 0.3)
    s.words(title, tsize, d0=0.45, step=0.12, em=em, mt=mt)
    s.fx(FX[key], 0.9); s.ill(svg, js, d=0.9, dur=0.5, style=f"margin-top:20px;zoom:{zoom};align-self:center")
    return s

def plain(t0, dur, theme, eye_t, title, tsize, art, em=(), zoom=1):
    s = Scene(t0, t0 + dur, theme); svg, js, key = art
    s.add(eye(eye_t), "fade", 0.3); s.fx(FX[key], 0.35); s.ill(svg, js, d=0.35, dur=0.5, style=f"margin-top:30px;zoom:{zoom}")
    s.words(title, tsize, d0=0.6, step=0.12, em=em, mt=30)
    return s

def cta(t0, dur, eye_t, title, tsize, btn, art, zoom=.8, extra=None):
    s = Scene(t0, t0 + dur, 'mag'); svg, js, key = art
    s.add(eye(eye_t), "fade", 0.3); s.fx(FX[key], 0.35); s.ill(svg, js, d=0.35, dur=0.5, style=f"margin-top:10px;zoom:{zoom};align-self:center")
    s.words(title, tsize, d0=0.7, step=0.13, mt=20)
    s.add(cta_btn(btn, "w"), "pop", 1.6, style="margin-top:auto")
    s.add(extra or DISC, "fade", 1.9, style="margin-top:30px")
    return s

def S(t0, dur, theme, eye_t, art, title, caption, n, i, tsize=104):
    return step(t0, dur, theme, eye_t, art, title, caption, n, i, tsize)

def reel4():
    sc = [hook(0, 4.2, 'mag', "Domanda di mestiere", "Dopo il prelievo, quanto aspetti prima di centrifugare?", 104, (7,), ART(B, 'r4_timer'), .78)]
    sc[0].parts[-1] = sc[0].parts[-1]
    sc.append(plain(4.2, 5.0, 'white', "Le risposte più comuni", "Qual è la tua?", 130, ART(B, 'r4_options'), (3,)))
    sc.append(S(9.2, 4.8, 'soft', "Nella pratica", ART(B, 'r4_ifu'), "Istruzioni del produttore", "Il tempo corretto dipende da provetta e analita.", 3, 0))
    sc.append(cta(14.0, 3.8, "Parliamone", "Raccontaci la tua routine.", 118, "Rispondi nei commenti", ART(A, 'r1_cta')))
    return "reel4-centrifuga", 17.8, sc

def reel5():
    sc = [hook(0, 4.6, 'soft', "Qualità e norme", "IVDR: cosa cambia per chi compra diagnostici?", 100, (5,), ART(B, 'r5_doc'), .72)]
    sc.append(S(4.6, 5.2, 'white', "Dispositivi legacy", ART(B, 'r5_timeline'), "Le scadenze", "Sul mercato fino a fine 2027 (classe D), 2028 (C), 2029 (B e A sterile).", 4, 0, 124))
    sc.append(S(9.8, 4.8, 'soft', "Ma non per tutti", ART(B, 'r5_checks'), "A condizioni precise", "Entro le date previste per ogni classe.", 4, 1, 104))
    sc.append(S(14.6, 5.0, 'white', "Cosa fare", ART(B, 'r5_ce'), "Chiedi al fornitore", "Marcatura e documenti. Sintesi: vale il testo ufficiale.", 4, 2, 112))
    sc.append(cta(19.6, 4.0, "Per il tuo team", "Condividilo con il responsabile qualità.", 96, "Salva il post", ART(B, 'r9_bookmark'), .7,
                  '<p style="font-size:30px;margin-top:0;opacity:.9">Reg. (UE) 2017/746 · Reg. (UE) 2024/1860 · reagenta.it · 081 8045042</p>'))
    return "reel5-ivdr", 23.6, sc

def reel6():
    sc = [hook(0, 3.8, 'mag', "Immunodiagnostica", "Colore o luce?", 170, (2,), ART(B, 'r6_vs'), .85)]
    sc.append(S(3.8, 5.0, 'white', "ELISA", ART(B, 'r6_elisa'), "Cambia colore", "La reazione enzimatica cambia colore: si misura l'assorbanza.", 2, 0, 116))
    sc.append(S(8.8, 5.0, 'navy', "CLIA", ART(B, 'r6_clia'), "Emette luce", "La reazione chemiluminescente emette luce: si misura il segnale luminoso.", 2, 1, 116))
    sc.append(cta(13.8, 3.8, "Parliamone", "Quale usate, e perché?", 130, "Rispondi nei commenti", ART(A, 'r1_cta')))
    return "reel6-elisa-clia", 17.6, sc

def reel7():
    sc = [hook(0, 4.2, 'soft', "Il caso del bancone", "Rosso, lattescente, giallo intenso: il campione ti parla.", 100, (6, 7), ART(B, 'r7_hook3'), .85)]
    sc.append(S(4.2, 5.0, 'white', "Rosso", ART(B, 'r7_emolisi'), "Emolisi", "Rottura dei globuli rossi: rilascia potassio, LDH, AST e può alterare i valori.", 4, 0, 130))
    sc.append(S(9.2, 4.8, 'soft', "Lattescente", ART(B, 'r7_lipemia'), "Lipemia", "Siero torbido: può interferire con i metodi ottici e fotometrici.", 4, 1, 130))
    sc.append(S(14.0, 4.8, 'white', "Giallo intenso", ART(B, 'r7_ittero'), "Ittero", "Bilirubina elevata: può interferire con alcuni metodi.", 4, 2, 130))
    sc.append(S(18.8, 5.2, 'soft', "Cosa fare", K(A.r1_visivo), "Guarda, poi analizza", "Procedura del laboratorio: indici HIL, commento al referto, nuovo prelievo se serve.", 4, 3, 112))
    sc.append(cta(24.0, 3.6, "Per il tuo team", "Salva e condividi.", 130, "Salva il post", ART(B, 'r9_bookmark'), .7))
    return "reel7-hil", 27.6, sc

def reel8():
    sc = [hook(0, 4.2, 'soft', "Appropriatezza", "Test rapido o laboratorio? Non è una gara.", 104, (5, 6, 7), ART(B, 'r8_scale'), .85)]
    sc.append(S(4.2, 4.6, 'white', "Test rapido", ART(B, 'r8_rapido'), "Pochi minuti", "Utile al punto di cura, vicino al paziente.", 4, 0, 130))
    sc.append(S(8.8, 4.8, 'soft', "Laboratorio", ART(B, 'r8_lab'), "Qualità e tracciabilità", "Risultati quantitativi, controlli di qualità, volumi maggiori.", 4, 1, 100))
    sc.append(S(13.6, 5.0, 'white', "Attenzione", ART(B, 'r8_attenzione'), "Negativo non sempre basta", "Può servire una conferma, secondo il quadro clinico.", 4, 2, 100))
    sc.append(S(18.6, 4.4, 'soft', "In breve", ART(B, 'r8_scale'), "Complementari", "L'interpretazione spetta al medico.", 4, 3, 130))
    sc.append(cta(23.0, 3.6, "Parliamone", "Tu quale usi, e per cosa?", 118, "Rispondi nei commenti", ART(A, 'r1_cta')))
    return "reel8-rapido-laboratorio", 26.6, sc

def reel9():
    sc = [hook(0, 4.0, 'white', "Checklist del tecnico", "Manutenzione preventiva: 5 controlli.", 108, (2, 3), ART(B, 'r9_gear'), .8)]
    items = [('r9_clean', "Pulizia", "Pulizia e decontaminazione."), ('r9_qc', "Controllo qualità", "Controllo di qualità interno."),
             ('r9_gear', "Verifiche", "Verifiche secondo il produttore."), ('r9_log', "Registro", "Registro degli interventi."),
             ('r9_stock', "Scorte", "Scorte e scadenze dei consumabili.")]
    a = 4.0
    for i, (k, t, c) in enumerate(items):
        sc.append(S(a, 3.6, 'soft' if i % 2 == 0 else 'white', f"Controllo {i+1} di 5", ART(B, k), t, c, 5, i, 112 if len(t) > 8 else 130)); a += 3.6
    sc.append(cta(a, 3.8, "Per il prossimo turno", "Salva il post.", 140, "Salva il post", ART(B, 'r9_bookmark'), .75,
                  '<p style="font-size:28px;margin-top:0;opacity:.9">Indicazioni generali: valgono le istruzioni del produttore.</p>'))
    return "reel9-manutenzione", a + 3.8, sc

def reel10():
    sc = [hook(0, 4.2, 'navy', "Domanda del venerdì", "Qual è la prima cosa che automatizzeresti?", 100, (5, 6), ART(B, 'r10_gears'), .8)]
    sc.append(plain(4.2, 5.4, 'soft', "Scegli", "Una sola risposta.", 124, ART(B, 'r10_options'), (1, 2)))
    sc.append(cta(9.6, 3.8, "Parliamone", "Scrivici in DM.", 150, "O rispondi nei commenti", ART(A, 'r1_cta')))
    return "reel10-automatizzare", 13.4, sc

REELS = {"4": (reel4, ['wipeU', 'iris', 'blinds']), "5": (reel5, ['blinds', 'slash', 'wipeL', 'iris']), "6": (reel6, ['iris', 'wipeR', 'slash']),
         "7": (reel7, ['slash', 'wipeL', 'blinds', 'wipeU', 'iris']), "8": (reel8, ['wipeR', 'blinds', 'iris', 'wipeU', 'slash']),
         "9": (reel9, ['blinds', 'wipeL', 'slash', 'iris', 'wipeU', 'wipeR']), "10": (reel10, ['slash', 'blinds'])}

def make(k):
    f, st = REELS[k]; n, T, sc = f()
    for j, s in enumerate(sc[1:]): s.trans = st[j % len(st)]
    return n, T, sc

if __name__ == "__main__":
    which = sys.argv[1]; mode = sys.argv[2] if len(sys.argv) > 2 else "both"
    ks = list(REELS) if which == "all" else which.split(",")
    if mode == "snap":
        from playwright.sync_api import sync_playwright
        out = pathlib.Path("/tmp/claude-0/chk3"); out.mkdir(parents=True, exist_ok=True)
        with sync_playwright() as pw:
            b = pw.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
            for k in ks:
                n, T, sc = make(k); h = build(n, T, sc, out); pg.goto("file://" + str(h)); pg.wait_for_timeout(700)
                for j, x in enumerate(sc):
                    for q, fr in enumerate((0.45, 0.85)):
                        pg.evaluate(f"seek({x.start+(x.end-x.start)*fr})"); pg.screenshot(path=str(out / f"{n}-{j:02d}-{q}.png"))
            b.close()
    else:
        for k in ks:
            n, T, sc = make(k)
            if mode in ("both", "video"): render_silent(n, T, sc)
            if mode in ("both", "audio"):
                ev = [e for s in sc for e in s.ev]; tr = [(s.start, s.trans) for s in sc[1:]]
                wav = pathlib.Path(f"/tmp/claude-0/{n}.wav"); AU.mix(T, ev, tr, wav); mux(n, wav, OUT)
