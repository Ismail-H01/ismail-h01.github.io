# Ismail Hussain: portfolio

Personal portfolio site, live at **https://ismail-h01.github.io**. Plain HTML, CSS and JavaScript: no framework, no build step, no trackers. Hosted free on GitHub Pages.

## Structure

```
index.html            Page content (all sections, JSON-LD, meta tags)
css/site.css          Styles, dark and light themes, print styles
js/site.js            Enhancements only: theme, reveal, counters, lightbox, skills filter, hero animation
404.html              Not-found page
robots.txt, sitemap.xml, .nojekyll
assets/img/           Photos, figures, favicons, social share image
assets/docs/          CV (PDF) and the EE3PEC paper (PDF)
tools/build_cv.py     Regenerates the CV PDF
tools/build_og.py     Regenerates the 1200x630 share image
tests/                pytest + Playwright + axe tests
docs/                 EDITING.md and CONTENT-SOURCES.md
.github/workflows/    CI: runs the tests on every push
```

Section order (the page's story): Hero, Highlights, About, Work, Experience (with education and membership), Skills, Leadership and outreach, Contact.

## Features

- Sticky nav with active-section highlighting, mobile menu, scroll progress bar. Opens in dark mode; the light theme is one click away and the choice is remembered.
- Motion system, all disabled under `prefers-reduced-motion`:
  - hero name rises letter by letter out of a mask; the rest of the hero fades and un-blurs in sequence;
  - hero drifts up and fades on scroll (parallax), with the animated PCB-trace canvas moving at a slower rate;
  - section headings reveal word by word; the About statement lights up word by word as you scroll;
  - a keyword marquee that speeds up with scroll velocity;
  - project and leadership cards unclip and rise; highlights stagger in; counters count up;
  - the experience timeline draws as you scroll, lighting each point it reaches, and the Amey delivery steps play in order;
  - gallery images wipe in when a drop-down opens; the lightbox zooms in.
- Project cards with drop-down photo and figure galleries and a keyboard-friendly lightbox.
- Skills chips that jump to the projects where each skill was used.
- Works without JavaScript (content visible, galleries open). Print stylesheet included.
- SEO and sharing: canonical, Open Graph and Twitter tags, JSON-LD `Person`, sitemap, robots, 1200x630 share image.
- Email address is assembled by JavaScript, not written in the page source.

## Run and test locally

```bash
python3 -m http.server 8000          # then open http://localhost:8000
pip install pytest playwright axe-playwright-python pypdf pillow
python3 -m pytest tests -q           # local server is started automatically
python3 -m pytest tests -q --base-url https://ismail-h01.github.io   # test the live site
```

The browser tests expect Google Chrome at `/usr/bin/google-chrome`; otherwise Playwright's own Chromium is used (`playwright install chromium`).

## What the tests guard

Required facts present (degree, MIET, roles, key figures); nothing unfinished or confidential-looking; every local file, anchor and `aria-controls` resolves; every image has alt text and dimensions; every skill chip maps to a project; JSON-LD valid; CV is one page; no horizontal scroll at 390 px or 1440 px in either theme; all interactions work (nav, theme, drop-downs, lightbox, skills, mobile menu); no-JS fallback; WCAG 2 A/AA axe scans in both themes.

## Adding a photo

See `docs/EDITING.md`, "Add a profile photo".

## Deploy

GitHub Pages serves the `main` branch root. Commit and push (or upload through the GitHub web interface); the "pages build and deployment" action publishes in about a minute. See `docs/EDITING.md` for common edits.

## Content rules

Renishaw content stays general: no part numbers, product or customer internals, or cost figures, and no claim that the test jig was deployed. Results are reported as measured, including failures. See `docs/CONTENT-SOURCES.md` for where each claim comes from.
