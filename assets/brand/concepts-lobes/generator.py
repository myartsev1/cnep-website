import math
# Brain as a union of lobe circles (side view, facing right). (cx, cy, r)
LOBES = [(33,46,16),(47,31,19),(65,28,17),(78,43,15),(66,55,14),(48,57,13)]
CEREB = (37,73,9)
STEM = ((46,78),(49,90))

def inside(x,y,margin=0.0, lobes=LOBES):
    return any(math.dist((x,y),(cx,cy)) <= r-margin for cx,cy,r in lobes)

def circles(lobes, fill, dr=0.0):
    return ''.join(f'<circle cx="{cx}" cy="{cy}" r="{r+dr:.2f}" fill="{fill}"/>' for cx,cy,r in lobes)

def grad(gid, stops, x1=14,y1=70,x2=96,y2=14):
    s=''.join(f'<stop offset="{o}" stop-color="{c}"/>' for o,c in stops)
    return f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{s}</linearGradient>'

def stem(fill, sw=4.2):
    (x1,y1),(x2,y2)=STEM
    return f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{fill}" stroke-width="{sw}" stroke-linecap="round" fill="none"/>'

# ---------- A. SOLID: lobed silhouette with a circuit knocked out ----------
def solid(gid, stops, bg_knock="#000"):
    fill=f'url(#{gid})'
    traces = ('<g fill="none" stroke="#000" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round">'
              '<path d="M22 46 H84"/><path d="M40 46 V30 H56"/><path d="M62 46 V60 H76"/><path d="M72 46 V28"/><path d="M50 46 V62"/></g>'
              '<g fill="#000"><circle cx="56" cy="30" r="3.4"/><circle cx="76" cy="60" r="3.4"/><circle cx="84" cy="46" r="3.4"/><circle cx="22" cy="46" r="3.4"/><circle cx="72" cy="28" r="3.4"/><circle cx="50" cy="62" r="3.4"/></g>'
              '<g fill="none" stroke="#000" stroke-width="2.6"><circle cx="40" cy="46" r="3.6"/><circle cx="62" cy="46" r="3.6"/></g>')
    mask=(f'<mask id="{gid}m" maskUnits="userSpaceOnUse" x="0" y="0" width="110" height="100"><rect width="110" height="100" fill="#000"/>'
          f'{circles(LOBES,"#fff")}{circles([CEREB],"#fff")}{stem("#fff")}{traces}</mask>')
    return f'<defs>{grad(gid,stops)}{mask}</defs><rect width="110" height="100" fill="{fill}" mask="url(#{gid}m)"/>'

# ---------- B. OUTLINE: lobed line with one signal through it ----------
def outline(gid, stops, sw=3.6):
    fill=f'url(#{gid})'
    mask=(f'<mask id="{gid}m" maskUnits="userSpaceOnUse" x="0" y="0" width="110" height="100"><rect width="110" height="100" fill="#000"/>'
          f'{circles(LOBES,"#fff")}{circles(LOBES,"#000",-sw)}'
          f'{circles([CEREB],"#fff")}{circles([CEREB],"#000",-sw)}'
          f'{stem("#fff", sw)}'
          # signal line and nodes
          f'<path d="M26 50 C38 36 52 62 66 42 C72 34 80 38 84 44" fill="none" stroke="#fff" stroke-width="{sw}" stroke-linecap="round"/>'
          f'<circle cx="26" cy="50" r="{sw*1.15}" fill="#fff"/><circle cx="84" cy="44" r="{sw*1.15}" fill="#fff"/><circle cx="52" cy="46" r="{sw*1.4}" fill="#fff"/>'
          '</mask>')
    return f'<defs>{grad(gid,stops)}{mask}</defs><rect width="110" height="100" fill="{fill}" mask="url(#{gid}m)"/>'

