from django.db import models
from define_form.models import ManagedEntity, CombineForm
from pypinyin import lazy_pinyin


# 作业界面定义
class OperandView(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="name")
    label = models.CharField(max_length=255, blank=True, null=True, verbose_name="表单名称")
    managed_entity = models.ForeignKey(ManagedEntity, on_delete=models.CASCADE, null=True, blank=True, verbose_name="管理实体")
    forms = models.ForeignKey(CombineForm, on_delete=models.CASCADE, null=True, blank=True, verbose_name="组合视图")

    def __str__(self):
        return str(self.label)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f'{"_".join(lazy_pinyin(self.label))}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "作业"
        verbose_name_plural = "作业"
        ordering = ['id']


# 源代码库
class SourceCode(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="版本")
    label = models.CharField(max_length=255, verbose_name="版本名称", null=True, blank=True)
    description = models.TextField(max_length=255, verbose_name="描述", null=True, blank=True)
    code = models.TextField(verbose_name="源代码")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")  

    def __str__(self):
        return str(self.create_time)

    class Meta:
        verbose_name = "源代码"
        verbose_name_plural = "源代码"
        ordering = ['id']


