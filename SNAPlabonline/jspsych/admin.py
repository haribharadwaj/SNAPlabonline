from django.contrib import admin
from .models import (
	Task, OneShotResponse,
	SingleTrialResponse, Study
	)

# Register your models here.
admin.site.register(Task)
admin.site.register(OneShotResponse)
admin.site.register(SingleTrialResponse)
admin.site.register(Study)
