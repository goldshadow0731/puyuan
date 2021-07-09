from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from user.models import UserProfile, UserSet, Default, Setting
from body.models import BloodPressure, Weight, BloodSugar, DiaryDiet, UserCare
from body.models import HbA1c, MedicalInformation, DrugInformation
from django.utils.timezone import activate
from friend.models import Friend
from datetime import datetime, timedelta
import json

# Create your views here.


@ csrf_exempt  # 取消此function CSRF功能
def user(request):  # 個人資訊設定OK & 個人資訊OK
    if request.method == "PATCH":
        try:
            data = json.loads((request.body).decode(
                'utf8'))  # Bytes -> Json -> dict
            if UserSet.objects.filter(UUID=request.user.UUID):
                userset = UserSet.objects.filter(UUID=request.user.UUID)
                userset.update(name=data["name"])
                userset.update(birthday=data["birthday"])
                userset.update(height=data["height"])
                userset.update(gender=data["gender"])
                userset.update(FCM_ID=data["fcm_id"])
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
                "gender": int(userset.gender),
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
                    "sugar_delta_max": int(default.sugar_delta_max),
                    "sugar_delta_min": int(default.sugar_delta_min),
                    "sugar_morning_max": int(default.sugar_morning_max),
                    "sugar_morning_min": int(default.sugar_morning_min),
                    "sugar_evening_max": int(default.sugar_evening_max),
                    "sugar_evening_min": int(default.sugar_evening_min),
                    "sugar_before_max": int(default.sugar_before_max),
                    "sugar_before_min": int(default.sugar_before_min),
                    "sugar_after_max": int(default.sugar_after_max),
                    "sugar_after_min": int(default.sugar_after_min),
                    "systolic_max": int(default.systolic_max),
                    "systolic_min": int(default.systolic_min),
                    "diastolic_max": int(default.diastolic_max),
                    "diastolic_min": int(default.diastolic_min),
                    "pulse_max": int(default.pulse_max),
                    "pulse_min": int(default.pulse_min),
                    "weight_max": int(default.weight_max),
                    "weight_min": int(default.weight_min),
                    "bmi_max": int(default.bmi_max),
                    "bmi_min": int(default.bmi_min),
                    "body_fat_max": int(default.body_fat_max),
                    "body_fat_min": int(default.body_fat_min),
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
            message = {"status": "0", "user": response}
        finally:
            return JsonResponse(message)


@ csrf_exempt
def default_value(request):  # 個人預設值OK
    if request.method == "PATCH":
        try:
            data = json.loads((request.body).decode(
                'utf8'))  # Bytes -> Json -> dict
            if Default.objects.filter(UUID=request.user.UUID):
                default = Default.objects.filter(UUID=request.user.UUID)
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
                ''' 血壓&脈搏 '''
                default.update(systolic_max=data["systolic_max"])
                default.update(systolic_min=data["systolic_min"])
                default.update(diastolic_max=data["diastolic_max"])
                default.update(diastolic_min=data["diastolic_min"])
                default.update(pulse_max=data["pulse_max"])
                default.update(pulse_min=data["pulse_min"])
                ''' 體重 '''
                default.update(weight_max=data["weight_max"])
                default.update(weight_min=data["weight_min"])
                default.update(bmi_max=data["bmi_max"])
                default.update(bmi_min=data["bmi_min"])
                default.update(body_fat_max=data["body_fat_max"])
                default.update(body_fat_min=data["body_fat_min"])
            else:
                raise Exception("NoUser")
        except Exception as e:
            message = {"status": "1"}
        else:
            message = {"status": "0"}
        finally:
            return JsonResponse(message)


