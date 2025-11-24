# 🌐 공개 URL 설정 가이드 (Windows)

로컬 서버를 외부에서 접속할 수 있게 만드는 방법입니다.

## 📋 준비물
1. ngrok (무료)
2. bit.ly 계정 (무료)

---

## 1단계: ngrok 설치

### 방법 A: 직접 다운로드 (추천)

1. **ngrok 다운로드**
   - https://ngrok.com/download 접속
   - "Download for Windows" 클릭
   - ZIP 파일 다운로드 및 압축 해제

2. **ngrok 계정 생성**
   - https://dashboard.ngrok.com/signup 에서 무료 계정 생성
   - 이메일 인증 완료

3. **인증 토큰 받기**
   - https://dashboard.ngrok.com/get-started/your-authtoken 접속
   - 표시된 토큰 복사 (예: `2abc123def456ghi789jkl012mno345pq`)

4. **ngrok 인증**
   - PowerShell 또는 명령 프롬프트 열기
   - ngrok.exe가 있는 폴더로 이동
   - 다음 명령 실행:
     ```powershell
     .\ngrok.exe config add-authtoken YOUR_TOKEN_HERE
     ```
   - YOUR_TOKEN_HERE를 복사한 토큰으로 교체

### 방법 B: Chocolatey 사용 (선택사항)

```powershell
choco install ngrok
```

---

## 2단계: 서버 실행

### 터미널 1: FastAPI 서버 실행

프로젝트 폴더에서:

```powershell
# 가상환경 활성화 (있는 경우)
.\venv\Scripts\Activate.ps1

# 서버 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

서버가 실행되면 다음과 같은 메시지가 표시됩니다:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**이 터미널은 그대로 두세요!**

---

## 3단계: ngrok 실행

### 터미널 2: ngrok 실행

**가장 쉬운 방법 (추천):**

1. **파일 탐색기 열기**
2. **ngrok.exe가 있는 폴더로 이동**
   - 보통: `C:\Users\본인계정이름\Downloads\ngrok` 또는 `ngrok-v3-stable-windows-amd64` 같은 폴더
3. **주소창에 `powershell` 입력하고 Enter**
4. **PowerShell 창에서 다음 명령어 입력:**
   ```
   .\ngrok.exe http 8000
   ```

**또는 전체 경로로 실행:**

```powershell
# 예시 (실제 경로로 변경하세요)
C:\Users\홍길동\Downloads\ngrok\ngrok.exe http 8000
```

**더 자세한 설명**: `ngrok_실행방법.md` 파일 참고

### ngrok 화면 확인

ngrok이 실행되면 다음과 같은 화면이 표시됩니다:

```
ngrok

Session Status                online
Account                       Your Name (Plan: Free)
Version                       3.x.x
Region                        United States (us)
Latency                       -
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://xxxx-xx-xx-xx-xx.ngrok-free.app -> http://localhost:8000

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

**중요**: `Forwarding` 줄의 `https://xxxx-xx-xx-xx-xx.ngrok-free.app` 부분을 복사하세요!

이것이 공개 URL입니다.

---

## 4단계: 공개 URL 테스트

브라우저에서 복사한 ngrok URL로 접속해보세요:
- 예: `https://xxxx-xx-xx-xx-xx.ngrok-free.app`

정상적으로 접속되면 성공입니다! ✅

---

## 5단계: bit.ly로 단축

1. **bit.ly 접속**
   - https://bit.ly 접속
   - 로그인 (없으면 무료 회원가입)

2. **URL 단축**
   - 우측 상단 "Create" 또는 "Shorten" 버튼 클릭
   - "Paste your link here"에 ngrok URL 붙여넣기
     - 예: `https://xxxx-xx-xx-xx-xx.ngrok-free.app`
   - "Custom back-half"에 원하는 이름 입력 (선택사항)
     - 예: `kairos-ai` → `bit.ly/kairos-ai`
   - "Create" 클릭

3. **단축 URL 확인**
   - 생성된 단축 URL 복사
   - 예: `bit.ly/kairos-ai`

---

## ✅ 완료!

이제 `bit.ly/kairos-ai` 같은 URL을 어디서든 공유할 수 있습니다!

---

## ⚠️ 주의사항

1. **ngrok 무료 버전 제한**
   - 세션이 종료되면 URL이 변경됩니다
   - 매번 새로운 URL을 받아야 합니다
   - 고정 URL이 필요하면 ngrok 유료 플랜 사용

2. **서버 실행 중 유지**
   - ngrok과 서버가 모두 실행 중이어야 접속 가능
   - 하나라도 종료하면 접속 불가

3. **방화벽 설정**
   - Windows 방화벽에서 포트 8000 허용 필요할 수 있음
   - 문제가 있으면 방화벽 설정 확인

---

## 🔧 문제 해결

### ngrok이 실행되지 않을 때
- ngrok 인증 토큰이 제대로 설정되었는지 확인
- `ngrok config check` 명령으로 확인

### 외부에서 접속이 안 될 때
- ngrok이 정상 실행 중인지 확인
- ngrok 화면에서 "Forwarding" URL 확인
- 서버가 8000 포트에서 실행 중인지 확인

### bit.ly 단축이 안 될 때
- ngrok URL이 정상 작동하는지 먼저 확인
- bit.ly에서 URL 형식 확인 (https://로 시작해야 함)

---

## 📞 추가 도움

문제가 계속되면:
1. ngrok 로그 확인 (http://127.0.0.1:4040)
2. 서버 로그 확인 (터미널 1)
3. 에러 메시지 캡처하여 확인

