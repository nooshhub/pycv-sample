import numpy as np
import cv2 as cv
import sys
from mt_cv import image_util


def generate_square_img(src):
    """将图片填充成正方形的

    将图片填充成正方形的，方便我们使用功能半径去分割地块而不至于越界

    Args:
        src: 输入图像

    Returns:
        正方形图像

    """
    h, w = src.shape[0], src.shape[1]
    topPad, bottomPad, leftPad, rightPad = 0, 0, 0, 0
    if h >= w:
        rightPad = h - w
    else:
        bottomPad = w - h

    padding = [topPad, bottomPad, leftPad, rightPad]
    # add additional padding 10px for each edge, so we can see axes clearly
    padding = [x + EXTRA_PADDING for x in padding]
    squared_img = cv.copyMakeBorder(src, padding[0], padding[1], padding[2], padding[3], cv.BORDER_CONSTANT,
                                    value=(255, 255, 255))
    return squared_img


def draw_rr(copy_of_squared_img, rr_radius, start_coordinate, show_detail=False):
    """画出功能半径分割图
    RR square is render N*N squares on screen depends on the size of square image and RR radius.
    The original image will be separate by the white RR line.

    Args:
        copy_of_squared_img: a copy of squared image
        rr_radius: 功能半径
        start_coordinate: 起始位置
        show_detail: True show bouding rect, RR label, blue RR line

    """
    # getStartCoordinate for Axes
    start_coordinate_x, start_coordinate_y = start_coordinate[0], start_coordinate[1]

    # get curren positions trackbars
    rr_thickness = 4
    maxSizeOfSrcImg = max(copy_of_squared_img.shape[0], copy_of_squared_img.shape[1])
    numberOfRRPerRow = round(maxSizeOfSrcImg / rr_radius)

    RR_LineColor = (255, 0, 0) if show_detail else (255, 255, 255)

    RR = np.zeros((numberOfRRPerRow, numberOfRRPerRow, 4), np.uint32)

    for row in range(numberOfRRPerRow):
        for col in range(numberOfRRPerRow):
            # each start position
            # start point
            x1 = EXTRA_PADDING + start_coordinate_x + col * rr_radius
            y1 = EXTRA_PADDING + start_coordinate_y + row * rr_radius
            # end point
            x2 = EXTRA_PADDING + start_coordinate_x + (col + 1) * rr_radius
            y2 = EXTRA_PADDING + start_coordinate_y + (row + 1) * rr_radius
            # print(row, col, x1, y1, x2, y2)
            cv.rectangle(copy_of_squared_img, (x1, y1), (x2, y2), RR_LineColor, rr_thickness, cv.LINE_AA)
            RR[row][col] = [x1, y1, x2, y2]

            if show_detail:
                # add RR label
                rrIndex = row * numberOfRRPerRow + col
                cv.putText(copy_of_squared_img, 'RR' + str(rrIndex), (x1, y1 + 30), cv.FONT_HERSHEY_SIMPLEX, 1,
                           (255, 0, 0), 2, cv.LINE_AA)

    return RR


def find_start_coordinate(cnts):
    """找出起始坐标

    获取所有地块的bounding rectangle，获取rectangle里最小的x和y坐标，就是起始坐标

    Args:
        src： 输入图像
        cnts: original contours
    Returns:
        StartCoordinate tuple (minX,minY)
    """

    minX, minY = sys.maxsize, sys.maxsize
    for cnt in cnts:
        rect = cv.boundingRect(cnt)
        x, y = rect[0], rect[1]
        minX = min(minX, x)
        minY = min(minY, y)
    return minX, minY


def find_external_contours(src):
    """Find Original Contours
    Find Original Contours from source image, we only need external contour.
    Args:
        src: source image
    Returns:
        Original contours
    """
    # preprocess, remove noise, a lot noise on the road
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)

    thresVal = 240
    maxVal = 255
    ret, thresh1 = cv.threshold(gray, thresVal, maxVal, cv.THRESH_BINARY)

    kernel = np.ones((5, 5), np.uint8)
    opening = cv.morphologyEx(thresh1, cv.MORPH_CLOSE, kernel)

    edges = cv.Canny(opening, 100, 200)
    contours, hierarchy = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    #     cv.imshow('gray', gray)
    #     cv.imshow('thresh1', thresh1)
    #     cv.imshow('opening', opening)
    return contours


