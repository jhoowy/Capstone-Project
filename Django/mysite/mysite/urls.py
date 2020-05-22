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
from django.urls import path
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

urlpatterns = [
    path('',view.homepage, name="homepage"),
    path('upload',view.upload),
    path('login',view.login, name="login"),
    path('signup',view.signup, name="signup"),
    url(r'^edit/download/(?P<video_id>\w+)/$', view.edit_download, name='edit'),
    url(r'^edit/(?P<video_id>\w+)/$', view.edit, name='edit'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
