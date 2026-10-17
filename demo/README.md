# Demo walkthrough

Run the tool from the repository root, then open the page:

```bash
bash testme.sh            # http://localhost:8000   (PORT=8765 bash testme.sh if 8000 is taken)
```

Live version: **[ADD the verified Posit Connect URL here]**

Each scenario below can be run two ways: click its button on the page, or send the file to the API:

```bash
curl -F "file=@data/commute_shortage.csv" http://localhost:8000/api/analyze
```

The numbers below were produced by exactly these files (see [data/CODEBOOK.md](../data/CODEBOOK.md)); a fresh clone gives the same values.

## 1. `baseline.csv`: a stable system

| | |
|---|---|
| Observations / stations / timepoints | 480 / 15 / 32 |
| Blocked rate (pbar, the chart's center line) | 4.6% |
| Control limits at n = 15 stations | 0.0% to 20.8% |
| Points outside the limits | **0** |
| Unavailable at the latest snapshot | ST10 (FULL), ST07 (FULL) |

**How to read this:** the process is in statistical control. About 1 station check in 22 finds a station empty or full, and
that rate wobbles randomly inside the limits. There is no special cause to hunt for. The two stations flagged at the last
snapshot are ordinary day-to-day events: send a van, but do not open an investigation.

## 2. `commute_shortage.csv`: a rush-hour wave (special cause)

| | |
|---|---|
| Blocked rate (pbar) | 17.3% |
| Control limits at n = 15 | 0.0% to 46.6% |
| Points above the upper limit | **7**: 08:00, 08:15, 08:30, 09:00, 09:15, 09:30, 09:45 |
| Back in control | from 10:00, blocked share 0% to 13% |
| Unavailable at the latest snapshot | ST05 (FULL), ST11 (EMPTY) |

**How to read this:** during the morning commute, 47% to 67% of stations are blocked at once, far outside what chance
produces (the 08:45 point, 33%, is the only dip back inside). That is a special cause, not noise: residential stations
`ST01` to `ST06` run EMPTY while downtown stations `ST07` to `ST10` run FULL. Action: pre-position vans before 08:00 and
move bikes from the full downtown docks back to the empty residential ones.

## 3. `mixed_imbalance.csv`: a chronic problem the time chart cannot see

| | |
|---|---|
| Blocked rate (pbar) | 17.3% |
| Points outside the limits | **0** (the p-chart looks in control) |
| Worst stations (blocked rate) | ST12 53.1% (always FULL), ST05 40.6% (FULL), ST03 37.5% (EMPTY), ST09 31.3% (EMPTY) |
| Best stations | ST01 0.0%, ST06 3.1% |
| Unavailable at the latest snapshot | ST05 (FULL), ST14 (FULL), ST07 (FULL) |

**How to read this:** the chart is quiet because the problem does not depend on the time of day: four stations are
blocked all day, every day. The station ranking (section 4 of the page) is where it shows up. Action: a permanent fix
for those stations (capacity, docking layout, regular rebalancing), not a one-off dispatch. This scenario is also the
reason the README says a p-chart signal means "investigate", and that a p-chart assumes the same blocking probability at
every station.

## Check the statistics yourself

```bash
pytest -q        # 14 tests, including a hand-calculated p-chart (tests/test_stats.py)
```

The known-answer test reproduces this hand calculation: 4 timepoints of 10 stations with 1, 1, 1 and 9 stations blocked
give pbar = 12/40 = 0.30 and limits 0.30 ± 3·sqrt(0.30·0.70/10) = 0 to 0.734741, so only the last point (0.90) signals.
