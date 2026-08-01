"""피카부(Peekaboo) 데모 — 학습용 플랫 버전.

평소엔 고개를 완전히 숙여 숨어 있다가, 잠시 뒤 "까꿍!" 하고 고개를 든다.
올라올 때마다 매번 랜덤하게 왼쪽/오른쪽으로 고개를 갸웃하는 귀여운 동작을 한다.
( 소리 감지는 사용하지 않는다. 안테나(귀)는 올라올 때 움직이지 않는다. )

실행: python peekaboo_demo.py
"""

import random
import sys
import time

from reachy_mini import ReachyMini
from reachy_mini.reachy_mini import (
    SLEEP_ANTENNAS_JOINT_POSITIONS,  # 로봇이 꺼질 때 안테나를 완전히 접는 위치
    SLEEP_HEAD_POSE,                 # 로봇이 꺼질 때 머리를 완전히 숙여 숨기는 자세
)
from reachy_mini.utils import create_head_pose

# Windows 한글 콘솔(cp949)에서도 이모지를 출력할 수 있게 UTF-8로 맞춘다.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# ─────────────────────────────────────────────────────────────────────────
# 설정값 (여기 숫자만 바꾸면 동작이 달라진다)
# ─────────────────────────────────────────────────────────────────────────
# ROBOT_HOST = "192.168.0.144"   # 무선 로봇 IP. (로봇 위에서 직접 실행하면 무시됨)
ROBOT_HOST = "localhost"   # 무선 로봇 IP (시뮬레이션시 "localhost")
# 소리 감지를 쓰지 않으므로 미디어(마이크/카메라)도 필요 없다 → "no_media".
# (덕분에 PC에서 네트워크로 붙어도 멈추지 않고 잘 돈다.)
MEDIA_BACKEND = "no_media"

# 숨김 자세: "로봇이 꺼질 때 머리가 완전히 숨는" 슬립 자세를 그대로 쓴다.
HIDDEN_POSE     = SLEEP_HEAD_POSE                 # 머리를 완전히 숙여 숨음
ANTENNAS_HIDDEN = SLEEP_ANTENNAS_JOINT_POSITIONS  # 안테나(귀)도 완전히 접음 (≈±175°)

# 까꿍(올라오기) 동작 파라미터
PEEK_Z_MM       = 18      # 머리를 들어 올리는 높이(mm)
PEEK_PITCH_DEG  = 10      # 살짝 위를 보는 각도
PEEK_YAW_RANGE  = (15, 30)  # 좌/우로 고개 돌리는 각도 범위(도) — 매번 이 안에서 랜덤
PEEK_ROLL_RANGE = (5, 12)   # 같은 방향으로 살짝 갸웃하는 각도 범위(도)

HIDE_PAUSE_RANGE = (1.5, 3.5)  # 숨어서 기다리는 시간(초) — 랜덤이라 언제 나올지 모른다
PEEK_DURATION    = 5   # 까꿍! 올라오는 시간(초)
PEEK_HOLD_SEC    = 1.2   # 올라와서 쳐다보며 머무는 시간
HIDE_DURATION    = 2.0   # 다시 숨는 시간


# ─────────────────────────────────────────────────────────────────────────
# 여기서부터가 실제 동작 흐름이다.
# ─────────────────────────────────────────────────────────────────────────
with ReachyMini(host=ROBOT_HOST, connection_mode="auto", media_backend=MEDIA_BACKEND) as mini:

    # 1) 초기화 — 모터를 켜고 중립 자세로 천천히 이동한 뒤 충분히 기다린다.
    print("[1] 초기화: 모터 켜고 중립으로...")
    mini.enable_motors()
    time.sleep(2.0)                                              # 토크가 걸릴 시간을 충분히 준다
    mini.goto_target(create_head_pose(), antennas=[0.0, 0.0],
                     body_yaw=0.0, duration=3.0)                 # 중립으로 천천히
    time.sleep(2.0)                                              # 자세가 안정될 때까지 대기

    # 2) 까꿍 반복 — 숨었다가 랜덤하게 좌/우로 고개를 갸웃하며 올라온다.
    print("[2] 까꿍 시작! 🙈  (Ctrl+C로 종료)")
    try:
        while True:
            # 2-1) 숨기 (머리 완전히 숙이고 안테나도 접음)
            mini.goto_target(HIDDEN_POSE, antennas=ANTENNAS_HIDDEN,
                             body_yaw=0.0, duration=HIDE_DURATION)
            print("  숨기 🙈")
            time.sleep(random.uniform(*HIDE_PAUSE_RANGE))       # 언제 나올지 모르게 랜덤 대기

            # 2-2) 까꿍! — 이번엔 어느 쪽으로 나올지 랜덤으로 정한다.
            side = random.choice([-1, +1])                      # 왼쪽(-1) / 오른쪽(+1)
            yaw = side * random.uniform(*PEEK_YAW_RANGE)        # 그 방향으로 고개 돌리기
            roll = side * random.uniform(*PEEK_ROLL_RANGE)      # 같은 방향으로 살짝 갸웃 (귀여움 포인트)
            peek_pose = create_head_pose(
                z=PEEK_Z_MM, pitch=PEEK_PITCH_DEG, yaw=yaw, roll=roll,
                mm=True, degrees=True,
            )
            # 안테나(귀)는 일부러 지정하지 않는다 → 올라올 때 귀는 움직이지 않는다.
            mini.goto_target(peek_pose, body_yaw=0.0,
                             duration=PEEK_DURATION, method="ease_in_out")
            print(f"  까꿍! 👀 ({'오른쪽' if side > 0 else '왼쪽'}으로 갸웃)")
            time.sleep(PEEK_HOLD_SEC)                           # 잠깐 쳐다보며 머문다
    except KeyboardInterrupt:
        print("\n종료합니다. 안녕! 👋")
