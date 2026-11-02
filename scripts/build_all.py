import re, csv, ast, sys
from datetime import date
from collections import defaultdict
sys.path.insert(0,'/home/claude/scripts')
MON={m:i+1 for i,m in enumerate("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split())}
CANON={"Tottenham Hotspur":"Tottenham","Spurs":"Tottenham","Wolverhampton Wanderers":"Wolverhampton","Wolves":"Wolverhampton","Man City":"Manchester City","Man United":"Manchester United","Man Utd":"Manchester United",
"Newcastle":"Newcastle United","Leicester":"Leicester City","West Brom":"West Bromwich Albion","Brighton":"Brighton & Hove Albion","Bournemouth":"AFC Bournemouth","Huddersfield":"Huddersfield Town","Cardiff":"Cardiff City",
"Swansea":"Swansea City","Stoke":"Stoke City","Hull":"Hull City","QPR":"Queens Park Rangers","Norwich":"Norwich City","Wigan":"Wigan Athletic","Blackburn":"Blackburn Rovers","Bolton":"Bolton Wanderers","Birmingham":"Birmingham City",
"West Ham":"West Ham United","Leeds":"Leeds United","Luton":"Luton Town","Sheffield Utd":"Sheffield United","Ipswich":"Ipswich Town","Nott'm Forest":"Nottingham Forest","Coventry":"Coventry City","Derby":"Derby County"}
def nm(n):
    n=n.strip()
    n=re.sub(r'\s+(AFC|FC)$','',n) if n!='AFC Bournemouth' else n
    return CANON.get(n,n)
def seasons(): return [f"{y}-{str(y+1)[2:]}" for y in range(2007,2027)]
def parse_of(sn):
    y=int(sn[:4]); cur=None; out=[]
    for line in open(f'/home/claude/openfootball/england/{sn}/1-premierleague.txt',encoding='utf-8'):
        m=re.match(r'^\s*(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+(\w{3})\s+(\d+)(?:\s+(\d{4}))?\s*$',line) or re.match(r'^\s*(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+(\w{3})\s+(\d+)(?:\s+(\d{4}))?(?=\s+\d\d:)',line)
        if m:
            mo=MON[m.group(1)]; yr=int(m.group(3)) if m.group(3) else (y if mo>=7 else y+1)
            if sn=='2019-20' and mo==7 and not m.group(3): yr=2020
            cur=date(yr,mo,int(m.group(2))); continue
        m=re.match(r'^\s+(?:\d\d[:.]\d\d\s+)?(.+?)\s+v\s+(.+?)\s+(\d+)-(\d+)(?:\s+\((\d+)-(\d+)\))?\s*$',line)
        if m and cur:
            h,a,hg,ag=m.group(1),m.group(2),m.group(3),m.group(4); out.append([sn,cur.isoformat(),nm(h),nm(a),int(hg),int(ag)]); continue
        m=re.match(r'^\s+(?:\d\d[:.]\d\d\s+)?(.+?)\s{2,}(\d+)-(\d+)(?:\s+\((\d+)-(\d+)\))?\s+(.+?)\s*$',line)
        if m and cur:
            h,hg,ag,_,_,a=m.groups(); out.append([sn,cur.isoformat(),nm(h),nm(a),int(hg),int(ag)])
    return out
M={}
for sn in seasons():
    ms=parse_of(sn)
    for r in ms: M[(sn,r[2],r[3])]=dict(season=sn,date=r[1],home=r[2],away=r[3],hg=r[4],ag=r[5],hy=None,ay=None,hr=None,ar=None,src='')
    print(sn,len(ms),end=' | ')
print()
# cards: football-data derived (2010-11..2019-20)
miss=0
for r in csv.DictReader(open('/home/claude/tara-nguyen/english-premier-league-datasets-for-10-seasons/epldat10seasons/epl-allseasons-matchstats.csv',encoding='utf-8')):
    y=int(r['Season'][:4]); sn=f"{y}-{str(y+1)[2:]}"; k=(sn,nm(r['HomeTeam']),nm(r['AwayTeam']))
    if k in M:
        m=M[k]; m['hy']=int(r['HomeYellowCards']);m['ay']=int(r['AwayYellowCards']);m['hr']=int(r['HomeRedCards']);m['ar']=int(r['AwayRedCards']);m['src']='football-data'
        if (m['hg'],m['ag'])!=(int(r['HomeGoals']),int(r['AwayGoals'])): print('SCORE DIFF',k,m['hg'],m['ag'],r['HomeGoals'],r['AwayGoals'])
    else: miss+=1; print('no match for',k)
print('tara unmatched',miss)
# FPL (2018-19..2025-26): fill where missing, and cross-check overlap
FPL='/home/claude/vaastav/fantasy-premier-league/data'
ALPHA18=["Arsenal","AFC Bournemouth","Brighton & Hove Albion","Burnley","Cardiff City","Chelsea","Crystal Palace","Everton","Fulham","Huddersfield Town","Leicester City","Liverpool","Manchester City","Manchester United","Newcastle United","Southampton","Tottenham","Watford","West Ham United","Wolverhampton"]
def stats(s):
    out={}
    for it in ast.literal_eval(s):
        if 'identifier' in it: ident=it['identifier'];body=it
        else: ident=list(it.keys())[0];body=it[ident]
        out[ident]={side:sum(e['value'] for e in body.get(side,[])) for side in ('h','a')}
    return out
diff=0;filled=0
for sn in seasons()[11:19]:
    d=f'{FPL}/{sn}'
    names={i+1:n for i,n in enumerate(ALPHA18)} if sn=='2018-19' else {int(r['id']):nm(r['name']) for r in csv.DictReader(open(f'{d}/teams.csv',encoding='utf-8'))}
    for r in csv.DictReader(open(f'{d}/fixtures.csv',encoding='utf-8')):
        if r['finished']!='True' or r['team_h_score']=='': continue
        k=(sn,names[int(r['team_h'])],names[int(r['team_a'])])
        if k not in M: print('FPL no match',k); continue
        st=stats(r['stats']); g=lambda i,s:st.get(i,{}).get(s,0)
        v=(g('yellow_cards','h'),g('yellow_cards','a'),g('red_cards','h'),g('red_cards','a')); m=M[k]
        if m['hy'] is None: m['hy'],m['ay'],m['hr'],m['ar']=v; m['src']='FPL'; filled+=1
        elif (m['hy'],m['ay'],m['hr'],m['ar'])!=v: diff+=1
print('FPL filled',filled,'overlap differences',diff)
# 2026-27 Chelsea games cards (hand-collected earlier)
rows=sorted(M.values(),key=lambda r:(r['season'],r['date'],r['home']))
w=csv.DictWriter(open('/home/claude/allmatches.csv','w',newline='',encoding='utf-8'),fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
cnt=defaultdict(lambda:[0,0])
for r in rows: cnt[r['season']][0]+=1; cnt[r['season']][1]+= r['hy'] is not None
print({k:tuple(v) for k,v in cnt.items()})
