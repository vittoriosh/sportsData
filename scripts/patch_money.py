import re
s=open('/home/claude/app2/template.html').read()
def rep(a,b,count=1):
    global s
    assert a in s,a[:80]
    s=s.replace(a,b,count)

# ---- titles / tabs / sections ----
rep("<title>Premier League Odds</title>","<title>Premier League Explorer</title>")
rep("<h1>Premier League Odds</h1>","<h1>Premier League Explorer</h1>")
rep('<button role="tab" data-v="seasons" aria-selected="false">Seasons</button>','<button role="tab" data-v="seasons" aria-selected="false">Seasons</button>\n      <button role="tab" data-v="money" aria-selected="false">Money</button>\n      <button role="tab" data-v="mgrs" aria-selected="false">Managers</button>')
rep("const VIEWS=['odds','team','seasons','matches'];","const VIEWS=['odds','team','seasons','money','mgrs','matches'];")
money_html='''<section class="view" id="v-money">
  <div class="card">
    <div class="controls" style="margin-top:0">
      <label class="f" for="moSeason">Season<select id="moSeason"></select></label>
    </div>
    <p class="hint" id="moNote"></p>
  </div>
  <div class="tiles" id="moTiles"></div>
  <div class="cols two">
    <div class="card" id="cardScat">
      <div class="cardhead"><div><h2 id="scatTitle">Spending against points</h2><p class="hint">Each dot is a club. The line is the average points that level of net spending bought that season. Dots above the line got more than the money suggests.</p></div>
        <div class="chips"><button class="btn expandbtn" data-card="cardScat">Expand</button><span class="fullbar"><button class="btn" data-act="rotate" aria-pressed="false">Rotate</button><button class="btn" data-act="close">Close</button></span></div></div>
      <div class="chartbox"><svg id="scatSvg" role="img" aria-label="Net transfer spend against league points"></svg><div class="tip" id="tipS"></div></div>
    </div>
    <div class="card" id="cardR2">
      <div class="cardhead"><div><h2>How much did spending explain?</h2><p class="hint">Share of the points differences between clubs that net spend explains, each season (R squared). Lighter bars use net spend for the current clubs only.</p></div>
        <div class="chips"><button class="btn expandbtn" data-card="cardR2">Expand</button><span class="fullbar"><button class="btn" data-act="rotate" aria-pressed="false">Rotate</button><button class="btn" data-act="close">Close</button></span></div></div>
      <div class="chartbox"><svg id="r2Svg" role="img" aria-label="Share of points variation explained by net spend, by season"></svg></div>
    </div>
  </div>
  <div class="card">
    <h2 id="moTitle">Club by club</h2>
    <p class="hint">Net spend is fees paid minus fees received across the summer and winter windows. Rank gap is spend rank minus finishing rank among the clubs shown: positive means the club finished higher than its spending ranks it.</p>
    <div class="tablewrap"><table id="moTable"></table></div>
  </div>
  <div class="cols two">
    <div class="card"><h2>Best value for money</h2><p class="hint">Most points above the line, 2007-08 to 2022-23, when every club has spending data.</p><div class="tablewrap"><table id="bestTable"></table></div></div>
    <div class="card"><h2>Worst value for money</h2><p class="hint">Most points below the line, same seasons.</p><div class="tablewrap"><table id="worstTable"></table></div></div>
  </div>
</section>

<section class="view" id="v-mgrs">
  <div class="tiles" id="mgTiles"></div>
  <div class="card">
    <div class="cardhead"><div><h2>Manager records</h2><p class="hint">League games only, 2007-08 onwards, all clubs. Points per game is the fairest comparison; remember clubs differ hugely in resources. Click a manager for their spells.</p></div></div>
    <div class="controls">
      <label class="f" for="mgMin" style="min-width:200px">Minimum games <span id="mgMinV" style="color:var(--ink)"></span><input type="range" id="mgMin" min="1" max="380" value="76" style="width:100%"></label>
      <button class="btn ghost" id="mgCare" aria-pressed="false">Include caretakers</button>
      <label class="f" for="mgSearch">Search<input type="search" id="mgSearch" placeholder="Name or club"></label>
    </div>
    <div class="tablewrap" style="max-height:620px"><table id="mgTable"></table></div>
  </div>
  <div class="card">
    <h2>Managers used each season</h2>
    <p class="hint">Permanent managers who took charge of at least one league game, counting caretakers separately. In-season changes are managers who started a game in the middle of the season.</p>
    <div class="tablewrap"><table id="chgTable"></table></div>
  </div>
  <div class="card">
    <h2>The new-manager bounce</h2>
    <p class="hint" id="bounceHint"></p>
    <div class="tiles" id="bounceTiles" style="margin-top:10px"></div>
    <div class="tablewrap"><table id="bounceTable"></table></div>
  </div>
</section>

'''
rep('<section class="view" id="v-matches">',money_html+'<section class="view" id="v-matches">')
# club tab: managers card after tiles
rep('<div class="tiles" id="tTiles"></div>','<div class="tiles" id="tTiles"></div>\n  <div class="card"><h2 id="cmTitle">Managers</h2><p class="hint">Every manager with league games at this club since 2007-08. Caretakers are marked.</p><div class="tablewrap"><table id="cmTable"></table></div></div>')

