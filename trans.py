# -*- coding: UTF-8 -*-
import json

import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
import time
from skimage import io



def get_array_opencv(img_path, reverse=False):
    # opencv 先灰度再二值
    # start = time.time()
    # img = cv2.imread(img_path)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # img = mpimg.imread(img_path)
    # img = np.asarray(Image.open(img_path))
    img = np.asarray(io.imread(img_path))
    # print(type(img))
    # print(img.shape)
    # end = time.time()
    # print("读取要花的时间是", (end - start) * 1000, "毫秒")

    # exit()

    # 二值化
    # ret, im_array = cv2.threshold(gray, 125, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # ret, im_array = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # 这个效果最好
    # print("cv2.THRESH_BINARY + cv2.THRESH_OTSU", cv2.THRESH_BINARY + cv2.THRESH_OTSU) # 8
    ret, im_array = cv2.threshold(img, 0, 255, 16)  # 这个效果最好

    # cv2.imwrite(r"E:\PushUP\P003_3\test\opencv.png", im_array)
    if reverse:
        im_array = ~im_array
    return im_array,img

def get_h(im_array, x):
    # h = 0
    # for i in range(len(im_array[0]) - 1):
    #     if im_array[x][i] == 0:
    #         h = i + 10
    #         break
    h = np.where(im_array[x] == 0)[0][0]

    return h


def get_h_255(im_array, x):
    h = 0
    for i in range(len(im_array[0]) - 1):
        if im_array[x][i] == 255:
            h = i + 10
            break

    return h


def get_number(path):
    # 得到第一张图片的编号
    first_file = os.listdir(path)[0]
    last_file = os.listdir(path)[-1]
    m = 0
    # print(first_file)
    for j in range(len(first_file)):
        if first_file[j].isdigit():
            continue
        elif first_file[j].isalpha():
            m = j
            break
    start = int(first_file[:m])
    end = int(last_file[:m])
    return start, end


def clock(func):
    def clocked(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        # print("函数", func.__name__, "运行了", (end - start)*1000, "毫秒")
        return result

    return clocked


# @clock
# def get_array_opencv(img_path, reverse=False):
#     # opencv 先灰度再二值
#     img = cv2.imread(img_path)
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     # 二值化
#     # ret, im_array = cv2.threshold(gray, 125, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
#     # ret, im_array = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # 这个效果最好
#     # print("cv2.THRESH_BINARY + cv2.THRESH_OTSU", cv2.THRESH_BINARY + cv2.THRESH_OTSU) # 8
#     ret, im_array = cv2.threshold(gray, 0, 255, 16)  # 这个效果最好
#     if reverse:
#         im_array = ~im_array
#     return im_array,img


def draw_circle_parameter_equation(x=0, y=0, r=1, s=360, c='r', w=0.5):
    '''
    :param x: 圆的横坐标,默认0
    :param y: 圆的纵坐标，默认0
    :param r: 圆的半径，默认1
    :param s: 插值，然后把插值后的点连成线，默认200，看起来已经很像圆了
    :param c: 颜色，默认红色
    :return:
    '''
    theta = np.linspace(0, 2 * np.pi, s)
    x1 = x + r * np.cos(theta)
    y1 = y + r * np.sin(theta)
    plt.plot(x1, y1, color=c, linewidth=w)


def show_picture(x, y, my_title=None, save=False, source_path=None):
    # 注意，save要在show之前，否则保存下来是白板，什么都没有
    plt.figure()
    plt.plot(x, y)
    plt.title = my_title
    if save:
        suffix = ".png"
        fig_name = '{}{}'.format(my_title, suffix)
        fig_path_out = os.path.join(source_path, fig_name)
        plt.savefig(fig_path_out)
    plt.show()
    plt.close()


def write_json(my_dict, json_path):
    # dict = {'name': '张三', 'age': 18, 'sex': '男'}

    with open(json_path, 'w', encoding='utf8') as fp:
        json.dump(my_dict, fp, ensure_ascii=False)


def read_json(json_path):
    with open(json_path, 'r', encoding='utf8') as fp:
        my_dict = json.load(fp)
    return my_dict


def findIntersection(x1, y1, x2, y2, x3, y3, x4, y4):
    px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / (
            (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
    py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / (
            (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
    return [px, py]
