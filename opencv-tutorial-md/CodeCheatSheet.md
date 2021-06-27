### trackbar

```python
import cv2 as cv
import numpy as np


def renderImage(x):
    copyOfImg = img.copy()

    # get curren positions trackbars
    RR_radius = cv.getTrackbarPos('RR_radius', 'Partition')
    RR_thickness = cv.getTrackbarPos('RR_thickness', 'Partition')
    cv.rectangle(copyOfImg, (0,0), (RR_radius, RR_radius), (255, 0, 0), RR_thickness, cv.LINE_AA)
    cv.imshow('Partition', copyOfImg)


def nothing(x):
    pass
    
# load image, create a widnow
img = cv.imread('partition2.png')
cv.namedWindow('Partition')

# cteate trackbars RR radius changes
# RR radius for draw rectangle
cv.createTrackbar('RR_radius', 'Partition', 250, 500, renderImage)
# RR radius line's tickness
cv.createTrackbar('RR_thickness', 'Partition', 1, 3, renderImage)


# init show image
renderImage(-1)


# loop until use press ESC
while(1):
    k = cv.waitKey(100) & 0xFF
    if k == 27:
        break
    
cv.destroyAllWindows()   
```

### numpy

非常牛逼，必须掌握

numpy是后续数据操作的基础，重要概念axes和shape。

axes坐标轴，例如

```python
# rows * cols * channel
img = np.zeros((4*4*3))
# use axes to access rows from 1 to 2, cols from 1 to 2
img[1:2, 1:2]  
# shape, shape 
image.shape
# (4,4)
# 当使用img[1:2, 1:2] = img[2:3, 2:3]时，前后的shape要是相同的(1,1)，不然报错

```

### matplotlib

非常牛逼，必须掌握

#### subplot

```python
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

img = cv.imread('test.png')
print(img.shape)

# rows from 3 to 23, cols from 30:50
# rows is y, cols is x, copy[y1:y2, x1:x2]
# axis is (30, 3), (50, 23)
roi = img[3:23, 30:50]
#cv.imshow('roi', roi)
#print(roi)
cv.rectangle(img, (30, 3), (50, 23), (255,0,0))

img2 = img[:, :, ::-1]
roi2 = roi[:, :, ::-1]
# 121 - 1 row 2 cols 1st
plt.subplot(121),plt.imshow(img2,'gray'),plt.title('ORIGINAL')
plt.subplot(122),plt.imshow(roi2,'gray'),plt.title('Region of interest')

#cv.imshow('src', img)
#cv.waitKey(0)
#cv.destroyAllWindows() 
```

[matplotlib如何显示原色](https://blog.csdn.net/weixin_42534624/article/details/106793919)

```python
import cv2
import matplotlib.pyplot as plt

img = cv2.imread('lena.jpg')
# img[:,:,0]表示图片的蓝色通道，对一个字符串s进行翻转用的是s[::-1]，
# 同样img[:,:,::-1]就表示BGR通道翻转，变成RGB
img2 = img[:, :, ::-1]
# 或使用
# img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# 显示不正确的图
plt.subplot(121),plt.imshow(img) 
# 显示正确的图
plt.subplot(122)
plt.xticks([]), plt.yticks([]) # 隐藏x和y轴
plt.imshow(img2)

plt.show()

```

#### hist

```python
import numpy as np
rg = np.random.default_rng(1)


# Build a vector of 10000 normal deviates with variance 0.5^2 and mean 2
mu, sigma = 3, 0.5
v = rg.normal(mu, sigma, 10000)
print(v)
# Plot a normalized histogram with 50 bins
plt.hist(v, bins=50, density=True)       # matplotlib version (plot)
# Compute the histogram with numpy and then plot it
(n, bins) = np.histogram(v, bins=50, density=True)  # NumPy version (no plot)
plt.plot(.5 * (bins[1:] + bins[:-1]), n)
```

如何使用plot显示颜色分布的柱状图

老师视频里有回头再看吧，不着急