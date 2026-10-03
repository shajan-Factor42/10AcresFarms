#!/usr/bin/env python3
"""Pre-launch check for 10acrefarms.com. Run before every push:  python3 scripts/check.py
Exits non-zero if anything must be fixed. Warnings are things to know about, not blockers.
Checks: internal links & assets, titles, meta descriptions, H1s, canonicals, schema JSON,
sitemap vs pages, robots, forms, analytics tag, page weight, header/footer consistency."""
import json, os, re, sys
from html.parser import HTMLParser
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://10acrefarms.com"
errors, warns = [], []
BANNED = ["organic", "pasture-raised", "pasture raised", "hormone-free", "antibiotic-free", "certified humane"]

class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.links=[]; s.h1=0; s.title=""; s._t=False; s.meta={}; s.canon=None
        s.ld=[]; s._ld=False; s.forms=[]; s.ids=set(); s.text=[]; s._skip=False; s.imgs_noalt=0
    def handle_starttag(s, tag, a):
        a = dict(a)
        if "id" in a: s.ids.add(a["id"])
        if tag == "a" and "href" in a: s.links.append(a["href"])
        if tag in ("link",) and a.get("rel") in ("stylesheet","icon","apple-touch-icon"): s.links.append(a["href"])
        if tag == "script" and "src" in a: s.links.append(a["src"])
        if tag == "img":
            s.links.append(a.get("src",""))
            if not a.get("alt"): s.imgs_noalt += 1
        if tag == "h1": s.h1 += 1
        if tag == "title": s._t = True
        if tag == "meta" and "name" in a: s.meta[a["name"]] = a.get("content","")
        if tag == "meta" and "property" in a: s.meta[a["property"]] = a.get("content","")
        if tag == "link" and a.get("rel") == "canonical": s.canon = a.get("href")
        if tag == "script" and a.get("type") == "application/ld+json": s._ld = True; s.ld.append("")
        if tag == "form": s.forms.append({"action": a.get("action"), "method": (a.get("method") or "").upper(), "fields": []})
        if tag in ("input","textarea","select") and s.forms: s.forms[-1]["fields"].append(a.get("name"))
        if tag in ("script","style"): s._skip = True
    def handle_endtag(s, tag):
        if tag == "title": s._t = False
        if tag == "script": s._ld = False
        if tag in ("script","style"): s._skip = False
    def handle_data(s, d):
        if s._t: s.title += d
        if s._ld: s.ld[-1] += d
        elif not s._skip: s.text.append(d)
    def handle_comment(s, d): pass

pages = {}
for dp, dn, fn in os.walk(ROOT):
    dn[:] = [d for d in dn if not d.startswith(".") and d not in ("scripts","node_modules")]
    for f in fn:
        if f.endswith(".html"):
            full = os.path.join(dp, f); rel = os.path.relpath(full, ROOT)
            src = open(full, encoding="utf-8").read(); p = P(); p.feed(src); pages[rel] = (p, src)

def url_for(rel):
    if rel == "404.html": return None
    return SITE + "/" + rel[:-len("index.html")]

