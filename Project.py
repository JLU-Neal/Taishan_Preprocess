import cv2
import numpy as np
import time
import ctypes

class Projection():
    def __init__(self):
        print()
        self.loop = Loop()


    def exec(self, xyzs):
        before = time.time()
        height = 480
        width = 640
        img = np.zeros((height, width), np.int8)


        step = 1
        scale = 3

        i = (xyzs[:, 1] - 500) // scale
        j = (xyzs[:, 0] + 1300) // scale

        i_mask = (i < 480) * (i>=0)
        j_mask = (j < 640) * (j>=0)

        i = i[i_mask]
        j = j[j_mask]
        before_loop = time.time()
        ij_length = i.shape[0]

        # C++ extension, 10x faster
        self.loop.exec(i.astype(np.int16), j.astype(np.int16), step, ij_length, height, width, img)

        # for index in range(i.shape[0]//step):
        #     index = index * step
        #     img[int(i[index]), int(j[index])] = img[int(i[index]), int(j[index])] + 1
        after_loop = time.time()
        # print("loop time: "+str(after_loop - before_loop))



        img = cv2.blur(img.astype(float), (9, 9))
        img *= 127
        threshold = 5
        img[img < threshold] = 0
        img[img >= threshold] = 127
        # img = img.astype(np.uint8)

        after = time.time()

        print("proj time: "+str(after - before))
        # cv2.imshow('image', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()


        return img
class Loop():
    def __init__(self):
        # FOR LINUX, command: g++ loop.cpp -fPIC -shared -o loop.so
        _file = 'loop.so'
        # FOR Windows, command: g++ --share loop.cpp -o loop.dll
        # _file = 'loop.dll'
        _path = './' + _file
        lib = ctypes.cdll.LoadLibrary(_path)
        self.c_loop = lib.func
        self.c_loop.restype = None
        self.c_loop.argtypes = [
            np.ctypeslib.ndpointer(dtype=np.int16, ndim=1), # i
            np.ctypeslib.ndpointer(dtype=np.int16, ndim=1), # j
            ctypes.c_int8, # step
            ctypes.c_int16, # ij_length
            ctypes.c_int16, # width
            ctypes.c_int16, # height
            np.ctypeslib.ndpointer(dtype=np.int8, ndim=2),  # img
        ]

    def exec(self, i, j, step, ij_length, height, width, img):
        self.c_loop(i, j, step, ij_length, height, width, img)