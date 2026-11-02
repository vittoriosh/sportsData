import csv
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from datetime import date

rows = list(csv.DictReader(open('/home/claude/chelsea_league_matches_old.csv', encoding='utf-8'))) + list(csv.DictReader(open('/home/claude/chelsea_league_matches.csv', encoding='utf-8')))
cur = [
 # date, opp, venue, gw, gf, ga, cY, cR, oY, oR, scorers, note
 ("2026-08-24","Fulham","A",1,3,2,3,0,2,0,"Joao Pedro, Rogers, Palmer","Cards: Colwill, Lavia, James (Chelsea); Bassey, Castagne (Fulham)"),
 ("2026-08-30","Brighton & Hove Albion","H",2,4,3,1,0,3,0,"Lavia, Neto, Joao Pedro, Palmer","Cards: Fofana (Chelsea); Brighton 3 (two named: Dunk, Boscagli)"),
 ("2026-09-06","Arsenal","A",3,1,2,4,0,2,0,"Rogers","Chelsea: Joao Pedro, Palmer, Rogers + Lacroix (team split inferred from 4-2 totals)"),
 ("2026-09-12","Hull City","H",4,2,2,1,0,5,0,"Rogers, Joao Pedro","Hull: McBurnie, Egan, Crooks, Iroegbunam, Norton-Cuffy. Chelsea's single yellow not identified"),
 ("2026-09-18","Brentford","A",5,0,3,0,0,2,0,"","Brentford: Igor Thiago, Sangare"),
 ("2026-10-10","AFC Bournemouth","H",6,5,1,0,0,4,0,"Henderson (2), Joao Pedro (2), Silva (og)","Bournemouth: Tavernier, Truffert, Adams, Christie"),
 ("2026-10-17","Everton","A",7,2,0,4,0,3,0,"Neto (2)","Chelsea: Neto, Acheampong, Rogers, Palmer. Everton: Armstrong, Tarkowski, Norgaard (Norgaard team inferred)"),
 ("2026-10-24","Tottenham","H",8,0,2,3,1,3,0,"","Palmer sent off 80' (second yellow). Sources disagree: one match table shows 2 Chelsea yellows, match report names 3 (Palmer, Neto, Rogers). Tottenham goals: Penders og, Tel"),
 ("2026-10-31","Manchester United","H",9,2,0,1,0,1,1,"Rogers, Palmer (pen)","PARTIAL: from live commentary. Chelsea: Penders yellow. Man Utd: Lisandro Martinez booked then sent off 63'. Other cards may be missing"),
]
for d,o,v,gw,gf,ga,cy,cr,oy,orr,sc,note in cur:
    rows.append(dict(season="2026-27",date=d,gw=gw,comp="Premier League",venue=v,opponent=o,gf=gf,ga=ga,
                     chel_yellow=cy,chel_red=cr,opp_yellow=oy,opp_red=orr,scorers=sc,note=note))

F = "Arial"
hdr_fill = PatternFill("solid", fgColor="034694"); hdr_font = Font(name=F, bold=True, color="FFFFFF")
base = Font(name=F, size=10); blue = Font(name=F, size=10, color="0000FF")

wb = Workbook()
ws = wb.active; ws.title = "Matches"
heads = ["Season","Date","Gameweek","Competition","Venue","Opponent","Chelsea Goals","Opp Goals","Result","Points",
         "Chelsea Yellows","Chelsea Reds","Opp Yellows","Opp Reds","Chelsea Scorers","Data note","Game #"]
ws.append(heads)
for c in ws[1]: c.fill, c.font, c.alignment = hdr_fill, hdr_font, Alignment(horizontal="center", wrap_text=True)
n = 0
for r in rows:
    n += 1; i = n + 1
    num = lambda k: (int(r[k]) if r[k] != "" else None)
    ws.append([r["season"], date.fromisoformat(r["date"]), num("gw"), r["comp"], r["venue"], r["opponent"],
               int(r["gf"]), int(r["ga"]), f'=IF(G{i}>H{i},"W",IF(G{i}=H{i},"D","L"))',
               f'=IF(G{i}>H{i},3,IF(G{i}=H{i},1,0))', num("chel_yellow"), num("chel_red"), num("opp_yellow"), num("opp_red"), r["scorers"], r.get("note",""), f'=COUNTIFS($A$2:A{i},A{i})'])
last = n + 1
for row in ws.iter_rows(min_row=2, max_row=last):
    for c in row: c.font = base
    row[1].number_format = "yyyy-mm-dd"
    for k in (0,2,4,6,7,8,9,10,11,12,13): row[k].alignment = Alignment(horizontal="center")
