from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from user.models import UserProfile, UserSet
from friend.models import Friend
from datetime import datetime
import json

# Create your views here.


@csrf_exempt
def code(request):  # 獲取控糖團邀請碼OK
    if request.method == "GET":
        try:
            if UserSet.objects.filter(UUID=request.user.UUID):
                userset = UserSet.objects.get(UUID=request.user.UUID)
            else:
                raise Exception("NoUser")
        except Exception as e:
            message = {"status": "1"}
        else:
            message = {"status": "0", "invite_code": userset.invite_code}
        finally:
            return JsonResponse(message)


@csrf_exempt
def list(request):  # 控糖團列表OK
    if request.method == "GET":
        try:
            friends = []
            friends_list = Friend.objects.filter(
                user_ID=request.user.ID, status=1)  # 好友列表(邀請人)
            if friends_list:
                for friend in friends_list:
                    friend_profile = UserProfile.objects.get(
                        ID=friend.relation_ID)  # 好友登入資料
                    friend_set = UserSet.objects.get(
                        UUID=friend_profile.UUID)  # 好友個人資料
                    friends.append(
                        {
                            "id": friend_profile.ID,
                            "name": friend_set.name,
                            "account": friend_profile.username,
                            "email": friend_profile.email,
                            "phone": friend_profile.phone,
                            "fb_id": friend_profile.FB_ID,
                            "status": friend_set.status,
                            "group": friend_set.group,
                            "birthday": friend_set.birthday,
                            "height": friend_set.height,
                            "gender": int(friend_set.gender),
                            "verified": int(friend_set.verified),
                            "privacy_policy": int(friend_set.privacy_policy),
                            "must_change_password": int(friend_set.must_change_password),
                            "badge": friend_set.badge,
                            "created_at": friend_set.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                            "updated_at": friend_set.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                            "relation_type": friend.friend_type
                        }
                    )

            friends_list = Friend.objects.filter(
                relation_ID=request.user.ID, status=1)  # 好友列表(被邀請人)
            if friends_list:
                for friend in friends_list:
                    friend_profile = UserProfile.objects.get(
                        ID=friend.user_ID)  # 好友登入資料
                    friend_set = UserSet.objects.get(
                        UUID=friend_profile.UUID)  # 好友個人資料
                    friends.append(
                        {
                            "id": friend_profile.ID,
                            "name": friend_set.name,
                            "account": friend_profile.username,
                            "email": friend_profile.email,
                            "phone": friend_profile.phone,
                            "fb_id": friend_profile.FB_ID,
                            "status": friend_set.status,
                            "group": friend_set.group,
                            "birthday": friend_set.birthday,
                            "height": friend_set.height,
                            "gender": int(friend_set.gender),
                            "verified": int(friend_set.verified),
                            "privacy_policy": int(friend_set.privacy_policy),
                            "must_change_password": int(friend_set.must_change_password),
                            "badge": friend_set.badge,
                            "created_at": friend_set.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                            "updated_at": friend_set.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                            "relation_type": friend.friend_type
                        }
                    )
        except Exception as e:
            message = {"status": "1"}
        else:
            message = {"status": "0", "friends": friends}
        finally:
            return JsonResponse(message)


@csrf_exempt
def requests(request):  # 獲取控糖團邀請OK
    if request.method == "GET":
        try:
            requests_data = []
            invite_list = Friend.objects.filter(
                relation_ID=request.user.ID, status=0)
            if invite_list:
                for invite in invite_list:
                    invite_friend_profile = UserProfile.objects.get(
                        ID=invite.user_ID)
                    invite_friend_set = UserSet.objects.get(
                        UUID=invite_friend_profile.UUID)
                    requests_data.append(
                        {
                            "id": invite.id,
                            "user_id": invite.user_ID,
                            "relation_id": invite.relation_ID,
                            "type": invite.friend_type,
                            "status": invite.status,
                            "created_at": invite.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                            "updated_at": invite.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                            "user": {
                                "id": invite_friend_profile.ID,
                                "name": invite_friend_set.name,
                                "account": invite_friend_profile.username,
                                "email": invite_friend_profile.email,
                                "phone": invite_friend_profile.phone,
                                "fb_id": invite_friend_profile.FB_ID,
                                "status": invite_friend_set.status,
                                "group": invite_friend_set.group,
                                "birthday": invite_friend_set.birthday,
                                "height": invite_friend_set.height,
                                "gender": int(invite_friend_set.gender),
                                "verified": int(invite_friend_set.verified),
                                "privacy_policy": int(invite_friend_set.privacy_policy),
                                "must_change_password": int(invite_friend_set.must_change_password),
                                "badge": invite_friend_set.badge,
                                "created_at": invite_friend_set.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                                "updated_at": invite_friend_set.updated_at.strftime('%Y-%m-%d %H:%M:%S')
                            }
                        }
                    )
        except Exception as e:
            message = {"status": "1"}
        else:
            message = {"status": "0", "requests": requests_data}
        finally:
            return JsonResponse(message)


