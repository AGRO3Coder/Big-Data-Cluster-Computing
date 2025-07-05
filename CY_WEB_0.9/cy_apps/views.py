import os
import sys

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.urls import reverse
from yolov5.models.yolo import DetectionModel  # 假设你的模型类路径正确# 获取项目根目录（即 manage.py 所在的目录）
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 拼接 yolov5 路径
YOLOV5_DIR = os.path.join(BASE_DIR, 'yolov5')
sys.path.append(YOLOV5_DIR)

sys.path.insert(0, YOLOV5_DIR)                          # 把 yolov5 插入到 sys.path 的最前面


from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.decorators import login_required
from .models import Profile  # 新增：导入Profile模型


@login_required
def home(request):
    return render(request, 'home/main_board.html')


# cy_apps/views.py
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password1'])
            user.save()

            # 使用get_or_create确保Profile唯一
            nickname = form.cleaned_data.get('nickname', '')
            profile, created = Profile.objects.get_or_create(user=user)
            profile.nickname = nickname
            profile.save()

            is_admin = form.cleaned_data.get('is_admin', False)
            if is_admin:
                user.is_staff = True
                user.save()

            messages.success(request, f'注册成功！你好，{nickname}，请登录。')
            return redirect('login')
        else:
            # 打印详细错误信息（可选）
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form.fields[field].label}: {error}")
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


# 新增：登录视图
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, '登录成功！')
                return redirect('workspace')  # 登录后跳转工作页面
            else:
                messages.error(request, '用户名或密码错误！')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


# 新增：工作区视图（需登录）
@login_required
def workspace(request):
    return render(request, 'home/main_board.html')  # 工作页面模板路径


# 新增：登出视图
def user_logout(request):
    logout(request)
    messages.success(request, '已成功退出登录！')
    return redirect('login')


from django.http import HttpResponse


def search_view(request):
    query = request.GET.get('q', '')
    if query:
        results = []  # 你的查询逻辑
        return HttpResponse('')  # 返回空内容，没反应
    else:
        return HttpResponse('')  # 返回空内容，没反应


# app/views.py
from django.contrib.auth.models import User
from django.shortcuts import render


def user_list(request):
    # 获取所有用户对象
    users = User.objects.all()

    # 将用户对象传递给模板
    return render(request, 'home/user/user_list.html', {'users': users})


# cy_apps/views.py
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import uuid


# 仅允许超级管理员访问
def superuser_required(view_func):
    def check_perms(user):
        return user.is_superuser

    return user_passes_test(check_perms)(view_func)


@superuser_required
def manage_user_permissions(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')

        if user_id:
            user = get_object_or_404(User, id=user_id)

            # 处理权限变更
            if action in ['promote', 'demote']:
                user.is_staff = (action == 'promote')
                user.save()
                messages.success(request,
                                 f"已将用户 {user.username} {'提升为管理员' if action == 'promote' else '降为普通用户'}")

            elif action == "set_password" and request.user.is_superuser:
                new_password = request.POST.get("new_password")
                if new_password:
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, f"已为用户 {user.username} 设置新密码。")
                else:
                    messages.error(request, "新密码不能为空！")
            # 处理密码重置
            elif action == 'reset_password':
                # 生成重置令牌（实际项目中应使用Django内置密码重置功能）
                reset_token = uuid.uuid4().hex
                user.userprofile.reset_token = reset_token  # 假设Profile模型有reset_token字段
                user.userprofile.save()

                # 发送重置邮件（实际应使用Django的PasswordResetView）
                subject = '密码重置请求'
                message = f'点击链接重置密码: {settings.SITE_URL}/reset-password/{reset_token}/'
                from_email = settings.DEFAULT_FROM_EMAIL
                send_mail(subject, message, from_email, [user.email])

                messages.success(request, f"已向 {user.email} 发送密码重置邮件")

            # 处理用户删除
            elif action == 'delete':
                username = user.username
                user.delete()
                messages.success(request, f"已删除用户 {username}")

            return redirect('manage_user_permissions')

    users = User.objects.exclude(is_superuser=True).order_by('-is_staff', 'username')
    return render(request, 'home/admin/manage_user_permissions.html', {'users': users})


# cy_apps/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from django.contrib import messages


@login_required
def profile(request):
    if request.method == 'POST':
        # 关键：必须传递 instance=request.user
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '个人信息已成功更新！')
            return redirect('profile')
    else:
        # 关键：必须传递 instance=request.user
        form = UserProfileForm(instance=request.user)

    # 调试输出（临时添加，确认用户是否正确）
    print(f"当前用户: {request.user.username}, 是否管理员: {request.user.is_superuser}")

    return render(request, 'home/user/profile.html', {'form': form})


