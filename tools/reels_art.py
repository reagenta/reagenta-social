"""Libreria di illustrazioni SVG animabili per i Reel (palette Reagenta). Ogni funzione ritorna (svg, js)."""
import itertools
_id = itertools.count(1)
NAVY, MAG, SOFT, LIGHT, WHITE = '#0C1633', '#FF2E5B', '#F4F6FC', '#C9D0EC', '#FFFFFF'
CAPS = ['#7AA2F7', MAG, '#F2B01E', '#2FB67C', '#9B7BE6']

def svg(w, h, inner):
    return f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" style="display:block;overflow:visible">{inner}</svg>'

def tube(x, y, w=80, h=300, cap=MAG, liq='#F2D58A', lvl=.62, cls='', stroke=NAVY, glass='rgba(255,255,255,.7)', sw=6, inner=None):
    cid = next(_id); r = w / 2
    body = f'M{x} {y} V{y+h-r} A{r} {r} 0 0 0 {x+w} {y+h-r} V{y}Z'
    ly = y + h - (h - 20) * lvl
    liqs = inner or f'<rect class="liq" x="{x}" y="{ly}" width="{w}" height="{h}" fill="{liq}"/>'
    return (f'<g class="{cls}"><defs><clipPath id="c{cid}"><path d="{body}"/></clipPath></defs><path d="{body}" fill="{glass}"/>'
            f'<g clip-path="url(#c{cid})">{liqs}</g><path d="{body}" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>'
            f'<rect x="{x-8}" y="{y-26}" width="{w+16}" height="38" rx="12" fill="{cap}" stroke="{stroke}" stroke-width="{sw}"/></g>')

DROP = 'M30 2C30 2 4 34 4 50a26 26 0 0052 0C56 34 30 2 30 2z'
GUT = 'M40 150 V80 A40 40 0 0 1 80 40 H120 A40 40 0 0 1 160 80 V150'
CHECK = 'M-28 2 L-8 24 L30 -22'
BAR = [3, 9, 5, 14, 2, 11, 7, 12, 4, 10, 6, 13, 3, 8]

def barcode(x, y, w, h, color=NAVY):
    out, cx, i = '', x, 0
    while cx < x + w - 6:
        bw = 3 + (BAR[i % len(BAR)] % 4) * 3
        out += f'<rect x="{cx}" y="{y}" width="{bw}" height="{h}" fill="{color}"/>'
        cx += bw + 4 + BAR[(i + 3) % len(BAR)] % 3 * 2; i += 1
    return out

# ---------------- REEL 1 ----------------
def r1_hook():
    t = ''.join(tube(110 + i * 160, 200, 80, 300, CAPS[i], ['#F2D58A', '#F2D58A', '#F2D58A', '#F2D58A', '#F2D58A'][i], .6, f't{i}', LIGHT, 'rgba(255,255,255,.12)') for i in range(5))
    rack = f'<rect x="40" y="430" width="840" height="76" rx="22" fill="#14224D" stroke="{LIGHT}" stroke-width="4"/>'
    bub = f'<g class="bub"><circle cx="460" cy="100" r="64" fill="{MAG}"/><path d="M430 150 L452 188 L478 150Z" fill="{MAG}"/><text x="460" y="128" text-anchor="middle" font-family="SG" font-weight="700" font-size="92" fill="#fff">?</text></g>'
    js = """for(let i=0;i<5;i++){const g=Q('.t'+i);const r=ease(seg(lt,i*.15,.65+i*.15));let dy=(1-r)*420;
if(i==2){const k=ease(seg(lt,1.5,1.8));dy-=k*46+Math.sin(lt*9)*5*k;}
g.setAttribute('transform','translate(0 '+dy+')');g.style.opacity=Math.min(1,r*3);}
const k=seg(lt,1.7,2.2);Q('.bub').setAttribute('transform','translate(460 100) scale('+(k>0?back(k):0)+') translate(-460 -100)');"""
    return svg(920, 560, t + rack + bub), js

