"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import view
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

urlpatterns = [
    path('',view.homepage, name="homepage"),
    path('upload',view.upload),
    path('upload_url', view.upload_url),
    path('login',view.login, name="login"),
    path('signup',view.signup, name="signup"),
    path('logout',view.logout),
    path('search',view.search),
    path('mypage', view.mypage, name='mypage'),
    url(r'^process/(?P<video_id>\w+)/$', view.process, name='process'),
    url(r'^process/download/(?P<video_id>\w+)/$', view.process_download, name='edit'),
    url(r'^edit/download/(?P<video_id>\w+)/$', view.edit_download, name='edit'),
    url(r'^edit/(?P<video_id>\w+)/$', view.edit, name='edit'),
    url(r'^search/download/(?P<video_id>\w+)/$', view.search_download, name='search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
