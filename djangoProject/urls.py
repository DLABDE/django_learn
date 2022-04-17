"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# APP路由文件
# from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings

# 导入APP
from login import views

# 这里添加路由
urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),  # 启用media

    # path('admin/', admin.site.urls),
    path('index/', views.index),  # 主界面
    path('pg/', views.p_get),  # 获取url参数
    path('login/', views.login),  # 登陆
    path('reg/', views.reg),  # 注册
    path('admin/', views.admin_dj),  # 管理员
    path('admin/mf/', views.admin_dj_mf),
    path('admin/<int:nid>/edit/', views.admin_mf_edit),  # <int:nid> 传入一个int参数 /admin/10/deit/ #函数中需要加参数(requests,nig)
    path('search/', views.search),  # 搜索
    path('re_login/', views.re_login),  # 带会话登陆
    path('re_reg/', views.re_reg),  # 新注册
    path('logout/', views.logout),  # 注销会话
    path('vercode/', views.ver_code),  # 验证码图片
    path('aj/', views.aj),  # 测试
    path('aj/test/', views.aj_test),  # 测试
    path('task/', views.task_scale),  # 任务表
    path('chart/', views.chart),  # 图表演示
    path('percen/', views.percen),  # 个人中心
]
