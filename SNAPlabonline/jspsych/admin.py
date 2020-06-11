from django.contrib import admin
from .models import Jstask, OneShotResponse, SingleTrialResponse

# Register your models here.
admin.site.register(Jstask)
admin.site.register(OneShotResponse)
admin.site.register(SingleTrialResponse)