# ---- data parsing ----
rep("const M=D.matches.map(r=>({s:r[0],d:r[1],h:r[2],a:r[3],hg:r[4],ag:r[5],hy:r[6],ay:r[7],hr:r[8],ar:r[9]}));",
    "const M=D.matches.map(r=>({s:r[0],d:r[1],h:r[2],a:r[3],hg:r[4],ag:r[5],hy:r[6],ay:r[7],hr:r[8],ar:r[9],hm:r[10],am:r[11]}));\nconst MG=D.mgr.map((r,i)=>({i,name:r[0],club:r[1],from:r[2],until:r[3],care:!!r[4]}));\nconst TRK={};D.tr.forEach(r=>{TRK[r[0]+'|'+r[1]]={spend:r[2],inc:r[3],net:r[4],gbp:!!r[5],gross:!!r[6],part:!!r[7]};});")
rep("return {d:m.d,gf:own?m.hg:m.ag,ga:own?m.ag:m.hg,y:own?m.hy:m.ay,r:own?m.hr:m.ar,opp:own?m.a:m.h,home:own,m};","return {d:m.d,gf:own?m.hg:m.ag,ga:own?m.ag:m.hg,y:own?m.hy:m.ay,r:own?m.hr:m.ar,opp:own?m.a:m.h,home:own,mg:own?m.hm:m.am,m};")

helpers=r'''
/* ---------- managers and money helpers ---------- */
const mfmt=v=>v===null||v===undefined?'<span class="zero">&ndash;</span>':(v<0?'&minus;':'')+Math.abs(Math.round(v))+'m';
const sym=(si,t)=>{const x=TRK[si+'|'+t];return x?(x.gbp?'£':'€'):'';};
const TS={};
M.forEach(m=>{[[m.hm,m.hg,m.ag],[m.am,m.ag,m.hg]].forEach(([id,gf,ga])=>{const o=TS[id]||(TS[id]={g:0,w:0,d:0,l:0,gf:0,ga:0});o.g++;o.gf+=gf;o.ga+=ga;if(gf>ga)o.w++;else if(gf===ga)o.d++;else o.l++;});});
const mainCache={};
function mainMgr(si,t){
  const k=si+'|'+t;if(mainCache[k])return mainCache[k];
  const c={};MS[si].forEach(m=>{if(m.h===t)c[m.hm]=(c[m.hm]||0)+1;else if(m.a===t)c[m.am]=(c[m.am]||0)+1;});
  const ids=Object.keys(c).map(Number).sort((a,b)=>c[b]-c[a]);
  if(!ids.length)return mainCache[k]=null;
  return mainCache[k]={name:MG[ids[0]].name,n:c[ids[0]],care:MG[ids[0]].care,others:ids.slice(1).map(i=>MG[i].name+(MG[i].care?' (caretaker)':''))};
}
function regress(pts){
  const n=pts.length;if(n<4)return null;const mx=pts.reduce((a,p)=>a+p.x,0)/n,my=pts.reduce((a,p)=>a+p.y,0)/n;
  const sxx=pts.reduce((a,p)=>a+(p.x-mx)**2,0),sxy=pts.reduce((a,p)=>a+(p.x-mx)*(p.y-my),0),syy=pts.reduce((a,p)=>a+(p.y-my)**2,0);
  if(!sxx)return null;const b=sxy/sxx,a=my-b*mx;return {a,b,r2:sxy*sxy/(sxx*syy)};
}
function moneyRows(si){
  const rows=seasonTable(si).map(o=>({...o,tr:TRK[si+'|'+o.t]||null})).filter(o=>o.tr&&o.tr.net!==null);
  const bySpend=[...rows].sort((a,b)=>b.tr.net-a.tr.net);bySpend.forEach((o,i)=>o.spendRank=i+1);
  const byPos=[...rows].sort((a,b)=>a.pos-b.pos);byPos.forEach((o,i)=>o.posRank=i+1);
  rows.forEach(o=>o.gap=o.spendRank-o.posRank);
  const reg=regress(rows.map(o=>({x:o.tr.net,y:o.Pts})));
  rows.forEach(o=>{o.res=reg?o.Pts-(reg.a+reg.b*o.tr.net):null;});
  return {rows,reg};
}
'''
rep("/* ---------- historical odds ---------- */",helpers+"\n/* ---------- historical odds ---------- */")

