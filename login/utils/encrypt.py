"""
MD5验证
"""
import hashlib

from django.conf import settings


def md5(data_string):
    """
    MD5加密
    :param data_string: 需要加密的字符串
    :return: 加密后的字符串
    """
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))  # 将settings.SECRET_KEY作为盐，如果盐不对，同一密码加密结果会不同
    obj.update(data_string.encode('utf-8'))  # 把字符串进行加密
    return obj.hexdigest()
