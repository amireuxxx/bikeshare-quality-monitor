from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app

client=TestClient(app)
ROOT=Path(__file__).resolve().parents[1]

def test_health():
    assert client.get("/api/health").json()=={"status":"ok"}

def test_home_and_examples():
    assert client.get("/").status_code==200
    examples=client.get("/api/examples")
    assert examples.status_code==200
    assert len(examples.json())==3

def test_all_sample_csv_files():
    for name in ("baseline.csv","commute_shortage.csv","mixed_imbalance.csv"):
        path=ROOT/"data"/name
        response=client.post("/api/analyze",files={"file":(name,path.read_bytes(),"text/csv")})
        assert response.status_code==200, (name,response.text)
        body=response.json()
        assert body["summary"]["observations"]>0
        assert len(body["p_chart"])>0
        assert len(body["stations"])>0

def test_invalid_csv_rejected():
    response=client.post("/api/analyze",files={"file":("broken.csv",b"bad,headers\n1,2\n","text/csv")})
    assert response.status_code==422
