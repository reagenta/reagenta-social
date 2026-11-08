"""Motion graphics Reel (1080x1920, 30 fps) per @reagenta.it.
Timeline in JS (seek(t)) -> screenshot di ogni frame con Playwright -> ffmpeg H.264.
Font, logo e palette come in gen_template / gen_2026-11-09_week_v2.
"""
import pathlib, subprocess, sys, shutil, html, json
from playwright.sync_api import sync_playwright
BASE = pathlib.Path(__file__).resolve().parent
src = (BASE / "gen_2026-11-09_week_v2.py").read_text().split("\nitems={}")[0]
ns = {}
exec(src, ns)           # CSS, TH, head, eye, mark, F, P ...
CSS, TH, head, eye, P = ns["CSS"], ns["TH"], ns["head"], ns["eye"], ns["P"]
FPS = 30

def e(inner, kind="up", d=0.0, dur=0.6, style=""):
    """elemento animato; d = ritardo dall'inizio della scena (settato da Scene)."""
    return ("E", inner, kind, d, dur, style)

class Scene:
    def __init__(s, start, end, theme):
        s.start, s.end, s.theme, s.parts, s.ev, s.trans = start, end, theme, [], [], 'wipeL'
    def add(s, inner, kind="up", d=0.0, dur=0.6, style=""):
        s.parts.append((inner, kind, d, dur, style))
        if kind == 'pop': s.ev.append((s.start + d, 'pop', 0.8))
        return s
    def fx(s, items, base=0.0):
        for off, name, *v in items: s.ev.append((s.start + base + off, name, v[0] if v else 1.0))
        return s
    def words(s, text, size, d0=0.2, step=0.13, em=(), style="", mt=24):
        """titolo parola per parola; em = indici in magenta"""
        ws = text.split()
        spans = []
        for i, w in enumerate(ws):
            inner = f'<em>{html.escape(w)}</em>' if i in em else html.escape(w)
            s.ev.append((s.start + d0 + i * step, 'tick', 0.22))
            spans.append(f'<span class="e" data-k="up" data-in="{s.start+d0+i*step:.3f}" data-d="0.55" style="display:inline-block;margin-right:.28em">{inner}</span>')
        s.parts.append((f'<h1 style="font-size:{size}px;margin-top:{mt}px;{style}">{"".join(spans)}</h1>', None, 0, 0, ""))
        return s
    def ill(s, svg, js, d=0.35, dur=0.5, style=""):
        code = html.escape(js, quote=True)
        s.parts.append((f'<div class="e" data-k="js" data-in="{s.start+d:.3f}" data-d="{dur}" data-js="{code}" style="{style}">{svg}</div>', None, 0, 0, ""))
        return s
    def render(s):
        th = TH[s.theme]
        v = ";".join(f"--{k}:{x}" for k, x in th.items())
        out = []
        for inner, kind, d, dur, style in s.parts:
            if kind is None:
                out.append(inner)
            else:
                out.append(f'<div class="e" data-k="{kind}" data-in="{s.start+d:.3f}" data-d="{dur}" style="{style}">{inner}</div>')
        return (f'<div class="sc" data-s="{s.start}" data-e="{s.end}" style="background:{th["bg"]};{v}">'
                f'<div class="wrap"><div style="height:111px;flex:none"></div>{"".join(out)}</div></div>')

