import cv2 as cv
import numpy as np

# Helper functions and classes
from mt_cv import image_util


class Vertex:
    def __init__(self, x_coord, y_coord):
        self.x = x_coord
        self.y = y_coord
        self.d = float('inf')  # distance from source
        self.color = 0
        self.parent_x = None
        self.parent_y = None
        self.processed = False
        self.index_in_queue = None


def get_neighbors(mat, r, c):
    """获取相邻节点，上下左右，左上，右上，左下，右下
    Args:
        mat: 输入图像举证
        r: 行
        c: 列
    """
    shape = mat.shape
    neighbors = []

    # 保证相邻节点都是在图像边界内
    # [-1,-1] [0, -1] [1,-1]
    # [-1, 0]  [0, 0] [1, 0]
    # [-1, 1] [0,  1] [1, 1]

    r_min = 1
    r_max = shape[0] - 2
    c_min = 1
    c_max = shape[1] - 2

    # 上左
    # if r > r_min and c > c_min and not mat[r - 1][c - 1].processed:
    #     neighbors.append(mat[r - 1][c - 1])
    # 上
    if r > r_min and not mat[r - 1][c].processed:
        neighbors.append(mat[r - 1][c])
    # 上右
    # if r > r_min and c < c_max and not mat[r - 1][c + 1].processed:
    #     neighbors.append(mat[r - 1][c + 1])

    # 左
    if c > c_min and not mat[r][c - 1].processed:
        neighbors.append(mat[r][c - 1])
    # 右
    if c < c_max and not mat[r][c + 1].processed:
        neighbors.append(mat[r][c + 1])

    # 下左
    # if r < r_max and c > c_min and not mat[r + 1][c - 1].processed:
    #     neighbors.append(mat[r + 1][c])
    # 下
    if r < r_max and not mat[r + 1][c].processed:
        neighbors.append(mat[r + 1][c])
    # 下右
    # if r < r_max and c < c_max and not mat[r + 1][c + 1].processed:
    #     neighbors.append(mat[r + 1][c])

    return neighbors


def bubble_up(queue, index):
    if index <= 0:
        return queue
    p_index = (index - 1) // 2
    if queue[index].d < queue[p_index].d:
        queue[index], queue[p_index] = queue[p_index], queue[index]
        queue[index].index_in_queue = index
        queue[p_index].index_in_queue = p_index
        queue = bubble_up(queue, p_index)
    return queue


def bubble_down(queue, index):
    length = len(queue)
    lc_index = 2 * index + 1
    rc_index = lc_index + 1
    if lc_index >= length:
        return queue
    if lc_index < length <= rc_index:  # just left child
        if queue[index].d > queue[lc_index].d:
            queue[index], queue[lc_index] = queue[lc_index], queue[index]
            queue[index].index_in_queue = index
            queue[lc_index].index_in_queue = lc_index
            queue = bubble_down(queue, lc_index)
    else:
        small = lc_index
        if queue[lc_index].d > queue[rc_index].d:
            small = rc_index
        if queue[small].d < queue[index].d:
            queue[index], queue[small] = queue[small], queue[index]
            queue[index].index_in_queue = index
            queue[small].index_in_queue = small
            queue = bubble_down(queue, small)
    return queue


def get_distance(img, u, v):
    return 0.1 + (float(img[v][0]) - float(img[u][0])) ** 2 + (float(img[v][1]) - float(img[u][1])) ** 2 + \
           (float(img[v][2]) - float(img[u][2])) ** 2


def draw_path(img, path, thickness=2):
    """path is a list of (x,y) tuples"""
    x0, y0 = path[0]
    for vertex in path[1:]:
        x1, y1 = vertex
        cv.line(img, (x0, y0), (x1, y1), (255, 0, 0), thickness)
        x0, y0 = vertex


def find_shortest_path(img, src, dst):
    """找出最短路径

    Args:
        img: 输入图像
        src: 起始点
        dst: 终点

    Returns:
        返回最短路径
    """
    # min-heap priority queue
    pq = []

    # 起点
    source_x = src[0]
    source_y = src[1]

    # 终点
    dest_x = dst[0]
    dest_y = dst[1]

    # 图像行列
    imagerows, imagecols = img.shape[0], img.shape[1]

    # 初始化一个矩阵，初始点vertex，坐标x，y，以及间距d
    matrix = np.full((imagerows, imagecols), None)  # access by matrix[row][col]
    for r in range(1, imagerows - 1):
        for c in range(1, imagecols - 1):
            matrix[r][c] = Vertex(c, r)
            matrix[r][c].index_in_queue = len(pq)
            pq.append(matrix[r][c])
    matrix[source_y][source_x].d = 0

    pq = bubble_up(pq, matrix[source_y][source_x].index_in_queue)
    while len(pq) > 0:
        u = pq[0]
        u.processed = True
        pq[0] = pq[-1]
        pq[0].index_in_queue = 0
        pq.pop()

        pq = bubble_down(pq, 0)

        neighbors = get_neighbors(matrix, u.y, u.x)

        for v in neighbors:
            dist = get_distance(img, (u.y, u.x), (v.y, v.x))
            if u.d + dist < v.d:
                v.d = u.d + dist
                v.parent_x = u.x
                v.parent_y = u.y
                idx = v.index_in_queue
                pq = bubble_down(pq, idx)
                pq = bubble_up(pq, idx)

    # 利用计算出的终点的parent，反向生成最短路径
    path = []
    iter_v = matrix[dest_y][dest_x]
    path.append((dest_x, dest_y))
    while iter_v.y != source_y or iter_v.x != source_x:
        path.append((iter_v.x, iter_v.y))
        iter_v = matrix[iter_v.parent_y][iter_v.parent_x]

    path.append((source_x, source_y))
    return path


if __name__ == '__main__':
    # image_folder = image_util.img_abs_path('/images/tmp/7bf573e0-4ce4-49ee-8e7a-cf5caf525a94')
    image_folder = image_util.img_abs_path('/images/tmp/5abf9a33-d9f6-4b77-bd43-94e1d52d57ae')
    img_path = image_folder + '/road/thinned.png'
    draw_img_path = image_folder + '/hot_cold.png'

    src = cv.imread(img_path)
    rows, cols = src.shape[:2]

    # 准备起点和终点数据
    start_coords = []
    for col in range(1, cols - 1):
        color = src[1][col]
        if color[0] == 255:
            start_coords.append([col, 1])

    end_coords = []
    row_end = rows - 2
    for col in range(1, cols - 1):
        color = src[row_end][col]
        if color[0] == 255:
            end_coords.append([col, row_end])

    e1 = cv.getTickCount()

    # demo3_1 start 0 end 0,1 should fail 2,3 should successs
    path = find_shortest_path(src, start_coords[0], end_coords[2])

    e2 = cv.getTickCount()
    time = (e2 - e1) / cv.getTickFrequency()
    print('takes ', time)

    copy = cv.imread(draw_img_path)
    draw_path(copy, path)
    image_util.generate_img(image_folder, '/road/path.png', copy)

