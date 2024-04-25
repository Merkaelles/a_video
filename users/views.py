import random
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.http import require_http_methods
from .models import User, UserFollow


@require_http_methods(['POST'])
def check_username(request):
    username = request.POST.get('username')
    user = User.objects.filter(username=username)
    result_data = {'valid': True}
    if user:
        result_data['valid'] = False
    return JsonResponse(result_data)


@require_http_methods(['GET'])
def generate_code(request):
    # 定义变量 用于画面的背景颜色 、宽、 高
    bg_color = (random.randrange(20, 100), random.randrange(20, 100), random.randrange(100, 255))
    width = 120
    height = 38
    # 创建画面对象
    im = Image.new('RGB', (width, height), bg_color)
    # 创建画笔的颜色
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪声点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill == fill)

    # 定义验证码的备选值
    str1 = 'ABCDEFGHIJKLMNOPQRSTUVXYZ0123456789'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]

    # 绘制4个字
    # 构造字体对象 字体对象的路径：
    font = ImageFont.truetype('ebrima.ttf', 23)
    # 构造字体的颜色
    # fontcolor = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
    draw.text((5, -3), rand_str[0], font=font,
              fill=(random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)))
    draw.text((25, -3), rand_str[1], font=font,
              fill=(random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)))
    draw.text((50, -3), rand_str[2], font=font,
              fill=(random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)))
    draw.text((75, -3), rand_str[3], font=font,
              fill=(random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)))
    # 释放画笔
    del draw
    request.session['verify_code'] = rand_str
    # 内存文件操作
    buf = BytesIO()
    # 将图片保存在内存中 文件类型：png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端 MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')


@require_http_methods(['POST'])
def verify_code(request):
    code1 = request.POST.get('captcha')
    code2 = request.session.get('verify_code')
    result_data = {'valid': False}
    if code1 == code2:
        result_data['valid'] = True
    return JsonResponse(result_data)


@require_http_methods(['POST'])
def create_account(request):
    User.objects.create_user(username=request.POST['username'],
                             password=request.POST['password'],
                             email=request.POST['email'],
                             phone=request.POST['phone'],
                             sex=request.POST['sex']
                             )
    result_data = {'code': 200}
    return JsonResponse(result_data)


@require_http_methods(['POST'])
def submit_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    remember = int(request.POST.get('remember', '1'))  # 若没有get值,则设置为1
    user = auth.authenticate(request=request, username=username, password=password)  # 验证用户名和密码是否均正确
    if user:
        auth.login(request, user)  # 验证session_key
        request.session.set_expiry(remember * 86400)
        return redirect('/video/')
    return redirect('/user/login/')


@login_required(login_url='/user/login/')
def logout(request):
    auth.logout(request)
    return redirect('/user/login/')


class UserListView(LoginRequiredMixin, View):
    def get(self, request):
        page_num = request.GET.get('page', 1)
        users = User.objects.exclude(id=request.user.id)
        paginator = Paginator(users, 10)
        page_range = paginator.page_range
        try:
            page = paginator.page(page_num)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        focus_ids = UserFollow.objects.filter(user__id=request.user.id).values_list('focus__id', flat=True)
        return render(request, 'user_list.html', {
            'user_page': page, 'page_range': page_range, 'current_page': page_num, 'focus_ids': focus_ids
        })


@login_required(login_url='/user/login/')
def my_focus(request):
    focus_id = UserFollow.objects.filter(user__id=request.user.id).values_list('focus__id', flat=True)
    focus_list = User.objects.filter(id__in=focus_id).all()
    return render(request, 'focus.html', {'focus_list': focus_list})


@login_required(login_url='/user/login/')
def my_fans(request):
    fans_id = UserFollow.objects.filter(focus=request.user).values_list('user__id', flat=True)
    fans_list = User.objects.filter(id__in=fans_id).all()
    print(fans_list)
    return render(request, 'fans.html', {'fans_list': fans_list})


@require_http_methods(['GET'])
@login_required(login_url='/user/login/')
def add_focus(request):
    focus_id = request.GET.get('focus_id')
    focus = User.objects.get(id=focus_id)
    UserFollow.objects.create(user=request.user, focus=focus)
    return redirect('/user/userlist/')


@require_http_methods(['GET'])
@login_required(login_url='/user/login/')
def cancel_focus(request):
    focus_id = request.GET.get('focus_id')
    focus_user = User.objects.get(id=focus_id)
    UserFollow.objects.filter(user=request.user, focus=focus_user).delete()
    return redirect('/user/userlist/')


class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'user_info.html')

    def post(self, request):
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        age = request.POST.get('age')
        sex = request.POST.get('sex')
        nation = request.POST.get('nation')
        user_icon = request.FILES.get('user_icon', None)
        if not user_icon:
            return HttpResponse('未选中用户')
        user = request.user
        user.username = username
        user.phone = phone
        user.age = age
        user.sex = sex
        user.nation = nation
        user.user_icon = user_icon
        user.save()
        return self.get(request)


def change(request):
    user = User.objects.get(username='Luke')
    print(user.fan.all())
    return HttpResponse('清除成功')
