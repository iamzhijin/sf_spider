"""rhino URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from django.views.generic import TemplateView

from . import views
from . import views


urlpatterns = [
    url(r'^web_monitor/',include('web_monitor.urls',namespace='web_monitor')),
    url(r'^common_utils/',include('common_utils.urls',namespace='common_utils')),
    url(r'^manual_crawler/', include('manual_crawler.urls',namespace='manual_crawler')),
    url(r'^crawler_manage/', include('crawler_manage.urls')),
    url(r'^monitor/', include('monitor.urls',namespace='monitor')),
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^overview$', views.overview, name='overview'),
    # url(r'^monitor$', TemplateView.as_view(template_name="index.html")),
    url(r'^download/(?P<file_name>.*)$', views.file_download, name='file_download'),

]
