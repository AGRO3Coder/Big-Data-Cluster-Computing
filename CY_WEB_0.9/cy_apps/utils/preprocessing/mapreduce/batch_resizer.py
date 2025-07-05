import concurrent.futures
from pathlib import Path
import logging
from preprocessing.utils.image_processor import ImageProcessor

logger = logging.getLogger(__name__)

class BatchResizer:
    def __init__(self, output_root='output'):
        self.num_workers = 2  # 临时减少worker数量便于调试
        self.output_root = Path(output_root).absolute()
        self.output_root.mkdir(parents=True, exist_ok=True)
        logger.info(f'初始化输出目录：{self.output_root}')

    def mapper(self, img_paths):
        tasks = []
        for path in img_paths:
            input_path = Path(path).absolute()
            output_path = self.output_root / f'resized_{input_path.name}'
            logger.debug(f'生成任务：{input_path} -> {output_path}')
            tasks.append((str(input_path), str(output_path)))
        return tasks

    def reducer(self, tasks):
        with concurrent.futures.ProcessPoolExecutor(
            max_workers=self.num_workers,
            initializer=self.init_worker
        ) as executor:
            futures = [
                executor.submit(self.process_single, inp, out)
                for inp, out in tasks
            ]
            
            for future in concurrent.futures.as_completed(futures):
                inp, out, success = future.result()
                if success:
                    logger.info(f'成功处理：{inp} -> {out}')
                    if not Path(out).exists():
                        logger.error(f'文件未生成：{out}')
                else:
                    logger.error(f'处理失败：{inp}')

    @staticmethod
    def init_worker():
        logging.basicConfig(level=logging.INFO)

    def process_single(self, input_path, output_path):
        try:
            logger.info(f'开始处理：{input_path}')
            success = ImageProcessor.resize_image(input_path, output_path)
            if success and Path(output_path).exists():
                return (input_path, output_path, True)
            return (input_path, output_path, False)
        except Exception as e:
            logger.error(f'处理异常：{input_path}\n{str(e)}')
            return (input_path, output_path, False)

    def process_batch(self, img_paths):
        logger.info('批量处理启动')
        tasks = self.mapper(img_paths)
        logger.info(f'共生成{len(tasks)}个处理任务')
        self.reducer(tasks)
        logger.info(f'最终输出目录内容：{list(self.output_root.glob("*"))}')