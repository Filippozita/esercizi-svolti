"""Dopo i build: link ai calcolatori in home e pagine materia, sitemap completa, JSON-LD su ogni pagina."""
import json
import re
from datetime import date

import build_sito as S
from build_calcolatori import CALC

calc_html = "<h2>Calcolatori gratis</h2><div class='cards'>" + "".join(
    f"<div class='card'><a href='{c['slug']}.html'>{c['title'].split(' (')[0]}</a><p>{c['desc'][:110]}…</p></div>" for c in CALC) + "</div>"
idx = S.OUT / "index.html"
h = idx.read_text(encoding="utf-8")
if "Calcolatori gratis" not in h:
    idx.write_text(h.replace("<div class='cta'>", calc_html + "<div class='cta'>", 1), encoding="utf-8")

# link calcolatore pertinente in ogni pagina materia
rel = {"partita-doppia-esercizi-svolti": ["calcolo-iva-scorporo-22"],
       "matematica-finanziaria-esercizi-svolti": ["calcolo-rata-mutuo-ammortamento-francese", "calcolo-interesse-composto-montante"],
       "statistica-esercizi-svolti": ["calcolatore-media-varianza-deviazione-standard"]}
tit = {c["slug"]: c["title"].split(" (")[0] for c in CALC}
for p, cs in rel.items():
    f = S.OUT / f"{p}.html"
    h = f.read_text(encoding="utf-8")
    if "Prova il calcolatore" not in h:
        box = "<div class='box'><b>Prova il calcolatore:</b> " + " · ".join(f"<a href='{s}.html'>{tit[s]}</a>" for s in cs) + "</div>"
        f.write_text(h.replace("<h2>1.", box + "<h2>1.", 1), encoding="utf-8")

pages = sorted(p for p in S.OUT.glob("*.html") if not p.name.startswith("google"))
urls = [S.BASE + ("" if p.name == "index.html" else p.name) for p in pages]
(S.OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                                   + "".join(f"<url><loc>{u}</loc><lastmod>{date.today().isoformat()}</lastmod></url>" for u in urls) + "</urlset>", encoding="utf-8")

for p, u in zip(pages, urls):
    h = p.read_text(encoding="utf-8")
    if "application/ld+json" in h:
        continue
    title = re.search(r"<title>(.*?)</title>", h).group(1)
    desc = re.search(r'<meta name="description" content="(.*?)">', h).group(1)
    typ = "WebApplication" if any(c["slug"] in p.name for c in CALC) else "LearningResource"
    ld = {"@context": "https://schema.org", "@type": typ, "name": title, "description": desc, "url": u,
          "inLanguage": "it", "isAccessibleForFree": True}
    if typ == "WebApplication":
        ld.update(applicationCategory="EducationalApplication", operatingSystem="Any",
                  offers={"@type": "Offer", "price": "0", "priceCurrency": "EUR"})
    else:
        ld.update(educationalLevel="Scuola superiore e università", learningResourceType="Esercizi svolti")
    h = h.replace("</head>", f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script></head>', 1)
    p.write_text(h, encoding="utf-8")
(S.ROOT / "tutti_url.txt").write_text("\n".join(urls))
print(len(urls), "pagine in sitemap")
