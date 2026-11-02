import re
s=open('/home/claude/app2/template.html').read()
a=s.index('<section class="view" id="v-money">'); b=s.index('<section class="view" id="v-mgrs">')
new_html='''<section class="view" id="v-money">
  <div class="card">
    <h2>Did the money help?</h2>
    <p class="hint">Pick how many seasons of spending to add up and the season they end in. We compare each club's points the season before the spending started with its points in the final season, and see whether the biggest spenders improved more than everyone else.</p>
    <div class="controls">
      <label class="f" for="moYears">Years of spending<select id="moYears"><option value="1">1 season</option><option value="2">2 seasons</option><option value="3" selected>3 seasons</option><option value="4">4 seasons</option><option value="5">5 seasons</option></select></label>
      <label class="f" for="moEnd">Ending in<select id="moEnd"></select></label>
    </div>
    <p class="hint" id="moNote"></p>
  </div>
  <div class="card" id="moHeadCard"><h2 id="moHeadTitle"></h2><p id="moHead" style="margin:6px 0 0;max-width:80ch"></p></div>
  <div class="tiles" id="moTiles"></div>
  <div class="card">
    <h2 id="moTitle">Club by club</h2>
    <p class="hint">Blue bars show net spending (money paid minus money received), green or red bars show the change in league points. Verdicts: <b>Helped</b> means an above-median spender gained 8 or more points. <b>Did not help</b> means an above-median spender lost 8 or more. Clubs that spent less are labelled by what happened to them. Everything in between is <b>little change</b>.</p>
    <div class="tablewrap"><table id="moTable"></table></div>
  </div>
  <div class="card" id="cardDb">
    <div class="cardhead"><div><h2 id="dbTitle">Spending rank against finishing rank</h2><p class="hint">One row per club, biggest spender at the top. The grey dot is where the club ranks for net spending that season, the blue dot is where it finished. A green line means it finished higher than its spending suggests, red means lower.</p></div>
      <div class="chips"><button class="btn expandbtn" data-card="cardDb">Expand</button><span class="fullbar"><button class="btn" data-act="rotate" aria-pressed="false">Rotate</button><button class="btn" data-act="close">Close</button></span></div></div>
    <div class="chartbox"><svg id="dbSvg" role="img" aria-label="Spending rank against finishing rank for each club"></svg></div>
  </div>
  <div class="card">
    <h2>Do big spenders finish higher?</h2>
    <p class="hint">Every season from 2007-08 to 2022-23, clubs are grouped by how much they spent in net terms that season (80 club-seasons per group), then we look at how each group finished.</p>
    <div class="tablewrap"><table id="bandTable"></table></div>
  </div>
  <div class="cols two">
    <div class="card"><h2>Spent least, finished highest</h2><p class="hint">The biggest gaps between spending rank and finishing rank, 2007-08 to 2022-23 (rank among all 20 clubs).</p><div class="tablewrap"><table id="bestTable"></table></div></div>
    <div class="card"><h2>Spent most, finished lowest</h2><p class="hint">The biggest gaps the other way, same seasons.</p><div class="tablewrap"><table id="worstTable"></table></div></div>
  </div>
</section>

'''
s=s[:a]+new_html+s[b:]
a=s.index('/* ---------- money ---------- */'); b=s.index('/* ---------- managers ---------- */')
js=r'''/* ---------- money ---------- */
const FXR=D.fx||1.19;
const netE=(si,t)=>{const x=TRK[si+'|'+t];return x&&x.net!==null?(x.gbp?x.net*FXR:x.net):null;};
const LASTFULL=S.indexOf('2022-23');
$('moEnd').innerHTML=S.map((s,i)=>i>=1&&i<CUR?`<option value="${i}">${s}${i>LASTFULL?' (current clubs only)':''}</option>`:'').filter(Boolean).reverse().join('');$('moEnd').value=LASTFULL;
$('moEnd').addEventListener('change',drawMoney);$('moYears').addEventListener('change',drawMoney);
const mE=v=>(v<-0.5?'&minus;':'')+'€'+Math.abs(Math.round(v))+'m';
function windowRows(end,N){
  const s0=end-N+1,base=s0-1;if(base<0)return {rows:[],s0,base};
  const rows=[];
  T.forEach((_,t)=>{
    let ok=true,spend=0;
    for(let si=base;si<=end;si++){if(!rowOf(si,t)){ok=false;break;}}
    if(!ok)return;
    for(let si=s0;si<=end;si++){const v=netE(si,t);if(v===null){ok=false;break;}spend+=v;}
    if(!ok)return;
    const b=rowOf(base,t),e=rowOf(end,t);
    rows.push({t,spend,before:b.Pts,after:e.Pts,delta:e.Pts-b.Pts,fb:b.pos,fa:e.pos});
  });
  [...rows].sort((a,b)=>b.spend-a.spend).forEach((r,i)=>r.rank=i+1);
  const med=rows.length?[...rows].map(r=>r.spend).sort((a,b)=>a-b)[Math.floor(rows.length/2)]:0;
  rows.forEach(r=>{r.hi=r.spend>=med;
    r.verdict=r.hi?(r.delta>=8?['W','Helped']:r.delta<=-8?['L','Did not help']:['D','Little change']):(r.delta>=8?['W','Improved on a budget']:r.delta<=-8?['L','Declined']:['D','Little change']);});
  return {rows,s0,base,med};
}
function drawMoney(){
  const end=+$('moEnd').value,N=+$('moYears').value,{rows,s0,base}=windowRows(end,N);
  const span=N===1?S[end]:`${S[s0]} to ${S[end]}`;
  const part=end>LASTFULL;
  $('moNote').innerHTML=`Spending: net fees across ${N===1?'the summer and winter windows of '+S[end]:'all windows from '+S[s0]+' to '+S[end]}. Compared with points in ${S[base]}. ${part?'Seasons after 2022-23 only have net spending for clubs now in the league, in pounds, converted to euros at about '+FXR.toFixed(2)+' per pound. ':'Euros, disclosed fees only. '}Only clubs in the league for every season from ${S[base]} to ${S[end]} are compared (${rows.length} clubs).`;
  $('moTitle').textContent=`Club by club: ${span}`;
  const me=rows.find(r=>r.t===team);
  if(me){
    const v=me.verdict[1],cls=me.hi;
    const txt=me.hi?(me.delta>=8?'So the spending helped.':me.delta<=-8?'So the spending did not help.':'So the spending did not change much.'):(me.delta>=8?'It improved without big spending.':me.delta<=-8?'It declined, and it did not spend much.':'Little changed, and it did not spend much.');
    $('moHeadTitle').textContent=T[team];
    $('moHead').innerHTML=`${T[team]} spent a net <b>≈${mE(me.spend)}</b> over ${span}, ${ord(me.rank)} highest of ${rows.length} clubs. Points went from <b>${me.before}</b> in ${S[base]} to <b>${me.after}</b> in ${S[end]} (<b>${sgn(me.delta)}</b>), and the club moved from ${ord(me.fb)} to ${ord(me.fa)}. ${txt}`;
  }else{
    $('moHeadTitle').textContent=T[team];
    $('moHead').textContent=`${T[team]} cannot be compared for ${span}: it needs to be in the Premier League for every season from ${S[base]} to ${S[end]} with spending data${part?' (after 2022-23 only clubs now in the league have it)':''}. Try a different window or pick another club.`;
  }
  const top=[...rows].sort((a,b)=>a.rank-b.rank).slice(0,5),rest=rows.filter(r=>r.rank>5);
  const av=a=>a.length?a.reduce((x,y)=>x+y.delta,0)/a.length:0;
  const tiles=[['Biggest 5 spenders',sgn(+av(top).toFixed(1))+' pts','Average change in points'],['All other clubs',sgn(+av(rest).toFixed(1))+' pts','Average change in points'],['Big spenders who improved',top.filter(r=>r.delta>0).length+' of '+top.length,'Top 5 by net spending'],['Clubs compared',rows.length+'','in the league the whole time']];
  $('moTiles').innerHTML=tiles.map(t=>`<div class="tile"><span class="k">${t[0]}</span><span class="v">${t[1]}</span><span class="s">${t[2]}</span></div>`).join('');
  const maxS=Math.max(1,...rows.map(r=>Math.abs(r.spend))),maxD=Math.max(10,...rows.map(r=>Math.abs(r.delta)));
  let h='<thead><tr><th>Spend rank</th><th class="l">Club</th><th class="l" style="min-width:210px">Net spend</th><th>Points before</th><th>Points after</th><th class="l" style="min-width:210px">Change in points</th><th class="l">Verdict</th></tr></thead><tbody>';
  [...rows].sort((a,b)=>a.rank-b.rank).forEach(r=>{
    const sw=Math.round(Math.abs(r.spend)/maxS*110),dw=Math.round(Math.abs(r.delta)/maxD*90);
    h+=`<tr class="row ${r.t===team?'sel':''}" data-t="${r.t}"><td>${r.rank}</td><td class="l">${T[r.t]}</td><td class="l"><span class="bar" style="width:${sw}px;${r.spend<0?'background:var(--gray)':''}"></span> ${mE(r.spend)}</td><td>${r.before}</td><td>${r.after}</td><td class="l"><span style="display:inline-block;width:92px;text-align:right">${r.delta<0?`<span class="bar" style="width:${dw}px;background:var(--bad)"></span>`:''}</span><span style="display:inline-block;width:92px">${r.delta>0?`<span class="bar" style="width:${dw}px;background:var(--good)"></span>`:''}</span> <b>${sgn(r.delta)}</b></td><td class="l"><span class="pill ${r.verdict[0]}" style="white-space:nowrap">${r.verdict[1]}</span></td></tr>`;});
  $('moTable').innerHTML=h+'</tbody>';
  $('moTable').querySelectorAll('tr.row').forEach(tr=>tr.addEventListener('click',()=>pick(+tr.dataset.t)));
  dumbbell(end);bands();bestWorst();
}
function dumbbell(si){
  const {rows}=moneyRows(si),svg=$('dbSvg'),dm=dims(svg.parentElement),W=dm.W,n=rows.length;
  $('dbTitle').textContent=`Spending rank against finishing rank, ${S[si]}`;
  if(n<4){svg.innerHTML='';return;}
  const m={l:W<520?110:150,r:24,t:40,b:16},H=dm.H||Math.max(280,n*26+m.t+m.b),rowH=(H-m.t-m.b)/n,iw=W-m.l-m.r,X=r=>m.l+(r-1)/(n-1)*iw;
  let g=`<text x="${m.l}" y="14" style="font-weight:700;fill:var(--ink)">1st</text><text x="${W-m.r}" y="14" text-anchor="end" style="font-weight:700;fill:var(--ink)">${ord(n)}</text><text x="${m.l+iw/2}" y="14" text-anchor="middle">Rank (1st = biggest spender / best finish)</text>`;
  [1,Math.round(n/4),Math.round(n/2),Math.round(3*n/4),n].forEach(r=>{g+=`<line x1="${X(r)}" x2="${X(r)}" y1="${m.t-6}" y2="${H-m.b}" stroke="var(--grid)"/><text x="${X(r)}" y="${m.t-12}" text-anchor="middle">${r}</text>`;});
  [...rows].sort((a,b)=>a.spendRank-b.spendRank).forEach((o,i)=>{const y=m.t+i*rowH+rowH/2,sel=o.t===team,c=o.posRank<o.spendRank?'var(--good)':o.posRank>o.spendRank?'var(--bad)':'var(--gray)';
    g+=`<text x="${m.l-10}" y="${y+4}" text-anchor="end" style="fill:var(--ink);font-weight:${sel?700:400}">${T[o.t]}</text>`;
    g+=`<line x1="${X(o.spendRank)}" x2="${X(o.posRank)}" y1="${y}" y2="${y}" stroke="${c}" stroke-width="3" opacity=".8"/>`;
    g+=`<circle cx="${X(o.spendRank)}" cy="${y}" r="5" fill="#fff" stroke="#8a8a8a" stroke-width="2"><title>${T[o.t]}: spending rank ${o.spendRank}</title></circle><circle cx="${X(o.posRank)}" cy="${y}" r="${sel?7:5.5}" fill="var(--cur)"><title>${T[o.t]}: finished ${ord(o.pos)} (rank ${o.posRank} of the clubs shown)</title></circle>`;});
  svg.setAttribute('viewBox',`0 0 ${W} ${H}`);svg.setAttribute('width',W);svg.setAttribute('height',H);svg.innerHTML=g;
}
function bands(){
  const acc=[0,1,2,3,4].map(()=>({n:0,pos:0,pts:0,t4:0,rel:0,t1:0}));
  S.forEach((_,si)=>{if(si>LASTFULL)return;const {rows}=moneyRows(si);rows.forEach(o=>{const b=Math.min(4,Math.floor((o.spendRank-1)/4)),a=acc[b];a.n++;a.pos+=o.pos;a.pts+=o.Pts;if(o.pos<=4)a.t4++;if(o.pos>=18)a.rel++;if(o.pos===1)a.t1++;});});
  const lab=['Biggest 4 spenders (rank 1-4)','Next 4 (5-8)','Middle 4 (9-12)','Next 4 (13-16)','Smallest 4 (17-20)'];
  let h='<thead><tr><th class="l">Net spending that season</th><th>Club-seasons</th><th>Average finish</th><th>Average points</th><th>Won the title</th><th>Top four</th><th>Bottom three</th></tr></thead><tbody>';
  acc.forEach((a,i)=>{h+=`<tr><td class="l">${lab[i]}</td><td>${a.n}</td><td><b>${(a.pos/a.n).toFixed(1)}</b></td><td>${(a.pts/a.n).toFixed(1)}</td><td>${Math.round(a.t1/a.n*100)}%</td><td><span class="bar" style="width:${Math.round(a.t4/a.n*80)}px"></span> ${Math.round(a.t4/a.n*100)}%</td><td><span class="bar rel" style="width:${Math.round(a.rel/a.n*80)}px"></span> ${Math.round(a.rel/a.n*100)}%</td></tr>`;});
  $('bandTable').innerHTML=h+'</tbody>';
}
function bestWorst(){
  const all=[];S.forEach((_,si)=>{if(si>LASTFULL)return;moneyRows(si).rows.forEach(o=>all.push({si,o}));});
  const mk=list=>{let h='<thead><tr><th class="l">Season</th><th class="l">Club</th><th>Net spend</th><th>Spend rank</th><th>Finish</th></tr></thead><tbody>';
    list.forEach(x=>{h+=`<tr class="row" data-t="${x.o.t}"><td class="l">${S[x.si]}</td><td class="l">${T[x.o.t]}</td><td>${mny(x.o.tr.net,'€')}</td><td>${x.o.spendRank}</td><td><b>${x.o.pos}</b></td></tr>`;});return h+'</tbody>';};
  const up=[...all].sort((a,b)=>(b.o.spendRank-b.o.pos)-(a.o.spendRank-a.o.pos)||a.o.pos-b.o.pos).slice(0,10),down=[...all].sort((a,b)=>(a.o.spendRank-a.o.pos)-(b.o.spendRank-b.o.pos)||b.o.pos-a.o.pos).slice(0,10);
  $('bestTable').innerHTML=mk(up);$('worstTable').innerHTML=mk(down);
  [$('bestTable'),$('worstTable')].forEach(t=>t.querySelectorAll('tr.row').forEach(tr=>tr.addEventListener('click',()=>pick(+tr.dataset.t))));
}

'''
s=s[:a]+js+s[b:]
open('/home/claude/app2/template.html','w').write(s)
open('/home/claude/app2/index.html','w').write(s.replace('__DATA__',open('/home/claude/app2/data.json').read().replace('</','<\\/')))
print('ok')
