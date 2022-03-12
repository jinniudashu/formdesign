from django.db import models
from django.forms.models import model_to_dict
import uuid

class Hssc(models.Model):
    label = models.CharField(max_length=255, blank=True, null=True, verbose_name="名称")
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="name")
    hssc_id = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="hsscID")

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.hssc_id is None:
            self.hssc_id = uuid.uuid1()
        super().save(*args, **kwargs)

    def backup_data(self):
        return {
            "hssc_id": self.hssc_id,
        }

    def restore_data(self, data):
        self.hssc_id = data["hssc_id"]
        self.save()