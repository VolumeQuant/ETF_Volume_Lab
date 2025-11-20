# 📊 VolumeQuant - ETF Volume Lab

**v0.2.0**

미국 ETF의 거래량 이상징후를 탐지하고 분석하는 AI 기반 트레이딩 시스템

## 🎯 프로젝트 목적

- **이벤트 기반 탐지**: ETF 거래량 폭증/급감 실시간 감지
- **시장 이상징후 분석**: 거래량 스파이크와 가격 반응 상관관계 분석  
- **포트폴리오 구성**: 이벤트 기반 자동 비중 조정
- **자동매매 준비**: 한국투자증권/키움 API 연동 확장 계획

## ✨ 핵심 기능

### 1. 거래량 이벤트 탐지 시스템
- ✅ yfinance 기반 실시간 데이터 수집
- ✅ 20일 이동평균 대비 거래량 스파이크 감지
- ✅ 4단계 이벤트 레벨 분류 (EXTREME, HIGH, MEDIUM, ALERT)
- ✅ 거래량-가격 상관관계 분석

### 2. ETF 유니버스
**섹터 ETF**: XLK, XLF, XLE, XLB, XLY, XLP, XLV, XLI, XLU, XLRE, XLC

**인더스트리 ETF**: SOXX(반도체), ITB(주택), NAIL(주택3x), DPST(은행3x), XBI(바이오), ARKK(혁신) 등

### 3. 웹 대시보드
- 📈 실시간 거래량 스파이크 모니터링
- 📊 Chart.js 기반 인터랙티브 차트
- 🤖 AI 기반 시장 인사이트 생성 (Groq API / Rule-based)
- ⚡ 빠른 스캔 (5일) & 전체 분석 (1년) 모드
- 🔧 강화된 에러 처리 및 JSON 직렬화

## 🚀 시작하기

### 필수 요구사항
- Python 3.10+
- pip / conda

### 설치

```bash
# 1. 저장소 클론
git clone <repository-url>
cd ETF_Volume_Lab

# 2. 가상환경 생성 (선택사항)
conda create -n volumequant python=3.10
conda activate volumequant

# 3. 패키지 설치
pip install -r requirements.txt

# 4. 환경 변수 설정 (선택사항 - AI 기능용)
# 프로젝트 루트에 .env 파일 생성
cat > .env << EOF
PROVIDER=groq
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant
EOF

# 또는 AI 없이 사용 (rule-based만 사용)
# .env 파일을 만들지 않거나 PROVIDER를 비워두면 됩니다.
# Groq API 키 발급: https://console.groq.com/
```

### 실행

```bash
# app 디렉토리로 이동
cd app

# 서버 실행
python main.py
```

서버가 시작되면 브라우저에서 접속:
```
http://localhost:8000
```

## 📁 프로젝트 구조

```
ETF_Volume_Lab/
├── app/
│   ├── main.py                    # FastAPI 서버
│   ├── config/
│   │   └── etf_universe.py       # ETF 유니버스 & 설정
│   ├── models/
│   │   ├── etf_data_collector.py # 데이터 수집 모듈
│   │   ├── volume_event_detector.py # 이벤트 탐지 엔진
│   │   └── etf_analyzer.py       # 통합 분석 파이프라인
│   ├── services/
│   │   └── llm.py                # AI 분석 (Groq/Rule-based)
│   └── static/
│       └── index.html            # 웹 대시보드
├── requirements.txt
└── README.md
```

## 🔧 API 엔드포인트

### `GET /api/analysis/quick`
빠른 스캔 (최근 5일 데이터)
```bash
curl http://localhost:8000/api/analysis/quick
```

### `GET /api/analysis/full`
전체 분석 (기본 1년 데이터)
```bash
curl http://localhost:8000/api/analysis/full

# 특정 티커만 분석
curl "http://localhost:8000/api/analysis/full?tickers=XLK,XLF,SOXX"

# 기간 지정 (1y, 6mo, 3mo 등)
curl "http://localhost:8000/api/analysis/full?period=6mo"

# 티커와 기간 모두 지정
curl "http://localhost:8000/api/analysis/full?tickers=XLK,SOXX&period=3mo"
```

