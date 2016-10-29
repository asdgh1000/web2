from django.db import models
from ..base.models import BaseModel


class Tag(BaseModel):
    tag_name = models.CharField(max_length=20)

    #标签的优先级
    priority = models.IntegerField(default=0, db_index=True)
