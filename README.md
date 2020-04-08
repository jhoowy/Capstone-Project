# Capstone Project

This project is based on [YOLOv3](https://github.com/ultralytics/yolov3).

Please check the original YOLOv3 repository for better understanding.

# Inference

`detect.py` runs inference on any sources:

```bash
python3 detect.py --cfg cfg/yolov3-spp.cfg --weights weights/yolov3-spp-ultralytics.pt --source ...
```

- Image:  `--source file.jpg`
- Video:  `--source file.mp4`
- Directory:  `--source dir/`
- Webcam:  `--source 0`
- RTSP stream:  `--source rtsp://170.93.143.139/rtplive/470011e600ef003a004ee33696235daa`
- HTTP stream:  `--source http://wmccpinetop.axiscam.net/mjpg/video.mjpg`

You can download COCO pretrained weights from [https://drive.google.com/open?id=1LezFG5g3BCW6iYaV89B2i64cqEUZD7e0](https://drive.google.com/open?id=1LezFG5g3BCW6iYaV89B2i64cqEUZD7e0)

Pretrained model only works for bottle class for now.

# Docker

**1. You need to change PROJECT_PATH in `run_docker.sh`** first. 

```shell
SERVER=10.0
GPU=0
SHMEMORY=16g
PROJECT_PATH=/YOUR/PROJECT/PATH
```

**2. Build docker**

```bash
./build_docker.sh
```

**3. Run docker**

```bash
./run_docker.sh
```

# TODO

...

# Have Done

...
