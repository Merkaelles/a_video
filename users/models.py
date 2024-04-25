from django.db import models
from django.contrib.auth.models import AbstractUser
from a_video.util.BaseModel import BaseModel


class User(AbstractUser, BaseModel):
    # username = models.CharField(max_length=255, verbose_name='用户名')  # AbstractUser中已定义，无需再定义
    phone = models.CharField('手机号码', max_length=11, unique=True)
    password = models.CharField('密码', max_length=255)
    sex = models.CharField('性别', max_length=10, blank=True, null=True)
    age = models.IntegerField('年龄', null=True, blank=True)
    nation = models.CharField('国籍', max_length=255, default='Austria', blank=True, null=True)
    user_icon = models.FileField('头像', max_length=255, default='33.jpg', blank=True, null=True)

    class Meta:
        db_table = 'user'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return f'{self.username}-{self.nation}'


class UserFollow(BaseModel):
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='用户')
    focus = models.ForeignKey('User', related_name='fan', on_delete=models.CASCADE, verbose_name='关注', null=True, blank=True)
    likes = models.OneToOneField('User', related_name='get_likes', on_delete=models.CASCADE, verbose_name='获赞', null=True, blank=True)

    class Meta:
        db_table = 'user_follow'
        verbose_name = '用户关注'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return f'{self.user}  关注: {self.focus} 获赞: {self.likes}'


class OperationLog(models.Model):
    ip = models.GenericIPAddressField('IP')
    method = models.CharField('请求方法', max_length=10)
    username = models.CharField('用户名', max_length=255)
    operate_time = models.DateTimeField('操作时间', auto_now_add=True)
    path = models.CharField('访问路径', max_length=255)
    duration = models.IntegerField('访问视图时间,ms', default=0)
    response_type = models.CharField('响应类型', max_length=255)
    status = models.IntegerField('响应状态码', default=200)
    is_success = models.BooleanField('响应是否成功', default=False)

    class Meta:
        db_table = 'operation_log'
        verbose_name = '操作日志'
        verbose_name_plural = verbose_name
        ordering = ['operate_time']