import math, random, re

# ---------- geometry helpers ----------
def parse_path(d):
    """Absolute M/C/Z path -> list of cubic segments [(p0,p1,p2,p3)]."""
    toks = re.findall(r'[MCZ]|-?\d+\.?\d*', d); i=0; cur=None; start=None; segs=[]
    while i < len(toks):
        t = toks[i]
        if t == 'M': cur = (float(toks[i+1]), float(toks[i+2])); start=cur; i += 3
        elif t == 'C':
            p1=(float(toks[i+1]),float(toks[i+2])); p2=(float(toks[i+3]),float(toks[i+4])); p3=(float(toks[i+5]),float(toks[i+6]))
            segs.append((cur,p1,p2,p3)); cur=p3; i += 7
        elif t == 'Z': i += 1
        else: i += 1
    return segs
def bez(p0,p1,p2,p3,t):
    u=1-t; return (u*u*u*p0[0]+3*u*u*t*p1[0]+3*u*t*t*p2[0]+t*t*t*p3[0], u*u*u*p0[1]+3*u*u*t*p1[1]+3*u*t*t*p2[1]+t*t*t*p3[1])
def outline(d, n_per=24):
    pts=[]
    for s in parse_path(d):
        for k in range(n_per): pts.append(bez(*s, k/n_per))
    return pts
def inside(poly, x, y):
    c=False; n=len(poly); j=n-1
    for i in range(n):
        xi,yi=poly[i]; xj,yj=poly[j]
        if ((yi>y)!=(yj>y)) and (x < (xj-xi)*(y-yi)/((yj-yi) or 1e-9)+xi): c=not c
        j=i
    return c
def resample(pts, step):
    out=[pts[0]]; acc=0
    for a,b in zip(pts, pts[1:]+pts[:1]):
        d=math.dist(a,b); 
        while acc+d >= step:
            t=(step-acc)/d; a=(a[0]+(b[0]-a[0])*t, a[1]+(b[1]-a[1])*t); out.append(a); d=math.dist(a,b); acc=0
        acc+=d
    return out
def centroid(poly):
    return (sum(p[0] for p in poly)/len(poly), sum(p[1] for p in poly)/len(poly))

# Lateral brain, facing right. Cerebellum + stem as a second closed region.
BRAIN = ("M20 58 C12 50 14 36 24 30 C26 18 40 12 50 16 C58 8 74 8 82 18 C94 20 98 34 92 44 "
         "C96 52 90 62 80 62 C78 70 66 74 58 68 C50 72 40 70 36 64 C28 66 22 64 20 58 Z")
CEREB = "M26 70 C28 65 42 65 45 71 C43 79 29 80 26 70 Z"

