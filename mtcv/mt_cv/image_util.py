import numpy as np
import cv2 as cv
import config


def resize_img(src, fixed_width=800):
    """缩小图像,方便看效果

    resize会损失像素，造成边缘像素模糊，不要再用于计算的原图上使用，仅在用来显示的测试图片上使用

    Args:
        src: 输入图像
        fixed_width: 默认宽度800

    Returns:
        resized image
    """
    height, width = src.shape[:2]
    ratio = fixed_width / width
    size = (int(width * ratio), int(height * ratio))
    img = cv.resize(src, size, interpolation=cv.INTER_AREA)
    return img


def find_bgr_colors(src, cnts):
    """找出颜色示例里的颜色BGR

    根据限定长，高，比例来过滤出实例颜色区域

    Args:
        src: 输入图像
        cnts: 轮廓

    Returns:
        bgr colors
    """
    w_range = [170, 180]
    h_range = [75, 85]
    ratio_range = [0.40, 0.50]
    colors = []

    for cnt in cnts:
        x, y, w, h = cv.boundingRect(cnt)
        ratio = round(h / w, 2)

        if ratio_range[0] < ratio < ratio_range[1] and w_range[0] < w < w_range[1] and h_range[0] < h < h_range[1]:
            # print(ratio,x,y,w,h)
            # 因为，原图色块矩形的周边和mask出来的颜色区都有模糊渐变的线
            # 无法使用cv.mean(colorRegion, meanMask)来计算实际颜色
            # 所以，取矩形的中心点的颜色最为准确
            cx, cy = round(x + w / 2), round(y + h / 2)
            bgr = src[cy, cx]
            colors.append(bgr)

    return colors


def get_roi_by_contour(src, cnt, use_white_bg=True):
    """获取ROI

    根据输入的contour来截取ROI(region of interest)

    Args:
        src: 输入图片
        cnt: 轮廓
        use_white_bg: 使用白色背景，False使用黑色背景

    Returns:
        白色背景的ROI
    """
    copy = src.copy()

    # 创建一个黑色背景mask，并根据mask截取ROI
    mask = np.zeros(copy.shape[:2], np.uint8)
    mask = cv.fillConvexPoly(mask, cnt, (255, 255, 255))
    roi = cv.bitwise_and(copy, copy, mask=mask)

    if not use_white_bg:
        return roi

    # 将ROI以外的部分填充为白色
    mask = cv.bitwise_not(mask)
    white_bg = np.full(copy.shape[:2], 255, dtype=np.uint8)
    white_bg = cv.bitwise_and(white_bg, white_bg, mask=mask)
    white_bg = cv.merge((white_bg, white_bg, white_bg))

    # 合并ROI和白色背景得到最终需要的图像
    roi_with_white_bg = cv.bitwise_or(roi, white_bg)

    return roi_with_white_bg


def bgr_with_threshold(bgr, threshold):
    """根据threshold重新计算BGR的值

    Args:
        bgr: bgr list
        threshold: 阈值

    Returns:
        new bgr list
    """
    new_bgr = []
    for x in bgr:
        if x + threshold < 0:
            new_bgr.append(0)
        elif x + threshold > 255:
            new_bgr.append(255)
        else:
            new_bgr.append(x + threshold)

    return new_bgr


def img_abs_path(img_path):
    """图片绝对路径"""
    return config.MTCV_HOME + img_path


def generate_square_img(src):
    """将图片填充成正方形的

    将图片填充成正方形的，方便我们使用功能半径去分割地块而不至于越界

    Args:
        src: 输入图像

    Returns:
        正方形图像

    """
    extra_padding = 10
    h, w = src.shape[0], src.shape[1]
    top_pad, bottom_pad, left_pad, right_pad = 0, 0, 0, 0
    if h >= w:
        right_pad = h - w
    else:
        bottom_pad = w - h

    padding = [top_pad, bottom_pad, left_pad, right_pad]
    # add additional padding 10px for each edge, so we can see axes clearly
    padding = [x + extra_padding for x in padding]
    squared_img = cv.copyMakeBorder(src, padding[0], padding[1], padding[2], padding[3], cv.BORDER_CONSTANT,
                                    value=(255, 255, 255))
    return squared_img


def convert_contour_to_pts(cnt):
    """将contour转换成point"""

    # 将轮廓转换成近似的多边形，按周长的0.1计算，如果不准确可以调小一些，例如0.05
    # 采用approx之后，返回值从1m变为45kb
    epsilon = 0.01 * cv.arcLength(cnt, True)
    approx_cnt = cv.approxPolyDP(cnt, epsilon, True)

    pts = []
    for pt in approx_cnt:
        pt_dict = {
            "xAxis": int(pt[0][0]),
            "yAxis": int(pt[0][1])
        }
        pts.append(pt_dict)

    return pts


def show_img(name, src):
    resize_src = resize_img(src)
    cv.imshow(name, resize_src)