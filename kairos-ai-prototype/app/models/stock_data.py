from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class StockInfo(BaseModel):
    """종목 기본 정보"""
    code: str
    name: str
    current_price: int
    change_rate: float
    change_price: int
    volume: int
    ai_summary: str

class SupplyDemandPeriod(BaseModel):
    """기간별 수급 정보"""
    period: str  # "1일", "1주일", "1개월"
    foreign_net: str
    institution_net: str
    individual_net: str

class SupplyDemand(BaseModel):
    """수급 정보"""
    foreign_net: str
    institution_net: str
    individual_net: str
    summary: str
    period_data: List[SupplyDemandPeriod]  # 일주일, 한달 데이터

class Performance(BaseModel):
    """실적 정보"""
    revenue: str
    operating_profit: str
    net_profit: str
    summary: str
    # 비교 데이터
    revenue_yoy: Optional[str] = None  # 전년동기대비
    revenue_qoq: Optional[str] = None  # 직전분기대비
    operating_profit_yoy: Optional[str] = None
    operating_profit_qoq: Optional[str] = None
    operating_profit_vs_consensus: Optional[str] = None  # 컨센서스대비
    earnings_surprise: Optional[str] = None  # 어닝서프라이즈 여부

class NewsItem(BaseModel):
    """뉴스 아이템"""
    date: str
    title: str
    summary: str
    url: str
    sentiment: str  # "positive", "negative", "neutral"

class InvestmentPoint(BaseModel):
    """투자 포인트"""
    positive: List[str]
    negative: List[str]

class AnalystOpinion(BaseModel):
    """애널리스트 의견"""
    target_price: str
    opinion: str
    firm: str
    trend: str  # "up", "down", "neutral" - 목표가 상승/하락 추세

class SectorNews(BaseModel):
    """섹터 뉴스"""
    date: str
    title: str
    summary: str
    sentiment: str  # "positive", "negative", "neutral"

class InvestmentMetrics(BaseModel):
    """투자 지표"""
    per: str
    pbr: str
    roe: str
    dividend_yield: str
    market_cap: str
    shares_outstanding: str

class StockAnalysis(BaseModel):
    """종목 종합 분석 데이터"""
    stock_info: StockInfo
    news_summary: str
    supply_demand: SupplyDemand
    performance: Performance
    investment_points: InvestmentPoint
    recent_issues: List[NewsItem]
    analyst_opinions: List[AnalystOpinion]
    sector_name: str
    sector_news: List[SectorNews]
    investment_metrics: InvestmentMetrics


