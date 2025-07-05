#!/usr/bin/env python
"""Django's command-line utility for administrative tasks with direct execution support."""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cy_website.settings')
import sys
from pathlib import Path

from django.core.management import execute_from_command_line
# 将YOLOv5的utils目录加入Python路径
yolov5_path = str(Path(__file__).parent / 'yolov5')  # 注意这里括号已闭合
if yolov5_path not in sys.path:
    sys.path.insert(0, yolov5_path)
def run_server():
    """启动开发服务器（默认8000端口）"""
    execute_from_command_line(['manage.py', 'runserver'])

def migrate_database():
    """执行数据库迁移"""
    execute_from_command_line(['manage.py', 'migrate'])

def create_super_user():
    """创建超级用户"""
    execute_from_command_line(['manage.py', 'createsuperuser'])

def main():
    """运行方式：
    python manage.py         → 启动服务器
    python manage.py migrate → 迁移数据库
    python manage.py createsuperuser → 创建超级用户
    """
    # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cy_website.settings")
    # for user in User.objects.all():
    #     Profile.objects.get_or_create(user=user)
    # 判断输入的参数
    if len(sys.argv) == 1:
        # 无参数时，默认运行服务器
        run_server()
    else:
        # 有参数时，根据参数决定模式
        command = sys.argv[1].lower()
        if command == "runserver":
            run_server()
        elif command == "migrate":
            migrate_database()
        elif command == "createsuperuser":
            create_super_user()
        else:
            # 其他命令：直接传给 Django
            execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
