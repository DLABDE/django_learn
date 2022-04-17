from django.http import JsonResponse
from django.core.validators import RegexValidator  # 正则化
from django.core.exceptions import ValidationError  # 抛出错误信息
from django.shortcuts import HttpResponse, redirect, render

from login import models
from login.models import UserInfo, Deparment, TaskInfo

# 导入表单
from login.login_forms.form import UseFrom, DepFrom, TaskForm
# 导入自定义组件
from login.utils.pagination import Pagination
from login.utils.delmethod import Delmethod
from login.utils.vercode import get_vercode


# from django.views.decorators.csrf import csrf_exempt


# 路由映射的处理函数

def index(request):
    """
    返回模板，默认APP注册顺序templates中找
    若'DIRS': [BASE_DIR / 'templates']，则先根目录找
    """
    # return HttpResponse('HI!') #返回HTML文本
    # return redirect('https://www.baidu.com')  #重定向
    web_title = '测试主界面'
    roles = ['DZD', '116382']
    a_list_pe = ['A', 'B', 'C']
    dict_test = {'name': '字典', 'val': 15}
    return render(request,
                  'index.html',
                  {
                      'title': web_title,
                      'creat': roles,
                      'lis': a_list_pe,
                      'dict_test': dict_test,
                  },
                  )  # f都需要返回request，在html可以取用{{ request.session.sess_info.sess_name}}(来自真·登陆函数)


def p_get(request):
    re_type = request.method  # 用户请求方式
    re_val = request.GET  # URL参数字典形式
    request.GET.urlencode()  # 字符串形式(n1=123&n2=321)
    # request.GET.get('n1')

    re_post = request.POST  # 请求体中数据
    print(re_type, re_val, re_post)
    return HttpResponse('HI!')


def login(request):
    """
    登陆界面
    """
    title = '登陆界面'
    if request.method == 'GET':
        # 注意HTML提交表单中加入{% csrf_token %}
        return render(request, 'login.html', {'title': title})
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        peo = UserInfo.objects.filter(name=username).first()
        if peo and peo.name == username and peo.password == password:
            return render(request, 'login.html', {'inf': '登陆成功', 'title': title})
        return render(request, 'login.html', {'inf': '登陆失败', 'title': title})


def reg(request):
    """
    注册界面
    """
    title = '注册界面'
    if request.method == 'GET':
        # 注意HTML提交表单中加入{% csrf_token %}
        return render(request, 'reg.html', {'title': title})
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        peo = UserInfo.objects.filter(name=username).first()

        if peo and peo.name == username:
            return render(request, 'reg.html', {'inf': '用户名已存在', 'title': title})

        UserInfo.objects.create(name=username, password=password)
        # return render(request, 'reg.html', {'inf': '注册成功', 'title': title})
        return redirect('/re_login/')  # 自动跳转


def admin_dj(request):
    """
    管理界面
    """
    title = '管理界面'
    data = UserInfo.objects.all().order_by('id')  # 选择排序方式 默认id 可以加负号反排序
    depa = Deparment.objects.all()  # 可以切片[0:10]
    del_peo = request.GET.get('del')
    del_ap = request.GET.get('del_ap')
    if request.method == 'GET':
        if del_ap:
            Deparment.objects.filter(id=del_ap).delete()
        if del_peo:
            UserInfo.objects.filter(id=del_peo).delete()
            # return redirect('/admin')
        return render(request, 'admin.html', {'inf': data, 'title': title, 'depa': depa})

    if request.method == 'POST':
        n1 = request.GET.get('pos')
        if n1 == '1':  # 添加人员
            username = request.POST.get('username')
            password = request.POST.get('password')
            deparment = int(request.POST.get('deparment'))
            peo = UserInfo.objects.filter(name=username).exists()  # 查找看是否存在
            if peo:
                return render(request, 'admin.html', {'inf': data, 'err': '用户已存在', 'title': title,
                                                      'depa': depa})
            UserInfo.objects.create(name=username, password=password, deparment_id=deparment)
            return render(request, 'admin.html', {'inf': data, 'err': '添加成功', 'title': title,
                                                  'depa': depa})
        if n1 == '2':  # 添加部门
            name = request.POST.get('name')
            peo = Deparment.objects.filter(title=name).exists()
            if peo:
                return render(request, 'admin.html', {'inf': data, 'err': '部门已存在', 'title': title,
                                                      'depa': depa})
            Deparment.objects.create(title=name)
            return render(request, 'admin.html', {'inf': data, 'err': '添加成功', 'title': title,
                                                  'depa': depa})


