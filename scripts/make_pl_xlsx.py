import csv, json
from collections import defaultdict
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter as L
from openpyxl.formatting.rule import CellIsRule
from datetime import date

F="Arial"; base=Font(name=F,size=10); blue=Font(name=F,size=10,color="0000FF"); bold=Font(name=F,size=10,bold=True)
hf=Font(name=F,size=10,bold=True,color="FFFFFF"); hfill=PatternFill("solid",fgColor="034694")
rows=list(csv.DictReader(open('/home/claude/allmatches_final.csv',encoding='utf-8')))
tables=json.load(open('/home/claude/tables.json'))
DED={('2009-10','Portsmouth'):9,('2023-24','Everton'):8,('2023-24','Nottingham Forest'):4}
wb=Workbook()
# ---------------- Matches ----------------
wm=wb.active; wm.title="Matches"
H=["Season","Date","Home","Away","Home Goals","Away Goals","Result","Home Yellows","Away Yellows","Home Reds","Away Reds","Cards source"]
wm.append(H)
for c in wm[1]: c.font,c.fill,c.alignment=hf,hfill,Alignment(horizontal="center",wrap_text=True)
def iv(x): return int(x) if x!="" else None
for i,r in enumerate(rows,start=2):
    wm.append([r['season'],date.fromisoformat(r['date']),r['home'],r['away'],int(r['hg']),int(r['ag']),
      f'=IF(E{i}>F{i},"H",IF(E{i}=F{i},"D","A"))',iv(r['hy']),iv(r['ay']),iv(r['hr']),iv(r['ar']),r['src']])
N=len(rows)+1
for row in wm.iter_rows(min_row=2,max_row=N):
    for c in row: c.font=base
    row[1].number_format="yyyy-mm-dd"
for col,w in zip("ABCDEFGHIJKL",[9,12,24,24,8,8,8,9,9,8,8,30]): wm.column_dimensions[col].width=w
wm.freeze_panes="A2"; wm.auto_filter.ref=f"A1:L{N}"
R=lambda c:f"Matches!${c}$2:${c}${N}"
# ---------------- League Tables ----------------
wt=wb.create_sheet("League Tables",0)
TH=["Season","Pos","Team","P","W","D","L","GF","GA","GD","Pts deducted","Pts","Yellows","Reds","Games with card data","Yellows/Game","Reds/Game"]
wt.append(TH)
for c in wt[1]: c.font,c.fill,c.alignment=hf,hfill,Alignment(horizontal="center",wrap_text=True)
i=1
for sn in sorted(tables, reverse=True):
    for pos,(team,s) in enumerate(tables[sn],start=1):
        i+=1; S=f"$A{i}"; T=f"$C{i}"
        h=lambda col,extra="":f'{R(col)},{S}' ; 
        P=f'=COUNTIFS({R("A")},{S},{R("C")},{T})+COUNTIFS({R("A")},{S},{R("D")},{T})'
        W=f'=COUNTIFS({R("A")},{S},{R("C")},{T},{R("G")},"H")+COUNTIFS({R("A")},{S},{R("D")},{T},{R("G")},"A")'
        D=f'=COUNTIFS({R("A")},{S},{R("C")},{T},{R("G")},"D")+COUNTIFS({R("A")},{S},{R("D")},{T},{R("G")},"D")'
        GF=f'=SUMIFS({R("E")},{R("A")},{S},{R("C")},{T})+SUMIFS({R("F")},{R("A")},{S},{R("D")},{T})'
        GA=f'=SUMIFS({R("F")},{R("A")},{S},{R("C")},{T})+SUMIFS({R("E")},{R("A")},{S},{R("D")},{T})'
        CG=f'=COUNTIFS({R("A")},{S},{R("C")},{T},{R("H")},">=0")+COUNTIFS({R("A")},{S},{R("D")},{T},{R("I")},">=0")'
        Y=f'=IF(O{i}=D{i}*0+O{i},IF(O{i}=D{i}+E{i}+G{i},SUMIFS({R("H")},{R("A")},{S},{R("C")},{T})+SUMIFS({R("I")},{R("A")},{S},{R("D")},{T}),""),"")'
        Y=f'=IF(O{i}=D{i},SUMIFS({R("H")},{R("A")},{S},{R("C")},{T})+SUMIFS({R("I")},{R("A")},{S},{R("D")},{T}),"")'
        Rd=f'=IF(O{i}=D{i},SUMIFS({R("J")},{R("A")},{S},{R("C")},{T})+SUMIFS({R("K")},{R("A")},{S},{R("D")},{T}),"")'
        wt.append([sn,pos,team,None,None,None,None,None,None,None,DED.get((sn,team),0),None,None,None,None,None,None])
        # columns: A Season B Pos C Team D P E W F D G L H GF I GA J GD K Ded L Pts M Y N R O cardgames P Y/g Q R/g
        wt.cell(i,4,P); wt.cell(i,5,W); wt.cell(i,6,D); wt.cell(i,7,f"=D{i}-E{i}-F{i}")
        wt.cell(i,8,GF); wt.cell(i,9,GA); wt.cell(i,10,f"=H{i}-I{i}")
        wt.cell(i,12,f"=3*E{i}+F{i}-K{i}")
        wt.cell(i,15,CG)
        wt.cell(i,13,f'=IF(O{i}=D{i},SUMIFS({R("H")},{R("A")},{S},{R("C")},{T})+SUMIFS({R("I")},{R("A")},{S},{R("D")},{T}),"")')
        wt.cell(i,14,f'=IF(O{i}=D{i},SUMIFS({R("J")},{R("A")},{S},{R("C")},{T})+SUMIFS({R("K")},{R("A")},{S},{R("D")},{T}),"")')
        wt.cell(i,16,f'=IF(M{i}="","",M{i}/D{i})'); wt.cell(i,17,f'=IF(N{i}="","",N{i}/D{i})')
