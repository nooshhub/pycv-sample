import numpy as np


def convert_bgr_to_rgb_str(bgr_list):
    """将bgr列表转换成string

    Args:
        bgr_list: bgr列表，ex: [0, 0, 255]

    Returns:
        rgb_str: ex: "rgb(255,0,0)"
    """
    rgb_str_list = [str(x) for x in reversed(bgr_list)]
    rgb_str = 'rgb(' + ','.join(rgb_str_list) + ')'
    # print(rgb_str)
    return rgb_str


def random_color(memo=None):
    """生成随机颜色"""

    b, g, r = np.random.randint(50, 250), np.random.randint(50, 250), np.random.randint(50, 250)

    if memo is not None:
        color_str = "_".join([str(b), str(g), str(r)])
        while color_str in memo:
            b, g, r = np.random.randint(50, 250), np.random.randint(50, 250), np.random.randint(50, 250)
            color_str = "_".join([str(b), str(g), str(r)])
        memo.add(color_str)

    return b, g, r


def color_id(bgr_color):
    """输入bgr color，可以是一个tuple，array，或者numpy array"""
    bgr_tuple = str(bgr_color[0]), str(bgr_color[1]), str(bgr_color[2])
    return "_".join(bgr_tuple)


if __name__ == '__main__':
    # bgr = np.array([0, 0, 255])
    bgr = [0, 0, 255]
    print(color_id(bgr))
