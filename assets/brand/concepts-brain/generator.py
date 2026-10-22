# Hand-drawn lateral brain (facing right) in a 100x100 box.
OUTLINE = ("M14 52 C10 40 16 26 30 22 C36 10 56 8 64 16 C74 10 92 16 92 30 C98 40 94 50 84 54 "
           "C86 64 76 72 64 70 C54 72 46 66 42 60 C32 62 22 60 14 52 Z")
CEREB   = "M26 61 C30 56 44 58 46 66 C44 74 28 74 24 66 C24 64 25 62 26 61 Z"
STEM    = "M40 73 C42 78 44 82 46 87"
# interior folds (gyri / sulci)
SYLVIAN = "M84 54 C74 50 62 54 50 50"
CENTRAL = "M57 12 C55 22 51 32 53 44"
FOLDS = [
    "M36 20 C44 27 52 19 60 25",     # parietal crown
    "M70 19 C78 25 85 24 89 31",     # frontal upper
    "M26 34 C34 41 44 33 52 39",     # parietal
    "M62 36 C70 43 78 35 86 41",     # frontal mid
    "M22 48 C29 53 37 46 45 50",     # occipital
    "M58 62 C65 67 73 60 80 62",     # temporal
]
CEREB_FOLDS = ["M30 64 C34 62 40 63 43 67", "M30 68 C34 66 40 67 42 70"]

def grad(gid, stops, x1=10,y1=80,x2=98,y2=10):
    s=''.join(f'<stop offset="{o}" stop-color="{c}"/>' for o,c in stops)
    return f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{s}</linearGradient>'

def paths(ds, stroke, sw, extra=""):
    return f'<g fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" {extra}>' + ''.join(f'<path d="{d}"/>' for d in ds) + '</g>'

# ---- A. LINE brain with the neural signal running along the Sylvian fissure ----
def line_signal(gid, stops, sw=3.0, accent=None):
    f=f'url(#{gid})'; acc = accent or f
    out=[f'<defs>{grad(gid,stops)}</defs>']
    out.append(paths([OUTLINE, CEREB, STEM], f, sw))
    out.append(paths([CENTRAL,FOLDS[0],FOLDS[1],FOLDS[3],FOLDS[5]]+CEREB_FOLDS, f, sw*0.8))
    # signal: enters at the back, runs the fissure, exits the front with a spike
    out.append(f'<path d="M4 50 H26 L32 50 L37 36 L43 64 L48 50 C60 54 74 50 84 54" fill="none" stroke="{acc}" stroke-width="{sw*1.15}" stroke-linecap="round" stroke-linejoin="round"/>')
    out.append(f'<circle cx="4" cy="50" r="{sw*1.2}" fill="{acc}"/>')
    return ''.join(out)

# ---- B. SOLID brain, folds knocked out, back half engineered ----
def solid_half(gid, stops, sw=3.0):
    f=f'url(#{gid})'
    circuit = ["M30 28 H40 V38", "M22 44 H34 V54 H42", "M40 20 V30", "M32 60 H42 V66"]
    pads = [(30,28),(40,38),(22,44),(42,54),(40,20),(42,66)]
    knock = (paths([SYLVIAN, CENTRAL]+FOLDS[:1]+FOLDS[4:5]+[FOLDS[3]]+CEREB_FOLDS, "#000", sw*0.9)
             + paths(circuit, "#000", sw*0.9)
             + ''.join(f'<circle cx="{x}" cy="{y}" r="{sw*0.9}" fill="#000"/>' for x,y in pads)
             + f'<path d="M50 14 V68" stroke="#000" stroke-width="{sw*0.6}" stroke-linecap="round" opacity=".9"/>')
    mask=(f'<mask id="{gid}m" maskUnits="userSpaceOnUse" x="0" y="0" width="100" height="100"><rect width="100" height="100" fill="#000"/>'
          f'<path d="{OUTLINE}" fill="#fff"/><path d="{CEREB}" fill="#fff"/>{paths([STEM],"#fff",sw*1.4)}{knock}</mask>')
    return f'<defs>{grad(gid,stops)}{mask}</defs><rect width="100" height="100" fill="{f}" mask="url(#{gid}m)"/>'

# ---- C. LINE brain, back half circuit traces, front half natural folds ----
def line_half(gid, stops, sw=3.0):
    f=f'url(#{gid})'
    out=[f'<defs>{grad(gid,stops)}</defs>']
    out.append(paths([OUTLINE, CEREB, STEM], f, sw))
    out.append(paths([CENTRAL, FOLDS[0], FOLDS[4], FOLDS[3], SYLVIAN], f, sw*0.8))     # front: natural
    circuit = ["M30 28 H40 V38", "M22 44 H34 V54 H42", "M40 20 V30", "M32 60 H42 V66"]
    out.append(paths(circuit, f, sw*0.8))
    for x,y in [(30,28),(40,38),(22,44),(42,54),(40,20),(42,66)]:
        out.append(f'<circle cx="{x}" cy="{y}" r="{sw*0.85}" fill="{f}"/>')
    return ''.join(out)

# ---- D. SOLID brain with natural folds only (the pure icon), gradient ----
def solid_pure(gid, stops, sw=3.0):
    f=f'url(#{gid})'
    knock = paths([SYLVIAN, CENTRAL]+FOLDS+CEREB_FOLDS, "#000", sw*0.9)
    mask=(f'<mask id="{gid}m" maskUnits="userSpaceOnUse" x="0" y="0" width="100" height="100"><rect width="100" height="100" fill="#000"/>'
          f'<path d="{OUTLINE}" fill="#fff"/><path d="{CEREB}" fill="#fff"/>{paths([STEM],"#fff",sw*1.4)}{knock}</mask>')
    return f'<defs>{grad(gid,stops)}{mask}</defs><rect width="100" height="100" fill="{f}" mask="url(#{gid}m)"/>'

def wrap(inner, size=100, vb="2 4 100 88", bg=None):
    b=f'<rect x="-50" y="-50" width="220" height="220" fill="{bg}"/>' if bg else ''
    vw,vh=float(vb.split()[2]),float(vb.split()[3])
    return f'<svg viewBox="{vb}" width="{size:.0f}" height="{size*vh/vw:.0f}" xmlns="http://www.w3.org/2000/svg">{b}{inner}</svg>'