JS = """
const seg=(x,a,b)=>Math.max(0,Math.min(1,(x-a)/(b-a)));
const ease=p=>1-Math.pow(1-p,3);
const back=p=>{const c1=1.70158,c3=c1+1;return 1+c3*Math.pow(p-1,3)+c1*Math.pow(p-1,2)};
function seek(t){
  document.querySelectorAll('.sc').forEach(sc=>{
    const s=+sc.dataset.s,e=+sc.dataset.e;
    const o=(t>=s&&t<e)?1:0;
    sc.style.opacity=o; sc.style.visibility=o>0?'visible':'hidden';
  });
  let cur=TH_[0]; for(const h of TH_) if(t>=h.s) cur=h;
  const gh=document.getElementById('gh'); gh.style.setProperty('--wm',cur.wm); gh.style.setProperty('--sub',cur.sub); gh.style.setProperty('--line',cur.line);
  ['t1','t2','t3a','t3b','t4','t5'].forEach(i=>document.getElementById(i).style.display='none');
  for(const [b,st] of B){const p=(t-(b-0.3))/0.6; if(!(p>0&&p<1)) continue; const h=p<0.5, q=h?ease(p*2):ease((p-0.5)*2);
    if(st==='wipeL'||st==='wipeR'){const el=document.getElementById('t1'),d=st==='wipeL'?1:-1;el.style.display='block';
      el.style.transform=h?`translateX(${-d*100+d*100*q}%)`:`translateX(${d*100*q}%)`}
    else if(st==='wipeU'){const el=document.getElementById('t2');el.style.display='block';
      el.style.transform=h?`translateY(${100-100*q}%)`:`translateY(${-100*q}%)`}
    else if(st==='iris'){const R=(h?q:1-q)*1180;
      for(const [id,r] of [['t3a',R+50],['t3b',R]]){const el=document.getElementById(id);el.style.display='block';el.style.clipPath=`circle(${Math.max(0,r)}px at 50% 50%)`}}
    else if(st==='blinds'){const el=document.getElementById('t4');el.style.display='block';
      [...el.children].forEach((c,i)=>{const u=seg(h?p*2:p*2-1,i*0.04,i*0.04+0.55),k=ease(u);
        if(h){c.style.transformOrigin='left center';c.style.transform=`scaleX(${k})`}else{c.style.transformOrigin='right center';c.style.transform=`scaleX(${1-k})`}})}
    else if(st==='slash'){const X=125*q;const el=document.getElementById('t5');el.style.display='block';
      el.style.clipPath=h?`polygon(0 0,${X}% 0,${X-25}% 100%,0 100%)`:`polygon(${X}% 0,100% 0,100% 100%,${X-25}% 100%)`}
  }
  document.querySelectorAll('.e').forEach(el=>{
    const i=+el.dataset.in,d=+el.dataset.d,k=el.dataset.k;
    let p=Math.max(0,Math.min(1,(t-i)/d));
    if(k==='up'){el.style.opacity=ease(p);el.style.transform=`translateY(${(1-ease(p))*70}px)`}
    else if(k==='pop'){el.style.opacity=Math.min(1,p*3);el.style.transform=`scale(${0.55+0.45*back(p)})`}
    else if(k==='left'){el.style.opacity=ease(p);el.style.transform=`translateX(${-(1-ease(p))*160}px)`}
    else if(k==='right'){el.style.opacity=ease(p);el.style.transform=`translateX(${(1-ease(p))*160}px)`}
    else if(k==='fade'){el.style.opacity=ease(p)}
    else if(k==='wipe'){el.style.transformOrigin='left center';el.style.transform=`scaleX(${ease(p)})`;el.style.opacity=p>0?1:0}
    else if(k==='grow'){el.style.transformOrigin='center bottom';el.style.transform=`scaleY(${ease(p)})`;el.style.opacity=p>0?1:0}
    else if(k==='js'){const f=el._f||(el._f=new Function('p','lt','el','ease','back','seg',"const Q=s=>el.querySelector(s),QA=s=>[...el.querySelectorAll(s)];el.style.opacity=ease(p);el.style.transform='scale('+(0.92+0.08*ease(p))+')';"+el.dataset.js)); f(p,Math.max(0,t-i),el,ease,back,seg);}
    else if(k==='count'){const to=+el.dataset.to,from=+el.dataset.from||0;
      const v=Math.round(from+(to-from)*ease(p));
      el.firstElementChild.textContent=(el.dataset.pad?String(v).padStart(2,'0'):v)+(el.dataset.suffix||'');
      el.style.opacity=Math.min(1,p*4);el.style.transform=`scale(${0.8+0.2*ease(p)})`}
  });
  const pb=document.getElementById('pb'); if(pb) pb.style.width=(100*t/T)+'%';
}
"""

