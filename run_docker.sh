SERVER=10.0
GPU=0
SHMEMORY=16g
PROJECT_PATH=~/workspace/git/Capstone-Project

nvidia-docker run -e NVIDIA_VISIBLE_DEVICES=$GPU --name $SERVER -v $PROJECT_PATH:/home/Capstone-Project --rm --shm-size $SHMEMORY -p 8000:8000 -it capstone/censoring:20.02-py3
