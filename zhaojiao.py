def get_points(im_array, reverse=True):
    section = []
    # im_array = im_array.transpose()
    # print("im_array",im_array.shape)
    # 有了长度了。
    width, height = im_array.shape
    if reverse:
        # shoulder_threshold_start = l - int(l * 0.6)
        # shoulder_threshold_end = l
        foot_threshold_start = width - int(width * 0.95)
        foot_threshold_end = width - int(width * 0.85)
    else:
        # shoulder_threshold_start = 0
        # shoulder_threshold_end = int(l * 0.6)
        foot_threshold_start = int(width * 0.65)
        foot_threshold_end = int(width * 0.9)

    # x = np.arange(0, l - 2 * shoulder_threshold_start)
    y = [0] * (width - 2 * 0)
    x_max = 0
    # 只考虑前半部分
    x1_list = []
    # for i in range(shoulder_threshold_start, shoulder_threshold_end):
    #     for j in range(len(im_array[0])):
    #         if im_array[i][j] == 0:
    #             y[i] += 1
    #     if x_max < y[i]:
    #         x1_list = [i]
    #         x_max = y[i]
    #     elif x_max == y[i]:
    #         x1_list.append(i)
    #  不管 reverse ，每次都是取中间位置，就无所谓了
    # x1 = x1_list[len(x1_list) // 2]
    # print("找到肩的位置", x1)
    # y1 = y[x1]

    # 234 277 660 680
    # 后半部分找脚，这个范围已经够大了
    x_max1 = 0
    x2 = 0
    for i in range(foot_threshold_start, foot_threshold_end):
        for j in range(height):
            if im_array[i][j] == 255:
                y[i] += 1
        if x_max1 <= y[i]:
            x_max1 = y[i]
            x2 = i
    # y2 = y[x2]
    # print("找到脚的位置", x2)
    for j in range(height):
        if im_array[x2][j] == 255:
            y = height-j;
            break
    # section.append(x1)
    # section.append(y1)
    section.append(x2)
    section.append(y)

    return section