# ####################################### ModelForm版本
def admin_dj_mf(request):
    """
    使用MF的用户管理界面
    """
    # sess_inf = request.session.get('sess_info')  # 根据用户（cookie）获取存进去的登陆信息{sess_id=,sess_name=}
    # if sess_inf is None:    #没有cookie,没登陆过
    #    return redirect('/re_login/')

    title = '管理界面FM'
    form_pe = UseFrom()
    form_de = DepFrom()
    data = UserInfo.objects.all()
    depa = Deparment.objects.all()

    del_peo_obj = Delmethod(request, UserInfo.objects)
    del_peo_html = del_peo_obj.del_html()
    Delmethod(request, Deparment.objects, 'del_ap')

    page_pe_obj = Pagination(request, data, page_size=5)
    page_pe_html = page_pe_obj.pag_html()

    push_ms = {
        'err': '', 'title': title, 'form_pe': form_pe, 'form_de': form_de,
        'inf': page_pe_obj.page_queryset, 'depa': depa,
        'the_pag_html': page_pe_html, 'del_html': del_peo_html,
    }
    if request.method == 'GET':
        return render(request, 'admin_mf.html', push_ms)

    if request.method == 'POST':
        n1 = request.GET.get('pos')
        if n1 == '2':  # 添加部门
            form_de = DepFrom(data=request.POST)  # 取得数据放入FM
            if form_de.is_valid():  # 利用FM（见上文两处@@）进行校验，默认按照模板定义查能不能为空，否则提示错误(不能查重之类的)，可以class中临时添加校验条件
                # print(form.cleaned_data)#输出上传得到的信息
                # {'title': '财务部'}
                form_de.save()  # 自动将输入的东西存到数据库中
                # form_de.instance.creat_time='2022-4-8' #手动添加额外东西--> .字段=值
                push_ms['err'] = '添加成功'  # 校验成功
            else:
                push_ms['err'] = '添加失败'
                print(form_de.errors)
            push_ms['form_de'] = form_de
            return render(request, 'admin_mf.html', push_ms)
            # 如果校验失败此时form_de中已有错误信息{{ .errors.0 }}，可以利用它提示用户

        if n1 == '1':  # 添加人员
            form_pe = UseFrom(data=request.POST)
            if form_pe.is_valid():
                form_pe.save()
                push_ms['err'] = '添加成功'
            else:
                push_ms['err'] = '添加失败'
            push_ms['form_pe'] = form_pe
            return render(request, 'admin_mf.html', push_ms)


class UseFrom_edit(UseFrom):  # 继承
    """
    用户编辑MF，继承UseFrom，修改了校验规则
    """

    def clean_name(self):  # 重写clean_name，更新校验规则
        txt_n = self.cleaned_data['name']  # 获得用户传来信息
        the_id = self.instance.pk  # 当前编辑数据的主键(ID)
        if UserInfo.objects.filter(name=txt_n).exclude(id=the_id).exists():  # 除自己以外，还有重复的名字
            raise ValidationError('姓名重复')
        return txt_n  # 验证通过 返回用户输入的值


def admin_mf_edit(request, nid):
    """
    使用了MF的用户数据修改界面
    :param nid: 需修改用户信息的数据库ID
    :param request:
    """
    title = '用户编辑'
    r_obj = models.UserInfo.objects.filter(id=nid).first()  # 获取已存值
    if r_obj == None:  # 没找到
        return redirect('/admin/mf/')
    form_pe = UseFrom_edit(instance=r_obj)  # 读进去,用来作为默认显示值
    push_ms = {
        'title': title, 'err': '', 'form': form_pe,
    }
    if request.method == 'GET':
        return render(request, 'admin_mf_edit.html', push_ms)
    if request.method == 'POST':
        form_pe = UseFrom_edit(data=request.POST, instance=r_obj)  # 读进去，让他知道是修改
        if form_pe.is_valid():
            form_pe.save()  # 注意和instance=连用！！
            return redirect('/admin/mf/')
        else:
            push_ms['err'] = '修改失败'
            push_ms['form'] = form_pe
            return render(request, 'admin_mf_edit.html', push_ms)


