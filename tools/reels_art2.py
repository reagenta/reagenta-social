"""Illustrazioni SVG animabili, seconda serie (reel 4-10)."""
import math
from reels_art import *

def T(x, y, txt, size=44, color=NAVY, anchor='middle', font='SG', ls=0, cls=''):
    w = 700 if font == 'SG' else 600
    return f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}" font-family="{font}" font-weight="{w}" font-size="{size}" letter-spacing="{ls}" fill="{color}">{txt}</text>'
def badge(cls, r=66, color=NAVY):
    return f'<g class="{cls}"><circle r="{r}" fill="{color}"/><path d="{CHECK}" fill="none" stroke="#fff" stroke-width="15" stroke-linecap="round" stroke-linejoin="round"/></g>'
def gear(cx, cy, r, teeth, color=NAVY, cls='', hole=None):
    t = ''.join(f'<rect x="{-r*.16}" y="{-r*1.18}" width="{r*.32}" height="{r*.34}" rx="{r*.08}" fill="{color}" transform="rotate({i*360/teeth})"/>' for i in range(teeth))
    hl = f'<circle r="{r*.34}" fill="{hole or "#fff"}"/>'
    return f'<g class="{cls}" transform="translate({cx} {cy})"><g class="gi">{t}<circle r="{r}" fill="{color}"/>{hl}</g></g>'

# ---------------- REEL 4: centrifugazione ----------------
def r4_timer():
    ticks = ''.join(f'<line x1="0" y1="-190" x2="0" y2="-{175 if i%5 else 158}" stroke="{NAVY}" stroke-width="{8 if i%5==0 else 4}" stroke-linecap="round" transform="rotate({i*6})"/>' for i in range(60))
    sw = (f'<g transform="translate(400 390)"><rect x="-32" y="-300" width="64" height="48" rx="14" fill="{NAVY}"/><rect x="-14" y="-262" width="28" height="30" fill="{NAVY}"/>'
          f'<circle r="230" fill="#fff" stroke="{NAVY}" stroke-width="16"/><path class="pie" d="" fill="{MAG}" opacity=".9"/>{ticks}'
          f'<line class="hand" x1="0" y1="30" x2="0" y2="-190" stroke="{NAVY}" stroke-width="12" stroke-linecap="round"/><circle r="18" fill="{NAVY}"/></g>')
    tb = tube(740, 250, 90, 330, CAPS[0], '#F2D58A', .6, 'tb')
    q = f'<g class="q" opacity="0"><circle cx="785" cy="160" r="52" fill="{MAG}"/>{T(785,190,"?",74,"#fff")}</g>'
    js = """const a=lt*140;const r=a*Math.PI/180;const x=190*Math.sin(r),y=-190*Math.cos(r);Q('.hand').setAttribute('transform','rotate('+a+')');
const f=Math.floor(a/360)%2==0;const aa=a%360;const x2=230*Math.sin(aa*Math.PI/180),y2=-230*Math.cos(aa*Math.PI/180);
Q('.pie').setAttribute('d',aa<1?'':'M0 0 L0 -230 A230 230 0 '+(aa>180?1:0)+' 1 '+x2+' '+y2+'Z');
Q('.tb').setAttribute('transform','translate(0 '+(Math.sin(lt*6)*4)+')');PO(Q('.q'),seg(lt,.8,1.2),785,160);Q('.q').setAttribute('opacity',seg(lt,.8,1.0));"""
    return svg(920, 720, sw + tb + q), js

def r4_options():
    cards = []
    pos = [(10, 20), (470, 20), (10, 390), (470, 390)]
    lab = ["Subito", "Entro un'ora", "Dall'analita", "Dal turno"]
    ico = [f'<path d="M-16 -70 L-56 14 H-8 L-26 70 L40 -18 H-8 L18 -70Z" fill="{MAG}"/>',
           f'<circle r="62" fill="none" stroke="{NAVY}" stroke-width="12"/><path d="M0 -36 V0 L26 18" fill="none" stroke="{MAG}" stroke-width="12" stroke-linecap="round"/>',
           f'<g transform="translate(-30 -76) scale(.62)">{tube(0,0,100,230,CAPS[1],"#F2D58A",.6,"",NAVY,"#fff")}</g>',
           f'<circle cx="-14" r="42" fill="{MAG}"/><path d="M42 -50 A60 60 0 1 0 42 50 A44 44 0 1 1 42 -50Z" fill="{NAVY}" opacity="0"/>' + ''.join(f'<line x1="-14" y1="-62" x2="-14" y2="-78" stroke="{MAG}" stroke-width="9" stroke-linecap="round" transform="rotate({a} -14 0)"/>' for a in range(0, 360, 45))]
    for i, (x, y) in enumerate(pos):
        cards.append(f'<g class="c{i}"><rect x="{x}" y="{y}" width="440" height="330" rx="52" fill="{SOFT}"/><g transform="translate({x+220} {y+120})">{ico[i]}</g>'
                     + T(x + 220, y + 270, lab[i], 46) + f'<rect class="hl{i}" x="{x}" y="{y}" width="440" height="330" rx="52" fill="none" stroke="{MAG}" stroke-width="10" opacity="0"/></g>')
    js = """for(let i=0;i<4;i++){PO(Q('.c'+i),seg(lt,.25+i*.4,.65+i*.4),[230,690,230,690][i],[185,185,555,555][i]);}
const w=Math.floor(Math.max(0,lt-2.2)/.45)%4;for(let i=0;i<4;i++)Q('.hl'+i).setAttribute('opacity',lt>2.2&&w==i?1:0);"""
    return svg(920, 720, ''.join(cards)), js

