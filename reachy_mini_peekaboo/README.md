---
title: Peekaboo
emoji: 🙈
colorFrom: red
colorTo: blue
sdk: static
pinned: false
short_description: Reachy Mini hides, then peeks up to a random side.
tags:
 - reachy_mini
 - reachy_mini_python_app
---

# Peekaboo 🙈 (피카부)

까꿍 놀이 앱입니다. Reachy Mini가 고개를 완전히 숙여 **숨었다가**, 잠시 뒤
**"까꿍!" 하고 고개를 들어** 매번 **랜덤하게 왼쪽/오른쪽으로 갸웃**하며 올라옵니다.

## 동작

1. **숨기** — 전원 OFF 때와 같은 슬립 자세로 머리를 완전히 숙이고 안테나를 접습니다.
2. **랜덤 대기** — 언제 나올지 모르게 잠깐(랜덤) 숨어 있습니다.
3. **까꿍!** — 고개를 들어 올립니다. 이번엔 어느 쪽으로 나올지 매번 랜덤으로 정해
   왼쪽 또는 오른쪽으로 고개를 갸웃합니다. (안테나/귀는 움직이지 않습니다.)
4. **다시 숨기** — 잠깐 쳐다본 뒤 다시 숨습니다. (반복)

> 소리 감지는 사용하지 않는 타이머 기반 동작이라, 마이크 없이도 어디서나 잘 동작합니다.

## 실행 방법

데몬이 실행 중인 상태에서:

```bash
# 앱 설치 (editable)
pip install -e .

# 직접 실행
python -m reachy_mini_peekaboo.main
```

또는 로봇 대시보드(<http://localhost:8000>)의 **Apps** 탭에서 실행할 수 있습니다.

## 튜닝

동작 감도/자세 등은 `reachy_mini_peekaboo/main.py` 상단의 파라미터로 조절합니다.

| 파라미터 | 설명 |
| :--- | :--- |
| `PEEK_Z_MM` / `PEEK_PITCH_DEG` | 올라올 때 머리 높이와 위를 보는 각도 |
| `PEEK_YAW_RANGE` / `PEEK_ROLL_RANGE` | 좌/우로 갸웃하는 각도 범위(랜덤) |
| `HIDE_PAUSE_RANGE` | 숨어서 기다리는 시간 범위(랜덤) |
| `PEEK_DURATION` / `PEEK_HOLD_SEC` / `HIDE_DURATION` | 올라오기/머무르기/숨기 속도 |

## License

Apache-2.0
