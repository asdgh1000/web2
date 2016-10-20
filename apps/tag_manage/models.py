from django.db import models
from ..base.models import BaseModel


class Tag(BaseModel):
    tag_name = models.CharField(max_length=20)
