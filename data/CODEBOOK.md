# Test data codebook

All three files are **synthetic**. They share one schema and are regenerated
exactly by `python generate_data.py` (fixed random seeds). One row = one
station observed at one timepoint. 15 stations x 32 timepoints (08:00 to 15:45,
every 15 minutes, 2026-10-16) = 480 rows per file.

| Column | Description | Type / unit |
|---|---|---|
| `timestamp` | ISO 8601 local observation time | datetime |
| `station_id` | Station code, `ST01` to `ST15` | categorical |
| `capacity` | Total docks at the station (15 to 30, fixed per station) | docks |
| `bikes_available` | Bikes docked and available to rent, 0 to `capacity` | bikes |

A station is **blocked** when `bikes_available = 0` (EMPTY: nothing to rent) or
`bikes_available = capacity` (FULL: nowhere to return a bike).

## Files

| File | Scenario | What it should show |
|---|---|---|
| `baseline.csv` | Every station fills to about half capacity with random day-to-day variation | A stable process: about 4.6% of observations blocked, no p-chart signals |
| `commute_shortage.csv` | 08:00 to 09:45 commute wave: residential stations `ST01` to `ST06` run EMPTY while downtown stations `ST07` to `ST10` run FULL | Seven of the first eight timepoints plotted above the upper control limit (special cause) |
| `mixed_imbalance.csv` | Chronic imbalance: `ST03` and `ST09` are usually EMPTY, `ST05` and `ST12` are usually FULL | A p-chart that looks in control, but a very uneven station ranking: the problem is *which* stations, not *when* |

## Collecting this for real

- Counts per station at fixed intervals, from manual scheduled counts or a permissioned station-status feed snapshot
- One time zone, and station capacity verified once per station
- Sampling across weekdays and weekends, and across the seasons
- Watch for missing snapshots, and remember that the same station is observed repeatedly, so observations are not fully independent
