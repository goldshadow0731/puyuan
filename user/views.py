from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from django.contrib.auth.tokens import default_token_generator
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from user.models import UserProfile, UserSet, Default, Setting, Notification
from friend.models import Friend
from datetime import datetime
import json
import random
import string
import uuid

# Create your views here.
# API功能 | OK -> 功能完成


@csrf_exempt  # 取消此function CSRF功能
def register(request):  # 註冊OK
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode(
                'utf8'))  # Bytes -> Json -> dict
            account = data['account']
            phone = data['phone']
            email = data['email']
            password = data['password']
            UUID = uuid.uuid3(uuid.NAMESPACE_DNS, account)  # 通用唯一標示符
            invite_code = str(random.randint(100000, 1000000))  # 隨機產生邀請碼
            time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            user = UserProfile.objects.create_user(
                username=account, UUID=UUID, phone=phone, email=email, created_at=time, updated_at=time)  # 建立使用者資料
            user.set_password(password)  # 加密密碼
            user.save()  # 寫入資料庫
            UserSet.objects.create(UUID=UUID, name=account, invite_code=invite_code,
                                   must_change_password=True, login_times=0, created_at=time, updated_at=time)  # 建立使用者資料
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
            data = json.loads((request.body).decode(
                'utf8'))  # Bytes -> Json -> dict
            if 'account' not in data or 'password' not in data:
                raise Exception('LoginFail')

            """if 'fb_id' in data:
                fb_id = data['fb_id']"""

            ''' 驗證使用者 '''
            if authenticate(request, username=data['account'], password=data['password']) is not None:  # 帳號登入
                auth_result = authenticate(
                    request, username=data['account'], password=data['password'])
                user = UserProfile.objects.get(username=data['account'])
            else:
                if UserProfile.objects.filter(phone=data["account"]):  # 手機登入
                    user = UserProfile.objects.get(phone=data["account"])
                    auth_result = authenticate(
                        request, username=user.username, password=data['password'])
                elif UserProfile.objects.filter(email=data['account']):  # 信箱登入
                    user = UserProfile.objects.get(email=data["account"])
                    auth_result = authenticate(
                        request, username=user.username, password=data['password'])
                elif UserProfile.objects.filter(FB_ID=data['account']):  # FB登入
                    user = UserProfile.objects.get(FB_ID=data["account"])
                    auth_result = authenticate(
                        request, username=user.username, password=data['password'])
                else:
                    raise Exception("LoginFail")
                # raise Exception("LoginFail")

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
            data = json.loads((request.body).decode(
                'utf8'))  # Bytes -> Json -> dict
            email = data["email"]
            phone = data["phone"]

            user = UserProfile.objects.get(email=email, phone=phone)
            if UserSet.objects.get(UUID=user.UUID).verified == False:
                token = default_token_generator.make_token(user)  # 建立token
                content = user.username + " 歡迎使用普元血糖App\n驗證碼: " + token  # email內容
                send_mail("普元血糖帳號驗證", content,
                          settings.DEFAULT_FROM_EMAIL, [email])  # 寄出email
            else:
                raise Exception("EmailVeriflied")
        except Exception as e:
            message = {"status": "1"}
        else:
            message = {"status": "0"}
        finally:
            return JsonResponse(message)


@csrf_exempt
def check(request):  # 檢查驗證碼OK
    if request.method == "POST":
        try:
            data = json.loads((request.body).decode(
                'utf8'))  # Bytes -> Json -> dict
            phone = data["phone"]
            code = data["code"]

            user = UserProfile.objects.get(phone=phone)  # 取得user資料
            if default_token_generator.check_token(user, code):  # 驗證token
                UserSet.objects.filter(UUID=user.UUID).update(verified=True)
            else:
                raise Exception("CodeFail")  # 驗證碼錯誤
        except Exception as e:
            message = {"status": "1"}
        else:
            message = {"status": "0"}
        finally:
            return JsonResponse(message)


@csrf_exempt
def forgot(request):  # 忘記密碼OK
    if request.method == "POST":
        try:
            data = json.loads((request.body).decode(
                'utf8'))  # Bytes -> Json -> dict
            email = data["email"]
            phone = data["phone"]

            chars = string.ascii_letters + string.digits  # 建立字母與數字字串
            password = "".join(random.choice(chars)for i in range(
                random.randint(8, 16)))  # 隨機從字串中隨機取8~16個字元作為密碼

            ''' 存入新密碼 '''
            if UserProfile.objects.filter(email=email, phone=phone):
                user = UserProfile.objects.get(
                    email=email, phone=phone)
                user.set_password(password)
                user.save()
                ''' 將需要改變密碼設為Ture '''
                UserSet.objects.filter(UUID=user.UUID).update(
                    must_change_password=True)
                content = "新的密碼為: " + password
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
            data = json.loads((request.body).decode(
                'utf8'))  # Bytes -> Json -> dict
            password = data["password"]
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
            data = json.loads((request.body).decode(
                'utf8'))  # Bytes -> Json -> dict
            if not UserProfile.objects.filter(username=data["account"]):
                raise Exception("NoUser")
        except Exception as e:
            message = {"status": "1"}
        else:
            message = {"status": "0"}
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
                        user_ID=request.user.ID, member_ID=friend.friend_type, reply_ID=friend.relation_ID, message=data["message"], updated_at=time)

            friend_list = Friend.objects.filter(
                relation_ID=request.user.ID, friend_type=1, status=1)
            if friend_list:
                time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                for friend in friend_list:
                    Notification.objects.create(
                        user_ID=request.user.ID, member_ID=friend.friend_type, reply_ID=friend.user_ID, message=data["message"], updated_at=time)
        except Exception as e:
            message = {"status": "1"}
        else:
            message = {"status": "0"}
        finally:
            return JsonResponse(message)
