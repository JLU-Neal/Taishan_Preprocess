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
        i = (xyzs[:, 1] - 800) // 10
        j = (xyzs[:, 0] + 1200) // 10
        before_loop = time.time()
        ij_length = i.shape[0]
        # C++ extension, 10x faster
        self.loop.exec(i.astype(np.int16), j.astype(np.int16), step, ij_length, height, width, img)
        # for index in range(i.shape[0]//step):
        #     index = index * step
        #     img[int(i[index]), int(j[index])] = img[int(i[index]), int(j[index])] + 1
        after_loop = time.time()
        print("loop time: "+str(after_loop - before_loop))
        threshold = 2
        img[img < threshold] = 0
        img[img >= threshold] = 127
        after = time.time()
        print("proj time: "+str(after - before))
        # cv2.imshow('image', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()


        return img
class Loop():
    def __init__(self):
        _file = 'loop.so' # FOR LINUX
        # _file = 'loop.dll' # FOR Windows
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