def network_brain(seed=7, bstep=7.0, imin=8.5, n_int=60, hub=2, rmin=1.8, rmax=3.6, bmin=1.6, bmax=2.6, k_int=2, chain=0.85, stem=True):
    rnd = random.Random(seed)
    poly = outline(BRAIN); cpoly = outline(CEREB)
    cx, cy = centroid(poly)
    # boundary nodes slightly inset, with jitter
    bnodes=[]
    for (x,y) in resample(poly, bstep):
        vx,vy = cx-x, cy-y; L=math.hypot(vx,vy); x+=vx/L*2.2+rnd.uniform(-.6,.6); y+=vy/L*2.2+rnd.uniform(-.6,.6)
        bnodes.append([x,y,rnd.uniform(bmin,bmax),'b'])
    for (x,y) in resample(cpoly, 6.0):
        bnodes.append([x,y,rnd.uniform(1.4,2.0),'c'])
    # interior nodes: Poisson-ish
    inodes=[]; tries=0
    while len(inodes) < n_int and tries < 20000:
        tries+=1; x=rnd.uniform(10,100); y=rnd.uniform(5,85)
        if not inside(poly,x,y): continue
        if any(math.dist((x,y),(p[0],p[1])) < imin for p in inodes): continue
        if any(math.dist((x,y),(p[0],p[1])) < imin*0.75 for p in bnodes): continue
        inodes.append([x,y,rnd.uniform(rmin,rmax),'i'])
    # hubs
    inodes.sort(key=lambda p: -p[2])
    for k in range(hub): inodes[k][2]=rnd.uniform(5.2,6.4); inodes[k][3]='h'
    nodes = bnodes+inodes
    # edges: each node to its 2 nearest; interior hubs to 4
    edges=set()
    for i,p in enumerate(nodes):
        k = 4 if p[3]=='h' else (k_int if p[3] in 'ih' else 1)
        ds = sorted(((math.dist((p[0],p[1]),(q[0],q[1])), j) for j,q in enumerate(nodes) if j!=i))[:k]
        for d,j in ds:
            if d < 20: edges.add(tuple(sorted((i,j))))
    # boundary chain to keep the silhouette
    nb=len(bnodes)
    for i in range(nb):
        j=(i+1)%nb
        if bnodes[i][3]==bnodes[j][3] and rnd.random()<chain: edges.add(tuple(sorted((i,j))))
    if stem:
        base=len(nodes); nodes += [[44,78,2.0,'s'],[46,85,1.8,'s']]
        edges |= {(base,base+1)}
        # attach stem to nearest cerebellum/boundary node
        j=min(range(base), key=lambda q: math.dist((44,78),(nodes[q][0],nodes[q][1]))); edges.add((j,base))
    return nodes, edges

def network_svg(nodes, edges, stops, size=100, bg=None, stroke_w=1.6, gid='ng'):
    xs=[p[0] for p in nodes]; ys=[p[1] for p in nodes]
    g = ''.join(f'<stop offset="{o}" stop-color="{c}"/>' for o,c in stops)
    out=[f'<svg viewBox="0 0 110 100" width="{size*1.1:.0f}" height="{size}" xmlns="http://www.w3.org/2000/svg">']
    out.append(f'<defs><linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{min(xs)}" y1="{max(ys)}" x2="{max(xs)}" y2="{min(ys)}">{g}</linearGradient></defs>')
    if bg: out.append(f'<rect width="110" height="100" fill="{bg}"/>')
    out.append(f'<g stroke="url(#{gid})" stroke-width="{stroke_w}" stroke-linecap="round" fill="none">')
    for i,j in edges: out.append(f'<line x1="{nodes[i][0]:.1f}" y1="{nodes[i][1]:.1f}" x2="{nodes[j][0]:.1f}" y2="{nodes[j][1]:.1f}"/>')
    out.append(f'</g><g fill="url(#{gid})">')
    for x,y,r,t in nodes: out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}"/>')
    out.append('</g></svg>')
    return ''.join(out)

# ---------- split brain (top-down): circuit left, dendrites right ----------
AXIAL = ("M50 17 C44 7 28 7 22 20 C14 34 15 56 26 74 C32 84 42 92 50 85 C58 92 68 84 74 74 "
         "C85 56 86 34 78 20 C72 7 56 7 50 17 Z")
