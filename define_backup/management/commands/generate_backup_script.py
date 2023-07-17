from django.core.management import BaseCommand
from django.apps import apps


class Command(BaseCommand):
    help = 'Restore design data from backuped json file'

    def handle(self, *args, **options):
        # 需要备份的app
        backup_apps = ['define', 'define_backup', 'define_icpc', 'define_operand']
        # 需要备份的模型
        backup_models = ["auth.User", "auth.Group",]
        # 获取所有app中的所有模型
        for app in backup_apps:
            service_app_config = apps.get_app_config(app)
            for model in service_app_config.get_models():
                backup_models.append(f"{app}.{model._meta.object_name}")
        # 生成命令
        backup_command = f"python manage.py dumpdata {' '.join(backup_models)} --output=./backup/backup.json"

        # 保存到文件
        with open("backup.py", "w", encoding='utf-8') as file:
            file.write(f"import os\nos.system('{backup_command}')\n\n# 恢复数据命令：\n# python manage.py loaddata ./backup/backup.json")
