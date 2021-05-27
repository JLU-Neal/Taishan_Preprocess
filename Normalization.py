import numpy as np
import cv2
import time

class Normalization():
    def __init__(self):
        self.j_set = None
        self.i_set = None
        self.min_j = None
        self.max_j = None
        self.min_i = None
        self.max_i = None
        self.times = None
        self.threshold = None

    def exec(self, img, threshold):
        before = time.time()
        if self.j_set is None:
            self.j_set = np.where(img > 0)[1]
            self.j_set = np.sort(self.j_set)
            self.min_j = self.j_set[int(0.05 * self.j_set.size)]
            self.max_j = self.j_set[int(0.95 * self.j_set.size)]
            self.length = int((self.max_j - self.min_j) * 1.25)
            self.times = 100 / self.length

            # self.i_set = np.where(img > 0)[0]
            # self.i_set = np.sort(self.i_set)
            # self.min_i = self.i_set[int(0.05 * self.i_set.size)]
            # self.max_i = self.i_set[int(0.99* self.i_set.size)]


        # img = cv2.resize(img, (0, 0), fx=self.times, fy=self.times, interpolation=cv2.INTER_NEAREST)
        # img = img[:int(self.length * 0.75 * self.times),
        #               int(self.min_j * self.times * 0.8):int((self.min_j + self.length) * self.times)]
        # img = img.astype(np.float)
        img = img[:int(self.length * 0.75),
              int(self.min_j * 0.8):int(self.min_j * 1.25 + self.length)]
        if self.threshold is None:
            self.threshold = threshold * (480 / img.shape[0])
        img = cv2.resize(img, (0, 0), fx=640/img.shape[1], fy=480 / img.shape[0], interpolation=cv2.INTER_NEAREST)


        # translate the image to the bottom
        offset = 0
        translation = np.float32([[1, 0, 0], [0, 1, img.shape[0] - self.threshold - offset]])
        rows, cols = img.shape
        img = cv2.warpAffine(img, translation, (cols, rows))



        after = time.time()
        # print("norm time: "+str(after - before))
        # cv2.imshow('image', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        return img