# #################################################### FM

def search(request):
    """
    搜索界面
    """
    sea_text = request.GET.get('q')
    form_tk = TaskForm()

    del_obj = Delmethod(request, UserInfo.objects)
    del_html = del_obj.del_html()

    queryset = UserInfo.objects.filter(name__contains=sea_text)
    us_page_obj = Pagination(request, queryset, page_size=5)
    us_page_html = us_page_obj.pag_html()
    task_qur = TaskInfo.objects.filter(title__contains=sea_text)
    tk_page_obj = Pagination(request, task_qur, page_size=5)
    tk_page_html = tk_page_obj.pag_html()

    if sea_text:
        return render(request, 'search.html', {'title': '搜索结果', 'old_sch': sea_text,
                                               'inf': us_page_obj.page_queryset, 'the_pag_html': us_page_html,
                                               'del_html': del_html,
                                               'form_tk': form_tk, 'data_tk': tk_page_obj.page_queryset,
                                               'tk_pag_html': tk_page_html,
                                               })
    return redirect('/index')


# ##这里使用的是Form表单（低级一些,没链接数据库）(可以用钩子)
from django import forms


class Login_form(forms.Form):
    name = forms.CharField(label='用户名',
                           widget=forms.TextInput(attrs={'class': 'form-control'}),
                           required=True)  # required=True不能为空
    password = forms.CharField(min_length=6, max_length=16, label='密码',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}, render_value=True),
                               validators=[RegexValidator(r'^[A-Za-z]', '密码必须字母开头')]
                               )
    ver_code = forms.CharField(label='验证码',
                               widget=forms.TextInput(attrs={'class': 'form-control'}),
                               required=True)


# 也可以重写init，参考MF；但不能继承，两者父类不同


def re_login(request):
    """
    带会话的登陆
    """
    form = Login_form()
    if request.method == 'POST':
        form = Login_form(data=request.POST)
        if form.is_valid():  # 获得数据    #form没链接数据库 所以没有form.save()
            # print(form.cleaned_data)    #{'name': '杜章定', 'password': 'qqq'}

            user_code = form.cleaned_data.pop('ver_code')  # 要弹出，因为下文涉及数据库地方没有这个
            img_code = request.session.get('vercode', '')  # 获取真验证码
            if user_code.upper() != img_code.upper():
                form.add_error('ver_code', '验证码错误')
                return render(request, 're_login.html', {'form': form, 'title': '真·登陆界面'})

            sql_data = models.UserInfo.objects.filter(**form.cleaned_data).first()  # 取得数据库数据
            if not sql_data:  # 数据不存在，验证失败
                form.add_error('password', '用户名或密码错误')  # 添加错误信息
                return render(request, 're_login.html', {'form': form, 'title': '真·登陆界面'})
            # 验证通过
            request.session['sess_info'] = {'sess_id': sql_data.id,
                                            'sess_name': sql_data.name}  # 自动生成cookie返回给用户并写入数据库(django_session)，并添加用户信息（{sess_id=,sess_name=}）
            request.session.set_expiry(60 * 60 * 3)  # 重新设置超时时间3h（验证码哪里改过了，所以这里需要重置）
            # return HttpResponse('登陆成功')
            return redirect('/index/')
    return render(request, 're_login.html', {'form': form, 'title': '真·登陆界面'})


def re_reg(request):
    """
    新·注册
    """
    form = Login_form()  # 因为是一样的直接用了
    if request.method == 'POST':
        form = Login_form(data=request.POST)
        if form.is_valid():
            user_code = form.cleaned_data.pop('ver_code')
            img_code = request.session.get('vercode', '')
            if user_code.upper() != img_code.upper():
                form.add_error('ver_code', '验证码错误')
                return render(request, 're_reg.html', {'form': form, 'title': '注册界面'})

            data = form.cleaned_data
            peo = UserInfo.objects.filter(name=data['name']).first()
            if peo and peo.name == data['name']:
                form.add_error('name', '用户名已存在')
                return render(request, 're_reg.html', {'form': form, 'title': '注册界面'})
            UserInfo.objects.create(name=data['name'], password=data['password'])
            return redirect('/re_login/')
    return render(request, 're_reg.html', {'form': form, 'title': '注册界面'})


