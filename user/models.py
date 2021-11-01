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
        msg = dict()
        msg = {
            'uid': self.UUID,
            'id': self.ID,
            'phone': self.phone,
            'email': self.email,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'fb_id': self.FB_ID
        }
        return str(msg)


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
        msg = dict()
        msg = {
            'uid': self.UUID,
            'name': self.name,
            'birthday': self.birthday,
            'height': self.height,
            'gender': self.gender,
            'fcm_id': self.FCM_ID,
            'address': self.address,
            'weight': self.weight,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'verified': self.verified,
            'privacy_policy': self.privacy_policy,
            'must_change_password': self.must_change_password,
            'login_times': self.login_times,
            'status': self.status,
            'badge': self.badge,
            'group': self.group

        }
        return str(msg)


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
        msg = dict()
        msg = {
            'uid': self.UUID,
            'sugar_delta_max': self.sugar_delta_max,
            'sugar_delta_min': self.sugar_delta_min,
            'sugar_morning_max': self.sugar_morning_max,
            'sugar_morning_min': self.sugar_morning_min,
            'sugar_evening_max': self.sugar_evening_max,
            'sugar_evening_min': self.sugar_evening_min,
            'sugar_before_max': self.sugar_before_max,
            'sugar_before_min': self.sugar_before_min,
            'sugar_after_max': self.sugar_after_max,
            'sugar_after_min': self.sugar_after_min,
            'systolic_max': self.systolic_max,
            'systolic_min': self.systolic_min,
            'diastolic_max': self.diastolic_max,
            'diastolic_min': self.diastolic_min,
            'pulse_max': self.pulse_max,
            'pulse_min': self.pulse_min,
            'weight_max': self.weight_max,
            'weight_min': self.weight_min,
            'bmi_max': self.bmi_max,
            'bmi_min': self.bmi_min,
            'body_fat_max': self.body_fat_max,
            'body_fat_min': self.body_fat_min,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        return str(msg)


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
        msg = dict()
        msg = {
            'uid': self.UUID,
            'after_recording': self.after_recording,
            'no_recording_for_a_day': self.no_recording_for_a_day,
            'over_max_or_under_min': self.over_max_or_under_min,
            'after_meal': self.after_meal,
            'unit_of_sugar': self.unit_of_sugar,
            'unit_of_weight': self.unit_of_weight,
            'unit_of_height': self.unit_of_height,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        return str(msg)


class Notification(models.Model):  # 親友團通知
    UUID = models.CharField(max_length=100)  # 使用者的辨識碼
    member_ID = models.IntegerField(null=True)  # 好友類型 | 0:醫師團 1:親友團 2:糖友團
    reply_ID = models.IntegerField(null=True)  # 好友ID null為罐頭訊息
    message = models.CharField(max_length=100, blank=True, null=True)  # 訊息

    created_at = models.DateTimeField(auto_now_add=True)  # 建立時間
    updated_at = models.DateTimeField(blank=True)  # 資料上傳時間

    def __str__(self):
        msg = dict()
        msg = {
            'uid': self.UUID,
            'member_id': self.member_ID,
            'reply_id': self.reply_ID,
            'message': self.message,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        return str(msg)


class Share(models.Model):
    uID = models.CharField(max_length=100, blank=True)
    fID = models.CharField(max_length=100, blank=True)
    data_type = models.CharField(max_length=100, blank=True)
    relation_type = models.CharField(max_length=100, blank=True)

    def __str__(self):
        message = dict()
        message = {
            'ID': self.uID,
            'fID': self.fID,
            'data_type': self.data_type,
            'relation_type': self.relation_type
        }
        return str(message)
