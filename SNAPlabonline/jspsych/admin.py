from django.contrib import admin
from .models import (
	ConstStimTask, OneShotResponse,
	SingleTrialResponse, Study,
	RawTask, AdaptiveTask, OpenSpeechTask
	)

# Register your models here.
admin.site.register(AdaptiveTask)
admin.site.register(OpenSpeechTask)
admin.site.register(RawTask)
admin.site.register(ConstStimTask)
admin.site.register(OneShotResponse)
admin.site.register(SingleTrialResponse)
admin.site.register(Study)
