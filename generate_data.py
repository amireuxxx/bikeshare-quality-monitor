"""Regenerate the three synthetic BikeShare test datasets (deterministic).

Run from the repository root:  python generate_data.py
Writes data/baseline.csv, data/commute_shortage.csv, data/mixed_imbalance.csv.

Model: at each timepoint every station holds a fraction of its capacity,
drawn from a normal distribution (mean `mu`, sd `SD`), rounded to whole bikes
and clipped to 0..capacity. A station is "blocked" when it has 0 bikes (EMPTY)
or 0 open docks (FULL). All data are synthetic.
"""
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

STATIONS = [f"ST{i:02d}" for i in range(1, 16)]
CAPACITY = dict(zip(STATIONS, [15, 20, 25, 20, 30, 20, 25, 15, 20, 30, 20, 25, 15, 20, 25]))
START = datetime(2026, 10, 16, 8, 0)
STEPS = 32                      # 08:00 to 15:45, every 15 minutes
SD = 0.24                       # spread of the fill fraction
BASE_MU = 0.50                  # typical station: half full

RESIDENTIAL = STATIONS[0:6]     # ST01-ST06: bikes leave in the morning commute
DOWNTOWN = STATIONS[6:10]       # ST07-ST10: docks fill up in the morning commute
CHRONIC_EMPTY = ["ST03", "ST09"]   # hill / low-demand-to-return stations
CHRONIC_FULL = ["ST05", "ST12"]    # popular destination stations

def build(mu_fn, seed):
    rng = random.Random(seed)
    rows = []
    for step in range(STEPS):
        ts = (START + timedelta(minutes=15 * step)).isoformat()
        for s in STATIONS:
            cap = CAPACITY[s]
            frac = rng.gauss(mu_fn(s, step), SD)
            bikes = min(cap, max(0, round(frac * cap)))
            rows.append((ts, s, cap, bikes))
    return rows

def baseline_mu(s, step):
    return BASE_MU

def commute_mu(s, step):
    if step <= 7:               # 08:00-09:45 morning commute wave
        if s in RESIDENTIAL:
            return -0.20        # residential stations run empty (demand pulls bikes out)
        if s in DOWNTOWN:
            return 1.20         # downtown stations run full (bikes pile up at work)
    return BASE_MU

def imbalance_mu(s, step):
    if s in CHRONIC_EMPTY:
        return 0.10
    if s in CHRONIC_FULL:
        return 0.90
    return BASE_MU

def blocked_at_last(rows):
    last = max(r[0] for r in rows)
    return sum(1 for r in rows if r[0] == last and (r[3] == 0 or r[3] == r[2]))

def pick_seed(mu_fn, start_seed):
    """First seed from start_seed whose final timepoint has at least 2 blocked stations,
    so the 'latest unavailable stations' panel has something to show."""
    seed = start_seed
    while blocked_at_last(build(mu_fn, seed)) < 2:
        seed += 1
    return seed

def write(name, rows):
    path = Path("data") / f"{name}.csv"
    path.parent.mkdir(exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["timestamp", "station_id", "capacity", "bikes_available"])
        w.writerows(rows)

if __name__ == "__main__":
    for name, fn, seed0 in [("baseline", baseline_mu, 100),
                            ("commute_shortage", commute_mu, 200),
                            ("mixed_imbalance", imbalance_mu, 300)]:
        write(name, build(fn, pick_seed(fn, seed0)))
        print("wrote data/%s.csv" % name)
