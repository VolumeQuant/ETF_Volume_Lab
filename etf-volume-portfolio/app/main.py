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
async def api_full_analysis(tickers: str = None, period: str = "1y"):
    """
    전체 ETF 거래량 분석
    ?tickers=XLK,XLF,XLE 형태로 특정 티커 지정 가능
    ?period=1y, 6mo, 3mo 등 기간 지정 가능
    """
    try:
        ticker_list = tickers.split(',') if tickers else None
        result = analyzer.run_full_pipeline(tickers=ticker_list, period=period)
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse(
            content={
                "error": True,
                "message": f"분석 중 오류가 발생했습니다: {str(e)}",
                "timestamp": __import__('datetime').datetime.now().isoformat()
            },
            status_code=500
        )

@app.get("/api/analysis/quick")
async def api_quick_scan(tickers: str = None):
    """
    빠른 스캔 (최근 5일 데이터)
    실시간 모니터링용
    """
    try:
        ticker_list = tickers.split(',') if tickers else None
        result = analyzer.quick_scan(tickers=ticker_list)
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse(
            content={
                "error": True,
                "message": f"빠른 스캔 중 오류가 발생했습니다: {str(e)}",
                "timestamp": __import__('datetime').datetime.now().isoformat()
            },
            status_code=500
        )

@app.get("/api/blob")
def api_blob():
    """레거시 엔드포인트 - 빠른 스캔으로 리다이렉트"""
    result = analyzer.quick_scan()
    return JSONResponse(result)

@app.post("/api/explain")
async def api_explain(payload: dict = Body(...)):
    if "blob" in payload:
        blob = payload["blob"]
        # 데이터 크기 축소: 핵심 정보만 추출
        summary_data = _create_summary_for_ai(blob)
        user_content = json.dumps(summary_data, ensure_ascii=False, indent=2)
    else:
        user_content = payload.get("text", "")
    result = await explain(user_content)
    return {"explanation": result}

def _create_summary_for_ai(data: dict) -> dict:
    """AI 전송용 요약 데이터 생성 (토큰 절약)"""
    summary = {}
    
    # 빠른 스캔 모드
    if data.get("mode") == "quick_scan":
        summary = {
            "mode": "quick_scan",
            "timestamp": data.get("timestamp", ""),
            "data": data.get("data", [])[:10]  # 최대 10개만
        }
    # 전체 분석 모드
    else:
        summary = {
            "mode": "full_analysis",
            "metadata": {
                "date_range": data.get("metadata", {}).get("date_range", {}),
                "tickers_analyzed": data.get("metadata", {}).get("tickers_analyzed", 0)
            },
            "summary": {
                "total_events": data.get("summary", {}).get("total_events", 0),
                "by_level": data.get("summary", {}).get("by_level", {}),
                "latest_events": data.get("summary", {}).get("latest_events", [])[:5]  # 최대 5개
            },
            "top_spikes": data.get("top_spikes", [])[:5]  # 최대 5개
        }
    
    return summary

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