# ---- club tab additions ----
rep("  drawHist();chips();drawLine();\n}\n","  drawHist();drawClubMgrs();chips();drawLine();\n}\n")
rep("function drawHist(){","""function drawClubMgrs(){
  $('cmTitle').textContent='Managers at '+T[team];
  const ids=MG.filter(g=>g.club===team&&TS[g.i]).sort((a,b)=>a.from<b.from?1:-1);
  let h='<thead><tr><th class="l">Manager</th><th class="l">From</th><th class="l">To</th><th>Games</th><th>W</th><th>D</th><th>L</th><th>Pts/g</th><th>Win %</th></tr></thead><tbody>';
  ids.forEach(g=>{const o=TS[g.i];const to=g.until>'9000'?'Present':dt(g.until),fr=g.from<'2007-07-01'?'Before 2007':dt(g.from);
    h+=`<tr class="${g.until>'9000'?'sel':''}"><td class="l">${g.name}${g.care?' <span class="zero">(caretaker)</span>':''}</td><td class="l">${fr}</td><td class="l">${to}</td><td>${o.g}</td><td>${o.w}</td><td>${o.d}</td><td>${o.l}</td><td><b>${((o.w*3+o.d)/o.g).toFixed(2)}</b></td><td>${Math.round(o.w/o.g*100)}%</td></tr>`;});
  $('cmTable').innerHTML=h+(ids.length?'':'<tr><td class="l">No league games recorded for this club since 2007-08.</td></tr>')+'</tbody>';
}
function drawHist(){""")
rep("let h='<thead><tr><th class=\"l\">Season</th><th>Pos</th><th>P</th><th>W</th><th>D</th><th>L</th><th>GF</th><th>GA</th><th>GD</th><th>Pts</th><th>Pts/g</th><th>Yel</th><th>Red</th></tr></thead><tbody>';\n  let any=false;",
    "let h='<thead><tr><th class=\"l\">Season</th><th class=\"l\">Manager</th><th>Pos</th><th>P</th><th>W</th><th>D</th><th>L</th><th>GF</th><th>GA</th><th>GD</th><th>Pts</th><th>Pts/g</th><th>Net spend</th><th>Spent</th><th>Sold</th><th>Yel</th><th>Red</th></tr></thead><tbody>';\n  let any=false;")
rep("h+=`<tr class=\"${si===CUR?'sel':''}\"><td class=\"l\">${S[si]}${si===CUR?' (so far)':''}</td><td>${ord(r.pos)}</td>",
    "const mm=mainMgr(si,team),tk=TRK[si+'|'+team],sy=sym(si,team);\n    h+=`<tr class=\"${si===CUR?'sel':''}\"><td class=\"l\">${S[si]}${si===CUR?' (so far)':''}</td><td class=\"l\">${mm?mm.name:'-'}${mm&&mm.others.length?` <span class=\"zero\" title=\"${mm.others.join(', ')}\">+${mm.others.length}</span>`:''}</td><td>${ord(r.pos)}</td>")
rep("<td>${(r.Pts/r.P).toFixed(2)}</td><td>${r.cd===r.P?r.Y:'<span class=\"zero\">&ndash;</span>'}</td><td>${r.cd===r.P?r.R:'<span class=\"zero\">&ndash;</span>'}</td></tr>`;}",
    "<td>${(r.Pts/r.P).toFixed(2)}</td><td>${tk&&tk.net!==null?'<b>'+sy+mfmt(tk.net).replace('&minus;','&minus;')+'</b>':mfmt(null)}</td><td>${tk&&tk.spend!==null?sy+mfmt(tk.spend):mfmt(null)}</td><td>${tk&&tk.inc!==null?sy+mfmt(tk.inc):mfmt(null)}</td><td>${r.cd===r.P?r.Y:'<span class=\"zero\">&ndash;</span>'}</td><td>${r.cd===r.P?r.R:'<span class=\"zero\">&ndash;</span>'}</td></tr>`;}")
rep("$('histTable').innerHTML=h+(any?'':'<tr><td class=\"l\">No league seasons.</td></tr>')+'</tbody>';","$('histTable').innerHTML=h+(any?'':'<tr><td class=\"l\">No league seasons.</td></tr>')+'</tbody>';")

# ---- seasons table: manager + net spend ----
rep("let h='<thead><tr><th>Pos</th><th class=\"l\">Club</th><th>P</th><th>W</th><th>D</th><th>L</th><th>GF</th><th>GA</th><th>GD</th><th>Pts</th><th>Yel</th><th>Red</th></tr></thead><tbody>';\n  rows.forEach(o=>{const cards=o.cd===o.P;",
    "let h='<thead><tr><th>Pos</th><th class=\"l\">Club</th><th class=\"l\">Manager</th><th>P</th><th>W</th><th>D</th><th>L</th><th>GF</th><th>GA</th><th>GD</th><th>Pts</th><th>Net spend</th><th>Yel</th><th>Red</th></tr></thead><tbody>';\n  rows.forEach(o=>{const cards=o.cd===o.P,mm=mainMgr(si,o.t),tk=TRK[si+'|'+o.t];")
