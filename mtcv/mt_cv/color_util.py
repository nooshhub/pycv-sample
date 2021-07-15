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


if __name__ == '__main__':
    bgr = [0, 0, 255]
    convert_bgr_to_rgb_str(bgr)