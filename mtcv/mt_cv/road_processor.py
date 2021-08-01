import numpy as np
import cv2 as cv
from mt_cv import image_util, test_util


def process(image_folder, img_path):
    """处理图片

    Args:
        image_folder: 图片文件夹
        img_path: 图片路径
    """
    # 道路检测的生成的图片都放到road文件夹下
    image_folder += '/road'

    src = cv.imread(img_path)

    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    thresh = cv.threshold(gray, 254, 255, cv.THRESH_BINARY)[1]
    image_util.generate_img(image_folder, 'thresh.png', thresh)

    thinned = cv.ximgproc.thinning(thresh)
    image_util.generate_img(image_folder, 'thinned.png', thinned)

    # houghline目前看起来只能用来帮助我们减少循环次数，使用线的点，而不是所有点
    # hough lines , minLineLength=60, maxLineGap=10
    lines = cv.HoughLinesP(thinned, cv.HOUGH_PROBABILISTIC, np.pi / 180, 100)

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

    # kernel = np.ones((3, 3), np.uint8)
    # morph = cv.morphologyEx(img_with_land_cnt, cv.MORPH_CLOSE, kernel)
    # image_util.generate_img(image_folder, 'road_morph.png', morph)

    # # TODO threshold怎么计算的？
    # edges = cv.Canny(morph, 100, 200)
    # # edges找出来，但是是锯齿状，会在找轮廓时形成很多点，这里加一道拉普拉斯锐化一下
    # edges = cv.Laplacian(edges, -1, (3, 3))
    # image_util.generate_img(image_folder, 'road_edges.png', edges)

    return {'todo': 'road'}


def main():
    # image_folder = image_util.img_abs_path('/images/tmp/7bf573e0-4ce4-49ee-8e7a-cf5caf525a94')
    image_folder = image_util.img_abs_path('/images/tmp/5abf9a33-d9f6-4b77-bd43-94e1d52d57ae')
    img_path = image_folder + '/hot_cold.png'

    process(image_folder, img_path)

    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