def r4_ifu():
    pg = (f'<path d="M460 80 Q330 40 150 70 V560 Q330 530 460 580Z" fill="#fff" stroke="{NAVY}" stroke-width="10" stroke-linejoin="round"/>'
          f'<path d="M460 80 Q590 40 770 70 V560 Q590 530 460 580Z" fill="#fff" stroke="{NAVY}" stroke-width="10" stroke-linejoin="round"/>')
    tb = f'<g transform="translate(225 170) scale(.9)">{tube(0,0,90,300,MAG,"#F2D58A",.6,"")}</g>'
    ln = ''.join(f'<rect class="ln" data-w="{w}" x="520" y="{150+i*62}" width="0" height="20" rx="10" fill="{LIGHT}"/>' for i, w in enumerate([210, 180, 210, 130, 190]))
    js = """QA('.ln').forEach((l,i)=>l.setAttribute('width',+l.dataset.w*ease(seg(lt,.3+i*.2,.7+i*.2))));const k=seg(lt,1.7,2.2);Q('.bd').setAttribute('transform','translate(700 540) scale('+(k>0?back(k):0)+')');"""
    return svg(920, 700, pg + tb + ln + badge('bd').replace('<g class="bd">', '<g class="bd" transform="translate(700 540) scale(0)"><g transform="translate(0 0)">', 1).replace('</g>', '</g></g>', 1)), js

# ---------------- REEL 5: IVDR ----------------
def r5_doc():
    stars = ''.join(f'<circle cx="{460+170*math.sin(i*math.pi/6):.1f}" cy="{330-170*math.cos(i*math.pi/6):.1f}" r="13" fill="#F2B01E"/>' for i in range(12))
    doc = (f'<rect x="250" y="60" width="420" height="560" rx="40" fill="#fff" stroke="{NAVY}" stroke-width="8"/><g class="ring">{stars}</g>'
           + T(460, 360, "IVDR", 96) + T(460, 430, "2017/746", 40, MAG, font='PM', ls=3)
           + ''.join(f'<rect x="{320}" y="{480+i*38}" width="{[280,220][i]}" height="16" rx="8" fill="{LIGHT}"/>' for i in range(2)))
    stamp = f'<g class="st"><circle r="76" fill="{MAG}"/>{T(0,24,"CE",70,"#fff")}</g>'
    js = """Q('.ring').setAttribute('transform','rotate('+(lt*20)+' 460 330)');PO(Q('.st'),seg(lt,1.2,1.7),650,560);Q('.st').setAttribute('transform',Q('.st').getAttribute('transform').replace('translate(650 560)','translate(650 560)'));"""
    # st positioned via PO at 650,560 -> wrap with initial translate
    stamp = f'<g class="stw" transform="translate(650 560)"><g class="st">{stamp[stamp.index(">")+1:-4]}</g></g>'
    js = """Q('.ring').setAttribute('transform','rotate('+(lt*20)+' 460 330)');const k=seg(lt,1.2,1.7);Q('.st').setAttribute('transform','scale('+(k>0?back(k):0)+')');"""
    return svg(920, 700, doc + stamp), js

def r5_timeline():
    mk = [(150, "2027", "D"), (460, "2028", "C"), (770, "2029", "B · A")]
    ln = f'<line class="ln" x1="80" y1="360" x2="840" y2="360" stroke="{NAVY}" stroke-width="12" stroke-linecap="round" pathLength="100" stroke-dasharray="100" stroke-dashoffset="100"/>'
    g = ''.join(f'<g class="m{i}"><circle cx="{x}" cy="360" r="46" fill="{MAG if i==0 else NAVY}"/>{T(x,376,c,40 if len(c)<3 else 28,"#fff")}{T(x,470,y,60)}{T(x,520,"31/12",26,MAG,font="PM",ls=3)}'
                f'<rect x="{x-40}" y="{150-i*0}" width="80" height="{0}" fill="{MAG}"/></g>' for i, (x, y, c) in enumerate(mk))
    bars = ''.join(f'<rect class="br{i}" x="{x-40}" y="320" width="80" height="0" rx="14" fill="{LIGHT}"/>' for i, (x, _, _) in enumerate(mk))
    js = """Q('.ln').setAttribute('stroke-dashoffset',100*(1-ease(seg(lt,.1,1.0))));
const H=[210,150,100];for(let i=0;i<3;i++){const k=seg(lt,.9+i*.5,1.4+i*.5);PO(Q('.m'+i),k,[150,460,770][i],360);const b=Q('.br'+i);const h=H[i]*ease(seg(lt,1.2+i*.5,1.9+i*.5));b.setAttribute('y',300-h);b.setAttribute('height',h);}"""
    return svg(920, 640, bars + ln + g), js

