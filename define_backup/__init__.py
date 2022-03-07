from os import path
from django.apps import AppConfig


def get_current_app_name(file):
    return path.dirname(file).replace('\\', '/').split('/')[-1]
 

class AppVerboseNameConfig(AppConfig):
    name = get_current_app_name(__file__)
    verbose_name = u'备份和导出'


default_app_config = get_current_app_name(__file__) + '.__init__.AppVerboseNameConfig'