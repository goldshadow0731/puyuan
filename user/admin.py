from django.contrib import admin
from .models import UserProfile, UserSet, Default, Setting, Notification

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(UserSet)
admin.site.register(Default)
admin.site.register(Setting)
admin.site.register(Notification)