def r5_checks():
    rows = ["Sistema qualità", "Organismo notificato", "Accordo scritto"]
    g = ''.join(f'<g><rect x="30" y="{40+i*200}" width="860" height="160" rx="44" fill="{SOFT}"/>{T(130,{0:140,1:340,2:540}[i]+0,rows[i],46,NAVY,"start")}'
                f'<circle cx="{790}" cy="{120+i*200}" r="50" fill="#fff" stroke="{LIGHT}" stroke-width="6"/><g class="k{i}" transform="translate(790 {120+i*200}) scale(0)"><circle r="50" fill="{MAG}"/><path d="M-20 2 L-6 18 L22 -16" fill="none" stroke="#fff" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/></g></g>' for i in range(3))
    js = """for(let i=0;i<3;i++){const k=seg(lt,.5+i*.7,.9+i*.7);Q('.k'+i).setAttribute('transform','translate(790 '+(120+i*200)+') scale('+(k>0?back(k):0)+')');}"""
    return svg(920, 640, g), js

def r5_ce():
    doc = ''.join(f'<rect x="{240+i*18}" y="{100+i*18}" width="360" height="460" rx="34" fill="#fff" stroke="{NAVY}" stroke-width="8"/>' for i in (2, 1, 0))
    ln = ''.join(f'<rect x="290" y="{300+i*56}" width="{[240,190,240][i]}" height="18" rx="9" fill="{LIGHT}"/>' for i in range(3))
    ce = f'<g class="ce"><circle cx="420" cy="220" r="86" fill="{NAVY}"/>{T(420,252,"CE",86,"#fff")}</g>'
    lens = f'<g class="lens"><line x1="64" y1="64" x2="150" y2="150" stroke="{MAG}" stroke-width="22" stroke-linecap="round"/><circle r="100" fill="rgba(255,46,91,.1)" stroke="{MAG}" stroke-width="14"/></g>'
    js = """PO(Q('.ce'),seg(lt,.3,.8),420,220);const u=ease(seg(lt,.9,2.2));Q('.lens').setAttribute('transform','translate('+(300+u*260)+' '+(250+Math.sin(u*6)*50+u*120)+')');"""
    return svg(920, 700, doc + ln + ce + lens), js

# ---------------- REEL 6: ELISA / CLIA ----------------
def plate(color_cls, dark=False):
    wells = ''
    for r in range(3):
        for c in range(6):
            wells += f'<circle class="{color_cls}" data-i="{r*6+c}" cx="{140+c*128}" cy="{285+r*125}" r="46" fill="#fff" stroke="{NAVY if not dark else LIGHT}" stroke-width="6"/>'
    return f'<rect x="50" y="200" width="820" height="420" rx="46" fill="{SOFT if not dark else "#14224D"}" stroke="{NAVY if not dark else LIGHT}" stroke-width="8"/>' + wells

def r6_elisa():
    beam = f'<polygon class="bm" points="396,150 524,150 504,640 416,640" fill="#F2C14E" opacity="0"/>'
    lamp = f'<rect x="400" y="60" width="120" height="90" rx="26" fill="{NAVY}"/><circle cx="460" cy="150" r="22" fill="#F2C14E"/>'
    sens = f'<rect x="380" y="640" width="160" height="40" rx="18" fill="{NAVY}"/>'
    js = """QA('.we').forEach(w=>{const i=+w.dataset.i;const k=ease(seg(lt,.3+i*.06,1.6+i*.06));const r=255,g=Math.round(255-60*k),b=Math.round(255-190*k);w.setAttribute('fill','rgb('+r+','+g+','+b+')');});
Q('.bm').setAttribute('opacity',seg(lt,1.8,2.2)*(0.5+0.2*Math.sin(lt*8)));"""
    return svg(920, 720, plate('we') + beam + lamp + sens), js

def r6_clia():
    rays = ''.join(f'<line class="ry" x1="0" y1="-62" x2="0" y2="-92" stroke="#fff" stroke-width="7" stroke-linecap="round" transform="rotate({a})"/>' for a in range(0, 360, 45))
    gl = ''.join(f'<g class="gl" data-i="{r*6+c}" transform="translate({140+c*128} {285+r*125})" opacity="0"><circle r="70" fill="url(#gg)"/>{rays}</g>' for r in range(3) for c in range(6))
    defs = '<defs><radialGradient id="gg"><stop offset="0" stop-color="#fff" stop-opacity=".95"/><stop offset=".45" stop-color="#FF8FA9" stop-opacity=".55"/><stop offset="1" stop-color="#FF2E5B" stop-opacity="0"/></radialGradient></defs>'
    det = f'<rect x="340" y="40" width="240" height="90" rx="28" fill="{LIGHT}"/>' + T(460, 98, "SEGNALE", 30, NAVY, font='PM', ls=4)
    js = """QA('.gl').forEach(g=>{const i=+g.dataset.i;const k=ease(seg(lt,.3+i*.06,1.0+i*.06));g.setAttribute('opacity',k*(0.82+0.18*Math.sin(lt*9+i)));});"""
    return svg(920, 720, plate('wc', True) + defs + gl + det), js