rep("<td>${o.pos}</td><td class=\"l\">${T[o.t]}</td><td>${o.P}</td><td>${o.W}</td>","<td>${o.pos}</td><td class=\"l\">${T[o.t]}</td><td class=\"l\">${mm?mm.name:'-'}${mm&&mm.others.length?` <span class=\"zero\" title=\"${mm.others.join(', ')}\">+${mm.others.length}</span>`:''}</td><td>${o.P}</td><td>${o.W}</td>")
rep("<td><b>${o.Pts}</b>${o.ded?'<sup title=\"points deducted\">*</sup>':''}</td><td>${cards?o.Y:","<td><b>${o.Pts}</b>${o.ded?'<sup title=\"points deducted\">*</sup>':''}</td><td>${tk&&tk.net!==null?(tk.gbp?'£':'€')+mfmt(tk.net):mfmt(null)}</td><td>${cards?o.Y:")
rep("'Click a club to follow it. Blue bar marks the top four, red the bottom three.'","'Managers: the one with most games that season, +N for others used (hover for names). Net spend is in euros up to 2022-23 and pounds after, for the current clubs only. Click a club to follow it.'")

# ---- money + managers drawing code ----
code=r'''
/* ---------- money ---------- */
const MOSEL=$('moSeason');
MOSEL.innerHTML=S.map((s,i)=>{const full=i<=S.indexOf('2022-23');return `<option value="${i}">${s}${full?'':' (partial)'}</option>`;}).reverse().join('');MOSEL.value=S.indexOf('2022-23');
MOSEL.addEventListener('change',drawMoney);
function scatter(id,tipId,pts,cfg){
  const svg=$(id),box=svg.parentElement,dm=dims(box),W=dm.W,H=dm.H||360,m={l:46,r:16,t:14,b:42},iw=W-m.l-m.r,ih=H-m.t-m.b;
  const xs=pts.map(p=>p.x),ys=pts.map(p=>p.y);const xr=nice(Math.max(...xs),Math.min(0,...xs)),yr=nice(Math.max(...ys)+3,Math.max(0,Math.min(...ys)-5));
  const X=v=>m.l+(v-xr.lo)/(xr.hi-xr.lo)*iw,Y=v=>m.t+ih-(v-yr.lo)/(yr.hi-yr.lo)*ih;let g='';
  yr.t.forEach(v=>{g+=`<line x1="${m.l}" x2="${W-m.r}" y1="${Y(v)}" y2="${Y(v)}" stroke="var(--grid)"/><text x="${m.l-6}" y="${Y(v)+4}" text-anchor="end">${v}</text>`;});
  xr.t.forEach(v=>{g+=`<line x1="${X(v)}" x2="${X(v)}" y1="${m.t}" y2="${m.t+ih}" stroke="var(--grid)"/><text x="${X(v)}" y="${H-m.b+16}" text-anchor="middle">${v}</text>`;});
  g+=`<text x="${m.l+iw/2}" y="${H-4}" text-anchor="middle">${cfg.xl}</text>`;
  if(xr.lo<0)g+=`<line x1="${X(0)}" x2="${X(0)}" y1="${m.t}" y2="${m.t+ih}" stroke="var(--muted)" stroke-opacity=".5"/>`;
  if(cfg.reg){const x0=xr.lo,x1=xr.hi;g+=`<line x1="${X(x0)}" y1="${Y(cfg.reg.a+cfg.reg.b*x0)}" x2="${X(x1)}" y2="${Y(cfg.reg.a+cfg.reg.b*x1)}" stroke="var(--ink)" stroke-dasharray="5 4" opacity=".7"/>`;}
  pts.forEach(p=>{const sel=p.t===team;g+=`<circle cx="${X(p.x)}" cy="${Y(p.y)}" r="${sel?8:5}" fill="${sel?'var(--cur)':p.c||'var(--gray)'}" stroke="#fff" stroke-width="1.5" opacity="${sel?1:.85}"/>`;
    if(sel||p.lab)g+=`<text x="${X(p.x)+9}" y="${Y(p.y)+4}" style="fill:var(--ink);font-weight:${sel?700:500};font-size:11px">${p.l}</text>`;});
  g+='<g id="hov"></g>'+`<rect id="hit" x="${m.l}" y="${m.t}" width="${iw}" height="${ih}" fill="transparent"/>`;
  svg.setAttribute('viewBox',`0 0 ${W} ${H}`);svg.setAttribute('width',W);svg.setAttribute('height',H);svg.innerHTML=g;
  const hit=svg.querySelector('#hit'),hov=svg.querySelector('#hov'),tip=$(tipId);
  const move=ev=>{const r=svg.getBoundingClientRect(),px=(fullCard&&rot)?(ev.clientY-r.top):(ev.clientX-r.left),py=(fullCard&&rot)?(r.right-ev.clientX):(ev.clientY-r.top);
    let b=null,bd=1e9;pts.forEach(p=>{const d=(X(p.x)-px)**2+(Y(p.y)-py)**2;if(d<bd){bd=d;b=p;}});if(!b||bd>2500){hov.innerHTML='';tip.style.display='none';return;}
    hov.innerHTML=`<circle cx="${X(b.x)}" cy="${Y(b.y)}" r="9" fill="none" stroke="var(--ink)" stroke-width="2"/>`;tip.innerHTML=cfg.tip(b);tip.style.display='block';
    let left=X(b.x)+14;if(left+tip.offsetWidth>box.clientWidth)left=X(b.x)-tip.offsetWidth-14;tip.style.left=Math.max(0,left)+'px';tip.style.top=Math.max(0,Y(b.y)-20)+'px';};
  hit.addEventListener('pointermove',move);hit.addEventListener('pointerdown',move);hit.addEventListener('pointerleave',()=>{hov.innerHTML='';tip.style.display='none';});
}
function drawMoney(){
  const si=+MOSEL.value,{rows,reg}=moneyRows(si),part=si>S.indexOf('2022-23'),sy=rows.length?(rows[0].tr.gbp?'£':'€'):'';
  $('moNote').textContent=part?`${S[si]}: net spend only (in pounds), for the clubs that are in the 2026-27 league, so ${rows.length} of this season's clubs are shown.${si===CUR?' This season covers the summer window only.':''}`:`${S[si]}: gross spend, income and net, in euros, for every club (disclosed fees only; free transfers and undisclosed fees count as zero).`;
  const sel=rows.find(o=>o.t===team);
  const tiles=[['Clubs shown',rows.length+'','with spending data'],['Spending explains',reg?Math.round(reg.r2*100)+'%':'-','of the points gaps between these clubs'],['Each extra '+sy+'10m',reg?sgn(+(reg.b*10).toFixed(1))+' pts':'-','average points on the line']];
  if(sel)tiles.push([T[team],ord(sel.pos),`${sel.Pts} pts, spend rank ${sel.spendRank} of ${rows.length}`]);
  $('moTiles').innerHTML=tiles.map(t=>`<div class="tile"><span class="k">${t[0]}</span><span class="v">${t[1]}</span><span class="s">${t[2]}</span></div>`).join('');
  $('scatTitle').textContent=`Net spend against points, ${S[si]}`;
  scatter('scatSvg','tipS',rows.map(o=>({x:o.tr.net,y:o.Pts,t:o.t,l:T[o.t],lab:o.spendRank<=3||o.pos<=3||o.pos>=19,o})),{xl:`Net transfer spend (${sy}m, negative = net income)`,reg,
    tip:p=>`<b>${p.l}</b><div><span>Finished</span><b>${ord(p.o.pos)}</b></div><div><span>Points</span><b>${p.o.Pts}</b></div><div><span>Net spend</span><b>${sy}${Math.round(p.x)}m</b></div>${p.o.res!==null?`<div><span>Vs line</span><b>${sgn(Math.round(p.o.res))} pts</b></div>`:''}`});
  $('moTitle').textContent=`Club by club, ${S[si]}`;
  const hasG=rows.length&&rows[0].tr.gross;
  let h='<thead><tr><th>Spend rank</th><th class="l">Club</th>'+(hasG?'<th>Spent</th><th>Sold</th>':'')+'<th>Net spend</th><th>Finish</th><th>Pts</th><th>Rank gap</th><th>Pts vs line</th><th class="l">Manager</th></tr></thead><tbody>';
  [...rows].sort((a,b)=>a.spendRank-b.spendRank).forEach(o=>{const mm=mainMgr(si,o.t);
    h+=`<tr class="row ${o.t===team?'sel':''}" data-t="${o.t}"><td>${o.spendRank}</td><td class="l">${T[o.t]}</td>${hasG?`<td>${sy}${Math.round(o.tr.spend)}m</td><td>${sy}${Math.round(o.tr.inc)}m</td>`:''}<td><b>${sy}${mfmt(o.tr.net)}</b></td><td>${o.pos}</td><td>${o.Pts}</td><td><span class="delta ${o.gap>0?'up':o.gap<0?'down':''}">${sgn(o.gap)}</span></td><td>${o.res===null?'':sgn(Math.round(o.res))}</td><td class="l">${mm?mm.name:'-'}</td></tr>`;});
  $('moTable').innerHTML=h+'</tbody>';
  $('moTable').querySelectorAll('tr.row').forEach(tr=>tr.addEventListener('click',()=>pick(+tr.dataset.t)));
  r2Chart();bestWorst();
}
function r2Chart(){
  const svg=$('r2Svg'),dm=dims(svg.parentElement),W=dm.W,H=dm.H||320,m={l:40,r:10,t:12,b:40},iw=W-m.l-m.r,ih=H-m.t-m.b,band=iw/S.length,bw=Math.min(26,band*.6);
  const vals=S.map((_,si)=>{const r=moneyRows(si);return r.reg&&r.rows.length>=8?r.reg.r2:null;});const rot_=band<46;
  let g='';[0,.2,.4,.6,.8,1].forEach(v=>{const y=m.t+ih-v*ih;g+=`<line x1="${m.l}" x2="${W-m.r}" y1="${y}" y2="${y}" stroke="var(--grid)"/><text x="${m.l-6}" y="${y+4}" text-anchor="end">${Math.round(v*100)}%</text>`;});
  vals.forEach((v,i)=>{const cx=m.l+band*i+band/2,part=i>S.indexOf('2022-23');
    if(v!==null){const y=m.t+ih-v*ih;g+=`<rect x="${cx-bw/2}" y="${y}" width="${bw}" height="${v*ih}" fill="var(--cur)" opacity="${part?.4:1}"><title>${S[i]}: ${Math.round(v*100)}%</title></rect><text x="${cx}" y="${y-4}" text-anchor="middle" style="fill:var(--ink);font-size:11px;font-weight:700">${Math.round(v*100)}</text>`;}
    g+=`<text x="${cx}" y="${H-m.b+16}" text-anchor="${rot_?'end':'middle'}" transform="rotate(${rot_?-40:0} ${cx} ${H-m.b+16})">${rot_?S[i].slice(2):S[i]}</text>`;});
  svg.setAttribute('viewBox',`0 0 ${W} ${H}`);svg.setAttribute('width',W);svg.setAttribute('height',H);svg.innerHTML=g;
}
function bestWorst(){
  const all=[];S.forEach((_,si)=>{if(si>S.indexOf('2022-23'))return;const r=moneyRows(si);r.rows.forEach(o=>all.push({si,o,res:o.res}));});
  all.sort((a,b)=>b.res-a.res);
  const mk=list=>{let h='<thead><tr><th class="l">Season</th><th class="l">Club</th><th>Net spend</th><th>Finish</th><th>Pts</th><th>Vs line</th></tr></thead><tbody>';
    list.forEach(x=>{h+=`<tr class="row" data-t="${x.o.t}"><td class="l">${S[x.si]}</td><td class="l">${T[x.o.t]}</td><td>€${mfmt(x.o.tr.net)}</td><td>${x.o.pos}</td><td>${x.o.Pts}</td><td><b>${sgn(Math.round(x.res))}</b></td></tr>`;});return h+'</tbody>';};
  $('bestTable').innerHTML=mk(all.slice(0,10));$('worstTable').innerHTML=mk(all.slice(-10).reverse());
  [$('bestTable'),$('worstTable')].forEach(t=>t.querySelectorAll('tr.row').forEach(tr=>tr.addEventListener('click',()=>pick(+tr.dataset.t))));
}

/* ---------- managers ---------- */
let mgCare=false;
const PS={};
MG.forEach(g=>{const o=TS[g.i];if(!o)return;const p=PS[g.name]||(PS[g.name]={name:g.name,g:0,w:0,d:0,l:0,gf:0,ga:0,clubs:new Set(),spells:[],care:true});p.g+=o.g;p.w+=o.w;p.d+=o.d;p.l+=o.l;p.gf+=o.gf;p.ga+=o.ga;p.clubs.add(T[g.club]);p.spells.push({g,o});if(!g.care)p.care=false;});
$('mgMin').addEventListener('input',()=>drawMgrs());$('mgSearch').addEventListener('input',()=>drawMgrs());
$('mgCare').onclick=()=>{mgCare=!mgCare;$('mgCare').setAttribute('aria-pressed',mgCare);drawMgrs();};
let mgSort={k:'ppg',dir:-1},mgOpen=null;
function drawMgrs(){
  const min=+$('mgMin').value,q=$('mgSearch').value.trim().toLowerCase();$('mgMinV').textContent=min;
  let list=Object.values(PS).filter(p=>p.g>=min&&(mgCare||!p.care)&&(!q||p.name.toLowerCase().includes(q)||[...p.clubs].some(c=>c.toLowerCase().includes(q)))).map(p=>({...p,ppg:(p.w*3+p.d)/p.g,win:p.w/p.g,gd:(p.gf-p.ga)/p.g}));
  const k=mgSort.k;list.sort((a,b)=>{const x=k==='name'?a.name:a[k],y=k==='name'?b.name:b[k];return (x<y?-1:x>y?1:0)*mgSort.dir;});
  const cols=[['name','Manager','l'],['clubs','Clubs','l'],['g','Games'],['w','W'],['d','D'],['l','L'],['ppg','Pts/g'],['win','Win %'],['gd','Goal diff/g']];
  let h='<thead><tr>'+cols.map(([key,lab,cl])=>`<th class="s ${cl||''}" data-k="${key}" ${key===k?`aria-sort="${mgSort.dir>0?'ascending':'descending'}"`:''}>${lab}</th>`).join('')+'</tr></thead><tbody>';
  list.slice(0,300).forEach((p,i)=>{h+=`<tr class="row ${mgOpen===p.name?'sel':''}" data-n="${p.name.replace(/"/g,'&quot;')}"><td class="l">${p.name}${p.care?' <span class="zero">(caretaker)</span>':''}</td><td class="l">${[...p.clubs].join(', ')}</td><td>${p.g}</td><td>${p.w}</td><td>${p.d}</td><td>${p.l}</td><td><b>${p.ppg.toFixed(2)}</b></td><td>${Math.round(p.win*100)}%</td><td>${sgn(+p.gd.toFixed(2))}</td></tr>`;
    if(mgOpen===p.name){h+=`<tr class="detail"><td colspan="9" class="l" style="white-space:normal;background:var(--soft)">${p.spells.sort((a,b)=>a.g.from<b.g.from?-1:1).map(s=>`${T[s.g.club]}: ${s.g.from<'2007-07-01'?'before 2007':dt(s.g.from)} to ${s.g.until>'9000'?'present':dt(s.g.until)}, ${s.o.g} games, ${((s.o.w*3+s.o.d)/s.o.g).toFixed(2)} pts/g`).join('<br>')}</td></tr>`;}});
  $('mgTable').innerHTML=h+(list.length?'':'<tr><td class="l" colspan="9">No managers fit these filters.</td></tr>')+'</tbody>';
  $('mgTable').querySelectorAll('th.s').forEach(th=>th.addEventListener('click',()=>{const key=th.dataset.k;mgSort=mgSort.k===key?{k:key,dir:-mgSort.dir}:{k:key,dir:key==='name'||key==='clubs'?1:-1};drawMgrs();}));
  $('mgTable').querySelectorAll('tr.row').forEach(tr=>tr.addEventListener('click',()=>{const n=tr.dataset.n;mgOpen=mgOpen===n?null:n;drawMgrs();}));
  mgTiles(list);changes();bounce();
}
function mgTiles(list){
  const perm=Object.values(PS).filter(p=>!p.care&&p.g>=100).map(p=>({...p,ppg:(p.w*3+p.d)/p.g})).sort((a,b)=>b.ppg-a.ppg);
  const longest=MG.filter(g=>TS[g.i]).sort((a,b)=>TS[b.i].g-TS[a.i].g)[0];
  const cur=MG.filter(g=>g.until>'9000'&&!g.care&&curSet.has(g.club));
  const newest=cur.sort((a,b)=>a.from<b.from?1:-1)[0],oldest=cur.sort((a,b)=>a.from<b.from?-1:1)[0];
  const tiles=[['Best points per game',perm[0].ppg.toFixed(2),perm[0].name+', min 100 games'],['Most league games in one spell',TS[longest.i].g+'',`${longest.name}, ${T[longest.club]}`],['Longest-serving now',oldest.name,`${T[oldest.club]}, since ${dt(oldest.from)}`],['Newest appointment',newest.name,`${T[newest.club]}, ${dt(newest.from)}`],['Managers in the data',Object.keys(PS).length+'','since 2007-08, incl. caretakers']];
  $('mgTiles').innerHTML=tiles.map(t=>`<div class="tile"><span class="k">${t[0]}</span><span class="v" style="font-size:${t[1].length>10?'20px':'32px'}">${t[1]}</span><span class="s">${t[2]}</span></div>`).join('');
}
function changes(){
  let h='<thead><tr><th class="l">Season</th><th>Managers used</th><th>Mid-season changes</th><th>Caretaker spells</th><th class="l">Clubs that changed mid-season</th></tr></thead><tbody>';
  for(let si=S.length-1;si>=0;si--){
    const clubs={};MS[si].forEach(m=>{[[m.h,m.hm],[m.a,m.am]].forEach(([t,id])=>{(clubs[t]||(clubs[t]=new Set())).add(id);});});
    let used=0,chg=0,care=0;const names=[];
    Object.entries(clubs).forEach(([t,set])=>{const ids=[...set];const perm=ids.filter(i=>!MG[i].care);used+=perm.length;care+=ids.length-perm.length;if(perm.length>1||ids.length>perm.length&&perm.length>=1&&ids.length>1){const c=Math.max(0,ids.length-1);if(perm.length>1||(ids.length>1)){chg+=perm.length>1?perm.length-1:0;if(perm.length>1)names.push(T[+t]);}}});
    h+=`<tr><td class="l">${S[si]}${si===CUR?' (so far)':''}</td><td>${used}</td><td><b>${chg}</b></td><td>${care}</td><td class="l" style="white-space:normal">${names.join(', ')||'<span class="zero">none</span>'}</td></tr>`;}
  $('chgTable').innerHTML=h+'</tbody>';
}
function bounce(){
  const cases=[];
  S.forEach((_,si)=>{const byClub={};MS[si].forEach(m=>{(byClub[m.h]||(byClub[m.h]=[])).push({d:m.d,gf:m.hg,ga:m.ag,id:m.hm});(byClub[m.a]||(byClub[m.a]=[])).push({d:m.d,gf:m.ag,ga:m.hg,id:m.am});});
    Object.entries(byClub).forEach(([t,g])=>{g.sort((a,b)=>a.d<b.d?-1:1);for(let i=1;i<g.length;i++){if(g[i].id!==g[i-1].id&&!MG[g[i].id].care){
      const bef=g.slice(Math.max(0,i-10),i),aft=g.slice(i,i+10);if(bef.length<5||aft.length<5)continue;
      const pp=a=>a.reduce((x,y)=>x+(y.gf>y.ga?3:y.gf===y.ga?1:0),0)/a.length;
      cases.push({si,t:+t,mgr:MG[g[i].id].name,prev:MG[g[i-1].id].name,care:MG[g[i-1].id].care,before:pp(bef),after:pp(aft),nb:bef.length,na:aft.length,game:i+1});}}});});
  const avg=a=>a.reduce((x,y)=>x+y,0)/a.length,better=cases.filter(c=>c.after>c.before).length;
  $('bounceHint').textContent=`${cases.length} mid-season appointments of a permanent manager, comparing the 10 league games before and after (at least 5 each side). Managers usually arrive after bad runs, so some improvement is expected anyway: bad runs tend to end whoever is in charge.`;
  $('bounceTiles').innerHTML=[['Points per game before',avg(cases.map(c=>c.before)).toFixed(2),'Average over all cases'],['Points per game after',avg(cases.map(c=>c.after)).toFixed(2),'Average over all cases'],['Improved',Math.round(better/cases.length*100)+'%',`${better} of ${cases.length} cases`]].map(t=>`<div class="tile"><span class="k">${t[0]}</span><span class="v">${t[1]}</span><span class="s">${t[2]}</span></div>`).join('');
  const rows=[...cases].sort((a,b)=>(b.after-b.before)-(a.after-a.before));
  const top=rows.slice(0,8),bot=rows.slice(-8).reverse();
  let h='<thead><tr><th class="l">Season</th><th class="l">Club</th><th class="l">Arrived</th><th class="l">Replaced</th><th>Pts/g before</th><th>Pts/g after</th><th>Change</th></tr></thead><tbody><tr><td class="l" colspan="7"><b>Biggest bounces</b></td></tr>';
  const row=c=>`<tr class="row" data-t="${c.t}"><td class="l">${S[c.si]}</td><td class="l">${T[c.t]}</td><td class="l">${c.mgr}</td><td class="l">${c.prev}${c.care?' (caretaker)':''}</td><td>${c.before.toFixed(2)}</td><td>${c.after.toFixed(2)}</td><td><b>${sgn(+(c.after-c.before).toFixed(2))}</b></td></tr>`;
  h+=top.map(row).join('')+'<tr><td class="l" colspan="7"><b>Biggest drops</b></td></tr>'+bot.map(row).join('');
  $('bounceTable').innerHTML=h+'</tbody>';
  $('bounceTable').querySelectorAll('tr.row').forEach(tr=>tr.addEventListener('click',()=>pick(+tr.dataset.t)));
}
'''
rep("/* ---------- draw ---------- */",code+"\n/* ---------- draw ---------- */")
rep("  if(v==='seasons')drawSeasons();","  if(v==='seasons')drawSeasons();\n  if(v==='money')drawMoney();\n  if(v==='mgrs')drawMgrs();")
# footer
rep("Four Champions League places are assumed throughout.","Four Champions League places are assumed throughout. Managers: Wikipedia list of Premier League managers, matched to games by date. Transfers: Transfermarkt figures via github.com/ewenme/transfers (euros, 2007-08 to 2022-23, disclosed fees only) and a Football365 net-spend table (pounds, 2023-24 onward, clubs now in the league).")
open('/home/claude/app2/template.html','w').write(s)
open('/home/claude/app2/index.html','w').write(s.replace('__DATA__',open('/home/claude/app2/data.json').read().replace('</','<\\/')))
print('ok')
