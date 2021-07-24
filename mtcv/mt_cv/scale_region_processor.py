import cv2 as cv
import numpy as np

from mt_cv import test_util


def process(img_path, debug=False):
    """找出比例尺像素, 默认作为1km的比例长度

    Args:
        img_path: 图片路径
        debug: 调试
    """
    src = cv.imread(img_path)
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)

    # 找出轮廓
    edges = cv.Canny(gray, 85, 255)

    # 从轮廓里找直线
    lines = cv.HoughLinesP(edges, 1, np.pi / 180, 100)

    # 测试代码
    if debug:
        copy = src.copy()
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv.line(copy, (x1, y1), (x2, y2), (255, 0, 0), 2)
        test_util.show_img("lines", copy)

    # 从直线里找出y坐标一样的两个点，就是比例尺
    scale = 0
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if y1 == y2:
            scale = x2 - x1
            break

    return scale


if __name__ == '__main__':
    image_folder = '../images/tmp/0a0937ba-ca3e-4d8c-9c3b-dbecfb5b1d68'
    img_path = image_folder + '/scale_region.png'

    scale = process(img_path, debug=True)
    # scale = process(img_path)
    print(scale)

    cv.waitKey(0)
    cv.destroyAllWindows()
