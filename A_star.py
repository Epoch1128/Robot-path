import math
import numpy as np
from matplotlib import pyplot as plt


def A_star_algorithm(area, start_point, finish_point, directions=8):
    """
    :param directions: 八邻域搜索or四邻域搜索
    :param area: 区域,01表示的地图,数组类型
    :param start_point: 起始点
    :param finish_point: 终点
    :return:
    """
    # Initialize
    start_point[-1] = area.shape[-1] - start_point[-1] - 1
    finish_point[-1] = area.shape[-1] - finish_point[-1] - 1
    if area[start_point[0]][start_point[1]] == 1 or area[finish_point[0]][finish_point[1]] == 1:
        print('The start or finish point is hinder itself! You select a wrong point to start or finish!')
        return
    cost = [[start_point, distance(start_point, finish_point), None]]
    save = [[start_point, distance(start_point, finish_point), None]]
    dx = [0, 0, -1, 1, 1, 1, -1, -1]
    dy = [1, -1, 0, 0, 1, -1, 1, -1]
    iterable = 0
    path = []
    x = []
    y = []
    print("The process of searching is shown as follow:")
    while len(cost) != 0:
        temp = cost[0][0]
        plt.scatter(temp[0], temp[1])
        path.append(cost[0])
        cost.pop(0)
        iterable += 1
        if distance(temp, finish_point) == 0:
            break
        print('Closed: ({}, {})'.format(temp[0], area.shape[1] - temp[1] - 1))
        for k in range(directions):
            if in_map(area, [temp[0] + dx[k], temp[1] + dy[k]]):
                if area[temp[0] + dx[k]][temp[1] + dy[k]] == 0 and is_in_list(list1=save, key=[temp[0] + dx[k], temp[1] + dy[k]]) is False:
                    cost.append(
                        [[temp[0] + dx[k], temp[1] + dy[k]],
                         iterable + distance([temp[0] + dx[k], temp[1] + dy[k]], finish_point), temp])
                    save.append(
                        [[temp[0] + dx[k], temp[1] + dy[k]],
                         iterable + distance([temp[0] + dx[k], temp[1] + dy[k]], finish_point), temp])
        cost.sort(key=lambda d: d[1])
        print('Open:')
        for item in cost:
            print('({}, {})'.format(item[0][0], area.shape[1] - item[0][-1] - 1))
    point = finish_point
    if len(cost) is not 0:
        while point is not None:
            for item in path:
                if point[0] == item[0][0] and point[1] == item[0][1]:
                    x.append(point[0])
                    y.append(point[1])
                    point = item[-1]
                    break
        plt.plot(x, y, 'black')
    else:
        start_point[-1] = area.shape[-1] - start_point[-1] - 1
        finish_point[-1] = area.shape[-1] - finish_point[-1] - 1
        print('Fail to find a path from {} to {}!'.format(start_point, finish_point))


def distance(pointA, pointB):
    total = 0
    for x, y in zip(pointA, pointB):
        total += math.fabs(x - y)
    return total


def in_map(area, point):
    for i, item in enumerate(point):
        if item > area.shape[i] - 1 or item < 0:
            return False
    return True


def set_maze(length, width, point_list):
    maze = np.zeros((length, width), dtype='int')
    for hind in point_list:
        maze[hind[0]][width - hind[1] - 1] = 1
    plt.figure()
    for item in point_list:
        plt.scatter(item[0], width - item[1] - 1, marker='x', c='black')
    return maze


def is_in_list(list1, key):
    for item in list1:
        if key[0] == item[0][0] and key[1] == item[0][1]:
            return True
    return False


if __name__ == '__main__':
    hinder = [[0, 1], [0, 9], [2, 3], [2, 7], [2, 9], [3, 1], [4, 5], [5, 2], [6, 3], [6, 7], [8, 1], [8, 3], [8, 9]]
    loc = set_maze(10, 10, hinder)
    start = [3, 3]
    finish = [9, 9]
    A_star_algorithm(area=loc, start_point=start, finish_point=finish)
    plt.xlim(-1, loc.shape[0])
    plt.ylim(-1, loc.shape[1])
    plt.axis(emit=False)
    plt.grid()
    plt.show()