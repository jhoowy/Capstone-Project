import math
import os
import shutil
import subprocess
import cv2
from pathlib import Path

class VideoLoader:
    def __init__(self, path):
        self.ms = 0
        self.cap = cv2.VideoCapture(path)
        self.nframes = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

    def __iter__(self):
        self.count = 0
        return self

    def __next__(self):
        if self.count == self.nframes:
            if self.cap != None:
                self.cap.release()
            raise StopIteration

        ret_val, img = self.cap.read()
        self.count += 1
        self.ms = self.cap.get(cv2.CAP_PROP_POS_MSEC)

        return img, self.ms, self.cap

    def __len__(self):
        return self.nframes


def mosaic_video(path, save_path, box_list, fourcc='mp4v'):
    ms = 0
    video = VideoLoader(path)
    fps = video.cap.get(cv2.CAP_PROP_FPS)
    w = int(video.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(video.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    vid_writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*fourcc), fps, (w, h))

    for img, ms, cap in video:
        for box in box_list:
            x, y, w, h, ts, te = box
            if ms >= ts and ms <= te:
                mosaic_one_box(x, y, w, h, img)

        vid_writer.write(img)
    
    vid_writer.release()
    add_audio(path, save_path)

def mosaic_one_box(x, y, w, h, img, mosaic_rate=30):
    # Mosaic result box
    box = img[y:y+h, x:x+w]
    box = cv2.resize(box, (max(1, w//mosaic_rate), max(1, h//mosaic_rate)))
    box = cv2.resize(box, (w, h), interpolation=cv2.INTER_AREA)
    img[y:y+h, x:x+w] = box

def add_audio(source, out):
    # Add audio from source videos to output files
    temp_folder = "temp"
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

    temp_path = str(Path(temp_folder) / Path(source).name)
    os.rename(out, temp_path)

    p = subprocess.Popen(['ffmpeg', '-y', '-i', source, '-i', temp_path, '-c:v', 'libx264', '-c:a', 'copy', '-map', '1:v:0', '-map', '0:a:0', out], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p_out, err = p.communicate()
    exitcode = p.returncode
    if exitcode != 0:
        print(exitcode, p_out.decode('utf8'), err.decode('utf8'))

    shutil.rmtree(temp_folder)