def ident(stroke=NAVY, bg_label='#fff'):
    t = tube(380, 120, 160, 540, MAG, '#F2D58A', .55, 'tb', stroke)
    lab = f'<rect x="395" y="300" width="130" height="190" rx="10" fill="{bg_label}" stroke="{stroke}" stroke-width="4"/>' + barcode(408, 330, 104, 120, stroke)
    br = ''.join(f'<path d="{d}" fill="none" stroke="{MAG}" stroke-width="10" stroke-linecap="round" class="br"/>' for d in
                 ['M350 330 V280 H400', 'M550 280 H600 V330', 'M600 470 V520 H550', 'M400 520 H350 V470'])
    beam = f'<defs><linearGradient id="bg{next(_id)}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{MAG}" stop-opacity="0"/><stop offset="1" stop-color="{MAG}" stop-opacity=".45"/></linearGradient></defs>'
    gid = f'bg{_id.__next__()-1}'
    bm = f'<g class="beam"><rect x="330" y="-44" width="280" height="44" fill="{MAG}" opacity=".25"/><rect x="330" y="-5" width="280" height="10" rx="5" fill="{MAG}"/></g>'
    chk = f'<g class="chk"><circle cx="0" cy="0" r="66" fill="{NAVY}"/><path d="{CHECK}" fill="none" stroke="#fff" stroke-width="15" stroke-linecap="round" stroke-linejoin="round"/></g>'
    js = """const a=ease(seg(lt,.1,.6));QA('.br').forEach((b,i)=>{b.style.opacity=a;});
const sw=lt<2.4?(0.5+0.5*Math.sin(lt*3.4-1.4)):0.5;const y=300+190*sw;
Q('.beam').setAttribute('transform','translate(0 '+y+')');Q('.beam').style.opacity=lt<2.3?1:Math.max(0,1-(lt-2.3)*4);
const k=seg(lt,2.5,3.0);Q('.chk').setAttribute('transform','translate(620 220) scale('+(k>0?back(k):0)+')');"""
    return svg(920, 720, t + lab + br + bm + chk), js

def r1_prelievo():
    x0 = [60 + i * 170 for i in range(5)]
    base = f'<rect x="30" y="578" width="860" height="26" rx="13" fill="{NAVY}"/>'
    tubes = ''.join(tube(x0[i], 250, 84, 330, CAPS[i], ['#9DB7F2', '#F27C93', '#F5D58A', '#7CD2AE', '#BFA9F0'][i], .6, f't{i}') for i in range(5))
    nums = ''.join(f'<g class="n{i}"><circle cx="{x0[i]+42}" cy="170" r="46" fill="{NAVY}"/><text x="{x0[i]+42}" y="190" text-anchor="middle" font-family="SG" font-weight="700" font-size="54" fill="#fff">{i+1}</text></g>' for i in range(5))
    arr = f'<path class="arr" d="M70 650 H840" stroke="{MAG}" stroke-width="12" stroke-linecap="round" fill="none" pathLength="100" stroke-dasharray="100"/><path class="ah" d="M800 618 L850 650 L800 682" stroke="{MAG}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" fill="none"/>'
    js = """for(let i=0;i<5;i++){const r=ease(seg(lt,i*.18,.7+i*.18));Q('.t'+i).setAttribute('transform','translate('+((1-r)*900)+' 0)');
const k=seg(lt,1.1+i*.25,1.5+i*.25);Q('.n'+i).setAttribute('transform','translate('+(Math.round(0))+' 0) translate('+(60+i*170+42)+' 170) scale('+(k>0?back(k):0)+') translate('+(-(60+i*170+42))+' -170)');}
Q('.arr').setAttribute('stroke-dashoffset',100*(1-ease(seg(lt,2.3,3.0))));Q('.ah').style.opacity=seg(lt,2.8,3.0);"""
    return svg(920, 720, base + tubes + nums + arr), js

