import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
import random
from ultralytics import YOLO
import cv2
import os
import subprocess
from djitellopy import tello

# 공유 플래그를 받아서 사람 감지 시 True로 바꾸는 함수
def detect(shared_flag):
    model = YOLO("./pretrained/yolov8s.pt")

    # Tello 드론 초기화
    drone = tello.Tello()
    drone.connect()
    drone.streamon()  # 비디오 스트리밍 시작
    print(f"Battery: {drone.get_battery()}%")

    try:
        while True:
            frame = drone.get_frame_read().frame
            results = model(frame)  # 전체 객체 감지
            annotated_frame = results[0].plot()

            # 화면에 출력
            cv2.imshow("Tello YOLOv8 Detection", annotated_frame)

            # 감지된 클래스 ID들 확인
            cls_ids = results[0].boxes.cls.cpu().numpy() if results[0].boxes is not None else []

            # 사람 클래스 (0번) 감지되었는지 확인
            if 0 in cls_ids:
                print("[YOLO_CAM] 사람 감지됨! 복귀 플래그 설정")
                shared_flag.value = True
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        drone.streamoff()
        drone.end()
        cv2.destroyAllWindows()
