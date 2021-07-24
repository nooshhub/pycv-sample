import numpy as np
import cv2 as cv
import json
from mt_cv import color_data, image_util, color_util, test_util


def find_total_land_contour(src):
    """找出总地块轮廓

    Args:
        src: 输入图片必须是白色背景的图片

    Returns:
        所有地块轮廓
    """
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)

    # 二值化，将不是白色的都变为黑色
    ret, thresh1 = cv.threshold(gray, 226, 255, cv.THRESH_BINARY_INV)
    # test_util.show_img('thresh1', thresh1)

    contours = cv.findContours(thresh1, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[0]
    # test_util.show_contours(src, contours, rect=False)

    return contours[0]


def find_all_land_contours(src):
    """找出所有地块轮廓

    Args:
        src: 输入图片必须是白色背景的图片

    Returns:
        所有地块轮廓
    """
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)

    # 二值化，将不是白色的都变为黑色
    ret, thresh1 = cv.threshold(gray, 226, 255, cv.THRESH_BINARY_INV)

    kernel = np.ones((5, 5), np.uint8)
    dst = cv.erode(thresh1, kernel, iterations=1)

    edges = cv.Canny(dst, 100, 200)
    # edges找出来，但是是锯齿状，会在找轮廓时形成很多点，这里加一道拉普拉斯锐化一下
    edges = cv.Laplacian(edges, -1, (3, 3))

    contours = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[0]

    return contours


def find_color_regions_for_all_lands(img_white_bg, land_cnts, bgr_colors, scale,
                                     debug=False, debug_from=0, debug_len=3,
                                     land_data_only=False):
    """使用颜色来分块，并返回所有地块和色块父子关系

    Args:
        img_white_bg: 输入图片，白色背景
        land_cnts: 地块轮廓
        bgr_colors: 色块颜色
        scale: 比例尺像素
        debug: 开启debug，只演示前三个地块的识别过程，可以通过debugFrom:debugLen来调整debug开始位置和长度
        debug_from: debug开始位置
        debug_len: debug长度
        land_data_only: 只返回地块数据，为生成冷热分区的图片做准备
    """

    # 过滤掉面积小于100的轮廓
    filtered_land_cnts = [cnt for cnt in land_cnts if cv.contourArea(cnt) > 100]

    land_data_list = []

    if debug:
        filtered_land_cnts = filtered_land_cnts[debug_from:debug_len]

    if land_data_only:
        land_data_list = []
        for index, land_cnt in enumerate(filtered_land_cnts):
            land_data = {'id': index, 'points': image_util.convert_contour_to_pts(land_cnt)}
            land_data_list.append(land_data)

    else:
        for land_cnt in filtered_land_cnts:
            land_data = find_color_regions_for_land(img_white_bg, land_cnt, bgr_colors, scale, debug)
            land_data_list.append(land_data)

    return land_data_list


def find_color_regions_for_land(img_white_bg, land_cnt, bgr_colors, scale, debug=False):
    """使用颜色来找出单个地块内的色块

    Args:
        img_white_bg: 输入图片，白色背景
        land_cnt: 地块轮廓
        bgr_colors: 色块颜色
        scale: 比例尺像素
        debug: 开启debug

    """
    land_color_dict = {'area': image_util.calc_area(land_cnt, scale),
                       'points': image_util.convert_contour_to_pts(land_cnt),
                       'children': []}

    land_region = image_util.get_roi_by_contour(img_white_bg, land_cnt)
    if debug:
        cv.imshow("land regions", np.hstack([image_util.resize_img(img_white_bg), image_util.resize_img(land_region)]))

    color_cnts = []
    for bgr in bgr_colors:
        # 图片里的颜色可能和示例颜色不相等，适当增加点阈值来防色差
        threshold = 5
        lower = np.array(image_util.bgr_with_threshold(bgr, -threshold), dtype="uint8")
        upper = np.array(image_util.bgr_with_threshold(bgr, threshold), dtype="uint8")
        # 根据阈值找到对应颜色区域，黑底白块
        mask = cv.inRange(land_region, lower, upper)

        # 过滤出于颜色匹配的色块
        non_zero_count = cv.countNonZero(mask)
        if non_zero_count == 0:
            continue

        contours, hierarchy = cv.findContours(mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        # 单个地块内的也可能包含多个相同色块，使用extend插入到color_cnts列表里
        color_cnts.extend(contours)

        if debug:
            # 黑白变白黑
            mask_inv = 255 - mask
            # 展示图片
            output = cv.bitwise_and(land_region, land_region, mask=mask_inv)
            cv.imshow("compare images", np.hstack([image_util.resize_img(land_region), image_util.resize_img(output)]))
            cv.waitKey(0)

        color_dicts = []
        for color_cnt in contours:
            color_cnt_area = image_util.calc_area(color_cnt, scale)
            if color_cnt_area > 0:
                color_dict = {'area': color_cnt_area,
                              'points': image_util.convert_contour_to_pts(color_cnt),
                              'color': color_util.convert_bgr_to_rgb_str(bgr)}
                color_dicts.append(color_dict)
        land_color_dict['children'].extend(color_dicts)

    return land_color_dict


def process(img_path, bgr_colors, scale, debug=False, debug_len=3, land_data_only=False):
    """处理图片，返回地块，色块，以及图片宽高

    Args:
        img_path: 图片路径
        bgr_colors: 色块颜色
        scale: 比例尺像素
        debug: debug
        debug_len: debug长度
        land_data_only: 只返回地块数据，为生成冷热分区的图片做准备
    """
    src = cv.imread(img_path)
    image_width_height = {'width': int(src.shape[1]), 'height': int(src.shape[0])}

    # 去掉湖泊
    src[np.where((src == [255, 255, 127]).all(axis=2))] = [255, 255, 255]

    # 找出总地块
    total_land_cnt = find_total_land_contour(src)
    # 总面积包含道路面积
    total_land_dict = {'area': image_util.calc_area(total_land_cnt, scale), 'data': []}

    # 找出地块
    land_cnts = find_all_land_contours(src)

    e1 = cv.getTickCount()

    # 通过颜色来检测地块内色块
    land_data_list = find_color_regions_for_all_lands(src, land_cnts, bgr_colors, scale,
                                                      debug=debug, debug_len=debug_len,
                                                      land_data_only=land_data_only)

    e2 = cv.getTickCount()
    time = (e2 - e1) / cv.getTickFrequency()
    print('takes ', time)

    total_land_dict['data'] = land_data_list

    return total_land_dict, image_width_height


def main():
    image_folder = '../images/tmp/6700df9c-b425-40d5-9e7c-e934ecf52d48'
    img_path = image_folder + '/land_region.png'
    scale = 147

    # land_dict, image_width_height = process(img_path, color_data.bgr_colors, scale, debug=True, debug_len=None)
    land_dict, image_width_height = process(img_path, color_data.bgr_colors, scale, land_data_only=True)
    # land_dict, image_width_height = process(img_path, color_data.bgr_colors, scale)
    # print(image_width_height)

    json_data = json.dumps(land_dict, sort_keys=True, indent=4, separators=(',', ': '))
    print(json_data)

    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
