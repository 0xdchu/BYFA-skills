(async()=>{const w=[...document.querySelectorAll('widget, .fe-geo-chart-generated, div')].find(d=>d.innerText&&d.innerText.startsWith('Interest by region'));
if(!w) return 'NOWIDGET';
const out=[];for(let i=0;i<60;i++){const t=w.innerText;const m=[...t.matchAll(/\n(\d+)\n([^\n]+)\n(\d+|<1)(?=\n)/g)].map(x=>x[2]+'='+x[3]);out.push(...m);
const b=[...w.querySelectorAll('button')].find(b=>/next/i.test(b.getAttribute('aria-label')||b.innerText));if(!b||b.disabled||b.classList.contains('disabled'))break;b.click();await new Promise(r=>setTimeout(r,400));
if(w.innerText===t)break;}
return [...new Set(out)].join(';')})()
