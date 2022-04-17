"""
自定义中间件
"""
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect


class Sess_Midware(MiddlewareMixin):
    """
    登陆检验中间件
    """

    def process_request(self, request):  # 无返回值（None）则可通过
        """
        进入登陆检验
        """
        path = request.path_info  # 获取用户访问URL
        if path in ['/re_login/', '/reg/', '/index/', '/login/', '/vercode/','/re_reg/']:  # 排除不受检验的URL
            return None

        sess_inf = request.session.get('sess_info')  # 根据用户（cookie）获取存进去的登陆信息{sess_id=,sess_name=}
        if sess_inf is None:  # 没有cookie,没登陆过
            return redirect('/re_login/')

    def process_response(self, request, response):
        """
        出去登陆检验
        """
        return response
