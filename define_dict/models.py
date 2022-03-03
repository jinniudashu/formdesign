from django.db import models
import uuid
from pypinyin import Style, lazy_pinyin

from define_icpc.models import Icpc

# 字典列表
class DicList(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="字典表名")
    label = models.CharField(max_length=100, verbose_name="字典名称")
    related_field = models.CharField(max_length=100, verbose_name="关联字段")
    pym = models.CharField(max_length=100, null=True, blank=True, verbose_name="拼音码")
    dic_id = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="字典ID")

    def __str__(self):
        return str(self.label)

    def save(self, *args, **kwargs):
        if self.dic_id is None:
            self.dic_id = uuid.uuid1()
        if self.label:
            self.pym = ''.join(lazy_pinyin(self.label, style=Style.FIRST_LETTER))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "字典列表"
        verbose_name_plural = "字典列表"

# 字典明细
class DicDetail(models.Model):
    diclist = models.ForeignKey(DicList, on_delete=models.CASCADE, blank=True, null=True, verbose_name="字典")
    item = models.CharField(max_length=255, verbose_name="值")
    icpc = models.ForeignKey(Icpc, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="ICPC")
    pym = models.CharField(max_length=255, blank=True, null=True, verbose_name="拼音码")
    item_id = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="字典项目ID")

    def __str__(self):
        return self.item

    def save(self, *args, **kwargs):
        if self.item_id is None:
            self.item_id = uuid.uuid1()
        if self.item:
            self.pym = ''.join(lazy_pinyin(self.item, style=Style.FIRST_LETTER))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "字典明细"
        verbose_name_plural = "字典明细"


# 管理实体定义
class ManagedEntity(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Entity name")
    label = models.CharField(max_length=100, verbose_name="管理实体名称", null=True, blank=True)
    app_name = models.CharField(max_length=100, verbose_name="实体app名", null=True, blank=True)
    model_name = models.CharField(max_length=100, verbose_name="实体model名", null=True, blank=True)
    display_field = models.CharField(max_length=100, null=True, blank=True, verbose_name="显示字段")
    related_field = models.CharField(max_length=100, null=True, blank=True, verbose_name="关联字段")
    description = models.TextField(max_length=255, verbose_name="描述", null=True, blank=True)
    entity_id = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="实体ID")

    def __str__(self):
        return str(self.label)

    def save(self, *args, **kwargs):
        if self.entity_id is None:
            self.entity_id = uuid.uuid1()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "管理实体清单"
        verbose_name_plural = "管理实体清单"
