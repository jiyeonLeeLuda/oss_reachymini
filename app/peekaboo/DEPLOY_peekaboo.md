# Reachy Mini Peekaboo 앱 — 배포 가이드 📦

피카부(까꿍) 앱을 **Hugging Face Spaces 앱 스토어**에 처음 배포하는 전 과정을 정리한 문서다.
실제로 검증하며 겪은 함정과 해결법까지 포함한다.

- 앱 동작: 머리를 완전히 숙여 **숨었다가**, 잠시 뒤 **"까꿍!"** 하고 고개를 들어 **매번 랜덤하게 좌/우로 갸웃**한다. (소리 감지 없음 · 타이머 기반 · 안테나는 올라올 때 안 움직임)
- 공식 문서: <https://huggingface.co/docs/reachy_mini/index>
- 앱 제작·배포 블로그: <https://huggingface.co/blog/pollen-robotics/make-and-publish-your-reachy-mini-apps>

---

## 1. 생성된 파일

### 1-1. 배포되는 앱 패키지 — `reachy_mini_peekaboo/`

HF Space로 **그대로 게시되는** 폴더다. 폴더명(`reachy_mini_peekaboo`)이 곧 Space 이름이 된다.

```
reachy_mini_peekaboo/
├── pyproject.toml         # 패키지 정의 + 의존성 + entry point
├── README.md              # HF Space 카드(메타데이터: title·tags) + 앱 설명
├── index.html             # Space 랜딩 페이지(정적 HTML)
├── style.css              # 랜딩 페이지 스타일
├── .gitignore             # build/, *.egg-info/, __pycache__ 등 제외
└── reachy_mini_peekaboo/  # 실제 파이썬 패키지(=module)
    ├── __init__.py        # ReachyMiniPeekaboo 클래스 노출
    └── main.py            # 앱 본체 (ReachyMiniApp 상속, run() 구현)
```

| 파일 | 역할 | 검증(check)이 요구하는 핵심 |
| :--- | :--- | :--- |
| `pyproject.toml` | 패키지/entry point 정의 | `[project.entry-points."reachy_mini_apps"]`에 `reachy_mini_peekaboo = "reachy_mini_peekaboo.main:ReachyMiniPeekaboo"` |
| `README.md` | HF Space 카드 | 프론트매터에 `title`, `tags`(= `reachy_mini` + `reachy_mini_python_app`) |
| `index.html` | Space 랜딩 페이지 | 앱 **루트에 반드시 존재** |
| `style.css` | 랜딩 스타일 | 앱 **루트에 반드시 존재** |
| `reachy_mini_peekaboo/main.py` | 앱 로직 | `class ReachyMiniPeekaboo(ReachyMiniApp)` 포함 |
| `reachy_mini_peekaboo/__init__.py` | 패키지 초기화 | `from .main import ReachyMiniPeekaboo` |

> ⚠️ **명명 규칙**: 클래스명은 패키지명을 PascalCase로 바꾼 값이어야 한다.
> `reachy_mini_peekaboo` → `ReachyMiniPeekaboo`. (검증이 이 이름을 강제한다.)

### 1-2. 학습용 스크립트 — `peekaboo_demo.py` (배포 대상 아님)

같은 동작을 **클래스/함수 없이** 흐름이 한눈에 보이게 쓴 학습용 단일 스크립트.
공부·실험용이며 HF에는 올리지 않는다. 실행: `python peekaboo_demo.py`

---

## 2. 사전 준비물

| 도구 | 확인 명령 | 비고 |
| :--- | :--- | :--- |
| reachy-mini SDK | `python -c "import reachy_mini"` | **로봇 데몬과 같은 버전**(현재 1.8.3) |
| `hf` CLI | `hf version` | huggingface_hub 설치 시 포함 |
| git | `git --version` | |
| git-lfs | `git lfs version` | 모델/대용량 파일용 |
| HF 계정 | — | 토큰(Write) 발급 필요 |

---

## 3. 단계별 배포 절차

### Step 0 — 앱 동작 확인 (선택)

배포 전 로봇/시뮬에서 한 번 돌려본다.

```powershell
# 로컬에 editable 설치
.\.venv\Scripts\python.exe -m pip install -e .\reachy_mini_peekaboo

# 직접 실행 (데몬이 떠 있어야 함)
.\.venv\Scripts\python.exe -m reachy_mini_peekaboo.main
```

