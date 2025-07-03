from hdfs import InsecureClient
from django.conf import settings

class HDFSOperator:
    def __init__(self):
        self.client = InsecureClient(
            f'http://{settings.HDFS_NAMENODE}:{settings.HDFS_PORT}',
            user=settings.HDFS_USER
        )

    def upload_file(self, local_path, hdfs_path):
        """上传本地文件到HDFS"""
        try:
            self.client.upload(hdfs_path, local_path)
            return True, "上传成功"
        except Exception as e:
            return False, f"上传失败: {str(e)}"

    def delete_path(self, hdfs_path):
        """删除HDFS路径（文件或目录）"""
        try:
            if self.client.status(hdfs_path, strict=False):
                self.client.delete(hdfs_path, recursive=True)
                return True, "删除成功"
            return False, "路径不存在"
        except Exception as e:
            return False, f"删除失败: {str(e)}"