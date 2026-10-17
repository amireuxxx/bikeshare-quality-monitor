# SPEC: BikeShare Quality Monitor

## 1. Team and prompt
- **Team:** Hangting Zhu and Yuxin Wang
- **Track:** On-campus (24 hours), Oct 16-17, 2026
- **Prompt we chose:** 1. Urban Systems: Bikeshare Fleets (Devpost on-campus prompts)
- **Our public repo:** github.com/amireuxxx/bikeshare-quality-monitor

## 2. User and use case
- **User:** the fleet operations supervisor of a municipal bikeshare system, who decides where maintenance and rebalancing vans go.
- **Decision the tool helps them make, and when:** which stations to send a van to next, and whether a period of blocked stations (such as the morning rush) is an abnormal event or ordinary variation. Used after each round of station counts, and at the start of each shift.
- **Why this matches the prompt:** the prompt describes a "docks full / docks empty" crisis in which vans are dispatched blindly; the tool shows when stations are unusable (p-chart over time), where (station ranking) and what to do now (dispatch list).

## 3. Inputs
| Input | Type and units | Where the user gets it |
|---|---|---|
| `bikeshare.csv`, one row per station per observation time: `timestamp`, `station_id`, `capacity`, `bikes_available` | ISO 8601 time, text, docks, bikes | a scheduled manual count or a permissioned station-status snapshot |

No parameters: the control limits are fixed at three sigma. Four columns is the minimum needed to say whether a station is empty or full.

## 4. The statistics, and why
- **Method:** a p-chart with variable subgroup size. At each time t, n_t stations are observed and d_t are blocked (0 bikes or 0 open docks). p_t = d_t / n_t, the center line is pbar = sum(d_t) / sum(n_t), and the limits are pbar ± 3·sqrt(pbar·(1 − pbar) / n_t), clipped to 0 and 1.
- **Why it fits the use case:** each station observation is a pass/fail (blocked or not), so the proportion of blocked stations at each time is attribute data, and a p-chart separates ordinary variation from special causes such as a rush-hour wave.
- **Assumptions and how the tool checks them:** independent observations with the same blocking probability at every station. The tool does not hide that this is only approximate (the same stations are seen repeatedly; commuting is predictable): the output carries a warning, and the `mixed_imbalance.csv` scenario shows the limit, with an in-control chart but four chronically blocked stations that only the station ranking reveals.
- **Known-answer check:** `tests/test_stats.py`. Four timepoints of 10 stations with 1, 1, 1, 9 blocked give pbar = 12/40 = 0.30 and limits 0 to 0.734741 (= 0.30 + 3·sqrt(0.30·0.70/10)), so only the last point signals. Degenerate cases: nothing blocked (pbar = 0, no signals), a single timepoint, and fewer stations at one time (wider limits).

## 5. Delivery
- **Stack:** Python REST API (FastAPI) and a browser dashboard (HTML, JavaScript and Chart.js) served by the same app.
- **Entry point:** `backend.main:app`; statistics in `backend/analysis.py` (no web code inside it).
- **Scripts:** `testme.sh` (run locally), `manifestme.sh` (write the Posit Connect manifest), `deployme.sh` (publish).
- Deployed on the course Posit Connect server: <https://connect.systems-apps.com/content/03f2311e-aedb-498d-a3b2-a1e91474a54d/>.

## 6. Outputs
- Summary cards: observations, stations, blocked rate, out-of-control points, stations unavailable now.
- A p-chart of the blocked share at each time with upper limit, center and lower limit (points outside the limits are flagged).
- A station table ranked by blocked rate with empty and full counts and the latest status.
- Dispatch suggestions for stations that are empty ("Deliver bikes") or full ("Redistribute bikes") at the latest observation.

## 7. Test datasets and codebook
Three synthetic CSVs in `data/`, regenerated exactly by `python generate_data.py`: `baseline.csv` (stable), `commute_shortage.csv` (08:00 to 09:45 wave), `mixed_imbalance.csv` (four chronically blocked stations). `data/CODEBOOK.md` documents every column, scenario and what real collection would take.

## 8. Documentation and reproducibility
`README.md` (what it does, inputs, endpoints, how to run), `demo/README.md` (walkthrough of each dataset), a public GitHub repository, pinned dependencies and 14 passing tests in GitHub Actions.

## 9. Out of scope
Live sensor feeds, route optimization, forecasting, logins and databases, and any claim that the synthetic data are real observations.
