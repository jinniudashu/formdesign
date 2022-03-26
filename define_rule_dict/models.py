from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
import uuid
from pypinyin import lazy_pinyin

from formdesign.hsscbase_class import HsscBase
from define.models import Component


