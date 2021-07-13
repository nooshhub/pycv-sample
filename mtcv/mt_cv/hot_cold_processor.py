import numpy as np
import cv2 as cv
import sys
from mt_cv import image_util


def draw_rr(copy_of_squared_img, rr_radius, start_coordinate, show_detail=False):
    """画出功能半径分割图
    RR square is render N*N squares on screen depends on the size of square image and RR radius.
    The original image will be separate by the white RR line.

    Args:
        copy_of_squared_img: a copy of squared image
        rr_radius: 功能半径
        start_coordinate: 起始位置
        show_detail: True show bounding rect, RR label, blue RR line

    """
    # getStartCoordinate for Axes
    start_coordinate_x, start_coordinate_y = start_coordinate[0], start_coordinate[1]

    # get curren positions trackbars
    rr_thickness = 4
    max_size_of_src_img = max(copy_of_squared_img.shape[0], copy_of_squared_img.shape[1])
    number_of_rr_per_row = round(max_size_of_src_img / rr_radius)

    rr_line_color = (255, 0, 0) if show_detail else (255, 255, 255)

    RR = np.zeros((number_of_rr_per_row, number_of_rr_per_row, 4), np.uint32)

    for row in range(number_of_rr_per_row):
        for col in range(number_of_rr_per_row):
            # each start position
            # start point
            x1 = start_coordinate_x + col * rr_radius
            y1 = start_coordinate_y + row * rr_radius
            # end point
            x2 = start_coordinate_x + (col + 1) * rr_radius
            y2 = start_coordinate_y + (row + 1) * rr_radius
            # print(row, col, x1, y1, x2, y2)
            cv.rectangle(copy_of_squared_img, (x1, y1), (x2, y2), rr_line_color, rr_thickness, cv.LINE_AA)
            RR[row][col] = [x1, y1, x2, y2]

            if show_detail:
                # add RR label
                rrIndex = row * number_of_rr_per_row + col
                cv.putText(copy_of_squared_img, 'RR' + str(rrIndex), (x1, y1 + 30), cv.FONT_HERSHEY_SIMPLEX, 1,
                           (255, 0, 0), 2, cv.LINE_AA)

    return RR


def find_start_coordinate(cnts):
    """找出起始坐标

    获取所有地块的bounding rectangle，获取rectangle里最小的x和y坐标，就是起始坐标

    Args:
        src： 输入图像
        cnts: original contours
    Returns:
        StartCoordinate tuple (minX,minY)
    """

    minX, minY = sys.maxsize, sys.maxsize
    for cnt in cnts:
        rect = cv.boundingRect(cnt)
        x, y = rect[0], rect[1]
        minX = min(minX, x)
        minY = min(minY, y)
    return minX, minY


def find_external_contours(src):
    """Find Original Contours
    Find Original Contours from source image, we only need external contour.
    Args:
        src: source image
    Returns:
        Original contours
    """
    # preprocess, remove noise, a lot noise on the road
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)

    thresVal = 240
    maxVal = 255
    ret, thresh1 = cv.threshold(gray, thresVal, maxVal, cv.THRESH_BINARY)

    kernel = np.ones((5, 5), np.uint8)
    opening = cv.morphologyEx(thresh1, cv.MORPH_CLOSE, kernel)

    edges = cv.Canny(opening, 100, 200)
    contours, hierarchy = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    #     cv.imshow('gray', gray)
    #     cv.imshow('thresh1', thresh1)
    #     cv.imshow('opening', opening)
    return contours


def is_contour_intersect(original_image, contour1, contour2):
    """地块轮廓交集检查
    """
    # Two separate contours trying to check intersection on
    contours = [contour1, contour2]

    # Create image filled with zeros the same size of original image
    blank = np.zeros(original_image.shape[0:2])

    # Copy each contour into its own image and fill it with '1'
    image1 = cv.drawContours(blank.copy(), contours, 0, 1)
    image2 = cv.drawContours(blank.copy(), contours, 1, 1)

    # Use the logical AND operation on the two images
    # Since the two images had bitwise AND applied to it,
    # there should be a '1' or 'True' where there was intersection
    # and a '0' or 'False' where it didnt intersect
    intersection = np.logical_and(image1, image2)

    # Check if there was a '1' in the intersection array
    return intersection.any()


