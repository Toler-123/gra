from djitellopy import Tello
import time
import pickle

# 경로 파일 불러오기
with open("route.pkl", "rb") as f:
    route = pickle.load(f)

# 드론 초기화
tello = Tello()
tello.connect()
tello.streamon()

print(f"[BACK] Battery: {tello.get_battery()}%")

# 이륙
tello.takeoff()
time.sleep(2)

# 역순 경로 따라 복귀
print(f"[BACK] 저장된 {len(route)}단계 경로 따라 복귀 중...")
for (x, y, z) in reversed(route):
    print(f"[BACK] 이동 중: x={x}, y={y}, z={z}")
    tello.go_xyz_speed(x, y, z, 30)  # 좌표로 이동 (상대좌표)
    time.sleep(2)  # 이동 대기

# 착륙
tello.land()
tello.streamoff()
tello.end()

print("[BACK] 복귀 완료 및 착륙")
