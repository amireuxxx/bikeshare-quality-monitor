# BikeShare Quality Monitor

A quality-control tool for the Cornell Six Sigma Hackathon prompt **Urban Systems: Bikeshare Fleets**. It turns station bike counts into a p-chart, a station ranking and a dispatch list, so maintenance vans stop being sent blindly.

**Live demo:** <https://connect.systems-apps.com/content/9bdb4f14-e4de-47eb-b7cc-cc1093312e94/>

## Who it is for
The fleet operations supervisor of a bikeshare system, who decides which stations get a rebalancing or maintenance van next, and whether a stretch of blocked stations (for example the morning rush) is abnormal or ordinary variation.

## What it does
Upload timestamped station counts (a CSV), or pick one of three synthetic scenarios, and the page shows:
- Summary cards: observations, stations, blocked rate, out-of-control points, stations unavailable now.
- A p-chart of the share of stations that are empty or full at each time, with 3-sigma limits that depend on how many stations were observed.
- A station ranking by blocked rate, with empty and full counts and the latest status.
- Dispatch suggestions for stations that are empty ("Deliver bikes") or full ("Redistribute bikes") at the latest observation.

It is an exploratory statistical aid, not a real-time feed. No live sensors or external API are assumed.

## Run it (Python 3.12)
```bash
python3.12 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
bash testme.sh                     # then open http://localhost:8000
```
Use `PORT=8765 bash testme.sh` if port 8000 is busy. Chart.js is bundled in `static/`, so the page works without an internet connection. Interactive API docs are at `/docs`.

## Inputs
One CSV, one row per station per observation time. There are no other parameters: the control limits are fixed at three sigma.

| Column | Meaning |
|---|---|
| `timestamp` | ISO 8601 local time of the count |
| `station_id` | station code (unique per station) |
| `capacity` | number of docks, a positive integer |
| `bikes_available` | bikes docked, from 0 to `capacity` |

One observation per station and timestamp; at most 50,000 rows and 5 MB. A station is **blocked** when it has 0 bikes (EMPTY) or 0 open docks (FULL). Every column is described in [data/CODEBOOK.md](data/CODEBOOK.md).

## API
| Endpoint | What it does |
|---|---|
| `GET /` | the dashboard |
| `GET /api/health` | `{"status": "ok"}` |
| `POST /api/analyze` | upload a CSV (form field `file`); returns the summary, the p-chart points, the station ranking, the dispatch list and a methodology note. A bad file returns HTTP 422 with the reason |
| `GET /api/examples` | the three example files, served from `/data/` |

```bash
curl -F "file=@data/commute_shortage.csv" http://localhost:8000/api/analyze
```

## Statistical method
At each time t, let `n_t` be the stations observed and `d_t` the number with 0 bikes or 0 open docks. The blocked rate is `p_t = d_t / n_t`. The pooled center is `pbar = sum(d_t) / sum(n_t)`; the 3-sigma limits are `max(0, pbar - 3*sqrt(pbar*(1-pbar)/n_t))` and `min(1, pbar + 3*sqrt(pbar*(1-pbar)/n_t))`. This is a conventional binomial p-chart. A point outside the limits is flagged as a special cause.

The p-chart assumes each station observation is an independent draw with the same blocking probability. In practice the same stations are observed repeatedly and demand follows commuting patterns, so a signal means "investigate", not "proof of a special cause". The `mixed_imbalance.csv` scenario shows the limit: its p-chart looks in control, yet four stations account for most blocked observations, which only the station ranking reveals.

The code is in [backend/analysis.py](backend/analysis.py), a plain module with no web code in it.

## Test data and demo
Three synthetic datasets (15 stations, 32 timepoints, 480 rows each) in [data/](data/): `baseline.csv` (stable), `commute_shortage.csv` (a morning commute wave) and `mixed_imbalance.csv` (four chronically blocked stations). [demo/README.md](demo/README.md) walks through each one with the exact numbers and how to read them. The data are **not real observations**; `python generate_data.py` regenerates them exactly, because every random draw uses a fixed seed.

## Tests
```bash
pytest -q        # 14 tests
```
They include a hand-calculated known-answer case and degenerate cases for the p-chart in `tests/test_stats.py`, and a check that the committed CSV files match `generate_data.py`. GitHub Actions runs them on every push.

## Deploy (Posit Connect)
`manifestme.sh` writes `manifest.json`, `deployme.sh` publishes (it needs `CONNECT_SERVER` and `CONNECT_API_KEY` in a gitignored `.env`, see `.env.example`), and `.python-version` pins Python 3.12. Dependencies are pinned in `requirements.txt`.

## Limitations
The test datasets are synthetic. Dispatch suggestions use the most recent observation only, not optimized routes. There is no booking or sensor feed, and station observations are treated as independent, which is only approximate.
