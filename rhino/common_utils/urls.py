
from django.conf.urls import url
from . import views


app_name = 'common_utils'

urlpatterns = [
    # Email接口
    url(r'^util/send_email$', views.Email_send, name='Email_send'),
    url(r'^code_ai$', views.code_ai)
]