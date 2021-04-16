
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
        self.threshold = None
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
        angleX = 1 * (np.pi/4)
        rotationX = np.array([[1, 0, 0],
                             [0, np.cos(angleX), -np.sin(angleX)],
                             [0, np.sin(angleX), np.cos(angleX)]])

        angleY = 0
        rotationY = np.array([[np.cos(angleY), 0, np.sin(angleY)],
                              [0, 1, 0],
                              [-np.sin(angleY), 0, np.cos(angleY)]])
        angleZ = 0.1 * (np.pi/4)
        rotationZ = np.array([[np.cos(angleZ), -np.sin(angleZ), 0],
                              [np.sin(angleZ), np.cos(angleZ), 0],
                              [0, 0, 1]])

        xyzs = np.matmul(xyzs, rotationX)
        # xyzs = np.matmul(xyzs, rotationY)
        xyzs = np.matmul(xyzs, rotationZ)


        # find the ground
        if(self.threshold is None):
            point_count_height = np.zeros(1000)
            for index in range(xyzs.shape[0]):
                height = 1500 - xyzs[index, 1]
                point_count_height[int(height)] = point_count_height[int(height)] + 1

            x = 1500 - np.arange(point_count_height.shape[0])
            y = point_count_height
            plt.plot(x, y)
            plt.show()
            ground_mask = y > 100
            self.threshold = x[ground_mask].min() - 30

        # crop
        mask = (xyzs[:, 0] > -1200) * (xyzs[:, 0] < 1200) * (xyzs[:, 1] < self.threshold) * (xyzs[:, 2] > -1500) * (xyzs[:, 2 ] < 1200)
        xyzs = xyzs[mask]

        after = time.time()
        print("tran time: "+str(after - before))
        # fig = plt.figure()
        # ax = mplot3d.Axes3D(fig)
        # ax.scatter3D(xyzs.T[0], xyzs.T[1], xyzs.T[2])  # 散点图
        # plt.show()

        return xyzs

