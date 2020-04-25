import os
import subprocess
import pytube
import sys

url_link = sys.argv[1]
print(url_link)
yt = pytube.YouTube(url_link)  # 다운받을 동영상 URL 지정

vids = yt.streams.all()

'''
for i in range(len(vids)):
    print(i, '. ', vids[i])
'''

vnum = 0

parent_dir = "C:\\Users\\ja946\\PycharmProjects\\Capstone-Project"
vids[vnum].download(parent_dir)  # 다운로드 수행

print(vids[vnum].default_filename)

new_filename = "output_video.mp4"

default_filename = vids[vnum].default_filename
'''
subprocess.call(['ffmpeg', '-i',  # cmd 명령어 수행
                 os.path.join(parent_dir, default_filename),
                 os.path.join(parent_dir, new_filename)
                 ])

'''

subprocess.call(['python', 'detect.py', '--cfg', 'cfg/yolov3-spp.cfg',
                 '--weights', 'weights/yolov3-spp-ultralytics.pt',
                 '--source', vids[vnum].default_filename
                 ])
