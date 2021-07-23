import os
import urllib.request
import uuid
import pathlib
import shutil


def download_img(image_url):
    """根据图片的url下载图片

    Args：
        image_url: 图片URL

    """

    # 准备存储图片信息，文件夹唯一，图片默认为original.png
    folder_name = uuid.uuid4()
    image_extension = pathlib.Path(image_url).suffix
    image_file_name = 'original' + image_extension
    image_folder = '../images/tmp/' + str(folder_name)
    image_path = image_folder + '/' + image_file_name

    # 创建文件夹
    d = os.path.dirname(image_path)
    if not os.path.exists(d):
        os.makedirs(d)

    # 下载图片
    with open(image_path, 'wb') as f:
        with urllib.request.urlopen(image_url) as response:
            f.write(response.read())

    return image_folder, image_path


def clean_img(image_folder):
    """删除下载的图片以及文件夹

    Args:
        image_folder: 图片文件夹
    """
    try:
        shutil.rmtree(image_folder)
    except OSError as e:
        print("Error: %s : %s" % (image_folder, e.strerror))


if __name__ == '__main__':
    image_url = 'http://172.20.171.245/file/demo2.2.png'
    image_folder, image_path = download_img(image_url)
    # clean_img(image_folder)


