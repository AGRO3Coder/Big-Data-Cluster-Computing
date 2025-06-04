from hdfs import InsecureClient

class HDFSClient:
    def __init__(self, host='172.16.190.131', port=9870, user='root'):
        self.client = InsecureClient(f'http://{host}:{port}', user=user)
    
    def test_connection(self):
        try:
            # 尝试获取根目录状态验证连接
            status = self.client.status('/')
            return True, "连接成功"
        except Exception as e:
            return False, f"连接失败: {str(e)}"
    
    def list_files(self, hdfs_path='/'):
        """获取HDFS指定路径下的文件列表"""
        return self.client.list(hdfs_path, status=False)

    def read_file(self, hdfs_path):
        """读取HDFS文件内容"""
        with self.client.read(hdfs_path) as reader:
            return reader.read().decode('utf-8')