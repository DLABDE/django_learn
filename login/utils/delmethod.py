"""
删除组件
"""
from django.utils.safestring import mark_safe
import copy


class Delmethod(object):
    """
    删除组件_GET方法
    """

    def __init__(self, request, queryset, del_param='del'):
        """
        删除数据库数据
        :param request: 用户提交信息(来自前端)
        :param queryset: 被删除数据库表(UserInfo.objects)
        :param del_param: 前端删除参数名(&del=)
        """
        del_par = request.GET.get(del_param, '-1')  # 获取当前删除信息,没有则是'-1'
        self.del_param = del_param
        self.fix_req = copy.deepcopy(request.GET)  # 深拷贝
        self.fix_req._mutable = True  # 修改一下，使之允许改变request内容
        if del_par != '-1':  # 有输入
            if del_par.isdecimal():  # 为十进制数
                del_par = int(del_par)
                queryset.filter(id=del_par).delete()
                self.flag = 0  # 删除成功
        else:  # 输入无效
            self.flag = 1  # 删除失败

    def del_html(self):
        """
        获取删除按键的html
        :return: 删除按键的html
        """
        del_str = '?{}&{}'.format(self.fix_req.urlencode(), self.del_param)
        # <a href="{{ del_html }}={{ i.id }}">删除</a>
        return mark_safe(''.join(del_str))
