import numpy as np
import cv2 as cv
import sys

"""Transform Rectangle Image to Square

Change the original image from rectanle to square,
so we can build RR square without out of boundary

Args:
    img: source image

Returns:
    squared image

"""


def makeSqaureImg(src):
    h, w = src.shape[0], src.shape[1]
    topPad, bottomPad, leftPad, rightPad = 0, 0, 0, 0
    if h >= w:
        rightPad = h - w
    else:
        bottomPad = w - h

    padding = [topPad, bottomPad, leftPad, rightPad]
    # add additional padding 10px for each edge, so we can see axes clearly
    padding = [x + EXTRA_PADDING for x in padding]
    sqauredImg = cv.copyMakeBorder(src, padding[0], padding[1], padding[2], padding[3], cv.BORDER_CONSTANT,
                                   value=(255, 255, 255))
    return sqauredImg


"""Draw Rect for testing
Args:
    copyOfsqauredImg: A copy of squared image
    limit: limit the width and height, default is 100
"""


def drawRect(copyOfsqauredImg, cnts, limit=100):
    # draw contour rectangle
    for cnt in cnts:
        x, y, w, h = cv.boundingRect(cnt)
        if limit:
            if w > limit and h > limit:
                cv.rectangle(copyOfsqauredImg, (x, y), (x + w, y + h), (0, 255, 0), 2, cv.LINE_AA)


"""Draw RR
RR square is render N*N squares on screen depends on the size of square image and RR radius.
The original image will be separate by the white RR line.

Args:
    copyOfsqauredImg: a copy of squared image
    showDetail: True show bouding rect, RR label, blue RR line

"""


def drawRR(copyOfsqauredImg, showDetail=False):
    # getStartCoordiante for Axes
    startCoordinate = findStartCoordinate(src)
    startCoordianteX, startCoordianteY = startCoordinate[0], startCoordinate[1]

    # get curren positions trackbars
    RR_radius = cv.getTrackbarPos('RR_radius', 'Partition')
    RR_thickness = 4
    numberOfRRPerRow = round(maxSizeOfSrcImg / RR_radius)

    RR_LineColor = (255, 0, 0) if showDetail else (255, 255, 255)

    RR = np.zeros((numberOfRRPerRow, numberOfRRPerRow, 4), np.uint32)

    for row in range(numberOfRRPerRow):
        for col in range(numberOfRRPerRow):
            # each start position
            # start point
            x1 = EXTRA_PADDING + startCoordianteX + col * RR_radius
            y1 = EXTRA_PADDING + startCoordianteY + row * RR_radius
            # end point
            x2 = EXTRA_PADDING + startCoordianteX + (col + 1) * RR_radius
            y2 = EXTRA_PADDING + startCoordianteY + (row + 1) * RR_radius
            # print(row, col, x1, y1, x2, y2)
            cv.rectangle(copyOfsqauredImg, (x1, y1), (x2, y2), RR_LineColor, RR_thickness, cv.LINE_AA)
            RR[row][col] = [x1, y1, x2, y2]

            if showDetail:
                # add RR label
                rrIndex = row * numberOfRRPerRow + col
                cv.putText(copyOfsqauredImg, 'RR' + str(rrIndex), (x1, y1 + 30), cv.FONT_HERSHEY_SIMPLEX, 1,
                           (255, 0, 0), 2, cv.LINE_AA)

    return RR, RR_radius


"""Find Start Coordinate
Get all contours' bouding rectangles and get min y and min x from rectangle.
Args:
    cnts: original contours
Returns:
    StartCoordinate tuple (minX,minY)
"""


def findStartCoordinate(src):
    cnts = findExternalContours(src)

    minX, minY = sys.maxsize, sys.maxsize
    for cnt in cnts:
        rect = cv.boundingRect(cnt)
        x, y = rect[0], rect[1]
        minX = min(minX, x)
        minY = min(minY, y)
    return (minX, minY)


"""Find Original Contours
Find Original Contours from source image, we only need external contour.
Args:
    src: source image
Returns:
    Original contours
"""


def findExternalContours(src):
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


"""Contour Intersect
"""


def contourIntersect(original_image, contour1, contour2):
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


"""Chunked contour in side RR
"""


def ccInRR(cc, rr):
    rrX1, rrY1, rrX2, rrY2 = rr[0], rr[1], rr[2], rr[3]
    for ccPtr in cc:
        ccX, ccY = ccPtr[0][0], ccPtr[0][1]
        if ccX < rrX1 or ccX > rrX2 or ccY < rrY1 or ccY > rrY2:
            return False
    return True


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


def getRROCDic(copyOfsqauredImgForHC, RR, originalCnts, chunkedCnts, RR_radius):
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

                # Contour Approximation to reduce points and save calculation time
            #             epsilonOC = 0.1 * cv.arcLength(oc,True)
            #             approxOC = cv.approxPolyDP(oc,epsilonOC,True)

            #             epsilonCC = 0.1 * cv.arcLength(cc,True)
            #             approxCC = cv.approxPolyDP(cc,epsilonCC,True)

            #             retval = contour_intersect(approxOC, approxCC)
            #             retval = aInsideB(approxCC, approxOC)
            # getRROCDic takes  34.2955815s
            #             retval = contourIntersect(copyOfsqauredImgForHC, approxCC, approxOC)

            # getRROCDic takes  33.1093472s
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


