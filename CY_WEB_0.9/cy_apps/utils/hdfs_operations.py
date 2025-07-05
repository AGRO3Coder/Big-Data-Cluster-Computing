import os
import datetime
from hdfs import InsecureClient

class HDFSClient:
    _instance = None  # 用于存储单例实例

    def __new__(cls, host='192.168.56.100', port=50070, user='root'):
        # 如果实例不存在，则创建新实例；如果已存在，直接返回现有实例
        if not cls._instance:
            cls._instance = super(HDFSClient, cls).__new__(cls)
            # 初始化客户端
            cls._instance.client = InsecureClient(url=f'http://{host}:{port}', user=user)
        return cls._instance

    def test_connection(self):
        try:
            self.client.status('/')
            return True, "连接成功"
        except Exception as e:
            return False, f"连接失败：{str(e)}"

    def upload_file(self, local_path, hdfs_path):
        """
        上传本地文件到 HDFS
        :param local_path: 本地文件路径（临时文件路径）
        :param hdfs_path: HDFS 目标路径（如 /user/root/upload/xxx.txt）
        """
        try:
            # 检查并创建 HDFS 父目录
            hdfs_dir = '/'.join(hdfs_path.split('/')[:-1])
            if not self.client.status(hdfs_dir, strict=False):
                self.client.makedirs(hdfs_dir)

            # 执行上传
            self.client.upload(hdfs_path, local_path, overwrite=True)
            return True, "文件上传成功"
        except Exception as e:
            return False, str(e)

    def list_files(self, hdfs_path='/'):
        """列出指定路径下的文件和目录"""
        try:
            contents = self.client.list(hdfs_path, status=True)
            file_list = [item[0] for item in contents]
            return True, file_list
        except Exception as e:
            return False, str(e)

    def get_file_type_statistics(self, hdfs_path='/'):
        """
        统计指定路径下的文件类型分布
        :param hdfs_path: HDFS 目标路径（默认根目录）
        :return: 成功返回 {文件类型: 数量} 字典，失败返回空字典和错误信息
        """
        try:
            # 获取所有文件状态（包括目录）
            contents = self.client.list(hdfs_path, status=True)
            type_counts = {}

            for file_info in contents:
                file_name = file_info[0]
                file_status = file_info[1]

                # 跳过目录
                if file_status['type'] == 'DIRECTORY':
                    continue

                # 提取文件扩展名（类型）
                _, ext = os.path.splitext(file_name)
                file_type = ext.lower() if ext else '无扩展名'

                # 统计数量
                type_counts[file_type] = type_counts.get(file_type, 0) + 1

            return True, type_counts
        except Exception as e:
            return False, str(e)

    def get_daily_file_count(self, hdfs_path='/'):
        """
        统计指定路径下每日新增的文件数量
        :param hdfs_path: HDFS 目标路径（默认根目录）
        :return: 成功返回 {日期: 数量} 字典（日期格式YYYY-MM-DD），失败返回空字典和错误信息
        """
        try:
            # 获取所有文件状态（包括目录）
            contents = self.client.list(hdfs_path, status=True)
            daily_counts = {}

            for file_info in contents:
                file_name = file_info[0]
                file_status = file_info[1]

                # 跳过目录
                if file_status['type'] == 'DIRECTORY':
                    continue

                # 获取文件修改时间（HDFS返回的是毫秒级时间戳）
                mod_time = file_status['modificationTime']
                if mod_time == 0:
                    continue  # 跳过无时间戳的文件

                # 转换为日期字符串（YYYY-MM-DD）
                date = datetime.datetime.fromtimestamp(mod_time / 1000).strftime('%Y-%m-%d')

                # 统计数量
                daily_counts[date] = daily_counts.get(date, 0) + 1

            return True, daily_counts
        except Exception as e:
            return False, str(e)

    def delete_file(self, hdfs_path):
        print(f"[HDFS DEBUG] 正在删除路径: {hdfs_path}")
        # 添加递归删除和路径验证
        if not hdfs_path.startswith('/'):
            return False, "HDFS路径必须以/开头"
        """
        删除 HDFS 上指定路径的文件或目录
        :param hdfs_path: 要删除的 HDFS 路径
        :return: 成功返回 True 和提示信息，失败返回 False 和错误信息
        """
        try:
            self.client.delete(hdfs_path, recursive=True)
            return True, "文件/目录删除成功"
        except Exception as e:
            return False, str(e)

    def download_file(self, hdfs_path, local_path):
        try:
            status = self.client.status(hdfs_path, strict=True)
            if status['type'] == 'DIRECTORY':
                return False, "指定的 HDFS 路径是目录，无法直接下载，请确认路径为文件路径"
            local_dir = os.path.dirname(local_path)
            if local_dir and not os.path.exists(local_dir):
                os.makedirs(local_dir)
            self.client.download(hdfs_path, local_path, overwrite=True)
            return True, "文件下载成功"
        except Exception as e:
            return False, str(e)