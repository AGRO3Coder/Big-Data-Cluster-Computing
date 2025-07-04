from PIL import Image, ImageFilter, ImageOps
import logging

logger = logging.getLogger(__name__)

class ImageProcessor:
    @staticmethod
    def resize_image(img_path, output_path):
        """调整图像尺寸（带完整路径验证）"""
        try:
            logger.info(f'尝试打开文件: {img_path}')
            with Image.open(img_path) as img:
                logger.info(f'原始尺寸: {img.size}')
                img = img.resize((224, 224))
                logger.info(f'准备保存到: {output_path}')
                img.save(output_path)
                logger.info('保存成功')
                return True
        except Exception as e:
            logger.error(f'处理失败: {img_path} -> {output_path}\n错误信息: {str(e)}')
            return False

    @staticmethod
    def grayscale(img_path, output_path):
        """灰度化处理"""
        with Image.open(img_path) as img:
            img = ImageOps.grayscale(img)
            img.save(output_path)

    @staticmethod
    def gaussian_blur(img_path, output_path, radius=2):
        """高斯模糊"""
        with Image.open(img_path) as img:
            img = img.filter(ImageFilter.GaussianBlur(radius))
            img.save(output_path)

    @staticmethod
    def edge_detection(img_path, output_path):
        """边缘检测"""
        with Image.open(img_path) as img:
            img = img.filter(ImageFilter.FIND_EDGES)
            img.save(output_path)

    @staticmethod
    def histogram_equalization(img_path, output_path):
        """直方图均衡化"""
        with Image.open(img_path) as img:
            img = ImageOps.equalize(img)
            img.save(output_path)