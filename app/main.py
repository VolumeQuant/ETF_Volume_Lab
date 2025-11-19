from fastapi import FastAPI, Body
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from dotenv import load_dotenv
import json

# 환경 변수 로드
load_dotenv()

from models.sample_model import run_dummy_pipeline
from services.llm import explain

app = FastAPI(title="VolumeQuant Lite", version="0.2.0")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

STATIC_DIR = Path(__file__).parent / "static"

@app.get("/")
def serve_index():
    return FileResponse(STATIC_DIR / "index.html")

@app.get("/api/blob")
def api_blob():
    blob = run_dummy_pipeline()
    return JSONResponse(blob)

@app.post("/api/explain")
async def api_explain(payload: dict = Body(...)):
    if "blob" in payload:
        user_content = json.dumps(payload["blob"], ensure_ascii=False, indent=2)
    else:
        user_content = payload.get("text", "")
    result = await explain(user_content)
    return {"explanation": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
