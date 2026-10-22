#!/usr/bin/env python3
"""Generates the static CNEP site. Edit content below, then run:  python3 build.py"""
import os, html

OUT = os.path.dirname(os.path.abspath(__file__))
SITE = "Center for Neural Engineering & Prostheses"
EMAIL = "myartsev@berkeley.edu"
# Inquiry form delivery. Paste a Formspree endpoint such as "https://formspree.io/f/abcdwxyz" to have
# submissions emailed to EMAIL without opening the visitor's mail app. Leave empty to use a mailto fallback.
FORM_ENDPOINT = ""
PHOTO_EXT = {"adam-gazzaley": "jpg", "liberty-hamilton": "jpg", "richard-ivry": "jpg"}  # everything else is .webp

NAV = [
    ("about.html", "About"),
    ("leadership.html", "Leadership"),
    ("faculty.html", "Faculty"),
    ("annual-meeting.html", "Annual Meeting"),
    ("resources.html", "Tools & Resources"),
]

FACULTY_UCB = [
    ("Elad Alon", "elad-alon", "https://www2.eecs.berkeley.edu/Faculty/Homepages/elad.html"),
    ("Ruzena Bajcsy", "ruzena-bajcsy", "https://www2.eecs.berkeley.edu/Faculty/Homepages/bajcsy.html"),
    ("Jack Gallant", "jack-gallant", "https://vcresearch.berkeley.edu/faculty/jack-gallant"),
    ("Liberty Hamilton", "liberty-hamilton", "https://www.hamiltonlab.org/people/"),
    ("Alex Huth", "alex-huth", "https://vision.berkeley.edu/people/alexander-huth"),
    ("Richard Ivry", "richard-ivry", "https://vcresearch.berkeley.edu/faculty/richard-ivry"),
    ("Preeya Khanna", "preeya-khanna", "https://vcresearch.berkeley.edu/faculty/preeya-khanna"),
    ("Robert Knight", "robert-knight", "https://vcresearch.berkeley.edu/faculty/robert-thomas-knight"),
    ("Michael Lustig", "michael-lustig", "https://vcresearch.berkeley.edu/faculty/michael-miki-lustig"),
    ("Rikky Muller", "rikky-muller", "https://vcresearch.berkeley.edu/faculty/rikky-muller"),
    ("Bruno Olshausen", "bruno-olshausen", "https://www2.eecs.berkeley.edu/Faculty/Homepages/baolshausen.html"),
    ("Friedrich Sommer", "friedrich-sommer", "https://ccb.berkeley.edu/people/friedrich-sommer"),
    ("Frederic Theunissen", "frederic-theunissen", None),
    ("Claire Tomlin", "claire-tomlin", "https://www2.eecs.berkeley.edu/Faculty/Homepages/tomlin.html"),
    ("Joni Wallis", "joni-wallis", "https://vcresearch.berkeley.edu/faculty/joni-wallis"),
    ("Michael Yartsev", "michael-yartsev", "https://www.michaelyartsev.com/"),
]
FACULTY_UCSF = [
    ("Michael Beattie", "michael-beattie", "https://profiles.ucsf.edu/michael.beattie"),
    ("Mitchel Berger", "mitchel-berger", "https://profiles.ucsf.edu/mitchel.berger"),
    ("Joshua Berke", "joshua-berke", "https://profiles.ucsf.edu/joshua.berke"),
    ("Edward Chang", "edward-chang", "https://changlab.ucsf.edu"),
    ("Winston Chiong", "winston-chiong", "https://memory.ucsf.edu/people/winston-chiong"),
    ("Loren Frank", "loren-frank", "https://franklab.ucsf.edu"),
    ("Karunesh Ganguly", "karunesh-ganguly", "https://www.gangulylab.org"),
    ("Adam Gazzaley", "adam-gazzaley", "https://neuroscape.ucsf.edu/profile/adam-gazzaley/"),
    ("Andrew Krystal", "andrew-krystal", "https://dolby.ucsf.edu/content/andrew-krystal-md"),
    ("Andrew Lee", "andrew-lee", "https://profiles.ucsf.edu/andrew.m.lee"),
    ("Geoffrey Manley", "geoffrey-manley", "https://profiles.ucsf.edu/geoffrey.manley"),
    ("Khaled Moussawi", "khaled-moussawi", "https://tn2lab.ucsf.edu/content/khaled-moussawi-md-phd"),
    ("Richard O'Donnell", "richard-o-donnell", "https://profiles.ucsf.edu/richard.odonnell"),
    ("Christoph Schreiner", "christoph-schreiner", "https://neurograd.ucsf.edu/people/christoph-schreiner-md-phd"),
    ("Prasad Shirvalkar", "prasad-shirvalkar", "https://www.shirvalkarlab.com"),
    ("Philip Starr", "philip-starr", "https://starrlab.ucsf.edu/people/philip-starr"),
]
N_FACULTY = len(FACULTY_UCB) + len(FACULTY_UCSF)

