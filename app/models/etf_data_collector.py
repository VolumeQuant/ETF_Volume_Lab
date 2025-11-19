"""
ETF 데이터 수집 모듈
yfinance를 사용하여 실시간 ETF 데이터 수집
"""
from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class ETFDataCollector:
    """ETF OHLCV 데이터 수집기"""
    
    def __init__(self):
        self.cache = {}
        self.cache_timestamp = {}
        self.cache_ttl = 300  # 5분 캐시
    
    def fetch_data(
        self, 
        ticker: str, 
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: str = "1y"
    ) -> pd.DataFrame:
        """
        단일 ETF 데이터 수집
        
        Args:
            ticker: ETF 티커 심볼
            start_date: 시작일 (YYYY-MM-DD)
            end_date: 종료일 (YYYY-MM-DD)
            period: 기간 (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
        
        Returns:
            DataFrame with OHLCV data
        """
        try:
            # 캐시 확인
            cache_key = f"{ticker}_{period}_{start_date}_{end_date}"
            if cache_key in self.cache:
                if (datetime.now() - self.cache_timestamp[cache_key]).seconds < self.cache_ttl:
                    logger.info(f"캐시에서 {ticker} 데이터 로드")
                    return self.cache[cache_key].copy()
            
            # yfinance로 데이터 다운로드
            etf = yf.Ticker(ticker)
            
            if start_date and end_date:
                df = etf.history(start=start_date, end=end_date)
            else:
                df = etf.history(period=period)
            
            if df.empty:
                raise ValueError(f"{ticker} 데이터 없음")
            
            df = df.reset_index()
            df['Ticker'] = ticker
            
            # 캐시 저장
            self.cache[cache_key] = df.copy()
            self.cache_timestamp[cache_key] = datetime.now()
            
            logger.info(f"{ticker} 데이터 수집 완료: {len(df)} rows")
            return df
            
        except Exception as e:
            logger.error(f"{ticker} 데이터 수집 실패: {e}")
            raise
    
    def fetch_multiple(
        self, 
        tickers: List[str],
        period: str = "1y"
    ) -> pd.DataFrame:
        """
        여러 ETF 데이터 동시 수집
        
        Args:
            tickers: ETF 티커 리스트
            period: 기간
        
        Returns:
            Combined DataFrame
        """
        frames = []
        failed = []
        
        for ticker in tickers:
            try:
                df = self.fetch_data(ticker, period=period)
                frames.append(df)
            except Exception as e:
                logger.warning(f"{ticker} 스킵: {e}")
                failed.append(ticker)
        
        if not frames:
            raise ValueError("모든 티커 수집 실패")
        
        combined = pd.concat(frames, ignore_index=True)
        
        if failed:
            logger.warning(f"실패한 티커: {failed}")
        
        return combined
    
    def get_latest_price(self, ticker: str) -> Dict:
        """
        최신 가격 정보 조회
        
        Returns:
            {
                'price': float,
                'change': float,
                'change_percent': float,
                'volume': int,
                'timestamp': str
            }
        """
        try:
            etf = yf.Ticker(ticker)
            info = etf.info
            hist = etf.history(period="2d")
            
            if len(hist) < 2:
                raise ValueError("데이터 부족")
            
            current = hist.iloc[-1]
            previous = hist.iloc[-2]
            
            price = current['Close']
            prev_price = previous['Close']
            change = price - prev_price
            change_pct = (change / prev_price) * 100
            
            return {
                'ticker': ticker,
                'price': round(price, 2),
                'change': round(change, 2),
                'change_percent': round(change_pct, 2),
                'volume': int(current['Volume']),
                'timestamp': current.name.isoformat()
            }
            
        except Exception as e:
            logger.error(f"{ticker} 최신 가격 조회 실패: {e}")
            return None

