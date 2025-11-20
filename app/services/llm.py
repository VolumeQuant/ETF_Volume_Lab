import os, json, httpx

PROVIDER = os.getenv("PROVIDER", "").lower()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

SYSTEM_PROMPT = (
    "ETF 거래량 분석가. 데이터를 보고 3문장으로 요약: "
    "1) 주목할 ETF와 거래량 스파이크 비율, "
    "2) 가격 반응(상승/하락), "
    "3) 투자 시사점."
)

def _rule_based_explain(user_content: str) -> str:
    try:
        data = json.loads(user_content)
    except Exception:
        return f"입력 데이터를 해석했습니다:\n{user_content[:200]}..."

    lines = []
    
    # 빠른 스캔 모드 처리
    if data.get("mode") == "quick_scan":
        scan_data = data.get("data", [])
        timestamp = data.get("timestamp", "")
        
        lines.append(f"📊 빠른 스캔 분석 (기준: {timestamp[:19] if timestamp else '알 수 없음'})")
        lines.append(f"모니터링 ETF 수: {len(scan_data)}개\n")
        
        # 거래량 스파이크 기준 정렬
        sorted_data = sorted(scan_data, key=lambda x: x.get("volume_spike_ratio", 0) or 0, reverse=True)
        
        high_spikes = [d for d in sorted_data if (d.get("volume_spike_ratio") or 0) >= 1.5]
        
        if high_spikes:
            lines.append("⚡ 주목할 ETF (거래량 스파이크 1.5x 이상):")
            for item in high_spikes[:5]:
                ticker = item.get("ticker", "?")
                name = item.get("name", "")
                spike = item.get("volume_spike_ratio", 0)
                price_chg = item.get("price_change_pct", 0)
                lines.append(f"  • {ticker} ({name}): 거래량 {spike:.2f}x, 가격 {price_chg:+.2f}%")
            
            lines.append(f"\n💡 결론: {high_spikes[0].get('ticker')} 등에서 거래량 급증 감지. 단기 모멘텀 주목 필요.")
        else:
            lines.append("💡 현재 뚜렷한 거래량 이상징후 없음. 관망 권장.")
        
        return "\n".join(lines)
    
    # 전체 분석 모드 처리
    metadata = data.get("metadata", {})
    summary = data.get("summary", {})
    top_spikes = data.get("top_spikes", [])
    
    lines.append(f"📊 전체 분석 (기간: {metadata.get('date_range', {}).get('start', '?')} ~ {metadata.get('date_range', {}).get('end', '?')})")
    lines.append(f"분석 ETF 수: {metadata.get('tickers_analyzed', 0)}개\n")
    
    # 이벤트 요약
    total_events = summary.get("total_events", 0)
    by_level = summary.get("by_level", {})
    
    if total_events > 0:
        lines.append(f"🔍 감지된 거래량 이벤트: {total_events}개")
        if by_level:
            level_str = ", ".join([f"{level}: {count}개" for level, count in by_level.items()])
            lines.append(f"  분류: {level_str}\n")
        
        # 최대 스파이크 ETF
        if top_spikes:
            lines.append("🔥 최대 거래량 스파이크 TOP 5:")
            for spike in top_spikes[:5]:
                ticker = spike.get("Ticker", "?")
                date = spike.get("Date", "")
                spike_ratio = spike.get("Volume_Spike_Ratio", 0)
                price_chg = spike.get("Price_Change_Pct", 0)
                lines.append(f"  • {ticker} ({date}): {spike_ratio:.2f}x 스파이크, 가격 {price_chg:+.2f}%")
            
            # 최근 이벤트 분석
            latest_events = summary.get("latest_events", [])
            if latest_events:
                recent_tickers = list(set([e.get("Ticker") for e in latest_events[:5]]))
                lines.append(f"\n💡 결론: 최근 {', '.join(recent_tickers[:3])} 등에서 거래량 이상징후 감지.")
                lines.append("   포지션 진입 시 2~3일 추세 지속 여부 확인 권장.")
            else:
                lines.append(f"\n💡 결론: {top_spikes[0].get('Ticker')} 등의 과거 스파이크 확인됨. 현재는 관망 모드 권장.")
        else:
            lines.append("\n💡 결론: 분석 기간 내 뚜렷한 거래량 이상징후 없음. 정상 범위 내 거래.")
    else:
        lines.append("🔍 감지된 거래량 이벤트 없음")
        lines.append("\n💡 결론: 분석 기간 내 특이사항 없음. 정상적인 거래량 수준 유지.")
    
    return "\n".join(lines)

async def _explain_with_groq(user_content: str) -> str:
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY 없음")
    if not user_content or not user_content.strip():
        raise RuntimeError("입력 데이터가 비었습니다")

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_content}
    ]
    payload = {
        "model": GROQ_MODEL,
        "messages": messages,
        "temperature": 0.4,
        "max_tokens": 200,  # 토큰 절약
    }
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(url, headers=headers, json=payload)
        # 400일 때 서버가 주는 에러 본문을 그대로 노출해 원인 파악
        if r.status_code >= 400:
            try:
                err = r.json()
            except Exception:
                err = {"error_text": r.text}
            raise RuntimeError(f"Groq API {r.status_code}: {err}")
        data = r.json()
        return data["choices"][0]["message"]["content"]

async def explain(user_content: str) -> str:
    if PROVIDER == "groq":
        try:
            return await _explain_with_groq(user_content)
        except Exception as e:
            return _rule_based_explain(user_content) + f"\n\n[참고] Groq 폴백: {e}"
    return _rule_based_explain(user_content)