@ csrf_exempt
def setting(request):  # 個人設定OK
    if request.method == "PATCH":
        try:
            data = json.loads((request.body).decode(
                'utf8'))  # Bytes -> Json -> dict
            if Setting.objects.filter(UUID=request.user.UUID):
                setting = Setting.objects.filter(UUID=request.user.UUID)
                setting.update(after_recording=data["after_recording"])
                setting.update(
                    no_recording_for_a_day=data["no_recording_for_a_day"])
                setting.update(
                    over_max_or_under_min=data["over_max_or_under_min"])
                setting.update(after_meal=data["after_meal"])
                setting.update(unit_of_sugar=data["unit_of_sugar"])
                setting.update(unit_of_weight=data["unit_of_weight"])
                setting.update(unit_of_height=data["unit_of_height"])
            else:
                raise Exception("NoUser")
        except Exception as e:
            message = {"status": "1"}
        else:
            message = {"status": "0"}
        finally:
            return JsonResponse(message)


@csrf_exempt
def blood_pressure(request):  # 上傳血壓測量結果OK
    if request.method == "POST":
        try:
            data = json.loads((request.body).decode(
                'utf8'))  # Bytes -> Json -> dict
            BloodPressure.objects.create(
                user_ID=request.user.ID, systolic=data["systolic"], diastolic=data["diastolic"], pulse=data["pulse"], recorded_at=data["recorded_at"])
        except Exception as e:
            message = {"status": "1"}
        else:
            message = {"status": "0"}
        finally:
            return JsonResponse(message)


@csrf_exempt
def weight(request):  # 上傳體重測量結果OK
    if request.method == "POST":
        try:
            data = json.loads((request.body).decode(
                'utf8'))  # Bytes -> Json -> dict
            Weight.objects.create(user_ID=request.user.ID, weight=data["weight"], body_fat=data[
                                  "body_fat"], BMI=data["bmi"], recorded_at=data["recorded_at"])
        except Exception as e:
            message = {"status": "1"}
        else:
            message = {"status": "0"}
        finally:
            return JsonResponse(message)


@csrf_exempt
def blood_sugar(request):  # 上傳血糖OK
    if request.method == "POST":
        try:
            data = json.loads((request.body).decode(
                'utf8'))  # Bytes -> Json -> dict
            BloodSugar.objects.create(
                user_ID=request.user.ID, sugar=data["sugar"], timeperiod=data["timeperiod"], recorded_at=data["recorded_at"])
        except Exception as e:
            message = {"status": "1"}
        else:
            message = {"status": "0"}
        finally:
            return JsonResponse(message)


@csrf_exempt
def diet(request):  # 飲食日記OK
    if request.method == "POST":
        try:
            data = json.loads((request.body).decode(
                'utf8'))  # Bytes -> Json -> dict
            DiaryDiet.objects.create(user_ID=request.user.ID, description=data["description"], meal=data["meal"], tag=data[
                "tag[]"], image_count=data["image"], lat=data["lat"], lng=data["lng"], recorded_at=data["recorded_at"])
            image_url = "http://211.23.17.100:3001/diet_1_2020-08-17_11:11:11_0"
        except Exception as e:
            message = {"status": "1"}
        else:
            message = {"status": "0", "image_url": image_url}
        finally:
            return JsonResponse(message)


@csrf_exempt
def last_upload(request):  # 最後上傳時間OK
    if request.method == "GET":
        try:
            last_upload = {}
            blood_pressure = str(BloodPressure.objects.filter(
                user_ID=request.user.ID).latest('recorded_at').recorded_at).split("+")[0]
            last_upload["blood_pressure"] = blood_pressure

            weight = str(Weight.objects.filter(
                user_ID=request.user.ID).latest('recorded_at').recorded_at).split("+")[0]
            last_upload["weight"] = weight

            blood_sugar = str(BloodSugar.objects.filter(
                user_ID=request.user.ID).latest('recorded_at').recorded_at).split("+")[0]
            last_upload["sugar"] = blood_sugar

            diary_diet = str(DiaryDiet.objects.filter(
                user_ID=request.user.ID).latest('recorded_at').recorded_at).split("+")[0]
            last_upload["diet"] = diary_diet
        except Exception as e:
            message = {"status": "1"}
        else:
            message = {"status": "0", "last_upload": last_upload}
        finally:
            return JsonResponse(message)


