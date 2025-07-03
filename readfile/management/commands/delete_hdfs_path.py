from django.core.management.base import BaseCommand
from readfile.utils.hdfs_operations import HDFSOperator

class Command(BaseCommand):
    help = '删除HDFS指定路径'

    def add_arguments(self, parser):
        parser.add_argument('hdfs_path', type=str, help='需要删除的HDFS路径')

    def handle(self, *args, **options):
        operator = HDFSOperator()
        success, message = operator.delete_path(options['hdfs_path'])
        if success:
            self.stdout.write(self.style.SUCCESS(message))
        else:
            self.stdout.write(self.style.ERROR(message))