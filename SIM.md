# 시뮬레이션에서 Peekaboo 실행하기 🖥️

실물 로봇 없이 [MuJoCo](https://mujoco.org) 물리 시뮬레이터에서 앱을 실행·테스트하는 방법.
시뮬 로봇은 USB로 연결된 실물 Reachy Mini Lite와 완전히 동일하게 동작하므로,
코드 수정 없이 그대로 검증할 수 있다.

- 공식 가이드: <https://huggingface.co/docs/reachy_mini/platforms/simulation/get_started>

## 1. 가상환경 + 시뮬레이션용 SDK 설치

시뮬레이터는 MuJoCo 기반이라 `[mujoco]` extra를 붙여 설치한다.

```powershell
cd d:\git\oss_reachymini
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install "reachy-mini[mujoco]"
```

## 2. 시뮬레이션 데몬 실행 (별도 터미널)

```powershell
reachy-mini-daemon --sim
```

MuJoCo 3D 뷰어 창이 뜨고, 데몬이 `localhost:8000`에서 대기한다.
뷰어는 마우스 드래그로 회전, 우클릭 드래그로 이동, 스크롤로 줌.

> ⚠️ **Windows 함정**: `--sim`만 쓰면 MuJoCo 뷰어 창을 띄우려다 막혀서
> **8000 포트가 안 열리는 경우**가 있다. 그럴 땐 뷰어 없이 headless로 실행한다.
>
> ```powershell
> reachy-mini-daemon --sim --headless
> ```
>
> 3D 화면은 없지만 대시보드(<http://localhost:8000>)와 앱 실행은 정상 동작한다.

### 씬 옵션

| 옵션 | 내용 |
| :--- | :--- |
| `--scene empty` (기본) | 로봇만 있는 빈 공간 |
| `--scene minimal` | 책상 + 소품(사과, 크루아상, 오리) 추가 |

```powershell
reachy-mini-daemon --sim --scene minimal
```

## 3. Peekaboo 앱 실행

### 방법 A — 앱 패키지 실행 (권장)

```powershell
pip install -e .\reachy_mini_peekaboo
python -m reachy_mini_peekaboo.main
```

앱은 기본적으로 localhost 데몬에 붙으므로 수정 없이 바로 시뮬 로봇이 까꿍 동작을 한다.
대시보드(<http://localhost:8000>)의 **Apps** 탭에서 실행해도 된다.

### 방법 B — 학습용 데모 스크립트

`app/peekaboo/peekaboo_demo.py` 상단의 `ROBOT_HOST`(무선 로봇 IP)를 `"localhost"`로 바꾼 뒤:

```powershell
python .\app\peekaboo\peekaboo_demo.py
```

## 4. 확인 포인트

- 뷰어(`--sim`)로 실행했다면 3D 창에서 로봇이 머리를 숙여 숨었다가
  좌/우로 갸웃하며 올라오는 동작을 직접 볼 수 있다.
- 시뮬 모드에선 온보드 마이크/카메라 하드웨어가 없지만,
  Peekaboo는 `no_media`(타이머 기반)라 영향이 없다.
  (미디어를 쓰는 앱이라면: 에코 캔슬은 XMOS 하드웨어 대신
  GStreamer 소프트웨어 처리로 시스템 기본 마이크/스피커를 사용한다.)

## 한눈에 보는 명령 요약

```powershell
# 터미널 1 — 시뮬 데몬
.\.venv\Scripts\Activate.ps1
reachy-mini-daemon --sim            # 뷰어 포함 (안 되면 --headless 추가)

# 터미널 2 — 앱 실행
.\.venv\Scripts\Activate.ps1
pip install -e .\reachy_mini_peekaboo
python -m reachy_mini_peekaboo.main
```
