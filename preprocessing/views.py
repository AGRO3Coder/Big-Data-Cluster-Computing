from django.shortcuts import render
from django.http import HttpResponseRedirect
from .reduce import map_reduce_images
from myfile.hdfs_config import client as hdfs_client


# 获取HDFS中的图片文件列表
def get_images_from_hdfs():
    try:
        file_list = hdfs_client.list('/images')
        return file_list
    except Exception as e:
        print(f"Error fetching images from HDFS: {e}")
        return []


# 数据预处理视图
def preprocess_image(request):
    if request.method == 'POST':
        # 获取用户选择的图像名称
        image_name = request.POST.get('image_name')
        if not image_name:
            return render(request, 'preprocessing/preprocessing.html', {'error': 'No image selected.'})

        # 构造HDFS中的图像路径
        image_path = f"/images/{image_name}"

        # 调用MapReduce任务处理图像
        try:
            processed_path = map_reduce_images(image_path)
            return render(request, 'preprocessing/preprocessing_result.html', {
                'original_image': image_name,
                'processed_image': processed_path.split('/')[-1]
            })
        except Exception as e:
            return render(request, 'preprocessing/preprocessing.html', {'error': str(e)})

    # 获取HDFS中的图片文件列表
    images = get_images_from_hdfs()
    return render(request, 'preprocessing/preprocessing.html', {'images': images})