RESOURCES = [
    ("OpenMind Consortium", "openmind-consortium.notion.site", "https://openmind-consortium.notion.site/Welcome-f9421eec768240f9914478939a0ed6c4",
     "Engineering and regulatory resources for clinical studies using Medtronic Percept and other advanced neuromodulation systems. An NIH BRAIN Initiative technology dissemination program led from UCSF."),
    ("IEEE Brain", "brain.ieee.org", "https://brain.ieee.org/",
     "Upcoming neural engineering workshops and other resources from the IEEE Brain Technical Community."),
    ("Open-Source Quality Management System", "OpenMind Consortium", "https://openmind-consortium.notion.site/895f8140b6b64f7bb78e4b9442ea62d7",
     "A fully templated QMS for academic device teams starting quality systems for FDA IDE studies."),
    ("Weill Neurohub", "weillneurohub.org", "https://www.weillneurohub.org/",
     "A cross-institutional umbrella supporting team-based translational neuroscience across UC Berkeley, UCSF, the University of Washington, and the Allen Institute."),
    ("Bakar BioEnginuity Hub", "UC Berkeley", "https://bio.bakarlabs.org/campus-programs/",
     "A multi-faceted resource for technology transfer and commercialization, including incubator space and entrepreneurship expertise."),
    ("Bakar Computational Biomedicine Initiative", "UC Berkeley &middot; UCSF", "https://bcbi.berkeley.edu/",
     "A joint UC Berkeley-UCSF initiative combining AI, computing and experimental biology to uncover disease mechanisms and accelerate new diagnostics and therapies."),
    ("Berkeley Wireless Research Center", "UC Berkeley", "https://bwrc.berkeley.edu/",
     "A UC Berkeley research center for wireless systems and integrated circuits, working with industry members and training graduate students and postdocs."),
    ("iBCI-CC", "ibci-cc.org", "https://www.ibci-cc.org/",
     "An FDA Collaborative Community developing resources for the implantable brain-computer interface development community."),
    ("Neuroethics Resources", "OpenMind Consortium", "https://openmind-consortium.notion.site/00e98e6f57d041aaa6f62937ddbabd27",
     "A selection of publications on neuroethics, with an emphasis on neuromodulation."),
    ("IDE Materials &amp; FDA Guidance", "OpenMind Consortium", "https://openmind-consortium.notion.site/07426baee3b94c46a6c2a96518f80c6b",
     "Example IDE protocols, FDA correspondence and a curated list of FDA guidance documents relevant to neural device research."),
]


# Face centers (x, y as fractions of width/height, origin top-left) and image aspect ratio (w/h),
# measured with macOS Vision. Used to compute object-position so every crop is framed on the face.
FACE = {
    "adam-gazzaley": (0.565, 0.438, 1.00), "alex-huth": (0.482, 0.485, 0.75), "andrew-krystal": (0.627, 0.313, 1.50),
    "andrew-lee": (0.491, 0.459, 1.78), "bruno-olshausen": (0.507, 0.531, 0.78), "christoph-schreiner": (0.499, 0.351, 0.66),
    "claire-tomlin": (0.561, 0.403, 0.71), "edward-chang-lead": (0.490, 0.555, 0.83), "edward-chang": (0.468, 0.353, 0.86),
    "elad-alon": (0.550, 0.514, 0.65), "frederic-theunissen": (0.563, 0.456, 1.50), "friedrich-sommer": (0.488, 0.539, 1.50),
    "geoffrey-manley": (0.492, 0.290, 1.00), "jack-gallant": (0.449, 0.635, 2.00), "liberty-hamilton": (0.518, 0.462, 1.05), "joni-wallis": (0.518, 0.470, 1.50),
    "joshua-berke": (0.524, 0.520, 0.81), "karunesh-ganguly": (0.524, 0.343, 1.00), "khaled-moussawi": (0.631, 0.385, 1.00),
    "loren-frank": (0.515, 0.458, 0.75), "michael-beattie": (0.502, 0.398, 0.82), "michael-lustig": (0.689, 0.530, 0.73),
    "michael-yartsev-lead": (0.481, 0.545, 0.83), "michael-yartsev": (0.501, 0.519, 1.00), "mitchel-berger": (0.488, 0.450, 1.00),
    "philip-starr": (0.480, 0.375, 0.86), "prasad-shirvalkar": (0.485, 0.527, 1.00), "preeya-khanna": (0.499, 0.502, 1.20),
    "richard-ivry": (0.568, 0.545, 1.00), "richard-o-donnell": (0.500, 0.442, 0.69), "rikky-muller": (0.491, 0.408, 0.78),
    "robert-knight": (0.493, 0.593, 0.75), "ruzena-bajcsy": (0.510, 0.501, 0.71), "winston-chiong": (0.461, 0.527, 1.00),
}

def face_pos(slug, box=0.8, face_y=0.42):
    """object-position that places the detected face at the horizontal center and at `face_y` of a box with w/h = `box`."""
    if slug not in FACE: return "center top"
    cx, cy, r = FACE[slug]
    if r > box:   # image wider than box: horizontal overflow
        x = (cx * r - box / 2) / (r - box); y = 0.5
    elif r < box: # image taller than box: vertical overflow
        x = 0.5; y = (cy / r - face_y / box) / (1 / r - 1 / box)
    else:
        x, y = 0.5, 0.5
    x = min(1, max(0, x)); y = min(1, max(0, y))
    return f"{x*100:.0f}% {y*100:.0f}%"

def img_face(slug, alt="", box=0.8, **attrs):
    extra = "".join(f' {k}="{v}"' for k, v in attrs.items())
    return f'<img src="assets/people/{slug}.{PHOTO_EXT.get(slug, "webp")}" alt="{e(alt)}" style="object-position:{face_pos(slug, box)}"{extra}>'

ARR = '<span class="arr" aria-hidden="true">&rarr;</span>'
SPIKE_PATH = "M5 22 H14 L17.5 22 L20 9 L22.5 29 L25 22 H35"
DOTS = [(9,9),(16.33,9),(23.67,9),(31,9),(9,31),(16.33,31),(23.67,31),(31,31),(9,16.33),(31,16.33),(9,23.67),(31,23.67)]
_dots = "".join(f'<circle cx="{x}" cy="{y}" r="1.5"/>' for x,y in DOTS)
LOGO_SVG = (f'<svg class="brand__mark" viewBox="0 0 40 40" aria-hidden="true">'
            f'<rect x="1" y="1" width="38" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="1.6"/>'
            f'<g fill="currentColor" opacity=".35">{_dots}</g>'
            f'<path d="{SPIKE_PATH}" fill="none" stroke="var(--mark-accent,#0073e6)" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round"/>'
            f'</svg>')
