import math, re

def _bez(p0,p1,p2,p3,t):
    u=1-t; return (u*u*u*p0[0]+3*u*u*t*p1[0]+3*u*t*t*p2[0]+t*t*t*p3[0], u*u*u*p0[1]+3*u*u*t*p1[1]+3*u*t*t*p2[1]+t*t*t*p3[1])
def band(p0,p1,p2,p3,w0,w1,n=48):
    L=[];R=[]
    for i in range(n+1):
        t=i/n; x,y=_bez(p0,p1,p2,p3,t); x2,y2=_bez(p0,p1,p2,p3,min(1,t+1e-3))
        tx,ty=x2-x,y2-y; m=math.hypot(tx,ty) or 1; nx,ny=-ty/m,tx/m
        w=(w0*(1-t)+w1*t)/2
        L.append((x+nx*w,y+ny*w)); R.append((x-nx*w,y-ny*w))
    pts=L+R[::-1]
    return "M"+" L".join(f"{x:.2f} {y:.2f}" for x,y in pts)+" Z"
def mirror(d):
    toks=re.findall(r'[MCLHVZ]|-?\d+\.?\d*', d); out=[]; i=0; cmd=None
    while i<len(toks):
        t=toks[i]
        if t in "MCLHVZ": cmd=t; out.append(t); i+=1; continue
        if cmd=='H': out.append(f"{100-float(t):g}"); i+=1
        elif cmd=='V': out.append(t); i+=1
        else: out.append(f"{100-float(t):g}"); out.append(toks[i+1]); i+=2
    return " ".join(out)

# ---- silhouette: axial brain, 100 x 120 ----
LEFT = "M50 8 C46 3 36 3 28 9 C16 18 8 36 8 60 C8 84 16 102 28 111 C36 117 46 117 50 112"
OUTLINE = LEFT + " " + mirror("M50 112 C54 117 64 117 72 111 C84 102 92 84 92 60 C92 36 84 18 72 9 C64 3 54 3 50 8").replace("M","L",1) + " Z"
# (mirror of the right side written explicitly to keep direction continuous)
OUTLINE = ("M50 9 C46 4 35 4 27 10 C14 19 6 37 6 60 C6 83 14 101 27 109 C35 115 46 115 50 110 "
           "C54 115 65 115 73 109 C86 101 94 83 94 60 C94 37 86 19 73 10 C65 4 54 4 50 9 Z")

# ---- ventricles ----
LAT_L  = band((42,32),(36,43),(39,57),(46,65), 7.6, 2.6)
STEM   = "M48.4 70 L51.6 70 L51.1 84 L48.9 84 Z"
WING_L = band((50,86),(45,84),(40,88),(34,97), 4.4, 1.4)

# ---- circuitry, left hemisphere (mirrored to the right) ----
TR = [  # (path, pad point, pad style)
    ("M13 40 L19 34 H29 L33 30 V23", (33,23), "dot"),
    ("M12 56 H21 L25 60 H31", (31,60), "ring"),
    ("M14 73 L20 79 H27 V88", (27,88), "dot"),
    ("M25 100 L30 95 H36 L40 99", (40,99), "ring"),
    ("M31 13 L35 17 H43", (43,17), "dot"),
    ("M18 46 V51", (18,51), "dot"),
    ("M23 66 L29 72 V79", (29,79), "ring"),
    ("M36 44 L32 48 V53", (32,53), "dot"),
    ("M41 106 H47", (47,106), "dot"),
    ("M21 85 V91 L18 94", (18,94), "ring"),
    ("M26 24 V18 L30 14", None, None),
    ("M38 76 L42 80", (42,80), "dot"),
]
CHIPS = [(19,22,8,7),(13,62,6,8)]   # x,y,w,h small components

