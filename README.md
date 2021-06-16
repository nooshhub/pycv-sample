# OpenCV-Python Tutorials 

## 学习记录

- [Introduction to OpenCV](https://docs.opencv.org/4.5.2/da/df6/tutorial_py_table_of_contents_setup.html)

  Learn how to setup OpenCV-Python on your computer!

  直接用anaconda，跳过

  

- [Gui Features in OpenCV](https://docs.opencv.org/4.5.2/dc/d4d/tutorial_py_table_of_contents_gui.html)

  Here you will learn how to display and save images and videos, control mouse events and create trackbar.

  这里最有用的就是这个trackbar了，因为我们需要它来自动变换框选的矩形的长度，这样就可以可视化的验证我们的理论了。冷热分区和电力分区，都可以在图上动态的标记出来或者渲染出来。

  我们还可以尝试添加更多的空例如，重置按钮，预处理展示按钮，也就是不同的模式了。

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



- [Core Operations](https://docs.opencv.org/4.5.2/d7/d16/tutorial_py_table_of_contents_core.html)

  In this section you will learn basic operations on image like pixel editing, geometric transformations, code optimization, some mathematical tools etc.





- [Image Processing in OpenCV](https://docs.opencv.org/4.5.2/d2/d96/tutorial_py_table_of_contents_imgproc.html)

  In this section you will learn different image processing functions inside OpenCV.



- [Feature Detection and Description](https://docs.opencv.org/4.5.2/db/d27/tutorial_py_table_of_contents_feature2d.html)

  In this section you will learn about feature detectors and descriptors

- [Video analysis (video module)](https://docs.opencv.org/4.5.2/da/dd0/tutorial_table_of_content_video.html)

  In this section you will learn different techniques to work with videos like object tracking etc.

- [Camera Calibration and 3D Reconstruction](https://docs.opencv.org/4.5.2/d9/db7/tutorial_py_table_of_contents_calib3d.html)

  In this section we will learn about camera calibration, stereo imaging etc.

- [Machine Learning](https://docs.opencv.org/4.5.2/d6/de2/tutorial_py_table_of_contents_ml.html)

  In this section you will learn different image processing functions inside OpenCV.

- [Computational Photography](https://docs.opencv.org/4.5.2/d0/d07/tutorial_py_table_of_contents_photo.html)

  In this section you will learn different computational photography techniques like image denoising etc.

- [Object Detection (objdetect module)](https://docs.opencv.org/4.5.2/d2/d64/tutorial_table_of_content_objdetect.html)

  In this section you will learn object detection techniques like face detection etc.

- [OpenCV-Python Bindings](https://docs.opencv.org/4.5.2/df/da2/tutorial_py_table_of_contents_bindings.html)

  In this section, we will see how OpenCV-Python bindings are generated 