FAVICON_SVG = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40">'
               f'<rect width="40" height="40" rx="6" fill="#001f44"/>'
               f'<g fill="#fff" opacity=".3">{_dots}</g>'
               f'<path d="{SPIKE_PATH}" fill="none" stroke="#fff" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>'
               f'</svg>')
SITE_URL = "https://myartsev1.github.io/cnep-website/"

def e(s): return html.escape(s, quote=True)

def brand(cls=""):
    return f"""<a class="brand {cls}" href="index.html" aria-label="CNEP home">{LOGO_SVG}
<span class="brand__text"><span class="brand__name">CNEP</span><span class="brand__sub">Center for Neural Engineering &amp; Prostheses</span></span></a>"""

def header(current):
    def links(cls=""):
        out = []
        for href, label in NAV:
            cur = ' aria-current="page"' if href == current else ""
            out.append(f'<a href="{href}"{cur}>{label}</a>')
        return "".join(out)
    donate_cur = ' aria-current="page"' if current == "donate.html" else ""
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="header">
  <div class="container">
    {brand()}
    <nav class="nav" aria-label="Primary">{links()}<a class="btn btn--solid" href="donate.html"{donate_cur}>Support CNEP</a></nav>
    <button class="menu-btn" aria-expanded="false" aria-controls="mobile-nav" aria-label="Toggle menu"><span></span><span></span><span></span></button>
  </div>
  <nav class="mobile-nav" id="mobile-nav" aria-label="Mobile">{links()}<a href="donate.html"{donate_cur}>Support CNEP</a></nav>
</header>"""

def footer():
    nav_links = "".join(f'<li><a href="{h}">{l}</a></li>' for h, l in [("index.html","Home")] + NAV + [("donate.html","Support CNEP")])
    return f"""<footer class="footer">
  <div class="container">
    <div class="footer__top">
      <div>{brand()}<p class="footer__desc">The {SITE} is a collaborative enterprise of UCSF and the University of California, Berkeley, developing technology to restore function for people with neurological disabilities.</p></div>
      <div><h4>Navigate</h4><ul>{nav_links}</ul></div>
      <div><h4>Institutions</h4><ul>
        <li><a href="https://www.berkeley.edu" rel="noopener">UC Berkeley</a></li>
        <li><a href="https://www.ucsf.edu" rel="noopener">UCSF</a></li>
        <li><a href="https://neurosurgery.ucsf.edu" rel="noopener">UCSF Neurological Surgery</a></li>
        <li><a href="https://bioeng.berkeley.edu" rel="noopener">Berkeley Bioengineering</a></li>
      </ul></div>
      <div><h4>Contact</h4><ul>
        <li><a href="donate.html#inquiry">Send us a message</a></li>
        <li><a href="donate.html">Giving inquiries</a></li>
      </ul></div>
    </div>
    <div class="footer__bottom">
      <span class="mono">&copy; 2026 {SITE}</span>
      <span class="mono">Est. 2010 &middot; Berkeley &amp; San Francisco, California</span>
    </div>
  </div>
</footer>"""

os.makedirs(os.path.join(OUT, "assets", "brand"), exist_ok=True)
with open(os.path.join(OUT, "assets", "brand", "favicon.svg"), "w", encoding="utf-8") as _f:
    _f.write(FAVICON_SVG)

def page(filename, title, description, body):
    full_title = SITE if filename == "index.html" else f"{title} — CNEP"
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full_title)}</title>
<meta name="description" content="{e(description)}">
<meta property="og:title" content="{e(full_title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:type" content="website">
<meta property="og:image" content="{SITE_URL}assets/brand/cnep-social.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/brand/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/brand/apple-touch-icon.png">
<meta name="theme-color" content="#fbf8f2">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&family=Source+Serif+4:opsz,wght@8..60,300;8..60,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css">
</head>
<body>
{header(filename)}
<main id="main">
{body}
</main>
{footer()}
<script src="js/main.js"></script>
</body>
</html>
"""
    with open(os.path.join(OUT, filename), "w", encoding="utf-8") as f:
        f.write(doc)
    print("wrote", filename)

def person_card(name, slug, url, inst, lg=False):
    link = f'<a class="link small person__link" href="{url}" rel="noopener">Profile {ARR}</a>' if url else ""
    cls = "person person--lg" if lg else "person"
    return f"""<div class="{cls}">
  <div class="person__photo">{img_face(slug, name, 0.8, loading="lazy")}</div>
  <div><div class="person__name">{e(name)}</div><div class="mono person__meta">{inst}</div>{link}</div>
</div>"""

def page_head(eyebrow, title, lede="", aside=""):
    lede_html = f'<p class="lede">{lede}</p>' if lede else ""
    if aside:
        return f"""<section class="page-head container"><div class="page-head__grid">
  <div><div class="eyebrow mono">{eyebrow}</div><h1 class="display">{title}</h1>{lede_html}</div>
  <div class="hero__aside">{aside}</div></div></section>"""
    return f"""<section class="page-head container"><div class="eyebrow mono">{eyebrow}</div><h1 class="display">{title}</h1>{lede_html}</section>"""


def inquiry_form(heading="Send us a message", intro=""):
    intro_html = f'<p class="lede" style="margin-top:.75rem">{intro}</p>' if intro else ""
    return f"""<div class="inquiry" id="inquiry">
  <div class="mono" style="margin-bottom:.75rem">Contact</div>
  <h2 class="h3" style="color:var(--navy)">{heading}</h2>{intro_html}
  <form class="iform" action="{FORM_ENDPOINT}" method="POST" data-endpoint="{FORM_ENDPOINT}" data-to="{EMAIL}" novalidate>
    <div class="iform__row">
      <label class="ifield"><span class="mono">Name</span><input type="text" name="name" autocomplete="name" required></label>
      <label class="ifield"><span class="mono">Email</span><input type="email" name="email" autocomplete="email" required></label>
    </div>
    <div class="iform__row">
      <label class="ifield"><span class="mono">Affiliation <em>optional</em></span><input type="text" name="affiliation" autocomplete="organization"></label>
      <label class="ifield"><span class="mono">Topic</span>
        <select name="topic"><option>Giving inquiry</option><option>Collaboration</option><option>Annual meeting</option><option>Suggest a resource</option><option>Other</option></select></label>
    </div>
    <label class="ifield"><span class="mono">Message</span><textarea name="message" rows="6" required></textarea></label>
    <input type="text" name="_gotcha" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px">
    <div class="iform__foot">
      <button class="btn btn--solid" type="submit">Send message <span class="arr" aria-hidden="true">&rarr;</span></button>
      <span class="iform__status small muted" role="status" aria-live="polite"></span>
    </div>
  </form>
</div>"""