for col, w in zip("ABCDEFGHIJKLMNOPQ", [9,12,10,16,7,24,9,9,8,7,10,9,10,9,40,60,8]): ws.column_dimensions[col].width = w
ws.row_dimensions[1].height = 32
ws.freeze_panes = "A2"; ws.auto_filter.ref = f"A1:Q{last}"

ss = wb.create_sheet("Seasons")
sh = ["Season","League Pos","P","W","D","L","GF","GA","GD","Pts","Win %","Pts/Game","Yellows","Reds","Games w/ card data","Yellows/Game","Reds/Game","Clean Sheets","Home Pts","Away Pts"]
ss.append(sh)
for c in ss[1]: c.fill, c.font, c.alignment = hdr_fill, hdr_font, Alignment(horizontal="center", wrap_text=True)
pos = {"2007-08":2,"2008-09":3,"2009-10":1,"2010-11":2,"2011-12":6,"2012-13":3,"2013-14":3,"2014-15":1,"2015-16":10,"2016-17":1,"2017-18":5,"2018-19":3,"2019-20":4,"2020-21":4,"2021-22":3,"2022-23":12,"2023-24":6,"2024-25":4,"2025-26":10,"2026-27":4}
M = "Matches!"
rng = lambda col: f"{M}${col}$2:${col}${last}"
for k, (s, p) in enumerate(pos.items()):
    i = k + 2
    ss.append([s, p,
      f'=COUNTIFS({rng("A")},A{i})', f'=COUNTIFS({rng("A")},A{i},{rng("I")},"W")', f'=COUNTIFS({rng("A")},A{i},{rng("I")},"D")',
      f'=COUNTIFS({rng("A")},A{i},{rng("I")},"L")', f'=SUMIFS({rng("G")},{rng("A")},A{i})', f'=SUMIFS({rng("H")},{rng("A")},A{i})',
      f'=G{i}-H{i}', f'=SUMIFS({rng("J")},{rng("A")},A{i})', f'=IF(C{i}=0,0,D{i}/C{i})', f'=IF(C{i}=0,0,J{i}/C{i})',
      f'=SUMIFS({rng("K")},{rng("A")},A{i})', f'=SUMIFS({rng("L")},{rng("A")},A{i})',
      f'=COUNTIFS({rng("A")},A{i},{rng("K")},">=0")', f'=IF(O{i}=0,"n/a",M{i}/O{i})', f'=IF(O{i}=0,"n/a",N{i}/O{i})',
      f'=COUNTIFS({rng("A")},A{i},{rng("H")},0)',
      f'=SUMIFS({rng("J")},{rng("A")},A{i},{rng("E")},"H")', f'=SUMIFS({rng("J")},{rng("A")},A{i},{rng("E")},"A")'])
    ss.cell(i,2).font = blue
t = len(pos) + 2
ss.cell(t,1,"Total"); 
for col in "CDEFGHIJMNOR": 
    ss[f"{col}{t}"] = f"=SUM({col}2:{col}{t-1})"
ss[f"K{t}"] = f"=IF(C{t}=0,0,D{t}/C{t})"; ss[f"L{t}"] = f"=IF(C{t}=0,0,J{t}/C{t})"
ss[f"P{t}"] = f"=IF(O{t}=0,\"n/a\",M{t}/O{t})"; ss[f"Q{t}"] = f"=IF(O{t}=0,\"n/a\",N{t}/O{t})"
ss[f"S{t}"] = f"=SUM(S2:S{t-1})"; ss[f"T{t}"] = f"=SUM(T2:T{t-1})"
for row in ss.iter_rows(min_row=2, max_row=t):
    for c in row:
        if c.font != blue: c.font = base
        c.alignment = Alignment(horizontal="center")
    row[10].number_format = "0.0%"; row[11].number_format = "0.00"; row[15].number_format = "0.00"; row[16].number_format = "0.00"
