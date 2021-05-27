# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI3.22.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from final_gui import *
from trans_video_gui import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1134, 1000)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.choose_dir_button = QtWidgets.QPushButton(self.centralwidget)
        self.choose_dir_button.setGeometry(QtCore.QRect(120, 70, 161, 71))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.choose_dir_button.setFont(font)
        self.choose_dir_button.setObjectName("choose_dir_button")

        self.choose_out_dir_button = QtWidgets.QPushButton(self.centralwidget)
        self.choose_out_dir_button.setGeometry(QtCore.QRect(370, 70, 161, 71))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.choose_out_dir_button.setFont(font)
        self.choose_out_dir_button.setObjectName("choose_out_dir_button")


        self.choose_input_images = QtWidgets.QPushButton(self.centralwidget)
        self.choose_input_images.setGeometry(QtCore.QRect(620, 70, 161, 71))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.choose_input_images.setFont(font)
        self.choose_input_images.setObjectName("choose_input_images")

        self.choose_output_video_dir = QtWidgets.QPushButton(self.centralwidget)
        self.choose_output_video_dir.setGeometry(QtCore.QRect(870, 70, 161, 71))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.choose_output_video_dir.setFont(font)
        self.choose_output_video_dir.setObjectName("choose_output_video_dir")

        self.start_Button = QtWidgets.QPushButton(self.centralwidget)
        self.start_Button.setGeometry(QtCore.QRect(200, 290, 261, 91))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(23)
        font.setBold(True)
        font.setWeight(75)
        self.start_Button.setFont(font)
        self.start_Button.setStyleSheet("background-color: rgb(0, 255, 0);")
        self.start_Button.setAutoDefault(False)
        self.start_Button.setObjectName("start_Button")

        self.video_Button = QtWidgets.QPushButton(self.centralwidget)
        self.video_Button.setGeometry(QtCore.QRect(690, 290, 261, 91))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(23)
        font.setBold(True)
        font.setWeight(75)
        self.video_Button.setFont(font)
        self.video_Button.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.video_Button.setObjectName("video_Button")

        self.reverse_Button = QtWidgets.QPushButton(self.centralwidget)
        self.reverse_Button.setGeometry(QtCore.QRect(620, 180, 161, 61))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.reverse_Button.setFont(font)
        self.reverse_Button.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.reverse_Button.setObjectName("reverse_Button")

        self.start_image = QtWidgets.QLineEdit(self.centralwidget)
        self.start_image.setGeometry(QtCore.QRect(370, 180, 161, 61))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.start_image.setFont(font)
        self.start_image.setObjectName("start_image")

        # self.end_image = QtWidgets.QLineEdit(self.centralwidget)
        # self.end_image.setGeometry(QtCore.QRect(370, 180, 161, 61))
        # font = QtGui.QFont()
        # font.setPointSize(11)
        # self.end_image.setFont(font)
        # self.end_image.setObjectName("end_image")

        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(-5, 650, 1141, 331))
        self.textBrowser.setObjectName("textBrowser")
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(20)
        self.textBrowser.setFont(font)
        self.textBrowser.setObjectName("textBrowser")

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.choose_dir_button.setText(_translate("MainWindow", "选择深度图目录"))
        self.choose_out_dir_button.setText(_translate("MainWindow", "选择输出目录"))
        self.choose_input_images.setText(_translate("MainWindow", "输入图片目录"))
        self.choose_output_video_dir.setText(_translate("MainWindow", "输出视频目录"))
        self.start_Button.setText(_translate("MainWindow", "开始"))
        self.video_Button.setText(_translate("MainWindow", "输出视频"))
        self.start_image.setText(_translate("MainWindow", "40"))
        self.reverse_Button.setText(_translate("MainWindow", "人从左进入"))
        # self.end_image.setText(_translate("MainWindow", "输入结束图片，如 200"))




        self.choose_dir_button.clicked.connect(self.button_click)

        self.choose_out_dir_button.clicked.connect(self.button_click1)

        self.choose_input_images.clicked.connect(self.button_click2)

        self.choose_output_video_dir.clicked.connect(self.button_click3)

        self.reverse_Button.clicked.connect(self.button_click4)

        self.dir = None
        self.out_dir = None
        self.start_Button.clicked.connect(lambda:self.taishan(self.dir,self.out_dir))

        self.input_dir = None
        self.video_dir = None
        self.video_Button.clicked.connect(lambda: self.video_trans(self.input_dir,self.video_dir))

        self.start_image_num = 150
        self.end_image_num = 200
        self.count = 0
        self.reverse = False
        # self.start_image_num = self.start_image.text()
        # self.end_image_num = self.end_image.text()


    def button_click(self):
        self.dir = QtWidgets.QFileDialog.getExistingDirectory(None, "请选择输入深度图文件夹", r"./")
        # filename,_=QFileDialog.getOpenFileName(None,'open',r"C:/",' ')
        # return filename

    def button_click1(self):
        self.out_dir = QtWidgets.QFileDialog.getExistingDirectory(None, "请选择输出图片文件夹", r"./")

    def button_click2(self):
        self.input_dir = QtWidgets.QFileDialog.getExistingDirectory(None, "请选择要合成视频的图片文件夹", r"./")

    def button_click3(self):
        self.video_dir = QtWidgets.QFileDialog.getExistingDirectory(None, "请选择输入视频文件夹", r"./")

    def button_click4(self):
        _translate = QtCore.QCoreApplication.translate
        self.count+=1
        if self.count % 2 == 0:
            self.reverse_Button.setText(_translate("MainWindow", "人从左进入"))
            self.reverse = False
        elif self.count % 2 == 1:
            self.reverse_Button.setText(_translate("MainWindow", "人从右进入"))
            self.reverse = True

    def taishan(self,dir,out_dir):
        self.start_image_num = self.start_image.text()
        # self.end_image_num = self.end_image.text()
        if dir == None or out_dir == None or not self.start_image_num.isdigit():
            self.textBrowser.setText("请输入正确路径")
        else:
            print("go_to_main")
            try:
                nums,action_list,action_right_dict = main(dir,out_dir,int(self.start_image_num),self.reverse)
                self.output(nums,action_list,action_right_dict)
            except:
                print("start or end image error")

    def video_trans(self,in_dir,out_dir):
        if in_dir == None or out_dir == None:
            return self.textBrowser.setText("请输入正确路径")
        else:
            try:
                trans_video(in_dir,out_dir)
            except:
                self.textBrowser.append("选择输入图片错误")

    def output(self,nums,action_list,action_right_dict):
        self.textBrowser.setText("俯卧撑总数量:共做了"+ str(nums)+ "个俯卧撑")
        self.textBrowser.append("每个俯卧撑对应的图片区间:"+str(action_list))
        self.textBrowser.append("每个区间是俯卧撑的概率为:"+str(action_right_dict))
        self.textBrowser.append("\n具体动作信息，请在输出图片文件夹中查看")
        # self.textBrowser.append("平均每张图片运行了"+str(avg_time)+ "毫秒")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)  # 创建一个QApplication，也就是你要开发的软件app
    MainWindow = QtWidgets.QMainWindow()  # 创建一个QMainWindow，用来装载你需要的各种组件、控件
    ui = Ui_MainWindow()     # ui是Ui_MainWindow()类的实例化对象，Ui_MainWindow需要根据你的实例化对象的objectname，默认是MainWindow。
    ui.setupUi(MainWindow)  # 执行类中的setupUi方法，方法的参数是第二步中创建的QMainWindow
    MainWindow.show()  # 执行QMainWindow的show()方法，显示这个QMainWindow
    sys.exit(app.exec_())  # 使用exit()或者点击关闭按钮退出QApp
