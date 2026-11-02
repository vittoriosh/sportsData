import re
s=open('/home/claude/app/template.html').read()
def rep(a,b):
    global s
    assert s.count(a)>=1,a[:70]
    s=s.replace(a,b)
s,nsub=re.subn(r"const COLORS = \{[^}]*\};","const COLORS = {}; SEASONS.slice(0,-1).forEach((s,i)=>{COLORS[s]=`hsl(${Math.round((i*137.508)%360)} 58% 42%)`;});",s,count=1); assert nsub==1
rep("'var(--g'+SEASONS.indexOf(s)+')'","`hsl(0 0% ${(74-SEASONS.indexOf(s)*(32/(SEASONS.length-1))).toFixed(1)}%)`")
rep("let shown=new Set(SEASONS)","let shown=new Set(SEASONS.slice(-10))")
rep('<button class="btn ghost" id="selLast5">Last 5</button>','<button class="btn ghost" id="selLast10">Last 10</button>\n        <button class="btn ghost" id="selLast5">Last 5</button>')
rep("$('selLast5').onclick=","$('selLast10').onclick=()=>{shown=new Set(SEASONS.slice(-10));chips();drawLine();};\n$('selLast5').onclick=")
rep("Premier League 2017-18 to 2026-27","Premier League 2007-08 to 2026-27")
rep("g.forEach(m=>{p+=pts(m);gf+=m.gf;ga+=m.ga;y+=m.cy;r+=m.cr;\n    cum[s].pts.push(p);cum[s].gf.push(gf);cum[s].ga.push(ga);cum[s].gd.push(gf-ga);cum[s].y.push(y);cum[s].r.push(r);});",
    "g.forEach(m=>{p+=pts(m);gf+=m.gf;ga+=m.ga;\n    cum[s].pts.push(p);cum[s].gf.push(gf);cum[s].ga.push(ga);cum[s].gd.push(gf-ga);\n    if(m.cy!==null){y+=m.cy;r+=m.cr;cum[s].y.push(y);cum[s].r.push(r);}});")
rep("const stat = {};","const hasCards=s=>bySeason[s].length>0&&bySeason[s].every(m=>m.cy!==null);\nconst CARDSEASONS=SEASONS.filter(hasCards);\nconst stat = {};")
rep("g.forEach(m=>{const r=res(m);o[r]++;o.GF+=m.gf;o.GA+=m.ga;o.Y+=m.cy;o.R+=m.cr;o.OY+=m.oy;o.OR+=m.orr;if(m.ga===0)o.CS++;});\n  o.GD=o.GF-o.GA;o.Pts=o.W*3+o.D;o.PPG=o.P?o.Pts/o.P:0;o.YPG=o.P?o.Y/o.P:0;",
    "g.forEach(m=>{const r=res(m);o[r]++;o.GF+=m.gf;o.GA+=m.ga;o.Y+=m.cy||0;o.R+=m.cr||0;o.OY+=m.oy||0;o.OR+=m.orr||0;if(m.ga===0)o.CS++;});\n  o.GD=o.GF-o.GA;o.Pts=o.W*3+o.D;o.PPG=o.P?o.Pts/o.P:0;o.YPG=o.P&&hasCards(s)?o.Y/o.P:null;")
rep("['Yellow cards per game',c.YPG.toFixed(2),'This season. '+SEASONS[0]+' was '+stat[SEASONS[0]].YPG.toFixed(2)],",
    "['Yellow cards per game',c.YPG.toFixed(2),'This season. '+CARDSEASONS[0]+' was '+stat[CARDSEASONS[0]].YPG.toFixed(2)],")
