# OpenCV-Python Tutorials 



## 安装

anaconda全家桶



国内镜像加速

https://blog.csdn.net/sinat_21591675/article/details/82770360

用阿里的



使用pip之前新建一个C:\Users\lenovo\pip\pip.ini

[global]

index-url = http://mirrors.aliyun.com/pypi/simple/

[install]

trusted-host = mirrors.aliyun.com



安装 

pip install opencv-python==4.5.1.48

pip install opencv-contrib-python==4.5.1.48

设置jupyter-notebook的root为我们的代码根目录，在jupyter启动的快捷方式里修改 目标

![设置jupyter-notebook的root为我们的代码根目录](image-md/jupytor-root.png)

启动jupyter开始欢快的玩耍！



## 代码笔记

6-16 开始按照官网的教程来用python实现需求3，适当了解一些基本的python语法

[编码规范](https://www.runoob.com/w3cnote/google-python-styleguide.html)

[Code Cheat Sheet](opencv-tutorial-md/CodeCheatSheet.md)

[1GuiFeaturesTrackBar.ipynb](http://localhost:8888/notebooks/opencv-tutorial-md/1GuiFeaturesTrackBar.ipynb)

[2Core.ipynb](http://localhost:8888/notebooks/opencv-tutorial-md/2Core.ipynb)

[3ImageProcessCannyEdges.ipynb](http://localhost:8888/notebooks/opencv-tutorial-md/3ImageProcessCannyEdges.ipynb)

[3ImageProcessMorphological.ipynb](http://localhost:8888/notebooks/opencv-tutorial-md/3ImageProcessMorphological.ipynb)

[3ImageProcessTemplateMatch.ipynb](http://localhost:8888/notebooks/opencv-tutorial-md/3ImageProcessTemplateMatch.ipynb)

[3ImageProcessThresholdSmooth.ipynb](http://localhost:8888/notebooks/opencv-tutorial-md/3ImageProcessThresholdSmooth.ipynb)

[3ImageProcessWaterSehed.ipynb](http://localhost:8888/notebooks/opencv-tutorial-md/3ImageProcessWaterSehed.ipynb)



6-19 出基本成果 python YYDS

[Partition2ShootingStar.ipynb](http://localhost:8888/notebooks/hotcold/Partition2ShootingStar.ipynb)

还有些bug，不过冷热分区，合并分区到同一个冷热分区的初步架子已经成型。



## 参考官方教程

- [Introduction to OpenCV](https://docs.opencv.org/4.5.2/da/df6/tutorial_py_table_of_contents_setup.html)

  Learn how to setup OpenCV-Python on your computer!

  直接用anaconda，跳过

  入门Py常用资料：

1. A Quick guide to Python - [A Byte of Python](http://swaroopch.com/notes/python/)
2. [NumPy Quickstart tutorial](https://numpy.org/devdocs/user/quickstart.html)
3. [NumPy Reference](https://numpy.org/devdocs/reference/index.html#reference)
4. [OpenCV Documentation](http://docs.opencv.org/)
5. [OpenCV Forum](https://forum.opencv.org/)



- [Gui Features in OpenCV](https://docs.opencv.org/4.5.2/dc/d4d/tutorial_py_table_of_contents_gui.html)

  Here you will learn how to display and save images and videos, control mouse events and create trackbar.

  这里最有用的就是这个trackbar了，因为我们需要它来自动变换框选的矩形的长度，这样就可以可视化的验证我们的理论了。冷热分区和电力分区，都可以在图上动态的标记出来或者渲染出来。

  ~~我们还可以尝试添加更多的空例如，重置按钮，预处理展示按钮，也就是不同的模式了。Button需要QT，直接放弃，安装QT很耗时~~
  
  那就将图片预处理了，保存下来，然后我们基于预处理的图片进行操作
  
  状态：100%



- [Core Operations](https://docs.opencv.org/4.5.2/d7/d16/tutorial_py_table_of_contents_core.html)

  In this section you will learn basic operations on image like pixel editing, geometric transformations, code optimization, some mathematical tools etc.

状态：100% 必须掌握 numpy matplotlib



- [Image Processing in OpenCV](https://docs.opencv.org/4.5.2/d2/d96/tutorial_py_table_of_contents_imgproc.html)

  In this section you will learn different image processing functions inside OpenCV.

状态：100%

![partition1 success](hotcold/partition1hotcold.png)

![partition2 still have bugs](hotcold/partition2hotcoldWithBugs.png)

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



## 框架 Tensorflow/Keras/PyTorch

看看这些DL的框架能不能有些帮助，貌似都在做预测和分类识别，对目前的需求没有，可能后期的OCR会有帮助，就是做识别的。

[Tensorflow2](tensorflow/Tensorflow2.md)

[手撸神经网络](https://www.bilibili.com/video/BV1m4411x7KU/?spm_id_from=333.788.recommend_more_video.5)，有利于全局的理解神经网络和熟悉numpy的高级用法

[Keras](tensorflow/Keras.md)

[Keras英语视频 练习相关专业的口语和听力](https://www.bilibili.com/video/BV1g64y1S7Kz/?spm_id_from=333.788.recommend_more_video.1)

[PyTorch](tensorflow/PyTorch.md)





## 输出地块色块面积和父子关系

```json
{
    "area":50000, /*最外面的是总面积*/
    "data":[ /*data是地块的信息*/
        {
            "area":330,
            "color":"(255,255,255)",
            "points":[
                {
                    "xAxis":22.4,
                    "yAxis":44.34
                }
            ],
            "children":[ /*children是色块的信息*/
                {
                    "area":330,
                    "color":"(255,255,255)",
                    "points":[
                        {
                            "xAxis":22.4,
                            "yAxis":44.34
                        }
                    ]
                }
            ]
        }
    ]
}
```

<img src="image-md\bock-sample.png" alt="image-20210627121101413" style="zoom:50%;" />

比如蓝色框出来的就是地块

然后绿色框出来的是色块



学习opencv3中文版 

第14章 轮廓  canny是布尔矩阵 findContours将canny的布尔矩阵转换成坐标形式的矩阵

307 - Canny 的threashold怎么计算 



图像处理、分析与机器视觉  

全部



## road detection/ Extract road from map / aerial image / satellite image

回到道路检测的问题上来

https://stackoverflow.com/questions/62623836/simple-way-to-detect-street-area-in-google-map-images-aerial-images

https://www.cs.toronto.edu/~hinton/absps/road_detection.pdf

https://towardsdatascience.com/satellite-coasts-detection-model-with-python-and-opencv-28d1b4b8474e

