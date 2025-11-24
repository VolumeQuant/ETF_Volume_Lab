# ngrok 실행 방법 (Windows)

## 🎯 핵심: ngrok.exe 파일이 있는 위치를 찾아서 실행하면 됩니다!

---

## 방법 1: 파일 탐색기로 찾아서 실행 (가장 쉬움)

### 1단계: ngrok.exe 파일 찾기

1. **파일 탐색기 열기** (Windows 키 + E)
2. **다운로드 폴더로 이동**
   - 보통: `C:\Users\본인계정이름\Downloads`
3. **ngrok 폴더 찾기**
   - 다운로드한 ngrok ZIP 파일을 압축 해제한 폴더
   - 예: `C:\Users\YourName\Downloads\ngrok-v3-stable-windows-amd64`
   - 또는 `C:\Users\YourName\Downloads\ngrok`

4. **ngrok.exe 파일 확인**
   - 폴더 안에 `ngrok.exe` 파일이 있어야 합니다

### 2단계: PowerShell에서 실행

1. **ngrok.exe가 있는 폴더에서 PowerShell 열기**
   - 파일 탐색기에서 ngrok 폴더로 이동
   - 주소창에 `powershell` 입력하고 Enter
   - 또는 폴더 안에서 Shift + 우클릭 → "PowerShell 창 여기서 열기"

2. **명령어 입력**:
   ```
   .\ngrok.exe http 8000
   ```
   또는
   ```
   ngrok.exe http 8000
   ```

---

## 방법 2: 전체 경로로 실행 (경로를 알고 있을 때)

### 예시:

만약 ngrok.exe가 `C:\Users\홍길동\Downloads\ngrok` 폴더에 있다면:

**PowerShell에서:**
```powershell
C:\Users\홍길동\Downloads\ngrok\ngrok.exe http 8000
```

**명령 프롬프트(cmd)에서:**
```cmd
C:\Users\홍길동\Downloads\ngrok\ngrok.exe http 8000
```

---

## 방법 3: ngrok을 시스템 PATH에 추가 (고급)

한 번만 설정하면 어디서든 `ngrok` 명령어로 실행 가능합니다.

### 설정 방법:

1. **ngrok.exe가 있는 폴더 경로 복사**
   - 예: `C:\Users\홍길동\Downloads\ngrok`

2. **시스템 환경 변수 설정**
   - Windows 키 + R → `sysdm.cpl` 입력 → Enter
   - "고급" 탭 → "환경 변수" 클릭
   - "시스템 변수"에서 "Path" 선택 → "편집" 클릭
   - "새로 만들기" 클릭
   - ngrok 폴더 경로 붙여넣기 (예: `C:\Users\홍길동\Downloads\ngrok`)
   - "확인" 클릭

3. **PowerShell 재시작 후 어디서든 실행:**
   ```powershell
   ngrok http 8000
   ```

---

## 📝 실제 예시

### 상황: ngrok.exe가 `C:\Users\김철수\Downloads\ngrok-v3` 폴더에 있음

**방법 1 (파일 탐색기 사용):**
1. 파일 탐색기에서 `C:\Users\김철수\Downloads\ngrok-v3` 폴더 열기
2. 주소창에 `powershell` 입력하고 Enter
3. PowerShell 창에서:
   ```
   .\ngrok.exe http 8000
   ```

**방법 2 (전체 경로 사용):**
1. PowerShell 열기 (어디서든)
2. 다음 명령어 입력:
   ```
   C:\Users\김철수\Downloads\ngrok-v3\ngrok.exe http 8000
   ```

---

## ✅ 실행 확인

ngrok이 정상 실행되면 다음과 같은 화면이 나타납니다:

```
ngrok

Session Status                online
Account                       Your Name (Plan: Free)
Version                       3.x.x
Region                        United States (us)
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://xxxx-xx-xx-xx-xx.ngrok-free.app -> http://localhost:8000

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

**중요**: `Forwarding` 줄의 URL을 복사하세요!

---

## ❓ 여전히 안 되나요?

### 문제 1: "ngrok.exe를 찾을 수 없습니다"
- ngrok.exe 파일이 실제로 있는지 확인
- 파일 경로가 정확한지 확인
- 파일 탐색기에서 직접 더블클릭해서 실행해보기

### 문제 2: "인증 토큰이 필요합니다"
- ngrok 계정 생성 및 인증 토큰 설정 필요
- 다음 명령어로 설정:
  ```
  .\ngrok.exe config add-authtoken YOUR_TOKEN
  ```

### 문제 3: "포트 8000이 이미 사용 중입니다"
- 서버가 이미 실행 중인지 확인
- 다른 포트 사용: `.\ngrok.exe http 8001`

---

## 💡 팁

**가장 쉬운 방법:**
1. 파일 탐색기에서 ngrok.exe가 있는 폴더 열기
2. 주소창에 `powershell` 입력
3. `.\ngrok.exe http 8000` 입력

이렇게 하면 경로를 몰라도 됩니다!

