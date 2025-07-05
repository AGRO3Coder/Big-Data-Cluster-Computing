# cy_apps/urls.py
from django.urls import path
from .views import home, register, user_login, workspace, user_logout, detect_view  # 新增导入
from . import views
# app/urls.py
from django.urls import path
from .views import user_list
# 在项目的 urls.py 或应用的 __init__.py 中添加
from yolov5.models.yolo import DetectionModel
from .views import upload_view
from .views import connection_view
from .views import browse_view
from .views import hdfs_download_page

# 注册安全全局类
urlpatterns = [
    path('', home, name='home'),  # 原有路由
    path('accounts/register/', register, name='register'),
    path('accounts/login/', user_login, name='login'),
    path('accounts/workspace/', workspace, name='workspace'),
    path('accounts/logout/', user_logout, name='logout'),
    path('search/', views.search_view, name='search'),
    path('user/list/', views.user_list, name='user_list'),
    path('admin-panel/manage-permissions/', views.manage_user_permissions, name='manage_user_permissions'),
    path('profile/', views.profile, name='profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('detect/', detect_view, name='detect'),
    path('detect/', detect_view, name='detect_view'),
    path('hdfs_download.html', hdfs_download_page, name='hdfs_download'),

    path('upload.html', upload_view, name='upload'),
    path('connection.html', connection_view, name='connection'),
    path('browse.html', browse_view, name='browse'),

    path('image_preprocessing.html', views.image_preprocessing_view, name='image_preprocessing'),
    path('hdfs-statistics/', views.hdfs_statistics, name='hdfs_statistics'),
    path('cluster-connection/', views.cluster_connection, name='cluster_connection'),
    path('hdfs-upload/', views.hdfs_upload_view, name='hdfs-upload'),
    path('hdfs/test-connection/', views.test_hdfs_connection, name='test_hdfs_connection'),
    path('hdfs/get-files/', views.get_hdfs_files, name='get_hdfs_files'),
    path('hdfs/delete-file/', views.delete_hdfs_file, name='delete_hdfs_file'),
    path('hdfs-download/', views.hdfs_download_page, name='hdfs_download_page'),
    path('download-hdfs/', views.download_hdfs_file, name='download_hdfs_file'),  # 新的下载接口
    path('hdfs-file-download/', views.hdfs_file_download, name='hdfs_file_download'),
    # 新的状态查询接口
    path('hdfs-download-status/', views.hdfs_download_status, name='hdfs_download_status'),

]
