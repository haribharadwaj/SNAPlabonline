from django.contrib import admin
from .models import (
	Jstask, OneShotResponse,
	SingleTrialResponse, Study,
	Jsrawtask
	)

# Register your models here.
admin.site.register(Jsrawtask)
admin.site.register(Jstask)
admin.site.register(OneShotResponse)
admin.site.register(SingleTrialResponse)
admin.site.register(Study)
