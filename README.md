# sportsData

Premier League data and explorer, 2007-08 to 2026-27 (2026-27 through 31 Oct 2026).

## Run locally

```
cd web
npm install
npm run dev        # http://localhost:3000
```

Production: `npm run build && npm start`.

## Layout

- `web/` – Next.js (App Router) app. Markup in `components/body.html`, styles in `app/globals.css`, explorer logic in `public/app.js`, dataset in `public/data.js`.
- `data/` – `data.json` and the Excel workbooks (all clubs, 7,306 matches; Chelsea with cards).
- `scripts/` – scripts that build the data and workbooks, plus `managers.txt` and `results_2026_27.txt`.
- `legacy/` – the original single-file `index.html` version (open directly in a browser).

Sources: openfootball/england, football-data cards via public datasets, Fantasy-Premier-League stats, Transfermarkt (ewenme/transfers), Football365 net-spend table, Wikipedia manager lists. Transfer fees are disclosed fees only; 2026-27 cards are incomplete outside Chelsea.
