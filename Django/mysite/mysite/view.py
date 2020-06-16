from __future__ import absolute_import, unicode_literals
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators import csrf
from django.contrib.auth.models import User
from django.contrib import auth
from video.models import Videos
from mysite.utils.utils import *
from celery import shared_task

from pathlib import Path

import os
import secrets
import json
import numpy as np
import cv2
import mimetypes
import subprocess
import pytube
import sys

vid_formats = ['.mp4', '.avi', '.mov']


def homepage(request):
    username = request.session.get('username')
    if username is not None:
        label = "<a class='loginlogo' href='/search'>Search</a><a class='loginlogo' href='/logout'>Logout</a><a class='loginlogo' href='/'>Welcome Back " + username + " !   </a>"
        return render(request, 'homepage.html', {"logs": label})
    else:
        label = "<a class='loginlogo' href='/search'>Search</a><a class='loginlogo' href='/signup'>Sign Up</a><a class='loginlogo' href='/login'>Login</a>"
        return render(request, 'homepage.html', {"logs": label})


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            request.session["username"] = username
            return redirect(homepage)
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


def upload(request):
    file = request.FILES.get('file')  # Got the file, it is binary, it can be operated directly
    formats = os.path.splitext(file.name)[-1].lower()

    if formats not in vid_formats:
        return HttpResponse('Failed to upload : Invalid extension')

    video_id = secrets.token_hex(4)

    with open(os.path.join(settings.MEDIA_ROOT, video_id + formats), 'wb') as f:
        for line in file:
            f.write(line)

    cap = cv2.VideoCapture(os.path.join(settings.MEDIA_ROOT, video_id + formats))
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()

    video = Videos(video_id=video_id, total_frame=fps, file_name=file.name, user=request.user)
    video.save()

    return HttpResponse('{}'.format(video_id))  # Here is just get the file from client to server, we can do the operation here.

def upload_url(request):
    url = request.POST.get('url')
    yt = pytube.YouTube(url)
            
    # streams = yt.streams.filter(adaptive=True, file_extension='mp4').all()
    # if len(streams) == 0:
    #    streams = yt.streams.all()
    
    streams = yt.streams.all()
    stream = streams[0]

    video_id = secrets.token_hex(4)
    filename = stream.default_filename
    stream.download(settings.MEDIA_ROOT, video_id)

    cap = cv2.VideoCapture(os.path.join(settings.MEDIA_ROOT, video_id + '.mp4'))
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()

    video = Videos(video_id=video_id, total_frame=fps, file_name=filename, user=request.user)
    video.save()

    return HttpResponse('{}'.format(video_id))

def signup(request):
    if request.method == "POST":
        if request.POST["password1"] == request.POST["password2"]:
            user = User.objects.create_user(
                username=request.POST["username"], password=request.POST["password1"])
            auth.login(request, user)
            return redirect("homepage")
        return render(request, "signup.html")
    return render(request, "signup.html")


def process(request, video_id=None):
    username = request.session.get('username')
    if username is not None:
        if video_id is None:
            return HttpResponse("No Video")

        try:
            video_object = get_object_or_404(Videos, pk=video_id)
        except Videos.DoesNotExist:
            return HttpResponse("Video id doesn't exists.")

        video_path = video_object.get_path()
        video_url = settings.MEDIA_URL + video_path

        return render(request, 'process.html', {'video_url': video_url, 'vid': video_id})
    else:
        return render(request, 'login.html')

def process_download(request, video_id=None):
    try:
        video_object = get_object_or_404(Videos, pk=video_id)
    except Videos.DoesNotExist:
        return HttpResponse("Video id doesn't exists.")

    if video_object.processed:
        if video_object.progress_time == video_object.total_frame:
            video_url = settings.MEDIA_URL + 'processed/' + video_id
            return HttpResponse('OK')
        return HttpResponse('')
    else:
        print("PROCESS START")
        video_object.processed = True
        video_object.save()
        process_video(video_object)
        return HttpResponse('')


