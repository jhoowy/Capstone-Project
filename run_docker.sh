SERVER=10.0
GPU=all
SHMEMORY=16g
PROJECT_PATH=~/Capstone-Project

docker run -e NVIDIA_VISIBLE_DEVICES=$GPU --gpus all --name $SERVER -v $PROJECT_PATH:/home/Capstone-Project --rm --shm-size $SHMEMORY -p 8000:8000 -it capstone/censoring:20.02-py3