def r1_conserv():
    th = (f'<rect x="120" y="150" width="60" height="400" rx="30" fill="rgba(255,255,255,.1)" stroke="{LIGHT}" stroke-width="8"/>'
          f'<circle cx="150" cy="580" r="66" fill="{MAG}"/><rect class="merc" x="138" y="500" width="24" height="60" rx="12" fill="{MAG}"/>')
    snow = ''.join(f'<line x1="-40" y1="0" x2="40" y2="0" stroke="{LIGHT}" stroke-width="8" stroke-linecap="round" transform="rotate({a})"/>' for a in (0, 60, 120))
    snow = f'<g class="snow">{snow}</g>'
    tb = tube(425, 230, 90, 330, '#7AA2F7', '#9DB7F2', .6, 'tb', LIGHT, 'rgba(255,255,255,.12)')
    ticks = ''.join(f'<line x1="0" y1="-135" x2="0" y2="-{150 if i%3 else 122}" stroke="{LIGHT}" stroke-width="{8 if i%3==0 else 5}" stroke-linecap="round" transform="rotate({i*30})"/>' for i in range(12))
    clock = (f'<g transform="translate(740 340)"><circle r="170" fill="rgba(255,255,255,.06)" stroke="{LIGHT}" stroke-width="10"/>{ticks}'
             f'<line class="hh" x1="0" y1="0" x2="0" y2="-80" stroke="#fff" stroke-width="14" stroke-linecap="round"/>'
             f'<line class="mh" x1="0" y1="0" x2="0" y2="-120" stroke="{MAG}" stroke-width="10" stroke-linecap="round"/><circle r="14" fill="{MAG}"/></g>')
    js = """const k=ease(seg(lt,.3,2.4));const my=560-4-k*380;Q('.merc').setAttribute('y',my+4);Q('.merc').setAttribute('height',560-my);
Q('.snow').setAttribute('transform','translate(150 90) rotate('+(lt*40)+')');
Q('.mh').setAttribute('transform','rotate('+(lt*160)+')');Q('.hh').setAttribute('transform','rotate('+(lt*160/12)+')');"""
    return svg(920, 720, th + snow + tb + clock), js

def r1_centrifuga():
    slots = ''.join(f'<circle cx="{160*__import__("math").cos(i*3.14159/3):.1f}" cy="{160*__import__("math").sin(i*3.14159/3):.1f}" r="46" fill="{"#FF6E8E" if i%2==0 else LIGHT}" stroke="#fff" stroke-width="5"/>' for i in range(6))
    rotor = (f'<g transform="translate(290 360)"><g class="mot" fill="none" stroke="{MAG}" stroke-width="10" stroke-linecap="round" opacity="0">'
             f'<path d="M-290 -20 A290 290 0 0 1 -150 -250"/><path d="M290 20 A290 290 0 0 1 150 250"/><path d="M-20 290 A290 290 0 0 1 -250 150"/></g>'
             f'<circle r="250" fill="{NAVY}"/><g class="rot">{slots}</g><circle r="64" fill="{MAG}"/><circle r="22" fill="#fff"/></g>')
    inner = ('<rect class="ser" x="600" y="140" width="130" height="500" fill="#F2D58A"/><rect class="rbc" x="600" y="640" width="130" height="0" fill="#B3243F"/>'
             '<rect class="mix" x="600" y="140" width="130" height="500" fill="#D9565C"/>')
    tb = tube(610, 150, 110, 480, NAVY, inner=inner, cls='tb')
    lab = (f'<g class="lab1" opacity="0"><text x="745" y="260" font-family="PM" font-weight="600" font-size="26" letter-spacing="4" fill="{NAVY}">SIERO</text></g>'
           f'<g class="lab2" opacity="0"><text x="745" y="560" font-family="PM" font-weight="600" font-size="26" letter-spacing="4" fill="{MAG}">CELLULE</text></g>')
    js = """const a=lt<2?60*lt*lt:240+240*(lt-2);Q('.rot').setAttribute('transform','rotate('+a+')');
Q('.mot').setAttribute('opacity',Math.min(1,Math.max(0,(a-80)/200))*(0.6+0.4*Math.sin(lt*30)));Q('.mot').setAttribute('transform','rotate('+(a*1.0)+')');
const k=ease(seg(lt,.8,3.2));const hh=k*190;Q('.rbc').setAttribute('y',640-hh);Q('.rbc').setAttribute('height',hh);Q('.mix').setAttribute('opacity',1-k);
Q('.lab1').setAttribute('opacity',seg(lt,2.9,3.3));Q('.lab2').setAttribute('opacity',seg(lt,3.0,3.4));"""
    return svg(920, 720, rotor + tb + lab), js

