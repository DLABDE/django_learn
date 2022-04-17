"""
login APP 的 ModelForm
"""
from django import forms
from django.core.validators import RegexValidator  # 正则化
from django.core.exceptions import ValidationError

from login import models
from login.utils.bootstrap import BootStrapModelForm


# from login.utils.encrypt import md5


class UseFrom(forms.ModelForm):
    """
    用户ModelForm
    """

    def __init__(self, *args, **kwargs):  # 通过重写初始化函数，在其中修改每个对象的属性（注意！可能会丢失原来的东西)
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            # print(name, field)
            # if name=='password':#可以选择性操作
            #    continue
            if field.widget.attrs:  # 如果本来就有东西，就只添加
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = field.label
            else:
                field.widget.attrs = {'class': 'form-control',  # 统一加上css样式
                                      'placeholder': field.label,
                                      }

    password = forms.CharField(  # @@ 设置更多通用校验规则（在models基础上添加
        min_length=6, max_length=16, label='密码',  # disabled=True 不可编辑
        widget=forms.PasswordInput(render_value=True),  # 写这里也可以！#插件为forms.PasswordInput
        # render_value=True,如果需要重新提交，不会删除密码
        validators=[RegexValidator(r'^[A-Za-z]', '密码必须字母开头')]
    )  # validators正则规则

    class Meta:
        """
        labels = None           #提示信息 相当于verbose_name
        help_texts = None       #帮助提示信息
        error_messages = None   #自定义错误信息
        exclude                 #需要排除的
        """
        # 写法都和下文widgets={}一样

        model = models.UserInfo
        fields = ('name', 'password', 'gender', 'deparment', 'creat_time')  # 默认是forms.TextInput插件
        # fields='__all__'    #获取所有
        widgets = {  # 插件
            'name': forms.TextInput(attrs={'class': 'form-control'}),  # 手动单个加入css样式(属性：值)
            # 'password': forms.PasswordInput(attrs={'class': 'form-control'}),  # init中已经加入css所以不加也行(或者再在这里进行覆盖)
        }
        # <input type="text" class="form-control" name="username" placeholder="用户名"/> {{ form.0 }}
        # name = request.POST.get('username')需要有name="username",使用FM时不需要这种东西

    # 定义检查规则 clean_字段(fields定义的)
    def clean_name(self):  # @@ 也可以使用自己的规则(钩子)
        txt_n = self.cleaned_data['name']  # 获得用户传来信息
        # 以下为检验算法
        if models.UserInfo.objects.filter(name=txt_n).exists():  # 验证不通过
            raise ValidationError('姓名重复')  # 抛出错误信息给用户,不进行下一步（不提交到数据库）
        return txt_n  # 验证通过 返回用户输入的值(不同情况也可以给不同的东西)   #给到了form.cleaned_data,然后存入数据库
        # 这个return的值会互相影响，不是串行方式，是同时的  别的clean中用到的值就是别的return的和顺序没关系

    # def clean_password(self):   #密码校验
    #    pwd = self.cleaned_data['password']
    #    return md5(pwd) #进行加密再放入数据库（不可解密，只能对比来验证是否正确）


class DepFrom(BootStrapModelForm):  # 继承BootStrapModelForm(相当于上文重写了__init__),对比class UseFrom(forms.ModelForm)
    """
    部门ModelForm
    """

    class Meta:
        model = models.Deparment
        fields = {'title'}


class TaskForm(BootStrapModelForm):
    """
    任务单MF
    """

    class Meta:
        model = models.TaskInfo
        fields = '__all__'  # 获取所有

    def clean_title(self):
        """
        任务名校验
        """
        txt_n = self.cleaned_data['title']
        the_id = self.instance.pk
        if models.TaskInfo.objects.filter(title=txt_n).exclude(id=the_id).exists():  # 除自己以外，还有重复的名字
            raise ValidationError('任务名重复')
        return txt_n  # 验证通过 返回用户输入的值
