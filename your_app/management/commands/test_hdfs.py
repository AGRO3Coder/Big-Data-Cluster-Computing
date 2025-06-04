from django.core.management.base import BaseCommand
from your_app.utils.hdfs_client import HDFSClient

class Command(BaseCommand):
    help = '测试HDFS连接及文件操作'
    
    def add_arguments(self, parser):
        parser.add_argument('--list-files', action='store_true', help='列出HDFS根目录文件')
        parser.add_argument('--read-file', type=str, help='读取指定HDFS文件')

    def handle(self, *args, **options):
        hdfs = HDFSClient(host='172.16.190.131', port=9870)
        
        # 文件列表模式
        if options['list_files']:
            try:
                files = hdfs.list_files()
                self.stdout.write(f"HDFS根目录文件列表：\n" + "\n".join(files))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"获取文件列表失败: {str(e)}"))
        
        # 文件读取模式
        elif options['read_file']:
            try:
                content = hdfs.read_file(options['read_file'])
                self.stdout.write(f"文件内容：\n{content}")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"读取文件失败: {str(e)}"))
        
        # 默认连接测试
        else:
            success, message = hdfs.test_connection()
            if success:
                self.stdout.write(self.style.SUCCESS(message))
            else:
                self.stdout.write(self.style.ERROR(message))