### Step 1 — 검증 (`check`)

구조·메타데이터·entry point를 검사하고, 임시 가상환경에 설치 테스트까지 한다. (외부 영향 없음, 몇 분 소요)

```powershell
$env:PYTHONUTF8 = "1"
.\.venv\Scripts\reachy-mini-app-assistant.exe check .\reachy_mini_peekaboo
```

➡️ 마지막에 **`[OK] App 'reachy_mini_peekaboo' passed all checks!`** 가 나오면 통과.

### Step 2 — Hugging Face 계정 & 토큰

1. 계정 생성(없으면): <https://huggingface.co/join>
2. **Write 권한 토큰** 발급: <https://huggingface.co/settings/tokens>
   - **New token** → Type **Write** → 이름 입력 → **Create**
   - `hf_xxxxxxxx...` 토큰 복사 (한 번만 보임)

### Step 3 — 로그인

```powershell
cd D:\projects\reachy_mini_project
.\.venv\Scripts\Activate.ps1
hf auth login --token hf_여기에_복사한_토큰
hf auth whoami        # 사용자명이 나오면 성공
```

### Step 4 — 게시 (`publish`)

```powershell
$env:PYTHONUTF8 = "1"
reachy-mini-app-assistant publish .\reachy_mini_peekaboo "Initial Peekaboo app"
```

진행 중 질문:
- **public / private** → 앱 스토어에 공유하려면 **public**
- 이후 자동으로 `git init` → 커밋 → HF Space로 push

➡️ 게시 위치: `https://huggingface.co/spaces/<사용자명>/reachy_mini_peekaboo`

### Step 5 — 확인 & 설치

- 로봇 대시보드(`http://192.168.0.144:8000`)의 **App store** 탭에서 검색 → 원클릭 설치
- 또는 위 Space 주소를 브라우저로 확인

---

## 4. 업데이트(재배포) 방법

코드를 고친 뒤 같은 명령으로 다시 게시하면, 기존 Space에 변경분만 커밋·푸시된다.

```powershell
$env:PYTHONUTF8 = "1"
reachy-mini-app-assistant publish .\reachy_mini_peekaboo "Update: 동작 개선"
```

---

## 5. 트러블슈팅 (실제로 겪은 것들)

| 증상 | 원인 | 해결 |
| :--- | :--- | :--- |
| `check`/`publish` 중 `UnicodeDecodeError: cp949 ... 0xed` | SDK가 한글(UTF-8) `main.py`를 cp949로 읽음 | 명령 전에 `$env:PYTHONUTF8 = "1"` |
| `[ERROR] index.html is missing` / `style.css is missing` | 앱 루트에 정적 파일 없음 | 루트에 `index.html`, `style.css` 추가 |
| `main.py is missing the class ...` | 클래스명이 규칙과 다름 | 클래스명 = 패키지명 PascalCase (`ReachyMiniPeekaboo`) |
| 로봇이 연결은 되는데 **안 움직임** | SDK ↔ 데몬 버전 불일치 | `pip install "reachy-mini==<데몬버전>"`로 일치 |
| PC에서 `media_backend="default"`로 멈춤 | 원격에선 온보드 마이크/카메라 캡처 불가 | `media_backend="no_media"` 사용 |
| 시뮬 데몬이 8000 포트를 안 엶 | `--sim`이 MuJoCo 뷰어 창을 띄우려다 막힘 | `--sim --headless`로 실행 |
| Windows 콘솔에서 이모지 출력 오류 | cp949 콘솔 | 스크립트 상단 `sys.stdout.reconfigure(encoding="utf-8")` |

---

## 6. 한눈에 보는 명령 요약

```powershell
# 0) (선택) 로컬 실행
.\.venv\Scripts\python.exe -m reachy_mini_peekaboo.main

# 1) 검증
$env:PYTHONUTF8 = "1"
.\.venv\Scripts\reachy-mini-app-assistant.exe check .\reachy_mini_peekaboo

# 2~3) 토큰 발급(웹) 후 로그인
hf auth login --token hf_xxxxxxxx
hf auth whoami

# 4) 게시
$env:PYTHONUTF8 = "1"
reachy-mini-app-assistant publish .\reachy_mini_peekaboo "Initial Peekaboo app"
```