def r6_vs():
    L = f'<g class="L"><rect x="20" y="60" width="410" height="520" rx="56" fill="#fff"/><circle cx="225" cy="270" r="104" fill="#F2C14E"/><circle cx="225" cy="270" r="104" fill="none" stroke="{NAVY}" stroke-width="10"/>' + T(225, 480, "Colore", 56) + T(225, 534, "ELISA", 28, MAG, font='PM', ls=5) + '</g>'
    R = f'<g class="R"><rect x="490" y="60" width="410" height="520" rx="56" fill="#14224D" stroke="{LIGHT}" stroke-width="6"/><circle cx="695" cy="270" r="140" fill="url(#gg2)"/><circle cx="695" cy="270" r="54" fill="#fff"/>' + T(695, 480, "Luce", 56, "#fff") + T(695, 534, "CLIA", 28, "#FF6E8E", font='PM', ls=5) + '</g>'
    defs = '<defs><radialGradient id="gg2"><stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset=".5" stop-color="#FF8FA9" stop-opacity=".5"/><stop offset="1" stop-color="#FF2E5B" stop-opacity="0"/></radialGradient></defs>'
    vs = f'<g class="vs"><circle cx="460" cy="320" r="62" fill="{MAG}"/>{T(460,344,"VS",60,"#fff")}</g>'
    js = """const a=ease(seg(lt,.2,.9)),b=ease(seg(lt,.4,1.1));Q('.L').setAttribute('transform','translate('+(-(1-a)*600)+' 0)');Q('.R').setAttribute('transform','translate('+((1-b)*600)+' 0)');PO(Q('.vs'),seg(lt,1.0,1.5),460,320);"""
    return svg(920, 640, defs + L + R + vs), js

# ---------------- REEL 7: HIL ----------------
def r7_hook3():
    cols = ['#E05A6F', '#F7F3EA', '#F0A81C']
    t = ''.join(tube(150 + i * 270, 130, 120, 400, [MAG, '#7AA2F7', CAPS[2]][i], cols[i], .75, f't{i}', NAVY, 'rgba(255,255,255,.7)') for i in range(3))
    q = ''.join(f'<g class="q{i}"><circle cx="{210+i*270}" cy="60" r="50" fill="{NAVY}"/>{T(210+i*270,88,"?",70,"#fff")}</g>' for i in range(3))
    js = """for(let i=0;i<3;i++){const r=ease(seg(lt,i*.25,.7+i*.25));Q('.t'+i).setAttribute('transform','translate(0 '+((1-r)*500)+')');PO(Q('.q'+i),seg(lt,1.0+i*.3,1.4+i*.3),210+i*270,60);}"""
    return svg(920, 640, t + q), js

def r7_emolisi():
    inner = '<rect class="liq" x="380" y="200" width="160" height="440" fill="#F2D58A"/><rect class="red" x="380" y="200" width="160" height="440" fill="#E05A6F" opacity="0"/>'
    tb = tube(380, 120, 160, 520, MAG, inner=inner, cls='tb')
    cells = ''.join(f'<circle class="ce" data-x="{x}" data-y="{y}" cx="{460+x}" cy="{y}" r="26" fill="#C41E3A" stroke="#7A0F25" stroke-width="4"/>' for x, y in [(-50, 300), (30, 350), (-10, 410), (50, 470), (-40, 520), (10, 560), (-55, 450)])
    tags = ''.join(f'<g class="tg{i}" transform="translate({x} {y}) scale(0)"><rect x="-80" y="-34" width="160" height="68" rx="34" fill="{MAG}"/>{T(0,14,n,36,"#fff")}</g>' for i, (n, x, y) in enumerate([("K⁺", 190, 260), ("LDH", 730, 380), ("AST", 190, 520)]))
    js = """const b=ease(seg(lt,.8,1.8));QA('.ce').forEach((c,i)=>{const x=+c.dataset.x,y=+c.dataset.y;c.setAttribute('r',26*(1-b*.7));c.setAttribute('cx',460+x*(1+b*1.1)+Math.sin(lt*5+i)*6*b);c.setAttribute('cy',y+Math.cos(lt*4+i)*6*b);c.setAttribute('opacity',1-b*.45)});
Q('.red').setAttribute('opacity',b*.85);[[190,260],[730,380],[190,520]].forEach((p,i)=>{const k=seg(lt,1.4+i*.35,1.8+i*.35);Q('.tg'+i).setAttribute('transform','translate('+p[0]+' '+p[1]+') scale('+(k>0?back(k):0)+')')});"""
    return svg(920, 720, tb + cells + tags), js

