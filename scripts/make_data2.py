import csv, json, re
from datetime import date
import pandas as pd
exec(open('/home/claude/scripts/build_all.py').read().split("def seasons()")[0])
rows=list(csv.DictReader(open('/home/claude/allmatches_final.csv',encoding='utf-8')))
seasons=sorted({r['season'] for r in rows})
teams=sorted({r['home'] for r in rows}|{r['away'] for r in rows})
ti={t:i for i,t in enumerate(teams)}; si={s:i for i,s in enumerate(seasons)}
cur26={r['home'] for r in rows if r['season']=='2026-27'}|{r['away'] for r in rows if r['season']=='2026-27'}
iv=lambda x:int(x) if x!='' else None
# managers
mrows=[l.strip().split('|') for l in open('/home/claude/scripts/managers.txt',encoding='utf-8') if l.strip()]
mgr=[[r[1],ti[r[0]],r[2],r[3],int(r[4])] for r in mrows]
byclub={}
for i,t in enumerate(mgr): byclub.setdefault(t[1],[]).append((i,t))
def pick(club,d):
    c=[(i,t) for i,t in byclub.get(club,[]) if t[2]<=d<=t[3]]
    if c:
        perm=[x for x in c if not x[1][4]]; pool=perm or c
        return max(pool,key=lambda x:x[1][2])[0]
    dd=date.fromisoformat(d); best=None;bd=1e9
    for i,t in byclub.get(club,[]):
        f=date.fromisoformat(t[2]); u=date.fromisoformat(t[3] if t[3]<'9999' else '2999-01-01')
        k=min(abs((dd-f).days),abs((dd-u).days))
        if k<bd: bd=k;best=i
    return best
ms=[]
for r in rows:
    ms.append([si[r['season']],r['date'],ti[r['home']],ti[r['away']],int(r['hg']),int(r['ag']),iv(r['hy']),iv(r['ay']),iv(r['hr']),iv(r['ar']),pick(ti[r['home']],r['date']),pick(ti[r['away']],r['date'])])
ms.sort(key=lambda x:(x[1],x[2]))
played={(r['home'],r['away']) for r in rows if r['season']=='2026-27'}
cur=None; fx=[]
for line in open('/home/claude/openfootball/england/2026-27/1-premierleague.txt',encoding='utf-8'):
    m=re.match(r'^\s*(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+(\w{3})\s+(\d+)(?:\s+(\d{4}))?(?=\s|$)',line)
    if m:
        mo=MON[m.group(1)]; yr=int(m.group(3)) if m.group(3) else (2026 if mo>=7 else 2027); cur=date(yr,mo,int(m.group(2))); continue
    if re.search(r'\d+-\d+\s*(\(|$)',line) and ' v ' in line: continue
    m=re.match(r'^\s+(?:\d\d[:.]\d\d\s+)?(.+?)\s+v\s+(.+?)\s*$',line)
    if m and cur:
        h,a=nm(m.group(1)),nm(m.group(2))
        if (h,a) not in played: fx.append([cur.isoformat(),ti[h],ti[a]])
fx.sort()
ded={f"{si['2009-10']}|{ti['Portsmouth']}":9,f"{si['2023-24']}|{ti['Everton']}":8,f"{si['2023-24']}|{ti['Nottingham Forest']}":4}
# transfers
d=pd.read_csv('/home/claude/ewenme/transfers/data/premier-league.csv')
d=d[d.season.isin([f"{y}/{y+1}" for y in range(2007,2023)])].copy(); d['club']=d.club_name.map(nm); d['fee_cleaned']=d.fee_cleaned.fillna(0)
g=d.groupby(['season','club','transfer_movement']).fee_cleaned.sum().unstack(fill_value=0).reset_index(); g.columns.name=None
tr=[]
for _,r in g.iterrows():
    sn=r.season[:4]+'-'+r.season[7:]
    tr.append([si[sn],ti[r.club],round(r['in'],1),round(r['out'],1),round(r['in']-r['out'],1),0,1,0])
f365={'Tottenham':[-173.34,-156.46,-110.39,-125.5,-117],'Manchester United':[-100.82,-147.68,-102.56,-128.48,-191.94],'Arsenal':[-78.91,-246.26,-20.81,-144.26,-141.39],'Chelsea':[35.25,0.1,-19.24,-144.65,-485.17],
'Liverpool':[-200.22,-223.4,29.14,-92.26,-53.96],'Manchester City':[-162.26,-172.7,-87.75,-104.64,5.94],'Newcastle United':[-29.08,-89.94,18.26,-95.55,-149.73],'Nottingham Forest':[19.3,-97.28,-15.58,-42.28,-167.48],
'Ipswich Town':[-172.65,25.98,-130.32,-4.92,-1.65],'AFC Bournemouth':[-57.81,113.26,-59.67,-111.27,-78.57],'Fulham':[-70.25,-48.82,-18.86,-16.55,-42.03],'Sunderland':[-37.74,-133.74,5.41,-1.54,5.08],
'Brentford':[-95.5,43.51,-20.12,-52.3,-38.44],'Coventry City':[-123,-2.91,-18.43,3.24,1.52],'Hull City':[-133.28,5.4,9.85,-8.21,6.36],'Crystal Palace':[37.72,-41.27,7.45,-56.2,-34.11],
'Leeds United':[-64.6,-91.51,109.47,-1.95,-41.44],'Aston Villa':[55.81,-14,39.54,-65.44,-38.25],'Everton':[21.19,-101.87,28.17,36.23,21.7],'Brighton & Hove Albion':[10.86,56.51,-191.58,69.1,70.82]}
x2223={}
for t,v in f365.items(): x2223[t]=-v[4]
# cross-check 2022-23 rank agreement
e=g[g.season=='2022/2023'].set_index('club'); e['net']=e['in']-e['out']
common=[t for t in x2223 if t in e.index]
a=pd.Series({t:e.loc[t,'net'] for t in common}); b=pd.Series({t:x2223[t] for t in common})
print('2022-23 rank corr (ewenme EUR vs football365 GBP) n=',len(common),round(a.rank().corr(b.rank()),3))
for t,v in f365.items():
    for k,s in enumerate(['2026-27','2025-26','2024-25','2023-24']):
        tr.append([si[s],ti[t],None,None,round(-v[k],2),1,0,1 if s=='2026-27' else 0])
data=dict(teams=teams,seasons=seasons,matches=ms,fixtures=fx,ded=ded,current=sorted(ti[t] for t in cur26),mgr=mgr,tr=tr)
json.dump(data,open('/home/claude/app2/data.json','w'),separators=(',',':'),ensure_ascii=False)
print(len(ms),len(mgr),len(tr),len(open('/home/claude/app2/data.json').read()))
