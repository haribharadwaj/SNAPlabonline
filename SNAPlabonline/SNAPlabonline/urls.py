"""SNAPlabonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from tasks import views as task_views
from jspsych import views as jspsych_views
from users import views as users_views
from jspsych.views import (
    TaskListView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView
    )


urlpatterns = [
	path('', task_views.index, name='tasks-home'),
	# path('createtask/', task_views.create_task, name='create-task'),
    path('task/new/', TaskCreateView.as_view(), name='create-task'),
    path('task/<pk>/update/', TaskUpdateView.as_view(), name='update-task'),
	path('task/run/<taskurl>/', jspsych_views.run_task, name='run-task'),
    path('task/results/<taskurl>/', jspsych_views.download_task_results, name='download-results'),
    path('mytasks/', TaskListView.as_view(), name='mytasks'),
    path('task/<pk>/delete/', TaskDeleteView.as_view(), name='delete-task'),
    path('labmembers/', task_views.for_lab_members, name='tasks-labmembers'),
	path('register/', users_views.register, name='users-register'),
    # path('newsubject/<path:next>/', users_views.subject_entry, name='subject-entry'),
    path('newsubject/', users_views.subject_entry, name='subject-entry'),
    # path('consent/<path:next>/', users_views.subject_consent, name='consent'),
    path('consent/', users_views.subject_consent, name='consent'),
    path('coresurvey/', users_views.core_survey, name='core-survey'),
	path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
	path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/',
        auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),
        name='password_reset'),
    path('password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
        name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
        name='password_reset_confirm'),
    path('password-reset-complete/done/',
        auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
        name='password_reset_complete'),
    path('admin/', admin.site.urls),
    path('savejspdata/', jspsych_views.create_OneShotResponse, name='savejspdata'),
    path('savejsptrial/', jspsych_views.create_TrialResponse, name='savejsptrial'),
    path('study/', include(studytree.urls))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