def r7_lipemia():
    inner = '<rect class="liq" x="380" y="200" width="160" height="440" fill="#F2D58A"/><rect class="mk" x="380" y="200" width="160" height="440" fill="#F7F3EA" opacity="0"/>'
    tb = tube(380, 120, 160, 520, '#7AA2F7', inner=inner, cls='tb')
    dr = ''.join(f'<circle class="dr" data-i="{i}" cx="{400+ (i*37)%120}" cy="{230+(i*61)%380}" r="{6+i%4*3}" fill="#fff" opacity="0"/>' for i in range(24))
    beam = f'<rect x="40" y="378" width="340" height="24" rx="12" fill="#FFD36B"/><rect class="b2" x="540" y="378" width="0" height="24" rx="12" fill="#FFD36B"/>'
    sc = ''.join(f'<circle class="sc" cx="460" cy="390" r="6" fill="#FFD36B" opacity="0"/>' for i in range(5))
    js = """const m=ease(seg(lt,.6,2.0));Q('.mk').setAttribute('opacity',m*.92);QA('.dr').forEach(d=>{const i=+d.dataset.i;d.setAttribute('opacity',Math.min(1,Math.max(0,(m*24-i)/3))*.9)});
Q('.b2').setAttribute('width',340*(1-m)*(1-m));QA('.sc').forEach((s,i)=>{const u=((lt*1.2+i*.2)%1);s.setAttribute('opacity',m>.2?(1-u)*.9:0);s.setAttribute('cx',460+Math.cos(i*1.9)*u*220*m);s.setAttribute('cy',390+Math.sin(i*1.9)*u*220*m)});"""
    return svg(920, 720, beam + tb + dr + sc), js

def r7_ittero():
    inner = '<rect class="liq" x="380" y="200" width="160" height="440" fill="#F2D58A"/><rect class="am" x="380" y="200" width="160" height="440" fill="#F0A81C" opacity="0"/>'
    tb = tube(380, 120, 160, 520, CAPS[2], inner=inner, cls='tb')
    rays = ''.join(f'<line class="rr" x1="0" y1="-300" x2="0" y2="-360" stroke="#F0A81C" stroke-width="12" stroke-linecap="round" transform="rotate({a})"/>' for a in range(0, 360, 30))
    sun = f'<g class="sun" transform="translate(460 380)" opacity="0">{rays}</g>'
    lab = f'<g class="lb"><rect x="270" y="660" width="380" height="54" rx="27" fill="{NAVY}"/>{T(460,697,"BILIRUBINA",26,"#fff",font="PM",ls=5)}</g>'
    js = """const a=ease(seg(lt,.5,1.8));Q('.am').setAttribute('opacity',a*.95);const s=Q('.sun');s.setAttribute('opacity',a*(.5+.3*Math.sin(lt*5)));s.setAttribute('transform','translate(460 380) rotate('+(lt*25)+')');PO(Q('.lb'),seg(lt,1.6,2.1),460,687);"""
    return svg(920, 740, sun + tb + lab), js

# ---------------- REEL 8: rapido vs laboratorio ----------------
def r8_rapido():
    cas = (f'<rect x="90" y="260" width="520" height="260" rx="50" fill="{SOFT}" stroke="{NAVY}" stroke-width="8"/><circle cx="170" cy="390" r="32" fill="{NAVY}"/><rect x="250" y="330" width="320" height="120" rx="24" fill="#fff" stroke="{NAVY}" stroke-width="5"/>'
           f'<rect class="cl" x="500" y="350" width="14" height="80" rx="7" fill="{NAVY}" opacity="0"/><rect class="tl" x="410" y="350" width="14" height="80" rx="7" fill="{MAG}" opacity="0"/>')
    ticks = ''.join(f'<line x1="0" y1="-92" x2="0" y2="-76" stroke="{NAVY}" stroke-width="6" stroke-linecap="round" transform="rotate({i*30})"/>' for i in range(12))
    clk = f'<g transform="translate(740 360)"><circle r="110" fill="#fff" stroke="{NAVY}" stroke-width="12"/>{ticks}<line class="h" x1="0" y1="0" x2="0" y2="-80" stroke="{MAG}" stroke-width="10" stroke-linecap="round"/><circle r="12" fill="{MAG}"/></g>'
    js = """Q('.h').setAttribute('transform','rotate('+(lt*320)+')');Q('.cl').setAttribute('opacity',seg(lt,1.2,1.4));const t=seg(lt,1.6,2.0);Q('.tl').setAttribute('opacity',t);"""
    return svg(920, 640, cas + clk), js