# cy_apps/views.py
from django.contrib.auth.forms import PasswordChangeForm  # 新增导入
from django.contrib.auth import update_session_auth_hash  # 新增导入
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def change_password(request):
    if request.method == 'POST':
        # 关键：传递 user=request.user
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # 保持用户登录状态
            update_session_auth_hash(request, form.user)
            messages.success(request, '密码已成功修改！')
            return redirect('profile')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'home/user/change_password.html', {'form': form})

#目标检测逻辑
import io
import os
import uuid
import base64
import cv2
import torch
import numpy as np
from django.conf import settings
from django.shortcuts import render
from yolov5.models.common import DetectMultiBackend
from yolov5.utils.augmentations import letterbox
from yolov5.utils.general import non_max_suppression, scale_boxes
from yolov5.utils.plots import Annotator, colors
from yolov5.utils.torch_utils import select_device

device = select_device('cpu')
imgsz = (640, 640)

# 用于获取类别名等（默认初始化一次 best.pt）
default_model_path = 'yolov5/runs/train/wild_detector2/weights/best.pt'
default_data_yaml = 'yolov5/dataset/data.yaml'
dummy_model = DetectMultiBackend(default_model_path, device=device, data=default_data_yaml)
dummy_model.eval()
names = dummy_model.names
stride = dummy_model.stride
MODEL_DIR = os.path.join('yolov5', 'runs', 'train', 'wild_detector2', 'weights')


def detect_view(request):
    image_data = None
    results_table = []
    selected_model = 'best.pt'

    # 获取静态图片列表
    img_dir = os.path.join(settings.STATICFILES_DIRS[0], 'assets', 'img', 'jpg')
    preset_images = sorted([f for f in os.listdir(img_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])

    # 获取模型列表
    model_files = [f for f in os.listdir(MODEL_DIR) if f.endswith('.pt')]

    # 处理模型上传
    if request.method == 'POST' and request.FILES.get('model_file'):
        model_file = request.FILES['model_file']
        if model_file.name.endswith('.pt'):
            fs = FileSystemStorage(location=MODEL_DIR)
            fs.save(model_file.name, model_file)
            return HttpResponseRedirect(reverse('detect_view'))
        else:
            return render(request, 'home/detect.html', {
                'error': '只支持上传 .pt 格式的模型文件',
                'model_files': model_files,
                'selected_model': selected_model,
                'preset_images': preset_images
            })

    # 处理检测请求
    if request.method == 'POST' and ('image' in request.FILES or 'preset_image' in request.POST):
        selected_model = request.POST.get('model', 'best.pt')
        model_path = os.path.join(MODEL_DIR, selected_model)

        # 获取图片数据
        if 'preset_image' in request.POST:
            # 处理预设图片
            preset_path = request.POST['preset_image']
            full_path = os.path.join(settings.STATICFILES_DIRS[0], preset_path)
            with open(full_path, 'rb') as f:
                image_bytes = f.read()
        else:
            # 处理上传图片
            uploaded_file = request.FILES['image']
            image_bytes = uploaded_file.read()

        # 读取图像为OpenCV格式
        np_arr = np.frombuffer(image_bytes, np.uint8)
        im0 = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # 加载模型
        model = DetectMultiBackend(model_path, device=device, data=default_data_yaml)
        model.eval()
        names = model.names

        # 图像预处理
        img = letterbox(im0, imgsz, stride=model.stride, auto=True)[0]
        img = img.transpose((2, 0, 1))[::-1]
        img = np.ascontiguousarray(img)
        img = torch.from_numpy(img).to(device).float() / 255.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # 推理与NMS
        pred = model(img)
        pred = non_max_suppression(pred, 0.25, 0.45)

        annotator = Annotator(im0.copy(), line_width=3, example=str(names), font_size=2)

        for det in pred:
            if len(det):
                det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], im0.shape[:2]).round()
                for *xyxy, conf, cls in reversed(det):
                    label = f'{names[int(cls)]} {conf:.2f}'
                    annotator.box_label(xyxy, label, color=colors(int(cls), True))

                    x1, y1, x2, y2 = map(int, xyxy)
                    w, h = x2 - x1, y2 - y1
                    results_table.append({
                        'class': names[int(cls)],
                        'conf': round(float(conf), 2),
                        'position': [x1, y1, w, h]
                    })

        result_img = annotator.result()
        _, buffer = cv2.imencode('.jpg', result_img)
        image_data = base64.b64encode(buffer).decode('utf-8')

    return render(request, 'home/detect.html', {
        'image_data': image_data,
        'results_table': results_table,
        'model_files': model_files,
        'selected_model': selected_model,
        'preset_images': preset_images,
        'show_results': image_data is not None
    })


from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm  # 新增导入
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils.hdfs_operations import HDFSClient
from django.views.decorators.csrf import csrf_protect
import tempfile
import os


