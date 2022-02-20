from django.db import models

# 字典列表
class DicList(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="字典表名")
    label = models.CharField(max_length=100, verbose_name="字典名称")
    related_field = models.CharField(max_length=100, verbose_name="关联字段")
    content = models.TextField(max_length=1024, null=True, blank=True, verbose_name="字典内容")

    def __str__(self):
        return str(self.label)

    class Meta:
        verbose_name = "字典列表"
        verbose_name_plural = "字典列表"


# 管理实体定义
class ManagedEntity(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Entity name")
    label = models.CharField(max_length=100, verbose_name="管理实体名称", null=True, blank=True)
    app_name = models.CharField(max_length=100, verbose_name="实体app名", null=True, blank=True)
    model_name = models.CharField(max_length=100, verbose_name="实体model名", null=True, blank=True)
    display_field = models.CharField(max_length=100, null=True, blank=True, verbose_name="显示字段")
    related_field = models.CharField(max_length=100, null=True, blank=True, verbose_name="关联字段")
    description = models.TextField(max_length=255, verbose_name="描述", null=True, blank=True)

    def __str__(self):
        return str(self.label)

    class Meta:
        verbose_name = "管理实体清单"
        verbose_name_plural = "管理实体清单"