def build(name, T, scenes, outdir):
    body = "".join(sc.render() for sc in scenes)
    page = f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}
body{{width:1080px;height:1920px;background:#0C1633;position:relative;overflow:hidden}}
.sc{{position:absolute;inset:0;opacity:0;visibility:hidden;color:var(--fg)}}
.sc .wrap{{top:200px;bottom:330px}}
.e{{will-change:transform,opacity;opacity:0}}
#gh{{height:111px}}
.tr{{position:absolute;inset:0;z-index:8;display:none}}
#pbw{{position:absolute;left:0;right:0;bottom:0;height:12px;background:rgba(127,127,160,.25);z-index:9}}
#pb{{height:100%;width:0;background:#FF2E5B}}
.dot{{width:26px;height:26px;border-radius:50%;background:#C9D0EC}}
.dot.on{{background:#FF2E5B;width:70px;border-radius:14px}}
</style></head><body>{body}<div id="gh" class="wrap" style="top:200px;z-index:9">{head()}</div>
<div id="t1" class="tr" style="background:linear-gradient(to right,#0C1633 0 40px,#FF2E5B 40px calc(100% - 40px),#0C1633 calc(100% - 40px))"></div>
<div id="t2" class="tr" style="background:linear-gradient(to bottom,#0C1633 0 40px,#FF2E5B 40px calc(100% - 40px),#0C1633 calc(100% - 40px))"></div>
<div id="t3a" class="tr" style="background:#0C1633"></div><div id="t3b" class="tr" style="background:#FF2E5B"></div>
<div id="t4" class="tr" style="background:none">{"".join(f'<div style="position:absolute;left:0;right:0;top:{i*160}px;height:161px;background:{"#FF2E5B" if i%2==0 else "#0C1633"}"></div>' for i in range(12))}</div>
<div id="t5" class="tr" style="background:#FF2E5B"></div>
<div id="pbw"><div id="pb"></div></div>
<script>const T={T};const B={json.dumps([[sc.start, sc.trans] for sc in scenes[1:]])};const TH_={json.dumps([dict(s=sc.start, wm=TH[sc.theme]['wm'], sub=TH[sc.theme]['sub'], line=TH[sc.theme]['line']) for sc in scenes])};{JS}seek(0)</script></body></html>"""
    f = outdir / f"{name}.html"
    f.write_text(page)
    return f

def render_silent(name, T, scenes):
    work = pathlib.Path("/tmp/claude-0/reelwork") / name
    if work.exists(): shutil.rmtree(work)
    work.mkdir(parents=True)
    f = build(name, T, scenes, work)
    n = int(T * FPS)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto("file://" + str(f)); pg.wait_for_timeout(800)
        for i in range(n):
            pg.evaluate(f"seek({i/FPS})")
            pg.screenshot(path=str(work / f"f{i:05d}.jpg"), type="jpeg", quality=92)
        b.close()
    sd = pathlib.Path("/tmp/claude-0/silent"); sd.mkdir(parents=True, exist_ok=True)
    mp4 = sd / f"{name}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(work / "f%05d.jpg"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "21", "-preset", "medium", "-movflags", "+faststart",
                    "-r", str(FPS), str(mp4)], check=True)
    shutil.copy(work / f"f{int(1.6*FPS):05d}.jpg", sd / f"{name}-cover.jpg")
    shutil.rmtree(work)
    return mp4

def mux(name, wav, outroot):
    outroot = pathlib.Path(outroot); outroot.mkdir(parents=True, exist_ok=True)
    out = outroot / f"{name}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"/tmp/claude-0/silent/{name}.mp4", "-i", str(wav),
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(out)], check=True)
    shutil.copy(f"/tmp/claude-0/silent/{name}-cover.jpg", outroot / f"{name}-cover.jpg")
    print(out, out.stat().st_size // 1024, "KB")
    return out
