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
        xyzs = self.transform.exec(depth_bg)
        img = self.project.exec(xyzs)
        img = self.norm.exec(img)
        after = time.time()
        print("totaltime: "+str(after - before))
        cv2.imshow('image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return img

# Demo
if __name__ == '__main__':
    # print_hi('PyCharm')
    depth_bg = cv2.imread('./depth (250).png', -1)
    pp = PreProcess()
    pp.exec(depth_bg)