@csrf_exempt
def send(request):  # 送出控糖團邀請OK
    if request.method == "POST":
        try:
            data = json.loads((request.body).decode(
                'utf8'))  # Bytes -> Json -> dict
            friend_type = data["type"]
            invite_code = data["invite_code"]

            if UserSet.objects.filter(invite_code=invite_code):
                friend_set = UserSet.objects.get(invite_code=invite_code)
                friend_profile = UserProfile.objects.get(UUID=friend_set.UUID)
                if not (Friend.objects.filter(user_ID=request.user.ID, relation_ID=friend_profile.ID) or Friend.objects.filter(user_ID=friend_profile.ID, relation_ID=request.user.ID)):
                    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    Friend.objects.create(user_ID=request.user.ID, relation_ID=friend_profile.ID,
                                          friend_type=friend_type, status=0, read=False, created_at=time, updated_at=time)
                else:
                    raise Exception("HaveBecomeFriends")
            else:
                raise Exception("InvalidInviteCode")
        except Exception as e:
            '''
                InvalidInviteCode -> 1
                HaveBecomeFriends -> 2
            '''
            if str(e) == "InvalidInviteCode":
                message = {"status": "1"}
            elif str(e) == "HaveBecomeFriends":
                message = {"status": "2"}
            else:
                message = {"status": "1"}
        else:
            message = {"status": "0"}
        finally:
            return JsonResponse(message)


@csrf_exempt
def accept(request, friend_invite_id):  # 接受控糖團邀請OK
    if request.method == "GET":
        try:
            if Friend.objects.filter(id=friend_invite_id, relation_ID=request.user.ID, status=0):
                Friend.objects.filter(
                    id=friend_invite_id, relation_ID=request.user.ID, status=0).update(status=1)
            else:
                raise Exception("ErrorFriendInviteId")
        except Exception as e:
            message = {"status": "1"}
        else:
            message = {"status": "0"}
        finally:
            return JsonResponse(message)


@csrf_exempt
def refuse(request, friend_invite_id):  # 拒絕控糖團邀請OK
    if request.method == "GET":
        try:
            if Friend.objects.filter(id=friend_invite_id, relation_ID=request.user.ID, status=0):
                Friend.objects.filter(
                    id=friend_invite_id, relation_ID=request.user.ID, status=0).update(status=2)
            else:
                raise Exception("ErrorFriendInviteId")
        except Exception as e:
            message = {"status": "1"}
        else:
            message = {"status": "0"}
        finally:
            return JsonResponse(message)


@csrf_exempt
def remove(request, friend_id=None):  # 刪除控糖團邀請OK & 刪除更多好友OK
    if request.method == "GET":
        try:
            if Friend.objects.filter(user_ID=request.user.ID, relation_ID=friend_id, status=0):
                Friend.objects.filter(
                    user_ID=request.user.ID, relation_ID=friend_id, status=0).delete()
            else:
                raise Exception("ErrorFriendID")
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
            IDs = data["ids[]"]

            for ID in IDs:
                # 邀請人
                if Friend.objects.filter(user_ID=request.user.ID, relation_ID=ID, status=1):
                    Friend.objects.filter(
                        user_ID=request.user.ID, relation_ID=ID, status=1).delete()
                # 被邀請人
                elif Friend.objects.filter(user_ID=ID, relation_ID=request.user.ID, status=1):
                    Friend.objects.filter(
                        user_ID=ID, relation_ID=request.user.ID, status=1).delete()
                else:
                    raise Exception("ErrorFriendID")
        except Exception as e:
            message = {"status": "1"}
        else:
            message = {"status": "0"}
        finally:
            return JsonResponse(message)


@csrf_exempt
def results(request):  # 控糖團結果OK
    if request.method == "GET":
        try:
            invite_results = []
            result_list = Friend.objects.filter(
                user_ID=request.user.ID, read=False)
            if result_list:
                for result in result_list:
                    friend_profile = UserProfile.objects.get(
                        ID=result.relation_ID)
                    friend_set = UserSet.objects.get(UUID=friend_profile.UUID)
                    invite_results.append(
                        {
                            "id": result.id,
                            "user_id": result.user_ID,
                            "relation_id": result.relation_ID,
                            "type": result.friend_type,
                            "status": int(result.status),
                            "read": result.read,
                            "created_at": result.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                            "updated_at": result.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                            "relation": {
                                "id": friend_profile.ID,
                                "name": friend_set.name,
                                "account": friend_profile.username,
                                "email": friend_profile.email,
                                "phone": friend_profile.phone,
                                "fb_id": friend_profile.FB_ID,
                                "status": friend_set.status,
                                "group": friend_set.group,
                                "birthday": friend_set.birthday,
                                "height": friend_set.height,
                                "gender": friend_set.gender,
                                "unread_records": [
                                    friend_set.unread_records_one,
                                    friend_set.unread_records_two,
                                    friend_set.unread_records_three
                                ],
                                "verified": friend_set.verified,
                                "privacy_policy": friend_set.privacy_policy,
                                "must_change_password": friend_set.must_change_password,
                                "badge": friend_set.badge,
                                "created_at": friend_set.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                                "updated_at": friend_set.updated_at.strftime('%Y-%m-%d %H:%M:%S')
                            }
                        }
                    )
                result_list.update(read=True)
        except Exception as e:
            message = {"status": "1"}
        else:
            message = {"status": "0", "results": invite_results}
        finally:
            return JsonResponse(message)
