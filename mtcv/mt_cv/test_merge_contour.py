import cv2 as cv
import numpy as np

from mt_cv import image_util


def find_if_close(cnt1, cnt2):
    row1, row2 = cnt1.shape[0], cnt2.shape[0]
    for i in range(row1):
        for j in range(row2):
            dist = np.linalg.norm(cnt1[i] - cnt2[j])
            if abs(dist) < 50:
                return True
            elif i == row1 - 1 and j == row2 - 1:
                return False


# https://dsp.stackexchange.com/questions/2564/opencv-c-connect-nearby-contours-based-on-distance-between-them
if __name__ == '__main__':

    img_abs_path = image_util.img_abs_path('/images/id1/id1_test.png')
    img = cv.imread(img_abs_path)

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    cv.imshow('gray', gray)

    ret, thresh = cv.threshold(gray, 254, 255, cv.THRESH_BINARY_INV)
    cv.imshow('thresh', thresh)

    contours, hier = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    LENGTH = len(contours)
    print('length of contours ', LENGTH)

    status = np.zeros((LENGTH, 1))

    for i, cnt1 in enumerate(contours):
        x = i
        if i != LENGTH - 1:
            for j, cnt2 in enumerate(contours[i + 1:]):
                x = x + 1
                is_close = find_if_close(cnt1, cnt2)
                if is_close:
                    val = min(status[i], status[x])
                    status[x] = status[i] = val
                else:
                    if status[x] == status[i]:
                        status[x] = i + 1

    unified = []
    maximum = int(status.max()) + 1
    for i in range(maximum):
        pos = np.where(status == i)[0]
        if pos.size != 0:
            cont = np.vstack(list(contours[i] for i in pos))
            hull = cv.convexHull(cont)
            unified.append(hull)

    cv.drawContours(img, unified, -1, (0, 255, 0), 2)
    cv.drawContours(thresh, unified, -1, 255, -1)

    cv.imshow('drawn img', img)
    cv.imshow('drawn thresh', thresh)

    cv.waitKey(0)
    cv.destroyAllWindows()
