import numpy as np
import cv2 as cv
import json
from mt_cv import color_data, image_util
import os


def find_roi_contours(src):
    """找出ROI，用于分割原图

    原图有四块区域，一个是地块区域，一个是颜色示例区域，一个距离标尺区域，一个南北方向区域
    理论上倒排后的最大轮廓的是地块区域
    """
    copy = src.copy()
    gray = cv.cvtColor(copy, cv.COLOR_BGR2GRAY)

    # 低于thresh都变为黑色，maxval是给binary用的
    # 白底 254, 255 黑底 0, 255
    threshold = cv.threshold(gray, 0, 255, cv.THRESH_BINARY)[1]
    contours, hierarchy = cv.findContours(threshold, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    sorted_cnts = sorted(contours, key=cv.contourArea, reverse=True)
    return sorted_cnts


def find_all_land_contours(src):
    """找出所有的地块轮廓
    """
    copy = src.copy()
    contours = find_external_contours(copy)
    return contours


def find_external_contours(src):
    """找出所有外部轮廓

    Args:
        src: 输入图片必须是白色背景的图片

    Returns:
        所有外部轮廓
    """
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    # 二值化，将不是白色的都变为黑色
    ret, thresh1 = cv.threshold(gray, 254, 255, cv.THRESH_BINARY)

    kernel = np.ones((7, 7), np.uint8)
    morph = cv.morphologyEx(thresh1, cv.MORPH_CLOSE, kernel)

    # TODO threshold怎么计算的？
    edges = cv.Canny(morph, 100, 200)
    # edges找出来，但是是锯齿状，会在找轮廓时形成很多点，这里加一道拉普拉斯锐化一下
    edges = cv.Laplacian(edges, -1, (3, 3))

    contours = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[0]
    return contours


def find_color_regions_for_all_lands(img_white_bg, land_cnts, debug=False, debug_from=0, debug_len=3):
    """使用颜色来分块，并返回所有地块和色块父子关系

    Args:
        img_white_bg: 输入图片，白色背景
        land_cnts: 地块轮廓
        debug: 开启debug，只演示前三个地块的识别过程，可以通过debugFrom:debugLen来调整debug开始位置和长度
        debug_from: debug开始位置
        debug_len: debug长度
    """

    # 过滤掉面积小于100的轮廓
    filtered_land_cnts = [cnt for cnt in land_cnts if cv.contourArea(cnt) > 100]

    land_dict = {'area': 0, 'data': []}

    if debug:
        filtered_land_cnts = filtered_land_cnts[debug_from:debug_len]

    total_area = 0
    for land_cnt in filtered_land_cnts:
        total_area += cv.contourArea(land_cnt)
        land_data = find_color_regions_for_land(img_white_bg, land_cnt, debug)
        land_dict['data'].append(land_data)

    land_dict['area'] = total_area
    return land_dict


def convert_contour_to_pts(cnt):
    """将contour转换成point"""
    pts = []
    for pt in cnt:
        pt_dict = {
            "xAxis": int(pt[0][0]),
            "yAxis": int(pt[0][1])
        }
        pts.append(pt_dict)

    return pts


def find_color_regions_for_land(img_white_bg, land_cnt, debug=False):
    """使用颜色来找出单个地块内的色块

    Args:
        img_white_bg: 输入图片，白色背景
        land_cnt: 地块轮廓
        debug: 开启debug

    """
    land_color_dict = {'area': cv.contourArea(land_cnt), 'points': convert_contour_to_pts(land_cnt), 'children': []}

    land_region = image_util.get_roi_by_contour(img_white_bg, land_cnt)
    if debug:
        cv.imshow("land regions", np.hstack([image_util.resize_img(img_white_bg), image_util.resize_img(land_region)]))

    color_cnts = []
    for bgr in color_data.bgr_colors:
        # 图片里的颜色可能和示例颜色不相等，适当增加点阈值来防色差
        threshold = 5
        lower = np.array(image_util.bgr_with_threshold(bgr, -threshold), dtype="uint8")
        upper = np.array(image_util.bgr_with_threshold(bgr, threshold), dtype="uint8")
        # 根据阈值找到对应颜色区域，黑底白块
        mask = cv.inRange(land_region, lower, upper)

        # 过滤出于颜色匹配的色块
        nonZeroCount = cv.countNonZero(mask)
        if nonZeroCount == 0:
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
            color_dict = {'area': cv.contourArea(color_cnt), 'points': convert_contour_to_pts(color_cnt), 'color': bgr}
            color_dicts.append(color_dict)
        land_color_dict['children'].extend(color_dicts)

    return land_color_dict


def find_land_region(img_white_bg):
    """找出总地块

    Args:
        img_white_bg: 输入图片
    """
    roi_img_path = os.path.abspath('../images/id1/id1_roi.png')
    img = cv.imread(roi_img_path)
    # TODO 找出最大的是总地块，目前将图片按照轮廓排序，取最大面积的
    sorted_cnts = find_roi_contours(img)
    root_region = image_util.get_roi_by_contour(img_white_bg, sorted_cnts[0])
    return root_region


def find_scale(img_white_bg):
    """找出比例尺, 获取像素和千米的比例

    Args:
        img_white_bg: 输入图片

    Returns:
        ratio = pixel / meter
    """
    # TODO 找出比例尺轮廓
    px_to_1km = 670
    px_km_scale = px_to_1km / 1000
    print(1 / (px_km_scale * px_km_scale))
    return px_km_scale


def process(img_path):
    """处理图片

    Args:
        img_path: 图片路径
    """
    img_white_bg = cv.imread(img_path)
    land_region = find_land_region(img_white_bg)
    scale = find_scale(img_white_bg)

    # 找出地块
    copy = land_region.copy()
    land_cnts = find_all_land_contours(copy)

    e1 = cv.getTickCount()

    # 通过颜色来检测地块内色块
    # land_dict = find_color_regions_for_all_lands(img_white_bg, land_cnts, debug=True, debugLen=1)
    land_dict = find_color_regions_for_all_lands(img_white_bg, land_cnts)

    e2 = cv.getTickCount()
    time = (e2 - e1) / cv.getTickFrequency()
    print('takes ', time)

    return land_dict


def main():
    img_path = '../images/id1/id1_part.png'
    land_dict = process(img_path)
    json_data = json.dumps(land_dict, sort_keys=True, indent=4, separators=(',', ': '))
    print(json_data)

    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