for c in ss[t]: c.font = Font(name=F, size=10, bold=True)
ss.column_dimensions["A"].width = 10
for j in range(2, 21): ss.column_dimensions[get_column_letter(j)].width = 11
ss.row_dimensions[1].height = 45; ss.freeze_panes = "B2"
notes = [
 "Notes & sources",
 "2026-27 is in progress: 9 league games to 31 Oct 2026. Final-position cell shows current rank (4th, 16 pts).",
 "League Pos (blue) is typed in by hand from public final tables; 2025-26 (10th) and 2024-25 (4th) were confirmed against sourced tables.",
 "Scores, dates, cards and scorers for 2017-18 to 2025-26: Fantasy Premier League match-event data (github.com/vaastav/fantasy-premier-league).",
 "Cross-check: season W/D/L/GF/GA/points match the official tables for all 9 completed seasons; 2017-18 to 2019-20 yellow/red totals match football-data.co.uk-derived data exactly.",
 "2026-27 (9 games): scores, scorers and cards gathered from match pages (footballwebpages.co.uk, Sports Mole, Opta/The Analyst, FotMob, soccernews.com); each row has a Data note. The Man Utd game (31 Oct) cards are partial; Tottenham yellows are disputed (2 vs 3).",
 "Cards are league (Premier League) only. A second yellow that becomes a red is counted as a red; check before comparing exact card totals with other sites.",
 "2010-11 to 2016-17: scores and cards from the football-data.co.uk-derived EPL dataset (github.com/tara-nguyen). 2007-08 to 2009-10: scores from openfootball/england; no card or scorer data (cells blank).",
 "Scope: Premier League matches only. FA Cup, League Cup and European games are not included.",
]
for k, txt in enumerate(notes):
    c = ss.cell(t + 2 + k, 1, txt); c.font = Font(name=F, size=10, bold=(k == 0))

from openpyxl.chart import LineChart, Reference
from openpyxl.chart.shapes import GraphicalProperties
pg = wb.create_sheet("Points Progression", 1)
pg["A1"] = "Cumulative Premier League points by game (each line = one season)"; pg["A1"].font = Font(name=F, bold=True, size=12)
pg["A2"] = "Game #"
seasons = list(pos.keys())
for j, sn in enumerate(seasons):
    pg.cell(2, 2 + j, sn)
for c in pg[2]:
    if c.value is not None: c.fill, c.font, c.alignment = hdr_fill, hdr_font, Alignment(horizontal="center")
played = {sn: sum(1 for r in rows if r["season"] == sn) for sn in seasons}
for g in range(1, 39):
    pg.cell(2 + g, 1, g).font = base
    for j, sn in enumerate(seasons):
        if g <= played[sn]:
            col = get_column_letter(2 + j)
            c = pg.cell(2 + g, 2 + j, f'=SUMIFS(Matches!$J$2:$J${last},Matches!$A$2:$A${last},{col}$2,Matches!$Q$2:$Q${last},"<="&$A{2+g})')
            c.font = base
        for_cell = pg.cell(2 + g, 2 + j); for_cell.alignment = Alignment(horizontal="center")
    pg.cell(2 + g, 1).alignment = Alignment(horizontal="center")
pg.column_dimensions["A"].width = 8
for j in range(len(seasons)): pg.column_dimensions[get_column_letter(2 + j)].width = 10
pg.freeze_panes = "B3"
ch = LineChart(); ch.title = "Chelsea: points progression by season"; ch.height = 14; ch.width = 28
ch.y_axis.title = "Cumulative points"; ch.x_axis.title = "Games played"
ch.add_data(Reference(pg, min_col=2, max_col=1 + len(seasons), min_row=2, max_row=40), titles_from_data=True)
ch.set_categories(Reference(pg, min_col=1, min_row=3, max_row=40))
import colorsys
palette = []
for i in range(len(seasons)-1):
    r_, g_, b_ = colorsys.hls_to_rgb(((i*0.381966) % 1.0), 0.42, 0.55)
    palette.append("%02X%02X%02X" % (int(r_*255), int(g_*255), int(b_*255)))
palette.append("034694")
for k, sr in enumerate(ch.series):
    sr.smooth = False; sr.marker.symbol = "none"
    sr.graphicalProperties.line.solidFill = palette[k]
    sr.graphicalProperties.line.width = 38000 if k == len(seasons) - 1 else 19000
ch.x_axis.delete = False; ch.y_axis.delete = False
ch.y_axis.scaling.min = 0; ch.y_axis.majorGridlines = ch.y_axis.majorGridlines
ch.legend.position = "r"
pg.add_chart(ch, "M2")
pg["A42"] = "2026-27 stops at games played so far (thick blue line). 2007-08 to 2009-10 have scores only (no card data). Values are formulas on the Matches tab."; pg["A42"].font = Font(name=F, italic=True, size=9)
wb.save("/home/claude/out/Chelsea_10_Seasons_Match_Data.xlsx")
print(len(rows))
