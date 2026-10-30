# macOS 로컬 세팅 가이드 — 가상환경 + 시뮬레이터 실행

이 문서는 **macOS(Apple Silicon)** 에서 실물 로봇 없이 MuJoCo 시뮬레이터로
Reachy Mini 앱을 실행하기 위한 로컬 환경 세팅 절차를 정리한 것이다.
(Windows PowerShell 기준 절차는 `GUIDE.md` 참고)

---

## 0. 전제 조건

- Python **3.11 이상** (3.12 권장 — 3.14는 일부 의존성 wheel 미지원 가능성 있음)
- 이 저장소 루트(`oss_reachymini/`)에서 작업

pyenv를 쓰는 경우 설치된 버전 확인:

```bash
pyenv versions          # 예: 3.12.11
```

## 1. 가상환경 생성 (최초 1회)

저장소 루트에서:

```bash
# pyenv의 3.12로 .venv 생성
~/.pyenv/versions/3.12.11/bin/python -m venv .venv

# (pyenv를 안 쓰면) python3 -m venv .venv
```

## 2. 가상환경 활성화

```bash
source .venv/bin/activate
```

- 프롬프트 앞에 `(.venv)` 가 붙으면 성공.
- 비활성화는 `deactivate`.
- 활성화하지 않고 `.venv/bin/python`, `.venv/bin/reachy-mini-daemon` 처럼
  실행 파일을 직접 호출해도 된다.

## 3. SDK 설치 (최초 1회)

```bash
pip install "reachy-mini[mujoco]"
```

- `[mujoco]` extra가 시뮬레이터 의존성(MuJoCo 등)을 함께 설치한다.
- 설치 확인:

```bash
pip show reachy-mini    # Version: 1.12.0 (예시)
```

> **참고**: 실물 로봇과 연결할 때는 SDK 버전을 로봇 데몬 버전과 맞춰야 한다
> (`pip install "reachy-mini==<데몬버전>"`). 시뮬 전용이면 최신 버전으로 충분하다.

## 4. 시뮬레이션 데몬 실행 — [터미널 1]

```bash
source .venv/bin/activate
reachy-mini-daemon --sim --no-media
```

> **⚠️ macOS에서는 `--no-media`가 사실상 필수.** 이 옵션 없이 실행하면
> GStreamer 미디어 초기화 단계에서 데몬이 행이 걸려 포트 8000이 영영 안 열린다
> (로그가 `Daemon version: ...` 한 줄에서 멈춤). 시뮬 학습에는 카메라/오디오가
> 필요 없으므로 항상 붙이고 시작하자.

- 3D MuJoCo 뷰어 창이 함께 뜬다.
  - 회전: 좌클릭+드래그 / 이동: 우클릭+드래그 / 줌: 스크롤
- 뷰어 없이 돌리려면 (백그라운드 실행·원격 터미널):

```bash
reachy-mini-daemon --sim --headless --no-media
```

- 책상·소품이 있는 씬:

```bash
reachy-mini-daemon --sim --scene minimal --no-media
```

데몬이 다 뜨면 웹 대시보드가 열린다 → **http://localhost:8000**
(로그에 `Uvicorn running on http://127.0.0.1:8000` 이 보이면 준비 완료)

## 5. 연결 확인 (첫 번째 프로그램) — [터미널 2]

```bash
source .venv/bin/activate
python - <<'EOF'
from reachy_mini import ReachyMini

with ReachyMini(media_backend="no_media") as mini:
    print("Reachy Mini 연결 성공!")
EOF
```

## 6. Peekaboo 데모 실행 — [터미널 2]

데몬([터미널 1])이 떠 있는 상태에서:

```bash
source .venv/bin/activate
python app/peekaboo/peekaboo_demo.py
```

- 로봇이 고개를 숙여 숨었다가 랜덤 타이밍에 좌/우로 갸웃하며 올라오면 성공 🙈👀
- 종료: `Ctrl+C`

## 7. 종료 순서

1. [터미널 2] 앱을 `Ctrl+C`로 종료
2. [터미널 1] 데몬을 `Ctrl+C`로 종료

---

## 트러블슈팅

| 증상 | 원인/해결 |
| --- | --- |
| `reachy-mini-daemon: command not found` | 가상환경 미활성화 → `source .venv/bin/activate` 또는 `.venv/bin/reachy-mini-daemon` 직접 호출 |
| 포트 8000이 안 열리고 로그가 `Daemon version:`에서 멈춤 | GStreamer 미디어 초기화 행 (macOS에서 실제 발생) → 데몬 죽이고 `--no-media` 붙여 재실행 |
| 앱이 연결 후 멈춤 | `media_backend="no_media"` 인지 확인 (네트워크 연결 시 `"default"`는 멈춤) |
| 설치 중 wheel 빌드 실패 | Python 3.14 등 너무 새 버전 → 3.12로 venv 재생성 |
| 주소 이미 사용 중 (port in use) | 이전 데몬이 살아 있음 → `pkill -f reachy-mini-daemon` 후 재실행 |
