from djitellopy import Tello
import time
import pickle

# 드론 초기화 및 연결
tello = Tello()
tello.connect()
tello.streamon()

print(f"[START] Battery: {tello.get_battery()}%")

# 이륙
tello.takeoff()
time.sleep(2)

# 약간 전진
tello.send_rc_control(0, 30, 0, 0)  # 전진 속도 30
time.sleep(1)

# 정지
tello.send_rc_control(0, 0, 0, 0)

# 이동 경로 기록 (예: 전진 한 번만 기록)
route = [(0, 30, 0)]  # (x, y, z) 형식의 상대 이동 좌표

# 경로 파일로 저장
with open("route.pkl", "wb") as f:
    pickle.dump(route, f)

print("[START] 이동 경로 저장 완료")

# 스트리밍 종료
tello.streamoff()
tello.end()
