from django.contrib import admin
from .models import BaseNode, StudyRoot, TaskNode, BranchNode


# Register your models here.
admin.site.register(BaseNode)
admin.site.register(StudyRoot)
admin.site.register(TaskNode)
admin.site.register(BranchNode)