def r1_visivo():
    liqs = ['#F2D58A', '#E05A6F', '#F7F3EA', '#F0A81C']; names = ['OK', 'EMOLISI', 'LIPEMIA', 'ITTERO']
    tb = ''.join(tube(70 + i * 200, 170, 90, 340, [CAPS[0], MAG, CAPS[2], CAPS[3]][i], liqs[i], .72, f't{i}') for i in range(4))
    lb = ''.join(f'<g class="l{i}" opacity="0"><rect x="{70+i*200-30}" y="560" width="150" height="56" rx="28" fill="{MAG if i else NAVY}"/><text x="{70+i*200+45}" y="598" text-anchor="middle" font-family="PM" font-weight="600" font-size="26" letter-spacing="3" fill="#fff">{names[i]}</text></g>' for i in range(4))
    lens = (f'<g class="lens"><line x1="64" y1="64" x2="150" y2="150" stroke="{NAVY}" stroke-width="22" stroke-linecap="round"/>'
            f'<circle r="92" fill="rgba(255,255,255,.35)" stroke="{NAVY}" stroke-width="12"/></g>')
    js = """const u=Math.max(0,(lt-.3)/.95);const fi=Math.min(3,Math.floor(u)+ease(u%1));
Q('.lens').setAttribute('transform','translate('+(115+fi*200)+' '+(300+Math.sin(lt*5)*8)+')');
for(let i=0;i<4;i++){const k=seg(u,i-.3,i-.1);Q('.l'+i).setAttribute('opacity',k);}"""
    return svg(920, 720, tb + lb + lens), js

def r1_cta():
    inner = (f'<g class="bb"><rect x="120" y="40" width="680" height="340" rx="90" fill="#fff"/><path d="M200 370 L170 470 L300 380Z" fill="#fff"/>'
             f'<circle class="d0" cx="360" cy="210" r="34" fill="{NAVY}"/><circle class="d1" cx="460" cy="210" r="34" fill="{NAVY}"/><circle class="d2" cx="560" cy="210" r="34" fill="{NAVY}"/></g>')
    js = """const k=seg(lt,.2,.8);Q('.bb').setAttribute('transform','translate(460 420) scale('+(k>0?back(k):0)+') translate(-460 -420)');
for(let i=0;i<3;i++){const s=1+0.35*Math.max(0,Math.sin(lt*6-i*0.9));Q('.d'+i).setAttribute('transform','translate('+(360+i*100)+' 210) scale('+s+') translate('+(-(360+i*100))+' -210)');}"""
    return svg(920, 520, inner), js

# ---------------- REEL 2 ----------------
def gut_icon(sw=14, color=NAVY, bg='#fff', cls=''):
    return (f'<path class="{cls}" d="{GUT}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" pathLength="100"/>'
            f'<path d="{GUT}" fill="none" stroke="{bg}" stroke-width="{sw+2}" pathLength="100" stroke-dasharray="1.1 5.4" stroke-dashoffset="-2.5"/>')

def r2_hook():
    c1 = f'<g class="c1"><rect x="40" y="130" width="340" height="340" rx="60" fill="#fff"/><g transform="translate(130 190) scale(2.9)"><path d="{DROP}" fill="{MAG}"/></g></g>'
    c2 = f'<g class="c2"><rect x="540" y="130" width="340" height="340" rx="60" fill="#fff"/><g transform="translate(490 91) scale(2.2)">{gut_icon(14)}</g></g>'
    eq = f'<g class="eq"><rect x="-44" y="-36" width="88" height="18" rx="9" fill="{NAVY}"/><rect x="-44" y="18" width="88" height="18" rx="9" fill="{NAVY}"/></g>'
    js = """const a=seg(lt,.3,.8),b=seg(lt,.5,1.0),c=seg(lt,.9,1.3);
Q('.c1').setAttribute('transform','translate(210 300) scale('+(a>0?back(a):0)+') translate(-210 -300)');
Q('.c2').setAttribute('transform','translate(710 300) scale('+(b>0?back(b):0)+') translate(-710 -300)');
Q('.eq').setAttribute('transform','translate(460 300) rotate('+(Math.sin(lt*7)*7*c)+') scale('+(c>0?back(c):0)+')');"""
    return svg(920, 600, c1 + c2 + eq), js