def logout(request):
    """
    注销会话
    """
    request.session.clear()
    return redirect('/index/')


def ver_code(request):
    """
    生成验证码
    """
    img, code = get_vercode()
    request.session['vercode'] = code  # 写入会话
    request.session.set_expiry(60)  # 超时时间60s
    return HttpResponse(img)


def aj(request):
    """
    AJ测试
    """
    return render(request, 'aj.html')


# @csrf_exempt  # 禁用csrf验证，否则需要加入{% csrf_token %}
def aj_test(request):
    """
    AJ测试
    """
    # print(request.GET)
    print(request.POST)
    data_sc = {'status': True, 'data': {'n1': 1, 'n2': 2}}
    # json_string=json.dumps(data_sc)#AJ一般都是返回json格式
    # return HttpResponse(json_string)
    return JsonResponse(data_sc)  # 自带方式返回JSON


def task_scale(request):
    """
    任务表
    """
    title = '任务清单'
    del_text = request.GET.get('d')
    edit_gettext = request.GET.get('ed')
    edit_getdata = request.GET.get('edit')

    data = TaskInfo.objects.all().order_by('-id')
    page_obj = Pagination(request, data, page_size=5)
    page_html = page_obj.pag_html()

    form = TaskForm()
    if edit_gettext:
        # 得到字典,.values_list()元组
        edit_data = TaskInfo.objects.filter(id=edit_gettext).values('title', 'content', 'creat_time', 'lev', 'per',
                                                                    'status').first()
        # {'title': '11', 'content': '11', 'creat_time': datetime.datetime(2022, 4, 15, 0, 0, tzinfo=datetime.timezone.utc), 'lev': 0, 'per': 13, 'status': 0}
        return JsonResponse({'status': True, 'edit_data': edit_data})
    if del_text:
        TaskInfo.objects.filter(id=del_text).delete()
        return JsonResponse({'status': True})
    if request.method == 'POST':
        form = TaskForm(data=request.POST)
        if edit_getdata:  # 编辑状态
            edit_obj = models.TaskInfo.objects.filter(id=edit_getdata).first()  # 获取已存值
            form = TaskForm(data=request.POST, instance=edit_obj)
        if form.is_valid():  # 成功
            form.save()
            return JsonResponse({'status': True})
        # 失败
        return JsonResponse({'status': False, 'err': form.errors})
    return render(request, 'task.html', {'title': title,
                                         'form': form,
                                         'data': page_obj.page_queryset,
                                         'the_pag_html': page_html,
                                         })


def chart(request):
    """
    图表展示
    """
    bar_text = request.GET.get('bar')
    if bar_text:
        title = '后台数据示例'
        xAxis = ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子']
        legend = ['销量', '业绩']
        series = [
            {
                'name': '销量',
                'type': 'bar',
                'data': [5, 20, 36, 10, 10, 20]
            },
            {
                'name': '业绩',
                'type': 'bar',
                'data': [7, 15, 43, 16, 20, 15]
            }
        ]
        return JsonResponse({'title': title, 'legend': legend, 'xAxis': xAxis, 'series': series})

    return render(request, 'chart.html')


from django.conf import settings


def percen(request):
    title = '个人中心'
    name = request.session.get('sess_info')['sess_name']
    id = request.session.get('sess_info')['sess_id']
    avatar = settings.MEDIA_URL + 'avatar/' + str(id) + '.jpg'  # media/avatar/13.jpg
    if request.method == 'POST':
        file_png = request.FILES.get('avatar')  # file_png.name 文件名
        with open('media/avatar/' + str(id) + '.jpg', mode='wb') as f:  # 文件是一点一点传上来的
            for i in file_png.chunks():
                f.write(i)

    return render(request, 'percen.html', {'title': title, 'name': name, 'avatar': avatar})