def upload_view(request):
    return render(request, 'home/upload.html')


def connection_view(request):
    return render(request, 'home/connection.html')


def browse_view(request):
    return render(request, 'home/browse.html')


@login_required
def image_preprocessing_view(request):
    return render(request, 'home/image_preprocessing.html')


import json


def hdfs_statistics(request):
    # 初始化HDFS客户端
    hdfs_client = HDFSClient()

    # 获取文件类型统计数据
    success, file_types = hdfs_client.get_file_type_statistics()
    if not success:
        messages.error(request, f"获取文件类型统计失败：{file_types}")
        file_types = {}

    # 获取每日文件数量统计
    success, daily_counts = hdfs_client.get_daily_file_count()
    if not success:
        messages.error(request, f"获取每日文件统计失败：{daily_counts}")
        daily_counts = {}

    # 准备折线图数据（按日期排序）
    sorted_dates = sorted(daily_counts.keys())
    sorted_counts = [daily_counts[date] for date in sorted_dates]

    # 序列化数据
    file_types_json = json.dumps(file_types)
    daily_data_json = json.dumps({"dates": sorted_dates, "counts": sorted_counts})

    return render(request, 'home/hdfs_statistics.html', {
        'file_types_json': file_types_json,
        'daily_data_json': daily_data_json
    })


def cluster_connection(request):
    # 模拟集群状态数据
    node_status = {
        '活跃节点': 8,
        '备用节点': 2,
        '故障节点': 1
    }
    storage_data = {
        'dates': ['10:00', '11:00', '12:00', '13:00', '14:00'],
        'usage': [65, 68, 72, 70, 75]
    }
    connection_logs = [
        {'time': '14:05', 'status': '成功', 'message': '集群连接建立'},
        {'time': '14:10', 'status': '警告', 'message': '节点03负载过高'},
        {'time': '14:15', 'status': '成功', 'message': '自动扩容完成'}]
    # 序列化数据
    return render(request, 'home/cluster_connection.html', {
        'node_status': json.dumps(node_status),
        'storage_data': json.dumps(storage_data),
        'connection_logs': json.dumps(connection_logs)
    })


@csrf_exempt
def hdfs_upload_view(request):
    if request.method == 'POST':
        # 获取上传的文件
        uploaded_file = request.FILES.get('file')
        # 获取目标 HDFS 目录路径（前端应传入目录路径，如 /user/hdfs/upload/）
        hdfs_directory = request.POST.get('hdfs_path')

        if not uploaded_file:
            return JsonResponse({'error': '请选择要上传的文件'}, status=400)
        if not hdfs_directory:
            return JsonResponse({'error': '请指定 HDFS 目标目录'}, status=400)

        # 确保目录路径以斜杠结尾
        if not hdfs_directory.endswith('/'):
            hdfs_directory += '/'

        # 构建完整的 HDFS 文件路径（目录 + 原文件名）
        hdfs_file_path = hdfs_directory + uploaded_file.name

        # 保存到临时文件
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            for chunk in uploaded_file.chunks():
                temp_file.write(chunk)
            temp_path = temp_file.name

        try:
            # 使用 HDFS 客户端
            hdfs_client = HDFSClient()

            # 上传文件到计算的 HDFS 路径
            success, msg = hdfs_client.upload_file(temp_path, hdfs_file_path)

            if success:
                return JsonResponse({
                    'success': True,
                    'message': msg,
                    'hdfs_path': hdfs_file_path
                })
            else:
                return JsonResponse({'error': msg}, status=500)
        finally:
            # 无论成功失败，删除临时文件
            os.remove(temp_path)

    return JsonResponse({'error': '不支持的请求方法'}, status=405)


def test_hdfs_connection(request):
    # 使用单例的 HDFS 客户端
    hdfs_client = HDFSClient()
    success, message = hdfs_client.test_connection()
    return JsonResponse({'success': success, 'message': message})


def get_hdfs_files(request):
    """
    获取指定 HDFS 路径下的文件列表
    前端通过查询参数 ?path=xxx 传递路径
    """
    hdfs_path = request.GET.get('path', '/')  # 默认根路径，支持前端传自定义路径
    hdfs_client = HDFSClient()
    success, result = hdfs_client.list_files(hdfs_path=hdfs_path)
    if success:
        return JsonResponse({'success': True, 'files': result, 'current_path': hdfs_path})
    else:
        return JsonResponse({'success': False, 'message': result}, status=500)


