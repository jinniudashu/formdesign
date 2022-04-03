from django.db import models
from django.forms.models import model_to_dict
from datetime import timedelta
import uuid
import re
from pypinyin import Style, lazy_pinyin

# 自定义管理器：设计数据备份、恢复
class HsscBackupManager(models.Manager):
    def backup_data(self):
        backup_data = []
        for item in self.all():
            item_dict = model_to_dict(item)

            # 遍历模型非多对多字段，如果是外键，则用外键的hssc_id替换外键id
            for field in self.model._meta.fields:
                # if item_dict[field.name] or field.__class__.__name__ == 'DurationField':  # 如果字段不为空或字段为DurationField类型，进行检查替换
                if item_dict[field.name]:  # 如果字段不为空或字段为DurationField类型，进行检查替换
                    if field.name in ['name_icpc', 'icpc']:  # 如果是ICPC外键，获取icpc_code
                        _object = field.related_model.objects.get(id=item_dict[field.name])
                        item_dict[field.name] = _object.icpc_code
                    else:
                        if (field.one_to_one or field.many_to_one):  # 一对一、多对一字段, 获取外键的hssc_id
                            _object = field.related_model.objects.get(id=item_dict[field.name])
                            item_dict[field.name] = _object.hssc_id
                        elif field.__class__.__name__ == 'DurationField':  # duration字段
                            item_dict[field.name] = str(item_dict[field.name])


            # 遍历模型多对多字段，用hssc_id或icpc_code替换外键id
            for field in self.model._meta.many_to_many:
                if item_dict[field.name]:  # 如果字段不为空，进行检查替换
                    # 先获取多对多字段对象的id List
                    _ids = []
                    for _field in item_dict[field.name]:
                        _ids.append(_field.id)
                    ids = []
                    for _object in field.related_model.objects.filter(id__in=_ids):
                        # 如果是ICPC外键，获取icpc_code，否则获取hssc_id
                        if field.name in ['name_icpc', 'icpc']:
                            ids.append(_object.icpc_code)
                        else:
                            ids.append(_object.hssc_id)
                    item_dict[field.name] = ids

            item_dict.pop('id')  # 删除id字段
            backup_data.append(item_dict)
        return backup_data

    def restore_data(self, data):
        if data is None or len(data) == 0:
            return 'No data to restore'

        print('开始恢复：', self.model.__name__)
        self.all().delete()
        for item_dict in data:
            item = {}
            # 遍历模型非多对多字段，如果是外键，则用外键的hssc_id找回关联对象
            for field in self.model._meta.fields:
                if item_dict.get(field.name):  # 如果字段存在且不为空，进行检查替换                    
                    if field.name in ['name_icpc', 'icpc']:  # 如果是ICPC外键，用icpc_code获取对象
                        _object = field.related_model.objects.get(icpc_code=item_dict[field.name])
                        item[field.name] = _object
                    else:
                        if (field.one_to_one or field.many_to_one):  # 一对一、多对一字段, 用hssc_id获取对象
                            try:
                                _object = field.related_model.objects.get(hssc_id=item_dict[field.name])
                            except field.related_model.DoesNotExist:  # ManagedEntity.base_form中的hssc_id可能为空
                                _object = None
                            item[field.name] = _object
                        elif field.__class__.__name__ == 'DurationField':  # duration字段
                            item[field.name] = parse_timedelta(item_dict[field.name])
                        else:
                            item[field.name] = item_dict[field.name]

            # 插入构造好的记录，不包括多对多字段
            _instance=self.model.objects.create(**item)

            # 遍历模型多对多字段，用hssc_id或icpc_code获取对象
            for field in self.model._meta.many_to_many:
                if item_dict.get(field.name):  # 如果字段不为空，进行检查替换
                    objects = []
                    # 如果是ICPC外键，用icpc_code获取对象，否则用hssc_id获取对象
                    if field.name in ['name_icpc', 'icpc']:
                        for _object in field.related_model.objects.filter(icpc_code__in=item_dict[field.name]):
                            objects.append(_object)
                    else:
                        for _object in field.related_model.objects.filter(hssc_id__in=item_dict[field.name]):
                            objects.append(_object)

                    # 将对象添加到多对多字段中
                    eval(f'_instance.{field.name}').set(objects)
            
        return f'{self.model} 已恢复'


# Hssc基类
class HsscBase(models.Model):
    label = models.CharField(max_length=255, null=True, verbose_name="名称")
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="name")
    hssc_id = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="hsscID")
    objects = HsscBackupManager()

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.label)

    def save(self, *args, **kwargs):
        if self.hssc_id is None:
            self.hssc_id = uuid.uuid1()
        super().save(*args, **kwargs)


class HsscPymBase(HsscBase):
    pym = models.CharField(max_length=255, blank=True, null=True, verbose_name="拼音码")

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.label:
            self.pym = ''.join(lazy_pinyin(self.label, style=Style.FIRST_LETTER))
            if self.name is None or self.name=='':
                self.name = "_".join(lazy_pinyin(self.label))
        super().save(*args, **kwargs)


# 转换string to timedelta
def parse_timedelta(stamp):
    if 'day' in stamp:
        m = re.match(r'(?P<d>[-\d]+) day[s]*, (?P<h>\d+):'
                     r'(?P<m>\d+):(?P<s>\d[\.\d+]*)', stamp)
    else:
        m = re.match(r'(?P<h>\d+):(?P<m>\d+):'
                     r'(?P<s>\d[\.\d+]*)', stamp)
    if not m:
        return ''

    time_dict = {key: float(val) for key, val in m.groupdict().items()}
    if 'd' in time_dict:
        return timedelta(days=time_dict['d'], hours=time_dict['h'],
                         minutes=time_dict['m'], seconds=time_dict['s'])
    else:
        return timedelta(hours=time_dict['h'],
                         minutes=time_dict['m'], seconds=time_dict['s'])