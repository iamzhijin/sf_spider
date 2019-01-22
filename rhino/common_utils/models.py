from django.db import models

# Create your models here.

class Code_AI(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    succeed = models.CharField(max_length=200)
    result = models.CharField(max_length=200)
    image_binary = models.TextField()

    class Meta:
        db_table = "code_ai"