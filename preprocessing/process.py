from PIL import Image
import io
import os
import uuid
from django.shortcuts import render
from hdfs import InsecureClient
from myfile.hdfs_config import client as hdfs_client


# 定义Map任务：图像处理（旋转、裁剪）
def map_process_image(image_path, output_path):
    # 从HDFS下载图像
    with hdfs_client.read(image_path) as reader:
        image_data = reader.read()

    # 使用Pillow库加载图像
    image = Image.open(io.BytesIO(image_data))

    # 图像处理：旋转90度
    rotated_image = image.rotate(90)

    # 图像处理：裁剪图像（例如裁剪中心区域）
    width, height = rotated_image.size
    left = (width - 100) / 2
    top = (height - 100) / 2
    right = (width + 100) / 2
    bottom = (height + 100) / 2
    cropped_image = rotated_image.crop((left, top, right, bottom))

    # 保存处理后的图像到临时文件
    temp_file = io.BytesIO()
    cropped_image.save(temp_file, format='JPEG')
    temp_file.seek(0)

    # 上传处理后的图像到HDFS
    hdfs_client.write(output_path, temp_file, overwrite=True)


# 定义MapReduce任务
def map_reduce_images(image_path):
    # 生成唯一文件名
    unique_filename = f"processed_{uuid.uuid4().hex}.jpg"
    output_path = f"/processed_images/{unique_filename}"

    # 调用图像处理函数
    map_process_image(image_path, output_path)
    return output_path