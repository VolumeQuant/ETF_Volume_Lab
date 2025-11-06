import os, json, httpx

PROVIDER = os.getenv("PROVIDER", "").lower()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-8b-8192")

SYSTEM_PROMPT = (
    "너는 ETF 기반 투자 전략 설명가야. 주어진 JSON 말뭉치를 읽고, "
    "핵심 시그널(거래량 스파이크, OBV 추세, 매크로 국면)을 3~5문장으로 간결하게 요약하되, "
    "왜 지금 특정 ETF가 유리/불리한지 데이터로 근거를 제시해줘."
)

def _rule_based_explain(user_content: str) -> str:
    try:
        data = json.loads(user_content)
    except Exception:
        return f"입력 데이터를 해석했습니다:\n{user_content}"

    sig = data.get("signals", {}); asof = data.get("asof", "")
    pos, neg, neutral = [], [], []
    for etf, s in sig.items():
        vol = s.get("vol_spike", 0); obv = str(s.get("obv_trend","")).lower()
        phase = s.get("phase",""); score = 0
        if vol >= 2.0: score += 2
        elif vol >= 1.5: score += 1
        if obv == "up": score += 1
        elif obv == "down": score -= 1
        item = (etf, vol, obv, phase, score)
        (pos if score>=2 else neg if score<=-1 else neutral).append(item)

    def fmt(items):
        return "\n".join([f"- {e[0]}: vol_spike {e[1]:.1f}, OBV {e[2]}, 국면 {e[3]}" for e in items]) or "- 없음"

    lines = []
    if asof: lines.append(f"[기준 시각] {asof}")
    lines += ["요약:"]
    if pos: lines += ["① 매수 유리 후보:", fmt(sorted(pos, key=lambda x: x[4], reverse=True))]
    if neutral: lines += ["② 관찰 대상:", fmt(neutral)]
    if neg: lines += ["③ 비선호:", fmt(sorted(neg, key=lambda x: x[4]))]
    if pos:
        tops = ", ".join([e[0] for e in sorted(pos, key=lambda x: x[4], reverse=True)[:2]])
        lines.append(f"\n결론: {tops} 위주 분할 진입이 유리합니다. 2~3거래일 추세 지속 확인 권장.")
    else:
        lines.append("\n결론: 뚜렷한 유입 우위 없음. 관망 또는 소액 탐색 진입 권장.")
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
        {"role": "user", "content": f"[DATA]\n{user_content}\n\n[요약]:"}
    ]
    payload = {
        "model": GROQ_MODEL,                 # 예: "llama3-8b-8192"
        "messages": messages,
        "temperature": 0.4,
        "max_tokens": 350,
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
