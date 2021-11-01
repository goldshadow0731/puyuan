from json import encoder
from django.conf import settings
from django.contrib.sessions.models import Session
from django.http import JsonResponse
from django.shortcuts import render, resolve_url
from django.views.decorators.csrf import csrf_exempt
from user.models import UserProfile, UserSet, Default, Setting
from body.models import BloodPressure, Weight, BloodSugar, DiaryDiet, UserCare
from body.models import HbA1c, MedicalInformation, DrugInformation
from django.utils.timezone import make_aware
from friend.models import Friend
from datetime import datetime, timedelta
import json
import pytz
import urllib

# Create your views here.


@ csrf_exempt  # 取消此function CSRF功能
def user(request):  # 個人資訊設定OK & 個人資訊OK
    if request.method == "PATCH":
        try:
            data = {
                row_data.split('=')[0]: row_data.split('=')[1]
                for row_data in urllib.parse.unquote(str(request.body, encoding='utf-8')).split('&') if 1
            }
            if UserSet.objects.filter(UUID=request.user.UUID):
                userset = UserSet.objects.filter(UUID=request.user.UUID)
                if "fcm_id" in data:
                    userset.update(FCM_ID=data["fcm_id"])
                else:
                    userset.update(name=data["name"])
                    userset.update(birthday=data["birthday"])
                    userset.update(height=data["height"])
                    userset.update(gender=data["gender"])
                    userset.update(address=data["address"])
                    userset.update(weight=float(data["weight"]))
                    user = UserProfile.objects.filter(UUID=request.user.UUID)
                    user.update(phone=data["phone"])
                    user.update(email=data["email"])
            else:
                raise Exception("NoUser")
        except Exception as e:
            message = {"status": "1"}
        else:
            print("patch user" + " " + "success")
            message = {"status": "0"}
        finally:
            return JsonResponse(message)
    elif request.method == "GET":
        try:
            user = UserProfile.objects.get(UUID=request.user.UUID)
            userset = UserSet.objects.get(UUID=user.UUID)
            default = Default.objects.get(UUID=user.UUID)
            setting = Setting.objects.get(UUID=user.UUID)
            response = {
                "id": user.ID,
                "name": userset.name,
                "account": user.username,
                "email": user.email,
                "phone": user.phone,
                "fb_id": user.FB_ID,
                "status": userset.status,
                "group": userset.group,
                "birthday": userset.birthday,
                "height": userset.height,
                "weight": userset.weight,
                "gender": int(userset.gender) if userset.gender != None else userset.gender,
                "address": userset.address,
                "unread_records": [
                    int(userset.unread_records_one),
                    userset.unread_records_two,
                    int(userset.unread_records_three)
                ],
                "verified": int(userset.verified),
                "privacy_policy": int(userset.privacy_policy),
                "must_change_password": 1 if userset.must_change_password else 0,
                "fcm_id": userset.FCM_ID,
                "badge": int(userset.badge),
                "login_times": int(userset.login_times),
                "created_at": userset.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": userset.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                "default": {
                    "id": default.id,
                    "user_id": default.UUID,
                    "sugar_delta_max": default.sugar_delta_max,
                    "sugar_delta_min": default.sugar_delta_min,
                    "sugar_morning_max": default.sugar_morning_max,
                    "sugar_morning_min": default.sugar_morning_min,
                    "sugar_evening_max": default.sugar_evening_max,
                    "sugar_evening_min": default.sugar_evening_min,
                    "sugar_before_max": default.sugar_before_max,
                    "sugar_before_min": default.sugar_before_min,
                    "sugar_after_max": default.sugar_after_max,
                    "sugar_after_min": default.sugar_after_min,
                    "systolic_max": default.systolic_max,
                    "systolic_min": default.systolic_min,
                    "diastolic_max": default.diastolic_max,
                    "diastolic_min": default.diastolic_min,
                    "pulse_max": default.pulse_max,
                    "pulse_min": default.pulse_min,
                    "weight_max": default.weight_max,
                    "weight_min": default.weight_min,
                    "bmi_max": default.bmi_max,
                    "bmi_min": default.bmi_min,
                    "body_fat_max": default.body_fat_max,
                    "body_fat_min": default.body_fat_min,
                    "created_at": default.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated_at": default.updated_at.strftime("%Y-%m-%d %H:%M:%S")
                },
                "setting": {
                    "id": setting.id,
                    "user_id": setting.UUID,
                    "after_recording": int(setting.after_recording),
                    "no_recording_for_a_day": int(setting.no_recording_for_a_day),
                    "over_max_or_under_min": int(setting.over_max_or_under_min),
                    "after_meal": int(setting.after_meal),
                    "unit_of_sugar": int(setting.unit_of_sugar),
                    "unit_of_weight": int(setting.unit_of_weight),
                    "unit_of_height": int(setting.unit_of_height),
                    "created_at": setting.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated_at": setting.updated_at.strftime("%Y-%m-%d %H:%M:%S")
                }
            }
        except Exception as e:
            message = {"status": "1"}
        else:
            print("get user" + " " + "success")
            message = {"status": "0", "user": response}
        finally:
            return JsonResponse(message)


