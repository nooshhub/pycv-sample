import os
import shutil
import uuid
from typing import List

import numpy as np
import cv2 as cv

from mt_cv import test_util, image_util, color_util
from mt_cv.test_land_data import test_input_data
from mt_cv.mt_cv_api_model import InputData, LandData, MtImage, MtCoordinate, MtScale


def generate(input_data: InputData, debug=False):
    mt_img = input_data.img_data
    # 新建一张白底图片，用来填充地块
    img = np.ones((mt_img.height, mt_img.width, 3), dtype=np.uint8) * 255
    # 新建一张白底图片，用来画出轮廓，配合input_land_cnts可以准确取到颜色，因为轮廓是在地块为外围不包含在地块内
    img_with_contour = np.ones((mt_img.height, mt_img.width, 3), dtype=np.uint8) * 255
    img_with_contour_only = np.ones((mt_img.height, mt_img.width, 3), dtype=np.uint8) * 255

    # 转换输入的input_data, 成为地块轮廓与id字典
    color_id_dict = {}
    input_land_cnts = []

    random_color_memo = set()
    for land_data in input_data.land_data:
        # 将输入数据里的点转成轮廓
        land_pts = []
        for pt in land_data.points:
            land_pts.append([pt.xAxis, pt.yAxis])
        cnt = np.array(land_pts, dtype=np.int32).reshape((-1, 1, 2))
        input_land_cnts.append(cnt)

        # 获取唯一地块颜色
        random_color = color_util.random_color(random_color_memo)
        # 填充地块
        # cv.fillConvexPoly(img, cnt, random_color)
        cv.fillPoly(img, [cnt], random_color)
        # 绘制轮廓
        cv.drawContours(img_with_contour_only, [cnt], -1, random_color, 2)
        cv.drawContours(img_with_contour, [cnt], -1, random_color, 2)
        # cv.fillConvexPoly(img_with_contour, cnt, random_color)
        cv.fillPoly(img_with_contour, [cnt], random_color)
        # 颜色与地块id字典
        color_id = color_util.color_id(random_color)
        color_id_dict[color_id] = land_data.id

    # 创建图片，uuid为文件夹名，hot_cold.png为文件名
    folder_name = uuid.uuid4()
    image_folder = image_util.img_abs_path('/images/tmp/' + str(folder_name))

    image_file_name = 'hot_cold.png'
    image_path = image_util.generate_img(image_folder, image_file_name, img)

    image_file_name = 'hot_cold_contour.png'
    image_with_contour_path = image_util.generate_img(image_folder, image_file_name, img_with_contour)

    image_file_name = 'hot_cold_contour_only.png'
    img_with_contour_only_path = image_util.generate_img(image_folder, image_file_name, img_with_contour_only)

    if debug:
        generated_img = cv.imread(image_path)
        test_util.show_img('generated_img', generated_img)

    return image_folder, image_path, color_id_dict, image_with_contour_path, input_land_cnts


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
