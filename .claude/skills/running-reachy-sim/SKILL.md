---
name: running-reachy-sim
description: Use when setting up or running the Reachy Mini MuJoCo simulation in this repo on Windows — fresh clone with no .venv, "reachy-mini-daemon not found", ModuleNotFoundError reachy_mini, or verifying the Peekaboo app without a physical robot.
---

# Reachy Mini 시뮬레이션 실행 (Windows)

## Overview

실물 로봇 없이 MuJoCo 시뮬 데몬을 띄우고 Peekaboo 앱 동작을 검증하는 절차.
2026-07 실제 실행으로 검증됨 (Python 3.11, reachy-mini 1.9.0).
시뮬은 데몬과 SDK가 같은 설치본이라 버전 불일치 문제가 없다.

## Setup (최초 1회)

```powershell
cd d:\git\oss_reachymini
$env:PYTHONUTF8 = "1"                                             # 한글 소스 cp949 깨짐 방지 (모든 pip/실행 전에)
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install "reachy-mini[mujoco]"   # MuJoCo extra 필수
.\.venv\Scripts\python.exe -m pip install -e .\reachy_mini_peekaboo
```

## Run

터미널 1 — 데몬 (백그라운드 실행 권장):

```powershell
$env:PYTHONUTF8 = "1"
.\.venv\Scripts\reachy-mini-daemon.exe --sim          # MuJoCo 뷰어 포함
# 뷰어가 막혀 8000 포트가 안 열리면: --sim --headless
# 책상+소품 씬: --scene minimal
```

터미널 2 — 앱:

```powershell
$env:PYTHONUTF8 = "1"
.\.venv\Scripts\python.exe -m reachy_mini_peekaboo.main
```

## Verify

기동 확인은 로그 + HTTP 둘 다 본다:

| 확인 | 방법 | 기대 결과 |
| :--- | :--- | :--- |
| 데몬 기동 | 데몬 로그 | `Daemon started successfully.` + `Uvicorn running on http://127.0.0.1:8000` |
| 대시보드 | `Invoke-WebRequest http://127.0.0.1:8000/` | HTTP 200 |
| 로봇 상태 | `Invoke-WebRequest http://127.0.0.1:8000/api/state/full` | head_pose/antennas JSON |
| 앱 동작 | `/api/state/full`을 몇 초 간격 2회 비교 | 숨기(z≈-43mm, 안테나 ±3.05rad) ↔ 까꿍(z>0, yaw≠0) 자세가 번갈아 나타남 |

앱은 stdout에 로그가 안 보여도 정상일 수 있다 — 판정은 반드시 API 상태 비교로 한다.

## Common Mistakes

| 증상 | 원인/해결 |
| :--- | :--- |
| `/api/daemon/status` 폴링이 계속 실패 | 그 엔드포인트는 없음(404). `/` 또는 `/api/state/full`로 확인 |
| 데몬 로그에 `[Central Relay] Authentication failed` 반복 | 클라우드 릴레이 연결 시도 — 로컬 시뮬에선 무해, 무시 |
| `No Reachy Mini Audio ... card found` 경고 | 시뮬엔 오디오 하드웨어가 없어 정상. Peekaboo는 `no_media`라 무관 |
| 8000 포트가 안 열림 | MuJoCo 뷰어 창이 막힌 것 → `--sim --headless`로 재실행 |
| `pip install -e` 또는 check 중 `UnicodeDecodeError: cp949` | `$env:PYTHONUTF8 = "1"` 먼저 설정 |
| `app/peekaboo/peekaboo_demo.py`가 안 붙음 | 상단 `ROBOT_HOST`(무선 로봇 IP)를 `"localhost"`로 변경 후 `.\.venv\Scripts\python.exe .\app\peekaboo\peekaboo_demo.py` (포트 설정 불필요) |

## 정리(종료)

데몬/앱은 각각 별도 프로세스 — 앱만 Ctrl+C로 끊어도 데몬은 살아 있다.
포트 점유 확인: `Get-NetTCPConnection -LocalPort 8000`
