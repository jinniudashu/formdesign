from django.db import models
from define_operand.models import Project
# 备份模型抽象类
class BackupBase(models.Model):
    name = models.CharField(max_length=255, unique=True, null=True, verbose_name="版本")
    label = models.CharField(max_length=255, null=True, blank=True, verbose_name="版本名称")
    code = models.TextField(null=True, verbose_name="源代码")
    description = models.TextField(max_length=255, verbose_name="描述", null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")  

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.create_time)


# 设计数据备份
class DesignBackup(BackupBase):
    class Meta:
        verbose_name = "设计数据备份"
        verbose_name_plural = verbose_name
        ordering = ['id']


# ICPC数据备份
class IcpcBackup(BackupBase):
    class Meta:
        verbose_name = "ICPC数据备份"
        verbose_name_plural = verbose_name
        ordering = ['id']


# 输出脚本
class SourceCode(BackupBase):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, verbose_name="项目")

    class Meta:
        verbose_name = "作业系统脚本"
        verbose_name_plural = verbose_name
        ordering = ['id']