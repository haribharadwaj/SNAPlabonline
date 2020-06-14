from django.contrib import admin
from .models import (
	Jstask, OneShotResponse, SingleTrialResponse,
	ObscureLink
	)

# Register your models here.

admin.site.register(Jstask)
admin.site.register(OneShotResponse)
admin.site.register(SingleTrialResponse)
admin.site.register(ObscureLink)
