import cv2 as cv


def find_bgr_colors(src, cnts):
    """找出颜色示例里的颜色BGR

    根据限定长，高，比例来过滤出实例颜色区域
    色块宽度是输入图片宽度的0.3到0.4之间
    色块宽高的比例是0.4到0.5之间

    Args:
        src: 输入图像
        cnts: 轮廓

    Returns:
        bgr colors
    """
    w_range = [0.3 * src.shape[1], 0.4 * src.shape[1]]
    ratio_range = [0.40, 0.50]
    colors = []

    for cnt in cnts:
        x, y, w, h = cv.boundingRect(cnt)
        ratio = round(h / w, 2)

        if ratio_range[0] < ratio < ratio_range[1] and w_range[0] < w < w_range[1]:
            # print(ratio, x, y, w, h)

            # 因为，原图色块矩形的周边和mask出来的颜色区都有模糊渐变的线
            # 无法使用cv.mean(colorRegion, meanMask)来计算实际颜色
            # 所以，取矩形的中心点的颜色最为准确
            cx, cy = round(x + w / 2), round(y + h / 2)
            bgr = src[cy, cx]
            colors.append(bgr.tolist())

    return colors


def process(img_path):
    src = cv.imread(img_path)
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)

    # 低于thresh都变为黑色，maxval是给binary用的
    threshold = cv.threshold(gray, 254, 255, cv.THRESH_BINARY_INV)[1]

    contours, hierarchy = cv.findContours(threshold, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

    bgr_colros = find_bgr_colors(src, contours)
    # print(bgr_colros)
    return bgr_colros


if __name__ == '__main__':
    id = 'id2'
    file_name = 'color_region.png'
    img_path = '../images/' + id + '/' + file_name

    process(img_path)

    cv.waitKey(0)
    cv.destroyAllWindows()