def r2_mito():
    drop = f'<g transform="translate(70 120) scale(4.6)"><path d="{DROP}" fill="{MAG}"/></g>'
    gut = f'<g transform="translate(480 70) scale(2.2)">{gut_icon(14, LIGHT, NAVY)}</g>'
    eq = f'<rect x="395" y="250" width="130" height="22" rx="11" fill="#fff"/><rect x="395" y="320" width="130" height="22" rx="11" fill="#fff"/>'
    slash = f'<path class="sl" d="M380 160 L540 430" stroke="{MAG}" stroke-width="26" stroke-linecap="round" fill="none" pathLength="100" stroke-dasharray="100" stroke-dashoffset="100"/>'
    stamp = (f'<g class="st"><rect x="-210" y="-85" width="420" height="170" rx="26" fill="none" stroke="{MAG}" stroke-width="12"/>'
             f'<text y="42" text-anchor="middle" font-family="SG" font-weight="700" font-size="124" fill="{MAG}" letter-spacing="8">MITO</text></g>')
    js = """const k=ease(seg(lt,.9,1.4));Q('.sl').setAttribute('stroke-dashoffset',100*(1-k));
const s=seg(lt,1.8,2.2);const sh=s>0.9?Math.sin(lt*40)*4*(1-seg(lt,2.2,2.6)):0;
Q('.st').setAttribute('transform','translate('+(460+sh)+' 540) rotate(-8) scale('+(s>0?(1+(1-s)*1.4)*(back(s)>0?1:1):0)+')');Q('.st').style.opacity=Math.min(1,s*4);"""
    return svg(920, 640, drop + gut + eq + slash + stamp), js

def r2_fob():
    cas = (f'<rect x="170" y="320" width="580" height="290" rx="50" fill="{SOFT}" stroke="{NAVY}" stroke-width="8"/>'
           f'<circle cx="250" cy="465" r="36" fill="{NAVY}"/><rect x="340" y="395" width="350" height="140" rx="26" fill="#fff" stroke="{NAVY}" stroke-width="5"/>'
           f'<text x="470" y="382" text-anchor="middle" font-family="PM" font-weight="600" font-size="28" fill="{MAG}">T</text><text x="590" y="382" text-anchor="middle" font-family="PM" font-weight="600" font-size="28" fill="{NAVY}">C</text>'
           f'<rect class="cl" x="584" y="415" width="14" height="100" rx="7" fill="{NAVY}" opacity="0"/><rect class="tl" x="464" y="415" width="14" height="100" rx="7" fill="{MAG}" opacity="0"/>')
    pip = f'<rect x="214" y="10" width="72" height="130" rx="36" fill="{NAVY}"/><polygon points="226,140 274,140 250,200" fill="{NAVY}"/>'
    drops = ''.join(f'<g class="d{i}" opacity="0"><g transform="translate(250 0) scale(.7) translate(-30 0)"><path d="{DROP}" fill="{MAG}"/></g></g>' for i in range(3))
    js = """for(let i=0;i<3;i++){const u=((lt-.5-i*.55)%1.65)/1.0;const d=Q('.d'+i);if(lt>.5+i*.55&&lt<2.6&&u>=0&&u<1){const y=205+ease(u)*190;d.setAttribute('transform','translate(0 '+y+')');d.setAttribute('opacity',u>.9?(1-u)*10:1);}else d.setAttribute('opacity',0);}
Q('.cl').setAttribute('opacity',seg(lt,1.6,1.9));const t2=seg(lt,2.4,2.9);Q('.tl').setAttribute('opacity',t2);Q('.tl').setAttribute('transform','translate(471 465) scale(1 '+ease(t2)+') translate(-471 -465)');"""
    return svg(920, 640, cas + pip + drops), js

def r2_calpro():
    infl = f'<path class="inf" d="{GUT}" fill="none" stroke="{MAG}" stroke-width="14" stroke-linecap="round" pathLength="100" stroke-dasharray="0 100" stroke-dashoffset="-20"/>'
    base = f'<path class="base" d="{GUT}" fill="none" stroke="{NAVY}" stroke-width="14" stroke-linecap="round" stroke-linejoin="round" pathLength="100" stroke-dasharray="100 100" stroke-dashoffset="100"/>'
    rip = ''.join(f'<circle class="r{i}" cx="62" cy="62" r="10" fill="none" stroke="{MAG}" stroke-width="1.6" opacity="0"/>' for i in range(3))
    cuts = f'<path d="{GUT}" fill="none" stroke="{SOFT}" stroke-width="16" pathLength="100" stroke-dasharray="1.1 5.4" stroke-dashoffset="-2.5"/>'
    g = f'<g transform="translate(40 -105) scale(4.2)">{base}{infl}{cuts}{rip}</g>'
    js = """const k=ease(seg(lt,.2,1.5));Q('.base').setAttribute('stroke-dashoffset',100*(1-k));
const f=ease(seg(lt,1.5,2.0));const w=14+Math.max(0,Math.sin(lt*8))*5*f;const inf=Q('.inf');inf.setAttribute('stroke-dasharray',(24*f)+' 100');inf.setAttribute('stroke-width',w);
for(let i=0;i<3;i++){const u=((lt-1.7-i*.5)%1.5)/1.5;const c=Q('.r'+i);if(lt>1.7&&u>=0){c.setAttribute('r',10+u*55);c.setAttribute('opacity',(1-u)*.9);}else c.setAttribute('opacity',0);}"""
    return svg(920, 600, g), js

