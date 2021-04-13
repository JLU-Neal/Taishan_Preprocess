import cv2

import time
from PreProcess import PreProcess



# Demo
if __name__ == '__main__':
    # print_hi('PyCharm')

    depth_bg = cv2.imread('./depth (260).png', -1)
    before = time.time()
    pp = PreProcess()
    pp.exec(depth_bg)
    after = time.time()
    print("totaltime: "+str(after - before))