def r8_lab():
    inst = (f'<rect x="60" y="330" width="560" height="260" rx="40" fill="{NAVY}"/><rect x="100" y="380" width="200" height="40" rx="20" fill="#050B1F"/>'
            + ''.join(f'<circle class="led{i}" cx="{140+i*44}" cy="520" r="13" fill="#2A3A6E"/>' for i in range(3)))
    bars = ''.join(f'<rect class="bar" data-h="{h}" x="{680+i*58}" y="590" width="40" height="0" rx="10" fill="{MAG if i==3 else NAVY}"/>' for i, h in enumerate([120, 200, 160, 280]))
    sh = f'<g class="sh" transform="translate(340 190) scale(0)"><path d="M0 -110 L90 -76 V10 Q90 82 0 118 Q-90 82 -90 10 V-76Z" fill="{MAG}"/><path d="{CHECK}" transform="translate(0 6)" fill="none" stroke="#fff" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/></g>'
    js = """QA('.bar').forEach((b,i)=>{const h=+b.dataset.h*ease(seg(lt,.3+i*.2,.9+i*.2));b.setAttribute('y',590-h);b.setAttribute('height',h)});
for(let i=0;i<3;i++)Q('.led'+i).setAttribute('fill',lt>.5+i*.3?'#FF2E5B':'#2A3A6E');const k=seg(lt,1.4,1.9);Q('.sh').setAttribute('transform','translate(340 190) scale('+(k>0?back(k):0)+')');"""
    return svg(920, 640, inst + bars + sh), js

def r8_attenzione():
    cas = (f'<g class="cs"><rect x="40" y="300" width="440" height="220" rx="44" fill="{SOFT}" stroke="{NAVY}" stroke-width="8"/><circle cx="105" cy="410" r="26" fill="{NAVY}"/><rect x="170" y="355" width="270" height="110" rx="22" fill="#fff" stroke="{NAVY}" stroke-width="5"/>'
           f'<rect x="372" y="372" width="12" height="76" rx="6" fill="{NAVY}"/></g>')
    q = f'<g class="qm"><circle cx="260" cy="190" r="62" fill="{MAG}"/>{T(260,222,"?",84,"#fff")}</g>'
    ar = f'<path class="ar" d="M500 410 H640" stroke="{MAG}" stroke-width="12" stroke-linecap="round" fill="none" pathLength="100" stroke-dasharray="100" stroke-dashoffset="100"/><path class="ah" d="M610 380 L650 410 L610 440" stroke="{MAG}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" fill="none" opacity="0"/>'
    tb = tube(720, 270, 80, 280, MAG, '#F2D58A', .6, 'tbx')
    ck = badge('bd', 54)
    js = """PO(Q('.qm'),seg(lt,.3,.8),260,190);Q('.qm').setAttribute('transform',Q('.qm').getAttribute('transform')+' translate(0 '+(Math.sin(lt*5)*6)+')');
Q('.ar').setAttribute('stroke-dashoffset',100*(1-ease(seg(lt,1.1,1.7))));Q('.ah').setAttribute('opacity',seg(lt,1.6,1.8));const k=seg(lt,2.0,2.5);Q('.bd').setAttribute('transform','translate(780 250) scale('+(k>0?back(k):0)+')');"""
    return svg(920, 640, cas + q + ar + tb + ck.replace('class="bd"', 'class="bd" transform="translate(780 250) scale(0)"')), js

def r8_scale():
    beam = (f'<g class="bm"><rect x="120" y="205" width="680" height="22" rx="11" fill="{NAVY}"/>'
            f'<line x1="170" y1="216" x2="170" y2="330" stroke="{NAVY}" stroke-width="6"/><line x1="750" y1="216" x2="750" y2="330" stroke="{NAVY}" stroke-width="6"/>'
            f'<path d="M80 330 H260 A90 90 0 0 1 80 330Z" fill="{MAG}"/><path d="M660 330 H840 A90 90 0 0 1 660 330Z" fill="{NAVY}"/>'
            f'<g transform="translate(115 245) scale(.55)"><rect width="260" height="82" rx="20" fill="#fff"/><rect x="170" y="14" width="10" height="54" rx="5" fill="{NAVY}"/><rect x="195" y="14" width="10" height="54" rx="5" fill="{MAG}"/></g>'
            f'<g transform="translate(735 250) scale(.42)">{tube(0,0,70,150,MAG,"#F2D58A",.6,"",NAVY,"#fff")}</g></g>')
    fu = f'<path d="M460 216 L380 560 H540Z" fill="{NAVY}"/><rect x="330" y="560" width="260" height="30" rx="15" fill="{NAVY}"/>'
    js = """const a=14*(1-ease(seg(lt,.3,1.8)))*Math.cos(lt*5)*Math.exp(-lt*.6)+(lt<.3?14:0);Q('.bm').setAttribute('transform','rotate('+(lt<1.5?14*(1-ease(seg(lt,.2,1.5)))+Math.sin(lt*7)*3*seg(lt,1.2,1.5)*(1-seg(lt,1.5,2.5)):0)+' 460 216)');"""
    return svg(920, 640, fu + beam), js

# ---------------- REEL 9: manutenzione ----------------
def r9_gear():
    g = gear(330, 330, 150, 10, NAVY, 'g1') + gear(640, 460, 100, 8, MAG, 'g2')
    js = """const a=lt*60;Q('.g1').setAttribute('transform','translate(330 330) rotate('+a+')');Q('.g2').setAttribute('transform','translate(640 460) rotate('+(-a*1.5+11)+')');"""
    return svg(920, 700, g), js