titles, descs = {}, {}
for rel, (p, src) in sorted(pages.items()):
    noindex = "noindex" in p.meta.get("robots","")
    # links & assets
    for href in p.links:
        if not href or href.startswith(("mailto:","tel:","#","javascript:")): continue
        u = urlparse(href)
        if u.scheme in ("http","https"):
            if u.netloc.endswith("10acrefarms.com"): errors.append(f"{rel}: absolute link to own site {href} (use relative)")
            continue
        if rel == "404.html" and href.startswith("/"): target = os.path.join(ROOT, u.path.lstrip("/"))
        else: target = os.path.normpath(os.path.join(ROOT, os.path.dirname(rel), u.path))
        if os.path.isdir(target): target = os.path.join(target, "index.html")
        if not os.path.exists(target): errors.append(f"{rel}: broken link -> {href}")
        elif u.fragment and target.endswith(".html"):
            tp = pages.get(os.path.relpath(target, ROOT))
            if tp and u.fragment not in tp[0].ids: errors.append(f"{rel}: missing anchor #{u.fragment} in {href}")
    # head
    t = p.title.strip()
    if not t: errors.append(f"{rel}: no <title>")
    elif len(t) > 60: warns.append(f"{rel}: title is {len(t)} chars (aim <= 60): {t}")
    d = p.meta.get("description","")
    if not d: errors.append(f"{rel}: no meta description")
    elif len(d) > 160: warns.append(f"{rel}: description is {len(d)} chars (aim <= 160)")
    if not noindex:
        if t in titles: errors.append(f"{rel}: duplicate title with {titles[t]}")
        titles[t] = rel
        if d in descs: errors.append(f"{rel}: duplicate description with {descs[d]}")
        descs[d] = rel
    if p.h1 != 1: errors.append(f"{rel}: has {p.h1} H1 tags (need exactly 1)")
    if 'name="viewport"' not in src: errors.append(f"{rel}: missing mobile viewport tag")
    exp = url_for(rel)
    if exp and p.canon != exp: errors.append(f"{rel}: canonical {p.canon} != {exp}")
    for k in ("og:title","og:description","og:image"):
        if k not in p.meta: warns.append(f"{rel}: missing {k}")
    for i, block in enumerate(p.ld):
        try:
            j = json.loads(block)
            if "@context" not in j or "@type" not in j: errors.append(f"{rel}: schema #{i+1} missing @context/@type")
        except Exception as e: errors.append(f"{rel}: schema #{i+1} is not valid JSON ({e})")
    if p.imgs_noalt: errors.append(f"{rel}: {p.imgs_noalt} image(s) without alt text")
    # forms
    for f in p.forms:
        if not f["action"] or f["method"] != "POST": errors.append(f"{rel}: form missing action or not POST")
        if "_honey" not in f["fields"]: warns.append(f"{rel}: form has no spam trap (_honey)")
        if "_next" not in f["fields"]: warns.append(f"{rel}: form has no thank-you redirect (_next)")
    # claims (D-005): banned words in visible text, except where we explicitly say we're NOT organic
    text = " ".join(p.text).lower()
    for w in BANNED:
        for m in re.finditer(re.escape(w), text):
            ctx = text[max(0, m.start()-40): m.end()+5]
            if text[m.end():m.end()+1] == "?": continue  # a question like "Are your eggs organic?"
            if not re.search(r"\b(not|no|isn't|aren't|won't)\b[^.]*$", ctx.split(w)[0]):
                errors.append(f"{rel}: claim '{w}' used without a negation — check DECISIONS.md D-005: ...{ctx}...")
    # analytics
    if "googletagmanager.com/gtag" not in src and "<!-- ANALYTICS" in src: pass
    # weight
    kb = len(src.encode()) / 1024
    if kb > 100: warns.append(f"{rel}: HTML is {kb:.0f} KB")

if not any("googletagmanager.com/gtag" in s for _, s in pages.values()):
    warns.append("Analytics: GA4 not installed yet (D-012)")

# header/footer consistency (normalize relative prefixes)
def chunk(src, a, b):
    m = re.search(a + r".*?" + b, src, re.S); return re.sub(r'(href|src)="/', r'\1="', re.sub(r'(\.\./)+', '', m.group(0))) if m else ""
def norm(s): return re.sub(r'\s*aria-current="page"', "", s).replace('href="./"', 'href=""')
ref = pages.get("index.html")
if ref:
    h0 = norm(chunk(ref[1], "<header", "</header>")); f0 = norm(chunk(ref[1], "<footer", "</footer>"))
    for rel, (p, src) in pages.items():
        if norm(chunk(src, "<header", "</header>")) != h0: warns.append(f"{rel}: header differs from home page")
        if norm(chunk(src, "<footer", "</footer>")) != f0: warns.append(f"{rel}: footer differs from home page")

# sitemap
sm = open(os.path.join(ROOT, "sitemap.xml")).read()
locs = re.findall(r"<loc>(.*?)</loc>", sm)
indexable = {url_for(r) for r, (p, _) in pages.items() if url_for(r) and "noindex" not in p.meta.get("robots","")}
for l in locs:
    if l not in indexable: errors.append(f"sitemap: {l} has no matching indexable page")
for u in indexable - set(locs): errors.append(f"sitemap: page {u} missing from sitemap")
rb = open(os.path.join(ROOT, "robots.txt")).read()
if "Sitemap:" not in rb: errors.append("robots.txt: no Sitemap line")
if re.search(r"Disallow:\s*/\s*$", rb, re.M): errors.append("robots.txt blocks the whole site!")

# asset weight
total = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fn in os.walk(os.path.join(ROOT, "assets")) for f in fn)
print(f"Pages: {len(pages)}   Sitemap URLs: {len(locs)}   Assets: {total/1024:.0f} KB")
for w in warns: print("WARN ", w)
for e in errors: print("ERROR", e)
print("PASS" if not errors else f"FAIL ({len(errors)} errors)")
sys.exit(1 if errors else 0)
