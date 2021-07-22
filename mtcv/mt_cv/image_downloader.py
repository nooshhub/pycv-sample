import os
import urllib.request
import uuid
import pathlib


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

    return folder_name, image_path


if __name__ == '__main__':
    image_url = 'http://172.20.171.245/file/demo2.2.png'
    download_img(image_url)



