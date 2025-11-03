from datetime import datetime
import pandas as pd
from pandas_datareader import data as pdr

SECTOR = [
    "XLK"
]

INDUSTRY = [
    # 반도체/바이오/주택/은행/에너지/리츠/소비/사이버/항공/운송/인프라 등
    "SOXX"
]
TICKERS = sorted(set(SECTOR + INDUSTRY))

def fetch_stooq(ticker, start="2015-01-01", end=None):
    if end is None:
        end = datetime.today().strftime("%Y-%m-%d")
    tried = []
    for t in (ticker, ticker.upper(), ticker.lower(), f"{ticker}.us"):
        try:
            df = pdr.DataReader(t, "stooq", start=start, end=end)
            if df is not None and len(df) > 0:
                df = df.sort_index()  # Stooq는 역순 → 정순 정렬
                df["ticker"] = ticker
                return df
        except Exception as e:
            tried.append((t, str(e)))
    raise RuntimeError(f"[{ticker}] Stooq 조회 실패. 시도: {tried}")

def get_ohlcv_many(tickers, start="2015-01-01", end=None):
    frames = []
    for tk in tickers:
        try:
            frames.append(fetch_stooq(tk, start=start, end=end))
        except Exception as e:
            print(f"WARN: {tk} -> {e}")
    return pd.concat(frames, axis=0).reset_index().rename(columns={"index":"Date"})

# 20일 거래량 MA 및 스파이크 비율(당일/20MA) 계산
def add_volume_features(df):
    df = df.sort_values(["ticker","Date"])
    df["vol_ma20"] = df.groupby("ticker")["Volume"].transform(lambda s: s.rolling(20, min_periods=5).mean())
    df["vol_spike"] = df["Volume"] / df["vol_ma20"]
    return df

# 실행 예시
df = get_ohlcv_many(TICKERS, start="2018-01-01")
df = add_volume_features(df)

# 최근 1개월 각 산업/섹터 대표 ETF의 거래량 스파이크 상위 랭킹
last_month = df[df["Date"] >= (df["Date"].max() - pd.Timedelta(days=30))]
ranked = (last_month.groupby("ticker")
          .agg(last_close=("Close","last"),
               avg_vol=("Volume","mean"),
               avg_vol_ma20=("vol_ma20","mean"),
               max_spike=("vol_spike","max"))
          .sort_values("max_spike", ascending=False))
print(ranked.head(20))
