from fastapi import FastAPI, Body
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from dotenv import load_dotenv
import json
import sys

# 현재 디렉토리를 Python path에 추가
sys.path.insert(0, str(Path(__file__).parent))

# 환경 변수 로드
load_dotenv()

from models.etf_analyzer import ETFAnalyzer
from services.llm import explain

app = FastAPI(title="VolumeQuant Lite", version="0.2.0")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

STATIC_DIR = Path(__file__).parent / "static"

# 전역 분석기 인스턴스
analyzer = ETFAnalyzer()

@app.get("/")
def serve_index():
    return FileResponse(STATIC_DIR / "index.html")

@app.get("/api/analysis/full")
async def api_full_analysis(tickers: str = None):
    """
    전체 ETF 거래량 분석
    ?tickers=XLK,XLF,XLE 형태로 특정 티커 지정 가능
    """
    ticker_list = tickers.split(',') if tickers else None
    result = analyzer.run_full_pipeline(tickers=ticker_list)
    return JSONResponse(result)

@app.get("/api/analysis/quick")
async def api_quick_scan(tickers: str = None):
    """
    빠른 스캔 (최근 5일 데이터)
    실시간 모니터링용
    """
    ticker_list = tickers.split(',') if tickers else None
    result = analyzer.quick_scan(tickers=ticker_list)
    return JSONResponse(result)

@app.get("/api/blob")
def api_blob():
    """레거시 엔드포인트 - 빠른 스캔으로 리다이렉트"""
    result = analyzer.quick_scan()
    return JSONResponse(result)

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
