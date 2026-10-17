# Devpost project draft (verify every line with your teammates before submitting)

**Project name:** BikeShare Quality Monitor

**Elevator pitch:** A quality-control tool for bikeshare operators: a p-chart shows when stations are unusable, a ranking shows where, and a dispatch list shows which vans to send, instead of dispatching blindly.

## Inspiration
The Urban Systems prompt describes a "docks full / docks empty" crisis at rush hour, with maintenance vans dispatched blindly. Operators need to separate ordinary variation from a real special cause, and to know which stations need attention.

## What it does
Upload station counts as a CSV (timestamp, station, capacity, bikes available). The tool plots the share of blocked stations at each time on a 3-sigma p-chart with variable limits, ranks stations by how often they are empty or full, and lists the stations that need a van at the latest observation. Three synthetic scenarios show the behaviors: a stable system, a morning commute wave (7 points above the limit) and chronic imbalance at four stations that the time chart cannot see but the ranking does.

## How we built it
Python and FastAPI for the statistics and API, a browser dashboard with Chart.js, 14 automated tests (including a hand-calculated p-chart), GitHub Actions, and Posit Connect for deployment. The statistic is one plain tested module, and the three datasets are regenerated exactly by `generate_data.py`.

## Challenges and limitations
The same stations are observed repeatedly and commuting is predictable, so the binomial assumptions are only approximate; the tool says so. The datasets are synthetic, there is no live sensor feed, and dispatch suggestions use the latest observation only.

## Accomplishments
An end-to-end prototype with upload, an interactive p-chart, three documented test datasets, a codebook, a demo walkthrough and reproducible code.

## What's next
Stratify by time of day and by station group, add run-rule tests (for example eight points on one side of the center line), map the stations, and add staff and vehicle constraints once real data are collected.

**GitHub:** https://github.com/amireuxxx/bikeshare-quality-monitor

**Demo URL:** [ADD the verified live Posit Connect URL]

**Team members:** [ADD names, with each person's consent]

**Important:** do not claim the tool is live or deployed unless the URL has been tested.