@ csrf_exempt
def default_value(request):  # 個人預設值OK
    if request.method == "PATCH":
        try:
            data = {
                row_data.split('=')[0]: row_data.split('=')[1]
                for row_data in urllib.parse.unquote(str(request.body, encoding='utf-8')).split('&') if row_data.split("=")[1]
            }
            if Default.objects.filter(UUID=request.user.UUID):
                default = Default.objects.filter(UUID=request.user.UUID)
                if "sugar_delta_max" in data:
                    ''' 血糖 '''
                    default.update(sugar_delta_max=data["sugar_delta_max"])
                    default.update(sugar_delta_min=data["sugar_delta_min"])
                    default.update(sugar_morning_max=data["sugar_morning_max"])
                    default.update(sugar_morning_min=data["sugar_morning_min"])
                    default.update(sugar_evening_max=data["sugar_evening_max"])
                    default.update(sugar_evening_min=data["sugar_evening_min"])
                    default.update(sugar_before_max=data["sugar_before_max"])
                    default.update(sugar_before_min=data["sugar_before_min"])
                    default.update(sugar_after_max=data["sugar_after_max"])
                    default.update(sugar_after_min=data["sugar_after_min"])
                elif "systolic_max" in data:
                    ''' 血壓&脈搏 '''
                    default.update(systolic_max=data["systolic_max"])
                    default.update(systolic_min=data["systolic_min"])
                    default.update(diastolic_max=data["diastolic_max"])
                    default.update(diastolic_min=data["diastolic_min"])
                    default.update(pulse_max=data["pulse_max"])
                    default.update(pulse_min=data["pulse_min"])
                elif "weight_max" in data:
                    ''' 體重 '''
                    default.update(weight_max=data["weight_max"])
                    default.update(weight_min=data["weight_min"])
                elif "body_fat_max" in data:
                    ''' 體脂 '''
                    default.update(body_fat_max=data["body_fat_max"])
                    default.update(body_fat_min=data["body_fat_min"])
            else:
                raise Exception("NoUser")
        except Exception as e:
            message = {"status": "1"}
        else:
            print("patch default_value" + " " + "success")
            message = {"status": "0"}
        finally:
            return JsonResponse(message)


@ csrf_exempt
def setting(request):  # 個人設定OK
    if request.method == "PATCH":
        try:
            data = {
                row_data.split('=')[0]: row_data.split('=')[1]
                for row_data in urllib.parse.unquote(str(request.body, encoding='utf-8')).split('&') if 1
            }
            if Setting.objects.filter(UUID=request.user.UUID):
                setting = Setting.objects.filter(UUID=request.user.UUID)
                if "after_recording" in data:
                    setting.update(after_recording=data["after_recording"])
                    setting.update(
                        no_recording_for_a_day=data["no_recording_for_a_day"])
                    setting.update(
                        over_max_or_under_min=data["over_max_or_under_min"])
                elif "after_meal" in data:
                    setting.update(after_meal=data["after_meal"])
                    setting.update(unit_of_sugar=data["unit_of_sugar"])
                    setting.update(unit_of_weight=data["unit_of_weight"])
                    setting.update(unit_of_height=data["unit_of_height"])
            else:
                raise Exception("NoUser")
        except Exception as e:
            print(e)
            message = {"status": "1"}
        else:
            print("setting" + " " + "success")
            message = {"status": "0"}
        finally:
            return JsonResponse(message)


