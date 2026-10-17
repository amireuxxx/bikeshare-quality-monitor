from backend.analysis import parse_csv,analyze
def test_csv_and_stats():
    b=b"timestamp,station_id,capacity,bikes_available\n2026-10-16T12:00:00,A,4,0\n2026-10-16T12:00:00,B,4,2\n"
    result=analyze(parse_csv(b))
    assert result["summary"]["blocked_rate"]==0.5
    assert result["summary"]["stations"]==2
    assert result["dispatch"][0]["station_id"]=="A"
def test_bad_capacity():
    import pytest
    with pytest.raises(ValueError):
        parse_csv(b"timestamp,station_id,capacity,bikes_available\n2026-10-16T12:00:00,A,4,5\n")
def test_duplicate():
    import pytest
    b=b"timestamp,station_id,capacity,bikes_available\n2026-10-16T12:00:00,A,4,1\n2026-10-16T12:00:00,A,4,2\n"
    with pytest.raises(ValueError):parse_csv(b)
