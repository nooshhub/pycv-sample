import os
import shutil
import uuid
from typing import List

import numpy as np
import cv2 as cv

from mt_cv import test_util, image_util
from mt_cv.test_land_data import test_input_data
from mt_cv.mt_cv_api_model import InputData, LandData, MtImage, MtCoordinate, MtScale


def generate(input_data: InputData, debug=False):
    mt_img = input_data.img_data
    # 新建一张白底图片
    img = np.ones((mt_img.height, mt_img.width, 3), dtype=np.uint8) * 255

    for land_data in input_data.land_data:
        land_pts = []
        for pt in land_data.points:
            land_pts.append([pt.xAxis, pt.yAxis])

        cnt = np.array(land_pts, dtype=np.int32).reshape((-1, 1, 2))
        cv.drawContours(img, [cnt], -1, (255, 0, 0), 2)
        cv.fillConvexPoly(img, cnt, (127, 127, 127))

    folder_name = uuid.uuid4()
    image_file_name = 'hot_cold.png'
    image_folder = image_util.img_abs_path('/images/tmp/' + str(folder_name))

    image_path = image_util.generate_img(image_folder, image_file_name, img)

    if debug:
        generated_img = cv.imread(image_path)
        test_util.show_img('generated_img', generated_img)

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
    # 准备数据
    img_data = test_input_data['img_data']

    land_data_list = []
    for land in test_input_data['land_data']:
        coordinate_list = []
        for pt in land['points']:
            coordinate = MtCoordinate(xAxis=pt['xAxis'], yAxis=pt['yAxis'])
            coordinate_list.append(coordinate)
        land_data = LandData(id=land['id'], points=coordinate_list)
        land_data_list.append(land_data)

    scale = test_input_data['scale']

    input_data = InputData(img_data=img_data, land_data=land_data_list, scale=scale)

    # 生成图片
    generate(input_data, debug=True)

    cv.waitKey(0)
    cv.destroyAllWindows()
