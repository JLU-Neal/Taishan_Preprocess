
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import cv2
import numpy as np
import time
# scale = 4
# ox = 331.45630 / scale
# oy = 232.41992 / scale
# fx = 388.28809 / scale
# fy = 388.21179 / scale
# rows = 480 // scale
# cols = 640 // scale
class Transform():
    def __init__(self):
        self.scale = 4
        self.ox = 331.45630 / self.scale
        self.oy = 232.41992 / self.scale
        self.fx = 388.28809 / self.scale
        self.fy = 388.21179 / self.scale
        self.rows = 480 // self.scale
        self.cols = 640 // self.scale
    def exec(self, depth_bg):
        before = time.time()
        depth_bg = cv2.resize(depth_bg, (0, 0), fx=1./self.scale, fy=1./self.scale, interpolation=cv2.INTER_NEAREST)
        gridyy, gridxx = np.mgrid[:self.rows, :self.cols]

        xx_cam = (gridxx - self.ox) / self.fx * depth_bg
        yy_cam = (gridyy - self.oy) / self.fy * depth_bg

        depth_bg = depth_bg[..., np.newaxis]
        bg_xyz = np.concatenate((xx_cam[..., np.newaxis], yy_cam[..., np.newaxis], depth_bg), axis=2)
        bg_xyz_resh_all = np.reshape(bg_xyz, (-1, 3))
        bg_xyz_resh = bg_xyz_resh_all[bg_xyz_resh_all[:, 2] > 0]




        xyzs = bg_xyz_resh



        #rotate
        angle = 0.75 * (np.pi/4)
        rotation = np.array([[1, 0, 0],
                             [0, np.cos(angle), -np.sin(angle)],
                             [0, np.sin(angle), np.cos(angle)]])
        xyzs = np.matmul(xyzs, rotation)

        # crop
        mask = (xyzs[:, 0] > -1200) * (xyzs[:, 0] < 1200) * (xyzs[:, 1] < 1450) * (xyzs[:, 2] > -1500) * (xyzs[:, 2 ] < 1600)
        xyzs = xyzs[mask]

        after = time.time()
        print("tran time: "+str(after - before))
        # fig = plt.figure()
        # ax = mplot3d.Axes3D(fig)
        # ax.scatter3D(xyzs.T[0], xyzs.T[1], xyzs.T[2])  # 散点图
        # plt.show()
        return xyzs

