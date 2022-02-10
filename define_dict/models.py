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