def r9_clean():
    bench = f'<rect x="60" y="440" width="800" height="150" rx="34" fill="{NAVY}"/><rect x="60" y="410" width="800" height="50" rx="22" fill="{LIGHT}"/>'
    cloth = f'<g class="cl"><rect x="-110" y="-60" width="220" height="130" rx="40" fill="{MAG}"/><rect x="-90" y="-40" width="180" height="16" rx="8" fill="#fff" opacity=".4"/></g>'
    sp = ''.join(f'<g class="sp{i}"><path d="M0 -40 L9 -9 L40 0 L9 9 L0 40 L-9 9 L-40 0 L-9 -9Z" fill="#F2B01E"/></g>' for i in range(4))
    js = """const x=460+Math.sin(lt*3.2)*250*(lt<2.2?1:Math.max(0,1-(lt-2.2)*3));Q('.cl').setAttribute('transform','translate('+x+' 360)');
const P=[[200,330],[460,250],[720,330],[580,150]];for(let i=0;i<4;i++){const k=seg(lt,1.4+i*.3,1.9+i*.3);Q('.sp'+i).setAttribute('transform','translate('+P[i][0]+' '+P[i][1]+') scale('+(k>0?back(k)*(0.8+0.2*Math.sin(lt*8+i)):0)+') rotate('+(lt*40)+')')}"""
    return svg(920, 700, bench + cloth + sp), js

def r9_qc():
    band = f'<rect x="60" y="200" width="800" height="300" rx="30" fill="{SOFT}"/><line x1="60" y1="350" x2="860" y2="350" stroke="{NAVY}" stroke-width="6" stroke-dasharray="14 12"/>'
    for y in (200, 500): band += f'<line x1="60" y1="{y}" x2="860" y2="{y}" stroke="{MAG}" stroke-width="6"/>'
    pts = [(110, 380), (230, 310), (350, 400), (470, 330), (590, 290), (710, 380), (820, 340)]
    poly = f'<polyline class="pl" points="{" ".join(f"{x},{y}" for x,y in pts)}" fill="none" stroke="{NAVY}" stroke-width="9" stroke-linejoin="round" stroke-linecap="round" pathLength="100" stroke-dasharray="100" stroke-dashoffset="100"/>'
    dots = ''.join(f'<circle class="pt{i}" cx="{x}" cy="{y}" r="0" fill="{MAG}"/>' for i, (x, y) in enumerate(pts))
    js = """Q('.pl').setAttribute('stroke-dashoffset',100*(1-ease(seg(lt,.3,2.0))));for(let i=0;i<7;i++){Q('.pt'+i).setAttribute('r',16*ease(seg(lt,.3+i*.25,.6+i*.25)))}"""
    return svg(920, 700, band + poly + dots + badge('bd', 60).replace('class="bd"', 'class="bd" transform="translate(790 590) scale(0)"')), js + "\nconst k=seg(lt,2.2,2.7);Q('.bd').setAttribute('transform','translate(790 590) scale('+(k>0?back(k):0)+')');"

def r9_log():
    bk = f'<rect x="170" y="60" width="580" height="560" rx="44" fill="#fff" stroke="{NAVY}" stroke-width="10"/><rect x="170" y="60" width="90" height="560" rx="40" fill="{NAVY}"/>'
    ln = ''.join(f'<rect class="ln" data-w="{w}" x="310" y="{150+i*80}" width="0" height="20" rx="10" fill="{LIGHT}"/><circle class="tk{i}" cx="690" cy="{160+i*80}" r="0" fill="{MAG}"/>' for i, w in enumerate([330, 280, 330, 240, 300]))
    pen = f'<g class="pen"><rect x="0" y="-18" width="150" height="36" rx="12" fill="{MAG}" transform="rotate(-35)"/><polygon points="-6,6 -26,20 -18,-2" fill="{NAVY}"/></g>'
    js = """const n=5;let cur=0;QA('.ln').forEach((l,i)=>{const k=ease(seg(lt,.3+i*.45,.7+i*.45));l.setAttribute('width',+l.dataset.w*k);if(k>0&&k<1)cur=i;Q('.tk'+i).setAttribute('r',16*ease(seg(lt,.7+i*.45,.95+i*.45)))});
const i=Math.min(4,Math.max(0,Math.floor((lt-.3)/.45)));const k=ease(seg(lt,.3+i*.45,.7+i*.45));const w=[330,280,330,240,300][i];Q('.pen').setAttribute('transform','translate('+(310+w*k+10)+' '+(165+i*80)+')');Q('.pen').setAttribute('opacity',lt<2.7?1:0);"""
    return svg(920, 680, bk + ln + pen), js