def r2_confronto():
    c1 = f'<g class="c1"><rect x="20" y="40" width="425" height="560" rx="56" fill="#fff"/><g transform="translate(120 130) scale(3.4)"><path d="{DROP}" fill="{MAG}"/></g><text x="232" y="530" text-anchor="middle" font-family="SG" font-weight="700" font-size="56" fill="{NAVY}">Sangue</text></g>'
    c2 = f'<g class="c2"><rect x="475" y="40" width="425" height="560" rx="56" fill="#fff"/><g transform="translate(427 33) scale(2.6)">{gut_icon(14)}</g><text x="687" y="530" text-anchor="middle" font-family="SG" font-weight="700" font-size="56" fill="{NAVY}">Infiammazione</text></g>'
    js = """const a=ease(seg(lt,.2,.9)),b=ease(seg(lt,.5,1.2));Q('.c1').setAttribute('transform','translate('+(-(1-a)*700)+' 0)');Q('.c2').setAttribute('transform','translate('+((1-b)*700)+' 0)');"""
    return svg(920, 640, c1 + c2), js

def r2_close():
    bars = f'<rect x="320" y="150" width="280" height="40" rx="20" fill="#fff"/><rect x="320" y="250" width="280" height="40" rx="20" fill="#fff"/>'
    sl = f'<path class="sl" d="M290 330 L630 110" stroke="{NAVY}" stroke-width="40" stroke-linecap="round" fill="none" pathLength="100" stroke-dasharray="100" stroke-dashoffset="100"/>'
    js = """Q('.sl').setAttribute('stroke-dashoffset',100*(1-ease(seg(lt,.5,1.1))));"""
    return svg(920, 440, bars + sl), js

# ---------------- REEL 3 ----------------
def r3_carica():
    tb = tube(425, 30, 80, 270, MAG, '#F2D58A', .6, 'tb')
    inst = (f'<rect x="120" y="330" width="680" height="320" rx="46" fill="{NAVY}"/>'
            + ''.join(f'<rect x="{560+i*0}" y="{360+i*14}" width="200" height="4" fill="{MAG}" opacity=".5"/>' for i in range(10))
            + f'<rect x="355" y="330" width="220" height="40" rx="20" fill="#050B1F"/>'
            + ''.join(f'<circle class="led{i}" cx="{190+i*44}" cy="560" r="14" fill="#2A3A6E"/>' for i in range(3)))
    js = """const r=ease(seg(lt,.3,1.5));Q('.tb').setAttribute('transform','translate(0 '+(r*150)+')');
for(let i=0;i<3;i++){const on=lt>1.5+i*.35;Q('.led'+i).setAttribute('fill',on?'#FF2E5B':'#2A3A6E');}"""
    return svg(920, 720, tb + inst), js

