from datetime import datetime

def run_dummy_pipeline() -> dict:
    return {
        "asof": datetime.utcnow().isoformat() + "Z",
        "etl_version": "0.0.1",
        "universe": ["XLK", "XLF", "XLE", "XLY"],
        "signals": {
            "XLK": {"vol_spike": 2.1, "obv_trend": "up", "phase": "recovery"},
            "XLF": {"vol_spike": 1.3, "obv_trend": "flat", "phase": "transition"},
            "XLE": {"vol_spike": 0.9, "obv_trend": "down", "phase": "late-cycle"},
            "XLY": {"vol_spike": 1.7, "obv_trend": "up", "phase": "recovery"},
        },
        "note": "이건 데모용 임의 데이터입니다."
    }
