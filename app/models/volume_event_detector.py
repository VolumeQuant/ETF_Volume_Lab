"""
거래량 이벤트 탐지 엔진
전일 대비, 이동평균 대비 거래량 급등/급락 감지
"""
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class VolumeEventDetector:
    """거래량 이상징후 탐지기"""
    
    def __init__(
        self, 
        ma_period: int = 20,
        thresholds: Dict[str, float] = None
    ):
        """
        Args:
            ma_period: 이동평균 기간 (기본 20일)
            thresholds: 임계값 딕셔너리
        """
        self.ma_period = ma_period
        self.thresholds = thresholds or {
            "extreme": 2.5,
            "high": 2.0,
            "medium": 1.5,
            "alert": 1.3
        }
    
    def calculate_volume_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        거래량 특성 계산
        - 이동평균
        - 스파이크 비율
        - 전일 대비 변화율
        
        Args:
            df: OHLCV DataFrame (must have 'Ticker', 'Date', 'Volume' columns)
        
        Returns:
            Enhanced DataFrame with volume features
        """
        df = df.copy()
        df = df.sort_values(['Ticker', 'Date'])
        
        # 거래량 이동평균
        df['Volume_MA'] = df.groupby('Ticker')['Volume'].transform(
            lambda x: x.rolling(window=self.ma_period, min_periods=5).mean()
        )
        
        # 거래량 스파이크 비율 (당일 거래량 / 이동평균)
        df['Volume_Spike_Ratio'] = df['Volume'] / df['Volume_MA']
        
        # 전일 대비 거래량 변화율
        df['Volume_Change_Pct'] = df.groupby('Ticker')['Volume'].pct_change() * 100
        
        # 가격 변화율
        df['Price_Change_Pct'] = df.groupby('Ticker')['Close'].pct_change() * 100
        
        return df
    
    def detect_events(
        self, 
        df: pd.DataFrame,
        recent_days: int = 30
    ) -> pd.DataFrame:
        """
        거래량 이벤트 탐지
        
        Args:
            df: Volume features가 포함된 DataFrame
            recent_days: 최근 며칠간 이벤트만 추출
        
        Returns:
            DataFrame with detected events
        """
        df = df.copy()
        
        # 최근 데이터만 필터링
        cutoff_date = df['Date'].max() - pd.Timedelta(days=recent_days)
        recent_df = df[df['Date'] >= cutoff_date].copy()
        
        # 이벤트 레벨 분류 (아직 없는 경우에만)
        if 'Event_Level' not in recent_df.columns:
            def classify_event(ratio):
                if pd.isna(ratio):
                    return None
                if ratio >= self.thresholds['extreme']:
                    return 'EXTREME'
                elif ratio >= self.thresholds['high']:
                    return 'HIGH'
                elif ratio >= self.thresholds['medium']:
                    return 'MEDIUM'
                elif ratio >= self.thresholds['alert']:
                    return 'ALERT'
                return None
            
            recent_df['Event_Level'] = recent_df['Volume_Spike_Ratio'].apply(classify_event)
        
        # 이벤트만 필터링
        events = recent_df[recent_df['Event_Level'].notna()].copy()
        
        # 이벤트 메타데이터 추가
        events['Event_Type'] = 'VOLUME_SPIKE'
        events['Detected_At'] = datetime.now().isoformat()
        
        # 가격 반응 분석
        events['Price_Direction'] = events['Price_Change_Pct'].apply(
            lambda x: 'UP' if x > 0.5 else ('DOWN' if x < -0.5 else 'NEUTRAL')
        )
        
        logger.info(f"총 {len(events)}개 이벤트 탐지 (최근 {recent_days}일)")
        
        return events
    
    def get_event_summary(self, events: pd.DataFrame) -> Dict:
        """
        이벤트 요약 통계
        
        Returns:
            {
                'total_events': int,
                'by_level': dict,
                'by_ticker': dict,
                'latest_events': list
            }
        """
        if events.empty:
            return {
                'total_events': 0,
                'by_level': {},
                'by_ticker': {},
                'latest_events': []
            }
        
        summary = {
            'total_events': len(events),
            'by_level': events['Event_Level'].value_counts().to_dict(),
            'by_ticker': events['Ticker'].value_counts().to_dict(),
            'date_range': {
                'start': events['Date'].min().strftime('%Y-%m-%d'),
                'end': events['Date'].max().strftime('%Y-%m-%d')
            }
        }
        
        # 최신 이벤트 10개
        latest = events.nlargest(10, 'Date')[
            ['Date', 'Ticker', 'Event_Level', 'Volume_Spike_Ratio', 
             'Volume_Change_Pct', 'Price_Change_Pct', 'Price_Direction']
        ].copy()
        
        latest['Date'] = latest['Date'].dt.strftime('%Y-%m-%d')
        summary['latest_events'] = latest.to_dict('records')
        
        return summary
    
    def analyze_ticker(
        self, 
        df: pd.DataFrame, 
        ticker: str,
        lookback_days: int = 90
    ) -> Dict:
        """
        특정 ETF의 거래량 패턴 상세 분석
        
        Returns:
            {
                'ticker': str,
                'current_volume': int,
                'avg_volume': float,
                'volume_spike_ratio': float,
                'event_count': int,
                'price_correlation': float,
                'recent_events': list
            }
        """
        ticker_df = df[df['Ticker'] == ticker].copy()
        
        if ticker_df.empty:
            return None
        
        ticker_df = ticker_df.sort_values('Date')
        recent = ticker_df.tail(lookback_days)
        
        # 현재 (최신) 데이터
        latest = ticker_df.iloc[-1]
        
        # 통계
        avg_volume = recent['Volume'].mean()
        current_spike = latest['Volume_Spike_Ratio']
        
        # 거래량-가격 상관관계
        correlation = recent[['Volume_Change_Pct', 'Price_Change_Pct']].corr().iloc[0, 1]
        
        # 최근 이벤트 (Event_Level 컬럼이 있는 경우만)
        if 'Event_Level' in recent.columns:
            recent_events = recent[recent['Event_Level'].notna()]
        else:
            recent_events = pd.DataFrame()
        
        # recent_events의 Date를 문자열로 변환
        events_list = []
        if not recent_events.empty:
            events_copy = recent_events.tail(5).copy()
            if 'Date' in events_copy.columns:
                events_copy['Date'] = events_copy['Date'].dt.strftime('%Y-%m-%d')
            events_list = events_copy.to_dict('records')
        
        analysis = {
            'ticker': ticker,
            'current_date': latest['Date'].strftime('%Y-%m-%d'),
            'current_price': round(latest['Close'], 2),
            'current_volume': int(latest['Volume']),
            'avg_volume_20d': int(latest['Volume_MA']) if not pd.isna(latest['Volume_MA']) else None,
            'volume_spike_ratio': round(current_spike, 2) if not pd.isna(current_spike) else None,
            'price_change_pct': round(latest['Price_Change_Pct'], 2) if not pd.isna(latest['Price_Change_Pct']) else None,
            'event_count_90d': len(recent_events),
            'volume_price_correlation': round(correlation, 3) if not pd.isna(correlation) else None,
            'recent_events': events_list
        }
        
        return analysis
    
    def find_top_spikes(
        self, 
        df: pd.DataFrame, 
        top_n: int = 10,
        min_date: Optional[str] = None
    ) -> List[Dict]:
        """
        최근 최대 거래량 스파이크 ETF 찾기
        
        Args:
            df: Enhanced DataFrame
            top_n: 상위 N개
            min_date: 최소 날짜 필터
        
        Returns:
            List of top spike events
        """
        temp_df = df.copy()
        
        if min_date:
            temp_df = temp_df[temp_df['Date'] >= min_date]
        
        # 스파이크 비율 기준 정렬
        top_spikes = temp_df.nlargest(top_n, 'Volume_Spike_Ratio')[
            ['Date', 'Ticker', 'Close', 'Volume', 'Volume_MA', 
             'Volume_Spike_Ratio', 'Volume_Change_Pct', 'Price_Change_Pct']
        ].copy()
        
        # Date를 문자열로 변환
        if 'Date' in top_spikes.columns:
            top_spikes['Date'] = pd.to_datetime(top_spikes['Date']).dt.strftime('%Y-%m-%d')
        
        return top_spikes.to_dict('records')