def r3_prepara():
    liq = '<rect class="lq" x="380" y="600" width="160" height="0" fill="#F2D58A"/><rect class="lq2" x="380" y="600" width="160" height="0" fill="#7AA2F7" opacity=".6"/>'
    tb = tube(380, 250, 160, 380, NAVY, inner=liq, cls='tb')
    pip = f'<rect x="434" y="10" width="52" height="110" rx="26" fill="{NAVY}"/><polygon points="442,120 478,120 460,170" fill="{NAVY}"/>'
    drops = ''.join(f'<g class="d{i}" opacity="0"><g transform="translate(460 0) scale(.5) translate(-30 0)"><path d="{DROP}" fill="{MAG}"/></g></g>' for i in range(3))
    ring = f'<circle class="ring" cx="460" cy="440" r="215" fill="none" stroke="{MAG}" stroke-width="10" stroke-dasharray="46 36" stroke-linecap="round" opacity="0"/>'
    bub = ''.join(f'<circle class="b{i}" cx="{420+i*40}" cy="600" r="{8+i*3}" fill="#fff" opacity="0"/>' for i in range(3))
    js = """const lv=ease(seg(lt,.5,2.6));const h=lv*250;Q('.lq').setAttribute('y',630-h);Q('.lq').setAttribute('height',h);Q('.lq2').setAttribute('y',630-h*.45);Q('.lq2').setAttribute('height',h*.45);
for(let i=0;i<3;i++){const u=((lt-.2-i*.6)%1.2)/1.2;const d=Q('.d'+i);if(lt<2.6&&lt>.2+i*.6&&u>=0&&u<1){d.setAttribute('transform','translate(0 '+(180+ease(u)*190)+')');d.setAttribute('opacity',u>.85?(1-u)*6.6:1)}else d.setAttribute('opacity',0);}
const rr=seg(lt,2.2,2.6);Q('.ring').setAttribute('opacity',rr);Q('.ring').setAttribute('transform','rotate('+(lt*180)+' 460 440)');
for(let i=0;i<3;i++){const u=((lt-2.2-i*.35)%1.2)/1.2;const b=Q('.b'+i);if(lt>2.2&&u>=0){b.setAttribute('transform','translate(0 '+(-u*280)+')');b.setAttribute('opacity',(1-u)*.9)}else b.setAttribute('opacity',0)}"""
    return svg(920, 720, tb + pip + drops + ring + bub), js

CELLS = [(-120, -80, 38, 38, 0), (60, -150, 30, 30, 1), (150, 20, 46, 30, 2), (-30, 60, 34, 34, 0), (-150, 120, 28, 44, 2), (90, 140, 36, 36, 1), (-60, -170, 24, 24, 1), (20, -30, 26, 26, 0)]
CFILL = ['#C9D0EC', '#FF8FA9', '#fff']

def field(cx, cy, r, stroke=NAVY):
    cid = next(_id)
    cells = ''.join(f'<ellipse class="cell" data-x="{x}" data-y="{y}" data-i="{i}" cx="{cx+x}" cy="{cy+y}" rx="{rx}" ry="{ry}" fill="{CFILL[c]}"/>' for i, (x, y, rx, ry, c) in enumerate(CELLS))
    return (f'<defs><clipPath id="f{cid}"><circle cx="{cx}" cy="{cy}" r="{r-16}"/></clipPath></defs><circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff" stroke="{stroke}" stroke-width="14"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r-16}" fill="{NAVY}"/><g clip-path="url(#f{cid})">{cells}</g>')

def r3_osserva():
    brk = ''.join(f'<path class="bk" d="{d}" fill="none" stroke="{MAG}" stroke-width="12" stroke-linecap="round"/>' for d in
                  ['M100 80 V20 H160', 'M820 80 V20 H760', 'M100 600 V660 H160', 'M820 600 V660 H760'])
    rec = f'<circle class="rec" cx="130" cy="120" r="12" fill="{MAG}"/>'
    fl = '<rect class="fl" x="-50" y="-50" width="1020" height="820" fill="#fff" opacity="0"/>'
    js = """QA('.cell').forEach(c=>{const i=+c.dataset.i,x=+c.dataset.x,y=+c.dataset.y;c.setAttribute('cx',460+x+Math.sin(lt*1.8+i*1.7)*34);c.setAttribute('cy',340+y+Math.cos(lt*1.5+i*2.1)*28);});
Q('.rec').setAttribute('opacity',Math.sin(lt*7)>0?1:0.15);const f=lt>2.4?Math.max(0,.9-(lt-2.4)*3):0;Q('.fl').setAttribute('opacity',f);
QA('.bk').forEach(b=>b.setAttribute('opacity',seg(lt,.1,.5)));"""
    return svg(920, 700, field(460, 340, 270) + brk + rec + fl), js