@ csrf_exempt
def records(request):  # 上一筆紀錄資訊OK & 40.刪除日記記錄OK
    if request.method == "POST":
        try:
            output = {}

            # 血糖
            blood_sugar = BloodSugar.objects.filter(
                user_ID=request.user.ID).latest("recorded_at")
            output["blood_sugars"] = {
                "id": blood_sugar.id,
                "user_id": blood_sugar.user_ID,
                "sugar": blood_sugar.sugar,
                "timeperiod": blood_sugar.timeperiod,
                "recorded_at": str(blood_sugar.recorded_at)
            }
            # 血壓
            blood_pressures = BloodPressure.objects.filter(
                user_ID=request.user.ID).latest("recorded_at")
            output["blood_pressures"] = {
                "id": blood_pressures.id,
                "user_id": blood_pressures.user_ID,
                "systolic": blood_pressures.systolic,
                "diastolic": blood_pressures.diastolic,
                "pulse": blood_pressures.pulse,
                "recorded_at": str(blood_pressures.recorded_at)
            }
            # 體重
            weights = Weight.objects.filter(
                user_ID=request.user.ID).latest("recorded_at")
            output["weights"] = {
                "id": weights.id,
                "user_id": weights.user_ID,
                "weight": weights.weight,
                "body_fat": weights.body_fat,
                "bmi": weights.BMI,
                "recorded_at": str(weights.recorded_at)
            }

            timeperiod_list = ['晨起', '早餐前', '早餐後',
                               '午餐前', '午餐後', '晚餐前', '晚餐後', '睡前']
        except Exception as e:
            message = {"status": "1"}
        else:
            message = {"status": "0"}
            message.update(output)
        finally:
            return JsonResponse(message, safe=False)
    elif request.method == "DELETE":
        try:
            data = json.loads((request.body).decode(
                'utf8'))  # Bytes -> Json -> dict
            # 血糖
            if data["blood_sugars[]"]:
                for blood_sugar in data["blood_sugars[]"]:
                    BloodSugar.objects.filter(id=blood_sugar).delete()
            # 血壓
            if data["blood_pressures[]"]:
                for blood_pressures in data["blood_pressures[]"]:
                    BloodPressure.objects.filter(id=blood_pressures).delete()
            # 體重
            if data["weights[]"]:
                for weight in data["weights[]"]:
                    Weight.objects.filter(id=weight).delete()
            # 日記
            if data["diets[]"]:
                for diet in data["diets[]"]:
                    DiaryDiet.objects.filter(id=diet).delete()
        except Exception as e:
            message = {"status": "1"}
        else:
            message = {"status": "0"}
        finally:
            return JsonResponse(message)


