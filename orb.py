import cv2
import os
import subprocess

# === 설정 ===
video_path = '/home/cvip/Desktop/gwanyong_work/gra/video.mp4'  # 영상 파일명
output_dir = 'frames'  # 프레임 저장 폴더
orbslam_path = '/home/cvip/Desktop/gwanyong_work/gra/ORB_SLAM3'  # ORB-SLAM3 루트 폴더
vocab_path = os.path.join(orbslam_path, 'Vocabulary', 'ORBvoc.txt')
mono_exec = os.path.join(orbslam_path, 'Examples', 'Monocular', 'mono_tum')
yaml_path = 'mono.yaml'

print("[1] Extracting frames...")
os.makedirs(output_dir, exist_ok=True)
cap = cv2.VideoCapture(video_path)

# 자동으로 FPS 추출
fps = cap.get(cv2.CAP_PROP_FPS)
if fps == 0:
    raise ValueError("⚠️ FPS 정보를 가져오지 못했습니다. video_path가 잘못되었거나 손상된 영상일 수 있습니다.")
print(f"🎞 FPS: {fps:.2f}")

frame_id = 0
timestamp_path = os.path.join(output_dir, 'timestamp.txt')
with open(timestamp_path, 'w') as ts_file:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        filename = os.path.join(output_dir, f'frame_{frame_id:04d}.png')
        cv2.imwrite(filename, frame)

        timestamp = frame_id / fps
        ts_file.write(f"{timestamp:.6f} frame_{frame_id:04d}.png\n")
        frame_id += 1

cap.release()
print(f"✅ {frame_id} frames saved to '{output_dir}'")
print(f"✅ timestamp.txt created at '{timestamp_path}'")

# === ORB-SLAM3 실행 ===
print("[2] Running ORB-SLAM3... (Pangolin 창이 뜹니다)")
cmd = [mono_exec, vocab_path, yaml_path, output_dir]
subprocess.run(cmd)
