from django.conf.urls import url
from .views import *

urlpatterns = [
    url('predict', predict.as_view()),
    url('uploadimage', upload_file.as_view()),
]