@shared_task
def process_video(video):
    print("start")
    video_path = os.path.join(settings.MEDIA_ROOT, video.get_path())
    output_path = os.path.join(settings.MEDIA_ROOT, 'processed')

    '''
    TODO
    Update video's progress time
    '''

    video.progress_time = 0
    video.save()

    subprocess.call(['python3', 'YOLOv3/detect.py', '--cfg', 'YOLOv3/cfg/yolov3-spp-3cls-custom.cfg',
                 '--weights', 'YOLOv3/weights/best.pt',
                 '--names', 'YOLOv3/data/inapp_obj.names',
                 '--source', video_path,
                 '--output', output_path
                 ])
    
    video.progress_time = video.total_frame
    video.save()


def edit_download(request, video_id):
    try:
        video_object = get_object_or_404(Videos, pk=video_id)
    except Videos.DoesNotExist:
        return HttpResponse("Video id doesn't exists.")
    
    path = os.path.join(settings.MEDIA_ROOT, 'edited', video_object.get_path())
    with open(path, 'rb') as f:
        mime_type, _ = mimetypes.guess_type(path)
        response = HttpResponse(f.read(), content_type=mime_type)
        response['Content-Disposition'] = 'attachment; filename=' + video_object.file_name
        return response


def edit(request, video_id=None):
    username = request.session.get('username')
    if username is not None:
        if video_id is None:
            return HttpResponse("No Video")

        try:
            video_object = get_object_or_404(Videos, pk=video_id)
        except Videos.DoesNotExist:
            return HttpResponse("Video id doesn't exists.")
        
        v_path = video_object.get_path()

        if video_object.processed:
            video_url = settings.MEDIA_URL + 'processed/' + v_path
            video_path = os.path.join(settings.MEDIA_ROOT, 'processed', v_path)
        else:
            video_url = settings.MEDIA_URL + v_path
            video_path = os.path.join(settings.MEDIA_ROOT, v_path)   
        save_path = os.path.join(settings.MEDIA_ROOT, 'edited', v_path)

        # If client send blurring request
        if request.POST:
            data = json.loads(request.POST.get('data', ''))
            box_list = []
            for i in range(len(data)):
                x = int(data[i]['box']['x'])
                y = int(data[i]['box']['y'])
                w = int(data[i]['box']['w'])
                h = int(data[i]['box']['h'])
                ts = 1000 * float(data[i]['time'][0])
                te = 1000 * float(data[i]['time'][1])
                box_list.append([x, y, w, h, ts, te])

            mosaic_video(video_path, save_path, box_list)

            return HttpResponse('')

        return render(request, 'edit.html', {'video_url': video_url})
    else:
        return render(request, 'login.html')


def logout(request):
    request.session.flush()
    return render(request, 'homepage.html')


def search(request):
    username = request.session.get('username')
    if username is not None:
        return render(request, 'search.html')
    else:
        return render(request, 'login.html')

def search_download(request, vidId):  
    yt = pytube.YouTube("https://www.youtube.com/watch?v=" + vidId)  # 다운받을 동영상 URL 지정
            
    vids = yt.streams.all()

    '''
    for i in range(len(vids)):
        print(i, '. ', vids[i])
    '''
    vnum = 0

    parent_dir = "../media/"
    vids[vnum].download(parent_dir)  # 다운로드 수행

    print(vids[vnum].default_filename)
    default_filename = vids[vnum].default_filename

    new_filename = "output_video.mp4"

    subprocess.call(['python', 'detect.py', '--cfg', 'cfg/yolov3-spp.cfg',
                    '--weights', 'weights/yolov3-spp-ultralytics.pt',
                    '--source', default_filename
                    ])

    # subprocess.call(["rm", url_link, "best", "-o", "output_stream.mp4"], timeout = 10)
    return HttpResponse('')

def mypage(request):
    username = request.session.get('username')
    user = request.user
    video_list = Videos.objects.filter(user=user)
    print(video_list)

    if username is not None:
        return render(request, 'mypage.html', {'video_list' : video_list})
    else:
        return render(request, 'login.html')