from django.db import models

class Image(models.Model):
    imagefile = models.FileField(upload_to="image/%Y/%m/%d") # 파일을 image/yyyy/MM/dd 경로에 저장하겠다.
