"""
分页组件
"""
from django.utils.safestring import mark_safe
import copy


class Pagination(object):
    """
    分页组件1
    """

    def __init__(self, request, queryset, page_param='pg', page_size=15, plus=5):
        """
        初始化页码组件
        :param request: 用户提交信息(来自前端)
        :param queryset: 数据库搜索结果(.objects.filter)
        :param page_param: 前端当前页参数名(&pg=)
        :param page_size: 每页显示条数
        :param plus: 显示的分页按钮个数
        """
        page = request.GET.get(page_param, '1')  # 获取当前页码信息,没有则是'1'
        if page.isdecimal():  # 为十进制数
            page = int(page)
        else:
            page = 1

        que_count = queryset.count()  # 总数目条数
        page_count, div = divmod(que_count, page_size)  # 计算除数余数
        if div:
            page_count += 1

        self.fix_req = copy.deepcopy(request.GET)  # 深拷贝
        self.fix_req._mutable = True  # 修改一下，使之允许改变request内容

        self.page_param = page_param  # 参数名
        self.page_count = page_count  # 总页码数
        self.page = page  # 当前页
        self.page_size = page_size  # 每页显示数目
        self.start = (page - 1) * page_size  # 当前页切片起点
        self.end = page * page_size  # 当前页切片终点
        self.page_queryset = queryset[self.start:self.end]  # 当前页内容
        self.plus = plus  # 分页按钮数

    def pag_html(self):
        """
        生成分页脚HTML(根据需求重写或修改)
        :return: 格式化html文本
        """

        self.fix_req.setlist(self.page_param, [self.page])  # 原基础上添加一个URL参数(&pg={page})
        # 当有搜索参数时能维持搜索状态不变

        page_str = list()
        page_str.append('<div><nav aria-label="Page navigation"><ul class="pagination">')
        for i in range(1, self.page_count + 1):
            self.fix_req[self.page_param] = i  # 每一个按钮都在原基础参数上添加个页码参数
            if i == self.page:
                page_str.append('<li class="active"><a href="?{}">{}</a></li>'.format(self.fix_req.urlencode(), i))
            else:
                page_str.append('<li><a href="?{}">{}</a></li>'.format(self.fix_req.urlencode(), i))
        page_str.append('</ul></nav></div>')
        return mark_safe(''.join(page_str))  # 解除保护，否则只输出文本效果（非html效果）
