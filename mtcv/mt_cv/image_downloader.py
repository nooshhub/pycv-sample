import os
import urllib.request


def download_img(image_url, destination):
    img_folder = '../images'
    image_file_name = 'idx.png'
    image_path = img_folder + destination + '/' + image_file_name
    check_folder(image_path)

    with open(image_path, 'wb') as f:
        with urllib.request.urlopen(image_url) as response:
            f.write(response.read())


def check_folder(folder_path):
    d = os.path.dirname(folder_path)
    if not os.path.exists(d):
        os.makedirs(d)


if __name__ == '__main__':
    image_url = 'http://x/file/demo2.2.png'
    destination = '/tmp'
    download_img(image_url, destination)
