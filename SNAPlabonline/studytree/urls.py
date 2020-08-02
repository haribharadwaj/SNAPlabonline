from django.urls import path
from .views import (
	StudyCreateView, AddTaskView, AddBranchView,
	AddAltTaskView, AddAltBranchView, MyStudies,
	StudyDeleteView, experimenter_view, subject_view,
	demo_view, pilot_view, progress_view,
	wrong_id, routing_fail, redirect_home
	)


urlpatterns = [
	path('create/', StudyCreateView.as_view(), name='study-create'),
	path('addtask/<int:parentpk>/', AddTaskView.as_view(), name='study-addtask'),
	path('addtask/alt/<int:parentpk>/', AddAltTaskView.as_view(), name='study-addtask-alt'),
	path('addbranch/<int:parentpk>/', AddBranchView.as_view(), name='study-addbranch'),
	path('addbranch/alt/<int:parentpk>/', AddAltBranchView.as_view(), name='study-addbranch-alt'),
	path('', MyStudies.as_view(), name='study-home'),
	path('run/<slug>/', subject_view, name='study-run'),
	path('demo/<slug>/', demo_view, name='study-demo'),
	path('pilot/<slug>/', pilot_view, name='study-pilot'),
	path('viewedit/<slug>/', experimenter_view, name='study-viewedit'),
	path('progress/<slug>/', progress_view, name='study-progress'),
	path('<pk>/delete/', StudyDeleteView.as_view(), name='study-delete'),
	path('wrongid/', wrong_id, name='study-wrongid'),
	path('routingfail/', routing_fail, name='study-routingfail'),
	path('redirecthome/', redirect_home, name='study-redirecthome')
	]