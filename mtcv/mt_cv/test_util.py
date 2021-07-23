import cv2 as cv
import numpy as np
import image_util


def show_contours(img, contours, rect=False):
    """在新的图片里画出轮廓

    Args:
        img: 输入图片
        contours: 轮廓
        rect: 是否显示成矩形，默认False
    """
    img = img.copy()

    print('show_contours, contours length is ', len(contours))
    for i in contours:
        if rect:
            x, y, w, h = cv.boundingRect(i)
            cv.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv.putText(img, 'Area' + str(cv.contourArea(i)), (x + 5, y + 15), cv.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1,
                       cv.LINE_AA)
        else:
            cv.drawContours(img, [i], -1, (255, 0, 0), 2)
    cv.imshow("detect", image_util.resize_img(img))
    cv.waitKey(0)


def show_img(name, src):
    """显示一张图"""
    resize_src = image_util.resize_img(src)
    cv.imshow(name, resize_src)


def show_compare_img(img1, img2):
    """显示两张图片进行对比"""
    cv.imshow("compare images", np.hstack([image_util.resize_img(img1), image_util.resize_img(img2)]))