@ csrf_exempt
def blood_pressure(request):  # 上傳血壓測量結果OK
    if request.method == "POST":
        try:
            data = {
                row_data.split('=')[0]: row_data.split('=')[1]
                for row_data in str(request.body, encoding='utf-8').split('&') if row_data.split("=")[1]
            }
            data['recorded_at'] = urllib.parse.unquote(data['recorded_at'])
            data['recorded_at'] = datetime.strptime(
                data['recorded_at'], "%Y-%m-%d %H:%M:%S")
            tz = pytz.timezone('Asia/Taipei')
            data['recorded_at'] = make_aware(data['recorded_at'], tz)
            BloodPressure.objects.create(
                UUID=request.user.UUID, systolic=data["systolic"], diastolic=data["diastolic"], pulse=data["pulse"], recorded_at=data["recorded_at"])
        except Exception as e:
            message = {"status": "1"}
        else:
            print("blood_pressure" + " " + "success")
            message = {"status": "0"}
        finally:
            return JsonResponse(message)


@ csrf_exempt
def weight(request):  # 上傳體重測量結果OK
    if request.method == "POST":
        try:
            data = {
                row_data.split('=')[0]: row_data.split('=')[1]
                for row_data in str(request.body, encoding='utf-8').split('&') if row_data.split("=")[1]
            }
            data['recorded_at'] = urllib.parse.unquote(data['recorded_at'])
            data['recorded_at'] = datetime.strptime(
                data['recorded_at'], "%Y-%m-%d %H:%M:%S")
            tz = pytz.timezone('Asia/Taipei')
            data['recorded_at'] = make_aware(data['recorded_at'], tz)
            Weight.objects.create(UUID=request.user.UUID, weight=data["weight"], body_fat=data[
                                  "body_fat"], BMI=data["bmi"], recorded_at=data["recorded_at"])
        except Exception as e:
            message = {"status": "1"}
        else:
            print("weight" + " " + "success")
            message = {"status": "0"}
        finally:
            return JsonResponse(message)


@ csrf_exempt
def blood_sugar(request):  # 上傳血糖OK
    if request.method == "POST":
        try:
            data = {
                row_data.split('=')[0]: row_data.split('=')[1]
                for row_data in str(request.body, encoding='utf-8').split('&') if row_data.split("=")[1]
            }
            data['recorded_at'] = urllib.parse.unquote(data['recorded_at'])
            data['recorded_at'] = datetime.strptime(
                data['recorded_at'], "%Y-%m-%d %H:%M:%S")
            tz = pytz.timezone('Asia/Taipei')
            data['recorded_at'] = make_aware(data['recorded_at'], tz)
            BloodSugar.objects.create(
                UUID=request.user.UUID, sugar=data["sugar"], timeperiod=data["timeperiod"], recorded_at=data["recorded_at"])
        except Exception as e:
            message = {"status": "1"}
        else:
            print("blood_sugar" + " " + "success")
            message = {"status": "0"}
        finally:
            return JsonResponse(message)


@ csrf_exempt
def diet(request):  # 飲食日記OK
    if request.method == "POST":
        try:
            data = {
                row_data.split('=')[0]: row_data.split('=')[1]
                for row_data in urllib.parse.unquote(str(request.body, encoding='utf-8')).split('&') if 1
            }
            data['recorded_at'] = datetime.strptime(
                data['recorded_at'], "%Y-%m-%d %H:%M:%S")
            tz = pytz.timezone('Asia/Taipei')
            data['recorded_at'] = make_aware(data['recorded_at'], tz)
            # DiaryDiet.objects.create(UUID=request.user.UUID, description=data["description"], meal=data[
            #     "meal"], image_count=data["image"], lat=data["lat"], lng=data["lng"], recorded_at=data["recorded_at"])
            image_url = "http://211.23.17.100:3001/diet_1_2020-08-17_11:11:11_0"
        except Exception as e:
            print(e)
            message = {"status": "1"}
        else:
            message = {"status": "0", "image_url": image_url}
        finally:
            return JsonResponse(message)


