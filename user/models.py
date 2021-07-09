from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UserProfile(AbstractUser):  # 用戶登入資料
    ID = models.AutoField(primary_key=True)  # 主鍵
    username = models.CharField(max_length=100, unique=True)  # 使用者名稱
    UUID = models.CharField(max_length=100)  # 使用者的辨識碼
    phone = models.CharField(max_length=100, blank=True, null=True)  # 使用者的電話
    email = models.CharField(max_length=100, blank=True, null=True)  # 使用者的郵件
    FB_ID = models.CharField(max_length=100, blank=True, null=True)  # FB ID

    created_at = models.DateTimeField(auto_now_add=True)  # 建立時間
    updated_at = models.DateTimeField(auto_now=True)  # 最後上線時間

    def __str__(self):
        return self.username


class UserSet(models.Model):  # 用戶個人資訊
    UUID = models.CharField(max_length=100)  # 使用者的辨識碼
    ''' 個人資訊 '''
    name = models.CharField(max_length=100, blank=True, null=True)  # 暱稱
    status = models.CharField(max_length=100, default="Normal")  # 狀態 ?
    group = models.CharField(max_length=100, blank=True, null=True)  # 群組 ?
    birthday = models.DateField(blank=True, null=True)  # 生日
    height = models.DecimalField(
        max_digits=10, decimal_places=5, blank=True, null=True)  # 身高
    weight = models.DecimalField(
        max_digits=10, decimal_places=5, blank=True, null=True)  # 體重
    gender = models.BooleanField(blank=True, null=True)  # 性別0男1女
    address = models.CharField(max_length=100, blank=True, null=True)  # 地址
    invite_code = models.CharField(max_length=100)  # 邀請碼
    unread_records_one = models.DecimalField(
        max_digits=10, decimal_places=0, default=0)  # 未讀紀錄1
    unread_records_two = models.CharField(
        max_length=100, default="0", blank=True)  # 未讀紀錄2
    unread_records_three = models.DecimalField(
        max_digits=10, decimal_places=0, default=0)  # 未讀紀錄3
    verified = models.BooleanField(default=False)  # 驗證狀態
    privacy_policy = models.BooleanField(default=False)  # 隱私政策
    must_change_password = models.BooleanField(default=False)  # 是否需要改密碼
    # Firebase Cloud Messaging ID
    FCM_ID = models.CharField(max_length=100, blank=True, null=True)
    badge = models.DecimalField(
        max_digits=10, decimal_places=0, default=0)  # 徽章
    login_times = models.DecimalField(
        max_digits=20, decimal_places=0, default=0)  # 登入時間

    created_at = models.DateTimeField(auto_now_add=True)  # 建立時間
    updated_at = models.DateTimeField(auto_now=True)  # 資料上傳時間

    def __str__(self):
        return self.UUID


class Default(models.Model):  # 個人預設值
    UUID = models.CharField(max_length=100)  # 使用者的辨識碼
    ''' 血糖 '''
    sugar_delta_max = models.DecimalField(
        max_digits=5, decimal_places=0, blank=True, null=True)
    sugar_delta_min = models.DecimalField(
        max_digits=5, decimal_places=0, blank=True, null=True)
    sugar_morning_max = models.DecimalField(
        max_digits=5, decimal_places=0, blank=True, null=True)
    sugar_morning_min = models.DecimalField(
        max_digits=5, decimal_places=0, blank=True, null=True)
    sugar_evening_max = models.DecimalField(
        max_digits=5, decimal_places=0, blank=True, null=True)
    sugar_evening_min = models.DecimalField(
        max_digits=5, decimal_places=0, blank=True, null=True)
    sugar_before_max = models.DecimalField(
        max_digits=5, decimal_places=0, blank=True, null=True)
    sugar_before_min = models.DecimalField(
        max_digits=5, decimal_places=0, blank=True, null=True)
    sugar_after_max = models.DecimalField(
        max_digits=5, decimal_places=0, blank=True, null=True)
    sugar_after_min = models.DecimalField(
        max_digits=5, decimal_places=0, blank=True, null=True)
    ''' 血壓 脈搏 '''
    systolic_max = models.DecimalField(
        max_digits=5, decimal_places=0, blank=True, null=True)
    systolic_min = models.DecimalField(
        max_digits=5, decimal_places=0, blank=True, null=True)
    diastolic_max = models.DecimalField(
        max_digits=5, decimal_places=0, blank=True, null=True)
    diastolic_min = models.DecimalField(
        max_digits=5, decimal_places=0, blank=True, null=True)
    pulse_max = models.DecimalField(
        max_digits=5, decimal_places=0, blank=True, null=True)
    pulse_min = models.DecimalField(
        max_digits=5, decimal_places=0, blank=True, null=True)
    ''' 體重 BMI '''
    weight_max = models.DecimalField(
        max_digits=5, decimal_places=0, blank=True, null=True)
    weight_min = models.DecimalField(
        max_digits=5, decimal_places=0, blank=True, null=True)
    bmi_max = models.DecimalField(
        max_digits=5, decimal_places=0, blank=True, null=True)
    bmi_min = models.DecimalField(
        max_digits=5, decimal_places=0, blank=True, null=True)
    body_fat_max = models.DecimalField(
        max_digits=5, decimal_places=0, blank=True, null=True)
    body_fat_min = models.DecimalField(
        max_digits=5, decimal_places=0, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)  # 建立時間
    updated_at = models.DateTimeField(auto_now=True)  # 最後上傳時間

    def __str__(self):
        return self.UUID


class Setting(models.Model):  # 個人設定
    UUID = models.CharField(max_length=100)  # 使用者的辨識碼
    after_recording = models.BooleanField(default=False)
    no_recording_for_a_day = models.BooleanField(default=False)  # 未記錄天數
    over_max_or_under_min = models.BooleanField(default=False)
    after_meal = models.BooleanField(default=False)
    unit_of_sugar = models.BooleanField(default=False)  # 血糖單位
    unit_of_weight = models.BooleanField(default=False)  # 體重單位
    unit_of_height = models.BooleanField(default=False)  # 身高單位

    created_at = models.DateTimeField(auto_now_add=True)  # 建立時間
    updated_at = models.DateTimeField(auto_now=True)  # 資料上傳時間

    def __str__(self):
        return self.UUID


class Notification(models.Model):  # 親友團通知
    user_ID = models.IntegerField(null=True)  # 使用者的ID
    member_ID = models.IntegerField(null=True)  # 好友類型 | 0:醫師團 1:親友團 2:糖友團
    reply_ID = models.IntegerField(null=True)  # 好友ID null為罐頭訊息
    message = models.CharField(max_length=100, blank=True, null=True)  # 訊息

    created_at = models.DateTimeField(auto_now_add=True)  # 建立時間
    updated_at = models.DateTimeField(blank=True)  # 資料上傳時間

    def __str__(self):
        return self.user_ID