rep("const o={P:g.length,W:0,D:0,L:0,GF:0,GA:0,Y:0,R:0,CS:0};\n  g.forEach(m=>{o[res(m)]++;o.GF+=m.gf;o.GA+=m.ga;o.Y+=m.cy;o.R+=m.cr;if(m.ga===0)o.CS++;});\n  o.GD=o.GF-o.GA;o.Pts=o.W*3+o.D;o.PPG=o.P?o.Pts/o.P:0;o.YPG=o.P?o.Y/o.P:0;return o;",
    "const o={P:g.length,W:0,D:0,L:0,GF:0,GA:0,Y:0,R:0,CS:0};\n  const cd=g.filter(m=>m.cy!==null).length;\n  g.forEach(m=>{o[res(m)]++;o.GF+=m.gf;o.GA+=m.ga;o.Y+=m.cy||0;o.R+=m.cr||0;if(m.ga===0)o.CS++;});\n  o.GD=o.GF-o.GA;o.Pts=o.W*3+o.D;o.PPG=o.P?o.Pts/o.P:0;\n  if(!cd){o.Y=null;o.R=null;o.YPG=null;}else o.YPG=o.Y/cd;return o;")
rep("<td>${c(o.Y)}</td><td>${c(o.R)}</td><td>${none?d:o.YPG.toFixed(2)}</td>","<td>${o.Y===null?d:c(o.Y)}</td><td>${o.R===null?d:c(o.R)}</td><td>${(none||o.YPG===null)?d:o.YPG.toFixed(2)}</td>")
rep("const cells=SEASONS.map(s=>bs.map(([a,b])=>{const g=bySeason[s].slice(a-1,b);return {g,len:b-a+1,v:g.length?gridVal(key,g):null};}));",
    "const cardKey=key==='y'||key==='r';\n  const cells=SEASONS.map(s=>bs.map(([a,b])=>{const g=bySeason[s].slice(a-1,b);return {g,len:b-a+1,v:(g.length&&(!cardKey||g[0].cy!==null))?gridVal(key,g):null};}));")
