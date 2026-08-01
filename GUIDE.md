# Reachy Mini Peekaboo 시뮬레이션 실행 가이드 🤖🙈

이 가이드는 실물 로봇 없이 **MuJoCo 시뮬레이터** 상에서 Reachy Mini의 **Peekaboo(까꿍) 데모 앱**을 실행하고 테스트하는 전체 과정을 정리한 문서입니다.

---

## 1. 가상환경 준비 및 PowerShell 오류 해결

### 1-1. 가상환경 활성화
```powershell
# 가상환경 활성화
.\.venv\Scripts\Activate.ps1
```

### 1-2. PowerShell 보안 오류 (`PSSecurityException`) 해결
PowerShell 기본 실행 정책으로 인해 `Activate.ps1` 로드가 차단되는 경우, 현재 터미널 세션에 한해 스크립트 실행 권한을 부여합니다.
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\.venv\Scripts\Activate.ps1
```

> **💡 대안**: 가상환경을 활성화하지 않고도 실행 파일 경로를 직접 호출할 수도 있습니다.
> - 데몬 실행: `.\.venv\Scripts\reachy-mini-daemon.exe --sim`
> - 파이썬 실행: `.\.venv\Scripts\python.exe app/peekaboo/peekaboo_demo.py`

---

## 2. 시뮬레이션 데몬 실행 (`reachy-mini-daemon`)

앱에 명령을 전달받아 3D 물리를 연산하고 뷰어를 띄워주는 **데몬 서버**를 먼저 실행해야 합니다. **[터미널 1]**에서 실행합니다.

### 2-1. 기본 실행 (3D MuJoCo 뷰어 창 포함)
```powershell
reachy-mini-daemon --sim
```
- **3D 뷰어 조작법**:
  - 회전: 마우스 좌클릭 + 드래그
  - 이동: 마우스 우클릭 + 드래그
  - 줌: 마우스 스크롤

### 2-2. 헤드리스 (Headless) 모드 (백그라운드 실행 시)
Windows 환경에서 GUI 뷰어 창 생성이 멈추거나 8000 포트 생성이 안 될 경우, 3D 창 없이 웹 대시보드 기반으로 데몬을 띄울 수 있습니다.
```powershell
reachy-mini-daemon --sim --headless
```

### 2-3. 씬(Scene) 추가 옵션
```powershell
reachy-mini-daemon --sim --scene minimal   # 책상 + 소품(사과, 크루아상, 오리 등) 추가
```

### 2-4. 웹 대시보드
데몬이 실행되면 브라우저에서 [http://localhost:8000](http://localhost:8000) 접속을 통해 로봇의 연결 상태, 카메라/오디오 스트림 및 등록된 앱 목록을 확인할 수 있습니다.

---

## 3. Peekaboo 앱 실행 (2가지 방법)

데몬이 작동 중인 상태에서 **[터미널 2]**를 열고 앱을 실행합니다.

### 방법 A. 학습용 플랫 데모 스크립트 실행 (추천 ⭐️)
`app/peekaboo/peekaboo_demo.py` 스크립트는 흐름이 한눈에 보이는 공부·실험용 코드입니다.

1. **`ROBOT_HOST` 설정 확인** ([peekaboo_demo.py](file:///d:/git/oss_reachymini/app/peekaboo/peekaboo_demo.py#L31))
   ```python
   ROBOT_HOST = "localhost"   # 시뮬레이션 연결 시 "localhost"
   ```
2. **스크립트 실행**
   ```powershell
   python app/peekaboo/peekaboo_demo.py
   ```

---

### 방법 B. 배포용 앱 패키지 실행 (`reachy_mini_peekaboo`)
Hugging Face Spaces 앱 스토어 배포 구조를 갖춘 패키지 앱 실행 방법입니다.

1. **패키지 설치 (Editable 모드)**
   ```powershell
   pip install -e .\reachy_mini_peekaboo
   ```
2. **앱 실행**
   ```powershell
   python -m reachy_mini_peekaboo.main
   ```

---

## 4. 자주 묻는 질문 & 트러블슈팅 (FAQ)

### Q1. `python app/peekaboo/peekaboo_demo.py`를 실행했는데 터미널에 텍스트만 나오고 3D 로봇 화면이 안 보입니다.
- **원인**: `peekaboo_demo.py`는 모션 제어 명령만 보내는 **클라이언트**이며, 3D 화면을 그려주는 주체는 **시뮬레이션 데몬(`reachy-mini-daemon`)**입니다.
- **해결법**: 
  1. **터미널 1**에서 `reachy-mini-daemon --sim`을 먼저 실행하여 3D 뷰어 창을 엽니다.
  2. **터미널 2**에서 `python app/peekaboo/peekaboo_demo.py`를 실행하면 터미널 1의 3D 창에서 로봇이 움직이는 모습을 보실 수 있습니다.

### Q2. 스크립트 실행 정책 오류 (`PSSecurityException`)가 발생합니다.
- `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process` 명령을 현재 PowerShell 세션에 입력한 후 활성화 스크립트를 재실행하세요.

### Q3. 시뮬레이션 환경에서 온보드 카메라/마이크는 어떻게 작동하나요?
- Peekaboo 앱은 타이머 기반(`no_media`) 앱이므로 미디어 하드웨어가 없어도 시뮬레이션에서 문제없이 동작합니다.
