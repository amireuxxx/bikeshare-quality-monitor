"""Known-answer and degenerate-case tests for the p-chart (the statistic the tool is graded on).

Hand calculation for the known-answer case: 4 timepoints x 10 stations, with 1, 1, 1 and 9
stations blocked. pbar = 12/40 = 0.30. Every timepoint has n = 10, so
3*sqrt(pbar*(1-pbar)/n) = 3*sqrt(0.3*0.7/10) = 0.434741.
UCL = 0.30 + 0.434741 = 0.734741 and LCL = max(0, 0.30 - 0.434741) = 0.
Only the last timepoint (9/10 = 0.90) is above the UCL.
"""
import pytest
from backend.analysis import parse_csv, analyze

HEADER = "timestamp,station_id,capacity,bikes_available\n"


def make_csv(blocked_per_time, n_stations=10, capacity=4):
    """One row per station per timepoint; a blocked station has 0 bikes (EMPTY)."""
    lines = []
    for t, k in enumerate(blocked_per_time):
        ts = f"2026-10-16T08:{t * 15:02d}:00" if t < 4 else f"2026-10-16T09:{(t - 4) * 15:02d}:00"
        for s in range(n_stations):
            bikes = 0 if s < k else 2
            lines.append(f"{ts},S{s:02d},{capacity},{bikes}")
    return (HEADER + "\n".join(lines) + "\n").encode()


def test_p_chart_known_answer():
    result = analyze(parse_csv(make_csv([1, 1, 1, 9])))
    chart = result["p_chart"]
    assert result["summary"]["blocked_rate"] == pytest.approx(0.30)
    assert all(c["center"] == pytest.approx(0.30) for c in chart)
    assert all(c["ucl"] == pytest.approx(0.734741, abs=1e-6) for c in chart)
    assert all(c["lcl"] == 0.0 for c in chart)
    assert [c["out_of_control"] for c in chart] == [False, False, False, True]
    assert result["summary"]["out_of_control_timepoints"] == 1


def test_limits_are_clipped_to_zero_and_one():
    result = analyze(parse_csv(make_csv([5, 5], n_stations=2)))   # n = 2 gives very wide limits
    for c in result["p_chart"]:
        assert 0.0 <= c["lcl"] <= c["center"] <= c["ucl"] <= 1.0


def test_degenerate_constant_data_has_no_signals():
    """Nothing is ever blocked: pbar = 0, limits collapse to 0, and no point is flagged."""
    result = analyze(parse_csv(make_csv([0, 0, 0, 0])))
    assert result["summary"]["blocked_rate"] == 0.0
    assert all(c["ucl"] == 0.0 and c["lcl"] == 0.0 for c in result["p_chart"])
    assert result["summary"]["out_of_control_timepoints"] == 0
    assert result["dispatch"] == []


def test_degenerate_single_timepoint():
    result = analyze(parse_csv(make_csv([3])))
    assert result["summary"]["timepoints"] == 1
    assert result["p_chart"][0]["blocked_rate"] == pytest.approx(0.3)


def test_variable_subgroup_size_changes_limit_width():
    """A timepoint with fewer stations observed gets wider limits (variable-n p-chart)."""
    rows = HEADER
    rows += "2026-10-16T08:00:00,A,4,0\n2026-10-16T08:00:00,B,4,2\n"
    for s in "ABCDEFGHIJ":
        rows += f"2026-10-16T08:15:00,{s},4,2\n"
    chart = analyze(parse_csv(rows.encode()))["p_chart"]
    assert chart[0]["n"] == 2 and chart[1]["n"] == 10
    assert (chart[0]["ucl"] - chart[0]["center"]) > (chart[1]["ucl"] - chart[1]["center"])
