# 10acresfarms.com

Website for 10 Acre Farms — cage-free, free-range chicken and duck eggs, Lawrenceville (Gwinnett County), GA.

- Plain HTML/CSS, no build step. Hosted on GitHub Pages from `main` (pushing = publishing). Domain: 10acresfarms.com (keep the `CNAME` file).
- Read `DECISIONS.md` before changing anything. Only the website tech lead pushes to `main` (D-020).
- Before every push: `python3 scripts/check.py` must say PASS.
- Preview locally: `python3 -m http.server -d .` then open http://localhost:8000

## Still to do
- Real photos for the four tan photo slots (each has an HTML comment with the replacement `<img>` tag) and a real social share image.
- Farm email + social links in the footer (TODO comment in every page).
- Activate FormSubmit (click the link in the first email it sends), then swap the plain email in form actions for the FormSubmit alias.
- GA4 + Search Console (D-012).
- Owner to review the draft farm story.
