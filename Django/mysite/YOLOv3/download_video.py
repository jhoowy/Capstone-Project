import subprocess
import pytube
import sys

url_link = sys.argv[1]
video_format = sys.argv[2]
if len(sys.argv) == 4:
    timeout_factor = sys.argv[3]

if video_format == "video":
    yt = pytube.YouTube(url_link)  # 다운받을 동영상 URL 지정

    vids = yt.streams.all()

    '''
    for i in range(len(vids)):
        print(i, '. ', vids[i])
    '''

    vnum = 0

    parent_dir = "C:\\Users\\jason\\PycharmProjects\\github\\Capstone-Project"
    vids[vnum].download(parent_dir)  # 다운로드 수행

    print(vids[vnum].default_filename)
    default_filename = vids[vnum].default_filename
elif video_format == "stream":
    try:
        subprocess.call(["streamlink", url_link, "best", "-o", "output_stream.mp4"], timeout = float(timeout_factor))
    except subprocess.TimeoutExpired:
        print("timeout! stop download and start mosaic")

    default_filename = "output_stream.mp4"

new_filename = "output_video.mp4"

subprocess.call(['python', 'detect.py', '--cfg', 'cfg/yolov3-spp.cfg',
                 '--weights', 'weights/yolov3-spp-ultralytics.pt',
                 '--source', default_filename
                 ])

subprocess.call(["rm", url_link, "best", "-o", "output_stream.mp4"], timeout = 10)