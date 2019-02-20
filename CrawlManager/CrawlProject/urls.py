from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProjectList, name="ProjectList"),
    path('CreateProject/', views.CreateProject, name='CreateProject'),
    path('ProjectList/', views.ProjectList, name="ProjectList"),

]