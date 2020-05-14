from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators import csrf
 
def homepage(request):
    return render(request,'homepage.html')

def upload(request):
    file = request.FILES.get('file')# Got the file, it is binary, it can be operated directly
    with open(file.name,'wb') as f:
        for line in file:
            f.write(line)
    return HttpResponse('succed')#Here is just get the file from client to server, we can do the operation here.

def login(request):
    return render(request,'login.html')
