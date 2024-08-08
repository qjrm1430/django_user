from django.db import models

from user.models import Custom


# Create your models here.
class todo(models.Model):
    custom = models.ForeignKey(Custom, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title