def contourIntersect(original_image, contour1, contour2):
    """Contour Intersect
    """
    # Two separate contours trying to check intersection on
    contours = [contour1, contour2]

    # Create image filled with zeros the same size of original image
    blank = np.zeros(original_image.shape[0:2])

    # Copy each contour into its own image and fill it with '1'
    image1 = cv.drawContours(blank.copy(), contours, 0, 1)
    image2 = cv.drawContours(blank.copy(), contours, 1, 1)

    # Use the logical AND operation on the two images
    # Since the two images had bitwise AND applied to it,
    # there should be a '1' or 'True' where there was intersection
    # and a '0' or 'False' where it didnt intersect
    intersection = np.logical_and(image1, image2)

    # Check if there was a '1' in the intersection array
    return intersection.any()


def ccInRR(cc, rr):
    """Chunked contour in side RR
    """
    rrX1, rrY1, rrX2, rrY2 = rr[0], rr[1], rr[2], rr[3]
    for ccPtr in cc:
        ccX, ccY = ccPtr[0][0], ccPtr[0][1]
        if ccX < rrX1 or ccX > rrX2 or ccY < rrY1 or ccY > rrY2:
            return False
    return True


def get_rr_land_dict(copyOfsqauredImgForHC, RR, originalCnts, chunkedCnts, RR_radius):
    """Get the RR and Origianl contours dictionary
    Get the RR region as Hot Cold Region and has a list of original contours related to the Hot Cold Region

    Args:
        RR: RR region, and after calculated it will be the Hot Cold Region
        originalCnts: Origianl contours
        chunkedCnts: chunked up Origianl contours
        RR_radius: RR region's size, RR is a square

    Returns:
        rrocDict: RR to Origianl contours dictionary
        ocRRDict: Origianl contours to RR dictionary
    """
    # prepare RR area for rrRatio = ccArea / rrArea
    rrArea = RR_radius * RR_radius

    # prepare chunked contour to RR's dictionary
    ccRRDict = {}

    for row, rrRow in enumerate(RR):
        for col, rr in enumerate(rrRow):

            for ccIndex, cc in enumerate(chunkedCnts):
                ccArea = cv.contourArea(cc)
                # exclude too small chunked contour and some noises point
                if ccArea < 100:
                    continue

                # Contour Approximation to reduce points and save calculation time
                epsilonCC = 0.1 * cv.arcLength(cc, True)
                approxCC = cv.approxPolyDP(cc, epsilonCC, True)

                retval = ccInRR(approxCC, rr)

                if retval:
                    rrRatio = round(ccArea / rrArea * 100, 2)
                    rrIndex = row * (len(RR)) + col
                    # cc and rr are one to one relationship
                    ccRRDict[ccIndex] = [rrIndex, rrRatio]

    # prepare original contour to RR's dictionary by the chunked contour and RR's dictionary
    ocRRDict = {}
    for ocIndex, oc in enumerate(originalCnts):
        for ccIndex, cc in enumerate(chunkedCnts):

            # the cc may be too small to be calculated, it may not in the ccRRDict, skip it
            if ccIndex not in ccRRDict:
                continue

            retval = contourIntersect(copyOfsqauredImgForHC, cc, oc)

            if retval:
                rr = ccRRDict[ccIndex]
                rrIndex = rr[0]
                rrRatio = rr[1]
                if ocIndex not in ocRRDict:
                    ocRRDict[ocIndex] = [rrIndex, rrRatio]
                else:
                    # check if the current cc's RR ratio is bigger than the previous saved in ocRRDict one
                    prevRR = ocRRDict[ocIndex]
                    prevRatio = prevRR[1]
                    if rrRatio > prevRatio:
                        ocRRDict[ocIndex] = [rrIndex, rrRatio]

    # get RR to original contours map
    rrocDict = {}
    for ocIndex in ocRRDict:
        rr = ocRRDict[ocIndex]
        rrIndex = rr[0]
        ocList = rrocDict.get(rrIndex, [])
        ocList.append(ocIndex)
        rrocDict[rrIndex] = ocList

    print('ccRRDict', ccRRDict)
    print('ocRRDict', ocRRDict)
    print('rrocDict', rrocDict)
    return rrocDict, ocRRDict


