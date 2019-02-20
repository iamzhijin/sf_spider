from django.urls import path
from . import views


urlpatterns = [
    path('', views.regist_html, name='regist_html'),
    path('regist/', views.regist, name='regist')
]