@ csrf_exempt
def last_upload(request):  # 最後上傳時間OK
    if request.method == "GET":
        try:
            last_upload = {}
            blood_pressure = str(BloodPressure.objects.filter(
                UUID=request.user.UUID).latest('recorded_at').recorded_at).split("+")[0]
            last_upload["blood_pressure"] = blood_pressure

            weight = str(Weight.objects.filter(
                UUID=request.user.UUID).latest('recorded_at').recorded_at).split("+")[0]
            last_upload["weight"] = weight

            blood_sugar = str(BloodSugar.objects.filter(
                UUID=request.user.UUID).latest('recorded_at').recorded_at).split("+")[0]
            last_upload["sugar"] = blood_sugar

            diary_diet = str(DiaryDiet.objects.filter(
                UUID=request.user.UUID).latest('recorded_at').recorded_at).split("+")[0]
            last_upload["diet"] = diary_diet
        except Exception as e:
            message = {"status": "1"}
        else:
            print("last_upload" + " " + "success")
            message = {"status": "0", "last_upload": last_upload}
        finally:
            return JsonResponse(message)


@ csrf_exempt
def records(request):  # 上一筆紀錄資訊OK & 40.刪除日記記錄OK
    if request.method == "POST":
        try:
            print(request)
            print(request.body)
            output = {}

            # 血糖
            if BloodSugar.objects.filter(UUID=request.user.UUID):
                blood_sugar = BloodSugar.objects.filter(
                    UUID=request.user.UUID).latest("recorded_at")
                output["blood_sugars"] = {
                    "id": blood_sugar.id,
                    "user_id": blood_sugar.UUID,
                    "sugar": blood_sugar.sugar,
                    "timeperiod": blood_sugar.timeperiod,
                    "recorded_at": str(blood_sugar.recorded_at)
                }
            else:
                output["blood_sugars"] = {
                    "id": None,
                    "user_id": None,
                    "sugar": None,
                    "timeperiod": None,
                    "recorded_at": None
                }
            # 血壓
            if BloodPressure.objects.filter(UUID=request.user.UUID):
                blood_pressures = BloodPressure.objects.filter(
                    UUID=request.user.UUID).latest("recorded_at")
                output["blood_pressures"] = {
                    "id": blood_pressures.id,
                    "user_id": blood_pressures.UUID,
                    "systolic": blood_pressures.systolic,
                    "diastolic": blood_pressures.diastolic,
                    "pulse": blood_pressures.pulse,
                    "recorded_at": str(blood_pressures.recorded_at)
                }
            else:
                output["blood_pressures"] = {
                    "id": None,
                    "user_id": None,
                    "systolic": None,
                    "diastolic": None,
                    "pulse": None,
                    "recorded_at": None
                }
            # 體重

            if Weight.objects.filter(UUID=request.user.UUID):
                weights = Weight.objects.filter(
                    UUID=request.user.UUID).latest("recorded_at")
                output["weights"] = {
                    "id": weights.id,
                    "user_id": weights.UUID,
                    "weight": weights.weight,
                    "body_fat": weights.body_fat,
                    "bmi": weights.BMI,
                    "recorded_at": str(weights.recorded_at)
                }
            else:
                output["weights"] = {
                    "id": None,
                    "user_id": None,
                    "weight": None,
                    "body_fat": None,
                    "bmi": None,
                    "recorded_at": None
                }

            # timeperiod_list = ['晨起', '早餐前', '早餐後',
            #                    '午餐前', '午餐後', '晚餐前', '晚餐後', '睡前']
        except Exception as e:
            message = {"status": "1"}
        else:
            print("post record" + " " + "success")
            message = {"status": "0"}
            message.update(output)
        finally:
            return JsonResponse(message, safe=False)
    elif request.method == "DELETE":
        try:
            # 血糖
            if request.GET.getlist("blood_sugars[]"):
                data_list = request.GET.getlist("blood_sugars[]")
                for data in data_list:
                    BloodSugar.objects.filter(id=data).delete()
            # 血壓
            if request.GET.getlist("blood_pressures[]"):
                data_list = request.GET.getlist("blood_pressures[]")
                for data in data_list:
                    BloodPressure.objects.filter(id=data).delete()
            # 體重
            if request.GET.getlist("weights[]"):
                data_list = request.GET.getlist("weights[]")
                for data in data_list:
                    Weight.objects.filter(id=data).delete()
            # 日記
            if request.GET.getlist("diets[]"):
                data_list = request.GET.getlist("diets[]")
                for data in data_list:
                    DiaryDiet.objects.filter(id=data).delete()
        except Exception as e:
            message = {"status": "1"}
        else:
            print("delete record" + " " + "success")
            message = {"status": "0"}
        finally:
            return JsonResponse(message)


