import csv, sys, re
sys.path.insert(0,'/home/claude/scripts')
from collections import defaultdict
exec(open('/home/claude/scripts/build_all.py').read().split("def seasons()")[0])  # reuse nm/CANON
rows=list(csv.DictReader(open('/home/claude/allmatches.csv',encoding='utf-8')))
of2627={(r['home'],r['away']):(r['hg'],r['ag']) for r in rows if r['season']=='2026-27'}
rows=[r for r in rows if r['season']!='2026-27']
v=[l.strip().split(', ') for l in open('/home/claude/scripts/results_2026_27.txt') if l.strip()]
new=[]
for d,h,a,hg,ag in v:
    h,a=nm(h),nm(a); 
    if (h,a) in of2627 and of2627[(h,a)]!=(hg,ag): print('MISMATCH',h,a,of2627[(h,a)],hg,ag)
    new.append(dict(season='2026-27',date=d,home=h,away=a,hg=hg,ag=ag,hy='',ay='',hr='',ar='',src=''))
print('openfootball 2026-27 games not in vavel:',[k for k in of2627 if k not in {(r['home'],r['away']) for r in new}])
# Chelsea hand-collected cards 2026-27: date -> (chelsea Y,R, opp Y,R)
cards={'2026-08-24':(3,0,2,0),'2026-08-30':(1,0,3,0),'2026-09-06':(4,0,2,0),'2026-09-12':(1,0,5,0),'2026-09-18':(0,0,2,0),'2026-10-10':(0,0,4,0),'2026-10-17':(4,0,3,0),'2026-10-24':(3,1,3,0),'2026-10-31':(1,0,1,1)}
for r in new:
    if 'Chelsea' in (r['home'],r['away']) and r['date'] in cards:
        cy,cr,oy,orr=cards[r['date']]
        if r['home']=='Chelsea': r['hy'],r['hr'],r['ay'],r['ar']=cy,cr,oy,orr
        else: r['ay'],r['ar'],r['hy'],r['hr']=cy,cr,oy,orr
        r['src']='match reports (Chelsea games only)'
rows+=new
rows.sort(key=lambda r:(r['season'],r['date'],r['home']))
w=csv.DictWriter(open('/home/claude/allmatches_final.csv','w',newline='',encoding='utf-8'),fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
# tables
DED={('2009-10','Portsmouth'):9,('2023-24','Everton'):8,('2023-24','Nottingham Forest'):4}
T=defaultdict(lambda:defaultdict(lambda:dict(P=0,W=0,D=0,L=0,GF=0,GA=0,Y=0,R=0)))
for r in rows:
    hg,ag=int(r['hg']),int(r['ag'])
    for team,gf,ga,y,rd in ((r['home'],hg,ag,r['hy'],r['hr']),(r['away'],ag,hg,r['ay'],r['ar'])):
        t=T[r['season']][team]; t['P']+=1; t['GF']+=gf; t['GA']+=ga
        t['W' if gf>ga else 'D' if gf==ga else 'L']+=1
for sn in T:
    for team,t in T[sn].items(): t['Pts']=t['W']*3+t['D']-DED.get((sn,team),0); t['GD']=t['GF']-t['GA']
order={}
for sn in sorted(T):
    order[sn]=sorted(T[sn].items(),key=lambda kv:(-kv[1]['Pts'],-kv[1]['GD'],-kv[1]['GF']))
import json
json.dump({sn:[(t,s) for t,s in order[sn]] for sn in order},open('/home/claude/tables.json','w'))
for sn in sorted(order):
    top=order[sn][0]; print(sn,'1st',top[0],top[1]['Pts'],'| 2nd',order[sn][1][0],order[sn][1][1]['Pts'],'| last',order[sn][-1][0],order[sn][-1][1]['Pts'],'| teams',len(order[sn]))
chel={"2007-08":2,"2008-09":3,"2009-10":1,"2010-11":2,"2011-12":6,"2012-13":3,"2013-14":3,"2014-15":1,"2015-16":10,"2016-17":1,"2017-18":5,"2018-19":3,"2019-20":4,"2020-21":4,"2021-22":3,"2022-23":12,"2023-24":6,"2024-25":4,"2025-26":10}
bad=[(sn,[t for t,_ in order[sn]].index('Chelsea')+1,p) for sn,p in chel.items() if [t for t,_ in order[sn]].index('Chelsea')+1!=p]
print('Chelsea position mismatches:',bad)
print('2025-26 top7',[(t,s['Pts']) for t,s in order['2025-26'][:10]])
