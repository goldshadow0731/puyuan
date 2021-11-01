from django.core.mail import send_mail
from django.conf import settings
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from django.contrib.auth.tokens import default_token_generator
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from user.models import UserProfile, UserSet, Default, Setting, Notification, Share
from body.models import BloodPressure, Weight, BloodSugar, DiaryDiet
from friend.models import Friend
from datetime import datetime
import json
import random
import string
import uuid
import urllib

# Create your views here.
# API功能 | OK -> 功能完成


@csrf_exempt  # 取消此function CSRF功能
def register(request):  # 註冊OK
    if request.method == "POST":
        try:
            data = urllib.parse.unquote(str(request.body, encoding="utf-8"))
            account = data.split("&")[0].split("=")[1]
            email = data.split("&")[1].split("=")[1]
            password = data.split("&")[2].split("=")[1]

            UUID = uuid.uuid3(uuid.NAMESPACE_DNS, account)  # 通用唯一標示符
            invite_code = str(random.randint(100000, 1000000))  # 隨機產生邀請碼
            time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            user = UserProfile.objects.create_user(
                username=account, UUID=UUID, email=email, created_at=time, updated_at=time)  # 建立使用者資料
            user.set_password(password)  # 加密密碼
            user.save()  # 寫入資料庫
            UserSet.objects.create(UUID=UUID, name=account, invite_code=invite_code,
                                   must_change_password=False, login_times=0, created_at=time, updated_at=time)  # 建立使用者資料
            Default.objects.create(
                UUID=UUID, created_at=time, updated_at=time)  # 建立使用者預設值
            Setting.objects.create(
                UUID=UUID, created_at=time, updated_at=time)  # 建立使用者設定
        except Exception as e:
            message = {"status": "1"}
        else:
            message = {"status": "0"}
        finally:
            return JsonResponse(message)


@csrf_exempt
def auth(request):  # 登入OK
    if request.method == "POST":
        try:
            data = urllib.parse.unquote(str(request.body, encoding="utf-8"))
            account = data.split("&")[0].split("=")[1]
            password = data.split("&")[2].split("=")[1]

            ''' 驗證使用者 '''
            # 帳號登入
            if authenticate(request, username=account, password=password) is not None:
                auth_result = authenticate(
                    request, username=account, password=password)
                user = UserProfile.objects.get(username=account)
            else:
                raise Exception("LoginFail")

            if UserSet.objects.get(UUID=user.UUID).verified is True:
                login(request, auth_result)  # 登入使用者
                request.session.create()  # 建立token
            else:
                raise Exception("EmailNoneVerifly")
        except Exception as e:
            '''
                LoginFail -> 1
                EmailNoneVerifly -> 2
                FBStatementUnchecked -> 3
            '''
            if str(e) == "LoginFail":
                message = {"status": "1"}
            elif str(e) == "EmailNoneVerifly":
                message = {"status": "2"}
            elif str(e) == "FBStatementUnchecked":
                message = {"status": "3"}
            else:
                message = {"status": "1"}
        else:
            message = {"status": "0", "token": request.session.session_key}
        finally:
            return JsonResponse(message)


@csrf_exempt
def logout(request):  # 登出OK
    if request.method == "POST":
        try:
            logout(request)
        except Exception as e:
            message = {"status": "1"}
        else:
            message = {"status": "0"}
        finally:
            return JsonResponse(message)


@csrf_exempt
def send(request):  # 發送驗證碼OK
    if request.method == "POST":
        try:
            data = urllib.parse.unquote(str(request.body, encoding="utf-8"))
            email = data.split('=')[1]
            token = "token"
            # link = "http://192.168.1.217:8000/api/check/" + token
            # email內容
            content = "歡迎使用普元血糖App\n" + "驗證碼為：" + token
            # "請點選下列連結完成註冊:\n" + link
            send_mail("普元血糖帳號驗證", content,
                      settings.DEFAULT_FROM_EMAIL, [email])  # 寄出email
        except Exception as e:
            message = {"status": "1"}
        else:
            message = {"status": "0"}
        finally:
            return JsonResponse(message)


