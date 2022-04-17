from django.db import models

# 数据库表操作

# 提交到数据库(将这里的操作同步到数据库，此改则改,直接改数据库会丢步)
# python manage.py makemigrations
# python manage.py migrate

'''
    会自动创建一个表，名字为[APP_类名（小写）]
    create table login_userinfo(
            id bigint auto_increment primary key,(Django自动添加，自加主键id)
            name varchar(32),
            password varchar(64),
            age int
    )
    '''


class Deparment(models.Model):
    """
    部门表 login_deparment
    """
    title = models.CharField(max_length=16, verbose_name='部门')

    def __str__(self):  # print(对象) 会显示__str__(这里是title的verbose_name) 而不是一堆信息
        return self.title  # 在FM中链接表过来时能显示名字


class UserInfo(models.Model):
    """
    用户表 login_userinfo
    """

    # 默认不能为空;null=True,blank=True;可以为空
    # verbose_name 注解 html中{{ .label }}
    name = models.CharField(max_length=32, verbose_name='姓名')  # 字符串类型,max_length必须写
    password = models.CharField(max_length=64, verbose_name='密码')
    age = models.IntegerField(null=True, blank=True, verbose_name='年龄')  # 整形
    # models.BigAutoField长整形 #models.AutoField整形 #models.SmallIntegerField短整形
    account = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='余额')  # 小数，总长10，小数位2，默认值为0
    creat_time = models.DateTimeField(verbose_name='创建时间', null=True, blank=True)  # 9999-12-31 23:59:59
    # html获取格式化时间 {{ i.creat_time|date:"Y-m-d H:i:s" }}#models.DateField#只有年月日

    deparment = models.ForeignKey(to='Deparment', to_field='id', null=True, blank=True,
                                  on_delete=models.SET_NULL,
                                  verbose_name='部门')  # 表连接 有约束 链接到Deparment表的id列 django生成表时会变成deparment_id
    # 链接表被删时 on_delete=models.CASCADE级联删除  models.SET_NULL置空
    # 获取它的内容i.deparment_id
    # peo = UserInfo.objects.filter(name=username).first()
    # peo.deparment_id-->id
    # peo.deparment-->(对象)  Django会自动处理得到值
    # peo.deparment.title-->'市场营销'
    # html中{{ i.deparment.title }}

    gender_choices = ((0, '男'), (1, '女'))
    # 获取它的内容
    # peo = UserInfo.objects.filter(name=username).first()
    # peo.gender-->0
    # peo.get_gender_display()-->'男'  Django会自动处理得到值
    # html中 {{ i.get_gender_display }}
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choices, default=0)  # 设置约束选择

    def __str__(self):
        return self.name


# 以下需要执行，可以from-import这个类在views.py中运行

# 添加数据
# insert into login_userinfo(name)values("DZD")
# UserInfo.objects.create(name='DZD',password='123321',age=20)

# 获取数据
# 返回列表 [QuerySet类型,...]
# data_list=UserInfo.objects.all()
# data_list[0].id
# UserInfo.objects.filter(id=1)[0].name
# UserInfo.objects.filter(id=1,name='XXX').first().password
# 可以使用字典方式查找 sch_di={'name':'XXX','id__gt=1':1}  #字典为空则获取所有
# UserInfo.objects.filter(**sch_di).first()
# UserInfo.objects.filter(id__gt=1,name__startswith='XXX')
# 【字段名__XXX】id__gt=1查找id>1的 id__gte=1查找id>=1的  （小于：lt）
# 【字段名__XXX】 name__startswith='XX'查找以此开头的 name__endswith查找以此结尾的 name__contains包含的


# 删除数据
# 筛选加删除
# UserInfo.objects.filter(name='AAA').delete()
# UserInfo.objects.all().delete()    #全删

# 更新数据
# UserInfo.objects.filter(id=1).update(name='AA')

class TaskInfo(models.Model):
    """
    任务表
    """
    title = models.CharField(max_length=16, verbose_name='任务名称')
    content = models.TextField(verbose_name='任务内容')
    creat_time = models.DateTimeField(verbose_name='创建时间', null=True, blank=True)
    lev_choices = ((0, '正常'), (1, '紧急'), (2, '迫切'))
    lev = models.SmallIntegerField(verbose_name='级别', choices=lev_choices, default=0)
    per = models.ForeignKey(to='UserInfo', to_field='id', null=True, blank=True,
                            on_delete=models.SET_NULL,
                            verbose_name='负责人')
    status_choices = ((0, '未完成'), (1, '完成'), (2, '丢弃'))
    status = models.SmallIntegerField(verbose_name='完成情况', choices=status_choices, default=0)

    #MF中  (FORM当然也可以，不过就只有验证功能) #需要先配置media(settings.py urls.py)
    # file_jpg=forms.FileField()        #还支持文件上传
    # form = CLASS(data=request.POST, files=request.FILES, uplode_to='avatar/')
    # form.save时文件自动保存到media下的avatar
    # 还会将地址写入数据库（file_jpg字段）
