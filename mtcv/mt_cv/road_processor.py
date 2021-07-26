import numpy as np
import cv2 as cv
from mt_cv import image_util, test_util


def find_all_land_contours(src, debug=False):
    """找出所有地块轮廓

    Args:
        src: 输入图片必须是白色背景的图片
        debug: 调试

    Returns:
        所有地块轮廓
    """

    # 去除黑线
    src[np.where((src < [70, 70, 70]).all(axis=2))] = [255, 255, 255]

    if debug:
        test_util.show_img('all lands src', src)

    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    if debug:
        test_util.show_img('all lands gray', gray)

    # 二值化，将不是白色的都变为黑色
    ret, thresh1 = cv.threshold(gray, 226, 255, cv.THRESH_BINARY_INV)

    # 腐蚀去掉外部的分割线
    kernel = np.ones((5, 5), np.uint8)
    # dst = cv.morphologyEx(thresh1, cv.MORPH_OPEN, kernel, iterations=1)
    dst = cv.erode(thresh1, kernel, iterations=1)

    if debug:
        test_util.show_img('all lands erode', dst)

    edges = cv.Canny(dst, 100, 200)
    # edges找出来，但是是锯齿状，会在找轮廓时形成很多点，这里加一道拉普拉斯锐化一下
    edges = cv.Laplacian(edges, -1, (3, 3))

    if debug:
        test_util.show_img('all lands edges', edges)

    contours = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[0]

    return contours

def process(image_folder, img_path):
    """处理图片

    Args:
        image_folder: 图片文件夹
        img_path: 图片路径
    """
    # 道路检测的生成的图片都放到road文件夹下
    image_folder += '/road'

    src = cv.imread(img_path)

    # 找出所有地块轮廓
    land_cnts = find_all_land_contours(src)

    # approx 一下，但是会乱掉
    appox_land_cnts = []
    for cnt in land_cnts:
        epsilon = 0.001 * cv.arcLength(cnt, True)
        approx_cnt = cv.approxPolyDP(cnt, epsilon, True)
        appox_land_cnts.append(approx_cnt)

    img_with_land_cnt = np.zeros(src.shape[:2], np.uint8)
    cv.drawContours(img_with_land_cnt, appox_land_cnts, -1, (255, 255, 255), 1)
    image_util.generate_img(image_folder, 'img_with_land_cnt.png', img_with_land_cnt)

    # houghline目前看起来只能用来帮助我们减少循环次数，使用线的点，而不是所有点
    # hough lines , minLineLength=60, maxLineGap=10
    lines = cv.HoughLinesP(img_with_land_cnt, cv.HOUGH_PROBABILISTIC, np.pi / 180, 10)

    copy_for_drawn_lines = src.copy()
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv.line(copy_for_drawn_lines, (x1, y1), (x2, y2), (0, 255, 0), 2)
    image_util.generate_img(image_folder, 'copy_for_drawn_lines.png', copy_for_drawn_lines)

    # todo 尝试将轮廓线，或者点进行合并成一条中间的线

    # for x in range(0, len(lines)):
    #     for x1, y1, x2, y2 in lines[x]:
    #         # cv2.line(src,(x1,y1),(x2,y2),(0,128,0),2, cv2.LINE_AA)
    #         pts = np.array([[x1, y1], [x2, y2]], np.int32)
    #         cv.polylines(src, [pts], True, (0, 255, 0))
    #

    # kernel = np.ones((5, 5), np.uint8)
    # morph = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel)
    # image_util.generate_img(image_folder, 'road_morph.png', morph)
    #
    # # TODO threshold怎么计算的？
    # edges = cv.Canny(morph, 100, 200)
    # # edges找出来，但是是锯齿状，会在找轮廓时形成很多点，这里加一道拉普拉斯锐化一下
    # edges = cv.Laplacian(edges, -1, (3, 3))
    # image_util.generate_img(image_folder, 'road_edges.png', edges)

    return {'todo': 'road'}


def main():
    image_folder = image_util.img_abs_path('/images/tmp/702b699e-f9a3-465b-a2b0-072662cf4f35')
    img_path = image_folder + '/land_region.png'

    land_dict = process(image_folder, img_path)

    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
