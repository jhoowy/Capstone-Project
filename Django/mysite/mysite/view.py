from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators import csrf
from django.contrib.auth.models import User
from django.contrib import auth
from video.models import Videos

from pathlib import Path

import os
import secrets
import json
import numpy as np
import cv2

vid_formats = ['.mp4', '.avi', '.mpg', '.mpeg', '.wmv']

 
def homepage(request):
    return render(request,'homepage.html')

def upload(request):
    file = request.FILES.get('file') # Got the file, it is binary, it can be operated directly
    formats = Path(file.name).suffix.lower()
    
    if formats not in vid_formats:
        return HttpResponse('Failed to upload : Invalid extension')

    video_id = secrets.token_hex(4)

    with open(os.path.join(settings.MEDIA_ROOT, video_id), 'wb') as f:
        for line in file:
            f.write(line)

    video = Videos(video_id=video_id, file_name=file.name)
    video.save()

    return HttpResponse('succeed. video_id : {}'.format(video_id)) #Here is just get the file from client to server, we can do the operation here.

def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
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

def edit(request, video_id=None):
    if video_id is None:
        return HttpResponse("No Video")
    
    try:
        video_object = get_object_or_404(Videos, pk=video_id)
    except Videos.DoesNotExist:
        return HttpResponse("Video id doesn't exists.")

    video_url = settings.MEDIA_URL + video_id

    if request.POST:
        data = json.loads(request.POST.get('data', ''))
        for i in range(len(data)):
            x = data[i]['box']['x']
            y = data[i]['box']['y']
            w = data[i]['box']['w']
            h = data[i]['box']['h']
            ts = data[i]['time'][0]
            te = data[i]['time'][1]

    return render(request, 'edit.html', {"video_url" : video_url})