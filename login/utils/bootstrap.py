"""
BootStrap样式组件
"""

from django import forms


class BootStrapModelForm(forms.ModelForm):
    """
    写一个BootStrapModelForm类，不用每次都重写__init__改CSS,直接继承就行
    """

    def __init__(self, *args, **kwargs):  # 通过重写初始化函数，在其中修改每个对象的属性（注意！可能会丢失原来的东西）
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
                                      'placeholder': field.label,  # 统一加上placeholder属性
                                      }
