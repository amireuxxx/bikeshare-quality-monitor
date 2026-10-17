# BikeShare Quality Monitor

A working demonstration quality-control tool for the Cornell Six Sigma Hackathon Bikeshare Fleets prompt.

## What it does
Users upload timestamped station bike counts (manually collected or synthetic CSV) and view:
- Blocked-station proportions per observation time, with a variable-subgroup-size 3-sigma p-chart.
- A station-level ranking of empty or full events.
- Latest unavailable stations and simple redistribution suggestions.
- Three reproducible sample datasets.

The tool is an exploratory statistical aid, not a real-time feed. No live sensors or external API are assumed.

## Launch (Python 3.10+)
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --reload
```
Open http://127.0.0.1:8000/ in a browser. The UI fetches Chart.js from a CDN (internet connection required). API docs: http://127.0.0.1:8000/docs

## Test
```bash
pytest -q
```

## CSV schema
`timestamp`: ISO 8601 local timestamp; `station_id`: unique station code; `capacity`: dock count (positive integer); `bikes_available`: bike count 0..capacity. One observation per station/timestamp. See [data/CODEBOOK.md](data/CODEBOOK.md).

## Statistical method
At each time t, let `n_t` be stations observed and `d_t` the number with 0 bikes or 0 open docks. The blocked rate is `p_t=d_t/n_t`. The pooled center is `pbar=Σd_t/Σn_t`; 3-sigma limits are `max(0,pbar-3√[pbar(1-pbar)/n_t])` and `min(1,pbar+3√[pbar(1-pbar)/n_t])`. This is a conventional binomial p-chart, but repeated stations and predictable commuting patterns challenge independence and constant-risk assumptions. Treat signals as prompts for further stratified investigation, not proof of abnormal causes.

## Reproducibility and limitations
The test datasets are **synthetic**, not actual station observations. `generate_data.py` regenerates them deterministically. There is no booking feed or deployment claim. Staff dispatch suggestions rely on most recent observations, not optimized routes. The application is suitable as a local demonstration; instructor Posit Connect deployment is a separate step requiring course access.

## Submission
Use this public repository link and the project/demo details on Devpost. See [DEVPOST_SUBMISSION.md](DEVPOST_SUBMISSION.md). Add actual team members and a verified live deployment URL once available.
