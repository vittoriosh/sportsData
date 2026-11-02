s=open('/home/claude/app2/template.html').read()
def rep(a,b):
    global s
    assert a in s,a[:80]
    s=s.replace(a,b,1)
card='''<div class="card" id="cardTrj">
    <div class="cardhead"><div><h2 id="trjTitle">Spending and results, last 10 seasons</h2><p class="hint" id="trjSum"></p></div>
      <div class="chips"><button class="btn expandbtn" data-card="cardTrj">Expand</button><span class="fullbar"><button class="btn" data-act="rotate" aria-pressed="false">Rotate</button><button class="btn" data-act="close">Close</button></span></div></div>
    <div class="legendline"><span><i style="background:var(--cur)"></i>Net spent that season</span><span><i style="background:#b9b9b9"></i>Net income from sales</span><span><i style="background:#111"></i>3-season net spend (dashed)</span><span><i style="background:var(--cur);border-radius:50%"></i>League points</span><span><i style="background:#e8a400"></i>Points of 4th place</span></div>
    <div class="chartbox"><svg id="trjSvg" role="img" aria-label="Transfer spending and league points by season"></svg><div class="tip" id="tipT"></div></div>
  </div>
  '''
rep('<div class="card"><h2 id="cmTitle">Managers</h2>',card+'<div class="card"><h2 id="cmTitle">Managers</h2>')
rep("  drawHist();drawClubMgrs();chips();drawLine();\n}\n","  drawTrj();drawHist();drawClubMgrs();chips();drawLine();\n}\n")
code=r'''
function drawTrj(){
  const svg=$('trjSvg'),box=svg.parentElement,dm=dims(box),W=dm.W,H=dm.H||(W<560?480:540),tip=$('tipT');
  const seas=[];for(let si=Math.max(0,CUR-9);si<=CUR;si++)seas.push(si);const n=seas.length;
  const D_=seas.map(si=>{const r=rowOf(si,team),x=TRK[si+'|'+team],part=si===CUR,st=seasonTable(si);
    return {si,r,part,net:netE(si,team),paid:x&&x.gross&&x.spend!==null?x.spend:null,got:x&&x.gross&&x.inc!==null?x.inc:null,gbp:x&&x.gbp,
      pts:r?(part?Math.round(r.Pts/r.P*38):r.Pts):null,pos:r?r.pos:null,four:part?null:(st[3]?st[3].Pts:null),mm:mainMgr(si,team)};});
  D_.forEach((d,i)=>{let sum=0,ok=true;for(let k=0;k<3;k++){const v=D_[i-k]?D_[i-k].net:null;if(v===null||v===undefined){ok=false;break;}sum+=v;}d.roll=ok?sum:null;});
  const have=D_.filter(d=>d.r);
  $('trjTitle').textContent=`${T[team]}: spending and results, ${S[seas[0]]} to ${S[CUR]}`;
  if(!have.length){svg.innerHTML='';$('trjSum').textContent='This club has no league seasons in this period.';return;}
  const done=D_.filter(d=>d.r&&!d.part&&d.net!==null);const l5=done.slice(-5),p5=done.slice(-10,-5);
  const sumN=a=>a.reduce((x,y)=>x+y.net,0),avg=(a,k)=>a.reduce((x,y)=>x+y[k],0)/a.length;
  $('trjSum').innerHTML=l5.length?`Last ${l5.length} completed seasons${p5.length===l5.length?` against the ${p5.length} before`:''}: net spending <b>≈${mE(sumN(l5))}</b>${p5.length===l5.length?` (was ≈${mE(sumN(p5))})`:''}, average points <b>${avg(l5,'pts').toFixed(0)}</b>${p5.length===l5.length?` (was ${avg(p5,'pts').toFixed(0)})`:''}, average finish <b>${avg(l5,'pos').toFixed(1)}</b>${p5.length===l5.length?` (was ${avg(p5,'pos').toFixed(1)})`:''}. Euros up to 2022-23; later seasons are pounds converted at ${FXR.toFixed(2)}. ${S[CUR]} is in progress: points are a 38-game pace and spending is the summer window only.`:'Not enough completed seasons with spending data for a comparison.';
  const m={l:62,r:16,t:22,b:36},gap=44,ih=H-m.t-m.b-gap,hA=ih*.46,hB=ih*.54,iw=W-m.l-m.r,band=iw/n,cx=i=>m.l+band*(i+.5);
  const nets=D_.flatMap(d=>[d.net,d.roll]).filter(v=>v!==null);const ar=nice(Math.max(50,...nets),Math.min(0,...nets));
  const yA=v=>m.t+hA-(v-ar.lo)/(ar.hi-ar.lo)*hA;
  const ptsAll=D_.flatMap(d=>[d.pts,d.four]).filter(v=>v!==null);const br=nice(Math.max(...ptsAll)+6,Math.max(0,Math.min(...ptsAll)-10));
  const y0B=m.t+hA+gap,yB=v=>y0B+hB-(v-br.lo)/(br.hi-br.lo)*hB;let g='';
  g+=`<text x="${m.l}" y="12" style="font-weight:700;fill:var(--ink)">Net transfer spending (≈€m)</text><text x="${m.l}" y="${y0B-10}" style="font-weight:700;fill:var(--ink)">League points</text>`;
  ar.t.forEach(v=>{g+=`<line x1="${m.l}" x2="${W-m.r}" y1="${yA(v)}" y2="${yA(v)}" stroke="${v===0?'var(--muted)':'var(--grid)'}"/><text x="${m.l-6}" y="${yA(v)+4}" text-anchor="end">${v}</text>`;});
  br.t.forEach(v=>{g+=`<line x1="${m.l}" x2="${W-m.r}" y1="${yB(v)}" y2="${yB(v)}" stroke="var(--grid)"/><text x="${m.l-6}" y="${yB(v)+4}" text-anchor="end">${v}</text>`;});
  const bw=Math.min(36,band*.5);
  D_.forEach((d,i)=>{if(d.net===null)return;const y=yA(d.net),z=yA(0);g+=`<rect x="${cx(i)-bw/2}" y="${Math.min(y,z)}" width="${bw}" height="${Math.max(1,Math.abs(z-y))}" fill="${d.net>=0?'var(--cur)':'#b9b9b9'}" opacity="${d.part?.45:1}"/>`;
    g+=`<text x="${cx(i)}" y="${d.net>=0?y-4:y+12}" text-anchor="middle" style="fill:var(--ink);font-size:11px;font-weight:700">${Math.round(d.net)}</text>`;});
  let dd='',pen=false;D_.forEach((d,i)=>{if(d.roll===null){pen=false;return;}dd+=(pen?'L':'M')+cx(i).toFixed(1)+' '+yA(d.roll).toFixed(1);pen=true;});
  g+=`<path d="${dd}" fill="none" stroke="#111" stroke-width="2" stroke-dasharray="5 4"/>`;D_.forEach((d,i)=>{if(d.roll!==null)g+=`<circle cx="${cx(i)}" cy="${yA(d.roll)}" r="3" fill="#111"/>`;});
  let fq='';pen=false;D_.forEach((d,i)=>{if(d.four===null){pen=false;return;}fq+=(pen?'L':'M')+cx(i).toFixed(1)+' '+yB(d.four).toFixed(1);pen=true;});
  g+=`<path d="${fq}" fill="none" stroke="#e8a400" stroke-width="2" stroke-dasharray="2 4"/>`;
  let pp='';pen=false;D_.forEach((d,i)=>{if(d.pts===null){pen=false;return;}pp+=(pen?'L':'M')+cx(i).toFixed(1)+' '+yB(d.pts).toFixed(1);pen=true;});
  g+=`<path d="${pp}" fill="none" stroke="var(--cur)" stroke-width="3" stroke-linejoin="round"/>`;
  D_.forEach((d,i)=>{if(d.pts===null)return;g+=`<circle cx="${cx(i)}" cy="${yB(d.pts)}" r="5.5" fill="${d.part?'#fff':'var(--cur)'}" stroke="var(--cur)" stroke-width="2.5"/><text x="${cx(i)}" y="${yB(d.pts)-11}" text-anchor="middle" style="fill:var(--ink);font-size:11px;font-weight:700">${d.pts}${d.part?'*':''}</text><text x="${cx(i)}" y="${yB(d.pts)+19}" text-anchor="middle" style="font-size:11px">${ord(d.pos)}</text>`;});
  const rot_=band<54;D_.forEach((d,i)=>{const lab=rot_?S[d.si].slice(2):S[d.si];g+=`<text x="${cx(i)}" y="${H-m.b+16}" text-anchor="${rot_?'end':'middle'}" transform="rotate(${rot_?-40:0} ${cx(i)} ${H-m.b+16})" style="${d.part?'font-weight:700;fill:var(--ink)':''}">${lab}${d.part?' so far':''}</text>`;});
  g+='<g id="hov"></g>';D_.forEach((d,i)=>{g+=`<rect class="col" data-i="${i}" x="${m.l+band*i}" y="${m.t-6}" width="${band}" height="${H-m.t-m.b+6}" fill="transparent"/>`;});
  svg.setAttribute('viewBox',`0 0 ${W} ${H}`);svg.setAttribute('width',W);svg.setAttribute('height',H);svg.innerHTML=g;
  const hov=svg.querySelector('#hov');
  const show=i=>{const d=D_[i];hov.innerHTML=`<rect x="${m.l+band*i}" y="${m.t-6}" width="${band}" height="${H-m.t-m.b+6}" fill="var(--ink)" opacity=".06"/>`;
    let t=`<b>${S[d.si]}${d.part?' (so far)':''}</b>`;
    if(!d.r)t+='<div><span>Not in the league</span></div>';else{
      t+=`<div><span>Finished</span><b>${ord(d.pos)}${d.part?' so far':''}</b></div><div><span>Points</span><b>${d.pts}${d.part?' (pace)':''}</b></div><div><span>Manager</span><b>${d.mm?d.mm.name:'-'}</b></div>`;
      t+=d.net===null?'<div><span>Net spend</span><b>n/a</b></div>':`<div><span>Net spend</span><b>≈${mE(d.net)}</b></div>`;
      if(d.paid!==null)t+=`<div><span>Paid</span><b>€${Math.round(d.paid)}m</b></div><div><span>Received</span><b>€${Math.round(d.got)}m</b></div>`;
      if(d.roll!==null)t+=`<div><span>3-season net</span><b>≈${mE(d.roll)}</b></div>`;
      if(d.four!==null)t+=`<div><span>4th place had</span><b>${d.four} pts</b></div>`;}
    tip.innerHTML=t;tip.style.display='block';let left=cx(i)+band/2+8;if(left+tip.offsetWidth>box.clientWidth)left=cx(i)-band/2-tip.offsetWidth-8;tip.style.left=Math.max(0,left)+'px';tip.style.top='8px';};
  svg.querySelectorAll('.col').forEach(r=>{r.addEventListener('pointerenter',()=>show(+r.dataset.i));r.addEventListener('pointermove',()=>show(+r.dataset.i));r.addEventListener('pointerdown',()=>show(+r.dataset.i));r.addEventListener('pointerleave',()=>{hov.innerHTML='';tip.style.display='none';});});
}
'''
rep("function drawClubMgrs(){",code+"function drawClubMgrs(){")
open('/home/claude/app2/template.html','w').write(s)
open('/home/claude/app2/index.html','w').write(s.replace('__DATA__',open('/home/claude/app2/data.json').read().replace('</','<\\/')))
print('ok')