NT=i
for row in wt.iter_rows(min_row=2,max_row=NT):
    for c in row: c.font=base
    row[1].font=blue; row[10].font=blue
    row[0].alignment=Alignment(horizontal="center")
    for k in list(range(1,2))+list(range(3,17)): row[k].alignment=Alignment(horizontal="center")
    row[15].number_format="0.00"; row[16].number_format="0.00"
for col,w in zip("ABCDEFGHIJKLMNOPQ",[9,6,24,6,6,6,6,6,6,6,10,6,9,7,12,10,9]): wt.column_dimensions[col].width=w
wt.freeze_panes="D2"; wt.auto_filter.ref=f"A1:Q{NT}"; wt.row_dimensions[1].height=40
# ---------------- Team x Season positions ----------------
seasons=sorted(tables)
cnt=defaultdict(int); 
for sn in seasons:
    for t,_ in tables[sn]: cnt[t]+=1
best=defaultdict(lambda:99)
for sn in seasons:
    for p,(t,_) in enumerate(tables[sn],1): best[t]=min(best[t],p)
teams=sorted(cnt,key=lambda t:(-cnt[t],best[t],t))
wx=wb.create_sheet("Position by Season",1)
wx.append(["Team"]+seasons+["Seasons in PL","Titles (completed seasons)","Best finish"])
for c in wx[1]: c.font,c.fill,c.alignment=hf,hfill,Alignment(horizontal="center",wrap_text=True)
for k,t in enumerate(teams,start=2):
    wx.cell(k,1,t)
    for j,sn in enumerate(seasons):
        c=wx.cell(k,2+j,f'=SUMIFS(\'League Tables\'!$B$2:$B${NT},\'League Tables\'!$A$2:$A${NT},{L(2+j)}$1,\'League Tables\'!$C$2:$C${NT},$A{k})')
        c.number_format='0;;'; c.alignment=Alignment(horizontal="center")
    a,b=L(2),L(1+len(seasons))
    wx.cell(k,2+len(seasons),f'=COUNTIF({a}{k}:{b}{k},">0")')
    wx.cell(k,3+len(seasons),f'=COUNTIF({a}{k}:{L(len(seasons))}{k},1)')
    wx.cell(k,4+len(seasons),f'=_xlfn.MINIFS({a}{k}:{b}{k},{a}{k}:{b}{k},">0")')
last=len(teams)+1
for row in wx.iter_rows(min_row=2,max_row=last):
    for c in row: c.font=base
    row[0].font=bold
    for c in row[1:]: c.alignment=Alignment(horizontal="center")
