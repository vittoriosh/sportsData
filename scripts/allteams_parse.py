import re, csv, json, ast
from datetime import date
MON={m:i+1 for i,m in enumerate("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split())}
def seasons():
    return [f"{y}-{str(y+1)[2:]}" for y in range(2007,2027)]
def parse_of(sn):
    y=int(sn[:4]); cur=None; out=[]
    for line in open(f'/home/claude/openfootball/england/{sn}/1-premierleague.txt',encoding='utf-8'):
        m=re.match(r'^\s*(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+(\w{3})\s+(\d+)(?:\s+(\d{4}))?',line)
        if m:
            mo=MON[m.group(1)]; yr=int(m.group(3)) if m.group(3) else (y if mo>=7 else y+1); cur=date(yr,mo,int(m.group(2))); continue
        m=re.match(r'^\s+(?:\d\d[:.]\d\d\s+)?(.+?)\s{2,}(\d+)-(\d+)(?:\s+\((\d+)-(\d+)\))?\s+(.+?)\s*$',line)
        if m and cur:
            h,hg,ag,_,_,a=m.groups(); out.append((sn,cur.isoformat(),h.strip(),a.strip(),int(hg),int(ag)))
    return out
if __name__=='__main__':
    names=set(); 
    for sn in seasons():
        ms=parse_of(sn); print(sn,len(ms)); names|={m[2] for m in ms}|{m[3] for m in ms}
    print(sorted(names))
