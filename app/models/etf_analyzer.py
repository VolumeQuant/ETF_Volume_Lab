"""
ETF 통합 분석 파이프라인
데이터 수집 → 특성 계산 → 이벤트 탐지 → 결과 생성
"""
from datetime import datetime
import pandas as pd
from typing import Dict, List, Optional
import logging
import sys
from pathlib import Path

# 상위 디렉토리를 path에 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.etf_data_collector import ETFDataCollector
from models.volume_event_detector import VolumeEventDetector
from config.etf_universe import (
    ALL_ETFS, 
    VOLUME_SPIKE_THRESHOLDS,
    MA_PERIOD,
    EVENT_HISTORY_DAYS,
    LOOKBACK_DAYS
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ETFAnalyzer:
    """ETF 거래량 분석 통합 시스템"""
    
    def __init__(self):
        self.collector = ETFDataCollector()
        self.detector = VolumeEventDetector(
            ma_period=MA_PERIOD,
            thresholds=VOLUME_SPIKE_THRESHOLDS
        )
        self.data_cache = None
        self.last_update = None
    
    def run_full_pipeline(
        self, 
        tickers: Optional[List[str]] = None,
        period: str = "1y",
        force_refresh: bool = False
    ) -> Dict:
        """
        전체 분석 파이프라인 실행
        
        Args:
            tickers: 분석할 티커 리스트 (None이면 전체 유니버스)
            period: 데이터 수집 기간
            force_refresh: 캐시 무시하고 재수집
        
        Returns:
            {
                'metadata': {...},
                'summary': {...},
                'events': [...],
                'top_spikes': [...],
                'ticker_analysis': {...}
            }
        """
        logger.info("=== ETF 분석 파이프라인 시작 ===")
        
        # 1단계: 데이터 수집
        if tickers is None:
            tickers = list(ALL_ETFS.keys())
        
        logger.info(f"분석 대상: {len(tickers)}개 ETF")
        
        try:
            df = self.collector.fetch_multiple(tickers, period=period)
            logger.info(f"데이터 수집 완료: {len(df)} rows")
        except Exception as e:
            logger.error(f"데이터 수집 실패: {e}")
            return self._error_response(str(e))
        
        # 2단계: 거래량 특성 계산
        df = self.detector.calculate_volume_features(df)
        logger.info("거래량 특성 계산 완료")
        
        # 3단계: 이벤트 탐지
        events = self.detector.detect_events(df, recent_days=EVENT_HISTORY_DAYS)
        event_summary = self.detector.get_event_summary(events)
        logger.info(f"이벤트 탐지 완료: {event_summary['total_events']}개")
        
        # 4단계: 최대 스파이크 찾기
        cutoff_date = df['Date'].max() - pd.Timedelta(days=EVENT_HISTORY_DAYS)
        top_spikes = self.detector.find_top_spikes(
            df, 
            top_n=10,
            min_date=cutoff_date
        )
        
        # 5단계: 개별 티커 분석 (이벤트 발생한 티커만)
        event_tickers = events['Ticker'].unique() if not events.empty else []
        ticker_analysis = {}
        
        for ticker in event_tickers[:5]:  # 상위 5개만
            analysis = self.detector.analyze_ticker(df, ticker)
            if analysis:
                ticker_analysis[ticker] = analysis
        
        # 캐시 업데이트
        self.data_cache = df
        self.last_update = datetime.now()
        
        # 최종 결과
        result = {
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'tickers_analyzed': len(tickers),
                'data_rows': len(df),
                'date_range': {
                    'start': df['Date'].min().strftime('%Y-%m-%d'),
                    'end': df['Date'].max().strftime('%Y-%m-%d')
                },
                'version': '0.2.0'
            },
            'summary': event_summary,
            'top_spikes': top_spikes,
            'ticker_analysis': ticker_analysis,
            'etf_universe': {ticker: ALL_ETFS[ticker] for ticker in tickers if ticker in ALL_ETFS}
        }
        
        logger.info("=== 파이프라인 완료 ===")
        return result
    
    def quick_scan(self, tickers: Optional[List[str]] = None) -> Dict:
        """
        빠른 스캔 (최근 5일 데이터만)
        실시간 모니터링용
        """
        if tickers is None:
            # 주요 ETF만
            tickers = ['XLK', 'XLF', 'XLE', 'XLY', 'SOXX', 'ITB']
        
        try:
            df = self.collector.fetch_multiple(tickers, period="5d")
            df = self.detector.calculate_volume_features(df)
            
            latest_data = []
            for ticker in tickers:
                ticker_df = df[df['Ticker'] == ticker]
                if not ticker_df.empty:
                    latest = ticker_df.iloc[-1]
                    latest_data.append({
                        'ticker': ticker,
                        'name': ALL_ETFS.get(ticker, 'Unknown'),
                        'price': round(latest['Close'], 2),
                        'volume': int(latest['Volume']),
                        'volume_spike_ratio': round(latest['Volume_Spike_Ratio'], 2) if not pd.isna(latest['Volume_Spike_Ratio']) else None,
                        'price_change_pct': round(latest['Price_Change_Pct'], 2) if not pd.isna(latest['Price_Change_Pct']) else None
                    })
            
            return {
                'timestamp': datetime.now().isoformat(),
                'mode': 'quick_scan',
                'data': latest_data
            }
        
        except Exception as e:
            logger.error(f"빠른 스캔 실패: {e}")
            return self._error_response(str(e))
    
    def _error_response(self, error_msg: str) -> Dict:
        """에러 응답 생성"""
        return {
            'error': True,
            'message': error_msg,
            'timestamp': datetime.now().isoformat()
        }

