# Redraw of the heritage CNEP mark: axial brain slice with ventricles and circuit traces.
OUT = ("M50 7 C44 1 29 2 21 13 C9 28 7 58 13 84 C18 104 32 117 50 113 C68 117 82 104 87 84 "
       "C93 58 91 28 79 13 C71 2 56 1 50 7 Z")
def mirror(d):
    import re
    def f(m):
        x=float(m.group(1)); return f"{100-x:g} {m.group(2)}"
    # replace "x y" number pairs; path uses only absolute coords
    toks=re.findall(r'[MCLHVZ]|-?\d+\.?\d*', d); out=[]; i=0; cmd=None
    while i<len(toks):
        t=toks[i]
        if t in "MCLHVZ": cmd=t; out.append(t); i+=1; continue
        if cmd=='H': out.append(f"{100-float(t):g}"); i+=1
        elif cmd=='V': out.append(t); i+=1
        else: out.append(f"{100-float(t):g}"); out.append(toks[i+1]); i+=2
    return " ".join(out)

# ventricles (white), left halves + mirrored

import math
def _bez(p0,p1,p2,p3,t):
    u=1-t; return (u*u*u*p0[0]+3*u*u*t*p1[0]+3*u*t*t*p2[0]+t*t*t*p3[0], u*u*u*p0[1]+3*u*u*t*p1[1]+3*u*t*t*p2[1]+t*t*t*p3[1])
def band(p0,p1,p2,p3,w0,w1,n=40,power=1.0):
    """Tapered band along a cubic centreline, width w0 at start -> w1 at end. Returns a closed path."""
    L=[];R=[]
    for i in range(n+1):
        t=i/n; x,y=_bez(p0,p1,p2,p3,t); x2,y2=_bez(p0,p1,p2,p3,min(1,t+1e-3))
        tx,ty=x2-x,y2-y; m=math.hypot(tx,ty) or 1; nx,ny=-ty/m,tx/m
        w=(w0*(1-t)+w1*t)**power/2 if power==1 else (w0+(w1-w0)*t**power)/2
        L.append((x+nx*w,y+ny*w)); R.append((x-nx*w,y-ny*w))
    pts=L+R[::-1]
    return "M"+" L".join(f"{x:.2f} {y:.2f}" for x,y in pts)+" Z"
# lateral ventricle, left: flared tip at top pointing outward, tapering down toward the midline
LAT_L = band((36,37),(30,47),(36,61),(46,68), 7.0, 2.6)
# fourth ventricle: two wings meeting at a peak, drawn as tapered bands
WING_L = band((50,90),(46,86),(40,88),(33,97), 4.6, 1.6)
BIRD = None

STEM  = "M48.3 72 L51.7 72 L51.2 91 L48.8 91 Z"

# circuit traces, left side (right side is mirrored with small changes)
TRACES_L = [
    ("M18 30 H27 L32 35 V44", (32,44), "ring"),
    ("M28 18 L33 23 H40", (40,23), "dot"),
    ("M14 52 H26", (26,52), "dot"),
    ("M17 64 L23 70 V80", (23,80), "ring"),
    ("M24 86 H30 L34 90 V98", (34,98), "dot"),
    ("M40 78 V84 L44 88", (44,88), "dot"),
    ("M30 60 H36", (36,60), "ring"),
    ("M22 40 V46", (22,46), "dot"),
]
TRACES_R = [
    ("M82 30 H73 L68 35 V44", (68,44), "ring"),
    ("M72 18 L67 23 H60", (60,23), "dot"),
    ("M86 54 H74 L70 58", (70,58), "dot"),
    ("M83 66 L77 72 V80", (77,80), "ring"),
    ("M76 88 H70 L66 92 V98", (66,98), "dot"),
    ("M60 78 V84 L56 88", (56,88), "dot"),
    ("M78 42 V48", (78,48), "ring"),
    ("M64 64 H70", (70,64), "dot"),
]

def mark(gid="ax", fill="#5f86c9", rim="#e9b949", rim2="#ffffff", trace="#001f44", vent="#ffffff", tw=1.9, rimw=4.6, one_colour=False, bg=None):
    out=[]
    if bg: out.append(f'<rect x="-50" y="-50" width="200" height="220" fill="{bg}"/>')
    if one_colour:
        # single colour: filled slice with knocked-out ventricles and traces via mask
        k = '#000'
        tr=''.join(f'<path d="{d}" fill="none" stroke="{k}" stroke-width="{tw}" stroke-linecap="round" stroke-linejoin="round"/>' for d,_,_ in TRACES_L+TRACES_R)
        pads=''.join((f'<circle cx="{p[0]}" cy="{p[1]}" r="2.4" fill="{k}"/>' if kind=="dot" else f'<circle cx="{p[0]}" cy="{p[1]}" r="2.2" fill="none" stroke="{k}" stroke-width="{tw}"/>') for _,p,kind in TRACES_L+TRACES_R)
        out.append(f'<defs><mask id="{gid}m" maskUnits="userSpaceOnUse" x="-50" y="-50" width="200" height="220"><rect x="-50" y="-50" width="200" height="220" fill="#000"/>'
                   f'<path d="{OUT}" fill="#fff"/><path d="{OUT}" fill="none" stroke="#000" stroke-width="{rimw*0.9}"/><path d="{OUT}" fill="none" stroke="#fff" stroke-width="{rimw*0.35}" transform="translate(0 0)"/>'
                   f'<path d="{LAT_L}" fill="{k}"/><path d="{mirror(LAT_L)}" fill="{k}"/><path d="{WING_L}" fill="{k}"/><path d="{mirror(WING_L)}" fill="{k}"/><path d="{STEM}" fill="{k}"/>{tr}{pads}</mask></defs>')
        out.append(f'<rect x="-50" y="-50" width="200" height="220" fill="{trace}" mask="url(#{gid}m)"/>')
        return ''.join(out)
    # colour version
    out.append(f'<path d="{OUT}" fill="{fill}" stroke="{rim}" stroke-width="{rimw}" stroke-linejoin="round"/>')
    out.append(f'<path d="{OUT}" fill="none" stroke="{rim2}" stroke-width="{rimw*0.3}" opacity=".95"/>')
    out.append(f'<g fill="none" stroke="{trace}" stroke-width="{tw}" stroke-linecap="round" stroke-linejoin="round">'+''.join(f'<path d="{d}"/>' for d,_,_ in TRACES_L+TRACES_R)+'</g>')
    for _,p,kind in TRACES_L+TRACES_R:
        out.append(f'<circle cx="{p[0]}" cy="{p[1]}" r="2.4" fill="{trace}"/>' if kind=="dot" else f'<circle cx="{p[0]}" cy="{p[1]}" r="2.2" fill="{fill}" stroke="{trace}" stroke-width="{tw}"/>')
    out.append(f'<g fill="{vent}"><path d="{LAT_L}"/><path d="{mirror(LAT_L)}"/><path d="{WING_L}"/><path d="{mirror(WING_L)}"/><path d="{STEM}"/></g>')
    return ''.join(out)

def wrap(inner, size=100, vb="4 -2 92 122"):
    vw,vh=float(vb.split()[2]),float(vb.split()[3])
    return f'<svg viewBox="{vb}" width="{size*vw/vh:.0f}" height="{size}" xmlns="http://www.w3.org/2000/svg">{inner}</svg>'
