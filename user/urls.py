"""puyuan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    # ========== 註冊&登入 ==========
    # 1.註冊OK => OK
    path('register/', views.register),
    # 2.登入OK => OK
    path('auth/', views.auth),
    # x.登出OK
    path('logout/', views.logout),
    # 3.發送驗證碼OK => OK
    path('verification/send/', views.send),
    # 4.檢查驗證碼OK
    path('verification/check/', views.check),
    # 5.忘記密碼OK
    path('password/forgot/', views.forgot),
    # 6.重設密碼OK
    path('password/reset/', views.reset),
    # 38.註冊確認OK => OK
    path('register/check/', views.register_check),
    # ========== 其他 ==========
    # 36.親友團通知OK
    path("notification/", views.notification),
    # 29.最新消息
    path('news/', views.news),
    # 23.分享
    path('share/', views.share),
    # 24.查看分享（含自己分享出去的）
    path('share/<int:relation_type>/', views.share_check)
]
