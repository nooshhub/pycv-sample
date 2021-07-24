import cv2 as cv
import numpy as np

from mt_cv import test_util, image_util
from mt_cv.color_data import bgr_colors


def process(img_path, debug=False):
    """从color_data.bgr_colors里过滤出当前图片中使用到的颜色，减少色块匹配的循环次数"""

    src = cv.imread(img_path)

    filtered_bgr_colors = []

    for bgr in bgr_colors:
        # 图片里的颜色可能和示例颜色不相等，适当增加点阈值来防色差
        threshold = 5
        lower = np.array(image_util.bgr_with_threshold(bgr, -threshold), dtype="uint8")
        upper = np.array(image_util.bgr_with_threshold(bgr, threshold), dtype="uint8")
        # 根据阈值找到对应颜色区域，黑底白块
        mask = cv.inRange(src, lower, upper)

        # 过滤出于颜色匹配的色块
        non_zero_count = cv.countNonZero(mask)
        if non_zero_count == 0:
            continue

        if debug:
            # 黑白变白黑
            mask_inv = 255 - mask
            # 展示图片
            output = cv.bitwise_and(src, src, mask=mask_inv)
            test_util.show_compare_img(src, output)

        filtered_bgr_colors.append(bgr)
    return filtered_bgr_colors


if __name__ == '__main__':
    image_folder = '../images/tmp/0a0937ba-ca3e-4d8c-9c3b-dbecfb5b1d68'
    img_path = image_folder + '/color_region.png'

    # bgr_colros = process(img_path, debug=True)
    bgr_colros = process(img_path)
    print(bgr_colros)

    cv.waitKey(0)
    cv.destroyAllWindows()
