from django.urls import include, path
from .views import (
	StudyCreateView, AddTaskView, AddBranchView,
	AddAltTaskView, AddAltBranchView,
	ExperimenterView, SubjectView
	)


urlpatterns = [
	path('/create/', StudyCreateView.as_view(), 'study-create'),
	path('/run/<studyslug>/', SubjectView.as_view(), 'study-run'),
	path('/viewedit/<studyslug>/', ExperimenterView.as_view(), 'study-viewedit'),
	path('/addtask/<int:parentpk>/', AddTaskView.as_view(), 'study-addtask'),
	path('/addtask/alt/<int:parentpk>/', AddAltTaskView.as_view(), 'study-addtask-alt'),
	path('/addbranch/<int:parentpk>/', AddBranchView.as_view(), 'study-addbranch'),
	path('/addbranch/alt/<int:parentpk>/', AddAltBranchView.as_view(), 'study-addbranch-alt')
	]