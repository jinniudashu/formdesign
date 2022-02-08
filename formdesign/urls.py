from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('define_dict/', include('define_dict.urls')),
    path('define_icpc/', include('define_icpc.urls')),
    path('define_operand/', include('define_operand.urls')),
]

admin.site.site_header = '智益医养服务供应链管理系统'
admin.site.site_title = 'HSSC'
admin.site.index_title = '业务设计系统'