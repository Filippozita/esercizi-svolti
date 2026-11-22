"""Genera un sito statico (GitHub Pages) con teoria + primi esercizi svolti gratis di ogni dispensa,
e link alla versione completa su Payhip. Output in sito/docs/."""
import re
import secrets
from datetime import date
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).parent
SRC = ROOT.parent / "dispense" / "pdf"
OUT = ROOT / "docs"
OUT.mkdir(exist_ok=True)
BASE = "https://filippozita.github.io/esercizi-svolti/"
GRATIS = 3  # esercizi mostrati gratis per pagina

PAGINE = [
    ("partita-doppia-esercizi-svolti", "economia-aziendale-partita-doppia",
     "Partita doppia: esercizi svolti con soluzioni (Economia aziendale)",
     "Regole DARE/AVERE, IVA, assestamento e scritture svolte di partita doppia con tabella quadrata. Teoria ed esercizi gratis.",
     "https://payhip.com/b/ghBQW", "4,00 €", 10),
    ("matematica-finanziaria-esercizi-svolti", "matematica-finanziaria",
     "Matematica finanziaria: formulario ed esercizi svolti",
     "Interesse semplice e composto, tassi equivalenti, rendite, ammortamento francese e italiano, VAN e TIR: formule ed esercizi svolti gratis.",
     "https://payhip.com/b/WMrnJ", "3,90 €", 11),
    ("statistica-esercizi-svolti", "statistica-di-base",
     "Statistica di base: formulario ed esercizi svolti",
     "Media, mediana, varianza, quartili, probabilità, binomiale, normale e regressione: formule ed esercizi svolti di statistica gratis.",
     "https://payhip.com/b/ix1aB", "3,50 €", 9),
    ("excel-esercizi-esame-informatica-icdl", "excel-esame-informatica-icdl",
     "Excel per l'esame di Informatica / ICDL: teoria ed esercizi svolti",
     "SE, CONTA.SE, SOMMA.SE, CERCA.VERT, riferimenti assoluti, pivot ed errori tipici: esercizi svolti di Excel per l'esame di informatica.",
     "https://payhip.com/b/vWD2U", "3,50 €", 12),
]
BUNDLE = "https://payhip.com/b/BkzUb"

src_css = (SRC / "statistica-di-base.html").read_text(encoding="utf-8")
DISP_CSS = re.search(r"<style>(.*?)</style>", src_css, re.S).group(1)
DISP_CSS = re.sub(r"@page[^}]*}", "", DISP_CSS).replace("page-break-before: always;", "")
CSS = DISP_CSS + """
body{max-width:820px;margin:0 auto;padding:16px;background:#fff}
header.top{display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #C9D6D1;padding-bottom:8px;margin-bottom:16px}
header.top a{color:#1F6F5C;text-decoration:none;font-weight:700}
.cta{background:#123F35;color:#fff;border-radius:8px;padding:16px 18px;margin:22px 0}
.cta a.btn{display:inline-block;background:#7FD1B3;color:#123F35;font-weight:700;padding:9px 16px;border-radius:6px;text-decoration:none;margin-top:8px}
.cta p{margin:4px 0}
.lock{border:2px dashed #C9D6D1;border-radius:8px;padding:14px;color:#555;text-align:center}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px}
.card{border:1px solid #C9D6D1;border-radius:8px;padding:14px}
.card a{color:#1F6F5C;font-weight:700}
table{display:block;overflow-x:auto}
footer{color:#777;font-size:9pt;margin-top:30px;border-top:1px solid #eee;padding-top:8px}
"""


def page(path, title, desc, body):
    html = f"""<!doctype html><html lang="it"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}">
<link rel="canonical" href="{BASE}{path}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<style>{CSS}</style></head><body>
<header class="top"><a href="./">Esercizi svolti gratis</a><a href="{BUNDLE}">Tutte le dispense →</a></header>
{body}
<footer>Materiale originale, risultati calcolati e verificati. Controlla sempre il programma e le convenzioni del tuo corso.</footer>
</body></html>"""
    (OUT / (path or "index.html")).write_text(html, encoding="utf-8")


def cta(link, prezzo, tot, mostrati):
    return f"""<div class="cta"><p><b>Ti sono stati utili?</b> La dispensa completa in PDF ha tutti i {tot} esercizi svolti
(qui ne vedi {mostrati}), pronta da stampare.</p>
<a class="btn" href="{link}">Scarica la dispensa completa – {prezzo}</a>
<p style="font-size:9.5pt;margin-top:8px">Oppure il <a href="{BUNDLE}" style="color:#7FD1B3">pacchetto con 4 dispense a 9,90 €</a>.</p></div>"""


urls = [BASE]
for slug, src, title, desc, link, prezzo, tot in PAGINE:
    soup = BeautifulSoup((SRC / f"{src}.html").read_text(encoding="utf-8"), "html.parser")
    body = soup.body
    for n in body.select(".cover, .toc"):
        n.decompose()
    for h in body.find_all("h2"):
        if h.get_text(strip=True) == "Indice":
            h.decompose()
    for n in body.find_all("p", class_="note"):
        if "Dispensa originale" in n.get_text():
            n.decompose()
    exs = body.select(".ex")
    for e in exs[GRATIS:]:
        e.decompose()
    if exs:
        exs[GRATIS - 1].insert_after(BeautifulSoup(
            f'<div class="lock">🔒 Altri {tot - GRATIS} esercizi svolti sono nella dispensa completa.</div>'
            + cta(link, prezzo, tot, GRATIS), "html.parser"))
    inner = "".join(str(c) for c in body.contents)
    intro = f"<h1>{title}</h1><p class='sub'>{desc}</p>" + cta(link, prezzo, tot, GRATIS)
    page(f"{slug}.html", title, desc, intro + inner)
    urls.append(BASE + f"{slug}.html")

cards = "".join(f'<div class="card"><a href="{s}.html">{t}</a><p>{d}</p></div>' for s, _, t, d, *_ in PAGINE)
page("", "Esercizi svolti gratis: partita doppia, matematica finanziaria, statistica, Excel",
     "Esercizi svolti con soluzioni passo passo di Economia aziendale, Matematica finanziaria, Statistica ed Excel/ICDL. Teoria e formulari gratis.",
     f"<h1>Esercizi svolti gratis</h1><p class='sub'>Teoria, formule ed esercizi con soluzione passo passo per verifiche, maturità ed esami universitari.</p><div class='cards'>{cards}</div>"
     + f"<div class='cta'><p><b>Vuoi tutti gli esercizi in PDF?</b> 4 dispense, 42 esercizi svolti.</p><a class='btn' href='{BUNDLE}'>Pacchetto completo – 9,90 €</a></div>")

today = date.today().isoformat()
(OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                                 + "".join(f"<url><loc>{u}</loc><lastmod>{today}</lastmod></url>" for u in urls) + "</urlset>", encoding="utf-8")
(OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n", encoding="utf-8")
keyf = ROOT / "indexnow.key"
key = keyf.read_text().strip() if keyf.exists() else secrets.token_hex(16)
keyf.write_text(key)
(OUT / f"{key}.txt").write_text(key)
(OUT / ".nojekyll").write_text("")
print("\n".join(urls))
