from django.contrib import admin
from .models import BloodPressure, Weight, BloodSugar, DiaryDiet, UserCare, HbA1c, MedicalInformation, DrugInformation

# Register your models here.
admin.site.register(BloodPressure)
admin.site.register(Weight)
admin.site.register(BloodSugar)
admin.site.register(DiaryDiet)
admin.site.register(UserCare)
admin.site.register(HbA1c)
admin.site.register(MedicalInformation)
admin.site.register(DrugInformation)