@ csrf_exempt
def check(request, token):  # 檢查驗證碼OK
    if request.method == "POST":
        try:
            data = json.loads((request.body).decode(
                'utf8'))  # Bytes -> Json -> dict
            email = data['email']
            username = data['account']
            # phone = data["phone"]
            # code = data["code"]

            user = UserProfile.objects.get(username=username)  # 取得user資料
            userset = UserSet.objects.filter(
                UUID=user.UUID).update(verified=True)
            # if default_token_generator.check_token(user, code):  # 驗證token
            #     UserSet.objects.filter(
            #         UUID=user.UUID).update(verified=True)
            # else:
            #     raise Exception("CodeFail")  # 驗證碼錯誤
        except Exception as e:
            message = {"status": "1"}
        else:
            message = {"status": "0"}
        finally:
            return JsonResponse(message)


@ csrf_exempt
def forgot(request):  # 忘記密碼OK
    if request.method == "POST":
        try:
            data = {
                row_data.split('=')[0]: row_data.split('=')[1]
                for row_data in urllib.parse.unquote(str(request.body, encoding='utf-8')).split('&') if row_data.split("=")[1]
            }
            phone = data["phone"]

            chars = string.ascii_letters + string.digits  # 建立字母與數字字串
            password = "".join(random.choice(chars)for i in range(
                random.randint(8, 16)))  # 隨機從字串中隨機取8~16個字元作為密碼

            ''' 存入新密碼 '''
            if UserProfile.objects.filter(phone=phone):
                user = UserProfile.objects.get(phone=phone)
                email = user.email
                user.set_password(password)
                user.save()
                ''' 將需要改變密碼設為Ture '''
                UserSet.objects.filter(UUID=user.UUID).update(
                    must_change_password=True)
                content = "新的密碼為: " + password
                print(password)
                send_mail("普元血糖找回密碼", content,
                          settings.DEFAULT_FROM_EMAIL, [email])  # 寄出email
        except Exception as e:
            message = {"status": "1"}
        else:
            message = {"status": "0"}
        finally:
            return JsonResponse(message)


@csrf_exempt
def reset(request):  # 重設密碼OK
    if request.method == "POST":
        try:
            password = urllib.parse.unquote(
                str(request.body, encoding='utf-8')).split("=")[1]
            sdata = Session.objects.get(pk=request.META.get("HTTP_COOKIE").split("; ")[
                                        1].split("=")[1]).get_decoded()  # 取得user ID
            user = UserProfile.objects.get(ID=sdata["_auth_user_id"])
            user.set_password(password)
            user.save()
            UserSet.objects.filter(
                UUID=user.UUID).update(must_change_password=False)
        except Exception as e:
            message = {"status": "1"}
        else:
            message = {"status": "0"}
        finally:
            return JsonResponse(message)


@ csrf_exempt
def register_check(request):  # 註冊確認OK
    if request.method == "GET":
        try:
            account = request.GET["account"]
            if not UserProfile.objects.filter(username=account):
                message = {"status": "0"}
            else:
                message = {"status": "1"}
        except Exception as e:
            message = {"status": "1"}
        finally:
            return JsonResponse(message)


@ csrf_exempt
def notification(request):  # 親友團通知OK
    if request.method == "POST":
        try:
            data = json.loads((request.body).decode(
                'utf8'))  # Bytes -> Json -> dict

            friend_list = Friend.objects.filter(
                user_ID=request.user.ID, friend_type=1, status=1)
            if friend_list:
                time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                for friend in friend_list:
                    Notification.objects.create(
                        UUID=request.user.UUID, member_ID=friend.friend_type, reply_ID=friend.relation_ID, message=data["message"], updated_at=time)

            friend_list = Friend.objects.filter(
                relation_ID=request.user.ID, friend_type=1, status=1)
            if friend_list:
                time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                for friend in friend_list:
                    Notification.objects.create(
                        UUID=request.user.UUID, member_ID=friend.friend_type, reply_ID=friend.user_ID, message=data["message"], updated_at=time)
        except Exception as e:
            message = {"status": "1"}
        else:
            message = {"status": "0"}
        finally:
            return JsonResponse(message)


