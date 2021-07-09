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
    # ========== 個人資訊設定 ==========
    # 7.個人資訊設定OK
    # 12.個人資訊OK
    path('', views.user),
    # 11.個人預設值OK
    path('default/', views.default_value),
    # 35.個人設定OK
    path('setting/', views.setting),
    # ========== 測量上傳 ==========
    # 8.上傳血壓測量結果OK
    path("blood/pressure/", views.blood_pressure),
    # 9.上傳體重測量結果OK
    path("weight/", views.weight),
    # 10.上傳血糖OK
    path("blood/sugar/", views.blood_sugar),
    # 25.最後上傳時間OK
    path("last-upload/", views.last_upload),
    # 44.上一筆紀錄資訊OK
    path("records/", views.records),
    # ========== 日記 ==========
    # 14.日記列表資料OK
    path("diary/", views.diary),
    # 15.飲食日記OK
    path("diet/", views.diet),
    # 40.刪除日記記錄OK
    # path("records/", views.records), -> 44.上一筆紀錄資訊
    # ========== 關懷資訊 ==========
    # 27.獲取關懷諮詢OK
    # 28.發送關懷諮詢OK
    path("care/", views.care),
    # ========== 糖化血色素 ==========
    # 32.糖化血色素OK
    # 33.送糖化血色素OK
    # 34.刪除糖化血色素OK
    path("a1c/", views.a1c),
    # ========== 就醫資訊 ==========
    # 30.就醫資訊OK
    # 31.更新就醫資訊OK
    path("medical/", views.medical),
    # ========== 藥物資訊 ==========
    # 41.藥物資訊OK
    # 42.上傳藥物資訊OK
    # 43.刪除藥物資訊OK
    path("drug-used/", views.drug),
]