@ csrf_exempt
def diary(request):  # 日記列表資料OK
    if request.method == "GET":
        try:
            data = json.loads((request.body).decode(
                'utf8'))  # Bytes -> Json -> dict
            start_date = datetime.strptime(
                data["date"], "%Y-%m-%d") + timedelta(hours=8) if "date" in data else datetime.now()
            end_date = start_date + timedelta(days=1)
            diary = []

            # 血壓
            blood_pressure_list = BloodPressure.objects.filter(
                user_ID=request.user.ID, created_at__range=(start_date, end_date))
            if blood_pressure_list:
                for blood_pressure in blood_pressure_list:
                    diary.append(
                        {
                            "id": blood_pressure.id,
                            "user_id": blood_pressure.user_ID,
                            "systolic": blood_pressure.systolic,
                            "diastolic": blood_pressure.diastolic,
                            "pulse": blood_pressure.pulse,
                            "recorded_at": blood_pressure.recorded_at.strftime('%Y-%m-%d %H:%M:%S'),
                            "type": "blood_pressure"
                        }
                    )

            # 體重
            weight_list = Weight.objects.filter(
                user_ID=request.user.ID, created_at__range=(start_date, end_date))
            if weight_list:
                for weight in weight_list:
                    diary.append(
                        {
                            "id": weight.id,
                            "user_id": weight.user_ID,
                            "weight": weight.weight,
                            "body_fat": weight.body_fat,
                            "bmi": weight.BMI,
                            "recorded_at": weight.recorded_at.strftime('%Y-%m-%d %H:%M:%S'),
                            "type": "weight"
                        }
                    )

            # 血糖
            blood_sugar_list = BloodSugar.objects.filter(
                user_ID=request.user.ID, created_at__range=(start_date, end_date))
            if blood_sugar_list:
                for blood_sugar in blood_sugar_list:
                    diary.append(
                        {
                            "id": blood_sugar.id,
                            "user_id": blood_sugar.user_ID,
                            "sugar": blood_sugar.sugar,
                            "timeperiod": blood_sugar.timeperiod,
                            "recorded_at": blood_sugar.recorded_at.strftime('%Y-%m-%d %H:%M:%S'),
                            "type": "blood_sugar"
                        }
                    )

            # 日記
            diet_list = DiaryDiet.objects.filter(
                user_ID=request.user.ID, created_at__range=(start_date, end_date))
            if diet_list:
                for diet in diet_list:
                    r = {
                        "id": diet.id,
                        "user_id": diet.user_ID,
                        "description": diet.description,
                        "meal": diet.meal,
                        "tag": diet.tag,
                        "image": diet.image_count,
                        "location": {
                            "lat": diet.lat,
                            "lng": diet.lng
                        },
                        "recorded_at": diet.recorded_at.strftime('%Y-%m-%d %H:%M:%S'),
                        "type": "diet"
                    }

                    # 關懷諮詢
                    user_care = UserCare.objects.filter(
                        reply_ID=request.user.ID, created_at__range=(start_date, end_date))
                    if user_care:
                        r["reply"] = user_care.latest("updated_at").message

                    diary.append(r)
        except Exception as e:
            message = {"status": "1"}
        else:
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
                    UserCare.objects.create(user_ID=request.user.ID, member_ID=friend.friend_type,
                                            reply_ID=friend.relation_ID, message=data["message"], created_at=time, updated_at=time)

            friend_list = Friend.objects.filter(
                relation_ID=request.user.ID, status=1)
            if friend_list:
                time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                for friend in friend_list:
                    UserCare.objects.create(user_ID=request.user.ID, member_ID=friend.friend_type,
                                            reply_ID=friend.user_ID, message=data["message"], created_at=time, updated_at=time)
        except Exception as e:
            message = {"status": "1"}
        else:
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
            message = {"status": "0", "cares": cares}
        finally:
            return JsonResponse(message)


@ csrf_exempt
def a1c(request):  # 糖化血色素OK & 送糖化血色素OK & 刪除糖化血色素OK
    if request.method == "GET":
        try:
            a1cs = []

            user_alc_list = HbA1c.objects.filter(user_ID=request.user.ID)
            if user_alc_list:
                for user_alc in user_alc_list:
                    a1cs.append(
                        {
                            "id": user_alc.id,
                            "user_id": user_alc.user_ID,
                            "a1c": user_alc.a1c,
                            "recorded_at": user_alc.recorded_at.strftime('%Y-%m-%d %H:%M:%S'),
                            "created_at": user_alc.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                            "updated_at": user_alc.updated_at.strftime('%Y-%m-%d %H:%M:%S')
                        }
                    )
        except Exception as e:
            message = {"status": "1"}
        else:
            message = {"status": "0", "a1cs": a1cs}
        finally:
            return JsonResponse(message)
    elif request.method == "POST":
        try:
            data = json.loads((request.body).decode(
                'utf8'))  # Bytes -> Json -> dict
            a1c = data["a1c"]
            recorded_at = data["recorded_at"]

            HbA1c.objects.create(user_ID=request.user.ID,
                                 a1c=a1c, recorded_at=recorded_at)
        except Exception as e:
            message = {"status": "1"}
        else:
            message = {"status": "0"}
        finally:
            return JsonResponse(message)
    elif request.method == "DELETE":
        try:
            data = json.loads((request.body).decode(
                'utf8'))  # Bytes -> Json -> dict
            if data["ids[]"]:
                for ID in data["ids[]"]:
                    HbA1c.objects.filter(
                        id=ID, user_ID=request.user.ID).delete()
        except Exception as e:
            message = {"status": "1"}
        else:
            message = {"status": "0"}
        finally:
            return JsonResponse(message)