@csrf_exempt
def news(request):  # 最新消息
    if request.method == 'GET':
        try:
            sdata = Session.objects.get(pk=request.META.get("HTTP_COOKIE").split("; ")[
                                        1].split("=")[1]).get_decoded()  # 取得user ID
            user = UserProfile.objects.get(ID=sdata['_auth_user_id'])
            UserSetdata = UserSet.objects.get(UUID=user.UUID)
            Notificationdata = Notification.objects.get(UUID=UserSetdata.UUID)
            message = {
                'status': '0',
                'news': {
                    'id': user.ID,
                    'member_id': Notificationdata.member_ID,
                    'group': UserSetdata.group,
                    'message': Notificationdata.message,
                    'pushed_at': datetime.strftime(UserSetdata.pushed_at, "%Y-%m-%d %H:%M:%S"),
                    'created_at': datetime.strftime(UserSetdata.created_at, "%Y-%m-%d %H:%M:%S"),
                    'updated_at': datetime.strftime(UserSetdata.updated_at, "%Y-%m-%d %H:%M:%S")
                }
            }
        except:
            message = {'status': '1'}
        print("news" + " " + "success")
        message = {'status': '0'}
        return JsonResponse(message)


@csrf_exempt
def share(request):  # 分享!
    uid = request.user.ID
    if request.method == 'POST':
        data = request.POST.dict()
        share_id = data['id']
        data_type = data['type']
        relation_type = data['relation_type']
        try:
            Share.objects.create(
                uid=uid, fid=share_id, data_type=data_type, relation_type=relation_type)
        except:
            output = {"status": "1"}
        else:
            output = {"status": "0"}
        return JsonResponse(output, safe=False)


