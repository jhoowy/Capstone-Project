from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators import csrf
from django.contrib.auth.models import User
from django.contrib import auth
from video.models import Videos
from mysite.utils.utils import *

from pathlib import Path

import os
import secrets
import json
import numpy as np
import cv2
import mimetypes

vid_formats = ['.mp4', '.avi', '.mpg', '.mpeg', '.wmv']

 
def homepage(request):
    username = request.session.get('username')
    if username is not None:
        label = "<a class='loginlogo' href='/logout'>Logout</a><a class='loginlogo' href='/'>Welcome Back "+username+" !   </a>"
        return render(request,'homepage.html',{"logs":label})
    else:
        label = "<a class='loginlogo' href='/signup'>Sign Up</a><a class='loginlogo' href='/login'>Login</a>"
        return render(request,'homepage.html',{"logs":label})

def upload(request):
    file = request.FILES.get('file') # Got the file, it is binary, it can be operated directly
    formats = Path(file.name).suffix.lower()
    
    if formats not in vid_formats:
        return HttpResponse('Failed to upload : Invalid extension')

    video_id = secrets.token_hex(4)

    with open(os.path.join(settings.MEDIA_ROOT, video_id), 'wb') as f:
        for line in file:
            f.write(line)

    video = Videos(video_id=video_id, file_name=file.name, user=request.user)
    video.save()

    return HttpResponse('succeed. video_id : {}'.format(video_id)) #Here is just get the file from client to server, we can do the operation here.

def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            request.session["username"] = username
            return redirect("homepage")
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def signup(request):
    if request.method == "POST":
        if request.POST["password1"] == request.POST["password2"]:
            user = User.objects.create_user(
                username=request.POST["username"],password=request.POST["password1"])
            auth.login(request, user)
            return redirect("homepage")
        return render(request, "signup.html")
    return render(request, "signup.html")

def edit_download(request, video_id):
    try:
        video_object = get_object_or_404(Videos, pk=video_id)
    except Videos.DoesNotExist:
        return HttpResponse("Video id doesn't exists.")
    
    path = os.path.join(settings.MEDIA_ROOT, video_object.file_name)
    with open(path, 'rb') as f:
        mime_type, _ = mimetypes.guess_type(path)
        response = HttpResponse(f.read(), content_type=mime_type)
        response['Content-Disposition'] = 'attachment; filename=' + video_object.file_name
        return response


def edit(request, video_id=None):
    if video_id is None:
        return HttpResponse("No Video")
    
    try:
        video_object = get_object_or_404(Videos, pk=video_id)
    except Videos.DoesNotExist:
        return HttpResponse("Video id doesn't exists.")

    video_url = settings.MEDIA_URL + video_id

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

        save_path = os.path.join(settings.MEDIA_ROOT, video_object.file_name)
        mosaic_video(os.path.join(settings.MEDIA_ROOT, video_object.video_id), save_path, box_list)
        
        return HttpResponse('')

    return render(request, 'edit.html', {'video_url' : video_url})

def logout(request):
    request.session.flush()
    return redirect("homepage")