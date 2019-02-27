from django.urls import path
from . import views

app_name = "CrawlProject"
urlpatterns = [
    path('', views.ManageProject, name="ManageProject"),
    path('CreateProject/', views.CreateProject, name='CreateProject'),
    path('ProjectList/', views.ProjectList, name="ProjectList"),
    path('DeleteProject/', views.DeleteProject, name="DeleteProject"),
    path('UpdateProject', views.UpdateProject, name="UpdateProject"),
]