@csrf_protect
def delete_hdfs_file(request):
    """删除 HDFS 文件/目录"""
    if request.method == 'POST':
        import json
        try:
            request_data = json.loads(request.body.decode('utf-8'))
            hdfs_path = request_data.get('file_path')
        except Exception as e:
            return JsonResponse({'success': False, 'message': '无效的请求格式'}, status=400)
        if not hdfs_path:
            return JsonResponse({'success': False, 'message': '请提供要删除的 HDFS 路径'}, status=400)
        hdfs_client = HDFSClient()
        success, result = hdfs_client.delete_file(hdfs_path)
        if success:
            return JsonResponse({'success': True, 'message': result})
        else:
            return JsonResponse({'success': False, 'message': result}, status=500)
    return JsonResponse({'success': False, 'message': '仅支持 POST 方法'}, status=405)


import os
from django.http import JsonResponse
from django.shortcuts import render
from hdfs import InsecureClient  # 确保已安装 hdfs 库：pip install hdfs


def hdfs_download_page(request):
    """渲染下载页面（包含前端表单、结果提示）"""
    return render(request, 'home/hdfs_download.html')


def download_hdfs_file(request):
    """处理 HDFS 文件下载逻辑，返回 JSON 响应"""
    hdfs_path = request.GET.get('hdfs_path')
    if not hdfs_path:
        return JsonResponse({'status': 'error', 'msg': 'HDFS 文件路径不能为空'}, status=400)

    # 替换为你的 HDFS 连接信息
    hdfs_client = InsecureClient(url='http://192.168.56.100:50070', user='root')
    local_base_path = r'C:\Users\86155\Desktop\new\CY_WEB_0.9\cy_apps\static\assets\img\jpg'
    filename = os.path.basename(hdfs_path)
    local_save_path = os.path.join(local_base_path, filename)

    try:
        # 检查文件是否存在
        if not hdfs_client.status(hdfs_path, strict=False):
            return JsonResponse({'status': 'error', 'msg': f'HDFS 文件不存在: {hdfs_path}'}, status=404)

        # 下载文件
        hdfs_client.download(hdfs_path, local_save_path, overwrite=True)
        return JsonResponse({'status': 'success', 'msg': '文件下载成功！'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'msg': f'下载失败: {str(e)}'}, status=500)


from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from hdfs import InsecureClient  # 导入InsecureClient
import os
import mimetypes
import logging

logger = logging.getLogger(__name__)


@require_http_methods(["GET"])
def hdfs_file_download(request):
    """处理HDFS文件下载请求，返回文件流触发浏览器下载"""
    hdfs_path = request.GET.get('hdfs_path', '').strip()

    if not hdfs_path:
        return JsonResponse({'status': 'error', 'msg': 'HDFS路径不能为空'}, status=400)

    try:
        # 关键修正：使用InsecureClient并指定正确的HTTP地址
        hdfs_client = InsecureClient(url='http://192.168.56.100:50070', user='root')
        logger.info(f"HDFS连接成功: {hdfs_client.url}")

        # 检查文件是否存在（使用HDFS路径）
        if not hdfs_client.status(hdfs_path, strict=False):
            return JsonResponse({'status': 'error', 'msg': f'文件不存在: {hdfs_path}'}, status=404)

        # 获取文件名用于下载
        file_name = os.path.basename(hdfs_path)
        logger.info(f"准备下载文件: {hdfs_path} -> {file_name}")

        # 打开HDFS文件流（使用HDFS路径，设置read=False表示获取文件流）
        with hdfs_client.read(hdfs_path, encoding=None, buffer_size=8192) as reader:
            # 创建HTTP响应对象
            content_type, _ = mimetypes.guess_type(file_name)
            response = HttpResponse(reader, content_type=content_type or 'application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            response['Content-Length'] = hdfs_client.status(hdfs_path)['length']
            return response

    except Exception as e:
        logger.error(f'HDFS文件下载异常: {str(e)}', exc_info=True)
        return JsonResponse({'status': 'error', 'msg': f'下载失败: {str(e)}'}, status=500)


@require_http_methods(["GET"])
def hdfs_download_status(request):
    """返回HDFS下载操作状态"""
    hdfs_path = request.GET.get('hdfs_path', '').strip()
    if not hdfs_path:
        return JsonResponse({'status': 'error', 'msg': 'HDFS路径不能为空'}, status=400)

    try:
        hdfs_client = InsecureClient(url='http://192.168.56.100:50070', user='root')
        file_status = hdfs_client.status(hdfs_path, strict=False)

        if file_status:
            return JsonResponse({
                'status': 'success',
                'msg': f'文件 {hdfs_path} 下载成功',
                'file_info': {
                    'name': os.path.basename(hdfs_path),
                    'size': file_status['length'],
                    'modified': file_status['modificationTime']
                }
            })
        else:
            return JsonResponse({'status': 'error', 'msg': f'文件不存在: {hdfs_path}'}, status=404)

    except Exception as e:
        logger.error(f'HDFS状态查询异常: {str(e)}', exc_info=True)
        return JsonResponse({'status': 'error', 'msg': f'查询失败: {str(e)}'}, status=500)