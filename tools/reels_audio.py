"""Sound design sintetizzato (nessun campione esterno, nessun diritto di terzi): SFX + base musicale leggera."""
import numpy as np, wave
SR = 44100
rng = np.random.default_rng(7)

def env(n, a=0.005, d=0.1):
    t = np.arange(n) / SR
    return np.minimum(1, t / a) * np.exp(-t / d)
def sine(f, dur, ph=0): 
    t = np.arange(int(SR * dur)) / SR
    f = np.broadcast_to(f, t.shape) if np.ndim(f) == 0 else f
    return np.sin(2 * np.pi * np.cumsum(f) / SR + ph)
def sweep(f0, f1, dur, curve=1.0):
    t = np.linspace(0, 1, int(SR * dur)); return f0 + (f1 - f0) * t ** curve
def lowpass(x, fc):
    fc = np.broadcast_to(fc, x.shape).astype(float); a = np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); p = 0.0
    for i in range(len(x)): p = (1 - a[i]) * x[i] + a[i] * p; y[i] = p
    return y
def noise_sweep(dur, f0, f1, peak=0.5, vol=.5):
    n = int(SR * dur); x = rng.standard_normal(n); fc = np.linspace(f0, f1, n)
    y = lowpass(lowpass(x, fc), fc * 1.3); y = y - lowpass(y, 120)
    t = np.linspace(0, 1, n); e = np.where(t < peak, (t / peak) ** 1.6, ((1 - t) / (1 - peak)) ** 1.4)
    return y / (np.abs(y).max() + 1e-9) * e * vol

def S_pop(): n = int(SR * .16); return sine(sweep(700, 220, .16, .5), .16) * env(n, .002, .045) * .7
def S_tick(): n = int(SR * .05); return sine(2100, .05) * env(n, .001, .012) * .5
def S_tock(): n = int(SR * .07); return sine(950, .07) * env(n, .001, .02) * .6
def S_beep(): n = int(SR * .09); return np.tanh(2 * sine(1250, .09)) * env(n, .003, .05) * .35
def S_ding():
    n = int(SR * 1.0); return (sine(1318.5, 1.0) + .4 * sine(2637, 1.0) + .15 * sine(3951, 1.0)) * env(n, .003, .28) * .45
def S_plip(): n = int(SR * .13); return sine(sweep(500, 1000, .13), .13) * env(n, .002, .04) * .6
def S_thud():
    n = int(SR * .45); return (sine(sweep(120, 45, .45, .4), .45) * env(n, .002, .12) + noise_sweep(.45, 900, 200, .02, .3) * .5) * .9
def S_shutter(): return np.concatenate([noise_sweep(.04, 5000, 3000, .1, .6), np.zeros(int(SR * .06)), noise_sweep(.05, 4000, 2000, .1, .5)])
def S_swish(): return noise_sweep(.3, 1500, 7000, .55, .55)
def S_boing():
    n = int(SR * .5); f = 260 + 120 * np.sin(np.linspace(0, 16, n)) * np.exp(-np.linspace(0, 4, n)); return sine(f, .5) * env(n, .003, .18) * .5
def S_rise(dur=2.0):
    n = int(SR * dur); t = np.linspace(0, 1, n); return sine(sweep(220, 880, dur, 1.6), dur) * (.6 + .4 * np.sin(t * 60)) * np.minimum(1, t * 10) * np.minimum(1, (1 - t) * 10) * .22
def S_whir(dur=3.0):
    n = int(SR * dur); t = np.linspace(0, 1, n); x = sum(sine(sweep(70 * k, 320 * k, dur, 1.5), dur) / k for k in (1, 2, 3)); return x * np.minimum(1, t * 12) * np.minimum(1, (1 - t) * 6) * .13
def S_bubble(): n = int(SR * .12); return sine(sweep(400, 900, .12), .12) * env(n, .003, .035) * .45

def S_wipeL(): return noise_sweep(.6, 600, 5500, .5, .55)
def S_wipeR(): return noise_sweep(.6, 5500, 600, .5, .55)
def S_wipeU(): return noise_sweep(.6, 400, 3500, .5, .5) + S_rise(.6) * .5
def S_iris():
    x = S_rise(.6) * 1.4; pp = np.pad(S_pop(), (int(SR * .22), 0))[:len(x)]; x[:len(pp)] += pp * .7; return x
def S_blinds():
    base = noise_sweep(.6, 1500, 4500, .5, .35)
    for i in range(12):
        p = int(SR * (.02 + i * .04)); tk = S_tick() * .8; base[p:p + len(tk)] += tk[:len(base) - p]
    return base
def S_slash(): return noise_sweep(.5, 2500, 9000, .45, .6)
TRANS = dict(wipeL=S_wipeL, wipeR=S_wipeR, wipeU=S_wipeU, iris=S_iris, blinds=S_blinds, slash=S_slash)
SFX = dict(pop=S_pop, tick=S_tick, tock=S_tock, beep=S_beep, ding=S_ding, plip=S_plip, thud=S_thud, shutter=S_shutter,
           swish=S_swish, boing=S_boing, rise=S_rise, whir=S_whir, bubble=S_bubble)

def bed(T, bpm=104):
    n = int(SR * T); out = np.zeros(n); beat = 60 / bpm
    chords = [[220.0, 261.63, 329.63], [174.61, 220.0, 261.63], [261.63, 329.63, 392.0], [196.0, 246.94, 293.66]]
    bass = [110.0, 87.31, 130.81, 98.0]; arp = [0, 1, 2, 1]
    nb = int(T / beat) + 2
    for b in range(nb):
        t0 = b * beat; bar = (b // 4) % 4; ch = chords[bar]
        def put(x, at):
            i = int(at * SR); 
            if i < n: out[i:i + len(x)] += x[:n - i]
        if b % 4 == 0 or b % 4 == 2:  # kick
            k = sine(sweep(110, 48, .22, .4), .22) * env(int(SR * .22), .002, .07) * .55; put(k, t0)
        h = noise_sweep(.05, 7000, 7000, .1, .12); put(h, t0 + beat / 2)
        for j in range(2):  # arpeggio 8th notes
            f = ch[arp[(b * 2 + j) % 4] % 3] * 2; m = int(SR * .35)
            pl = (sine(f, .35) + .3 * sine(f * 2, .35)) * env(m, .003, .12) * .22; put(pl, t0 + j * beat / 2)
        if b % 4 == 0:
            m = int(SR * beat * 4); pad = sum(sine(f * .5, beat * 4) for f in ch) / 3 * np.minimum(1, np.arange(m) / (SR * .5)) * np.exp(-np.arange(m) / (SR * 5)) * .18; put(pad, t0)
            bs = sine(bass[bar], beat * 4) * env(int(SR * beat * 4), .01, 1.4) * .35; put(bs, t0)
    fade = np.minimum(1, np.arange(n) / (SR * 1.0)) * np.minimum(1, (n - np.arange(n)) / (SR * 1.5))
    return out * fade

def mix(T, events, trans, path, bed_gain=0.0):
    n = int(SR * (T + .3)); out = np.zeros(n); out[:int(SR * T)] += bed(T) * bed_gain
    def put(x, t, v):
        i = max(0, int(t * SR))
        if i < n: out[i:i + len(x)] += x[:n - i] * v
    for t, name, v in events:
        f = SFX[name]; put(f(), t, v)
    for b, st in trans: put(TRANS[st](), b - .3, .8)
    out = np.tanh(out * 1.1); out = out / max(1e-9, np.abs(out).max()) * .9
    pcm = (out[:int(SR * T)] * 32767).astype(np.int16)
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    return path
