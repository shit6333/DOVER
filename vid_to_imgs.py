import cv2
import os
import argparse

def extract_frames(video_path: str, output_folder: str, target_fps: float):

    # 建立輸出資料夾
    os.makedirs(output_folder, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"Can't open the video file：{video_path}")

    orig_fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = max(int(round(orig_fps / target_fps)), 1)

    frame_idx = 0
    save_idx = 0 

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_idx % frame_interval == 0:
            filename = os.path.join(output_folder, f"frame_{save_idx:06d}.png")
            cv2.imwrite(filename, frame)
            save_idx += 1

        frame_idx += 1

    cap.release()
    print(f"Finish => {output_folder}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=" "
    )
    parser.add_argument("video", help="video path")
    parser.add_argument("out_folder", help="output folder")
    parser.add_argument(
        "--fps", type=float, default=1.0,
        help="FPS)"
    )
    args = parser.parse_args()

    extract_frames(args.video, args.out_folder, args.fps)


# python extract_frames.py path/to/video.mp4 path/to/output_folder --fps 2.5
