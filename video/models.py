from django.db import models
from a_video.util.BaseModel import BaseModel


class Video(BaseModel):
    title = models.CharField('title', max_length=255)
    intro = models.CharField('视频简介', max_length=255, blank=True, null=True)
    video_file = models.FileField('视频文件', max_length=255)
    video_icon = models.CharField('预览图片', max_length=255, blank=True, null=True)
    play_time = models.CharField('播放时长', max_length=255, blank=True, null=True)
    play_times = models.IntegerField('播放次数', default=0)
    released = models.BooleanField('是否发布成功', default=False)
    author = models.ForeignKey('users.User', related_name='video', on_delete=models.CASCADE, verbose_name='视频发布者')

    class Meta:
        db_table = 'video'
        verbose_name = '所有视频'
        verbose_name_plural = verbose_name
        ordering = ['create_time']

    def __str__(self):
        return f'{self.title}: {self.intro}'