def is_chunked_land_in_rr(cc, rr):
    """检查切割后的地块是否在供能方块内
    """
    rrX1, rrY1, rrX2, rrY2 = rr[0], rr[1], rr[2], rr[3]
    for ccPtr in cc:
        ccX, ccY = ccPtr[0][0], ccPtr[0][1]
        if ccX < rrX1 or ccX > rrX2 or ccY < rrY1 or ccY > rrY2:
            return False
    return True


def get_rr_land_dict(hot_cold_img, RR, land_cnts, chunked_land_cnts, rr_radius):
    """获取供能半径和地块的关系
    地块按照供能半径分组，供能半径从左往右，从0开始展开

    Args:
        hot_cold_img: 输入图片
        RR: 供能半径的位置信息，行和列
        land_cnts: 地块轮廓
        chunked_land_cnts: 被功能半径切割后的地块轮廓
        rr_radius: 供能半径的长度

    Returns:
        rr_land_dict: RR to Origianl contours dictionary
        land_rr_dict: Origianl contours to RR dictionary
    """
    # 计算单个功能方块面积，用于计算切割后的地块在供能方块里的占比，从而知道属于哪个供能方块
    # rr_ratio = cc_area / rr_area
    rr_area = rr_radius * rr_radius

    # 存放切割后的地块和供能方块的关系
    chunked_land_rr_dict = {}

    for row, rr_row in enumerate(RR):
        for col, rr in enumerate(rr_row):

            for chunked_land_index, chunked_land in enumerate(chunked_land_cnts):
                cc_area = cv.contourArea(chunked_land)
                # 去除一些很小的噪音点
                if cc_area < 100:
                    continue

                # Contour Approximation to reduce points and save calculation time
                epsilonCC = 0.1 * cv.arcLength(chunked_land, True)
                approxCC = cv.approxPolyDP(chunked_land, epsilonCC, True)

                retval = is_chunked_land_in_rr(approxCC, rr)

                if retval:
                    rr_ratio = round(cc_area / rr_area * 100, 2)
                    rr_index = row * (len(RR)) + col
                    # chunked_land and rr are one to one relationship
                    chunked_land_rr_dict[chunked_land_index] = [rr_index, rr_ratio]

    # 存放地块和供能方块的关系
    land_rr_dict = {}

    # 根据切割的地块与供能方块的关系，以及未切割前的原始地块，来计算地块和供能方块关系
    for land_index, land in enumerate(land_cnts):
        for chunked_land_index, chunked_land in enumerate(chunked_land_cnts):

            # TODO 可以考虑检查切割的地块颜色是否和原始地块匹配，来提升性能
            # 检查切割后的地块是否存在过滤后的地块和供能关系里
            if chunked_land_index not in chunked_land_rr_dict:
                continue

            retval = is_contour_intersect(hot_cold_img, chunked_land, land)

            if retval:
                rr = chunked_land_rr_dict[chunked_land_index]
                rr_index = rr[0]
                rr_ratio = rr[1]
                if land_index not in land_rr_dict:
                    land_rr_dict[land_index] = [rr_index, rr_ratio]
                else:
                    # 切割后的地块占供能方块的面积比例最大的，作为原始地块和供能方块关联的前提
                    prev_rr = land_rr_dict[land_index]
                    prev_ratio = prev_rr[1]
                    if rr_ratio > prev_ratio:
                        land_rr_dict[land_index] = [rr_index, rr_ratio]

    # 获取供能与原始地块的关系
    rr_land_dict = {}
    for land_index in land_rr_dict:
        rr = land_rr_dict[land_index]
        rr_index = rr[0]
        ocList = rr_land_dict.get(rr_index, [])
        ocList.append(land_index)
        rr_land_dict[rr_index] = ocList

    print('chunked_land_rr_dict', chunked_land_rr_dict)
    print('land_rr_dict', land_rr_dict)
    print('rr_land_dict', rr_land_dict)
    return rr_land_dict, land_rr_dict


