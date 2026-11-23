# Editing guide

All content is in `index.html`. After any edit run `python3 -m pytest tests -q`.

## Change text
Search `index.html` for the sentence and edit it. Keep copy short and plain. Avoid em dashes (a test checks).

## Add a project
Copy a whole `<article class="card reveal" ...>` block in the `#work` section, then change:
1. `id` (e.g. `p-newproject`) and `aria-labelledby`/title `id`.
2. `data-skills` to the skill keys used (must match `data-skill` keys in the Skills section).
3. The number, period, title, summary, bullets, results and facts.
4. For a photo drop-down: put images in `assets/img/`, give each `<img>` real `width`, `height` and descriptive `alt`, and use unique `aria-controls`/`id` pairs (`drop-xyz`) and a unique `data-gallery` name.
Remove the `.actions` block if there is no drop-down or download.

## Add a skill
Add `<button type="button" class="skill" data-skill="key" aria-pressed="false">Label</button>` in the right group, then add `key` to the `data-skills` of every card or timeline item that used it. A test fails if a chip has no project.

## Add a role or credential
Copy a `<li class="role-card reveal">` (Leadership) or `<li class="reveal">` (credentials). Update the Highlights number ("leadership, mentoring and outreach roles") if the count changes, and the `data-count`.

## Update the CV
Edit the content block at the top of `tools/build_cv.py`, then `python3 tools/build_cv.py`. The script writes `assets/docs/Ismail-Hussain-CV.pdf` (must stay one page; a test checks).

## Replace the paper or images
Overwrite the file in `assets/` with the same name. Keep the 1200x630 share image size.

## Colours and theme
Variables are at the top of `css/site.css` (`:root` for dark, `[data-theme="light"]`). The axe test checks contrast in both themes.

## Domain
The site URL is `https://ismail-h01.github.io/`. If it changes, update the canonical, Open Graph, JSON-LD, `robots.txt` and `sitemap.xml`.
