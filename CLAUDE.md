# 10acresfarms.com — working notes

Small family farm in Gwinnett County, GA selling cage-free, free-range chicken and duck eggs.

## Rules
- Read `DECISIONS.md` before any change. If a request conflicts with an entry, stop and say which one.
- Add a new entry to `DECISIONS.md` for every new design, content or technical decision (date + why).
- Pushing to `main` publishes the site (GitHub Pages). Never push without the owner's OK.
- Before every push run `python3 scripts/check.py` and fix every error.
- Product claims: see D-005. Never write "organic" or other unverified label claims.

## Layout
- Plain static HTML. Shared styles in `assets/css/site.css`, small script in `assets/js/site.js`.
- Header and footer are copied into each page (no build step). If you change one, change all — `scripts/check.py` warns when they drift.
- Blog posts live in `blog/<slug>/index.html`. Add each new post to `blog/index.html` and `sitemap.xml`.
- All internal links are relative.
