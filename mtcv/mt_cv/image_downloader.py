import os
import urllib.request


def download_img(image_url, destination):
    """根据图片的url下载图片，如果图片已经下载，删除已经存在的，然后更新为最新图片"""
    img_folder = '../images'
    image_file_name = 'idx.png'
    image_path = img_folder + destination + '/' + image_file_name
    check_folder(image_path)

    with open(image_path, 'wb') as f:
        with urllib.request.urlopen(image_url) as response:
            f.write(response.read())

    return id, file_name, img_path


def check_folder(folder_path):
    d = os.path.dirname(folder_path)
    if not os.path.exists(d):
        os.makedirs(d)


if __name__ == '__main__':
    image_url = 'http://x/file/demo2.2.png'
    # destination = '/tmp'
    # download_img(image_url, destination)
    import pathlib
    print(pathlib.Path(image_url).name)
    print(pathlib.Path(image_url).suffix)
    print(pathlib.Path(image_url).suffixes)
