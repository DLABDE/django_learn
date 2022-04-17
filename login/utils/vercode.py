"""
验证码
"""
import gvcode
from io import BytesIO


def get_vercode():
    """
    生成验证码图片与对应字符串
    :return: 图片，字符串
    """
    s, v = gvcode.generate()  # 序列解包，获得图片和对应字符串
    # s.show() #显示生成的验证码图片
    simg = BytesIO()
    s.save(simg, 'png')  # 生成文件，不过是存内存中的
    return simg.getvalue(), v
