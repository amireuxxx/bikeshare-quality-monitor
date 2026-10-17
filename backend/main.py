from pathlib import Path
from fastapi import FastAPI,File,UploadFile,HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .analysis import parse_csv,analyze
app=FastAPI(title="BikeShare Quality Monitor",version="1.0")
ROOT=Path(__file__).resolve().parents[1]
@app.get("/api/health")
def health(): return {"status":"ok"}
@app.post("/api/analyze")
async def analyze_upload(file:UploadFile=File(...)):
    try:
        raw=await file.read(5_000_001)
        if len(raw)>5_000_000: raise ValueError("Maximum file size 5MB")
        return analyze(parse_csv(raw))
    except ValueError as e: raise HTTPException(status_code=422,detail=str(e))
@app.get("/api/examples")
def examples(): return [{"filename":n,"url":"data/"+n} for n in ("baseline.csv","commute_shortage.csv","mixed_imbalance.csv")]
app.mount("/data",StaticFiles(directory=ROOT/"data"),name="data")
app.mount("/static",StaticFiles(directory=ROOT/"static"),name="static")
@app.get("/")
def root(): return FileResponse(ROOT/"standalone.html")
