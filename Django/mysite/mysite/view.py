from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators import csrf
from django.contrib.auth.models import User
from django.contrib import auth


def homepage(request):
    return render(request, 'homepage.html')


def upload(request):
    file = request.FILES.get('file')  # Got the file, it is binary, it can be operated directly
    with open(file.name, 'wb') as f:
        for line in file:
            f.write(line)
    return HttpResponse('succed')  # Here is just get the file from client to server, we can do the operation here.


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
