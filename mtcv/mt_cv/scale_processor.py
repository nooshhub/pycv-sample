import cv2 as cv

from mt_cv import image_util, test_util


def process(img_path):
    src = cv.imread(img_path)
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)

    # 低于thresh都变为黑色，maxval是给binary用的
    threshold = cv.threshold(gray, 254, 255, cv.THRESH_BINARY_INV)[1]
    cv.imshow('threshold', threshold)

    contours, hierarchy = cv.findContours(threshold, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

    # TODO 如何检测出比例尺
    # 举例底部最近的一条横线，线长度是图的80%？

    test_util.drawn_contours(copy, contours, rect=True)

    print(len(contours))


if __name__ == '__main__':
    id = 'id2'
    file_name = 'scale_region.png'
    img_path = '../images/' + id + '/' + file_name

    process(img_path)

    cv.waitKey(0)
    cv.destroyAllWindows()
