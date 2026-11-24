"""Calcolatori interattivi (JS puro) che portano traffico di ricerca e rimandano alle dispense."""
import build_sito as S

JS_FMT = "const f=(x,d=2)=>Number(x).toLocaleString('it-IT',{minimumFractionDigits:d,maximumFractionDigits:d});const v=id=>parseFloat(document.getElementById(id).value.replace(',','.'));"
FORM_CSS = "<style>.calc label{display:block;margin:8px 0 2px;font-weight:600}.calc input,.calc select{width:100%;max-width:320px;padding:7px;border:1px solid #C9D6D1;border-radius:6px;font-size:11pt}.calc button{margin-top:12px;background:#1F6F5C;color:#fff;border:0;border-radius:6px;padding:9px 18px;font-size:11pt;cursor:pointer}.out{margin-top:14px}</style>"

CALC = [
    dict(slug="calcolo-rata-mutuo-ammortamento-francese", link="https://payhip.com/b/WMrnJ", prezzo="3,90 €", tot=11,
         title="Calcolo rata mutuo e piano di ammortamento francese (calcolatore gratis)",
         desc="Calcola la rata costante di un prestito o mutuo con l'ammortamento francese e guarda il piano completo: quota interessi, quota capitale e debito residuo.",
         form="""<label>Importo del prestito (€)</label><input id="C" value="10000">
<label>Tasso annuo (%)</label><input id="i" value="5">
<label>Durata (anni)</label><input id="n" value="5">
<label>Rate all'anno</label><select id="m"><option value="1">1 (annuale)</option><option value="2">2 (semestrale)</option><option value="4">4 (trimestrale)</option><option value="12" selected>12 (mensile)</option></select>""",
         js="""const C=v('C'),ia=v('i')/100,m=v('m'),N=Math.round(v('n')*m),i=Math.pow(1+ia,1/m)-1;
const R=i===0?C/N:C*i/(1-Math.pow(1+i,-N));let D=C,rows='';
for(let k=1;k<=N;k++){const I=D*i,Q=R-I;D-=Q;if(k<=24||k===N)rows+=`<tr><td>${k}</td><td>${f(R)}</td><td>${f(I)}</td><td>${f(Q)}</td><td>${f(Math.max(D,0))}</td></tr>`;else if(k===25)rows+='<tr><td>…</td><td></td><td></td><td></td><td></td></tr>';}
out.innerHTML=`<div class="box">Tasso per periodo (equivalente): <b>${f(i*100,4)}%</b> · Rata: <b class="res">${f(R)} €</b> · Interessi totali: <b>${f(R*N-C)} €</b></div><table><tr><th>Rata</th><th>Importo</th><th>Interessi</th><th>Capitale</th><th>Debito residuo</th></tr>${rows}</table>`;""",
         teoria="""<h2>Formula della rata</h2><div class="box"><span class="f">R = C · i / (1 − (1+i)<sup>−n</sup>)</span><br>C = capitale, i = tasso del periodo, n = numero di rate. Con rate mensili il tasso annuo si converte nel tasso mensile equivalente: i<sub>12</sub> = (1+i)<sup>1/12</sup> − 1.</div>
<p>Nell'ammortamento francese la rata è costante: all'inizio è fatta soprattutto di interessi, verso la fine soprattutto di capitale. Nell'ammortamento italiano invece è costante la quota capitale.</p>"""),
    dict(slug="calcolo-interesse-composto-montante", link="https://payhip.com/b/WMrnJ", prezzo="3,90 €", tot=11,
         title="Calcolo interesse composto e montante (calcolatore gratis con formula)",
         desc="Calcola montante, interesse e valore attuale in capitalizzazione composta e semplice. Formula spiegata e confronto anno per anno.",
         form="""<label>Capitale iniziale (€)</label><input id="C" value="5000">
<label>Tasso annuo (%)</label><input id="i" value="3">
<label>Durata (anni)</label><input id="t" value="4">""",
         js="""const C=v('C'),i=v('i')/100,t=v('t');const Mc=C*Math.pow(1+i,t),Ms=C*(1+i*t);let rows='';
for(let k=1;k<=Math.min(Math.ceil(t),40);k++)rows+=`<tr><td>${k}</td><td>${f(C*(1+i*k))}</td><td>${f(C*Math.pow(1+i,k))}</td></tr>`;
out.innerHTML=`<div class="box">Montante composto: <b class="res">${f(Mc)} €</b> (interesse ${f(Mc-C)} €)<br>Montante semplice: <b>${f(Ms)} €</b> (interesse ${f(Ms-C)} €)<br>Tempo di raddoppio (composto): <b>${f(Math.log(2)/Math.log(1+i))} anni</b></div><table><tr><th>Anno</th><th>Semplice (€)</th><th>Composto (€)</th></tr>${rows}</table>`;""",
         teoria="""<h2>Formule</h2><div class="box">Semplice: <span class="f">M = C(1 + i·t)</span><br>Composto: <span class="f">M = C(1 + i)<sup>t</sup></span><br>Valore attuale: <span class="f">C = M(1 + i)<sup>−t</sup></span><br>Raddoppio: <span class="f">t = ln 2 / ln(1+i)</span></div>"""),
    dict(slug="calcolatore-media-varianza-deviazione-standard", link="https://payhip.com/b/ix1aB", prezzo="3,50 €", tot=9,
         title="Calcolatore media, mediana, varianza e deviazione standard (gratis)",
         desc="Inserisci i dati e calcola media, mediana, moda, varianza e deviazione standard (della popolazione e campionaria), quartili e coefficiente di variazione.",
         form="""<label>Dati (separati da spazio o punto e virgola)</label><input id="d" value="18; 24; 30; 27; 28; 30; 22; 25; 30; 26" style="max-width:100%">""",
         js="""const x=document.getElementById('d').value.split(/[;\\s]+/).map(s=>parseFloat(s.replace(',','.'))).filter(n=>!isNaN(n)).sort((a,b)=>a-b);const n=x.length;
if(n<2){out.innerHTML='<p>Inserisci almeno 2 numeri.</p>';return;}
const m=x.reduce((a,b)=>a+b,0)/n,ss=x.reduce((a,b)=>a+(b-m)**2,0),q=p=>{const h=(n-1)*p,l=Math.floor(h);return x[l]+(h-l)*((x[l+1]??x[l])-x[l]);};
const cnt={};x.forEach(z=>cnt[z]=(cnt[z]||0)+1);const mx=Math.max(...Object.values(cnt));const moda=mx>1?Object.keys(cnt).filter(k=>cnt[k]===mx).map(Number).map(z=>f(z,2)).join(' · '):'nessuna';
out.innerHTML=`<table><tr><th>Indice</th><th>Valore</th></tr><tr><td>n</td><td>${n}</td></tr><tr><td>Media</td><td><b>${f(m,4)}</b></td></tr><tr><td>Mediana</td><td>${f(q(.5),4)}</td></tr><tr><td>Moda</td><td>${moda}</td></tr>
<tr><td>Varianza popolazione (÷n)</td><td>${f(ss/n,4)}</td></tr><tr><td>Deviazione standard popolazione</td><td><b>${f(Math.sqrt(ss/n),4)}</b></td></tr>
<tr><td>Varianza campionaria (÷n−1)</td><td>${f(ss/(n-1),4)}</td></tr><tr><td>Deviazione standard campionaria</td><td><b>${f(Math.sqrt(ss/(n-1)),4)}</b></td></tr>
<tr><td>Q1 · Q3 (come QUARTILE.INC di Excel)</td><td>${f(q(.25),4)} · ${f(q(.75),4)}</td></tr><tr><td>Scarto interquartile</td><td>${f(q(.75)-q(.25),4)}</td></tr><tr><td>Coefficiente di variazione</td><td>${f(Math.sqrt(ss/n)/m*100,2)}%</td></tr></table>`;""",
         teoria="""<h2>Formule</h2><div class="box">Media: <span class="f">x̄ = Σx / n</span><br>Varianza della popolazione: <span class="f">σ² = Σ(x − x̄)² / n</span><br>Varianza campionaria: <span class="f">s² = Σ(x − x̄)² / (n − 1)</span><br>Deviazione standard = radice quadrata della varianza.</div>
<p>All'esame controlla quale varianza chiede il tuo corso: alcuni testi usano n, altri n − 1.</p>"""),
    dict(slug="calcolo-iva-scorporo-22", link="https://payhip.com/b/ghBQW", prezzo="4,00 €", tot=10,
         title="Come si scorpora l'IVA al 22%: formula e calcolatore gratis",
         desc="Come si scorpora l'IVA al 22%: dividi il prezzo ivato per 1,22 (es. 1.220 € → 1.000 € + 220 € di IVA). Calcolatore gratis per scorporare o aggiungere l'IVA al 22%, 10%, 5% e 4%.",
         form="""<label>Importo (€)</label><input id="a" value="1220">
<label>Aliquota</label><select id="r"><option>22</option><option>10</option><option>5</option><option>4</option></select>
<label>L'importo è</label><select id="t"><option value="lordo">IVA inclusa (scorpora)</option><option value="netto">imponibile (aggiungi IVA)</option></select>""",
         js="""const a=v('a'),r=v('r')/100,lordo=document.getElementById('t').value==='lordo';const imp=lordo?a/(1+r):a,iva=imp*r,tot=imp+iva;
out.innerHTML=`<div class="box">Imponibile: <b>${f(imp)} €</b> · IVA ${f(r*100,0)}%: <b class="res">${f(iva)} €</b> · Totale: <b>${f(tot)} €</b></div>
<p>Scrittura di un acquisto di merci con fattura (partita doppia):</p><table><tr><th>Conto</th><th>DARE</th><th>AVERE</th></tr><tr><td>Merci c/acquisti</td><td>${f(imp)}</td><td></td></tr><tr><td>IVA ns/credito</td><td>${f(iva)}</td><td></td></tr><tr><td>Debiti v/fornitori</td><td></td><td>${f(tot)}</td></tr></table>`;""",
         teoria="""<h2>Come si scorpora l'IVA al 22%</h2><p>Per scorporare l'IVA al 22% da un prezzo IVA inclusa si divide il prezzo per <b>1,22</b>: il risultato è l'imponibile, e la differenza tra prezzo e imponibile è l'IVA. Esempio: 122 € / 1,22 = 100 € di imponibile e 22 € di IVA. Attenzione: non basta togliere il 22% dal prezzo (122 € − 22% = 95,16 €, sbagliato).</p>
<h2>Formule</h2><div class="box">Aggiungere l'IVA: <span class="f">totale = imponibile × (1 + aliquota)</span><br>Scorporare l'IVA: <span class="f">imponibile = totale / (1 + aliquota)</span>; IVA = totale − imponibile.<br>Esempio: 1.220 € con IVA 22% → imponibile 1.000 €, IVA 220 €.</div>"""),
]

for c in CALC:
    body = (f"<h1>{c['title']}</h1><p class='sub'>{c['desc']}</p>{FORM_CSS}<div class='calc'>{c['form']}<br>"
            f"<button onclick='calcola()'>Calcola</button></div><div class='out' id='out'></div>"
            f"<script>{JS_FMT}const out=document.getElementById('out');function calcola(){{{c['js']}}}calcola();</script>"
            + c["teoria"] + S.cta(c["link"], c["prezzo"], c["tot"], 3)
            + "<p><a href='./'>Altri esercizi svolti e strumenti gratis →</a></p>")
    S.page(f"{c['slug']}.html", c["title"], c["desc"], body)
    print(S.BASE + c["slug"] + ".html")
