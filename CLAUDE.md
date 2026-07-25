# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Reachy Mini(폴른 로보틱스 로봇)용 **Peekaboo(까꿍) 앱**. 로봇이 머리를 숙여 숨었다가 랜덤 타이밍에 좌/우로 갸웃하며 올라오는 타이머 기반 동작 앱이다. Hugging Face Spaces 앱 스토어에 배포된다. 문서·주석은 한국어로 작성한다.

## Structure

- `reachy_mini_peekaboo/` — **배포되는 앱 패키지** (HF Space로 그대로 게시됨; 폴더명 = Space 이름)
  - `reachy_mini_peekaboo/main.py` — 앱 본체. `ReachyMiniApp`을 상속한 `ReachyMiniPeekaboo` 클래스의 `run()` 루프
  - `index.html`, `style.css` — Space 랜딩 페이지. **앱 루트에 반드시 존재해야 check 통과**
  - `README.md` — HF Space 카드. 프론트매터에 `title`, `tags`(`reachy_mini`, `reachy_mini_python_app`) 필수
  - `build/`, `*.egg-info/` — 빌드 산출물 (수정 금지)
- `app/peekaboo/peekaboo_demo.py` — 같은 동작의 학습용 플랫 스크립트 (클래스 없음, 배포 대상 아님)
- `app/peekaboo/DEPLOY_peekaboo.md` — 배포 전 과정 + 트러블슈팅 가이드

## Commands (PowerShell)

프로젝트 가상환경(`.venv`)과 실행 중인 reachy-mini 데몬이 전제다. 한글 소스를 SDK가 cp949로 읽다 깨지므로 **check/publish 전에 반드시 `$env:PYTHONUTF8 = "1"`** 을 설정한다.

```powershell
# editable 설치
pip install -e .\reachy_mini_peekaboo

# 직접 실행 (데몬 필요; 또는 로봇 대시보드 http://localhost:8000 의 Apps 탭)
python -m reachy_mini_peekaboo.main

# 학습용 데모 실행
python .\app\peekaboo\peekaboo_demo.py

# 배포 전 검증 — 구조·메타데이터·entry point 검사 + 임시 venv 설치 테스트
$env:PYTHONUTF8 = "1"
reachy-mini-app-assistant check .\reachy_mini_peekaboo
# → "[OK] App 'reachy_mini_peekaboo' passed all checks!" 가 나와야 통과

# HF Spaces 게시/재배포 (hf auth login 선행)
$env:PYTHONUTF8 = "1"
reachy-mini-app-assistant publish .\reachy_mini_peekaboo "커밋 메시지"
```

테스트 스위트나 린터는 없다. 검증은 `check` 명령과 로봇/시뮬 실행으로 한다.

## Architecture & conventions

- **앱 구조 규칙 (check가 강제함)**: `pyproject.toml`의 `[project.entry-points."reachy_mini_apps"]`가 `reachy_mini_peekaboo.main:ReachyMiniPeekaboo`를 가리켜야 하고, 클래스명은 패키지명의 PascalCase 변환값(`reachy_mini_peekaboo` → `ReachyMiniPeekaboo`)이어야 한다.
- **앱 라이프사이클**: `run(reachy_mini, stop_event)`이 메인 루프. 슬립에는 `time.sleep` 대신 `stop_event.wait()`를 써서 앱 중지 요청에 즉시 반응하게 한다.
- **동작 튜닝**: 자세·각도·타이밍 파라미터는 전부 `main.py` 상단 상수(`PEEK_Z_MM`, `PEEK_YAW_RANGE`, `HIDE_PAUSE_RANGE` 등)로 모아둔다. 동작 변경은 여기서 시작.
- **미디어 백엔드**: 이 앱은 소리/영상을 쓰지 않으므로 `request_media_backend = "no_media"`. PC에서 네트워크로 로봇에 붙을 때 `"default"`를 쓰면 온보드 마이크/카메라 캡처 불가로 멈춘다.
- **숨김 자세**: SDK의 `SLEEP_HEAD_POSE` / `SLEEP_ANTENNAS_JOINT_POSITIONS`(전원 OFF 슬립 자세)를 재사용한다. 까꿍 시 안테나는 일부러 지정하지 않아 움직이지 않게 한다.
- `main.py`(배포용)와 `peekaboo_demo.py`(학습용)는 같은 동작을 구현하므로 동작을 바꿀 때 둘 다 갱신할지 확인한다.

## Gotchas (실제 겪은 것)

- SDK와 로봇 데몬 버전이 다르면 연결은 되지만 로봇이 안 움직인다 → `pip install "reachy-mini==<데몬버전>"`으로 일치시킬 것 (현재 1.8.3)
- 시뮬 데몬은 `--sim --headless`로 실행해야 8000 포트가 열린다
- Windows cp949 콘솔에서 이모지 출력 오류 → 스크립트 상단 `sys.stdout.reconfigure(encoding="utf-8")`