def r3_riconosci():
    boxes = ''.join(f'<g class="bx" data-x="{x}" data-y="{y}"><rect x="{460+x-rx-16}" y="{340+y-ry-16}" width="{2*rx+32}" height="{2*ry+32}" rx="12" fill="none" stroke="{MAG}" stroke-width="7" pathLength="100" stroke-dasharray="100" stroke-dashoffset="100"/>'
                    f'<rect x="{460+x-rx-16}" y="{340+y-ry-46}" width="54" height="26" rx="8" fill="{MAG}" opacity="0"/></g>' for i, (x, y, rx, ry, c) in enumerate(CELLS[:6]))
    js = """QA('.cell').forEach(c=>{const x=+c.dataset.x,y=+c.dataset.y;c.setAttribute('cx',460+x);c.setAttribute('cy',340+y);});
QA('.bx').forEach((g,i)=>{const k=ease(seg(lt,.4+i*.35,.8+i*.35));g.children[0].setAttribute('stroke-dashoffset',100*(1-k));g.children[1].setAttribute('opacity',seg(lt,.8+i*.35,1.0+i*.35));});"""
    return svg(920, 700, field(460, 340, 270) + boxes), js

def r3_misura():
    hs = [160, 260, 200, 380, 300, 440]
    ax = f'<path d="M70 60 V580 H880" fill="none" stroke="{NAVY}" stroke-width="10" stroke-linecap="round"/>' + ''.join(f'<line x1="56" y1="{580-i*80}" x2="84" y2="{580-i*80}" stroke="{NAVY}" stroke-width="6"/>' for i in range(1, 7))
    bars = ''.join(f'<rect class="bar" data-h="{h}" x="{120+i*120}" y="580" width="82" height="0" rx="14" fill="{MAG if i==5 else NAVY}"/>' for i, h in enumerate(hs))
    thr = f'<line class="thr" x1="70" y1="150" x2="880" y2="150" stroke="{MAG}" stroke-width="6" stroke-dasharray="18 14" opacity="0"/>'
    js = """QA('.bar').forEach((b,i)=>{const h=+b.dataset.h*ease(seg(lt,.2+i*.18,.9+i*.18));b.setAttribute('y',578-h);b.setAttribute('height',h);});
Q('.thr').setAttribute('opacity',seg(lt,1.6,1.9));"""
    return svg(920, 640, ax + bars + thr), js

def r3_referta():
    doc = (f'<rect x="250" y="20" width="420" height="590" rx="40" fill="#fff" stroke="{NAVY}" stroke-width="8"/><rect x="290" y="62" width="80" height="80" rx="24" fill="#0E2156"/>'
           + ''.join(f'<rect x="298" y="{72+i*14}" width="64" height="5" fill="{MAG}"/>' for i in range(5)))
    lines = ''.join(f'<rect class="ln" data-w="{w}" x="290" y="{190+i*60}" width="0" height="22" rx="11" fill="{LIGHT}"/>' for i, w in enumerate([340, 300, 340, 220, 320, 260]))
    chk = f'<g class="chk"><circle r="72" fill="{MAG}"/><path d="{CHECK}" fill="none" stroke="#fff" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/></g>'
    js = """QA('.ln').forEach((l,i)=>l.setAttribute('width',+l.dataset.w*ease(seg(lt,.3+i*.2,.7+i*.2))));
const k=seg(lt,1.9,2.4);Q('.chk').setAttribute('transform','translate(650 580) scale('+(k>0?back(k):0)+')');"""
    return svg(920, 660, doc + lines + chk), js

def r3_close():
    ring = (f'<circle cx="460" cy="280" r="230" fill="none" stroke="rgba(255,255,255,.15)" stroke-width="28"/>'
            f'<circle class="pr" cx="460" cy="280" r="230" fill="none" stroke="{MAG}" stroke-width="28" stroke-linecap="round" pathLength="100" stroke-dasharray="0 100" transform="rotate(-90 460 280)"/>'
            f'<text class="n" x="460" y="310" text-anchor="middle" font-family="SG" font-weight="700" font-size="220" fill="#fff" letter-spacing="-6">0</text>'
            f'<text x="460" y="385" text-anchor="middle" font-family="PM" font-weight="600" font-size="28" letter-spacing="5" fill="{LIGHT}">CAMPIONI / ORA</text>')
    js = """const k=ease(seg(lt,.3,2.2));Q('.pr').setAttribute('stroke-dasharray',(100*k)+' 100');Q('.n').textContent=Math.round(90*k);"""
    return svg(920, 560, ring), js