def show_cnt_id(cnts, img, img_name):
    copy = img.copy()
    for ccIndex, cc in enumerate(cnts):
        x, y, w, h = cv.boundingRect(cc)
        cv.putText(copy, str(ccIndex), (x + 5, y + 10), cv.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1,
                   cv.LINE_AA)
    cv.imshow(img_name, copy)


def process(squared_img, rr_radius, debug=False):
    """处理图像
    生成一张带有功能半径的示例图像
    生成一张用于计算冷热分区的图像

    Args:
        squared_img: 正方形图像
        rr_radius: 供能半径

    Raises:
        ZeroDivisionError: division by zero
    """

    # 找出所有地块
    land_cnts = find_external_contours(squared_img)

    # 找出功能半径起始位置
    start_coordinate = find_start_coordinate(land_cnts)

    if debug:
        # 生成一张带有功能半径的验证图像
        rr_detail = squared_img.copy()
        show_cnt_id(land_cnts, rr_detail, 'rr_detail_with_land_id')

        # draw RR for testing
        draw_rr(rr_detail, rr_radius, start_coordinate, show_detail=True)
        cv.imshow('rr_detail', rr_detail)

    # 准备收集冷热分区
    copy_for_hot_cold = squared_img.copy()

    # 画出计算用的功能半径
    RR = draw_rr(copy_for_hot_cold, rr_radius, start_coordinate)

    # 找出所有被切割和未被切割的地块
    chunked_land_cnts = find_external_contours(copy_for_hot_cold)

    if debug:
        # add chunked contour ID for testing
        show_cnt_id(chunked_land_cnts, copy_for_hot_cold, 'copy_for_hot_cold_with_land_id')

    # 计算时间
    e1 = cv.getTickCount()

    # 获取功能半径和地块的关联关系
    rr_land_dict, land_rr_dict = get_rr_land_dict(copy_for_hot_cold, RR, land_cnts, chunked_land_cnts, rr_radius)

    e2 = cv.getTickCount()
    time = (e2 - e1) / cv.getTickFrequency()
    print('takes ', time)

    if debug:
        # mark HOT COLD region with different colors, same hot cold region use the same color
        for rrIndex in rr_land_dict:
            # prepare color for the same hot cold region's contours
            #         rng = np.random.randint(0, 255)
            #         b,g,r = rng&255, (rng>>8)&255, (rng>>16)&255
            b, g, r = np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255)

            #         b = 250 - rrIndex * 16
            #         g = 250 - rrIndex * 8
            #         r = 250 - rrIndex * 2
            color = (b, g, r)
            for land_index in rr_land_dict[rrIndex]:
                cv.fillConvexPoly(copy_for_hot_cold, land_cnts[land_index], color)

        # mark missed original contour as black for us to fix them later
        # not sure why, but the intersection algorithm is most likely to be the root cause
        for land_index, oc in enumerate(land_cnts):
            if land_index not in land_rr_dict:
                cv.fillConvexPoly(copy_for_hot_cold, oc, (0, 0, 0))

        cv.imshow('copy_for_hot_cold', copy_for_hot_cold)


# init global constant
EXTRA_PADDING = 10


def main():
    # 读取图片
    src = cv.imread('../images/id1/id1.png')

    # resize有助于提升处理速度
    src = image_util.resize_img(src)
    # 填充为正方形
    squared_img = generate_square_img(src)

    # 1km = 670 pixels
    scale = 670
    rr_radius = scale

    # 处理图像
    process(squared_img, rr_radius, debug=True)

    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
