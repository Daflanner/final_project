from django.contrib import admin
from counter.models import UserProfile, RecordedDays, MealType, Ingredient

admin.site.register(UserProfile)
admin.site.register(RecordedDays)# Register your models here.
admin.site.register(MealType)
admin.site.register(Ingredient)