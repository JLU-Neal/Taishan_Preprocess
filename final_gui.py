# -*- coding: UTF-8 -*-
from natsort import natsorted, ns
from scipy import signal  # 滤波等
from trans import *
import math
from PreProcess import PreProcess
from shuchutupian2 import *


# from numba import jit


# @clock
def find_angel(img_array, foot_x, knee_x, foot_y_criterion, foot_y_list, knee_expand_length=20, thigh_threshold=0.757,
               back1_threshold=0.546, back2_threshold=0.702):
    '''
    :param img_array: 图像矩阵
    :param foot_x: 第一张图的脚横坐标
    :param knee_x: 第一张图的膝盖横坐标
    :param knee_expand_length: 计算膝盖横坐标前后拓展的距离范围
    :param thigh_threshold: 大腿横坐标阈值，是脚横坐标与后背1之间的比重
    :param back1_threshold: 后背1横坐标阈值，占整幅图像的比重
    :param back2_threshold: 后背2横坐标阈值，占整幅图像的比重
    :return: 返回三个角度
    '''
    x = []
    y = []

    width, height = img_array.shape
    back1_x = int(width * back1_threshold)
    back2_x = int(width * back2_threshold)
    for i in range(foot_x, back1_x):
        body_where = np.where(img_array[i] == 255)
        x.append(i)
        if len(body_where[0]) > 0:
            y.append(height - body_where[0][0])
        else:
            y.append(height)
    # y = signal.savgol_filter(y, 15, 2)

    f1 = np.polyfit(x, y, 5)
    p1 = np.poly1d(f1)
    # 不计算k，b

    # k = p1(1) - p1(0)
    k = float((p1(x[-1]) - p1(x[0])) / (x[-1] - x[0]))
    b = p1(x[-1]) - k * x[-1]
    # knee_y = p1(knee_x)
    # foot_y = p1(foot_x)
    if (foot_y_criterion - 1 < p1(foot_x) < foot_y_criterion + 1):
        foot_y = p1(foot_x)
    else:
        foot_y = foot_y_list[-1]
    foot_y_list.append(foot_y)
    # foot_y = np.where(img_array[foot_x] == 255)
    # foot_y = height - foot_y[0].mean()

    distance = 0
    # bb = np.math.sqrt(1 + k * 2)
    # start = time.time()
    for i in range(knee_x - knee_expand_length, knee_x + knee_expand_length):
        new_distance = k * i - p1(i) + b
        if new_distance > distance:
            distance = new_distance
            knee_x = i
    # end = time.time()
    # print("循环用了", (end - start) * 1000, "毫秒")
    knee_y = p1(knee_x)

    # z_sum foot knee leg two backs
    back1_y = np.where(img_array[back1_x] == 255)[0][0]
    back2_y = np.where(img_array[back2_x] == 255)[0][0]
    # 这里的 foot_y 两种选择，一种是get_h得到，一种是拟合曲线得到
    thigh_x = int(foot_x + len(x) * thigh_threshold)
    z_sum = [[foot_x, foot_y], [knee_x, knee_y], [thigh_x, p1(thigh_x)], [back1_x, height - back1_y],
             [back2_x, height - back2_y]]

    k1 = (z_sum[1][1] - z_sum[0][1]) / (z_sum[1][0] - z_sum[0][0])  # 斜率1
    k2 = (z_sum[2][1] - z_sum[1][1]) / (z_sum[2][0] - z_sum[1][0])  # 斜率2
    k3 = (z_sum[4][1] - z_sum[3][1]) / (z_sum[4][0] - z_sum[3][0])  # 斜率3
    k4 = (z_sum[4][1] - z_sum[0][1]) / (z_sum[4][0] - z_sum[0][0])  # 斜率4
    # print("k4",k4)
    # print("第一种方法计算角度用了", (end - start) * 1000, "毫秒") 10000次 246 毫秒
    angle1 = 180 - int(math.fabs(np.arctan((k1 - k2) / (float(1 + k1 * k2))) * 180 / np.pi) + 0.5)
    angle2 = 180 - int(math.fabs(np.arctan((k2 - k3) / (float(1 + k2 * k3))) * 180 / np.pi) + 0.5)
    angle3 = 0 if k4 <= 0 else int(math.fabs(np.arctan(k4) * 180 / np.pi) + 0.5)
    # print("第二种方法计算角度用了", (end1 - start1) * 1000, "毫秒") 10000次 86.76767349243164 毫秒

    # print(angle1, angle2, angle3)
    return angle1, angle2, angle3, z_sum


