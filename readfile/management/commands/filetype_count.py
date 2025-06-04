from django.core.management.base import BaseCommand
from readfile.mapreduce.hdfs_counter import HDFSCounter

class Command(BaseCommand):
    help = '统计HDFS文件类型分布'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, default='/', 
                          help='HDFS目标路径（默认为根目录）')

    def handle(self, *args, **options):
        counter = HDFSCounter()
        success, result = counter.run(options['path'])
        
        if success:
            self.stdout.write("文件类型统计结果：")
            for file_type, count in result.items():
                self.stdout.write(f"{file_type}: {count}个")
        else:
            self.stdout.write(self.style.ERROR(f"执行失败: {result}"))