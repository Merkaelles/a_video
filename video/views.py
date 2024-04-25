import os
import subprocess

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from a_video import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from users.models import User
from .models import Video


def change(request):
    Video.objects.get(id=32).delete()
    return HttpResponse('clear all')


@login_required(login_url='/user/login/')
def index(request):
    return render(request, 'home.html')


class Release(LoginRequiredMixin, View):  # 视频类都要继承View
    def post(self, request):
        title = request.POST['title']
        intro = request.POST['intro']
        video_file = request.FILES['video']
        if not video_file:
            return HttpResponse('未选中文件')
        video = Video.objects.create(title=title, intro=intro, video_file=video_file, author=request.user,
                                     released=True)
        img_path = os.path.join(settings.BASE_DIR, 'media', f'{video.id}.jpg')
        video_player(video.id, video.video_file.path, img_path)
        return redirect('/video/videolist/mylist/')


def get_frame(cmd1, cmd2):
    flag1 = flag2 = False
    play_time = 0
    result1 = subprocess.run(cmd1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='GB18030', shell=True)
    result2 = subprocess.run(cmd2, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='GB18030', shell=True)
    if result1.returncode == 0:
        flag1 = True
        r1 = result1.stdout
        play_time = r1[:r1.find('.')]
        print(r1)
        print('已获取视频时长')
    else:
        print(result1.stderr)
        print('获取视频时长失败')
    if result2.returncode == 0:
        flag2 = True
        print('已成功截图')
    else:
        print(result2.stderr)
        print('截图失败')

    if flag1 and flag2:
        return True, int(play_time)
    else:
        return False, int(play_time)


def video_player(video_id, video_path, img_path):
    cmd1 = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 -i {video_path}'
    cmd2 = f'ffmpeg -ss 00:00:10 -i {video_path} -vframes 1 {img_path}'
    print(cmd1)
    print(cmd2)
    result = get_frame(cmd1, cmd2)
    print(result)
    if result[0]:
        img_name = os.path.basename(img_path)
        play_time = '%02d:%02d' % (int(result[1] / 60), result[1] % 60)
        Video.objects.filter(id=video_id).update(video_icon=img_name, play_time=play_time)


class VideoListView(LoginRequiredMixin, View):
    def get(self, request, operator):
        if operator == 'mylist':
            return self.my_video_list(request)
        elif operator == 'otherslist':
            return self.others_list(request)
        else:
            return HttpResponse('Jajajjajaja')

    def my_video_list(self, request):
        videos = Video.objects.filter(author=request.user, released=True)
        page_num = request.GET.get('page', 1)  # no page_num default 1
        paginator = Paginator(videos, 8)  # 每页最多显示8个视频
        try:
            page = paginator.page(page_num)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)  # paginator.num_pages 即是页数
        return render(request, 'video_list.html', {
            'video_page': page,
            'current_page': page.number,
            'page_range': paginator.page_range,
        })

    def others_list(self, request):
        uid = request.GET.get('uid')
        user = User.objects.get(id=uid)
        videos = Video.objects.filter(author__id=uid, released=True)
        return render(request, 'user_video_list.html', {
            'video_list': videos, 'author': user
        })


@login_required(login_url='/video/login/')
def play(request):
    vid = int(request.GET.get('id'))
    video = Video.objects.get(id=vid)
    Video.objects.filter(id=vid).update(play_times=video.play_times + 1)
    return JsonResponse({'data': 'OK'})


@login_required(login_url='/video/login/')
def delete(request):
    vid = int(request.GET.get('id'))
    video = Video.objects.get(id=vid).delete()
    return redirect('/video/videolist/mylist/')