@ csrf_exempt
def diary(request):  # 日記列表資料OK
    if request.method == "GET":
        try:
            data = request.GET["date"]  # str
            diary_date = datetime.strptime(data, "%Y-%m-%d")
            tz = pytz.timezone('Asia/Taipei')
            start_date = make_aware(diary_date, tz)
            end_date = start_date + timedelta(days=1)
            diary = []
            tz = pytz.timezone('Asia/Taipei')

            # 血壓
            blood_pressure_list = BloodPressure.objects.filter(
                UUID=request.user.UUID, created_at__range=(start_date, end_date))
            if blood_pressure_list:
                for blood_pressure in blood_pressure_list:
                    diary.append({
                        "id": blood_pressure.id,
                        "user_id": blood_pressure.UUID,
                        "systolic": blood_pressure.systolic,
                        "diastolic": blood_pressure.diastolic,
                        "pulse": int(blood_pressure.pulse),
                        "recorded_at": blood_pressure.recorded_at.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S'),
                        "type": "blood_pressure"
                    })
            # 體重
            weight_list = Weight.objects.filter(
                UUID=request.user.UUID, created_at__range=(start_date, end_date))
            if weight_list:
                for weight in weight_list:
                    diary.append({
                        "id": weight.id,
                        "user_id": weight.UUID,
                        "weight": weight.weight,
                        "body_fat": weight.body_fat,
                        "bmi": weight.BMI,
                        "recorded_at": weight.recorded_at.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S'),
                        "type": "weight"
                    })

            # 血糖
            blood_sugar_list = BloodSugar.objects.filter(
                UUID=request.user.UUID, created_at__range=(start_date, end_date))
            if blood_sugar_list:
                for blood_sugar in blood_sugar_list:
                    diary.append({
                        "id": blood_sugar.id,
                        "user_id": blood_sugar.UUID,
                        "sugar": int(blood_sugar.sugar),
                        "timeperiod": int(blood_sugar.timeperiod),
                        "recorded_at": blood_sugar.recorded_at.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S'),
                        "type": "blood_sugar"
                    })

            # 日記
            diet_list = DiaryDiet.objects.filter(
                UUID=request.user.UUID, created_at__range=(start_date, end_date))
            if diet_list:
                for diet in diet_list:
                    r = {
                        "id": diet.id,
                        "user_id": diet.UUID,
                        "description": diet.description,
                        "meal": diet.meal,
                        "tag": diet.tag,
                        "image": diet.image_count,
                        "location": {
                            "lat": diet.lat,
                            "lng": diet.lng
                        },
                        "recorded_at": diet.recorded_at.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S'),
                        "type": "diet"
                    }

                    # 關懷諮詢
                    user_care = UserCare.objects.filter(
                        UUID=request.user.UUID, created_at__range=(start_date, end_date))
                    if user_care:
                        r["reply"] = user_care.latest("updated_at").message

                    diary.append(r)
        except Exception as e:
            message = {"status": "1"}
        else:
            print("diary" + " " + "success")
            message = {"status": "0", "diary": diary}
        finally:
            return JsonResponse(message)


