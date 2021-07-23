import numpy as np
import cv2 as cv
from mt_cv import image_util, test_util


def find_road(src):
    """找出所有的地块轮廓
    """
    src = src.copy()
    src = image_util.resize_img(src, 600)
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    # 二值化，将不是白色的都变为黑色
    ret, thresh1 = cv.threshold(gray, 254, 255, cv.THRESH_BINARY)
    test_util.show_img('thresh1', thresh1)

    # hough lines
    lines = cv.HoughLinesP(thresh1, cv.HOUGH_PROBABILISTIC, np.pi / 180, 1, minLineLength=60, maxLineGap=10)

    # for line in lines:
    #     x1, y1, x2, y2 = line[0]
    #     cv.line(src, (x1, y1), (x2, y2), (0, 255, 0), 2)

    for x in range(0, len(lines)):
        for x1, y1, x2, y2 in lines[x]:
            # cv2.line(src,(x1,y1),(x2,y2),(0,128,0),2, cv2.LINE_AA)
            pts = np.array([[x1, y1], [x2, y2]], np.int32)
            cv.polylines(src, [pts], True, (0, 255, 0))

    test_util.show_img('src', src)

    # kernel = np.ones((7, 7), np.uint8)
    # morph = cv.morphologyEx(thresh1, cv.MORPH_CLOSE, kernel)
    # cv.imshow('morph', morph)
    #
    # # TODO threshold怎么计算的？
    # edges = cv.Canny(morph, 100, 200)
    # # edges找出来，但是是锯齿状，会在找轮廓时形成很多点，这里加一道拉普拉斯锐化一下
    # edges = cv.Laplacian(edges, -1, (3, 3))
    # cv.imshow('edges', edges)


def process(img_path):
    """处理图片

    Args:
        img_path: 图片路径
    """
    img = cv.imread(img_path)

    # 找出地块
    find_road(img)

    return {'todo': 'road'}


def main():
    img_path = '/images/id1/id1.png'

    land_dict = process(image_util.img_abs_path(img_path))

    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