def show_cnt_id(cnts, img, img_name):
    """显示地块轮廓id"""
    copy = img.copy()
    for ccIndex, cc in enumerate(cnts):
        x, y, w, h = cv.boundingRect(cc)
        cv.putText(copy, str(ccIndex), (x + 5, y + 10), cv.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1,
                   cv.LINE_AA)
    cv.imshow(img_name, copy)


def process_with_rr(squared_img, rr_radius, debug=False):
    """处理图像
    生成一张带有功能半径的示例图像
    生成一张用于计算冷热分区的图像

    Args:
        squared_img: 正方形图像
        rr_radius: 供能半径
        debug: 调式，默认False关闭

    Raises:
        ZeroDivisionError: division by zero
    """

    # 找出所有地块
    land_cnts = find_external_contours(squared_img)

    # 找出功能半径起始位置
    start_coordinate = find_start_coordinate(land_cnts)

    if debug:
        # 生成一张带有功能半径的验证图像
        rr_detail = squared_img.copy()
        show_cnt_id(land_cnts, rr_detail, 'rr_detail_with_land_id')

        # draw RR for testing
        draw_rr(rr_detail, rr_radius, start_coordinate, show_detail=True)
        cv.imshow('rr_detail', rr_detail)

    # 准备收集冷热分区
    copy_for_hot_cold = squared_img.copy()

    # 画出计算用的功能半径
    RR = draw_rr(copy_for_hot_cold, rr_radius, start_coordinate)

    # 找出所有被切割和未被切割的地块
    chunked_land_cnts = find_external_contours(copy_for_hot_cold)

    if debug:
        # add chunked contour ID for testing
        show_cnt_id(chunked_land_cnts, copy_for_hot_cold, 'copy_for_hot_cold_with_land_id')

    # 计算时间
    e1 = cv.getTickCount()

    # 获取功能半径和地块的关联关系
    rr_land_dict, land_rr_dict = get_rr_land_dict(copy_for_hot_cold, RR, land_cnts, chunked_land_cnts, rr_radius)

    e2 = cv.getTickCount()
    time = (e2 - e1) / cv.getTickFrequency()
    print('takes ', time)

    if debug:
        # 将相同冷暖区的地块填充为同一种随机色
        for rrIndex in rr_land_dict:
            b, g, r = np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255)
            color = (b, g, r)
            for land_index in rr_land_dict[rrIndex]:
                cv.fillConvexPoly(copy_for_hot_cold, land_cnts[land_index], color)

        # 没有找出来的地块用黑色填充
        for land_index, oc in enumerate(land_cnts):
            if land_index not in land_rr_dict:
                cv.fillConvexPoly(copy_for_hot_cold, oc, (0, 0, 0))

        cv.imshow('copy_for_hot_cold', copy_for_hot_cold)

    #TODO 返回按供能方块id分组的地块坐标，approx以后的，不然数据太大


def process(img_abs_path):
    """读入并处理图像"""
    src = cv.imread(img_abs_path)
    src_width = src.shape[1]

    # resize有助于提升处理速度
    # TODO 测试不同像素的处理速度，在800像素时效果最佳，识别率100%，17s左右
    fixed_width = 800
    src = image_util.resize_img(src, fixed_width=fixed_width)

    # TODO 填充为正方形，可以用于分类切割后的图片的填充，便于找边界，这里对原图填充显得多余
    # squared_img = generate_square_img(src)
    squared_img = src

    # TODO 从比例尺中获取像素和实际距离的比例
    # TODO 实际总地块长度也可以减少画出的供能方块，从而减少匹配时需要的个数
    # TODO 抠图后生成的 地块 方向 颜色 比例尺的小图也可以加速图片的处理，所以图片分类切割的第一步很重要
    # TODO 分割后的地块色块信息也是可以用来优化切割地块和原始地块的匹配速度的
    # 1km = 670 pixels
    src_scale = 670
    resized_scale = round(src_scale / (src_width / fixed_width))
    rr_radius = resized_scale

    # 处理图像
    process_with_rr(squared_img, rr_radius, debug=True)


def main():
    # 读取图片
    img_abs_path = image_util.img_abs_path('/images/id1/id1.png')

    process(img_abs_path)

    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