@ csrf_exempt
def care(request):  # 發送關懷諮詢OK & 獲取關懷諮詢OK
    if request.method == "POST":
        try:
            data = json.loads((request.body).decode(
                'utf8'))  # Bytes -> Json -> dict
            friend_list = Friend.objects.filter(
                user_ID=request.user.ID, status=1)
            if friend_list:
                time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                for friend in friend_list:
                    UserCare.objects.create(UUID=request.user.UUID, member_ID=friend.friend_type,
                                            reply_ID=friend.relation_ID, message=data["message"], created_at=time, updated_at=time)

            friend_list = Friend.objects.filter(
                relation_ID=request.user.ID, status=1)
            if friend_list:
                time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                for friend in friend_list:
                    UserCare.objects.create(UUID=request.user.UUID, member_ID=friend.friend_type,
                                            reply_ID=friend.user_ID, message=data["message"], created_at=time, updated_at=time)
        except Exception as e:
            message = {"status": "1"}
        else:
            print("post care" + " " + "success")
            message = {"status": "0"}
        finally:
            return JsonResponse(message)
    elif request.method == "GET":
        try:
            cares = []
            user_care_list = UserCare.objects.filter(reply_ID=request.user.ID)
            if user_care_list:
                for user_care in user_care_list:
                    cares.append(
                        {
                            "id": user_care.id,
                            "user_id": user_care.user_ID,
                            "member_id": user_care.member_ID,
                            "reply_id": user_care.reply_ID,
                            "message": user_care.message,
                            "created_at": user_care.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                            "updated_at": user_care.updated_at.strftime('%Y-%m-%d %H:%M:%S')
                        }
                    )
        except Exception as e:
            message = {"status": "1"}
        else:
            print("get care" + " " + "success")
            message = {"status": "0", "cares": cares}
        finally:
            return JsonResponse(message)


@ csrf_exempt
def a1c(request):  # 糖化血色素OK & 送糖化血色素OK & 刪除糖化血色素OK
    if request.method == "GET":
        try:
            a1cs = []

            user_alc_list = HbA1c.objects.filter(UUID=request.user.UUID)
            if user_alc_list:
                for user_alc in user_alc_list:
                    a1cs.append(
                        {
                            "id": user_alc.id,
                            "user_id": user_alc.UUID,
                            "a1c": user_alc.a1c,
                            "recorded_at": user_alc.recorded_at.strftime('%Y-%m-%d %H:%M:%S'),
                            "created_at": user_alc.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                            "updated_at": user_alc.updated_at.strftime('%Y-%m-%d %H:%M:%S')
                        }
                    )
        except Exception as e:
            message = {"status": "1"}
        else:
            print("get a1c" + " " + "success")
            message = {"status": "0", "a1cs": a1cs}
        finally:
            return JsonResponse(message)
    elif request.method == "POST":
        try:
            data = {
                row_data.split('=')[0]: row_data.split('=')[1]
                for row_data in urllib.parse.unquote(str(request.body, encoding='utf-8')).split('&') if row_data.split("=")[1]
            }
            data['recorded_at'] = datetime.strptime(
                data['recorded_at'], "%Y-%m-%d %H:%M:%S")
            tz = pytz.timezone('Asia/Taipei')
            data['recorded_at'] = make_aware(data['recorded_at'], tz)
            a1c = data["a1c"]
            recorded_at = data["recorded_at"]

            HbA1c.objects.create(UUID=request.user.UUID,
                                 a1c=a1c, recorded_at=recorded_at)
        except Exception as e:
            message = {"status": "1"}
        else:
            print("post a1c" + " " + "success")
            message = {"status": "0"}
        finally:
            return JsonResponse(message)
    elif request.method == "DELETE":
        try:
            print(request)
            if request.GET.getlist("ids[]"):
                for id in request.GET.getlist("ids[]"):
                    HbA1c.objects.filter(
                        id=id, UUID=request.user.UUID).delete()
        except Exception as e:
            message = {"status": "1"}
        else:
            print("delete a1c" + " " + "success")
            message = {"status": "0"}
        finally:
            return JsonResponse(message)