**쿼리 파라미터**:
- `tickers`: 쉼표로 구분된 티커 심볼 (선택사항, 기본값: 전체 유니버스)
- `period`: 데이터 기간 (선택사항, 기본값: `1y`)
  - 사용 가능: `1d`, `5d`, `1mo`, `3mo`, `6mo`, `1y`, `2y`, `5y`, `10y`, `ytd`, `max`

### `POST /api/explain`
AI 인사이트 생성
```bash
curl -X POST http://localhost:8000/api/explain \
  -H "Content-Type: application/json" \
  -d '{"blob": {...분석결과...}}'
```

## 📊 거래량 스파이크 기준

| 레벨 | 임계값 | 설명 |
|------|--------|------|
| EXTREME | 2.5x 이상 | 극단적 폭증 - 즉시 주목 |
| HIGH | 2.0x 이상 | 강한 폭증 - 중요 이벤트 |
| MEDIUM | 1.5x 이상 | 중간 폭증 - 모니터링 필요 |
| ALERT | 1.3x 이상 | 주의 단계 |

*기준: 20일 이동평균 대비 당일 거래량 비율*

## 🎨 웹 대시보드 기능

1. **빠른 스캔** 🚀
   - 주요 6개 ETF 최근 5일 모니터링
   - 실시간 가격 & 거래량 스파이크
   
2. **전체 분석** 🔍
   - 전체 ETF 유니버스 1년 데이터 분석
   - 이벤트 탐지 & 통계 생성
   - 최대 스파이크 순위

3. **AI 인사이트** 🤖
   - Groq AI (LLaMA3) 기반 시장 분석
   - Rule-based 폴백 시스템
   - 빠른 스캔 / 전체 분석 모드별 맞춤 설명
   - 거래량 패턴 해석 및 투자 시사점 제공

4. **차트 시각화** 📊
   - Chart.js 인터랙티브 차트
   - 거래량 스파이크 분포
   - 색상 코딩 (레벨별)

## 🔮 확장 계획

### Phase 1 (현재) ✅
- [x] 거래량 이벤트 탐지 시스템
- [x] 웹 대시보드
- [x] AI 인사이트 (Groq API + Rule-based)
- [x] 빠른 스캔 & 전체 분석 모드
- [x] 에러 처리 및 안정성 개선
- [x] JSON 직렬화 문제 해결

### Phase 2 (진행 예정)
- [ ] 포트폴리오 백테스팅 시뮬레이션
- [ ] 이벤트 기반 자동 리밸런싱 로직
- [ ] 실시간 알림 시스템 (이메일/텔레그램)
- [ ] 데이터베이스 연동 (PostgreSQL)

### Phase 3 (미래)
- [ ] 강화학습 기반 포트폴리오 최적화
- [ ] 한국투자증권 Open API 연동
- [ ] 자동매매 실행 시스템
- [ ] EPS/매출 성장률 기반 펀더멘털 통합

## 🛠 기술 스택

- **Backend**: Python 3.10, FastAPI, Uvicorn
- **Data**: yfinance, pandas, numpy
- **Visualization**: Chart.js
- **AI**: Groq API (LLaMA3) + Rule-based 폴백
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **HTTP Client**: httpx (async)

## 📝 사용 예시

### 1. 특정 ETF 분석
```python
from app.models.etf_analyzer import ETFAnalyzer

analyzer = ETFAnalyzer()
result = analyzer.run_full_pipeline(tickers=['XLK', 'SOXX'])
print(result['summary'])
```

### 2. 커스텀 임계값 설정
```python
from app.models.volume_event_detector import VolumeEventDetector

detector = VolumeEventDetector(
    ma_period=30,  # 30일 이동평균
    thresholds={
        "extreme": 3.0,
        "high": 2.5,
        "medium": 2.0,
        "alert": 1.5
    }
)
```



---

