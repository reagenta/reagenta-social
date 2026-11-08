"""Motion graphics Reel (1080x1920, 30 fps) per @reagenta.it.
Timeline in JS (seek(t)) -> screenshot di ogni frame con Playwright -> ffmpeg H.264.
Font, logo e palette come in gen_template / gen_2026-11-09_week_v2.
"""
import pathlib, subprocess, sys, shutil, html
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
        s.start, s.end, s.theme, s.parts = start, end, theme, []
    def add(s, inner, kind="up", d=0.0, dur=0.6, style=""):
        s.parts.append((inner, kind, d, dur, style)); return s
    def words(s, text, size, d0=0.2, step=0.13, em=(), style="", mt=24):
        """titolo parola per parola; em = indici in magenta"""
        ws = text.split()
        spans = []
        for i, w in enumerate(ws):
            inner = f'<em>{html.escape(w)}</em>' if i in em else html.escape(w)
            spans.append(f'<span class="e" data-k="up" data-in="{s.start+d0+i*step:.3f}" data-d="0.55" style="display:inline-block;margin-right:.28em">{inner}</span>')
        s.parts.append((f'<h1 style="font-size:{size}px;margin-top:{mt}px;{style}">{"".join(spans)}</h1>', None, 0, 0, ""))
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
                f'<div class="wrap">{head()}{"".join(out)}</div></div>')

JS = """
const ease=p=>1-Math.pow(1-p,3);
const back=p=>{const c1=1.70158,c3=c1+1;return 1+c3*Math.pow(p-1,3)+c1*Math.pow(p-1,2)};
function seek(t){
  document.querySelectorAll('.sc').forEach(sc=>{
    const s=+sc.dataset.s,e=+sc.dataset.e;
    let o=0;
    if(t>=s&&t<e){o=Math.min(1,(t-s)/0.25); if(t>e-0.25)o=Math.min(o,(e-t)/0.25);}
    sc.style.opacity=o; sc.style.visibility=o>0?'visible':'hidden';
  });
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
#pbw{{position:absolute;left:0;right:0;bottom:0;height:12px;background:rgba(127,127,160,.25);z-index:9}}
#pb{{height:100%;width:0;background:#FF2E5B}}
.dot{{width:26px;height:26px;border-radius:50%;background:#C9D0EC}}
.dot.on{{background:#FF2E5B;width:70px;border-radius:14px}}
</style></head><body>{body}<div id="pbw"><div id="pb"></div></div>
<script>const T={T};{JS}seek(0)</script></body></html>"""
    f = outdir / f"{name}.html"
    f.write_text(page)
    return f

def render(name, T, scenes, outroot):
    outroot = pathlib.Path(outroot); outroot.mkdir(parents=True, exist_ok=True)
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
    mp4 = outroot / f"{name}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(work / "f%05d.jpg"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "21", "-preset", "medium", "-movflags", "+faststart",
                    "-r", str(FPS), str(mp4)], check=True)
    # frame di anteprima (cover)
    for tt, nm in ((1.6, "cover"),):
        shutil.copy(work / f"f{int(tt*FPS):05d}.jpg", outroot / f"{name}-{nm}.jpg")
    shutil.rmtree(work)
    print(mp4, mp4.stat().st_size // 1024, "KB")
    return mp4