wx.column_dimensions["A"].width=24
for j in range(2,5+len(seasons)): wx.column_dimensions[L(j)].width=8.5
wx.column_dimensions[L(2+len(seasons))].width=10
rng=f"B2:{L(1+len(seasons))}{last}"
wx.conditional_formatting.add(rng,CellIsRule(operator='equal',formula=['1'],fill=PatternFill("solid",bgColor="034694",fgColor="034694"),font=Font(name=F,color="FFFFFF",bold=True)))
wx.conditional_formatting.add(rng,CellIsRule(operator='between',formula=['2','4'],fill=PatternFill("solid",bgColor="CFE0F7",fgColor="CFE0F7")))
wx.conditional_formatting.add(rng,CellIsRule(operator='between',formula=['18','20'],fill=PatternFill("solid",bgColor="F9D6D6",fgColor="F9D6D6")))
wx.freeze_panes="B2"
wx.cell(last+2,1,"Blue = champions, light blue = 2nd to 4th, red = 18th to 20th. Blank = not in the Premier League that season. 2026-27 is in progress (positions after the games played so far).").font=Font(name=F,italic=True,size=9)
# ---------------- Season summary ----------------
ws=wb.create_sheet("League Totals",2)
ws.append(["Season","Matches","Home wins","Draws","Away wins","Goals","Goals/Game","Home win %","Yellows","Reds","Games with card data","Yellows/Game","Reds/Game"])
for c in ws[1]: c.font,c.fill,c.alignment=hf,hfill,Alignment(horizontal="center",wrap_text=True)
for k,sn in enumerate(seasons,start=2):
    A=f"$A{k}"
    ws.append([sn,f'=COUNTIFS({R("A")},{A})',f'=COUNTIFS({R("A")},{A},{R("G")},"H")',f'=COUNTIFS({R("A")},{A},{R("G")},"D")',f'=COUNTIFS({R("A")},{A},{R("G")},"A")',
      f'=SUMIFS({R("E")},{R("A")},{A})+SUMIFS({R("F")},{R("A")},{A})',f'=F{k}/B{k}',f'=C{k}/B{k}',
      f'=SUMIFS({R("H")},{R("A")},{A})+SUMIFS({R("I")},{R("A")},{A})',f'=SUMIFS({R("J")},{R("A")},{A})+SUMIFS({R("K")},{R("A")},{A})',
      f'=COUNTIFS({R("A")},{A},{R("H")},">=0")',f'=IF(K{k}=0,"n/a",I{k}/K{k})',f'=IF(K{k}=0,"n/a",J{k}/K{k})'])
for row in ws.iter_rows(min_row=2,max_row=len(seasons)+1):
    for c in row: c.font=base; c.alignment=Alignment(horizontal="center")
    row[6].number_format="0.00";row[7].number_format="0.0%";row[11].number_format="0.00";row[12].number_format="0.00"
for j in range(1,14): ws.column_dimensions[L(j)].width=11
ws.row_dimensions[1].height=32; ws.freeze_panes="B2"
ws.cell(len(seasons)+3,1,"Yellows and reds are per game for matches that have card data; 2007-08 to 2009-10 have none, and 2026-27 only has Chelsea's games.").font=Font(name=F,italic=True,size=9)
# ---------------- Notes ----------------
wn=wb.create_sheet("Notes",0)
notes=["Premier League, 20 seasons (2007-08 to 2026-27)",
"",
"Sheets",
"League Tables: final table for every season (rows are formulas on the Matches sheet). Position is typed in (blue) from sorting by points, goal difference, goals scored.",
"Position by Season: every club, every season, with titles and best finish.",
"League Totals: goals, home/away split and cards per season.",
"Matches: all 7,306 league games.",
"",
"Sources",
"Results 2007-08 to 2025-26: openfootball/england (github.com/openfootball/england).",
"Results 2026-27 (to 31 Oct 2026): VAVEL results page, cross-checked against openfootball for the first 50 games (no differences). 86 games played so far; some clubs are a game behind.",
"Cards 2010-11 to 2019-20: football-data.co.uk-derived EPL dataset (github.com/tara-nguyen). Cards 2020-21 to 2025-26: Fantasy Premier League match data (github.com/vaastav/fantasy-premier-league).",
"Cards 2018-19 and 2019-20 exist in both sources; 10 of 760 games differ slightly (likely second-yellow handling). The football-data version is used.",
"No card data for 2007-08 to 2009-10. For 2026-27, cards are only entered for Chelsea's 9 games (from match reports); other clubs are blank.",
"",
"Checks",
"Champion and points total match the official table in all 19 completed seasons; Chelsea's finishing position matches in all 19; 2025-26 top ten spot-checked against a published table; 2026-27 leaders and bottom club match a published table.",
"Points deductions entered (blue): Portsmouth 2009-10 (9), Everton 2023-24 (8), Nottingham Forest 2023-24 (4). Any other deductions are not included.",
"2011-12: Manchester City and Manchester United both finished on 89 points; City won on goal difference.",
"",
"Scope: Premier League games only. Cups and European games are not included."]
for k,t in enumerate(notes,start=1):
    c=wn.cell(k,1,t); c.font=Font(name=F,size=12 if k==1 else 10,bold=(k==1 or t in("Sheets","Sources","Checks")))
wn.column_dimensions["A"].width=150
wb.save('/home/claude/out/Premier_League_20_Seasons.xlsx')
print(NT,N,len(teams))
