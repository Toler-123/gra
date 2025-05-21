import multiprocessing
import subprocess
import time
import os
import signal

#  YOLO_CAM.py 실행 함수    사람 탐지 코드드
def run_yolo_cam(shared_flag):
    from yolo_detect import detect
    detect(shared_flag)

#  orb 실행 함수    c파일이라고 가정
def run_orb():
    subprocess.run(["./orb_exec"])

#  YOLO_avoid.py 실행 함수  바운딩 박스 사용하여 장애물 회피 코드
def run_avoid():
    subprocess.run(["python", "YOLO_avoid.py"])

#  start.py 실행 함수 
def run_start():
    subprocess.run(["python", "start.py"])

#  메인 함수 
if __name__ == "__main__":
    # 사람 감지 여부 공유 변수 생성 (True/False)
    person_detected = multiprocessing.Value('b', False)

    # start 먼저 실행 (순차적으로 실행)
    print("[INFO] Initializing start.py...")
    subprocess.run(["python", "start.py"])

    # 이후 나머지 기능 병렬로 실행
    print("[INFO] Launching parallel processes...")
    p1 = multiprocessing.Process(target=run_yolo_cam, args=(person_detected,))
    p2 = multiprocessing.Process(target=run_orb)
    p3 = multiprocessing.Process(target=run_avoid)

    p1.start()
    p2.start()
    p3.start()

    try:
        while True:
            if person_detected.value:
                print("[ALERT] 사람 감지됨! 모든 프로세스 종료 및 back.py 실행")

                # 프로세스 모두 종료
                for p in [p1, p2, p3]:
                    if p.is_alive():
                        p.terminate()
                        p.join()

                # back.py 실행
                subprocess.run(["python", "back.py"])
                break

            time.sleep(0.2)

    except KeyboardInterrupt:
        print("[INFO] 강제 종료 요청됨. 프로세스 종료 중...")
        for p in [p1, p2, p3]:
            if p.is_alive():
                p.terminate()
                p.join()
