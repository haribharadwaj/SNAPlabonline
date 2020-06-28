from django.urls import include, path
from .views import StudyCreateView, AddTaskView, AddBranchView


urlpatterns = [
	path('/create/', StudyCreateView.as_view(), 'study-create'),
	path('/addtask/<studyslug>/', AddTaskView.as_view(), 'study-addtask'),
	path('/addbranch/<studyslug>/', AddBranchView.as_view(), 'study-addbranch')
	]