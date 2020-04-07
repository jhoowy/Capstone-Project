SERVER=10.0
GPU=0
SHMEMORY=16g
PROJECT_PATH=/mnt/hdd1/Shared/Capstone-Project

nvidia-docker run -e NVIDIA_VISIBLE_DEVICES=$GPU --name $SERVER -v $PROJECT_PATH:/home/Capstone-Project --rm --shm-size $SHMEMORY -it capstone/censoring:20.02-py3
