"""Peekaboo(피카부) 앱 본체.

동작 시나리오
-------------
1. 시작하면 머리를 완전히 숙여 "숨은"(전원 OFF 같은 슬립) 자세를 취한다.
2. 잠시(랜덤) 기다린 뒤 "까꿍!" 하고 고개를 든다.
3. 올라올 때마다 매번 랜덤하게 왼쪽/오른쪽으로 고개를 갸웃하는 귀여운 동작을 한다.
4. 잠깐 쳐다본 뒤 다시 숨는다. (1~4 반복)

※ 소리 감지는 사용하지 않는다(타이머 기반). 안테나(귀)는 올라올 때 움직이지 않는다.
"""

import random
import threading
import time

from reachy_mini import ReachyMini, ReachyMiniApp
from reachy_mini.reachy_mini import (
    SLEEP_ANTENNAS_JOINT_POSITIONS,  # 전원 OFF 때 안테나를 완전히 접는 위치
    SLEEP_HEAD_POSE,                 # 전원 OFF 때 머리를 완전히 숙여 숨기는 자세
)
from reachy_mini.utils import create_head_pose

# ---------------------------------------------------------------------------
# 동작 파라미터 (필요하면 값만 바꿔서 튜닝)
# ---------------------------------------------------------------------------
# 숨김 자세: 로봇이 꺼질 때(슬립)처럼 머리를 완전히 숙이고 안테나를 접는다.
HIDDEN_POSE = SLEEP_HEAD_POSE
ANTENNAS_HIDDEN = SLEEP_ANTENNAS_JOINT_POSITIONS  # 안테나 완전히 접음 (≈±175°)

# 까꿍(올라오기) 동작
PEEK_Z_MM = 18           # 머리를 들어 올리는 높이(mm)
PEEK_PITCH_DEG = 10      # 살짝 위를 보는 각도
PEEK_YAW_RANGE = (15, 30)   # 좌/우로 고개 돌리는 각도 범위(도) — 매번 랜덤
PEEK_ROLL_RANGE = (5, 12)   # 같은 방향으로 살짝 갸웃하는 각도 범위(도)

# 타이밍
HIDE_PAUSE_RANGE = (1.5, 3.5)  # 숨어서 기다리는 시간(초) — 랜덤
PEEK_DURATION = 0.6      # 까꿍! 올라오는 시간(초)
PEEK_HOLD_SEC = 1.2      # 올라와서 쳐다보며 머무는 시간
HIDE_DURATION = 1.0      # 다시 숨는 시간


class ReachyMiniPeekaboo(ReachyMiniApp):
    """숨었다가 랜덤하게 좌/우로 갸웃하며 올라오는 까꿍 앱."""

    request_media_backend = "no_media"  # 소리/영상 안 씀

    def run(self, reachy_mini: ReachyMini, stop_event: threading.Event) -> None:
        """앱 메인 루프."""
        # 1) 초기화 — 모터를 켜고 중립으로 천천히 이동한 뒤 잠시 안정화
        reachy_mini.enable_motors()
        stop_event.wait(1.5)
        reachy_mini.goto_target(
            create_head_pose(), antennas=[0.0, 0.0], body_yaw=0.0, duration=2.5
        )
        stop_event.wait(1.0)

        self.logger.info("피카부 시작! 🙈")
        while not stop_event.is_set():
            # 2-1) 숨기 (머리 완전히 숙이고 안테나도 접음)
            reachy_mini.goto_target(
                HIDDEN_POSE, antennas=ANTENNAS_HIDDEN, body_yaw=0.0, duration=HIDE_DURATION
            )
            self.logger.info("숨기 🙈")
            stop_event.wait(random.uniform(*HIDE_PAUSE_RANGE))  # 언제 나올지 모르게 랜덤 대기
            if stop_event.is_set():
                break

            # 2-2) 까꿍! — 이번엔 어느 쪽으로 나올지 랜덤으로 정한다.
            side = random.choice([-1, +1])                 # 왼쪽(-1) / 오른쪽(+1)
            yaw = side * random.uniform(*PEEK_YAW_RANGE)   # 그 방향으로 고개 돌리기
            roll = side * random.uniform(*PEEK_ROLL_RANGE)  # 같은 방향으로 살짝 갸웃
            peek_pose = create_head_pose(
                z=PEEK_Z_MM, pitch=PEEK_PITCH_DEG, yaw=yaw, roll=roll,
                mm=True, degrees=True,
            )
            # 안테나(귀)는 일부러 지정하지 않는다 → 올라올 때 귀는 움직이지 않는다.
            reachy_mini.goto_target(
                peek_pose, body_yaw=0.0, duration=PEEK_DURATION, method="ease_in_out"
            )
            self.logger.info(f"까꿍! 👀 ({'오른쪽' if side > 0 else '왼쪽'})")
            stop_event.wait(PEEK_HOLD_SEC)


if __name__ == "__main__":
    app = ReachyMiniPeekaboo()
    try:
        app.wrapped_run()
    except KeyboardInterrupt:
        app.stop()
