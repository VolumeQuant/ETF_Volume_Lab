from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api import stock_analysis

app = FastAPI(title="KAIROS AI 시황 분석 프로토타입")

# API 라우터 등록
app.include_router(stock_analysis.router, prefix="/api")

# 정적 파일 서빙
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
async def root():
    """메인 페이지"""
    return FileResponse("app/static/index.html")

@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {"status": "ok"}


