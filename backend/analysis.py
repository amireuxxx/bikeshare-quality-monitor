"""Bike-share station monitoring and statistical process control."""
import csv,io,math
from collections import defaultdict
from datetime import datetime
REQUIRED={"timestamp","station_id","capacity","bikes_available"}
def parse_csv(content):
    try: decoded=content.decode("utf-8-sig")
    except UnicodeDecodeError as e: raise ValueError("CSV must be UTF-8") from e
    reader=csv.DictReader(io.StringIO(decoded))
    if not reader.fieldnames or not REQUIRED.issubset(reader.fieldnames):
        raise ValueError("Required columns: timestamp, station_id, capacity, bikes_available")
    rows=[]; seen=set()
    for i,r in enumerate(reader,start=2):
        try:
            t=datetime.fromisoformat(r["timestamp"].replace("Z","+00:00")).isoformat()
            s=r["station_id"].strip(); c=int(r["capacity"]); b=int(r["bikes_available"])
            if not s or c<=0 or not 0<=b<=c: raise ValueError("Invalid station or capacity/bikes")
            if (t,s) in seen: raise ValueError("Duplicate timestamp and station")
            seen.add((t,s))
            rows.append(dict(timestamp=t,station_id=s,capacity=c,bikes_available=b,docks_available=c-b,status=("EMPTY" if b==0 else "FULL" if b==c else "AVAILABLE")))
        except (KeyError,TypeError,ValueError) as e: raise ValueError(f"Row {i}: {e}") from e
        if len(rows)>50000: raise ValueError("Limit 50,000 observations")
    if not rows: raise ValueError("CSV has no data")
    return sorted(rows,key=lambda r:(r["timestamp"],r["station_id"]))
def analyze(rows):
    if not rows: raise ValueError("At least one observation needed")
    times=defaultdict(list); stations=defaultdict(list)
    for r in rows: times[r["timestamp"]].append(r);stations[r["station_id"]].append(r)
    blocked=lambda r: r["status"]!="AVAILABLE"
    pbar=sum(blocked(r) for r in rows)/len(rows)
    chart=[]
    for t,g in sorted(times.items()):
        n=len(g); rate=sum(blocked(r) for r in g)/n
        delta=3*math.sqrt(pbar*(1-pbar)/n)
        u=min(1.,pbar+delta); l=max(0.,pbar-delta)
        chart.append(dict(timestamp=t,n=n,blocked_rate=round(rate,6),center=round(pbar,6),ucl=round(u,6),lcl=round(l,6),out_of_control=rate>u+1e-12 or rate<l-1e-12))
    summaries=[]
    for sid,g in sorted(stations.items()):
        latest=max(g,key=lambda r:r["timestamp"])
        summaries.append(dict(station_id=sid,observations=len(g),blocked_rate=round(sum(blocked(r) for r in g)/len(g),6),empty_count=sum(r["status"]=="EMPTY" for r in g),full_count=sum(r["status"]=="FULL" for r in g),latest_status=latest["status"],latest_bikes=latest["bikes_available"],latest_docks=latest["docks_available"],capacity=latest["capacity"]))
    summaries.sort(key=lambda s:(-s["blocked_rate"],s["station_id"]))
    dispatch=[dict(station_id=s["station_id"],issue=s["latest_status"],recommendation=("Deliver bikes" if s["latest_status"]=="EMPTY" else "Redistribute bikes"),blocked_rate=s["blocked_rate"]) for s in summaries if s["latest_status"]!="AVAILABLE"]
    return dict(summary=dict(observations=len(rows),stations=len(stations),timepoints=len(times),blocked_rate=round(pbar,6),out_of_control_timepoints=sum(c["out_of_control"] for c in chart),currently_unusable_stations=len(dispatch)),p_chart=chart,stations=summaries,dispatch=dispatch,methodology=dict(chart="Three-sigma p-chart of blocked station observations by time; variable subgroup n",warning="Exploratory: correlated stations and rush-hour variation may violate binomial assumptions; signals do not establish causality"))
