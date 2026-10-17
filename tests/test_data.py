import csv
from pathlib import Path
import generate_data
from backend.analysis import parse_csv, analyze

ROOT = Path(__file__).resolve().parents[1]

def test_generator_matches_committed_files(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    for name, fn, seed0 in [("baseline", generate_data.baseline_mu, 100),
                            ("commute_shortage", generate_data.commute_mu, 200),
                            ("mixed_imbalance", generate_data.imbalance_mu, 300)]:
        generate_data.write(name, generate_data.build(fn, generate_data.pick_seed(fn, seed0)))
        assert (tmp_path / "data" / f"{name}.csv").read_bytes() == (ROOT / "data" / f"{name}.csv").read_bytes()

def test_scenarios_behave_as_documented():
    res = {n: analyze(parse_csv((ROOT / "data" / f"{n}.csv").read_bytes()))
           for n in ("baseline", "commute_shortage", "mixed_imbalance")}
    assert res["baseline"]["summary"]["out_of_control_timepoints"] == 0
    assert res["commute_shortage"]["summary"]["out_of_control_timepoints"] >= 5
    assert res["mixed_imbalance"]["stations"][0]["blocked_rate"] > 0.4
    for r in res.values():
        assert r["summary"]["currently_unusable_stations"] >= 2
