import cv2
from Transform import Transform
from Project import Projection
from Normalization import Normalization
import time




class PreProcess():
    def __init__(self):
        self.transform = Transform()
        self.project = Projection()
        self.norm = Normalization()
        print("Construct Preprocessor")

    def exec(self, depth_bg):
        before = time.time()
        xyzs, threshold = self.transform.exec(depth_bg)
        img, threshold = self.project.exec(xyzs, threshold)
        img = self.norm.exec(img, threshold)

        after = time.time()
        # print("totaltime: "+str(after - before))
        cv2.imshow('image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print(img.shape)
        return img