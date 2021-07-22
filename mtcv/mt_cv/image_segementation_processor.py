import cv2 as cv
from mt_cv import image_util
import pathlib


def find_roi_rect(src):
    """找出ROI，用于分割原图

    原图有四块区域，一个是地块区域，一个是颜色示例区域，一个距离标尺区域
    理论上是从大到小排序的
    """
    copy = src.copy()
    gray = cv.cvtColor(copy, cv.COLOR_BGR2GRAY)

    # 低于thresh都变为黑色，maxval是给binary用的
    threshold = cv.threshold(gray, 254, 255, cv.THRESH_BINARY_INV)[1]

    contours, hierarchy = cv.findContours(threshold, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    sorted_cnts = sorted(contours, key=cv.contourArea, reverse=True)

    rois = []
    for cnt in sorted_cnts:
        x, y, w, h = cv.boundingRect(cnt)
        roi = [y, y + h, x, x + w]
        rois.append(roi)

    return rois


def process(folder_name, img_path):
    """分割图片，并将图片存储到当前图片的目录下

    Args:
        folder_name: 图片文件夹
        img_path: 图片路径
    """

    img = cv.imread(img_path)

    # 重置图片大小
    img_max_size = 2000
    if img.shape[1] > img_max_size:
        img = image_util.resize_img(img, fixed_width=img_max_size)

    # 找出地块，颜色样例块，比例尺块，从大到小
    roi_rects = find_roi_rect(img)
    land_region = image_util.get_roi_by_rect(img, roi_rects[0])
    color_region = image_util.get_roi_by_rect(img, roi_rects[1])
    sacle_region = image_util.get_roi_by_rect(img, roi_rects[2])

    # 保存三张图片到images目录
    file_extension = pathlib.Path(img_path).suffix

    land_region_path = '../images/tmp/' + folder_name + '/land_region' + file_extension
    cv.imwrite(land_region_path, land_region)

    color_region_path = '../images/tmp/' + folder_name + '/color_region' + file_extension
    cv.imwrite(color_region_path, color_region)

    scale_region_path = '../images/tmp/' + folder_name + '/scale_region' + file_extension
    cv.imwrite(scale_region_path, sacle_region)

    return land_region_path, color_region_path, scale_region_path


def main():
    # TODO 通过网络拉取图片
    # TODO 存储到临时目录，然后进行处理
    folder_name = '6700df9c-b425-40d5-9e7c-e934ecf52d48'
    img_path = '../images/tmp/' + folder_name + '/original.png'

    process(folder_name, img_path)

    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
