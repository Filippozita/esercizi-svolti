"""Una pagina per ogni esercizio: testo sempre, soluzione solo per i primi GRATIS. Aggiorna sitemap e indice."""
import re, unicodedata
from datetime import date
from pathlib import Path
from bs4 import BeautifulSoup
import build_sito as S

def slug(t):
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:70]

MAT = {"economia-aziendale-partita-doppia": "Economia aziendale", "matematica-finanziaria": "Matematica finanziaria",
       "statistica-di-base": "Statistica", "excel-esame-informatica-icdl": "Excel / ICDL"}
urls, elenco = [], {}
for pslug, src, ptitle, pdesc, link, prezzo, tot in S.PAGINE:
    soup = BeautifulSoup((S.SRC / f"{src}.html").read_text(encoding="utf-8"), "html.parser")
    items = []
    for k, ex in enumerate(soup.select(".ex")):
        t = ex.select_one("b.t").get_text(" ", strip=True)
        nome = t.split("—", 1)[-1].strip()
        sol = ex.select_one(".sol"); sol.extract(); ex.select_one("b.t").extract()
        testo = "".join(str(c) for c in ex.contents).strip()
        if testo.startswith("<br/>"): testo = testo[5:]
        tabella = soup.select_one("table") if src.startswith("excel") else None
        s = f"{slug(MAT[src])}-esercizio-svolto-{slug(nome)}"
        title = f"{nome}: esercizio svolto di {MAT[src]}"
        desc = BeautifulSoup(testo, "html.parser").get_text(" ", strip=True)[:150]
        if k < S.GRATIS:
            corpo = f"<div class='ex'><b class='t'>Testo</b><br>{testo}<div class='sol'>{sol}</div></div>"
        else:
            corpo = (f"<div class='ex'><b class='t'>Testo</b><br>{testo}</div>"
                     f"<div class='lock'>🔒 La soluzione passo passo di questo esercizio è nella dispensa completa.</div>")
        extra = f"<p>Tabella dati usata nell'esercizio:</p>{tabella}" if tabella else ""
        body = (f"<p class='note'><a href='{pslug}.html'>← {ptitle}</a></p><h1>{title}</h1>{extra}{corpo}"
                + S.cta(link, prezzo, tot, S.GRATIS)
                + f"<p><a href='{pslug}.html'>Teoria e altri esercizi svolti gratis di {MAT[src]} →</a></p>")
        S.page(f"{s}.html", title, desc, body)
        items.append((s, nome, k < S.GRATIS))
        urls.append(S.BASE + f"{s}.html")
    elenco[pslug] = items
    # aggiunge elenco esercizi in fondo alla pagina materia
    p = S.OUT / f"{pslug}.html"
    h = p.read_text(encoding="utf-8")
    lista = "<h2>Tutti gli esercizi</h2><ul>" + "".join(
        f"<li><a href='{s}.html'>{n}</a>{' (soluzione gratis)' if g else ''}</li>" for s, n, g in items) + "</ul>"
    p.write_text(h.replace("<footer>", lista + "<footer>"), encoding="utf-8")

sm = S.OUT / "sitemap.xml"
x = sm.read_text(encoding="utf-8").replace("</urlset>", "".join(
    f"<url><loc>{u}</loc><lastmod>{date.today().isoformat()}</lastmod></url>" for u in urls) + "</urlset>")
sm.write_text(x, encoding="utf-8")
Path(S.ROOT / "nuovi_url.txt").write_text("\n".join(urls))
print(len(urls), "pagine esercizio")
