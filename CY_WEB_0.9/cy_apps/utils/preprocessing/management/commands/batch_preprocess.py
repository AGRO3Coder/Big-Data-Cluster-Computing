from django.core.management.base import BaseCommand
from pathlib import Path
from preprocessing.mapreduce.batch_resizer import BatchResizer
from preprocessing.utils.image_processor import ImageProcessor
import os

class Command(BaseCommand):
    help = '批量图像预处理命令'

    def add_arguments(self, parser):
        parser.add_argument('input_dir', type=str, help='输入目录路径')
        parser.add_argument('output_dir', type=str, help='输出目录路径')
        parser.add_argument('--operation', type=str, default='resize',
                          choices=['resize', 'grayscale', 'blur', 'edge', 'histogram'],
                          help='选择预处理操作')

    def handle(self, *args, **options):
        input_dir = Path(options['input_dir']).absolute()
        output_dir = Path(options['output_dir']).absolute()
        
        self.stdout.write(f'输入目录：{input_dir}')
        self.stdout.write(f'输出目录：{output_dir}')
        
        output_dir.mkdir(parents=True, exist_ok=True)
        self.stdout.write(f'创建输出目录：{output_dir}')

        img_paths = list(input_dir.glob('*.jpg')) + list(input_dir.glob('*.png'))
        self.stdout.write(f'找到 {len(img_paths)} 个图像文件')

        if not img_paths:
            self.stdout.write(self.style.WARNING('未找到任何图像文件'))
            return

        try:
            if options['operation'] == 'resize':
                resizer = BatchResizer()
                resizer.process_batch([str(p) for p in img_paths])
            else:
                processor = {
                    'grayscale': ImageProcessor.grayscale,
                    'blur': ImageProcessor.gaussian_blur,
                    'edge': ImageProcessor.edge_detection,
                    'histogram': ImageProcessor.histogram_equalization
                }[options['operation']]

                for img_path in img_paths:
                    output_path = output_dir / f"processed_{img_path.name}"
                    self.stdout.write(f'处理中：{img_path} -> {output_path}')
                    processor(str(img_path), str(output_path))
                    
                    if not output_path.exists():
                        self.stdout.write(self.style.ERROR(f'文件未生成：{output_path}'))

            self.stdout.write(self.style.SUCCESS(f'成功处理 {len(img_paths)} 张图片'))
            
            # 列出输出目录内容
            output_files = list(output_dir.glob('*'))
            self.stdout.write(f'输出目录内容（{len(output_files)} 个文件）：')
            for f in output_files:
                self.stdout.write(f'• {f.name}')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'处理失败：{str(e)}'))
            import traceback
            self.stdout.write(traceback.format_exc())