def circuitry(col, tw=1.5, pad_fill=None):
    pf = pad_fill or col
    out=[f'<g fill="none" stroke="{col}" stroke-width="{tw}" stroke-linecap="round" stroke-linejoin="round">']
    for d,_,_ in TR: out.append(f'<path d="{d}"/><path d="{mirror(d)}"/>')
    for x,y,w,h in CHIPS:
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="1.2"/><rect x="{100-x-w}" y="{y}" width="{w}" height="{h}" rx="1.2"/>')
        for k in range(2):
            yy=y+h*(k+1)/3
            out.append(f'<path d="M{x-2.5} {yy:.1f} H{x}"/><path d="M{100-x} {yy:.1f} H{100-x+2.5}"/>')
    out.append('</g>')
    for _,p,kind in TR:
        if not p: continue
        for (px,py) in (p,(100-p[0],p[1])):
            if kind=="dot": out.append(f'<circle cx="{px}" cy="{py}" r="2.0" fill="{col}"/>')
            else: out.append(f'<circle cx="{px}" cy="{py}" r="1.9" fill="{pf}" stroke="{col}" stroke-width="{tw}"/>')
    return ''.join(out)

def mark(gid, fill_in="#7f9ddb", fill_out="#5c7cc3", trace="#1a2f6a", rim="#e2b23b", rim_glow="#f5d57a", vent="#ffffff", midline="#9fb5e6", rimw=4.2, tw=1.5, flat=False):
    defs=(f'<radialGradient id="{gid}f" cx="50%" cy="42%" r="62%"><stop offset="0" stop-color="{fill_in}"/><stop offset="1" stop-color="{fill_out}"/></radialGradient>'
          f'<linearGradient id="{gid}r" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{rim_glow}"/><stop offset="1" stop-color="{rim}"/></linearGradient>')
    fill = fill_out if flat else f'url(#{gid}f)'
    rimc = rim if flat else f'url(#{gid}r)'
    out=[f'<defs>{defs}</defs>']
    out.append(f'<path d="{OUTLINE}" fill="none" stroke="{rim_glow}" stroke-width="{rimw*2.4}" stroke-linejoin="round" opacity=".22"/>')
    out.append(f'<path d="{OUTLINE}" fill="{fill}" stroke="{rimc}" stroke-width="{rimw}" stroke-linejoin="round"/>')
    out.append(f'<path d="{OUTLINE}" fill="none" stroke="#ffffff" stroke-width="{rimw*0.28}" opacity=".85"/>')
    out.append(f'<path d="M50 14 V106" stroke="{midline}" stroke-width="1" opacity=".55"/>')
    out.append(circuitry(trace, tw, pad_fill=fill_out))
    out.append(f'<g fill="{vent}"><path d="{LAT_L}"/><path d="{mirror(LAT_L)}"/><path d="{STEM}"/><path d="{WING_L}"/><path d="{mirror(WING_L)}"/></g>')
    return ''.join(out)

def mark_mono(gid, col="#001f44"):
    """One colour: filled slice, everything else knocked out."""
    k='#000'
    knock=(circuitry(k, 1.6).replace(f'fill="{k}" stroke="{k}"',f'fill="#fff" stroke="{k}"')  # rings stay open
           + f'<g fill="{k}"><path d="{LAT_L}"/><path d="{mirror(LAT_L)}"/><path d="{STEM}"/><path d="{WING_L}"/><path d="{mirror(WING_L)}"/></g>'
           + f'<path d="M50 14 V106" stroke="{k}" stroke-width="1"/>'
           + f'<path d="{OUTLINE}" fill="none" stroke="{k}" stroke-width="2.2"/>')
    mask=f'<mask id="{gid}m" maskUnits="userSpaceOnUse" x="-20" y="-20" width="140" height="160"><rect x="-20" y="-20" width="140" height="160" fill="#000"/><path d="{OUTLINE}" fill="#fff" stroke="#fff" stroke-width="4.2"/>{knock}</mask>'
    return f'<defs>{mask}</defs><rect x="-20" y="-20" width="140" height="160" fill="{col}" mask="url(#{gid}m)"/>'

def wrap(inner, h=100, vb="2 0 96 120", bg=None):
    vw,vh=float(vb.split()[2]),float(vb.split()[3])
    b=f'<rect x="-60" y="-60" width="240" height="260" fill="{bg}"/>' if bg else ''
    return f'<svg viewBox="{vb}" width="{h*vw/vh:.0f}" height="{h}" xmlns="http://www.w3.org/2000/svg">{b}{inner}</svg>'
