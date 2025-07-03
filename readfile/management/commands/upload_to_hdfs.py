from django.core.management.base import BaseCommand
from readfile.utils.hdfs_operations import HDFSOperator

class Command(BaseCommand):
    help = '上传本地文件到HDFS'

    def add_arguments(self, parser):
        parser.add_argument('local_path', type=str, help='本地文件路径')
        parser.add_argument('hdfs_path', type=str, help='HDFS目标路径')

    def handle(self, *args, **options):
        operator = HDFSOperator()
        success, message = operator.upload_file(
            options['local_path'],
            options['hdfs_path']
        )
        if success:
            self.stdout.write(self.style.SUCCESS(message))
        else:
            self.stdout.write(self.style.ERROR(message))