def r9_stock():
    sh = f'<rect x="60" y="500" width="800" height="26" rx="13" fill="{NAVY}"/>'
    bx = ''.join(f'<g class="bx{i}"><rect x="{90+i*170}" y="{380-i%2*0}" width="140" height="120" rx="14" fill="{["#C9A56B","#D6B67C","#C9A56B"][i%3]}" stroke="{NAVY}" stroke-width="6"/><rect x="{90+i*170}" y="{380}" width="140" height="30" fill="rgba(12,22,51,.15)"/></g>' for i in range(4))
    cal = (f'<g class="cal"><rect x="590" y="90" width="270" height="250" rx="34" fill="#fff" stroke="{NAVY}" stroke-width="8"/><rect x="590" y="90" width="270" height="70" rx="30" fill="{MAG}"/>'
           + ''.join(f'<circle cx="{625+c*50}" cy="{205+r*50}" r="8" fill="{LIGHT}"/>' for r in range(3) for c in range(5)) + f'<circle class="mk" cx="725" cy="255" r="0" fill="none" stroke="{MAG}" stroke-width="8"/></g>')
    js = """for(let i=0;i<4;i++){const k=ease(seg(lt,.2+i*.25,.8+i*.25));Q('.bx'+i).setAttribute('transform','translate(0 '+(-(1-k)*500)+')')}PO(Q('.cal'),seg(lt,1.2,1.7),725,215);Q('.mk').setAttribute('r',32*ease(seg(lt,1.8,2.2)));"""
    return svg(920, 640, sh + bx + cal), js

def r9_bookmark():
    bm = f'<g class="bm"><path d="M-110 -170 H110 V190 L0 100 L-110 190Z" fill="{NAVY}" stroke="#fff" stroke-width="10" stroke-linejoin="round"/></g>'
    st = ''.join(f'<g class="s{i}"><path d="M0 -34 L8 -8 L34 0 L8 8 L0 34 L-8 8 L-34 0 L-8 -8Z" fill="#fff"/></g>' for i in range(3))
    js = """const d=ease(seg(lt,.2,.9));Q('.bm').setAttribute('transform','translate(460 '+(260-(1-d)*420)+') rotate('+((1-d)*-20+Math.sin(lt*6)*3*seg(lt,1,1.5))+')');
const P=[[280,200],[650,150],[690,350]];for(let i=0;i<3;i++){const k=seg(lt,.9+i*.25,1.3+i*.25);Q('.s'+i).setAttribute('transform','translate('+P[i][0]+' '+P[i][1]+') scale('+(k>0?back(k):0)+') rotate('+(lt*50)+')')}"""
    return svg(920, 520, bm + st), js

# ---------------- REEL 10: automatizzare ----------------
def r10_gears():
    g = gear(340, 330, 170, 12, '#fff', 'g1', hole=NAVY) + gear(700, 470, 110, 8, MAG, 'g2', hole=NAVY)
    ar = f'<path class="ar" d="M120 600 A300 300 0 0 0 330 640" fill="none" stroke="{NAVY}" stroke-width="0"/>'
    js = """const a=lt*55;Q('.g1').setAttribute('transform','translate(340 330) rotate('+a+')');Q('.g2').setAttribute('transform','translate(700 470) rotate('+(-a*1.55+13)+')');"""
    return svg(920, 700, g), js

def r10_options():
    pos = [(10, 20), (470, 20), (10, 380), (470, 380)]; lab = ["Preanalitica", "Parassitologia", "Refertazione", "Magazzino"]
    ico = [''.join(f'<g transform="translate({-100+i*54} -75) scale(.45)">{tube(0,0,80,300,CAPS[i],"#F2D58A",.6,"",NAVY,"#fff")}</g>' for i in range(4)),
           f'<circle r="70" fill="{NAVY}"/><circle cx="-20" cy="-18" r="14" fill="#FF8FA9"/><circle cx="26" cy="8" r="18" fill="#C9D0EC"/><circle cx="-6" cy="34" r="10" fill="#fff"/><circle r="70" fill="none" stroke="{MAG}" stroke-width="10"/>',
           f'<rect x="-52" y="-72" width="104" height="140" rx="16" fill="#fff" stroke="{NAVY}" stroke-width="8"/>' + ''.join(f'<rect x="-34" y="{-44+j*26}" width="{[68,52,68][j]}" height="10" rx="5" fill="{LIGHT}"/>' for j in range(3)) + f'<circle cx="38" cy="50" r="24" fill="{MAG}"/>',
           ''.join(f'<rect x="{-86+i*60}" y="{-10-j*50+ (0 if i<2 else 0)}" width="56" height="46" rx="8" fill="#C9A56B" stroke="{NAVY}" stroke-width="5"/>' for i in range(3) for j in range(2 if i<2 else 1))]
    cards = ''.join(f'<g class="c{i}"><rect x="{x}" y="{y}" width="440" height="330" rx="52" fill="#fff"/><g transform="translate({x+220} {y+125})">{ico[i]}</g>' + T(x + 220, y + 270, lab[i], 46) + f'<rect class="hl{i}" x="{x}" y="{y}" width="440" height="330" rx="52" fill="none" stroke="{MAG}" stroke-width="12" opacity="0"/></g>' for i, (x, y) in enumerate(pos))
    js = """for(let i=0;i<4;i++){PO(Q('.c'+i),seg(lt,.25+i*.4,.65+i*.4),[230,690,230,690][i],[185,185,545,545][i]);}
const w=Math.floor(Math.max(0,lt-2.2)/.5)%4;for(let i=0;i<4;i++)Q('.hl'+i).setAttribute('opacity',lt>2.2&&w==i?1:0);"""
    return svg(920, 700, cards), js
