import os
import platform

# TODO 自动找出项目根目录
# 公司
# MTCV_HOME = 'D:/anaconda3/pycv-sample/mtcv'

# 家
MTCV_HOME = 'D:/opencv/pynotebook/mtcv'

# server use root /
# MTCV_HOME = ''

if __name__ == '__main__':
    print(platform.system())
    print(os.environ['MTCV_HOME'])