# ---------- C. LATTICE: nodes on an ordered hex lattice, clipped to the lobes ----------
def lattice(gid, stops, s=8.6, base=2.3, hubs=((54,40),(72,38),(42,52)), link_w=1.9, phase=(0,0)):
    fill=f'url(#{gid})'
    nodes={}; dy=s*math.sqrt(3)/2
    row=0; y=12+phase[1]
    while y<70:
        x0=14+phase[0]+(s/2 if row%2 else 0); x=x0; col=0
        while x<100:
            if inside(x,y,margin=2.6): nodes[(row,col)]=[x,y,base]
            x+=s; col+=1
        y+=dy; row+=1
    # size hierarchy: hubs and a soft falloff
    for (hx,hy) in hubs:
        k=min(nodes, key=lambda k: math.dist((hx,hy),(nodes[k][0],nodes[k][1]))); nodes[k][2]=4.9
    for k,(x,y,r) in nodes.items():
        if r<4: 
            d=min(math.dist((x,y),h) for h in hubs); nodes[k][2]= base + 1.1*max(0,1-d/18)
    # edges along lattice; deterministic thinning so it reads as a network, not a grid
    edges=[]
    for (r,c) in nodes:
        for (dr,dc,tag) in [(0,1,'h'),(1,0 if r%2==0 else 1,'dr'),(1,-1 if r%2==0 else 0,'dl')]:
            k2=(r+dr,c+dc)
            if k2 in nodes:
                keep = {'h':(r+c)%3!=1, 'dr':(r*2+c)%3!=0, 'dl':(r+2*c)%3!=2}[tag]
                if keep: edges.append(((r,c),k2))
    out=[f'<defs>{grad(gid,stops)}</defs>']
    out.append(f'<g stroke="{fill}" stroke-width="{link_w}" stroke-linecap="round">')
    for a,b in edges:
        out.append(f'<line x1="{nodes[a][0]:.1f}" y1="{nodes[a][1]:.1f}" x2="{nodes[b][0]:.1f}" y2="{nodes[b][1]:.1f}"/>')
    out.append('</g>')
    # cerebellum cluster + stem
    cx,cy,cr=CEREB
    cl=[(cx-4,cy-2,2.2),(cx+3,cy-3,2.0),(cx-1,cy+4,2.4),(cx+5,cy+3,1.8)]
    out.append(f'<g stroke="{fill}" stroke-width="{link_w}" stroke-linecap="round"><path d="M{cl[0][0]} {cl[0][1]} L{cl[1][0]} {cl[1][1]} L{cl[3][0]} {cl[3][1]} L{cl[2][0]} {cl[2][1]} Z" fill="none"/><path d="M{cl[3][0]} {cl[3][1]} L47 86" fill="none"/></g>')
    out.append(f'<g fill="{fill}">')
    for x,y,r in cl: out.append(f'<circle cx="{x}" cy="{y}" r="{r}"/>')
    out.append('<circle cx="47" cy="87" r="2.4"/>')
    for x,y,r in nodes.values(): out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}"/>')
    out.append('</g>')
    return ''.join(out)

# ---------- D. SOLID SPLIT: back half electrode array, front half living gyri ----------
def solid_split(gid, stops):
    fill=f'url(#{gid})'
    dots=''.join(f'<circle cx="{x}" cy="{y}" r="2.1" fill="#000"/>' for y in range(24,66,7) for x in range(22,54,7) if inside(x,y,margin=3.5))
    gyri=('<g fill="none" stroke="#000" stroke-width="3.2" stroke-linecap="round">'
          '<path d="M64 20 C72 28 64 40 72 48 C78 54 70 62 64 66"/><path d="M62 34 C58 42 66 48 62 58"/><path d="M78 30 C86 36 86 46 80 52"/><path d="M84 56 C88 60 84 66 78 66"/></g>')
    mask=(f'<mask id="{gid}m" maskUnits="userSpaceOnUse" x="0" y="0" width="110" height="100"><rect width="110" height="100" fill="#000"/>'
          f'{circles(LOBES,"#fff")}{circles([CEREB],"#fff")}{stem("#fff")}{dots}{gyri}'
          f'<path d="M57 14 V70" stroke="#000" stroke-width="2.4" stroke-linecap="round"/></mask>')
    return f'<defs>{grad(gid,stops)}{mask}</defs><rect width="110" height="100" fill="{fill}" mask="url(#{gid}m)"/>'

def wrap(inner, size=100, vb="6 6 100 90", bg=None):
    b=f'<rect x="-50" y="-50" width="220" height="220" fill="{bg}"/>' if bg else ''
    vw,vh=float(vb.split()[2]),float(vb.split()[3])
    return f'<svg viewBox="{vb}" width="{size:.0f}" height="{size*vh/vw:.0f}" xmlns="http://www.w3.org/2000/svg">{b}{inner}</svg>'

def solid_spike(gid, stops):
    fill=f'url(#{gid})'
    spike=('<path d="M20 48 H42 L47 48 L52 24 L58 70 L63 48 H88" fill="none" stroke="#000" stroke-width="4.2" stroke-linejoin="round" stroke-linecap="round"/>')
    mask=(f'<mask id="{gid}m" maskUnits="userSpaceOnUse" x="0" y="0" width="110" height="100"><rect width="110" height="100" fill="#000"/>'
          f'{circles(LOBES,"#fff")}{circles([CEREB],"#fff")}{stem("#fff")}{spike}</mask>')
    return f'<defs>{grad(gid,stops)}{mask}</defs><rect width="110" height="100" fill="{fill}" mask="url(#{gid}m)"/>'