def split_brain(left, right, outline_col, sw=3.2):
    # outline as stroke only, split by midline
    circ = (f'<g fill="none" stroke="{left}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M38 24 H30 V38 H40 V50 H32 V64 H42"/><path d="M40 30 V44 H34"/><path d="M26 54 H36 V72"/><path d="M40 76 H30"/></g>'
            f'<g fill="{left}"><circle cx="38" cy="24" r="2.6"/><circle cx="42" cy="64" r="2.6"/><circle cx="40" cy="30" r="2.6"/><circle cx="36" cy="72" r="2.6"/><circle cx="40" cy="76" r="2.6"/></g>'
            f'<g fill="none" stroke="{left}" stroke-width="{sw*0.8}"><circle cx="26" cy="54" r="2.6"/><circle cx="34" cy="44" r="2.6"/></g>')
    dend = (f'<g fill="none" stroke="{right}" stroke-width="{sw}" stroke-linecap="round">'
            '<path d="M60 26 Q66 34 62 42 Q58 50 66 56 Q72 62 66 72"/><path d="M62 42 Q70 40 74 32"/><path d="M66 56 Q74 54 76 62"/>'
            '<path d="M56 68 Q60 76 56 82"/><path d="M68 30 Q72 24 70 18"/></g>'
            f'<g fill="{right}"><circle cx="74" cy="32" r="2.6"/><circle cx="76" cy="62" r="2.6"/><circle cx="56" cy="82" r="2.6"/><circle cx="70" cy="18" r="2.6"/><circle cx="66" cy="72" r="2.6"/><circle cx="60" cy="26" r="2.6"/></g>')
    return (f'<defs><clipPath id="L"><rect x="0" y="0" width="50" height="100"/></clipPath><clipPath id="R"><rect x="50" y="0" width="50" height="100"/></clipPath></defs>'
            f'<path d="{AXIAL}" fill="none" stroke="{left}" stroke-width="{sw}" clip-path="url(#L)"/>'
            f'<path d="{AXIAL}" fill="none" stroke="{right}" stroke-width="{sw}" clip-path="url(#R)"/>'
            f'<path d="M50 17 V85" fill="none" stroke="{outline_col}" stroke-width="{sw*0.8}" stroke-linecap="round"/>' + circ + dend)

def wrap(inner, size=100, vb="0 0 100 100", bg=None):
    b = f'<rect width="100" height="100" fill="{bg}"/>' if bg else ''
    return f'<svg viewBox="{vb}" width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg">{b}{inner}</svg>'

def split_lateral(back, front, sw=3.0):
    """Side-view brain outline split at the central sulcus: engineered back half, organic front half."""
    cb = CEREB
    circ = (f'<g fill="none" stroke="{back}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M30 42 H40 V30 H48"/><path d="M26 52 H44 V60"/><path d="M36 48 V40"/><path d="M48 36 V46 H54"/></g>'
            f'<g fill="{back}"><circle cx="48" cy="30" r="2.4"/><circle cx="44" cy="60" r="2.4"/><circle cx="54" cy="46" r="2.4"/></g>'
            f'<g fill="none" stroke="{back}" stroke-width="{sw*.8}"><circle cx="30" cy="42" r="2.4"/><circle cx="26" cy="52" r="2.4"/><circle cx="36" cy="40" r="2.2"/></g>')
    dend = (f'<g fill="none" stroke="{front}" stroke-width="{sw}" stroke-linecap="round">'
            '<path d="M62 30 Q70 36 66 44 Q62 52 70 58"/><path d="M66 44 Q76 42 80 34"/><path d="M70 58 Q78 56 84 50"/><path d="M64 36 Q58 44 60 54"/></g>'
            f'<g fill="{front}"><circle cx="62" cy="30" r="2.4"/><circle cx="80" cy="34" r="2.4"/><circle cx="84" cy="50" r="2.4"/><circle cx="70" cy="58" r="2.4"/><circle cx="60" cy="54" r="2.4"/></g>')
    return (f'<defs><clipPath id="sb"><rect x="0" y="0" width="56" height="100"/></clipPath><clipPath id="sf"><rect x="56" y="0" width="60" height="100"/></clipPath></defs>'
            f'<path d="{BRAIN}" fill="none" stroke="{back}" stroke-width="{sw}" clip-path="url(#sb)"/>'
            f'<path d="{BRAIN}" fill="none" stroke="{front}" stroke-width="{sw}" clip-path="url(#sf)"/>'
            f'<path d="{cb}" fill="none" stroke="{back}" stroke-width="{sw}"/>'
            f'<path d="M44 78 L47 88" fill="none" stroke="{back}" stroke-width="{sw}" stroke-linecap="round"/>'
            f'<path d="M56 12 L56 70" fill="none" stroke="{back}" stroke-width="{sw*.7}" stroke-linecap="round" stroke-dasharray="0.1 5"/>'
            + circ + dend)
