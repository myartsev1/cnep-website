# CNEP website redesign

Static redesign of https://www.uc-cnep.org/ for the Center for Neural Engineering & Prostheses (UC Berkeley · UCSF).
Standalone: no shared code or assets with any other site.

## Files
- `build.py` — single source of truth for all page content (nav, faculty list, resources, bios). Run `python3 build.py` to regenerate the HTML.
- `index.html`, `about.html`, `leadership.html`, `faculty.html`, `annual-meeting.html`, `resources.html`, `donate.html` — generated pages.
- `css/style.css` — design system (colors, type, layout).
- `js/main.js` — mobile menu toggle and scroll-reveal.
- `assets/` — photos pulled from the current CNEP site (`people/`, `meeting/`, `img/`), saved as WebP.

## Preview locally
```bash
python3 -m http.server 8765
```
then open http://localhost:8765/

## Deploy
Any static host works (GitHub Pages, Netlify, Cloudflare Pages). Upload the whole folder.
