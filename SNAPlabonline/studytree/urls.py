from django.urls import path
from .views import (
	StudyCreateView, AddTaskView, AddBranchView,
	AddAltTaskView, AddAltBranchView, MyStudies,
	StudyDeleteView, experimenter_view, subject_view,
	)


urlpatterns = [
	path('create/', StudyCreateView.as_view(), name='study-create'),
	path('addtask/<int:parentpk>/', AddTaskView.as_view(), name='study-addtask'),
	path('addtask/alt/<int:parentpk>/', AddAltTaskView.as_view(), name='study-addtask-alt'),
	path('addbranch/<int:parentpk>/', AddBranchView.as_view(), name='study-addbranch'),
	path('addbranch/alt/<int:parentpk>/', AddAltBranchView.as_view(), name='study-addbranch-alt'),
	path('', MyStudies.as_view(), name='study-home'),
	path('run/<slug>/', subject_view, name='study-run'),
	path('viewedit/<slug>/', experimenter_view, name='study-viewedit'),
	path('<pk>/delete/', StudyDeleteView.as_view(), name='study-delete'),
	]