"""Render Image

Render image with track bars, sqaure image, RR square, axes.
Track bars:    RR_radius - size for RR squqre
Square image:  the squared source image
RR square:     render N*N squares on screen depends on the size of square image and RR radius
Axes:          line to mark where the RR square start

Args:
    x: x

Raises:
    ZeroDivisionError: division by zero

"""


def renderImage(x):
    # 1 show details of RR
    copyOfsqauredImgForDetail = sqauredImg.copy()
    # find original contours for data preparation
    originalCnts = findExternalContours(copyOfsqauredImgForDetail)

    # add chunked contour ID for testing
    copyOfsqauredImgForDetailWithID = copyOfsqauredImgForDetail.copy()
    for ocIndex, oc in enumerate(originalCnts):
        x, y, w, h = cv.boundingRect(oc)
        cv.putText(copyOfsqauredImgForDetailWithID, str(ocIndex), (x + 5, y + 10), cv.FONT_HERSHEY_PLAIN, 1,
                   (255, 0, 0), 1, cv.LINE_AA)
    cv.imshow('copyOfsqauredImgForDetail with OCID', copyOfsqauredImgForDetailWithID)

    # draw RR for testing
    RR, RR_radius = drawRR(copyOfsqauredImgForDetail, True)

    # 2 start collecting HotCold Region
    copyOfsqauredImgForHC = sqauredImg.copy()
    # draw RR
    drawRR(copyOfsqauredImgForHC)
    # find chunked contours
    chunkedCnts = findExternalContours(copyOfsqauredImgForHC)

    # add chunked contour ID for testing
    copyOfsqauredImgForHCWithID = copyOfsqauredImgForHC.copy()
    for ccIndex, cc in enumerate(chunkedCnts):
        x, y, w, h = cv.boundingRect(cc)
        cv.putText(copyOfsqauredImgForHCWithID, str(ccIndex), (x + 5, y + 10), cv.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1,
                   cv.LINE_AA)
    cv.imshow('copyOfsqauredImgForHC with CCID', copyOfsqauredImgForHCWithID)

    e1 = cv.getTickCount()

    # get dictionary for RR and origianl contour's relationship
    rrocDict, ocRRDict = getRROCDic(copyOfsqauredImgForHC, RR, originalCnts, chunkedCnts, RR_radius)

    e2 = cv.getTickCount()
    time = (e2 - e1) / cv.getTickFrequency()
    print('getRROCDic takes ', time)

    # mark HOT COLD regison with different colors, same hot cold region use the same color
    for rrIndex in rrocDict:
        # prepare color for the same hot cold region's contours
        #         rng = np.random.randint(0, 255)
        #         b,g,r = rng&255, (rng>>8)&255, (rng>>16)&255
        b, g, r = np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255)

        #         b = 250 - rrIndex * 16
        #         g = 250 - rrIndex * 8
        #         r = 250 - rrIndex * 2
        color = (b, g, r)
        for ocIndex in rrocDict[rrIndex]:
            cv.fillConvexPoly(copyOfsqauredImgForHC, originalCnts[ocIndex], color)

    # mark missed original contour as black for us to fix them later
    # not sure why, but the intersection algorithm is most likely to be the root cause
    for ocIndex, oc in enumerate(originalCnts):
        if ocIndex not in ocRRDict:
            cv.fillConvexPoly(copyOfsqauredImgForHC, oc, (0, 0, 0))

    #     print(len(originalCnts))
    #     cv.drawContours(copyOfsqauredImgForDetail, originalCnts, -1, (0,0,255), 2)
    #     drawRect(copyOfsqauredImgForDetail, originalCnts)
    #     print(len(chunkedCnts))
    #     cv.drawContours(copyOfsqauredImgForHC, chunkedCnts, -1, (0,0,255), 2)
    #     drawRect(copyOfsqauredImgForHC, chunkedCnts, False)

    cv.imshow('Partition', copyOfsqauredImgForDetail)
    cv.imshow('CopyOfsqauredImgForHC', copyOfsqauredImgForHC)


# init
# init global constant
EXTRA_PADDING = 10
# init global variables here
src = cv.imread('partition1.png')
maxSizeOfOriginalSrcImg = max(src.shape[0], src.shape[1])
# resize to half
# src = cv.resize(src, (0,0), fx=0.3, fy=0.3)
src = cv.resize(src, (0, 0), fx=800 / maxSizeOfOriginalSrcImg, fy=800 / maxSizeOfOriginalSrcImg)

# prepare size and sqaured image after resize for a better demo
maxSizeOfSrcImg = max(src.shape[0], src.shape[1])
sqauredImg = makeSqaureImg(src)

# prepare
# create a widnow
cv.namedWindow('Partition')
# cteate trackbars RR radius changes
# RR radius for draw rectangle, 220 is as the demo
cv.createTrackbar('RR_radius', 'Partition', 200, maxSizeOfSrcImg, renderImage)

# render
renderImage(-1)

# loop until use press ESC
while (1):
    k = cv.waitKey(100) & 0xFF
    if k == 27:
        break

cv.destroyAllWindows()
