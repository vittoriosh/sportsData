import csv, re
from datetime import date
MON={m:i+1 for i,m in enumerate("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split())}
NAME={"Man City":"Manchester City","Man United":"Manchester United","Man Utd":"Manchester United","Spurs":"Tottenham","Tottenham Hotspur":"Tottenham",
"Newcastle":"Newcastle United","Newcastle United":"Newcastle United","Wolves":"Wolverhampton","Wolverhampton Wanderers":"Wolverhampton","West Brom":"West Bromwich Albion",
"Leicester":"Leicester City","Brighton":"Brighton & Hove Albion","Bournemouth":"AFC Bournemouth","Huddersfield":"Huddersfield Town","Cardiff":"Cardiff City","Swansea":"Swansea City",
"Stoke":"Stoke City","Hull":"Hull City","QPR":"Queens Park Rangers","Norwich":"Norwich City","Sunderland AFC":"Sunderland","Everton FC":"Everton","Arsenal FC":"Arsenal","Fulham FC":"Fulham",
"Liverpool FC":"Liverpool","Portsmouth FC":"Portsmouth","Burnley FC":"Burnley","Reading FC":"Reading","Middlesbrough FC":"Middlesbrough","Derby County":"Derby County","Birmingham City":"Birmingham City",
"Blackburn Rovers":"Blackburn Rovers","Bolton Wanderers":"Bolton Wanderers","Wigan Athletic":"Wigan Athletic","West Ham United":"West Ham United","Aston Villa":"Aston Villa","Southampton FC":"Southampton","Crystal Palace":"Crystal Palace","Watford FC":"Watford","Blackpool FC":"Blackpool","Swansea City":"Swansea City","Birmingham":"Birmingham City","Blackburn":"Blackburn Rovers","Bolton":"Bolton Wanderers","West Ham":"West Ham United","Wigan":"Wigan Athletic"}
def nm(n): n=n.strip(); return NAME.get(n,n)
rows=[]
# 2010/11 - 2016/17 from football-data derived dataset (with cards)
for r in csv.DictReader(open('tara-nguyen/english-premier-league-datasets-for-10-seasons/epldat10seasons/epl-allseasons-matchstats.csv',encoding='utf-8')):
    y=int(r['Season'][:4])
    if y>2016: continue
    for side,opp in (('Home','Away'),('Away','Home')):
        if r[side+'Team']=='Chelsea':
            rows.append(dict(season=f"{y}-{str(y+1)[2:]}",date=r['Date'],gw="",comp="Premier League",venue='H' if side=='Home' else 'A',opponent=nm(r[opp+'Team']),
              gf=int(r[side+'Goals']),ga=int(r[opp+'Goals']),chel_yellow=int(r[side+'YellowCards']),chel_red=int(r[side+'RedCards']),opp_yellow=int(r[opp+'YellowCards']),opp_red=int(r[opp+'RedCards']),scorers="",note=""))
# 2007-08 .. 2009-10 from openfootball (scores only)
for y in (2007,2008,2009):
    sn=f"{y}-{str(y+1)[2:]}"; cur=None
    for line in open(f'openfootball/england/{sn}/1-premierleague.txt',encoding='utf-8'):
        m=re.match(r'^\s*(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+(\w{3})\s+(\d+)(?:\s+(\d{4}))?',line)
        if m:
            mo=MON[m.group(1)]; yr=int(m.group(3)) if m.group(3) else (y if mo>=7 else y+1); cur=date(yr,mo,int(m.group(2))); continue
        m=re.match(r'^\s+(?:\d\d[:.]\d\d\s+)?(.+?)\s{2,}(\d+)-(\d+)(?:\s+\((\d+)-(\d+)\))?\s+(.+?)\s*$',line)
        if m and cur:
            h,hg,ag,_,_,a=m.groups()
            if 'Chelsea' in (h,a) or h.startswith('Chelsea') or a.startswith('Chelsea'):
                home=h.startswith('Chelsea')
                rows.append(dict(season=sn,date=cur.isoformat(),gw="",comp="Premier League",venue='H' if home else 'A',opponent=nm(a if home else h),
                  gf=int(hg if home else ag),ga=int(ag if home else hg),chel_yellow="",chel_red="",opp_yellow="",opp_red="",scorers="",note=""))
# normalise date format dd/mm/yyyy or iso
out=[]
for r in rows:
    d=r['date']
    if '-' in d and len(d)==10 and d[4]=='-': iso=d
    else:
        dd,mm,yy=d.split('/'); iso=f"{yy if len(yy)==4 else ('20'+yy)}-{mm}-{dd}"
    r['date']=iso; out.append(r)
out.sort(key=lambda r:r['date'])
w=csv.DictWriter(open('chelsea_league_matches_old.csv','w',newline='',encoding='utf-8'),fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
from collections import defaultdict
agg=defaultdict(lambda:[0,0,0,0,0,0])
for r in out:
    a=agg[r['season']]; a[0]+=1;a[1]+=r['gf']>r['ga'];a[2]+=r['gf']==r['ga'];a[3]+=r['gf']<r['ga'];a[4]+=r['gf'];a[5]+=r['ga']
for k in sorted(agg): a=agg[k]; print(k,'P',a[0],'W',a[1],'D',a[2],'L',a[3],'GF',a[4],'GA',a[5],'Pts',a[1]*3+a[2])
print(sorted({r['opponent'] for r in out}))
