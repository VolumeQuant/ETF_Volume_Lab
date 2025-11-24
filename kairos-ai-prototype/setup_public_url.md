# 공개 URL 설정 가이드

로컬 서버를 외부에서 접근 가능하게 만들고 bit.ly로 단축하는 방법입니다.

## 방법 1: ngrok 사용 (추천)

### 1단계: ngrok 설치 및 실행

1. ngrok 다운로드: https://ngrok.com/download
2. ngrok 계정 생성 및 인증 토큰 받기
3. 터미널에서 실행:

```bash
# 서버 실행 (다른 터미널)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# ngrok 실행 (새 터미널)
ngrok http 8000
```

4. ngrok이 제공하는 공개 URL을 복사 (예: `https://xxxx-xx-xx-xx-xx.ngrok-free.app`)

### 2단계: bit.ly로 단축

1. https://bit.ly 접속
2. 로그인 후 "Create" 클릭
3. ngrok URL을 입력하고 원하는 단축 URL 이름 설정
4. 생성된 bit.ly URL 공유

## 방법 2: 자동화 스크립트 (ngrok + bit.ly API)

bit.ly API를 사용하여 자동화하려면:

1. bit.ly API 키 발급: https://dev.bitly.com/
2. 아래 스크립트 사용

