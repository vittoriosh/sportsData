# sportsData

Premier League data and explorer, 2007-08 to 2026-27 (2026-27 through 31 Oct 2026).

- `app/index.html` – self-contained Premier League Explorer (odds, club, seasons, money, managers, matches). Open in a browser.
- `app/template.html` – app template (data is injected from `data/data.json`).
- `data/data.json` – matches, fixtures, managers and transfers used by the app.
- `data/Premier_League_20_Seasons.xlsx` – all clubs: league tables, positions, 7,306 matches.
- `data/Chelsea_10_Seasons_Match_Data.xlsx` – Chelsea league matches with scores, yellows, reds.
- `scripts/` – build and patch scripts, plus `managers.txt` and `results_2026_27.txt`.

Sources: openfootball/england, football-data cards via public datasets, Fantasy-Premier-League stats, Transfermarkt (ewenme/transfers), Football365 net-spend table, Wikipedia manager lists.
Notes: transfer fees are disclosed fees only; 2026-27 cards are incomplete outside Chelsea.