@ csrf_exempt
def medical(request):  # 就醫資訊OK & 更新就醫資訊OK
    if request.method == "GET":
        try:
            medical_info = []

            if MedicalInformation.objects.filter(user_ID=request.user.ID):
                medical = MedicalInformation.objects.get(
                    user_ID=request.user.ID)
                medical_info.append(
                    {
                        "id": medical.id,
                        "user_id": medical.user_ID,
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
            data = json.loads((request.body).decode(
                'utf8'))  # Bytes -> Json -> dict
            diabetes_type = data["diabetes_type"]
            oad = data["oad"]
            insulin = data["insulin"]
            anti_hypertensives = data["anti_hypertensives"]

            if MedicalInformation.objects.filter(user_ID=request.user.ID):
                MedicalInformation.objects.filter(user_ID=request.user.ID).update(
                    diabetes_type=diabetes_type, oad=oad, insulin=insulin, anti_hypertensives=anti_hypertensives)
            else:
                MedicalInformation.objects.create(
                    user_ID=request.user.ID, diabetes_type=diabetes_type, oad=oad, insulin=insulin, anti_hypertensives=anti_hypertensives)
        except Exception as e:
            message = {"status": "1"}
        else:
            message = {"status": "0"}
        finally:
            return JsonResponse(message)


@ csrf_exempt
def drug(request):  # 藥物資訊OK & 上傳藥物資訊OK & 刪除藥物資訊OK
    if request.method == "GET":
        try:
            drug_useds = []

            drug_list = DrugInformation.objects.filter(user_ID=request.user.ID)
            if drug_list:
                for drug in drug_list:
                    drug_useds.append(
                        {
                            "id": drug.id,
                            "user_id": drug.user_ID,
                            "type": int(drug.drug_type),
                            "name": drug.name,
                            "recorded_at": drug.recorded_at.strftime('%Y-%m-%d %H:%M:%S')
                        }
                    )
        except Exception as e:
            message = {"status": "1"}
        else:
            message = {"status": "0", "drug_useds": drug_useds}
        finally:
            return JsonResponse(message)
    elif request.method == "POST":
        try:
            data = json.loads((request.body).decode(
                'utf8'))  # Bytes -> Json -> dict
            drug_type = data["type"]
            name = data["name"]
            recorded_at = data["recorded_at"]

            DrugInformation.objects.create(
                user_ID=request.user.ID, drug_type=drug_type, name=name, recorded_at=recorded_at)
        except Exception as e:
            message = {"status": "1"}
        else:
            message = {"status": "0"}
        finally:
            return JsonResponse(message)
    elif request.method == "DELETE":
        try:
            data = json.loads((request.body).decode(
                'utf8'))  # Bytes -> Json -> dict
            if data["ids[]"]:
                for ID in data["ids[]"]:
                    DrugInformation.objects.filter(
                        id=ID, user_ID=request.user.ID).delete()
        except Exception as e:
            message = {"status": "1"}
        else:
            message = {"status": "0"}
        finally:
            return JsonResponse(message)
