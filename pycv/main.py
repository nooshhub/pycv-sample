def print_hi(name):
    color_sample_list = [{'label': '居住', 'rgb': (250, 250, 0),
                          'rgb_label': '黄', 'h_range': [26, 34], 's_range': [43, 255], 'v_range': [46, 255]
                          },
                         {'label': '办公', 'rgb': (250, 0, 250),
                          'rgb_label': '紫红', 'h_range': [125, 155], 's_range': [43, 255], 'v_range': [46, 255]
                          },
                         {'label': '商业', 'rgb': (250, 9, 9),
                          'rgb_label': '红', 'h_range': [0, 10], 's_range': [43, 255], 'v_range': [46, 255]
                          },
                         {'label': '商业2', 'rgb': (249, 9, 15),
                          'rgb_label': '红', 'h_range': [156, 180], 's_range': [43, 255], 'v_range': [46, 255]
                          },
                         {'label': '工业', 'rgb': (201, 103, 39),
                          'rgb_label': '棕', 'h_range': [11, 25], 's_range': [43, 255], 'v_range': [46, 255]
                          },
                         {'label': '绿地', 'rgb': (0, 250, 0),
                          'rgb_label': '绿', 'h_range': [35, 77], 's_range': [43, 255], 'v_range': [46, 255]
                          },
                         {'label': '湖泊', 'rgb': (0, 250, 250),
                          'rgb_label': '蓝', 'h_range': [100, 124], 's_range': [43, 255], 'v_range': [46, 255]
                          }]

    print(color_sample_list)

    offset = 1

    for color_sample in color_sample_list:
        rgb_tuple = color_sample['rgb']
        r, g, b = rgb_tuple[0] / 255, rgb_tuple[1] / 255, rgb_tuple[2] / 255

        rgb_min = min(r, g, b)
        v = max(r, g, b)
        if v != 0:
            s = (v - rgb_min) / v
        else:
            s = 0

        if r == v:
            h = (g - b) / (v - rgb_min) * 60
        if g == v:
            h = 120 + (b - r) / (v - rgb_min) * 60
        if b == v:
            h = 240 + (r - g) / (v - rgb_min) * 60
        if h < 0:
            h = h + 360

        print(color_sample['label'], color_sample['rgb_label'])
        print(h / 2, ',', s * 255, ',', v * 255)
        print('([', h / 2, ',', s * 255 - offset, ',', v * 255 - offset, '], [', color_sample['h_range'][1], ',',
              color_sample['s_range'][1], ',', color_sample['v_range'][1], '])')
        print('([', h / 2, ',',
              color_sample['s_range'][0], ',',
              color_sample['v_range'][0], '], [',
              color_sample['h_range'][1], ',',
              color_sample['s_range'][1], ',',
              color_sample['v_range'][1], '])')


if __name__ == '__main__':
    print_hi('PyCharm')