def find_foot_y(foot_x, height, imgs_path, png_names, reverse, left_reverse):
    foot_y_list = []
    for img_name in png_names:
        # print("img_name", img_name)
        depth_bg = cv2.imread(imgs_path + "/" + img_name, -1)
        pp = PreProcess()
        img2 = pp.exec(depth_bg)
        img2 = img2.astype("uint8")
        ret, img2 = cv2.threshold(img2, 0, 255, 16)
        if left_reverse:
            img2 = np.flip(img2, axis=1)
        if reverse:
            img2 = ~img2
        # img2 = np.flip(img2, axis=1)

        # img_path = os.path.join(imgs_path, img_name)
        # print("img_path", img_path)
        # if reverse:
        #     img2 = ~img2
        # start4 = time.time()
        # img_array, img3 = get_array_opencv(img_path, reverse=True)
        img_array = img2.transpose()
        mmm = np.where(img_array[foot_x] == 0)[0]
        if len(mmm) == 0:
            foot_y = foot_y_list[-1]
        else:
            foot_y = height - mmm[0]
        print("foot_y", foot_y)
        foot_y_list.append(foot_y)
    foot_y_list.sort()
    return foot_y_list[len(foot_y_list) // 2]


def get_foot_points(img_array, foot_threshold_start=0.05, foot_threshold_end=0.15):
    # width, height = len(img_array), len(img_array[0])
    width, height = img_array.shape
    foot_start = int(width * foot_threshold_start)
    foot_end = int(width * foot_threshold_end)
    y = [0] * width
    x_max1 = 0
    foot_x = 0
    for i in range(foot_start, foot_end):
        y[i] = len(np.where(img_array[i] == 0)[0])
        if x_max1 <= y[i]:
            x_max1 = y[i]
            foot_x = i
    # print(foot_x)
    return foot_x


def get_knee_point(img_array, foot_x, back1_threshold=0.546):
    x = []
    y = []
    width, height = img_array.shape
    knee_x = 0
    back1_x = int(width * back1_threshold)
    for i in range(foot_x, back1_x):
        body_where = np.where(img_array[i] == 0)
        if len(body_where[0]) == 0:
            x.append(i)
            y.append(y[-1])
            continue
        x.append(i)
        y.append(height - body_where[0][0])
    f1 = np.polyfit(x, y, 10)

    p1 = np.poly1d(f1)
    k = float((p1(x[-1]) - p1(x[0])) / (x[-1] - x[0]))
    b = p1(x[-1]) - k * x[-1]
    distance = 0
    for i in range(foot_x, 250):
        new_distance = k * i + b - p1(i)
        if new_distance > distance:
            distance = new_distance
            knee_x = i

    return knee_x


def get_shoulder_point(img_array, shoulder_threshold_start=0.4, shoulder_threshold_end=1):
    width, height = img_array.shape
    shoulder_start = int(width * shoulder_threshold_start)
    shoulder_end = int(width * shoulder_threshold_end)
    y = [0] * width
    x_max = 0
    shoulder_x_list = []
    for i in range(shoulder_start, shoulder_end):
        y[i] = len(np.where(img_array[i] == 0)[0])
        if x_max < y[i]:
            shoulder_x_list = [i]
            x_max = y[i]
        elif x_max == y[i]:
            shoulder_x_list.append(i)
    print("shoulder_x_list", shoulder_x_list)
    shoulder_x = shoulder_x_list[len(shoulder_x_list) // 2]
    return shoulder_x


# @clock
def get_peak(shoulder_y_list, height=0, distance=0, window_length=15, polyorder=2):
    tmp_smooth = signal.savgol_filter(shoulder_y_list, window_length, polyorder)
    num_peak = signal.find_peaks(tmp_smooth, height=height, distance=distance)
    return num_peak[0]


# @clock
def judge_by_angel(knee_angel_list, hip_angel_list, action_list, action_right_dict, knee_right_angel=150,
                   hip_right_angel=150,
                   right_threshold=0.8):
    action_list_new = []
    for action_index in range(len(action_list)):
        action = action_list[action_index]
        fig_right_count = 0
        action_start = action[0] - 1
        action_end = action[1] - 1
        for i in range(action_start, action_end + 1):
            if knee_angel_list[i] >= knee_right_angel and hip_angel_list[i] >= hip_right_angel:
                fig_right_count += 1
        accuracy = fig_right_count / (action_end - action_start + 1)
        # print("俯卧撑", action, "正确的数量有", fig_right_count)
        # print("俯卧撑", action, "错误的数量有", fig_wrong_count)
        # print("俯卧撑", action, "的正确率为", accuracy)
        action_right_dict[action] = round(accuracy, 2)
        if accuracy >= right_threshold:
            action_list_new.append(action)
    return action_list_new, action_right_dict


# @clock
def judge_by_gap_angel(shoulder_angel_list, action_list, action_right_dict, gap_right_angel=10):
    action_list_new = []
    for action_index in range(len(action_list)):
        action = action_list[action_index]
        action_start = action[0] - 1
        action_end = action[1] - 1
        for i in range(action_start, action_end + 1):
            if shoulder_angel_list[i] <= gap_right_angel:
                action_list_new.append(action)
                action_right_dict[action] = 100
                break
    return action_list_new, action_right_dict


# @clock
def get_action_list(peak_list, trough_list):
    action_list = []
    action_right_dict = {}
    k = 0
    for trough_i in range(len(trough_list)):
        if k == len(peak_list):
            break
        for peak_j in range(k, len(peak_list)):
            if trough_list[trough_i] > peak_list[peak_j]:
                continue
            else:
                action = (peak_list[peak_j - 1], peak_list[peak_j] - 1)
                if peak_list[peak_j - 1] >= peak_list[peak_j] - 1:
                    continue
                else:
                    action_list.append(action)
                    action_right_dict[action] = 0
                    k = peak_j + 1
                    break

    return action_list, action_right_dict


##################################################################################


# if __name__ == '__main__':
def main(dir_pic, dir_out_pic, start_num,left_reverse):
    '''
    输入：深度图
    输出：判别结果
    Step1:先计算第一张图，调用动态链接库，输入一张深度图的数据，得到这张图的rgb图像矩阵（因为中间过程生成的rgb图像不会保存）
          要计算初始值的是 脚和肩的横坐标。
    Step2: 后面开始

    0或者255，分别代表黑色和白色。
    '''
    start = time.time()
    foot_threshold_start = 0.05
    foot_threshold_end = 0.15
    knee_expand_length = 20
    thigh_threshold = 0.720
    back1_threshold = 0.770
    back2_threshold = 0.880
    shoulder_threshold_start = 0.6
    shoulder_threshold_end = 1

    shoulder_height_threshold = 15

    source_path = r"C:\Users\yanhao\Desktop\taishan_project\test_0_norm _del"
    P_list = ["P003_3", "P004", "P005", "P006", "P007", "P008", "P009", "P010"]
    P = "P003_3"
    origin = "origin4"
    suffix_png = ".png"
    suffix_json = ".json"

    reverse = True
    # left_reverse = False

    foot_y_criterion = -1
    foot_x = -1
    knee_x = -1
    shoulder_x = -1
    shoulder_y_list = []
    shoulder_y_reverse_list = []
    angels_list = []
    knee_angel_list = []
    hip_angel_list = []
    shoulder_angel_list = []

    standard = "standard"
    # 腿踝，屁股，深度，标准正确率
    standard_dict = {standard: [155, 148, 7, 0.8]}

    imgs_path = os.path.join(dir_pic)
    # nums = len(os.listdir(imgs_path))

    count = 1
    # end = ["470norm.png","432norm.png","620norm.png","528norm.png","596norm.png","278norm.png","620norm.png","620norm.png"]
    start_images = start_num
    # end_images = end_num
    # end = [1:340,2:283,3:266,5:345]

    png_names = os.listdir(imgs_path)
    png_names = natsorted(png_names, alg=ns.PATH)
    nums = 0

    foot_y_list = []
    foot_count = 0
    ####################################################
    pp = PreProcess()
    depth_first = cv2.imread(imgs_path + "/" + png_names[start_images+60], -1)
    pp.exec(depth_first)
    #####################################################
    for img_name in png_names[start_images:]:
        print("img_name", img_name)
        nums += 1
        # try:
        depth_bg = cv2.imread(imgs_path + "/" + img_name, -1)

        # pp = PreProcess()
        img2 = pp.exec(depth_bg)
        img2 = img2.astype("uint8")
        ret, img2 = cv2.threshold(img2, 0, 255, 16)
        # img2 = np.flip(img2, axis=1)

        # img_path = os.path.join(imgs_path, img_name)
        # print("img_path", img_path)
        if left_reverse:
            img2 = np.flip(img2, axis=1)
        if reverse:
            img2 = ~img2

        # start4 = time.time()
        # img_array, img3 = get_array_opencv(img_path, reverse=True)
        img_array = img2.transpose()
        # cv2.imshow('image', img2)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # print(img_array.shape)

        end4 = time.time()
        # all_time4 = (end4 - start4) * 1000
        # print("加载图像要", all_time4, "毫秒")
        # height, width = len(img_array), len(img_array[0])
        width, height = img_array.shape

        if foot_x <= 0 or knee_x <= 0 or shoulder_x <= 0:
            # img_array = img_array.transpose()
            # print(img_name)
            # im_np = np.array(img_array)
            start3 = time.time()
            foot_x = get_foot_points(img_array, foot_threshold_start=foot_threshold_start,
                                     foot_threshold_end=foot_threshold_end)
            # print("foot_x",foot_x)
            # print(img_array[foot_x])
            foot_y = height - np.where(img_array[foot_x] == 0)[0][0]
            print("foot_x", foot_x)
            print("foot_y", foot_y)
            knee_x = get_knee_point(img_array, foot_x, back1_threshold=back1_threshold)

            shoulder_x = get_shoulder_point(img_array, shoulder_threshold_start=shoulder_threshold_start,
                                            shoulder_threshold_end=shoulder_threshold_end)
            print("shoulder_x", shoulder_x)
            end3 = time.time()
            all_time3 = (end3 - start3) * 1000
            print("第一次总共运行了", all_time3, "毫秒")

            foot_y_criterion = find_foot_y(foot_x, height, imgs_path,
                                           png_names[start_images + 50: start_images + 60], reverse=reverse,
                                           left_reverse=left_reverse)
            foot_y_list.append(foot_y_criterion)

        # print(foot_x, knee_x, shoulder_x)

        # start2 = time.time()
        foot_count += 1
        if (foot_count == 6):
            print("-----------------------foot_image_name", img_name)
            break
        if (len(np.where((~img_array)[foot_x] == 255)[0]) == 0):
            print("-----------------------image_name", img_name)
            continue

        foot_count = 0
        knee_angel, hip_angel, shoulder_angel, coordinate_keys = find_angel(~img_array, foot_x, knee_x,
                                                                            foot_y_criterion, foot_y_list,
                                                                            knee_expand_length=knee_expand_length,
                                                                            thigh_threshold=thigh_threshold,
                                                                            back1_threshold=back1_threshold,
                                                                            back2_threshold=back2_threshold)

        angel = [knee_angel, hip_angel, shoulder_angel]
        shuchutupian(img2, img_array, angel, coordinate_keys, count, result_path=dir_out_pic)
        count += 1
        # end2 = time.time()
        # all_time2 = (end2 - start) * 1000
        # print("闫浩总共运行了", all_time2, "毫秒")

        knee_angel_list.append(knee_angel)
        hip_angel_list.append(hip_angel)
        shoulder_angel_list.append(shoulder_angel)

        # shoulder_y = get_h(img_array1, shoulder_x)
        try:
            shoulder_y = np.where(img_array[shoulder_x] == 0)[0][0]
        except:
            print(img_name)
            break

        shoulder_y_list.append(shoulder_y)
        shoulder_y_reverse_list.append(height - shoulder_y)
        # except:
        #     continue

    print("knee_angel_list", knee_angel_list)
    print("hip_angel_list", hip_angel_list)
    print("shoulder_angel_list", shoulder_angel_list)
    # end2 = time.time()
    # all_time2 = (end2 - start) * 1000 - all_time3
    # print("闫浩总共运行了", all_time2, "毫秒")
    # print("shoulder_angel_list", shoulder_angel_list)
    print(shoulder_y_list)
    print(shoulder_y_reverse_list)
    # trough_list = get_peak(shoulder_y_list, height=140, distance=20, window_length=15, polyorder=2)
    # peak_list = get_peak(shoulder_y_reverse_list, height=280, distance=20, window_length=15, polyorder=2)

    #############################################################################################################
    shoulder_y_list_sort = sorted(shoulder_y_list[:5])
    # print("shoulder_y_list_sort",shoulder_y_list_sort)
    shoulder_y_reverse_list_sort = sorted(shoulder_y_reverse_list[:5])
    trough_list = get_peak(shoulder_y_list, height=shoulder_y_list_sort[2] - shoulder_height_threshold, distance=20,
                           window_length=15, polyorder=2)
    peak_list = get_peak(shoulder_y_reverse_list, height=shoulder_y_reverse_list_sort[2] - shoulder_height_threshold,
                         distance=20,
                         window_length=15, polyorder=2)  # 波峰

    ###################################################################################################################

    print("trough_list", trough_list)
    print("peak_list", peak_list)
    # trough_list [113 159 203 228 275 339]
    # peak_list [ 37  71 138 182 216 246 304 362]

    # 通过 Image.open 读取图片得到的结果
    # trough_list [113 159 203 228 275 339]
    # peak_list [ 37  71 138 182 216 246 304 362]

    # 通过 skimage.io 读取图片得到的结果
    # trough_list [113 159 203 228 275 339]
    # peak_list [ 37  71 138 182 216 246 304 362]

    action_list, action_right_dict = get_action_list(peak_list, trough_list)
    print("action_list", action_list)

    # print("shoulder_angel_list", shoulder_angel_list)
    action_list_new_by_gap, action_right_dict = judge_by_gap_angel(shoulder_angel_list, action_list,
                                                                   action_right_dict,
                                                                   gap_right_angel=standard_dict[standard][2])

    action_list_new, action_right_dict = judge_by_angel(knee_angel_list, hip_angel_list, action_list_new_by_gap,
                                                        action_right_dict,
                                                        knee_right_angel=standard_dict[standard][0],
                                                        hip_right_angel=standard_dict[standard][1],
                                                        right_threshold=0.8)
    print("action_right_dict", action_right_dict)
    # print(action_right_dict)
    num = len(action_list_new)
    # print(action_list_new)
    # [[71, 137], [138, 181], [182, 215], [216, 245], [246, 303], [304, 361]]
    print("兄弟，你做了", num, "个俯卧撑，棒棒哒~")

    # print("ok")
    end = time.time()
    all_time = (end - start) * 1000
    avg_time = all_time / nums
    print("俯卧撑的动作区间是：", action_list)
    print("每个俯卧撑动作区间的概率是：", action_right_dict)
    print("总共运行了", all_time, "毫秒")
    print("一共", nums, "张图片")
    print("平均每张图片运行了", avg_time, "毫秒")
    return num, action_list, action_right_dict


dir_pic = r"D:\taishan_images\2-1"
dir_out_pic = r"D:\taishan_images\output_images"
main(dir_pic, dir_out_pic, 200, True)
