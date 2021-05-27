import cv2
import os


def trans_video(image_dir,out_dir):
    fps = 16
    size = (640, 480)
    videowriter = cv2.VideoWriter(os.path.join(out_dir, "video.avi"), cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps, size)
    # file_names

    for parent, dir_names, file_names in os.walk(image_dir):
        for file_name in file_names:
            if (file_name.lower().endswith(('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff'))):
                img = cv2.imread(parent + "/" + file_name)
                # print(parent + "/" + file_name)
                # print(img.shape)
                # print(type(img))
                # print(type(img) == "numpy")
                # print("file_name",file_name)

                videowriter.write(img)
            # img = cv2.imread('%d'.jpg % i)
            else:
                print(file_name)
                break
# image_dir =r"D:\taishan_images\test_gui"
# out_dir = r"D:\taishan_images\test_gui"
# trans_video(image_dir,out_dir)
#

