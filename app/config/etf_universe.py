"""
ETF 유니버스 정의
미국 섹터 ETF 및 인더스트리 ETF 중심
"""

# 섹터 ETF (SPDR Sector ETFs)
SECTOR_ETFS = {
    "XLK": "Technology",
    "XLF": "Financials", 
    "XLE": "Energy",
    "XLB": "Materials",
    "XLY": "Consumer Discretionary",
    "XLP": "Consumer Staples",
    "XLV": "Healthcare",
    "XLI": "Industrials",
    "XLU": "Utilities",
    "XLRE": "Real Estate",
    "XLC": "Communication Services"
}

# 인더스트리 ETF (테마/산업별)
INDUSTRY_ETFS = {
    "SOXX": "Semiconductors",
    "ITB": "Homebuilders",
    "NAIL": "Homebuilders 3x",
    "DPST": "Regional Banks 3x",
    "XBI": "Biotech",
    "XRT": "Retail",
    "XHB": "Homebuilders",
    "KRE": "Regional Banks",
    "IBB": "Biotech",
    "IYT": "Transportation",
    "JETS": "Airlines",
    "TAN": "Solar Energy",
    "HACK": "Cybersecurity",
    "ARKK": "Innovation",
    "ARKG": "Genomics"
}

# 전체 유니버스
ALL_ETFS = {**SECTOR_ETFS, **INDUSTRY_ETFS}

# 거래량 이벤트 탐지 설정
VOLUME_SPIKE_THRESHOLDS = {
    "extreme": 2.5,      # 250% 이상 (극단적 폭증)
    "high": 2.0,         # 200% 이상 (강한 폭증)
    "medium": 1.5,       # 150% 이상 (중간 폭증)
    "alert": 1.3         # 130% 이상 (주의)
}

# 분석 기간 설정
LOOKBACK_DAYS = 252      # 1년 (트레이딩 일수)
MA_PERIOD = 20           # 20일 이동평균
EVENT_HISTORY_DAYS = 30  # 최근 30일 이벤트 추적

