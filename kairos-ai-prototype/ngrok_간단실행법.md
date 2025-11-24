# ngrok 간단 실행법

## ✅ 네, 명령어를 쳐야 합니다!

ngrok.exe를 실행하려면 PowerShell이나 명령 프롬프트에서 명령어를 입력해야 합니다.

---

## 🚀 가장 쉬운 방법 (3단계)

### 1단계: ngrok.exe가 있는 폴더 열기

1. **파일 탐색기 열기** (Windows 키 + E)
2. **ngrok.exe가 있는 폴더로 이동**
   - 보통: `C:\Users\본인계정\Downloads\ngrok` 또는 `ngrok-v3-stable-windows-amd64` 같은 폴더

### 2단계: PowerShell 열기

**방법 A (추천):**
- 파일 탐색기 주소창에 `powershell` 입력하고 Enter

**방법 B:**
- 폴더 안에서 Shift + 우클릭 → "PowerShell 창 여기서 열기"

### 3단계: 명령어 입력

PowerShell 창에서 다음 명령어 입력:

```
.\ngrok.exe http 8000
```

Enter 키 누르기

---

## ✅ 완료!

이제 ngrok이 실행됩니다. 다음과 같은 화면이 나타나면 성공:

```
ngrok

Session Status                online
Forwarding                    https://xxxx-xx-xx-xx-xx.ngrok-free.app -> http://localhost:8000
```

**중요:** 이 창은 그대로 두세요! (닫지 마세요)

---

## 💡 팁

### 한 번만 설정하면 더 편하게 (선택사항)

ngrok을 시스템 PATH에 추가하면 어디서든 `ngrok http 8000` 명령어로 실행할 수 있습니다.

**설정 방법:**
1. ngrok.exe가 있는 폴더 경로 복사 (예: `C:\Users\홍길동\Downloads\ngrok`)
2. Windows 키 + R → `sysdm.cpl` 입력 → Enter
3. "고급" 탭 → "환경 변수" 클릭
4. "시스템 변수"에서 "Path" 선택 → "편집"
5. "새로 만들기" → ngrok 폴더 경로 붙여넣기
6. "확인" 클릭
7. PowerShell 재시작

**이후에는 어디서든:**
```
ngrok http 8000
```
이렇게만 입력하면 됩니다!

---

## ❓ 자주 묻는 질문

**Q: 매번 이렇게 해야 하나요?**
A: 네, ngrok을 실행할 때마다 명령어를 입력해야 합니다. 하지만 PATH에 추가하면 더 간단해집니다.

**Q: 명령어를 외워야 하나요?**
A: `.\ngrok.exe http 8000` 이 한 줄만 기억하시면 됩니다.

**Q: 다른 포트를 사용하면?**
A: `http 8000` 부분을 바꾸면 됩니다. 예: `.\ngrok.exe http 3000`

