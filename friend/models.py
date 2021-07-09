from django.db import models

# Create your models here.


class Friend(models.Model):  # 控糖團好友
    user_ID = models.IntegerField(null=True)  # 使用者的ID
    relation_ID = models.IntegerField(null=True)  # 好友的ID
    friend_type = models.IntegerField(null=True)  # 好友類型 | 0:醫師團 1:親友團 2:糖友團
    status = models.IntegerField(default=0)  # 邀請狀態 | 0:未看過邀請 1:同意 2:拒絕
    read = models.BooleanField(default=False)  # 使用者是否看過邀請結果(要對方同意或拒絕)

    created_at = models.DateTimeField(auto_now_add=True)  # 建立時間
    updated_at = models.DateTimeField(auto_now=True)  # 資料上傳時間

    def __str__(self):
        return self.user_ID
