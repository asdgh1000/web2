from django.db import models
from ..base.models import BaseModel


class User(BaseModel):
    name = models.CharField(max_length=50)
    passwd = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    img = models.CharField(max_length=255)
