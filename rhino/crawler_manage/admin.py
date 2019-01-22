from django.contrib import admin
from .models import *

# Register your models here.


admin.site.register(Crawler)
admin.site.register(Task)
admin.site.register(SpiderServer)
admin.site.register(Project)
admin.site.register(ValidateRule)
admin.site.register(TaskServer)