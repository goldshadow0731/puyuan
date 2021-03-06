from django.db import models

# Create your models here.


class BloodPressure(models.Model):  # 血壓
    UUID = models.CharField(max_length=100)  # 使用者的辨識碼
    systolic = models.FloatField(max_length=3, default=0, null=True)  # 使用者的收縮壓
    diastolic = models.FloatField(
        max_length=3, default=0, null=True)  # 使用者的舒張壓
    pulse = models.DecimalField(
        max_digits=3, decimal_places=0, default=0, null=True)  # 使用者的心跳

    created_at = models.DateTimeField(auto_now_add=True)  # 建立時間
    recorded_at = models.DateTimeField(blank=True, null=True)  # 紀錄時間

    def __str__(self):
        msg = dict()
        msg = {
            'uid':self.UUID,
            'systolic':self.systolic,
            'diastolic':self.diastolic,
            'pulse':self.pulse,
            'recorded_at':self.recorded_at,
            'created_at':self.created_at
        }
        return str(msg)


class Weight(models.Model):  # 體重
    UUID = models.CharField(max_length=100)  # 使用者的辨識碼
    weight = models.FloatField(max_length=3, default=0, null=True)  # 使用者的體重
    body_fat = models.FloatField(
        max_length=3, default=0, null=True)  # 使用者的體重變化
    BMI = models.FloatField(max_length=3, default=0, null=True)  # 使用者的BMI

    created_at = models.DateTimeField(auto_now_add=True)  # 建立時間
    recorded_at = models.DateTimeField(blank=True, null=True)  # 紀錄時間

    def __str__(self):
        msg = dict()
        msg = {
            'uid':self.UUID,
            'weight':self.weight,
            'body_fat':self.body_fat,
            'bmi':self.BMI,
            'recorded_at':self.recorded_at,
            'created_at':self.created_at
        }
        return str(msg)


class BloodSugar(models.Model):  # 血糖
    UUID = models.CharField(max_length=100)  # 使用者的辨識碼
    sugar = models.DecimalField(
        max_digits=3, decimal_places=0, default=0, null=True)  # 使用者的血糖
    timeperiod = models.DecimalField(
        max_digits=3, decimal_places=0, default=0, null=True)  # 使用者的時段

    created_at = models.DateTimeField(auto_now_add=True)  # 建立時間
    recorded_at = models.DateTimeField(blank=True, null=True)  # 紀錄時間

    def __str__(self):
        msg = dict()
        msg = {
            'uid':self.UUID,
            'sugar':self.sugar,
            'timeperiod':self.timeperiod,
            'recorded_at':self.recorded_at,
            'created_at':self.created_at
        }
        return str(msg)


class DiaryDiet(models.Model):  # 日記
    UUID = models.CharField(max_length=100)  # 使用者的辨識碼
    description = models.CharField(max_length=5, blank=True, null=True)  # 描述
    meal = models.DecimalField(
        max_digits=5, decimal_places=0, null=True)  # 使用者的時段 早餐 午餐 晚餐
    tag = models.CharField(max_length=100, blank=True, null=True)  # tag
    image = models.ImageField(
        upload_to='diet/diet_%Y-%m-%d_%H:%M:%S', blank=True, null=True)  # 照片
    image_count = models.IntegerField(null=True)  # 照片數量
    lat = models.FloatField(max_length=100, null=True)  # 緯度
    lng = models.FloatField(max_length=100, null=True)  # 經度

    created_at = models.DateTimeField(auto_now_add=True)  # 建立時間
    recorded_at = models.DateTimeField(blank=True, null=True)  # 使用者的記錄時間

    def __str__(self):
        msg = dict()
        msg = {
            'uid':self.UUID,
            'description':self.description,
            'meal':self.meal,
            'tag':self.tag,
            'image':self.image,
            'image_count':self.image_count,
            'lat':self.lat,
            'lng':self.lng,
            'created_at':self.created_at,
            'recorded_at':self.recorded_at
        }
        return str(msg)


class UserCare(models.Model):  # 關懷諮詢
    UUID = models.CharField(max_length=100)  # 使用者的辨識碼
    member_ID = models.IntegerField(null=True)  # 好友類型 | 0:醫師團 1:親友團 2:糖友團
    reply_ID = models.IntegerField(null=True)  # 好友ID null為罐頭訊息
    message = models.CharField(max_length=100, blank=True, null=True)  # 訊息

    created_at = models.DateTimeField(auto_now_add=True)  # 建立時間
    updated_at = models.DateTimeField(blank=True)  # 資料上傳時間

    def __str__(self):
        msg = dict()
        msg = {
            'uid':self.UUID,
            'member_id':self.member_ID,
            'reply_id':self.reply_ID,
            'message':self.message,
            'created_at':self.created_at,
            'updated_at':self.updated_at
        }
        return str(msg)


class HbA1c(models.Model):  # 糖化血色素
    UUID = models.CharField(max_length=100)  # 使用者的辨識碼
    a1c = models.DecimalField(
        max_digits=6, decimal_places=0, blank=True, null=True)  # 糖化血色素

    recorded_at = models.DateTimeField(blank=True, null=True)  # 使用者的記錄時間
    created_at = models.DateTimeField(auto_now_add=True)  # 建立時間
    updated_at = models.DateTimeField(auto_now=True)  # 資料上傳時間

    def __str__(self):
        msg = dict()
        msg = {
            'uid':self.UUID,
            'a1c':self.a1c,
            'recorded_at':self.recorded_at,
            'created_at':self.created_at,
            'updated_at':self.updated_at
        }
        return str(msg)


class MedicalInformation(models.Model):  # 就醫資訊
    UUID = models.CharField(max_length=100)  # 使用者的辨識碼
    diabetes_type = models.IntegerField(null=True)  # 0~4 無/糖尿病前期/第一型/第二型/妊娠
    oad = models.BooleanField(null=True)  # 糖尿病口服藥
    insulin = models.BooleanField(null=True)  # 胰島素
    anti_hypertensives = models.BooleanField(null=True)  # 高血壓藥

    created_at = models.DateTimeField(auto_now_add=True)  # 建立時間
    updated_at = models.DateTimeField(auto_now=True)  # 資料上傳時間

    def __str__(self):
        msg = dict()
        msg = {
            'uid':self.UUID,
            'oad':self.oad,
            'insulin':self.insulin,
            'anti_hypertensives':self.anti_hypertensives,
            'diabetes_type':self.diabetes_type,
            'created_at':self.created_at,
            'updated_at':self.updated_at
            
        }
        return str(msg)


class DrugInformation(models.Model):  # 藥物資訊
    UUID = models.CharField(max_length=100)  # 使用者的辨識碼
    drug_type = models.BooleanField(null=True)  # 使用藥物類型 | 0:糖尿病藥物 1:高血壓藥物
    name = models.CharField(max_length=100, blank=True, null=True)  # 藥物的名稱

    recorded_at = models.DateTimeField(blank=True, null=True)  # 使用者的記錄時間
    created_at = models.DateTimeField(auto_now_add=True)  # 建立時間
    updated_at = models.DateTimeField(auto_now=True)  # 資料上傳時間

    def __str__(self):
        msg = dict()
        msg = {
            'uid':self.UUID,
            'drugname':self.name,
            'drug_type':self.drug_type,
            'recorded_at':self.recorded_at,
            'created_at':self.created_at,
            'updated_at':self.updated_at
        }
        return str(msg)
