from collections import defaultdict
from your_app.utils.hdfs_client import HDFSClient

class HDFSCounter:
    def __init__(self):
        self.hdfs = HDFSClient(host='172.16.190.131', port=9870)
        
    def mapper(self, files):
        """映射函数：生成(文件类型, 1)的键值对"""
        for file in files:
            # 提取文件扩展名，无扩展名文件归为'no_extension'
            file_type = file.split('.')[-1] if '.' in file else 'no_extension'
            yield (file_type.lower(), 1)

    def reducer(self, mapped_items):
        """归约函数：统计每种文件类型的总数"""
        counts = defaultdict(int)
        for file_type, count in mapped_items:
            counts[file_type] += count
        return dict(counts)

    def run(self, hdfs_path='/'):
        """执行完整MapReduce流程"""
        try:
            # 从HDFS获取文件列表
            files = self.hdfs.list_files(hdfs_path)
            # 执行Map阶段
            mapped = self.mapper(files)
            # 执行Reduce阶段
            result = self.reducer(mapped)
            return True, result
        except Exception as e:
            return False, str(e)