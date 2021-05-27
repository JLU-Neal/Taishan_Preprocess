from trans import *

def shuchutupian(img,im_array1,angel_keys,coordinate_keys,count,result_path):
    # coordinate_keys = list(coordinate_dict.keys())
    # angel_keys = list(angel_dict.keys())
    # end = start + len(angel_keys)
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 图中文字体设置为黑体
    # for num in range(start, end):
    #     new_number = str(num - start + 1).zfill(3)
    #     key_number = num - start
    # final_results_img_name = '{}{}'.format(str(new_number), ".png")
    count = str(count).zfill(4)
    final_results_img_name = '{}{}'.format(str(count), ".png")
    # final_results_img_path = os.path.join(source_path, P, final_results_path, final_results_img_name)
    final_results_img_path = os.path.join(result_path,final_results_img_name)
    # img_name = '{}{}'.format(str(num), suffix1)
    # img_path = os.path.join(source_path, P, origin, img_name)

    # img, im_array1 = get_array_opencv(img_path, reverse)
    # im_array1 = im_array1.transpose()
    height = len(im_array1)
    width = len(im_array1[0])
    plt.axis('off')
    # if height != 641 or width != 481:
    #     print(num, "这张图片的大小和别的不一样")
    #     continue
    # else:
    # 读取角度
    angels = angel_keys
    # 把点描出来，再划线。我有5个点的坐标 1，2点连一条线，3，4点连一条线，1,5点连一条线
    points = coordinate_keys
    # 要算出1个交点，屁股点 (2,3,4,5点的交线)
    x_hip, y_hip = findIntersection(points[1][0], points[1][1], points[2][0], points[2][1], points[3][0],
                                    points[3][1], points[4][0], points[4][1])
    # 所以只需要4个点形成的3条线就可以 + 我要的那一条线
    # 水平线暂时不画
    x1_x2 = [points[0][0], points[1][0]]
    y1_y2 = [width - points[0][1], width - points[1][1]]
    x2_x_hip = [points[1][0], x_hip]
    y2_y_hip = [width - points[1][1], width - y_hip]
    x_hip_x5 = [x_hip, points[4][0]]
    y_hip_y5 = [width - y_hip, width - points[4][1]]
    x1_x5 = [points[0][0], points[4][0]]
    y1_y5 = [width - points[0][1], width - points[4][1]]
    for point in points:
        circle_x = point[0]
        circle_y = point[1]
        # if circle_x >= 625:
        #     circle_x = 625
        draw_circle_parameter_equation(circle_x, width - circle_y, 15, c='red', w=1.5)
    plt.plot(x1_x2, y1_y2, color="orange")
    plt.plot(x2_x_hip, y2_y_hip, color="yellow")
    plt.plot(x_hip_x5, y_hip_y5, color="green")
    plt.plot(x1_x5, y1_y5, color="blue")
    # 颜色不同
    # text_angel = '腿踝角度:{}臀部角度:{}:{}'.format(angels[0],angels[1],angels[2])
    plt.text(100, 10, "腿踝角度", fontsize=20, color="blue", horizontalalignment='center', verticalalignment='top')
    plt.text(200, 17, angels[0], fontsize=20, color="r", horizontalalignment='center', verticalalignment='top')
    plt.text(300, 10, "臀部角度", fontsize=20, color="blue", horizontalalignment='center', verticalalignment='top')
    plt.text(400, 17, angels[1], fontsize=20, color="r", horizontalalignment='center', verticalalignment='top')
    plt.text(500, 10, "俯身角度", fontsize=20, color="blue", horizontalalignment='center', verticalalignment='top')
    plt.text(600, 17, angels[2], fontsize=20, color="r", horizontalalignment='center', verticalalignment='top')
    # plt.text(320, 440, key_number + 1, fontsize=30, color="r", horizontalalignment='center',
    #          verticalalignment='bottom')
    # for action in action_list:
    #     if action[0] == (key_number + 1):
    #         state = "开始"
    #         plt.text(420, 440, state, fontsize=30, color="r", horizontalalignment='center',
    #                  verticalalignment='bottom')
    #     elif action[1] == (key_number + 1):
    #         state = "结束"
    #         plt.text(420, 440, state, fontsize=30, color="r", horizontalalignment='center',
    #                  verticalalignment='bottom')
    #         # 颜色不同
    #         # text_right = '俯卧撑{}-{}'.format(action[0], action[1])
    #         plt.text(70, 45, "图片", fontsize=20, color="blue", horizontalalignment='center',
    #                  verticalalignment='top')
    #         plt.text(170, 52, str(action[0]) + "-" + str(action[1]), fontsize=20, color="r",
    #                  horizontalalignment='center',
    #                  verticalalignment='top')
    #         plt.text(370, 45, "是俯卧撑的概率是", fontsize=20, color="blue", horizontalalignment='center',
    #                  verticalalignment='top')
    #         plt.text(570, 52, str(action_right_dict[tuple(action)]), fontsize=20, color="r",
    #                  horizontalalignment='center',
    #                  verticalalignment='top')
    #         break
    plt.imshow(img)
    plt.savefig(final_results_img_path)
    plt.close()
# main(r"D:\taishan_images\2-5","")