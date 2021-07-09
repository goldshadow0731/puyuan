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
    # ========== 控糖團好友 ==========
    # 16.獲取控糖團邀請碼OK
    path("code/", views.code),
    # 17.控糖團列表OK
    path("list/", views.list),
    # 18.獲取控糖團邀請OK
    path("requests/", views.requests),
    # 19.送出控糖團邀請OK
    path("send/", views.send),
    # 20.接受控糖團邀請OK
    path("<int:friend_invite_id>/accept/", views.accept),
    # 21.拒絕控糖團邀請OK
    path("<int:friend_invite_id>/refuse/", views.refuse),
    # 22.刪除控糖團邀請OK
    path("<int:friend_id>/remove/", views.remove),
    # 37.刪除更多好友OK
    path("remove/", views.remove),
    # 26.控糖團結果OK
    path("results/", views.results),
]
