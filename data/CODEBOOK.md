# Test data codebook
All three files are synthetic and use identical schemas. One row = one station sampled every 15 minutes.

| Column | Description | Unit |
|---|---|---|
| timestamp | ISO 8601 observation time (local) | time |
| station_id | Station identifier ST01 to ST15 | categorical |
| capacity | Total available docks | docks |
| bikes_available | Bikes parked and available for rental | bikes |

Files: `baseline.csv` = relatively stable station availability; `commute_shortage.csv` = artificial wave of empty stations; `mixed_imbalance.csv` = artificial empty/full imbalance. These are demonstration scenarios, not field measurements.

Real collection would require scheduled manual counts or permissioned station-feed snapshots, standardized time zone, station capacity verification, and sampling across weekdays/weekends. Missingness and multiple observations of the same station should be monitored.