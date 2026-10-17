# Devpost project draft — verify with your teammates

**Project name:** BikeShare Quality Monitor

**Elevator pitch:** A quality control tool that uses statistical process control to monitor bike-sharing stations, detect unusual patterns, and identify bike or dock shortages.

## Inspiration
Bike-share systems can be hard to use when stations run empty or docks become full. Operators need a way to turn observations into actionable service monitoring.

## What it does
Upload station counts as CSV, calculate the share of station observations blocked at each time, visualize a 3-sigma p-chart, view each station's event frequency, and see which stations currently need attention.

## How we built it
Python, FastAPI, JavaScript, HTML/CSS and Chart.js. We calculate pooled binomial p-chart limits, validate input CSVs, and test the tool with three fully synthetic scenarios.

## Challenges and limitations
Repeated station observations and predictable commute cycles complicate binomial assumptions. This demonstration does not ingest live sensors or optimize vehicle routes.

## Accomplishments
A reproducible end-to-end prototype with upload, interactive statistics, example data and transparent documentation.

## What's next
Add stratification by time of day, geographic station maps, and staff allocation constraints after collecting real data.

**GitHub:** https://github.com/amireuxxx/bikeshare-quality-monitor

**Demo URL:** [ADD verified live Posit Connect URL]

**Team members:** [ADD names, with their consent]

**Important:** Do not claim the tool is live or that it was deployed unless the URL has been tested.