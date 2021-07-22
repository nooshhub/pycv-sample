import cv2 as cv
import numpy as np


def process(img_path):
    """找出比例尺像素, 默认作为1km的比例长度

    Args:
        img_path: 图片路径
    """
    src = cv.imread(img_path)
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)

    # 找出轮廓
    edges = cv.Canny(gray, 85, 255)

    # 从轮廓里找直线
    lines = cv.HoughLinesP(edges, 1, np.pi / 180, 100)

    # 从直线里找出y坐标一样的两个点，就是比例尺
    scale = 0
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if y1 == y2:
            scale = x2 - x1
            break

    return scale


if __name__ == '__main__':
    image_folder = '../images/tmp/6700df9c-b425-40d5-9e7c-e934ecf52d48'
    img_path = image_folder + '/scale_region.png'

    process(img_path)

    cv.waitKey(0)
    cv.destroyAllWindows()