# ------------------------------------------------------------------ HERO GRAPHIC
def hero_graphic():
    """Original illustration: a multi-channel neural recording over an electrode grid.
    Deterministic pseudo-random so every build renders the same image."""
    import math, random
    rnd = random.Random(2010)
    W, H = 1600, 760
    out = []
    out.append(f'<svg class="neuro" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="neuro-t">')
    out.append('<title id="neuro-t">Illustration of multi-channel neural recordings over an electrode array</title>')
    out.append('<defs>'
               '<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0c2043"/><stop offset="1" stop-color="#001f44"/></linearGradient>'
               '<linearGradient id="fade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#001f44" stop-opacity="1"/><stop offset=".12" stop-color="#001f44" stop-opacity="0"/><stop offset=".9" stop-color="#001f44" stop-opacity="0"/><stop offset="1" stop-color="#001f44" stop-opacity="1"/></linearGradient>'
               '<radialGradient id="glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#0073e6" stop-opacity=".55"/><stop offset="1" stop-color="#0073e6" stop-opacity="0"/></radialGradient>'
               '</defs>')
    out.append(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
    # electrode grid (16 x 8), faint
    gx0, gy0, cols, rows, pitch = 120, 90, 16, 8, 84
    out.append('<g fill="none" stroke="#ffffff" stroke-opacity=".12" stroke-width="1">')
    for c in range(cols):
        x = gx0 + c * pitch
        out.append(f'<line x1="{x}" y1="{gy0-30}" x2="{x}" y2="{gy0+(rows-1)*pitch+30}"/>')
    for r in range(rows):
        y = gy0 + r * pitch
        out.append(f'<line x1="{gx0-30}" y1="{y}" x2="{gx0+(cols-1)*pitch+30}" y2="{y}"/>')
    out.append('</g>')
    # active electrode cluster glow
    out.append(f'<circle cx="{gx0+9*pitch}" cy="{gy0+3*pitch}" r="230" fill="url(#glow)"/>')
    out.append('<g>')
    for r in range(rows):
        for c in range(cols):
            x, y = gx0 + c * pitch, gy0 + r * pitch
            d = math.hypot(c - 9, r - 3)
            act = max(0.0, 1 - d / 5.5)
            op = 0.22 + 0.7 * act
            rad = 3.2 + 3.8 * act
            col = "#ffd74b" if act > 0.82 else "#ffffff"
            out.append(f'<circle cx="{x}" cy="{y}" r="{rad:.1f}" fill="{col}" fill-opacity="{op:.2f}"/>')
    out.append('</g>')
    # traces: 8 channels, smooth noise + spikes, drawn across the full width
    n_ch, x0, x1 = 8, 60, W - 60
    top, gap = 150, 68
    pts_n = 420
    out.append('<g fill="none" stroke-linecap="round" stroke-linejoin="round">')
    for ch in range(n_ch):
        base = top + ch * gap
        amp = 10 + 12 * math.exp(-((ch - 3.2) ** 2) / 6)
        # smooth noise via summed sines with random phase
        comps = [(rnd.uniform(0.6, 1.0), rnd.uniform(0, 6.28), rnd.uniform(3, 9)) for _ in range(5)]
        spikes = sorted(rnd.sample(range(40, pts_n - 40), rnd.randint(4, 9)))
        pts = []
        for i in range(pts_n):
            t = i / (pts_n - 1)
            v = sum(a * math.sin(t * f * 6.28 + ph) for a, ph, f in comps) / 3
            v += rnd.gauss(0, 0.22)
            for sp in spikes:
                dd = i - sp
                if -3 <= dd <= 8:
                    v -= (2.6 if ch in (2, 3, 4) else 1.6) * math.exp(-(dd * dd) / 5) * (1 if dd >= 0 else 0.4)
            x = x0 + t * (x1 - x0)
            pts.append((x, base + v * amp))
        d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        hot = ch in (2, 3, 4)
        stroke = "#9cc8ff" if hot else "#ffffff"
        op = 0.95 if hot else 0.55
        sw = 1.9 if hot else 1.3
        out.append(f'<path d="{d}" stroke="{stroke}" stroke-opacity="{op}" stroke-width="{sw}"/>')
        # channel label
        out.append(f'<text x="{x0}" y="{base-26}" font-family="IBM Plex Mono, monospace" font-size="13" letter-spacing="1.5" fill="#ffffff" fill-opacity=".45">CH {ch+1:02d}</text>')
    out.append('</g>')
    # spike-time raster strip at the bottom
    out.append('<g>')
    ry = H - 86
    out.append(f'<text x="{x0}" y="{ry-18}" font-family="IBM Plex Mono, monospace" font-size="13" letter-spacing="1.5" fill="#ffffff" fill-opacity=".45">UNITS</text>')
    for u in range(24):
        yy = ry + u * 2.6
        for _ in range(rnd.randint(9, 26)):
            xx = rnd.uniform(x0, x1)
            out.append(f'<rect x="{xx:.1f}" y="{yy:.1f}" width="1.6" height="1.6" fill="#ffd74b" fill-opacity=".8"/>')
    out.append('</g>')
    # time scale bar
    out.append(f'<g stroke="#ffffff" stroke-opacity=".7" stroke-width="1.5"><line x1="{x1-200}" y1="{H-30}" x2="{x1}" y2="{H-30}"/><line x1="{x1-200}" y1="{H-36}" x2="{x1-200}" y2="{H-24}"/><line x1="{x1}" y1="{H-36}" x2="{x1}" y2="{H-24}"/></g>')
    out.append(f'<text x="{x1-100}" y="{H-40}" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="13" letter-spacing="1.5" fill="#ffffff" fill-opacity=".7">500 ms</text>')
    out.append(f'<rect width="{W}" height="{H}" fill="url(#fade)"/>')
    out.append('</svg>')
    return "".join(out)

# ------------------------------------------------------------------ HOME
focus_items = [
    ("01", "Sensory function", "Interfaces that restore or augment sensory experience for people who have lost it, drawing on neural recording, stimulation and signal processing."),
    ("02", "Motor function", "Brain-computer interfaces and neuroprosthetic systems that let people with paralysis move, reach and act in the world again."),
    ("03", "Communication &amp; cognition", "Real-time decoding of the brain's speech signals and approaches to recover cognitive capacities, for people who have lost the ability to communicate."),
    ("04", "Neuropsychiatric symptoms", "Closed-loop neuromodulation for severe conditions such as major depression and chronic pain, pairing engineering with clinical neuroscience."),
]
focus_html = "".join(f"""<div class="focus__item reveal"><div class="focus__n">{n}</div><div class="focus__t">{t}</div><div class="focus__d">{d}</div></div>""" for n, t, d in focus_items)
strip = "".join(f'<div>{img_face(s, "", 1.0, loading="lazy")}</div>' for _, s, _ in (FACULTY_UCB[2:6] + FACULTY_UCSF[5:9]))

home = f"""
<section class="hero container">
  <div class="hero__grid">
    <div>
      <div class="eyebrow mono">Center for Neural Engineering &amp; Prostheses &middot; UC Berkeley &middot; UCSF</div>
      <h1 class="display">Engineering technology to restore function for people with neurological disabilities.</h1>
    </div>
    <div class="hero__aside">
      <p>The {SITE} is a collaborative enterprise of UCSF and the University of California, Berkeley. The center brings together experts in engineering, neurology and neurosurgery to develop state-of-the-art biomedical technology to restore function for patients with neurological disabilities such as paralysis and speech disorders.</p>
      <div class="btn-row"><a class="btn btn--solid" href="about.html">About the center {ARR}</a><a class="btn" href="faculty.html">Meet the faculty</a></div>
    </div>
  </div>
  <div class="hero-media reveal">
    <figure>
      <div class="frame frame--neuro">{hero_graphic()}</div>
      <figcaption><span class="mono">Multi-channel cortical recording over an electrode array</span><span class="mono">Illustration</span></figcaption>
    </figure>
  </div>
</section>

<section class="container section--tight">
  <div class="stats reveal">
    <div class="stat"><div class="mono stat__k">Founded</div><div class="stat__n">2010</div><div class="stat__s">Berkeley &amp; San Francisco</div></div>
    <div class="stat"><div class="mono stat__k">Campuses</div><div class="stat__n stat__n--text">UC Berkeley<br><span class="stat__amp">&amp;</span> UCSF</div><div class="stat__s">Two campuses, one community</div></div>
    <div class="stat"><div class="mono stat__k">Faculty</div><div class="stat__n">{N_FACULTY}</div><div class="stat__s">Engineers, neuroscientists and clinicians</div></div>
    <div class="stat"><div class="mono stat__k">Annual meeting</div><div class="stat__n">100<span class="stat__plus">+</span></div><div class="stat__s">Participants, January 2026</div></div>
  </div>
</section>

<section class="container section">
  <div class="section-head">
    <div><div class="eyebrow mono">What we work on</div><h2 class="h2">Restoring sensory, motor and cognitive function.</h2></div>
    <p class="lede aside">Across our projects we apply the latest approaches in data science, electrical engineering, neuroscience, and an array of clinical specialties to develop ground-breaking solutions for patients.</p>
  </div>
  <div class="focus">{focus_html}</div>
</section>

<section class="band section">
  <div class="container">
    <div class="split">
      <div>
        <div class="eyebrow mono">Our model</div>
        <h2 class="h2">Engineering and clinical neuroscience, side by side.</h2>
        <p class="lede" style="margin-top:1.5rem">Since its inception in 2010, CNEP has supported an unparalleled community of collaborative neural engineering researchers across UCSF and UC Berkeley. We foster cross-disciplinary collaborations, enable data and technology exchanges, and support top-tier training for the next generation of neural engineering innovators.</p>
        <div class="btn-row"><a class="btn btn--light-solid" href="about.html">More about our model {ARR}</a><a class="btn btn--light" href="annual-meeting.html">Annual meeting</a></div>
      </div>
      <div class="collage reveal">
        <div class="frame"><img src="assets/meeting/meeting-02.webp" alt="" loading="lazy"></div>
        <div class="frame"><img src="assets/meeting/meeting-05.webp" alt="" loading="lazy"></div>
        <div class="frame"><img src="assets/meeting/meeting-08.webp" alt="" loading="lazy"></div>
      </div>
    </div>
  </div>
</section>

<section class="container section">
  <div class="section-head">
    <div><div class="eyebrow mono">Leadership</div><h2 class="h2">Co-directed from both campuses.</h2></div>
    <div class="aside"><a class="link" href="leadership.html">Read the full biographies {ARR}</a></div>
  </div>
  <div class="grid grid-2 reveal">
    <a class="leader-card" href="leadership.html#chang">
      <div class="person__photo">{img_face("edward-chang-lead", "Edward Chang", 0.8, loading="lazy")}</div>
      <div><div class="h3">Edward Chang, MD</div><div class="mono person__meta">Co-Director &middot; UCSF</div><p class="muted small" style="margin-top:.6rem">Chair of Neurological Surgery at UCSF and a founding director of CNEP. Pioneer of real-time speech decoding through brain-computer interfaces.</p><span class="link small" style="margin-top:.6rem">Biography {ARR}</span></div>
    </a>
    <a class="leader-card" href="leadership.html#yartsev">
      <div class="person__photo">{img_face("michael-yartsev-lead", "Michael Yartsev", 0.8, loading="lazy")}</div>
      <div><div class="h3">Michael Yartsev, PhD</div><div class="mono person__meta">Co-Director &middot; UC Berkeley</div><p class="muted small" style="margin-top:.6rem">Howard Hughes Medical Institute Investigator and associate professor of Bioengineering and Neuroscience at UC Berkeley.</p><span class="link small" style="margin-top:.6rem">Biography {ARR}</span></div>
    </a>
  </div>
</section>

<section class="container section section--rule">
  <div class="section-head">
    <div><div class="eyebrow mono">Faculty</div><h2 class="h2">A world-class team.</h2></div>
    <p class="lede aside">More than two dozen faculty members from top institutions collaborating to harness the power of the human brain.</p>
  </div>
  <div class="avatar-strip reveal">{strip}</div>
  <div class="btn-row"><a class="btn" href="faculty.html">All {N_FACULTY} faculty {ARR}</a></div>
</section>

<section class="band--olive band section">
  <div class="container">
    <div class="split split--rev">
      <div class="frame reveal" style="aspect-ratio:4/3"><img src="assets/meeting/meeting-01.webp" alt="Attendees at the 2026 CNEP annual meeting" loading="lazy"></div>
      <div>
        <div class="eyebrow mono">Annual meeting &middot; January 16, 2026</div>
        <h2 class="h2">One community, two campuses, one room.</h2>
        <p class="lede" style="margin-top:1.5rem">CNEP's annual meetings bring together a dynamic community of researchers, engineers, clinicians, and trainees from UC Berkeley and UCSF to share ideas and spark new collaborations. At our most recent gathering, over 100 participants came together to present work spanning basic science, cutting-edge engineering, and translational neuroscience.</p>
        <div class="btn-row"><a class="btn" href="annual-meeting.html">About the meeting {ARR}</a></div>
      </div>
    </div>
  </div>
</section>

<section class="container section">
  <div class="section-head">
    <div><div class="eyebrow mono">Tools &amp; resources</div><h2 class="h2">For our community of innovators.</h2></div>
    <div class="aside"><a class="link" href="resources.html">All resources {ARR}</a></div>
  </div>
  <div class="rlist reveal">
    {"".join(f'<a class="rrow" href="{u}" rel="noopener"><div class="rrow__n">{i:02d}</div><div><div class="rrow__t">{t}</div><span class="mono rrow__o">{o}</span></div><div class="rrow__d">{e(d)}</div><span class="link rrow__l">Visit {ARR}</span></a>' for i,(t,o,u,d) in enumerate(RESOURCES[:4],1))}
  </div>
</section>

<section class="band section">
  <div class="container cta">
    <div><div class="eyebrow mono">Support CNEP</div><h2 class="h2">Endow the next breakthrough.</h2><p class="lede" style="margin-top:1.25rem">Your gift will endow leading-edge collaborations among the best researchers to support breakthrough treatments and technologies.</p></div>
    <div class="btn-row"><a class="btn btn--light-solid" href="donate.html">Discuss what's possible {ARR}</a></div>
  </div>
</section>
"""
page("index.html", "Home", f"The {SITE} is a collaborative enterprise of UCSF and UC Berkeley developing technology to restore function for patients with neurological disabilities.", home)

# ------------------------------------------------------------------ ABOUT
about = page_head("About", "A collaborative enterprise of UCSF and UC Berkeley.",
    "Since its inception in 2010, CNEP has supported an unparalleled community of collaborative neural engineering researchers across UCSF and UC Berkeley.") + f"""
<section class="container">
  <figure class="reveal" style="margin:0">
    <div class="frame" style="aspect-ratio:16/8"><img src="assets/img/about-participant.webp" alt="A research participant in a wheelchair watches a screen showing a digital avatar during a brain-computer interface session." width="1884" height="1266"></div>
    <figcaption class="mono" style="padding-top:.75rem">Credit: Noah Berger / UCSF</figcaption>
  </figure>
</section>
<section class="container section">
  <div class="split" style="align-items:start">
    <div><div class="eyebrow mono">Mission</div><h2 class="h2">Integrating cutting-edge engineering with world-class basic and clinical neuroscience.</h2></div>
    <div class="lede">
      <p>The Center's focus is on integrating cutting-edge engineering with world-class basic and clinical neurosciences to develop technology that helps patients suffering from disabling neurological conditions. We foster cross-disciplinary collaborations, enable data and technology exchanges, and support top-tier training for the next generation of neural engineering innovators.</p>
      <p>Across our projects &mdash; including efforts to restore sensory, motor and cognitive function, as well as programs focused on relieving neuropsychiatric symptoms &mdash; we apply the latest approaches in data science, electrical engineering, neuroscience, and an array of clinical specialties to develop ground-breaking solutions for patients.</p>
    </div>
  </div>
</section>
<section class="container section section--rule">
  <div class="section-head"><div><div class="eyebrow mono">How we work</div><h2 class="h2">Three commitments.</h2></div></div>
  <div class="focus">
    <div class="focus__item reveal"><div class="focus__n">01</div><div class="focus__t">Cross-disciplinary collaboration</div><div class="focus__d">Engineers, neuroscientists, neurologists and neurosurgeons working on shared problems, from the bench to the bedside, across both campuses.</div></div>
    <div class="focus__item reveal"><div class="focus__n">02</div><div class="focus__t">Data and technology exchange</div><div class="focus__d">Sharing devices, datasets, regulatory know-how and open-source tooling so that progress in one lab accelerates progress in all of them.</div></div>
    <div class="focus__item reveal"><div class="focus__n">03</div><div class="focus__t">Training the next generation</div><div class="focus__d">Top-tier training for students, postdocs and clinical fellows who will become the next generation of neural engineering innovators.</div></div>
  </div>
</section>
<section class="band section">
  <div class="container cta">
    <div><div class="eyebrow mono">People</div><h2 class="h2">{N_FACULTY} faculty across UC Berkeley and UCSF.</h2></div>
    <div class="btn-row"><a class="btn btn--light-solid" href="faculty.html">Meet the faculty {ARR}</a><a class="btn btn--light" href="leadership.html">Leadership</a></div>
  </div>
</section>
"""
page("about.html", "About", "CNEP integrates cutting-edge engineering with basic and clinical neuroscience to develop technology for patients with disabling neurological conditions.", about)

# ------------------------------------------------------------------ LEADERSHIP
leadership = page_head("Leadership", "Co-directed from both campuses.",
    "CNEP is led jointly by a neurosurgeon-scientist at UCSF and a systems neuroscientist and engineer at UC Berkeley.") + f"""
<section class="container">
  <article class="leader reveal" id="chang">
    <div><div class="person__photo">{img_face("edward-chang-lead", "Edward Chang", 0.8)}</div></div>
    <div class="leader__bio">
      <div class="mono" style="margin-bottom:.75rem">Co-Director &middot; UCSF</div>
      <h2 class="leader__name">Edward Chang, MD</h2>
      <div style="margin-top:1.5rem">
      <p>A founding director of CNEP, Dr. Edward Chang is Department Chair for Neurological Surgery at UCSF. His wide-ranging and impactful research has revealed critical aspects of the brain's ability to understand and produce language, and he has helped to pioneer real-time decoding of the brain's speech signals through brain-computer interfaces for those who have lost the ability to communicate. His research program has also helped to advance closed-loop neuromodulation approaches for the treatment of severe neuropsychiatric disorders such as major depression and chronic pain.</p>
      <p>As a neurosurgeon, Dr. Chang's clinical focus includes difficult-to-control epilepsy, brain tumors, trigeminal neuralgia, and movement disorders, with specialist expertise in advanced brain mapping methods to preserve crucial areas for speech and motor functions in the brain. He also has extensive experience with implantable neuromodulation devices to relieve seizure, movement, pain and other disorders.</p>
      <p>Dr. Chang earned his medical degree at UCSF, where he also completed a residency in neurosurgery. He was honored with the Blavatnik National Laureate for Life Sciences in 2015. In 2020, he was elected to the National Academy of Medicine, an honor that recognizes outstanding achievements and service in the fields of medical sciences, health care and public health.</p>
      </div>
      <div class="btn-row"><a class="btn" href="https://changlab.ucsf.edu" rel="noopener">Chang Lab {ARR}</a></div>
    </div>
  </article>
  <article class="leader reveal" id="yartsev">
    <div><div class="person__photo">{img_face("michael-yartsev-lead", "Michael Yartsev", 0.8)}</div></div>
    <div class="leader__bio">
      <div class="mono" style="margin-bottom:.75rem">Co-Director &middot; UC Berkeley</div>
      <h2 class="leader__name">Michael Yartsev, PhD</h2>
      <div style="margin-top:1.5rem">
      <p>Dr. Michael Yartsev is a Howard Hughes Medical Institute Investigator and associate professor of Bioengineering and Neuroscience at UC Berkeley. His research focuses on understanding the neural basis of natural spatial, social and acoustic capabilities in mammals, taking on investigations across multiple modalities of learning, information processing and complex behavior.</p>
      <p>Working with an ideal model system for such questions, the bat, Dr. Yartsev's research has pioneered a wide range of technologies for monitoring and manipulating neural activity in freely behaving animals &mdash; including wireless neurophysiology and wireless calcium imaging &mdash; to advance a detailed understanding of neural computations that enable complex behavior and learning. By taking a neuroethological approach to such advanced behaviors as spatial memory formation, precision navigation, communication and other interactions underpinning social groups, his research aims to uncover core principles of brain function that subserve complex natural behaviors in the mammalian brain.</p>
      <p>Dr. Yartsev completed his B.Sc. and M.Sc. in Biomedical Engineering at Ben-Gurion University in 2007, and received his Ph.D. in Neuroscience from the Weizmann Institute. He was subsequently a C.V. Starr fellow in neuroscience in the Princeton Neuroscience Institute, where he completed a post-doc in the laboratory of Carlos Brody. He holds a joint appointment in the departments of Bioengineering and Neuroscience at Berkeley.</p>
      </div>
      <div class="btn-row"><a class="btn" href="https://www.michaelyartsev.com/" rel="noopener">Yartsev Lab {ARR}</a></div>
    </div>
  </article>
</section>
"""
page("leadership.html", "Leadership", "CNEP is co-directed by Edward Chang, MD (UCSF) and Michael Yartsev, PhD (UC Berkeley).", leadership)

# ------------------------------------------------------------------ FACULTY
def group(title, inst, members):
    cards = "".join(person_card(n, s, u, inst) for n, s, u in members)
    return f"""<section class="container faculty-group" id="{inst.lower().replace(' ','-')}">
  <div class="faculty-group__head"><h2 class="h3">{title}</h2><span class="mono">{len(members)} faculty</span></div>
  <div class="faculty-grid reveal">{cards}</div>
</section>"""
faculty = page_head("Faculty", "A world-class team.",
    "More than two dozen faculty members from top institutions collaborating to harness the power of the human brain.",
    f'<div class="mono" style="margin-bottom:.75rem">Jump to</div><div class="btn-row" style="margin-top:0"><a class="btn" href="#uc-berkeley">UC Berkeley &middot; {len(FACULTY_UCB)}</a><a class="btn" href="#ucsf">UCSF &middot; {len(FACULTY_UCSF)}</a></div>') \
    + group("University of California, Berkeley", "UC Berkeley", FACULTY_UCB) \
    + group("University of California, San Francisco", "UCSF", FACULTY_UCSF)
page("faculty.html", "Faculty", f"{N_FACULTY} CNEP faculty members across UC Berkeley and UCSF.", faculty)

# ------------------------------------------------------------------ MEETING
photos = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15"]
wide = {"02","08","13"}
gal = "".join(f'<div class="frame{" wide" if p in wide else ""}"><img src="assets/meeting/meeting-{p}.webp" alt="Scene from the 2026 CNEP annual meeting" loading="lazy"></div>' for p in photos)
meeting = page_head("Annual meeting", "One community, two campuses, one room.",
    "CNEP's annual meetings bring together a dynamic community of researchers, engineers, clinicians, and trainees from UC Berkeley and UCSF to share ideas and spark new collaborations.",
    f"""<div class="mono" style="margin-bottom:.75rem">Most recent</div><div class="h3" style="color:var(--navy)">2026 CNEP Meeting</div><div class="mono" style="margin-top:.4rem">January 16, 2026 &middot; 100+ participants</div>""") + f"""
<section class="container">
  <div class="gallery reveal">{gal}</div>
</section>
<section class="container section">
  <div class="split" style="align-items:start">
    <div><div class="eyebrow mono">January 16, 2026</div><h2 class="h2">Basic science, cutting-edge engineering and translational neuroscience.</h2></div>
    <div class="lede">
      <p>At our most recent gathering on January 16th, 2026, over 100 participants came together to present and discuss work spanning basic science, cutting-edge engineering, and translational neuroscience.</p>
      <p>The meeting highlighted both the breadth of ongoing research and the collaborative spirit that defines CNEP, providing a forum for open exchange, new connections, and shaping the future direction of the center.</p>
    </div>
  </div>
</section>
"""
page("annual-meeting.html", "Annual Meeting", "CNEP's annual meeting brings together researchers, engineers, clinicians and trainees from UC Berkeley and UCSF.", meeting)

# ------------------------------------------------------------------ RESOURCES
rows = "".join(f"""<a class="rrow reveal" href="{u}" rel="noopener"><div class="rrow__n">{i:02d}</div><div><div class="rrow__t">{t}</div><span class="mono rrow__o">{o}</span></div><div class="rrow__d">{e(d)}</div><span class="link rrow__l">Visit {ARR}</span></a>""" for i,(t,o,u,d) in enumerate(RESOURCES,1))
resources = page_head("Tools &amp; resources", "For our community of innovators.",
    "Engineering, regulatory, commercialization and ethics resources curated for neural engineering teams at UC Berkeley, UCSF and beyond.") + f"""
<section class="container"><div class="rlist">{rows}</div></section>
<section class="container section">
  <div class="contact-card measure-wide">
    <div class="mono" style="margin-bottom:.75rem">Suggest a resource</div>
    <p class="lede">Know of a tool, dataset or program that should be listed here? <a class="link" href="donate.html#inquiry">Send us a message <span class="arr" aria-hidden="true">&rarr;</span></a></p>
  </div>
</section>
"""
page("resources.html", "Tools & Resources", "Engineering, regulatory and commercialization resources for the CNEP community.", resources)

# ------------------------------------------------------------------ DONATE
donate = f"""
<section class="page-head container">
  <div class="page-head__grid page-head__grid--form">
    <div>
      <div class="eyebrow mono">Support CNEP</div>
      <h1 class="display">Discuss what's possible.</h1>
      <p class="lede">Interested in joining our community of supporters? Your gift will endow leading-edge collaborations among the best researchers to support breakthrough treatments and technologies.</p>
      <blockquote style="margin-top:2.5rem">It is important to us that your gift supports the cause that inspires you.</blockquote>
      <p style="margin-top:1.5rem;color:var(--ink-2)">Whether that is fellowships for education and training, research, or the most pressing needs identified by the Center &mdash; reach out to us directly to talk with our leadership.</p>
    </div>
    {inquiry_form("Discuss what's possible with our leadership.", "Tell us a little about yourself and what you have in mind. Messages go directly to the Center's co-directors.")}
  </div>
</section>
<section class="container section section--rule">
  <div class="section-head"><div><div class="eyebrow mono">Where gifts go</div><h2 class="h2">Three ways to give.</h2></div></div>
  <div class="focus">
    <div class="focus__item reveal"><div class="focus__n">01</div><div class="focus__t">Fellowships</div><div class="focus__d">Education and training support for the students, postdocs and clinical fellows who will become the next generation of neural engineering innovators.</div></div>
    <div class="focus__item reveal"><div class="focus__n">02</div><div class="focus__t">Research</div><div class="focus__d">Seed and sustain collaborations between engineers and clinicians aimed at restoring sensory, motor and cognitive function.</div></div>
    <div class="focus__item reveal"><div class="focus__n">03</div><div class="focus__t">The Center's most pressing needs</div><div class="focus__d">Flexible support directed by CNEP's leadership to where it will have the greatest impact.</div></div>
  </div>
</section>
"""
page("donate.html", "Support CNEP", "Support the Center for Neural Engineering & Prostheses.", donate)

# ------------------------------------------------------------------ 404
page("404.html", "Page not found", "That page could not be found.", f"""
<section class="page-head container"><div class="eyebrow mono">404</div><h1 class="display">That page isn't here.</h1>
<p class="lede">The address may have changed. Try one of the pages below.</p>
<div class="btn-row"><a class="btn btn--solid" href="index.html">Home {ARR}</a><a class="btn" href="faculty.html">Faculty</a><a class="btn" href="resources.html">Tools &amp; Resources</a></div></section>
""")