@ csrf_exempt
def medical(request):  # 就醫資訊OK & 更新就醫資訊OK
    if request.method == "GET":
        try:
            medical_info = []

            if MedicalInformation.objects.filter(UUID=request.user.UUID):
                medical = MedicalInformation.objects.get(
                    UUID=request.user.UUID)
                medical_info.append(
                    {
                        "id": medical.id,
                        "user_id": medical.UUID,
                        "diabetes_type": medical.diabetes_type,
                        "oad": int(medical.oad),
                        "insulin": int(medical.insulin),
                        "anti_hypertensives": int(medical.anti_hypertensives),
                        "created_at": medical.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                        "updated_at": medical.updated_at.strftime('%Y-%m-%d %H:%M:%S')
                    }
                )
        except Exception as e:
            message = {"status": "1"}
        else:
            message = {"status": "0", "medical_info": medical_info}
        finally:
            return JsonResponse(message)
    elif request.method == "PATCH":
        try:
            data = {
                row_data.split('=')[0]: row_data.split('=')[1]
                for row_data in urllib.parse.unquote(str(request.body, encoding='utf-8')).split('&') if 1
            }
            diabetes_type = data["diabetes_type"]
            oad = data["oad"]
            insulin = data["insulin"]
            anti_hypertensives = data["anti_hypertensives"]

            if MedicalInformation.objects.filter(UUID=request.user.UUID):
                MedicalInformation.objects.filter(UUID=request.user.UUID).update(
                    diabetes_type=diabetes_type, oad=oad, insulin=insulin, anti_hypertensives=anti_hypertensives)
            else:
                MedicalInformation.objects.create(
                    UUID=request.user.UUID, diabetes_type=diabetes_type, oad=oad, insulin=insulin, anti_hypertensives=anti_hypertensives)
        except Exception as e:
            message = {"status": "1"}
        else:
            print("patch medical" + " " + "success")
            message = {"status": "0"}
        finally:
            return JsonResponse(message)


@ csrf_exempt
def drug(request):  # 藥物資訊OK & 上傳藥物資訊OK & 刪除藥物資訊OK
    if request.method == "GET":
        try:
            drug_useds = []

            drug_list = DrugInformation.objects.filter(UUID=request.user.UUID)
            if drug_list:
                for drug in drug_list:
                    drug_useds.append(
                        {
                            "id": drug.id,
                            "user_id": drug.UUID,
                            "type": int(drug.drug_type),
                            "name": drug.name,
                            "recorded_at": drug.recorded_at.strftime('%Y-%m-%d %H:%M:%S')
                        }
                    )
        except Exception as e:
            message = {"status": "1"}
        else:
            print("get drug" + " " + "success")
            message = {"status": "0", "drug_useds": drug_useds}
        finally:
            return JsonResponse(message)
    elif request.method == "POST":
        try:
            data = {
                row_data.split('=')[0]: row_data.split('=')[1]
                for row_data in urllib.parse.unquote(str(request.body, encoding='utf-8')).split('&') if row_data.split("=")[1]
            }
            data['recorded_at'] = datetime.strptime(
                data['recorded_at'], "%Y-%m-%d %H:%M:%S")
            tz = pytz.timezone('Asia/Taipei')
            data['recorded_at'] = make_aware(data['recorded_at'], tz)
            drug_type = data["type"]
            name = data["name"]
            recorded_at = data["recorded_at"]

            DrugInformation.objects.create(
                UUID=request.user.UUID, drug_type=drug_type, name=name, recorded_at=recorded_at)
        except Exception as e:
            message = {"status": "1"}
        else:
            print("post drug" + " " + "success")
            message = {"status": "0"}
        finally:
            return JsonResponse(message)
    elif request.method == "DELETE":
        try:
            print(request)
            if request.GET.getlist("ids[]"):
                for ID in request.GET.getlist("ids[]"):
                    DrugInformation.objects.filter(
                        id=ID, UUID=request.user.UUID).delete()
        except Exception as e:
            message = {"status": "1"}
        else:
            print("delete" + " " + "success")
            message = {"status": "0"}
        finally:
            return JsonResponse(message)


@csrf_exempt
def badge(request):  # 39.更新badge
    message = {"status": "1"}
    try:
        s = Session.objects.get(
            pk=request.headers.get('Authorization', '')[7:]).get_decoded()
        user = UserSet.objects.get(id=s['_auth_user_id'])
        if request.method == 'PUT':
            data = request.body.decode("utf-8")
            data = {
                i.split('=')[0]: i.split('=')[1]
                for i in data.replace('%40', '@').split('&') if i.split('=')[1]
            }
            if 'badge' in data:
                user.badge = data['badge']
                user.save()
                status = {"status": "0"}
    except:
        pass
    # print("badge" + " " + "success")
    return JsonResponse(message)
