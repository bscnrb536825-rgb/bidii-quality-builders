from django.urls import path
from . import views

app_name = 'project_app'

urlpatterns = [
    path('add_project/', views.add_project, name='add_project'),
    path('project_list/', views.project_list, name='project_list'),
]