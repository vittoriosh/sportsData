import ast, csv, sys, os
from collections import defaultdict

ROOT = "/home/claude/vaastav/fantasy-premier-league/data"
OUT = "/home/claude/chelsea_league_matches.csv"

ALPHA = {
    "2017-18": ["Arsenal","Bournemouth","Brighton","Burnley","Chelsea","Crystal Palace","Everton","Huddersfield","Leicester","Liverpool","Man City","Man Utd","Newcastle","Southampton","Stoke","Swansea","Spurs","Watford","West Brom","West Ham"],
    "2018-19": ["Arsenal","Bournemouth","Brighton","Burnley","Cardiff","Chelsea","Crystal Palace","Everton","Fulham","Huddersfield","Leicester","Liverpool","Man City","Man Utd","Newcastle","Southampton","Spurs","Watford","West Ham","Wolves"],
}
PRETTY = {"Spurs": "Tottenham", "Man City": "Manchester City", "Man Utd": "Manchester United",
          "Newcastle": "Newcastle United", "Leicester": "Leicester City", "Wolves": "Wolverhampton",
          "West Brom": "West Bromwich Albion", "Brighton": "Brighton & Hove Albion", "Leeds": "Leeds United",
          "Nott'm Forest": "Nottingham Forest", "Sheffield Utd": "Sheffield United", "Norwich": "Norwich City",
          "Bournemouth": "AFC Bournemouth", "Huddersfield": "Huddersfield Town", "Cardiff": "Cardiff City",
          "Swansea": "Swansea City", "Stoke": "Stoke City", "Ipswich": "Ipswich Town", "Luton": "Luton Town",
          "Hull": "Hull City", "Burnley": "Burnley", "Sunderland": "Sunderland"}

def pretty(n): return PRETTY.get(n, n)

def read_csv(p):
    with open(p, newline="", encoding="utf-8", errors="replace") as f:
        return list(csv.DictReader(f))

def parse_stats(s):
    """return dict identifier -> {'h': {element: value}, 'a': {...}}"""
    out = {}
    try:
        items = ast.literal_eval(s)
    except Exception:
        return out
    for it in items:
        if "identifier" in it:
            ident = it["identifier"]; body = it
        else:
            ident = list(it.keys())[0]; body = it[ident]
        d = {"h": defaultdict(int), "a": defaultdict(int)}
        for side in ("h", "a"):
            for e in body.get(side, []):
                d[side][e["element"]] += e["value"]
        out[ident] = d
    return out

rows = []
for season in ["2018-19","2019-20","2020-21","2021-22","2022-23","2023-24","2024-25","2025-26"]:
    base = f"{ROOT}/{season}"
    if season in ALPHA:
        names = {i+1: n for i, n in enumerate(ALPHA[season])}
    else:
        names = {int(r["id"]): r["name"] for r in read_csv(f"{base}/teams.csv")}
    chel = [k for k, v in names.items() if v == "Chelsea"][0]
    players = {int(r["id"]): r["web_name"] for r in read_csv(f"{base}/players_raw.csv")}
    for r in read_csv(f"{base}/fixtures.csv"):
        if r["finished"] != "True" or r["team_h_score"] == "" :
            continue
        h, a = int(r["team_h"] if "team_h" in r else r["team_h"]), int(r["team_a"])
        if chel not in (h, a):
            continue
        home = h == chel
        st = parse_stats(r["stats"])
        me, opp = ("h", "a") if home else ("a", "h")
        def tot(ident, side):
            return sum(st.get(ident, {}).get(side, {}).values())
        gf = int(r["team_h_score"]) if home else int(r["team_a_score"])
        ga = int(r["team_a_score"]) if home else int(r["team_h_score"])
        scorers = []
        for e, v in st.get("goals_scored", {}).get(me, {}).items():
            scorers.append(f"{players.get(e, e)}" + (f" ({v})" if v > 1 else ""))
        for e, v in st.get("own_goals", {}).get(opp, {}).items():
            scorers.append(f"{players.get(e, e)} (og)")
        rows.append(dict(season=season, date=r["kickoff_time"][:10], gw=r["event"],
                         comp="Premier League", venue="H" if home else "A",
                         opponent=pretty(names[a if home else h]), gf=gf, ga=ga,
                         chel_yellow=tot("yellow_cards", me), chel_red=tot("red_cards", me),
                         opp_yellow=tot("yellow_cards", opp), opp_red=tot("red_cards", opp),
                         scorers=", ".join(scorers)))

# 2017-18: derive from merged_gw (no fixtures.csv); Chelsea players from players_raw team id
season = "2017-18"
base = f"{ROOT}/{season}"
praw = read_csv(f"{base}/players_raw.csv")
tkey = "team" if "team" in praw[0] else None
chel_ids = {r["id"] for r in praw if r.get(tkey) == "5"} if tkey else set()
pname = {r["id"]: r["web_name"] for r in praw}
names = {i+1: n for i, n in enumerate(ALPHA[season])}
mg = read_csv(f"{base}/gws/merged_gw.csv")
cnt = defaultdict(int)
fx = defaultdict(lambda: dict(cy=0, cr=0, sc=defaultdict(int)))
meta = {}
for r in mg:
    if r["element"] not in chel_ids:
        continue
    key = (r["fixture"],)
    fx[key]["cy"] += int(r["yellow_cards"]); fx[key]["cr"] += int(r["red_cards"])
    if int(r["goals_scored"]):
        fx[key]["sc"][pname.get(r["element"], r["name"])] += int(r["goals_scored"])
    home = r["was_home"] == "True"
    meta[key] = (r["GW"], home, int(r["opponent_team"]), int(r["team_h_score"]), int(r["team_a_score"]), r["kickoff_time"][:10])
    cnt[key] += 1
# opponent cards: sum of all players with opponent == chelsea in same fixture
oc = defaultdict(lambda: [0, 0])
for r in mg:
    if r["opponent_team"] == "5" and r["element"] not in chel_ids and int(r["minutes"]) >= 0:
        key = (r["fixture"],)
        oc[key][0] += int(r["yellow_cards"]); oc[key][1] += int(r["red_cards"])
for key, v in fx.items():
    if cnt[key] < 15: continue
    gw, home, opp, hs, as_, kd = meta[key]
    rows.append(dict(season=season, date=kd, gw=gw, comp="Premier League", venue="H" if home else "A",
                     opponent=pretty(names[opp]), gf=hs if home else as_, ga=as_ if home else hs,
                     chel_yellow=v["cy"], chel_red=v["cr"], opp_yellow=oc[key][0], opp_red=oc[key][1],
                     scorers=", ".join(f"{n}" + (f" ({c})" if c > 1 else "") for n, c in v["sc"].items())))

rows.sort(key=lambda x: x["date"])
with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)

# sanity: per-season record
agg = defaultdict(lambda: [0,0,0,0,0,0,0,0,0])
for r in rows:
    a = agg[r["season"]]
    a[0] += 1
    a[1] += r["gf"] > r["ga"]; a[2] += r["gf"] == r["ga"]; a[3] += r["gf"] < r["ga"]
    a[4] += r["gf"]; a[5] += r["ga"]; a[6] += r["chel_yellow"]; a[7] += r["chel_red"]
for s in sorted(agg):
    a = agg[s]
    print(s, "P", a[0], "W", a[1], "D", a[2], "L", a[3], "GF", a[4], "GA", a[5], "Pts", a[1]*3+a[2], "Y", a[6], "R", a[7])
