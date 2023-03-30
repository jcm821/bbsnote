"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from bbsnote import views
urlpatterns = [
    # 'admin/'문자열과 일치하게 되면 django의 관리자 인터페이스 호출
    path("admin/", admin.site.urls),

    # 'bbsnote/' 문자열과 일치하게 되면 'bbsnote.urls'모듈에 정의된 URL패턴 목록이 포함됨
    path("bbsnote/", include('bbsnote.urls')),
    # 'common/' 문자열과 일치하게 되면 'common.urls'모듈에 정의된 URL패턴 목록이 포함됨
    path("common/", include('common.urls')),
    # 127.0.0.1:8000url로 접속할때 404오류가 뜨는것이 싫을 경우
    # 이 패턴이 빈 문자열과 일치하게 되면 views.index 뷰를 호출
    path('', views.index, name='index'),
]
