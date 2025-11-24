"""
로컬 서버를 공개 URL로 노출하고 bit.ly로 단축하는 스크립트
"""
import subprocess
import time
import requests
import json
import sys
import os

# 설정
NGROK_PORT = 8000
BITLY_ACCESS_TOKEN = os.getenv("BITLY_ACCESS_TOKEN")  # 환경 변수에서 가져오기
BITLY_GROUP_GUID = os.getenv("BITLY_GROUP_GUID")  # 선택사항

def start_uvicorn():
    """uvicorn 서버 시작"""
    print("🚀 uvicorn 서버 시작 중...")
    return subprocess.Popen(
        ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", str(NGROK_PORT)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

def get_ngrok_url():
    """ngrok API를 통해 공개 URL 가져오기"""
    print("🔍 ngrok 공개 URL 확인 중...")
    time.sleep(3)  # ngrok이 시작될 시간 대기
    
    try:
        response = requests.get("http://127.0.0.1:4040/api/tunnels", timeout=5)
        if response.status_code == 200:
            data = response.json()
            tunnels = data.get("tunnels", [])
            if tunnels:
                public_url = tunnels[0].get("public_url")
                if public_url:
                    return public_url.replace("http://", "https://")  # https로 변환
    except Exception as e:
        print(f"⚠️  ngrok URL 확인 실패: {e}")
        print("💡 ngrok이 실행 중인지 확인하세요: ngrok http 8000")
    
    return None

def shorten_with_bitly(long_url, custom_back_half=None):
    """bit.ly API를 사용하여 URL 단축"""
    if not BITLY_ACCESS_TOKEN:
        print("⚠️  BITLY_ACCESS_TOKEN 환경 변수가 설정되지 않았습니다.")
        print("💡 bit.ly API 토큰을 발급받아 환경 변수로 설정하세요.")
        return None
    
    url = "https://api-ssl.bitly.com/v4/shorten"
    headers = {
        "Authorization": f"Bearer {BITLY_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "long_url": long_url
    }
    
    if custom_back_half:
        payload["custom_bitlinks"] = [custom_back_half]
    
    if BITLY_GROUP_GUID:
        payload["group_guid"] = BITLY_GROUP_GUID
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        if response.status_code == 201:
            data = response.json()
            return data.get("link")
        else:
            print(f"⚠️  bit.ly API 오류: {response.status_code}")
            print(f"응답: {response.text}")
    except Exception as e:
        print(f"⚠️  bit.ly API 호출 실패: {e}")
    
    return None

def main():
    print("=" * 50)
    print("🌐 KAIROS AI 프로토타입 공개 URL 설정")
    print("=" * 50)
    
    # uvicorn 서버 시작
    uvicorn_process = start_uvicorn()
    time.sleep(2)
    
    # ngrok URL 가져오기
    ngrok_url = get_ngrok_url()
    
    if not ngrok_url:
        print("\n❌ ngrok URL을 가져올 수 없습니다.")
        print("\n📝 수동 설정 방법:")
        print("1. 새 터미널에서 실행: ngrok http 8000")
        print("2. ngrok이 제공하는 URL을 복사")
        print("3. https://bit.ly 에서 수동으로 단축 URL 생성")
        uvicorn_process.terminate()
        sys.exit(1)
    
    print(f"\n✅ ngrok 공개 URL: {ngrok_url}")
    
    # bit.ly로 단축
    if BITLY_ACCESS_TOKEN:
        print("\n🔗 bit.ly로 단축 중...")
        short_url = shorten_with_bitly(ngrok_url)
        if short_url:
            print(f"✅ 단축 URL: {short_url}")
        else:
            print("⚠️  bit.ly 단축 실패. ngrok URL을 직접 사용하세요.")
    else:
        print("\n💡 bit.ly 자동 단축을 사용하려면:")
        print("   export BITLY_ACCESS_TOKEN='your_token_here'")
        print("   그런 다음 https://bit.ly 에서 수동으로 단축하세요.")
    
    print("\n" + "=" * 50)
    print("📌 서버 실행 중...")
    print(f"📍 공개 URL: {ngrok_url}")
    print("🛑 종료하려면 Ctrl+C를 누르세요")
    print("=" * 50)
    
    try:
        uvicorn_process.wait()
    except KeyboardInterrupt:
        print("\n\n🛑 서버 종료 중...")
        uvicorn_process.terminate()
        print("✅ 종료 완료")

if __name__ == "__main__":
    main()

