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


# 字典列表
# 删除多余字典：
# 1. 职员表
# 2. 注册登录（行政管理）
# 3. 治疗
# 4. 机构清单
# 5. 评估和诊断
# 6. 症状和问题
# 7. 药品清单
# 8. 服务角色

# 以上建立专用字段