@csrf_exempt
def share_check(request, relation_type):  # 查看分享（含自己分享出去的）!
    uid = request.user.ID
    if request.method == 'GET':
        try:
            if Share.objects.filter(relation_type=relation_type):
                share_checks = Share.objects.filter(
                    relation_type=relation_type)
                datas = []
                for share_check in share_checks:
                    if int(share_check.uid) != uid:
                        Friend.objects.get(
                            user_ID=uid, relation_ID=share_check.uid, status=1, friend_type=relation_type)
                        user_pro = UserProfile.objects.get(ID=share_check.uid)
                        user = UserSet.objects.get(uid=user_pro.uid)
                    else:
                        user_pro = UserProfile.objects.get(ID=uid)
                        user = UserSet.objects.get(uid=user_pro.uid)

                    if share_check.data_type == '0':
                        share_data = BloodPressure.objects.get(
                            uid=share_check.uid, id=share_check.fid)
                        created_at = datetime.strftime(
                            share_data.created_at, '%Y-%m-%d %H:%M:%S')
                        recorded_at = datetime.strftime(
                            share_data.recorded_at, '%Y-%m-%d %H:%M:%S')
                        created_at_userfile = datetime.strftime(
                            user.created_at, '%Y-%m-%d %H:%M:%S')
                        updated_at_userfile = datetime.strftime(
                            user.updated_at, '%Y-%m-%d %H:%M:%S')
                        r = {
                            "id": share_data.id,
                            "user_id": share_data.uID,
                            "systolic": share_data.systolic,
                            "diastolic": share_data.diastolic,
                            "pulse": share_data.pulse,
                            "recorded_at": recorded_at,
                            "created_at": created_at,
                            "type": 0,
                            "user": {
                                "id": user_pro.UUID,
                                "name": user.name,
                                "account": user.email,
                                "email": user.email,
                                "phone": user.phone,
                                "fb_id": user_pro.fb_id,
                                "status": user.status,
                                "group": user.group,
                                "birthday": user.birthday,
                                "height": user.height,
                                "gender": user.gender,
                                "verified": user.verified,
                                "privacy_policy": user.privacy_policy,
                                "must_change_password": user.must_change_password,
                                "badge": user.badge,
                                "created_at": created_at_userfile,
                                "updated_at": updated_at_userfile
                            }
                        }
                    if share_check.data_type == '1':
                        share_data = Weight.objects.get(
                            UUID=share_check.uid, id=share_check.fid)
                        created_at = datetime.strftime(
                            share_data.created_at, '%Y-%m-%d %H:%M:%S')
                        recorded_at = datetime.strftime(
                            share_data.recorded_at, '%Y-%m-%d %H:%M:%S')
                        created_at_userfile = datetime.strftime(
                            user.created_at, '%Y-%m-%d %H:%M:%S')
                        updated_at_userfile = datetime.strftime(
                            user.updated_at, '%Y-%m-%d %H:%M:%S')
                        r = {
                            "id": share_data.id,
                            "user_id": share_data.uID,
                            "weight": float(share_data.weight),
                            "body_fat": float(share_data.body_fat),
                            "bmi": float(share_data.bmi),
                            "recorded_at": recorded_at,
                            "created_at": created_at,
                            "type": 1,
                            "user": {
                                "id": user_pro.UUID,
                                "name": user.name,
                                "account": user.email,
                                "email": user.email,
                                "phone": user.phone,
                                "fb_id": user_pro.fb_id,
                                "status": user.status,
                                "group": user.group,
                                "birthday": user.birthday,
                                "height": user.height,
                                "gender": user.gender,
                                "verified": user.verified,
                                "privacy_policy": user.privacy_policy,
                                "must_change_password": user.must_change_password,
                                "badge": user.badge,
                                "created_at": created_at_userfile,
                                "updated_at": updated_at_userfile
                            }
                        }
                    if share_check.data_type == '2':
                        share_data = BloodSugar.objects.get(
                            UUID=share_check.uid, id=share_check.fid)
                        created_at = datetime.strftime(
                            share_data.created_at, '%Y-%m-%d %H:%M:%S')
                        recorded_at = datetime.strftime(
                            share_data.recorded_at, '%Y-%m-%d %H:%M:%S')
                        created_at_userfile = datetime.strftime(
                            user.created_at, '%Y-%m-%d %H:%M:%S')
                        updated_at_userfile = datetime.strftime(
                            user.updated_at, '%Y-%m-%d %H:%M:%S')
                        r = {
                            "id": share_data.id,
                            "user_id": share_data.uID,
                            "sugar": float(share_data.sugar),
                            "timeperiod": int(share_data.timeperiod),
                            "recorded_at": recorded_at,
                            "created_at": created_at,
                            "type": 2,
                            "user": {
                                "id": user_pro.id,
                                "name": user.name,
                                "account": user.email,
                                "email": user.email,
                                "phone": user.phone,
                                "fb_id": user_pro.fb_id,
                                "status": user.status,
                                "group": user.group,
                                "birthday": user.birthday,
                                "height": user.height,
                                "gender": user.gender,
                                "verified": user.verified,
                                "privacy_policy": user.privacy_policy,
                                "must_change_password": user.must_change_password,
                                "badge": user.badge,
                                "created_at": created_at_userfile,
                                "updated_at": updated_at_userfile
                            }
                        }
                    if share_check.data_type == '3':
                        share_data = DiaryDiet.objects.get(
                            UUID=share_check.uid, id=share_check.fid)
                        created_at = datetime.strftime(
                            share_data.created_at, '%Y-%m-%d %H:%M:%S')
                        recorded_at = datetime.strftime(
                            share_data.recorded_at, '%Y-%m-%d %H:%M:%S')
                        created_at_userfile = datetime.strftime(
                            user.created_at, '%Y-%m-%d %H:%M:%S')
                        updated_at_userfile = datetime.strftime(
                            user.updated_at, '%Y-%m-%d %H:%M:%S')
                        image = str(share_data.image)
                        r = {
                            "id": share_data.id,
                            "user_id": share_data.uID,
                            "description": share_data.description,
                            "meal": int(share_data.meal),
                            "tag": share_data.tag,
                            "image": str(image),
                            "lat": share_data.lat,
                            "lng": share_data.lng,
                            "recorded_at": recorded_at,
                            "created_at": created_at,
                            "type": 3,
                            "user": {
                                "id": user_pro.UUID,
                                "name": user.name,
                                "account": user.email,
                                "email": user.email,
                                "phone": user.phone,
                                "fb_id": user_pro.fb_id,
                                "status": user.status,
                                "group": user.group,
                                "birthday": user.birthday,
                                "height": user.height,
                                "gender": user.gender,
                                "verified": user.verified,
                                "privacy_policy": user.privacy_policy,
                                "must_change_password": user.must_change_password,
                                "badge": user.badge,
                                "created_at": created_at_userfile,
                                "updated_at": updated_at_userfile
                            }
                        }
                    datas.append(r)
                output = {"status": "0", "records": datas}
            else:
                output = {"status": "0", "records": []}
        except Exception as e:
            output = {"status": "1"}
        finally:
            return JsonResponse(output)