rep("h+=`<td style=\"text-align:center\"><b>${f(gridVal(key,bySeason[s]))}</b></td></tr>`;","h+=`<td style=\"text-align:center\">${(cardKey&&!hasCards(s))?'<span class=\"zero\">&ndash;</span>':'<b>'+f(gridVal(key,bySeason[s]))+'</b>'}</td></tr>`;")
rep("function cardCell(n,t){ return n? `","function cardCell(n,t){ if(n===null)return '<span class=\"zero\">&ndash;</span>'; return n? `")
rep("t[res(m)]++;t.GF+=m.gf;t.GA+=m.ga;t.Y+=m.cy;t.R+=m.cr;t.OY+=m.oy;t.OR+=m.orr;","t[res(m)]++;t.GF+=m.gf;t.GA+=m.ga;t.Y+=m.cy||0;t.R+=m.cr||0;t.OY+=m.oy||0;t.OR+=m.orr||0;")
rep("bars('cardSvg',SEASONS.map(s=>({s,a:stat[s].Y/stat[s].P,b:stat[s].OY/stat[s].P}))","bars('cardSvg',CARDSEASONS.map(s=>({s,a:stat[s].Y/stat[s].P,b:stat[s].OY/stat[s].P}))")
rep("bars('redSvg',SEASONS.map(s=>({s,a:stat[s].R,b:stat[s].OR}))","bars('redSvg',CARDSEASONS.map(s=>({s,a:stat[s].R,b:stat[s].OR}))")
rep("const rows=[...M].map(m=>({m,sc:m.cy+m.cr*2}))","const rows=M.filter(m=>m.cy!==null).map(m=>({m,sc:m.cy+m.cr*2}))")
rep("const band=iw/items.length, bw=Math.min(18,band*.36);","const band=iw/items.length, bw=Math.min(18,band*.36), rotate=band<46;")
rep("""text-anchor="middle" transform="rotate(${W<520?-40:0} ${cx} ${H-m.b+16})" ${W<520?'text-anchor="end"':''}>${W<520?it.s.slice(2):it.s}</text>""","""text-anchor="${rotate?'end':'middle'}" transform="rotate(${rotate?-40:0} ${cx} ${H-m.b+16})">${rotate?it.s.slice(2):it.s}</text>""")
rep("League games only. Scores, dates and cards for 2017-18 to 2025-26 come from Fantasy Premier League match data and agree with official season totals.","League games only. 2017-18 to 2025-26: Fantasy Premier League match data. 2010-11 to 2016-17: football-data.co.uk-derived dataset. 2007-08 to 2009-10: scores only (openfootball), so cards show a dash. Every completed season matches its official points total.")
rep('<div class="tiles" id="tiles"></div>','<div class="tiles" id="tiles"></div>\n  <div class="card" id="projCard"></div>')
proj=r'''function drawProjection(){
  const el=$('projCard'), c=stat[CUR], n=c.P, left=38-n;
  if(n<3||left<=0){el.style.display='none';return;} el.style.display='';
  const done=SEASONS.filter(s=>s!==CUR&&bySeason[s].length>=38);
  const xs=done.map(s=>cum[s].pts[n-1]), ys=done.map(s=>cum[s].pts[37]);
  const k=xs.length, mx=xs.reduce((a,b)=>a+b,0)/k, my=ys.reduce((a,b)=>a+b,0)/k;
  const sxx=xs.reduce((a,x)=>a+(x-mx)**2,0), sxy=xs.reduce((a,x,i)=>a+(x-mx)*(ys[i]-my),0), syy=ys.reduce((a,y)=>a+(y-my)**2,0);
  const b=sxy/sxx, a0=my-b*mx;
  const sd=Math.sqrt(xs.reduce((a,x,i)=>a+(ys[i]-(a0+b*x))**2,0)/(k-2));
  const r=sxy/Math.sqrt(sxx*syy);
  const x=c.Pts, pace=x/n*38, model=a0+b*x;
  const usual=x+ys.reduce((a,y,i)=>a+(y-xs[i]),0)/k;
  const centre=Math.round((pace+model+usual)/3);
  const lo=Math.round(model-sd), hi=Math.round(model+sd);
  const near=done.filter(s=>Math.abs(cum[s].pts[37]-centre)<=4).sort((p,q)=>Math.abs(cum[p].pts[37]-centre)-Math.abs(cum[q].pts[37]-centre));
  const posList=near.map(s=>`${s}: ${ord(POS[s])} (${cum[s].pts[37]} pts)`).join(', ');
  const tile=(t,v,sub)=>`<div class="tile"><span class="k">${t}</span><span class="v">${v}</span><span class="s">${sub}</span></div>`;
  el.innerHTML=`<h2>Projected finish, ${CUR}</h2><p class="hint">${n} games played, ${x} points, ${left} to go. Built from ${k} completed seasons of Chelsea's own history.</p>
  <div class="tiles" style="margin-top:12px">
    ${tile('Current pace',Math.round(pace)+' pts',x+' points from '+n+' games, repeated over 38')}
    ${tile('From history',Math.round(model)+' pts','Typical range '+lo+' to '+hi+' (points after '+n+' games versus final points)')}
    ${tile('Usual rest of season',Math.round(usual)+' pts','Current points plus what Chelsea usually add in games '+(n+1)+' to 38')}
    ${tile('Middle estimate',centre+' pts','Average of the three, about '+(centre/38).toFixed(2)+' per game')}
  </div>
  <p class="hint" style="margin-top:12px">${near.length?'Seasons that ended within 4 points of '+centre+': '+posList+'.':'No earlier season ended within 4 points of '+centre+'.'}</p>
  <p class="hint">Early points only loosely predict the final total here (correlation ${r.toFixed(2)}), so treat the range as wide. It ignores the fixture list, injuries and other clubs, and I have no data for other clubs, so it cannot say whether that total reaches the top four.</p>`;
}
'''
rep("function drawOverview(){drawTiles();","function drawOverview(){drawTiles();drawProjection();")
s=s.replace("function drawOverview(){",proj+"function drawOverview(){",1)
open('/home/claude/app/template.html','w').write(s)
open('/home/claude/app/index.html','w').write(s.replace('__DATA__',open('/home/claude/app/data.json').read().replace('</','<\\/')))
print('ok')
