import threading
import numpy as np

import PyQt5
import sys
import os
import time
from PyQt5.QtWidgets import (QApplication, QGroupBox, QDialog, QLineEdit, QLabel, QSlider,
                             QPushButton, QGridLayout, QMessageBox, QStatusBar, QComboBox, QProgressBar, QFileDialog)
from PyQt5.QtCore import Qt, QBasicTimer
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtGui
import q
import math
from multiprocessing import Process
import color_setting
from image_canvas import Image2D
from user_manage import User_Manage

from pco_control import PCO_Control
from displacement_system import Displacement_Table_Control
from laser_control import LaserControl
from view3D import View3D
import cv2
from all import wave
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import copy
from PyQt5.Qt import *
from PyQt5.QtCore import QThread, pyqtSignal
import tkinter as tk
from tkinter import filedialog
import shutil

os.environ["CUDA_VISIBLE_DEVICES"] = "0"


class MyThread_change_laser(QThread):  # 建立一个任务线程类
    signal = pyqtSignal(str)  # 设置触发信号传递的参数数据类型,这里是字符串

    def __init__(self):
        super(MyThread_change_laser, self).__init__()
        self.wave_change_laser = wave()
        self.wave_change_laser.create()

    def run(self):  # 在启动线程后任务从这个函数里面开始执行
        print("doxiancheng ")
        self.wave_change_laser.sent_wave()


class MyThread_save_image(QThread):
    def __init__(self, data, i, j, name_x, name_y):
        super(MyThread_save_image, self).__init__()
        self.np_image = data
        self.xdistance_i = i
        self.ydistance_j = j
        self.name_x = name_x
        self.name_y = name_y

    def run(self):  # 在启动线程后任务从这个函数里面开始执行
        if q.start_save_buttom == 1:

            if q.start_save_weiyitai == 0:
                # print("start_save_buttom",q.start_save_buttom)
                # q.i = q.i + 1
                # print(q.i)ca
                # print('cunxhu')
                # print(time.asctime(time.localtime(time.time())))

                self.np_image.tofile(q.f)
            if q.start_save_buttom == 1:
                if q.start_save_weiyitai == 1:
                    q.f.close()
                    print("结束")
                    q.start_save_buttom = 0
                    q.start_save_weiyitai = 0
                    q.i = q.i + 1
                    # q.f = open("C:\\TEST\\" + str(q.filename) + "_" + str(q.i) + ".bin", 'ab')

                    # a = float(self.name_x) + (self.xdistance_i+1) * 320
                    # b = float(self.name_y) + (self.ydistance_j+1) * 320
                    #
                    # q.f = open(
                    #     "C:\\TEST\\" + str(q.filename) + "_" + "x_distance" + str(a) + "y_distance" + str(b) + ".bin",
                    #     'ab')


class MyThread_draw_image_1(QThread):
    def __init__(self, data):
        print("start")
        super(MyThread_draw_image, self).__init__()
        self.a = Image2D()
        self.a.imagedata = data

        # print(data)

    def run(self):  # 在启动线程后任务从这个函数里面开始执行
        print("rub")
        self.a.draw()


class MyThread_draw_image(QThread):  # 建立一个任务线程类
    _signal = pyqtSignal(np.ndarray, np.ndarray)  # 设置触发信号传递的参数数据类型,这里是字符串

    def __init__(self, b):
        super(MyThread_draw_image, self).__init__()
        # self.data=data
        self.b = b

    def run(self):  # 在启动线程后任务从这个函数里面开始执行
        # print("do111xiancheng ")
        # self.b.imagedata=self.data
        self.b.draw()
        self._signal.emit(self.b.hist, self.b.imagedata)  #####传参数
        # self.a.draw()


# class MyThread_draw_thread(QThread):
#     def __init__(self):
#         super(MyThread_draw_thread, self).__init__()
#
#
#
#     def run(self): # 在启动线程后任务从这个函数里面开始执行
#         while self.pco_control.start_flag:
#             self.pco_control.start_plot_thread()
#             self.np_image_save = copy.deepcopy(self.pco_control.np_image)
#             #print(self.np_image_save)
#
#             #self.widgets["image"][0].imagedata = copy.deepcopy(self.pco_control.np_image)
#             # t1= threading.Thread(target=self.save_image)
#             # t2 = threading.Thread(target=self.draw_iamge_thread)
#             # t1.start()
#             # t2.start()
#             # t1=self.pool.submit(self.save_image)
#             self.save_image_thread = MyThread_save_image(self.np_image_save)
#             self.draw_image_thread_pyqt = MyThread_draw_image(self.pco_control.np_image)
#
#             self.save_image_thread.start()
#             self.draw_image_thread_pyqt.start()
#             self.draw_image_thread_pyqt.wait(100)
#             # t2=self.pool.submit(self.draw_iamge_thread)
#             # t2.result()
class MyThread_chaxun_start_thread(QThread):
    def __init__(self, displacement):
        super(MyThread_chaxun_start_thread, self).__init__()
        self.displacement = displacement

    def run(self):  # 在启动线程后任务从这个函数里面开始执行
        self.displacement.chaxun_start_for_thread()


class MyThread_chaxun_end_thread(QThread):
    def __init__(self, displacement):
        super(MyThread_chaxun_end_thread, self).__init__()
        self.displacement = displacement
        # self.get_position=get_position
        self.i = 0

    def run(self):  # 在启动线程后任务从这个函数里面开始执行
        self.displacement.chaxun_end_for_thread()
        self.i = self.i + 1


# class MyThread_start_save_clicker_thread(QThread):
#     def __init__(self,displacement):
#         super(MyThread_start_save_clicker_thread, self).__init__()
#         self.displacement = displacement
#
#
#
#     def run(self): # 在启动线程后任务从这个函数里面开始执行
#         print("调用了保存采集")
#         print(self.pco_save_flag)
#
#         if self.pco_save_flag == False:
#             try:
#                 if self.pco_control.start_flag:
#                     # self.pco_control.run_save_thread()
#                     q.filename = self.widgets["schedule_bar"][1].text()
#                     # q.f = open("C:\\TEST\\" + str(q.filename) + ".bin", 'ab')
#                     self.widgets["schedule_bar"][0].setValue(self.step)
#                     for i in range(0, 30):
#                         self.xdistance_i = i
#
#                         for j in range(0, 8):
#                             self.xdistance_i = i
#                             a = float(self.widgets["displacement_control"][9].text()) + (self.xdistance_i) * 320
#                             b = float(self.widgets["displacement_control"][10].text()) + (self.ydistance_j) * 320
#                             q.f = open(
#                                 "Z:\\TEST\\" + str(q.filename) + "_" + "x_distance" + str(a) + "y_distance" + str(
#                                     b) + ".bin",
#                                 'ab')
#
#                             self.on_update_button_click_start()
#                             time.sleep(1)
#                             q.start_save_buttom = 1
#
#                             self.on_update_button_click_end()
#                             self.pco_save_flag = True
#                             self.widgets["start_button"][1].setText("采集中...")
#                             self.get_m_time()
#                             self.schedule_run()
#                             self.pco_save_flag = False
#                             print("q.save")
#                             print(q.start_save_buttom)
#                             # print(q.start_save_weiyitai)
#                             time.sleep(2)
#                             if q.start_save_buttom == 1:
#
#                                 while True:
#                                     time.sleep(0.5)
#                                     if q.start_save_buttom == 0:
#                                         break
#             #
#             except AttributeError:
#                 QMessageBox.warning(self, '警告',
#                                     '没有找到相机！请检查连接，并关闭其他相机使用的进程!')


class App(QDialog):

    # 初始化
    def __init__(self, user):
        super().__init__()
        self.title = '相机采集系统'
        self.user = user
        self.resize(1600, 800)
        self.setWindowTitle(self.title)
        self.widgets = {}
        self.point_dict = {}
        self.timer = QBasicTimer()
        self.crete_main_widget()
        self.Init = False
        self.pco_save_flag = False
        self.step = 0
        self.m_time = 0
        self.x_speed = 5
        self.y_speed = 5
        self.z_speed = 5
        self.unit_power = 1
        self.unit_distance = 0.1
        self.pool_wave = ThreadPoolExecutor(max_workers=4)
        self.pool_save = ThreadPoolExecutor(max_workers=4)
        self.a = 0
        self.xdistance_i = 0
        self.ydistance_j = 0
        self.set_final_schedule = 0
        print("qidongh weiyitai")
        # 初始启动位移台
        self.displacement_start()
        self.array_to_save_number = 0
        self.save_iamge_instantly_num = 0
        self.save_iamge_instantly_flag = 1
        self.end_save_image_instanly_flag = 0
        self.save_iamge_instantly_q_f_close = 1
        self.displacement_control_system
        self.end_save_image_once = 2

        self.judge_path()
        self.f_path = []
        self.break_get_position_thread = 1
        self.lock_thread = threading.Lock()
        # self.wave_change_laser=wave()
        # self.wave_change_laser.create()
        # t=self.pool_wave.submit(self.wave_change_laser.sent_wave)
        self.wave_change_laser = wave()
        self.wave_change_laser.create()
        t = self.pool_wave.submit(self.wave_change_laser.sent_wave)

        # self.change_laser_start.wave_change_laser.
        # self.wave_change_laser=wave()
        # self.wave_change_laser.create()
        # t=self.pool_wave.submit(self.wave_change_laser.sent_wave)

    # 添加控件主界面
    def crete_main_widget(self):

        self.setWindowFlags(Qt.WindowMaximizeButtonHint | Qt.WindowMinimizeButtonHint |
                            Qt.WindowCloseButtonHint)

        self.create_canvas()
        layout = QGridLayout(self)
        layout.addWidget(self.current_user_box, 0, 1, 2, 1)
        layout.addWidget(self.start_button_box, 2, 1, 1, 1)
        layout.addWidget(self.schedule_bar, 3, 1, 1, 1)
        layout.addWidget(self.laser_box, 4, 1, 4, 1)
        layout.addWidget(self.displacement_system_box, 8, 1, 4, 1)
        layout.addWidget(self.view3d_box, 13, 1, 1, 1)
        layout.addWidget(self.hist, 14, 1, 4, 4)

        layout.addWidget(self.image_slider_box, 0, 2, 20, 2)
        layout.addWidget(self.image_box, 0, 4, 20, 2)
        layout.setAlignment(QtCore.Qt.AlignLeft)

    # 创建界面
    def create_canvas(self):
        self.create_crrent_user()
        self.create_schedule_widget()
        self.create_start_button()
        self.create_image_axis_settings()
        self.create_slider()
        self.create_3d_slider()

        self.create_laser_setting()
        self.create_displacement_system()
        # self.create_camera_setting()
        self.create_image()
        self.paint()
        self.create_hist()

    ###创建显示画图的界面
    def paint(self):
        self.image_box = QGroupBox("采集相片显示")
        self.image_box.setMinimumSize(1000, 800)
        layout = QGridLayout(self)
        label = QLabel()
        label_1 = QLabel()
        self.image_box.setLayout(layout)

        layout.addWidget(label, 0, 0, 2, 2, QtCore.Qt.AlignBottom)
        layout.addWidget(label_1, 0, 3, 2, 2, QtCore.Qt.AlignBottom)
        self.label_for_paint = [label, label_1]

    # 创建用户图标，显示当前用户
    def create_crrent_user(self):
        self.current_user_box = QGroupBox("用户")
        # self.current_user_box.setMaximumSize(500, 500)

        image_Label = QLabel()
        image_Label.setMaximumSize(40, 40)
        pixmap = QPixmap("./res/user.png")
        image_Label.setPixmap(pixmap)  # 在label上显示图片
        image_Label.setScaledContents(True)
        image_Label.setStyleSheet("background-color:rgb(200,200,200);")

        text_Label = QLabel()
        text_Label.setText("当前用户: ")
        user_Label = QLabel()
        user_Label.setText(self.user)

        layout = QGridLayout()
        layout.addWidget(image_Label, 0, 0, 1, 1)
        layout.addWidget(text_Label, 1, 0, 1, 1)
        layout.addWidget(user_Label, 1, 1, 1, 1)
        layout.setAlignment(QtCore.Qt.AlignCenter)

        self.current_user_box.setLayout(layout)
        self.widgets["current_user"] = [image_Label, text_Label]

    # 创建进度条以及保存文件名的界面
    def create_schedule_widget(self):
        self.schedule_bar = QGroupBox("进度")

        progress_bar = QProgressBar()
        progress_bar.setOrientation(Qt.Horizontal)

        file_name = self.createText("文件名: ", [10, 70, 12])
        file_edit = QLineEdit()
        file_bottom = QPushButton()
        file_bottom.setText("选择文件夹")
        file_bottom.clicked.connect(self.insure_save_direction)

        layout = QGridLayout()
        layout.addWidget(progress_bar, 0, 0, 1, 4)
        layout.addWidget(file_name, 1, 0, 1, 1)
        layout.addWidget(file_edit, 1, 2, 1, 1)
        layout.addWidget(file_bottom, 1, 1, 1, 1)

        self.schedule_bar.setLayout(layout)
        self.widgets["schedule_bar"] = [progress_bar, file_edit, file_bottom]

    # 设置样本大小，没有调用，可删
    def create_image_axis_settings(self):
        self.image_setting_box = QGroupBox("样本大小")
        # self.image_setting_box.setStyleSheet("QGroupBox{border:1px;border-style:solid;margin-top: 2px;}")

        x_text = self.createText("X", [10, 10, 12])
        y_text = self.createText("Y", [10, 10, 12])
        z_text = self.createText("Z", [10, 10, 12])

        x_lineEdit = QLineEdit()
        y_lineEdit = QLineEdit()
        z_lineEdit = QLineEdit()

        layout = QGridLayout()
        layout.addWidget(x_text, 0, 0, 1, 1)
        layout.addWidget(x_lineEdit, 1, 0, 1, 1)
        layout.addWidget(y_text, 0, 1, 1, 1)
        layout.addWidget(y_lineEdit, 1, 1, 1, 1)
        layout.addWidget(z_text, 0, 2, 1, 1)
        layout.addWidget(z_lineEdit, 1, 2, 1, 1)

        self.image_setting_box.setLayout(layout)
        self.widgets["image_setting"] = [x_text, x_lineEdit, y_text, y_lineEdit, z_text, z_lineEdit, layout]

    #########停止位移台
    def stop_weiyitai(self):
        x_distance = float(self.widgets["displacement_control"][9].text()) / 0.05
        y_distance = float(self.widgets["displacement_control"][10].text()) / 0.05
        z_distance = float(self.widgets["displacement_control"][11].text()) / 0.05

        self.displacement_control_system.set_axial_speed(1, 10)
        self.displacement_control_system.set_axial_speed(2, 10)
        self.displacement_control_system.set_axial_speed(3, 10)

        self.displacement_control_system.chuansong_1(x_distance)
        self.displacement_control_system.chuansong_2(y_distance)
        self.displacement_control_system.chuansong_3(z_distance)
        self.displacement_control_system.chuansong_start_flag(1)

        q.start_save_buttom = 0
        q.start_save_weiyitai = 0
        q.save_thread_flag = 0
        # q.save
        # q.f.close()
        self.break_get_position_thread = 0
        self.displacement_get_position.join()
        time.sleep(1)

        self.break_get_position_thread = 0
        self.displacement_get_position.join()
        # t = threading.Thread(target=self.chaxun_start())
        # t.start()
        # t.join()
        q.start_save_buttom = 0
        q.start_save_weiyitai = 0
        # q.f.close()
        # q.save_thread_flag=0
        # self.save_collect_thread.join()
        q.save_thread_flag = 1
        self.pco_save_flag = False
        print("回到初始点")
        self.timer.stop()
        self.step = 0

        self.set_final_schedule = 1
        self.widgets["start_button"][1].setText("采集数据")
        try:
            self.stop_chaxun_end.join()
        except:
            pass
        q.start_save_buttom = 0
        q.start_save_weiyitai = 0
        # self.save_collect_thread.join()
        self.break_get_position_thread = 1
        q.f.close()
        self.displacement_get_position = threading.Thread(target=self.get_position_thread)
        print("zhunbei ")
        self.displacement_get_position.start()

    # 创建 灰度调节设置的界面
    def create_slider(self):
        self.image_slider_box = QGroupBox("相片设置")
        # self.image_slider_box.setMaximumSize(300,1200)

        name_text = self.createText("灰度值", [10, 50, 50])
        gray_slider = QSlider(Qt.Vertical)

        gray_slider.setMinimum(0)
        gray_slider.setMaximum(256)

        auto_button = QPushButton("自动")
        auto_button.setFocusPolicy(Qt.NoFocus)
        auto_button.released.connect(self.auto_button_pressed)
        auto_button.clicked.connect(self.auto_button_click)

        edit_min = QLineEdit('0', self)
        edit_max = QLineEdit('256', self)
        label_current = QLabel('0', self)

        edit_min.setMinimumSize(30, 10)
        edit_max.setMinimumSize(30, 10)

        edit_min.textEdited[str].connect(lambda: self.onChange())
        edit_max.textEdited[str].connect(lambda: self.onChange())

        layout = QGridLayout()
        layout.addWidget(name_text, 0, 0, 1, 2)
        layout.addWidget(edit_max, 1, 0, 1, 1)
        layout.addWidget(gray_slider, 2, 0, 1, 1)
        layout.addWidget(edit_min, 3, 0, 1, 1)
        layout.addWidget(label_current, 2, 1, 1, 1)
        layout.addWidget(auto_button, 4, 0, 1, 2)

        gray_slider.valueChanged.connect(lambda v: self.gray_slider_Change(label_current.setText(str(v))))
        self.image_slider_box.setLayout(layout)
        self.image_slider_box.setMinimumSize(70, 20)
        self.widgets["image_slider_setting"] = [name_text, gray_slider, edit_min, edit_max, label_current]

    # 显示三维的界面
    def create_3d_slider(self):
        self.view3d_box = QGroupBox("显示三维")

        show_3d_button = QPushButton("打开文件")
        show_3d_button.setFocusPolicy(Qt.NoFocus)

        show_3d_button.clicked.connect(self.show_3d_view)

        save_button = QPushButton("保存当前图片")
        save_button.clicked.connect(self.save_current_button_click)

        layout = QGridLayout()
        layout.addWidget(show_3d_button, 0, 0, 1, 1)
        layout.addWidget(save_button, 0, 1, 1, 1)

        self.view3d_box.setMaximumSize(200, 100)
        self.view3d_box.setLayout(layout)
        self.widgets["3d_slider"] = [show_3d_button]

    def create_hist(self):
        # self.hist = QGroupBox("直方图显示")
        #
        # self.hist.setMaximumSize(400, 400)
        # layout = QGridLayout()
        # canve =Image2D()
        # layout.addWidget(canve.slider_min, 0, 0, 1, 1)
        #
        # layout.addWidget(canve.slider_max, 1, 0, 1, 1)
        # self.hist.setLayout(layout)
        # # self.widgets["hist"] = [show_3d_button]
        self.hist = QGroupBox("停止运行")
        stop_bottom = QPushButton("停止运行")
        stop_bottom.setFocusPolicy(Qt.NoFocus)
        stop_bottom.clicked.connect(self.stop_weiyitai)

        self.hist.setMaximumSize(200, 100)
        layout_1 = QGridLayout()
        layout_1.addWidget(stop_bottom, 0, 0, 1, 1)

        # layout_1.addWidget(self.widgets["image"][0].slider_max, 1, 0, 1, 1)
        self.hist.setLayout(layout_1)

    # 信号函数，保存相机的当前界面成.tiff
    def save_current_button_click(self):
        print("保存")

        cv2.imwrite("C:\\xiangji\\" + str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))) + '.tiff',
                    self.pco_control.np_image)

    # 信号函数，打开保存三维的文件夹，启动还原三维
    def show_3d_view(self):
        print("点击三维按钮")

        # 获取文件夹
        directory = QFileDialog.getExistingDirectory(None, "选取文件夹", "C:/")
        file_list = directory.split("/")
        self.directory = ""
        for i in file_list:
            self.directory = self.directory + i + r"\\"

        self.file_size = 0

        # 获取文件数
        for _ in os.listdir(self.directory):
            self.file_size += 1

        self.file_size -= 1
        if self.file_size != 0:
            self.view3D_run()

    # 启动三维的函数
    def view3D_run(self):
        self.view3D = View3D()
        self.view3D.file_path = self.directory
        self.view3D.size_list[5] = self.file_size
        self.view3D.run()

    # 创建激光设置界面函数
    def create_laser_setting(self):
        self.laser_box = QGroupBox("激光设置")

        self.laser_control = LaserControl()
        self.laser_control.check_serial()

        button_close_all = self.create_Button("关闭全部", [60, 120])

        button_close_all.clicked.connect(self.close_all_laser)

        button_405 = self.create_Button("关闭", [60, 30])
        button_488 = self.create_Button("关闭", [60, 30])
        button_561 = self.create_Button("关闭", [60, 30])
        button_637 = self.create_Button("关闭", [60, 30])

        update_405 = self.create_Button("更新", [60, 30])
        update_488 = self.create_Button("更新", [60, 30])
        update_561 = self.create_Button("更新", [60, 30])
        update_637 = self.create_Button("更新", [60, 30])

        button_405.clicked.connect(self.on_button_405_click)
        button_488.clicked.connect(self.on_button_488_click)
        button_561.clicked.connect(self.on_button_561_click)
        button_637.clicked.connect(self.on_button_637_click)

        update_405.clicked.connect(self.on_update_405_click)
        update_488.clicked.connect(self.on_update_488_click)
        update_561.clicked.connect(self.on_update_561_click)
        update_637.clicked.connect(self.on_update_637_click)

        self.button_405_flag = False
        self.button_488_flag = False
        self.button_561_flag = False
        self.button_637_flag = False

        # Serial_label = self.createText("串口:",[10,50,14])
        # self.Serial_box = QComboBox()
        #
        # self.Serial_box.addItem("COM1")
        # self.Serial_box.addItem("COM2")
        # self.Serial_box.addItem("COM3")

        self.laser_control.portx = 'com3'
        self.on_combox_changed()
        # self.Serial_box.currentIndexChanged.connect(self.on_combox_changed)

        power_label = self.createText("功率 (%)", [10, 80, 14])
        filter_label = self.createText("滤波片", [10, 50, 14])

        label_405 = self.createText("405", [10, 30, 20])
        label_488 = self.createText("488", [10, 30, 20])
        label_561 = self.createText("561", [10, 30, 20])
        label_637 = self.createText("637", [10, 30, 20])

        label_405.setStyleSheet('background-color: rgb(170, 85, 255);')
        label_488.setStyleSheet('background-color: rgb(0, 170, 255);')
        label_561.setStyleSheet('background-color: rgb(0, 255, 0);')
        label_637.setStyleSheet('background-color: rgb(255, 0, 0);')

        edit_405_power = QLineEdit()
        edit_405_filter = QLineEdit()
        edit_488_power = QLineEdit()
        edit_488_filter = QLineEdit()
        edit_561_power = QLineEdit()
        edit_561_filter = QLineEdit()
        edit_637_power = QLineEdit()
        edit_637_filter = QLineEdit()

        button_405_add = self.create_Button("+", [30, 30])
        button_405_cut = self.create_Button("-", [30, 30])

        button_488_add = self.create_Button("+", [30, 30])
        button_488_cut = self.create_Button("-", [30, 30])

        button_561_add = self.create_Button("+", [30, 30])
        button_561_cut = self.create_Button("-", [30, 30])

        button_637_add = self.create_Button("+", [30, 30])
        button_637_cut = self.create_Button("-", [30, 30])

        button_405_add.clicked.connect(self.button_405_add_clicked)
        button_488_add.clicked.connect(self.button_488_add_clicked)
        button_561_add.clicked.connect(self.button_561_add_clicked)
        button_637_add.clicked.connect(self.button_637_add_clicked)

        button_405_cut.clicked.connect(self.button_405_cut_clicked)
        button_488_cut.clicked.connect(self.button_488_cut_clicked)
        button_561_cut.clicked.connect(self.button_561_cut_clicked)
        button_637_cut.clicked.connect(self.button_637_cut_clicked)

        edit_405_power.setText("10")
        edit_488_power.setText("10")
        edit_561_power.setText("10")
        edit_637_power.setText("10")

        edit_405_filter.setEnabled(False)
        edit_488_filter.setEnabled(False)
        edit_561_filter.setEnabled(False)
        edit_637_filter.setEnabled(False)

        edit_405_filter.setText("450/50m")
        edit_488_filter.setText("525/50m")
        edit_561_filter.setText("570lp")
        edit_637_filter.setText("655lp")

        layout = QGridLayout()
        # layout.addWidget(Serial_label, 0,0,1,1)
        # layout.addWidget(self.Serial_box, 0,1,1,1)
        layout.addWidget(power_label, 1, 5, 1, 1)
        layout.addWidget(filter_label, 1, 7, 1, 1)

        layout.addWidget(label_405, 2, 0, 1, 1)
        layout.addWidget(button_405, 2, 2, 1, 1)
        layout.addWidget(update_405, 2, 3, 1, 1)
        layout.addWidget(button_405_cut, 2, 4, 1, 1)
        layout.addWidget(edit_405_power, 2, 5, 1, 1)
        layout.addWidget(button_405_add, 2, 6, 1, 1)
        layout.addWidget(edit_405_filter, 2, 7, 1, 1)

        layout.addWidget(label_488, 3, 0, 1, 1)
        layout.addWidget(button_488, 3, 2, 1, 1)
        layout.addWidget(update_488, 3, 3, 1, 1)
        layout.addWidget(button_488_cut, 3, 4, 1, 1)
        layout.addWidget(edit_488_power, 3, 5, 1, 1)
        layout.addWidget(button_488_add, 3, 6, 1, 1)
        layout.addWidget(edit_488_filter, 3, 7, 1, 1)

        layout.addWidget(label_561, 4, 0, 1, 1)
        layout.addWidget(button_561, 4, 2, 1, 1)
        layout.addWidget(update_561, 4, 3, 1, 1)
        layout.addWidget(button_561_cut, 4, 4, 1, 1)
        layout.addWidget(edit_561_power, 4, 5, 1, 1)
        layout.addWidget(button_561_add, 4, 6, 1, 1)
        layout.addWidget(edit_561_filter, 4, 7, 1, 1)

        layout.addWidget(label_637, 5, 0, 1, 1)
        layout.addWidget(button_637, 5, 2, 1, 1)
        layout.addWidget(update_637, 5, 3, 1, 1)
        layout.addWidget(button_637_cut, 5, 4, 1, 1)
        layout.addWidget(edit_637_power, 5, 5, 1, 1)
        layout.addWidget(button_637_add, 5, 6, 1, 1)
        layout.addWidget(edit_637_filter, 5, 7, 1, 1)

        layout.addWidget(button_close_all, 2, 1, 4, 1)
        # layout.setAlignment(QtCore.Qt.AlignLeft)

        self.laser_box.setLayout(layout)
        self.widgets["laser_data"] = [button_405, button_488, button_561, button_637,
                                      edit_405_power, edit_488_power, edit_561_power, edit_637_power,
                                      edit_405_filter, edit_488_filter, edit_561_filter, edit_637_filter]

    # 创建位移台设置界面函数
    def create_displacement_system(self):
        # create text
        self.displacement_system_box = QGroupBox("位移台控制")
        # self.displacement_system_box.setMaximumSize(500, 500)

        self.displacement_control_system = Displacement_Table_Control()

        x_text = self.createText("X", [10, 20, 20])
        y_text = self.createText("Y", [10, 20, 20])
        z_text = self.createText("Z", [10, 20, 20])
        speed_text = self.createText("速度", [10, 40, 60])

        location_text = self.createText("当前位置", [10, 150, 20])
        distance_text = self.createText("目标位置", [10, 190, 20])
        start_text = self.createText("起点位置", [10, 150, 20])
        end_text = self.createText("终点位置", [10, 150, 20])

        location_tip = self.createText("μm", [10, 150, 20])
        distance_tip = self.createText("±12500μm", [10, 190, 20])
        start_tip = self.createText("μm", [10, 150, 20])
        end_tip = self.createText("μm", [10, 150, 20])

        # create_edit
        x_speed_combox = self.create_displacement_comboBox()
        y_speed_combox = self.create_displacement_comboBox()
        z_speed_combox = self.create_displacement_comboBox()

        x_speed_combox.activated[int].connect(self.set_x_speed)
        y_speed_combox.activated[int].connect(self.set_y_speed)
        z_speed_combox.activated[int].connect(self.set_z_speed)

        x_location_edit = QLineEdit()
        y_location_edit = QLineEdit()
        z_location_edit = QLineEdit()

        x_distance_edit = QLineEdit()
        y_distance_edit = QLineEdit()
        z_distance_edit = QLineEdit()

        x_distance_edit.setMinimumSize(70, 10)
        y_distance_edit.setMinimumSize(70, 10)
        z_distance_edit.setMinimumSize(70, 10)

        x_distance_edit.setText("0")
        y_distance_edit.setText("0")
        z_distance_edit.setText("0")

        x_start_edit = QLineEdit()
        y_start_edit = QLineEdit()
        z_start_edit = QLineEdit()

        x_end_edit = QLineEdit()
        y_end_edit = QLineEdit()
        z_end_edit = QLineEdit()

        x_location_edit.setEnabled(False)
        y_location_edit.setEnabled(False)
        z_location_edit.setEnabled(False)

        button_x_add = self.create_Button("+", [30, 30])
        button_x_cut = self.create_Button("-", [30, 30])

        button_y_add = self.create_Button("+", [30, 30])
        button_y_cut = self.create_Button("-", [30, 30])

        button_z_add = self.create_Button("+", [30, 30])
        button_z_cut = self.create_Button("-", [30, 30])

        button_x_add.clicked.connect(self.button_x_add_clicked)
        button_x_cut.clicked.connect(self.button_x_cut_clicked)

        button_y_add.clicked.connect(self.button_y_add_clicked)
        button_y_cut.clicked.connect(self.button_y_cut_clicked)

        button_z_add.clicked.connect(self.button_z_add_clicked)
        button_z_cut.clicked.connect(self.button_z_cut_clicked)

        update_button = QPushButton("更新位置")
        # stop_button = QPushButton("停止运行")
        start_point_button = QPushButton("设置起点")
        end_point_button = QPushButton("设置终点")

        update_button.setFocusPolicy(Qt.NoFocus)
        # stop_button.setFocusPolicy(Qt.NoFocus)
        start_point_button.setFocusPolicy(Qt.NoFocus)
        end_point_button.setFocusPolicy(Qt.NoFocus)

        # start_button.clicked.connect(self.displacement_start)
        update_button.clicked.connect(self.on_update_button_click)
        # stop_button.clicked.connect(self.stop_weiyitai)
        start_point_button.clicked.connect(self.on_start_point_button_click)
        end_point_button.clicked.connect(self.on_end_point_button_click)

        layout = QGridLayout(self)
        layout.addWidget(speed_text, 0, 1, 1, 1)
        layout.addWidget(location_text, 0, 2, 1, 1)
        layout.addWidget(distance_text, 0, 4, 1, 1)
        layout.addWidget(start_text, 0, 6, 1, 1)
        layout.addWidget(end_text, 0, 7, 1, 1)

        layout.addWidget(location_tip, 1, 2, 1, 1)
        layout.addWidget(distance_tip, 1, 4, 1, 1)
        layout.addWidget(start_tip, 1, 6, 1, 1)
        layout.addWidget(end_tip, 1, 7, 1, 1)

        layout.addWidget(x_text, 2, 0, 1, 1)
        layout.addWidget(y_text, 3, 0, 1, 1)
        layout.addWidget(z_text, 4, 0, 1, 1)

        layout.addWidget(x_speed_combox, 2, 1, 1, 1)
        layout.addWidget(y_speed_combox, 3, 1, 1, 1)
        layout.addWidget(z_speed_combox, 4, 1, 1, 1)

        layout.addWidget(x_location_edit, 2, 2, 1, 1)
        layout.addWidget(y_location_edit, 3, 2, 1, 1)
        layout.addWidget(z_location_edit, 4, 2, 1, 1)

        layout.addWidget(button_x_cut, 2, 3, 1, 1)
        layout.addWidget(button_y_cut, 3, 3, 1, 1)
        layout.addWidget(button_z_cut, 4, 3, 1, 1)

        layout.addWidget(x_distance_edit, 2, 4, 1, 1)
        layout.addWidget(y_distance_edit, 3, 4, 1, 1)
        layout.addWidget(z_distance_edit, 4, 4, 1, 1)

        layout.addWidget(button_x_add, 2, 5, 1, 1)
        layout.addWidget(button_y_add, 3, 5, 1, 1)
        layout.addWidget(button_z_add, 4, 5, 1, 1)

        layout.addWidget(x_start_edit, 2, 6, 1, 1)
        layout.addWidget(y_start_edit, 3, 6, 1, 1)
        layout.addWidget(z_start_edit, 4, 6, 1, 1)

        layout.addWidget(x_end_edit, 2, 7, 1, 1)
        layout.addWidget(y_end_edit, 3, 7, 1, 1)
        layout.addWidget(z_end_edit, 4, 7, 1, 1)

        # layout.addWidget(start_button, 5,1,1,1)
        layout.addWidget(update_button, 5, 2, 1, 1)
        # layout.addWidget(stop_button, 5, 4, 1, 1)
        layout.addWidget(start_point_button, 5, 6, 1, 1)
        layout.addWidget(end_point_button, 5, 7, 1, 1)

        self.displacement_system_box.setLayout(layout)

        self.widgets["displacement_control"] = [x_speed_combox, y_speed_combox, z_speed_combox,
                                                x_location_edit, y_location_edit, z_location_edit,
                                                x_distance_edit, y_distance_edit, z_distance_edit,
                                                x_start_edit, y_start_edit, z_start_edit,
                                                x_end_edit, y_end_edit, z_end_edit, update_button]

    # 位移台x 轴 当前位置增加按钮
    def button_x_add_clicked(self):
        current = int(self.widgets["displacement_control"][6].text())
        if current < 12500:
            self.widgets["displacement_control"][6].setText(str(current + 1))

    # 位移台x 轴 当前位置减少按钮
    def button_x_cut_clicked(self):
        current = int(self.widgets["displacement_control"][6].text())
        if current > -12500:
            self.widgets["displacement_control"][6].setText(str(current - 1))

    def button_y_add_clicked(self):
        current = int(self.widgets["displacement_control"][7].text())
        if current < 12500:
            self.widgets["displacement_control"][7].setText(str(current + 1))

    def button_y_cut_clicked(self):
        current = int(self.widgets["displacement_control"][7].text())
        if current > -12500:
            self.widgets["displacement_control"][7].setText(str(current - 1))

    def button_z_add_clicked(self):
        current = int(self.widgets["displacement_control"][8].text())
        if current < 12500:
            self.widgets["displacement_control"][8].setText(str(current + 1))

    def button_z_cut_clicked(self):
        current = int(self.widgets["displacement_control"][8].text())
        if current > -12500:
            self.widgets["displacement_control"][8].setText(str(current - 1))

    # 创建相机参数设置，无增加，可删
    def create_camera_setting(self):
        self.camera_setting_box = QGroupBox("相机参数设置")

        exposure_time_text = self.createText("曝光时间 (S)", [10, 120, 12])
        pate_text = self.createText("高/低 速率 (Hz)", [10, 120, 12])
        # dwlinetime_text = self.createText("每行曝光时间 (μS)", [10, 120, 12])
        # exposure_line_text = self.createText("曝光行数 (行)", [10, 120, 12])
        # delay_line_text = self.createText("延迟行数 (行)", [10, 140, 12])

        exposure_time_lineEdit = QLineEdit()
        pate_ComboBox = QComboBox()

        # value
        exposure_time_lineEdit.setEnabled(False)

        pate_ComboBox.addItem("272250000")
        pate_ComboBox.addItem("95333333")

        layout = QGridLayout()
        layout.addWidget(exposure_time_text, 0, 0, 1, 2)
        layout.addWidget(pate_text, 1, 0, 1, 1)

        layout.addWidget(exposure_time_lineEdit, 0, 1, 1, 1)
        layout.addWidget(pate_ComboBox, 1, 1, 1, 1)
        layout.addWidget(self.start_button_box, 2, 0, 1, 2)

        self.camera_setting_box.setLayout(layout)
        self.widgets["camera_setting"] = [exposure_time_lineEdit, pate_ComboBox]

    # 创建打开相机 与 采集数据 按钮的界面
    def create_start_button(self):
        self.start_button_box = QGroupBox("")
        # self.start_button_box.setMaximumSize(500, 500)

        start_button = QPushButton("打开相机")
        save_button = QPushButton("采集数据")

        start_button.setFocusPolicy(Qt.NoFocus)
        save_button.setFocusPolicy(Qt.NoFocus)

        start_button.clicked.connect(self.start_collect_clicked)
        save_button.clicked.connect(self.save_collect_clicked_thread)

        # exposure_time
        layout = QGridLayout()
        layout.addWidget(start_button, 0, 0, 1, 1)
        layout.addWidget(save_button, 0, 1, 1, 1)

        self.start_button_box.setLayout(layout)
        self.widgets["start_button"] = [start_button, save_button, layout]

    ####弹窗显示
    def show_message(self, information_1):
        QMessageBox.information(None, '标题', information_1,
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

    # 信号函数，调用保存相机数据 的函数
    def save_collect_clicked_thread(self):

        gb = 1024 ** 3  # GB == gigabyte
        total_b, used_b, free_b = shutil.disk_usage('c:\\TEST')  # 查看磁盘的使用情况

        total_b, used_b, free_b = shutil.disk_usage(self.f_path)
        information_path = '存储路径：' + str(self.f_path)
        information_a = '总的磁盘空间: {:6.2f} GB '.format(total_b / gb)
        information_b = '已经使用的 : {:6.2f} GB '.format(used_b / gb)
        information_c = '未使用的 : {:6.2f} GB '.format(free_b / gb)
        # free_size = info.f_bsize * info.f_bavail / 1024 / 1024
        # ifformation=str
        information = information_path + information_a + information_b + information_c
        show_message_return = self.show_message(information)
        print(show_message_return)
        # if show_message_return==QMessageBox.Yes:
        self.array_to_save = np.ones((abs(math.ceil(abs(int(self.widgets["displacement_control"][13].text()) - int(
            self.widgets["displacement_control"][10].text())) ) + 50), 180, 2048), dtype=np.uint16)
        print("my")
        print(abs(math.ceil(abs(int(self.widgets["displacement_control"][13].text()) - int(
            self.widgets["displacement_control"][10].text())) ) + 50))

        self.break_get_position_thread = 0
        self.displacement_get_position.join()
        # self.t2_save_image_instantly.start()
        self.t2_save_image_instantly = threading.Thread(target=self.save_iamge_instantly)
        self.t2_save_image_instantly.start()
        self.save_collect_thread = threading.Thread(target=self.save_collect_clicked)
        self.save_collect_thread.start()

        self.save_iamge_instantly_flag = 1
        self.get_m_time()
        # self.schedule_run()

    def save_collect_clicked(self):
        print("调用了保存采集")
        print(self.pco_save_flag)

        if self.pco_save_flag == False:
            try:
                if self.pco_control.start_flag:

                    # self.pco_control.run_save_thread()
                    q.filename = self.widgets["schedule_bar"][1].text()
                    # q.f = open("C:\\TEST\\" + str(q.filename) + ".bin", 'ab')
                    # self.widgets["schedule_bar"][0].setValue(self.step)
                    print("start_save")
                    try:
                        num_for_x = int(math.ceil((float(self.widgets["displacement_control"][12].text()) - float(
                            self.widgets["displacement_control"][9].text())) / 320))
                        num_for_z = int(math.ceil((float(self.widgets["displacement_control"][14].text()) - float(
                            self.widgets["displacement_control"][11].text())) / 27))
                    except:
                        num_for_x = 0
                        num_for_z = 0

                    # if num_for_x==0:
                    #     num_for_x=1
                    # if num_for_y==0:
                    #     num_for_y=1
                    ########要不要去做判定，是不是循环
                    for i in range(0, num_for_z + 1):
                        self.zdistance_i = i

                        for j in range(0, num_for_x + 1):
                            self.xdistance_j = j
                            self.save_iamge_instantly_num = 0
                            self.array_to_save_number = 0
                            try:

                                str_x_distance = float(self.widgets["displacement_control"][9].text()) + (
                                    self.xdistance_j) * 320
                                str_z_distance = float(self.widgets["displacement_control"][11].text()) + (
                                    self.zdistance_i) * 27
                            except:
                                str_x_distance = ' '
                                str_z_distance = ' '
                            self.wave_change_laser.control_488_displacement_off_on = 0
                            self.wave_change_laser.control_637_displacement_off_on = 0
                            self.wave_change_laser.create()
                            q.wave_flag = 0
                            while True:
                                time.sleep(0.1)
                                if q.wave_flag == 1:
                                    break
                            t = self.pool_wave.submit(self.wave_change_laser.sent_wave)

                            # q.f = open(
                            #     "Z:\\TEST\\" + str(q.filename) + "_" + "x_distance" + str(a) + "y_distance" + str(
                            #         b) + ".bin",
                            #     'ab')
                            try:
                                q.f.close()
                                q.filename = self.widgets["schedule_bar"][1].text()
                                q.f = open(self.f_path + '/' + str(q.filename) + "_" + "x_distance" + str(
                                    str_x_distance) + "z_distance" + str(
                                    str_z_distance) + ".bin", 'ab')
                                print("self.f_path")
                                print(self.f_path)
                            except:
                                q.filename = self.widgets["schedule_bar"][1].text()
                                q.f = open(
                                    "C:\\TEST\\" + str(q.filename) + "_" + "x_distance" + str(
                                        str_x_distance) + "y_distance" + str(
                                        str_z_distance) + ".bin",
                                    'ab')

                            self.on_update_button_click_start()
                            self.get_position_for_once()

                            self.wave_change_laser.control_488_displacement_off_on = 1
                            self.wave_change_laser.control_637_displacement_off_on = 1
                            self.wave_change_laser.create()
                            q.wave_flag = 0
                            while True:
                                time.sleep(0.1)
                                if q.wave_flag == 1:
                                    break
                            t = self.pool_wave.submit(self.wave_change_laser.sent_wave)

                            # self.lock_thread.acquire()
                            q.start_save_buttom = 1
                            # self.lock_thread.release()
                            self.on_update_button_click_end()
                            self.pco_save_flag = True

                            self.pco_save_flag = False
                            print("q.save")
                            print(q.start_save_buttom)
                            # print(q.start_save_weiyitai)
                            # time.sleep(2)
                            if q.start_save_buttom == 1:

                                while True:
                                    time.sleep(0.5)
                                    if q.start_save_buttom == 0 and self.end_save_image_once==1:
                                        self.end_save_image_once =0
                                        print("一个循环结束")
                                        break
                                    if q.save_thread_flag == 0:
                                        print("跳出第一层循环")
                                        q.start_save_buttom = 0
                                        break
                            if q.save_thread_flag == 0:
                                print("跳出第二层循环")
                                break
                        if q.save_thread_flag == 0:
                            q.save_thread_flag = 1
                            print("跳出最终循环")
                            break

                            ###########查询q.save bottom.如果是1的话就 开始做循环，如果是0的话就结束循环，同时
                self.end_save_image_instanly_flag = 1
                self.t2_save_image_instantly.join()
                self.end_save_image_instanly_flag = 0

                self.set_final_schedule = 1
                self.displacement_get_position = threading.Thread(target=self.get_position_thread)
                print("zhunbei ")
                self.displacement_get_position.start()


            #
            except AttributeError:
                QMessageBox.warning(self, '警告',
                                    '没有找到相机！请检查连接，并关闭其他相机使用的进程!')

    # 计算 运行时间函数，为计算进度条的时间

    def get_m_time(self):
        try:
            x_distance_start = float(self.widgets["displacement_control"][3].text())
            y_distance_start = float(self.widgets["displacement_control"][4].text())
            z_distance_start = float(self.widgets["displacement_control"][5].text())

            z_distance_start_start = float(self.widgets["displacement_control"][11].text())

            x_distance_end = float(self.widgets["displacement_control"][9].text())
            y_distance_end = float(self.widgets["displacement_control"][10].text())
            z_distance_end = float(self.widgets["displacement_control"][11].text())

            x_distance_end_end = float(self.widgets["displacement_control"][12].text())
            y_distance_end_end = float(self.widgets["displacement_control"][13].text())
            z_distance_end_end = float(self.widgets["displacement_control"][14].text())

            try:
                num_for_x = int(math.ceil((float(self.widgets["displacement_control"][12].text()) - float(
                    self.widgets["displacement_control"][9].text())) / 320))
                num_for_y = int(math.ceil((float(self.widgets["displacement_control"][13].text()) - float(
                    self.widgets["displacement_control"][10].text())) / 320))
            except:
                num_for_x = 0
                num_for_y = 0
            # if num_for_x==0:
            #     num_for_x=1
            # if num_for_y==0:
            #     num_for_y=1

            t1 = math.ceil((z_distance_end_end - z_distance_start_start) / 12)
            tx = math.ceil((x_distance_end - x_distance_start) / 250)
            ty = math.ceil((y_distance_end - y_distance_start) / 250)
            tz = math.ceil((z_distance_end - z_distance_start) / 250)

            tx_for_loop = math.ceil((x_distance_end_end - x_distance_end) / 500)
            ty_for_loop = math.ceil((y_distance_end_end - y_distance_end) / 500)

            t1 = (t1 + 1 + 0.3 + tx_for_loop + ty_for_loop + 0.3) * (num_for_x + 1) * (num_for_y + 1) + tx + ty + tz

            # t3 = math.ceil((y_distance_end - y_distance_start) / 500)

            self.m_time = t1 * 10

        except ValueError:
            pass

    # 信号函数，打开相机的函数
    def start_collect_clicked(self):

        try:
            if self.Init == False:
                self.pco_control = PCO_Control()


        except ValueError:
            QMessageBox.warning(self, '警告', '没有找到相机！请检查连接，并关闭其他相机使用的进程!')
            return

        if self.pco_control.start_flag == False:
            print("调用了开始收集")
            self.pco_control.start_flag = True
            self.Init = True
            try:
                self.pco_control.start_pco()
                self.draw_thread = threading.Thread(target=self.draw_image)
                self.draw_thread.start()
                # self.draw_thread_thread = MyThread_draw_thread()
                # self.draw_thread_thread.start()
                self.widgets["start_button"][0].setText("关闭相机")
            except:

                self.Init = False
                self.close_collect_clicked()
                self.widgets["start_button"][0].setText("打开相机")
                QMessageBox.warning(self, '警告', '没有找到相机！请检查连接，并关闭其他相机使用的进程!')


        else:
            print("调用了关闭收集")

            self.Init = False
            self.close_collect_clicked()
            self.widgets["start_button"][0].setText("打开相机")

    # 启动时间，启动进度条时间
    def schedule_run(self):
        self.timer.start(int(self.m_time), self)

    # 时间事件，计算进度条
    def timerEvent(self, e):
        self.widgets["start_button"][1].setText("采集中...")
        if self.step >= 100:
            self.timer.stop()
            self.step = 0
            self.widgets["start_button"][1].setText("采集数据")
            return

        self.step = self.step + 1

        if self.step == 100 and self.set_final_schedule == 0:
            self.step = 99

        if self.step == 100 and self.set_final_schedule == 1:
            self.set_final_schedule = 0
        self.widgets["schedule_bar"][0].setValue(self.step)

    # 画图函数，将相机的数据，画到主界面右边，
    def save_image(self):
        if q.start_save_buttom == 1:

            if q.start_save_weiyitai == 0:
                # print("start_save_buttom",q.start_save_buttom)
                # q.i = q.i + 1
                # print(q.i)
                print('cunxhu')
                # print(time.asctime(time.localtime(time.time())))
                try:
                    self.array_to_save[self.array_to_save_number, :, :] = self.np_image
                # print(self.np_image)
                # print(self.array_to_save[self.array_to_save_number,:,:])
                #
                # print(self.array_to_save.shape)
                    self.array_to_save_number = self.array_to_save_number + 1
                except:
                    pass

                # self.np_image.tofile(q.f)

        if q.start_save_buttom == 1:
            if q.start_save_weiyitai == 1:
                # q.f.close()
                print("结束")
                print("self.array_to_save_number")
                print(self.array_to_save_number)
                # self.lock_thread.acquire()
                q.start_save_buttom = 0
                q.start_save_weiyitai = 0
                # self.lock_thread.release()
                q.i = q.i + 1
                # q.f = open("C:\\TEST\\" + str(q.filename) + "_" + str(q.i) + ".bin", 'ab')

    ############存储数据
    def save_iamge_instantly(self):
        while True:
            if self.save_iamge_instantly_num < self.array_to_save_number:
                #print("self.save_iamge_instantly_num")
                #print(self.save_iamge_instantly_num)
                #print("self.array_to_save_number")
                #print(self.array_to_save_number)
                try:
                    self.array_to_save[self.save_iamge_instantly_num, :, :].tofile(q.f)

                except:
                    print("get edequente image")
                self.save_iamge_instantly_num = self.save_iamge_instantly_num + 1
            if self.save_iamge_instantly_num == abs(math.ceil(
                    abs(int(self.widgets["displacement_control"][13].text()) - int(
                            self.widgets["displacement_control"][10].text())) /1)):
                self.save_iamge_instantly_num = 0
                self.array_to_save_number = 0
                q.f.close()
                self.save_iamge_instantly_q_f_close = 0
                print("save_iamge_instanly close")
                self.save_iamge_instantly_flag = 1
                self.end_save_image_once=1
            if self.end_save_image_instanly_flag == 1 and self.save_iamge_instantly_q_f_close == 0:
                print("end_save_image")
                self.save_iamge_instantly_q_f_close = 1
                break
            if q.start_save_buttom == 1:

                if q.start_save_weiyitai == 0:
                    #print("sleep")
                    time.sleep(0.01)

        print("end_save_instanly")

        # break
        ########多线程画图
        ########多线程画图
        #####问题出在哪里呢？
    def draw_iamge_thread(self):
        # if q.start_save_buttom == 0:
        #
        #     if q.start_save_weiyitai == 0:

        self.widgets["image"][0].draw()

    # 画图函数，将相机的数据，画到主界面右边，
    # def save_image_thread(self):
    #     self.pco_control.plot_picture()

    def draw_image(self):
        draw_frq = 0
        while self.pco_control.start_flag:
            self.pco_control.plot_picture()
            self.np_image = copy.deepcopy(self.pco_control.np_image)
            self.widgets["image"][0].imagedata = self.pco_control.np_image
            t1 = threading.Thread(target=self.save_image)
            # t2 = threading.Thread(target=self.draw_iamge_thread)
            t1.start()
            # t2.start()
            ###############利用pyqt5自带的线程操作进行操作
            # self.save_image_thread=MyThread_save_image(self.np_image,self.xdistance_i,self.ydistance_j,self.widgets["displacement_control"][9].text(),self.widgets["displacement_control"][10].text())
            #
            #
            # self.save_image_thread.start()
            ##########利用python自带的线程池进行操作

            # t2=self.pool_save.submit(self.save_image)

            # print(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])

            self.draw_image_thread = MyThread_draw_image(self.widgets["image"][0])
            # self.MyThread_draw_image = None

            self.draw_image_thread._signal.connect(self.update_painter)
            t1.join()
            if q.start_save_buttom == 0:

                if q.start_save_weiyitai == 0:

                    if draw_frq == 0:
                        self.draw_image_thread.start()
                        self.draw_image_thread.wait()

            # pass
            draw_frq = draw_frq + 1
            if draw_frq == 20:
                draw_frq = 0

            # self.save_image_thread.wait()

            #self.draw_image_thread.wait()

            #t1.join()

            # self.update()

    # 信号函数，相机收集按钮执行关闭，执行代码
    def close_collect_clicked(self):
        print("self.pco_control.start_flag")
        # print(self.pco_control.start_flag)
        try:
            if self.pco_control.start_flag:
                self.pco_control.start_flag = False
                self.draw_thread.join()
                self.pco_control.stop_pco()
                cv2.destroyAllWindows()

                print("相机线程结束")



        except AttributeError:
            # print("zheli")
            QMessageBox.warning(self, '警告',
                                '没有找到相机！请检查连接，并关闭其他相机使用的进程!')

            self.write_log("无相机连接")
            return

    def close_collect_clicked_for_close_software(self):
        print("self.pco_control.start_flag")
        # print(self.pco_control.start_flag)
        try:
            if self.pco_control.start_flag:
                self.pco_control.start_flag = False
                self.draw_thread.join()
                self.pco_control.stop_pco()
                cv2.destroyAllWindows()

                print("相机线程结束")



        except AttributeError:
            # print("zheli")

            self.write_log("关闭相机后没有打开相机")
            return

    # 串口改变信号函数，无用，可删
    def on_combox_changed(self):
        # self.laser_control.portx = self.Serial_box.currentText()
        try:
            self.laser_control.open_serial()

        except Exception as e:
            return

    # 信号函数，改变灰度值界面上的数值
    def onChange(self):

        if ((not self.is_number(self.widgets["image_slider_setting"][2].text())) or
                (not self.is_number(self.widgets["image_slider_setting"][3].text()))):
            return

        try:

            min = int(self.widgets["image_slider_setting"][2].text())
            max = int(self.widgets["image_slider_setting"][3].text())

            self.widgets["image"][0].max = max
            self.widgets["image"][0].min = min

            # 设置lable最大最小
            self.widgets["image_slider_setting"][1].setMinimum(min)
            self.widgets["image_slider_setting"][1].setMaximum(max)

            self.widgets["image_slider_setting"][1].setValue(max)

        except Exception as e:
            pass

    # 信号函数，自动调节灰度 按钮的函数
    def auto_button_pressed(self):
        print("点击")
        self.widgets["image"][0].auto_Flag_press = True

    def auto_button_click(self):

        if self.widgets["image"][0].auto_Flag == False:
            self.widgets["image"][0].auto_Flag = True
        else:
            self.widgets["image"][0].auto_Flag = True

            # self.widgets["image_slider_setting"][2].setText(str(self.widgets["image"][0].auto_min))
            # self.widgets["image_slider_setting"][3].setText(str(self.widgets["image"][0].auto_max))
        #     self.widgets["image_slider_setting"][1].setEnabled(False)
        #     self.widgets["image_slider_setting"][2].setEnabled(False)
        #     self.widgets["image_slider_setting"][3].setEnabled(False)
        #
        # else:
        #     self.widgets["image"][0].auto_Flag = False
        #     self.widgets["image_slider_setting"][1].setEnabled(True)
        #     self.widgets["image_slider_setting"][2].setEnabled(True)
        #     self.widgets["image_slider_setting"][3].setEnabled(True)

    # 判断是否数字的函数
    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass

        return False

    # 打开/关闭 激光 405 按钮函数
    def on_button_405_click(self):
        if self.laser_control.serial_start_flag == True:
            if not self.button_405_flag:
                self.button_405_flag = True
                self.widgets["laser_data"][0].setText("启动")
                self.widgets["laser_data"][0].setStyleSheet("background-color: rgb(170, 85, 255);")

                self.laser_control.open_laser_1()

                # self.laser_control.change_laser_power_1(self.widgets["laser_data"][4].text())

            else:
                self.button_405_flag = False
                self.widgets["laser_data"][0].setText("关闭")
                self.widgets["laser_data"][0].setStyleSheet("background-color: rgb(102, 102, 102)")
                self.laser_control.close_laser_1()

    # 更新激光 405 按钮函数
    def on_update_405_click(self):
        print("尝试更新405")
        if (self.laser_control.serial_start_flag == True) and (self.button_405_flag == True):
            self.laser_control.change_laser_power_1(self.widgets["laser_data"][4].text())

    # 增加激光 405 功率函数
    def button_405_add_clicked(self):
        print("add 405")
        current = int(self.widgets["laser_data"][4].text())
        self.widgets["laser_data"][4].setText(str(current + self.unit_power))

    # 减少激光 405 功率函数
    def button_405_cut_clicked(self):
        print("cut 405")
        current = int(self.widgets["laser_data"][4].text())
        if current > 10:
            self.widgets["laser_data"][4].setText(str(current - self.unit_power))

    def on_button_488_click(self):

        if self.laser_control.serial_start_flag == True:
            if not self.button_488_flag:
                self.button_488_flag = True
                self.widgets["laser_data"][1].setText("启动")
                self.widgets["laser_data"][1].setStyleSheet("background-color: rgb(0, 170, 255);")
                # self.laser_control.open_laser_2()
                # self.laser_control.change_laser_power_2(self.widgets["laser_data"][5].text())
                # wave_change_laser=wave()

                self.wave_change_laser.powerpercen488 = 10
                self.wave_change_laser.ligtopenbuttom488 = 1
                self.wave_change_laser.create()
                q.wave_flag = 0
                while True:
                    if q.wave_flag == 1:
                        break
                t = self.pool_wave.submit(self.wave_change_laser.sent_wave)
                # q.wave_flag=0
                # while True:
                #     if q.wave_flag==1:
                #         break
                # t=self.pool_wave.submit(self.wave_change_laser.sent_wave)
                # t.start()
            else:
                self.button_488_flag = False
                self.widgets["laser_data"][1].setText("关闭")
                self.widgets["laser_data"][1].setStyleSheet("background-color: rgb(102, 102, 102)")
                # self.laser_control.close_laser_2()
                # wave_change_laser=wave()
                self.wave_change_laser.powerpercen488 = 10
                self.wave_change_laser.ligtopenbuttom488 = 0
                self.wave_change_laser.create()
                q.wave_flag = 0
                while True:
                    if q.wave_flag == 1:
                        break
                t = self.pool_wave.submit(self.wave_change_laser.sent_wave)
                # t.start()

    def on_update_488_click(self):
        print("尝试更新488")
        if (self.laser_control.serial_start_flag == True) and (self.button_488_flag == True):
            # self.laser_control.change_laser_power_2(self.widgets["laser_data"][5].text())
            # wave_change_laser = wave()
            self.wave_change_laser.powerpercen488 = int(self.widgets["laser_data"][5].text())
            self.wave_change_laser.ligtopenbuttom488 = 1
            self.wave_change_laser.create()
            q.wave_flag = 0
            while True:
                if q.wave_flag == 1:
                    break
            t = self.pool_wave.submit(self.wave_change_laser.sent_wave)
            # t.start()

    def button_488_add_clicked(self):
        print("add 488")
        current = int(self.widgets["laser_data"][5].text())
        self.widgets["laser_data"][5].setText(str(current + self.unit_power))

    def button_488_cut_clicked(self):
        print("cut 488")
        current = int(self.widgets["laser_data"][5].text())
        if current > 10:
            self.widgets["laser_data"][5].setText(str(current - self.unit_power))

    def on_button_561_click(self):
        if self.laser_control.serial_start_flag == True:
            if not self.button_561_flag:
                self.button_561_flag = True
                self.widgets["laser_data"][2].setText("启动")
                self.widgets["laser_data"][2].setStyleSheet("background-color: rgb(0, 255, 0);")
                self.laser_control.open_laser_3()
                # self.laser_control.change_laser_power_3(self.widgets["laser_data"][6].text())
            else:
                self.button_561_flag = False
                self.widgets["laser_data"][2].setText("关闭")
                self.widgets["laser_data"][2].setStyleSheet("background-color: rgb(102, 102, 102)")
                self.laser_control.close_laser_3()

    def on_update_561_click(self):
        print("尝试更新561")
        if (self.laser_control.serial_start_flag == True) and (self.button_561_flag == True):
            self.laser_control.change_laser_power_3(self.widgets["laser_data"][6].text())

    def button_561_add_clicked(self):
        print("add 561")
        current = int(self.widgets["laser_data"][6].text())
        self.widgets["laser_data"][6].setText(str(current + self.unit_power))

    def button_561_cut_clicked(self):
        print("cut 561")
        current = int(self.widgets["laser_data"][6].text())
        if current > 10:
            self.widgets["laser_data"][6].setText(str(current - self.unit_power))

    def on_button_637_click(self):
        if self.laser_control.serial_start_flag == True:
            if not self.button_637_flag:
                print("激光开始")
                self.button_637_flag = True
                self.widgets["laser_data"][3].setText("启动")
                self.widgets["laser_data"][3].setStyleSheet("background-color: rgb(255, 0, 0);")
                ###self.laser_control.open_laser_4()
                #####构造波形函数
                # wave_change_laser=wave()
                self.wave_change_laser.powerpercen637 = 10
                self.wave_change_laser.ligtopenbuttom637 = 1
                self.wave_change_laser.create()
                q.wave_flag = 0
                while True:
                    if q.wave_flag == 1:
                        break
                t = self.pool_wave.submit(self.wave_change_laser.sent_wave)
                # t.start()

                # self.laser_control.change_laser_power_4(self.widgets["laser_data"][7].text())
            else:
                self.button_637_flag = False
                self.widgets["laser_data"][3].setText("关闭")
                self.widgets["laser_data"][3].setStyleSheet("background-color: rgb(102, 102, 102)")
                # self.laser_control.close_laser_4()
                # wave_change_laser=wave()
                self.wave_change_laser.powerpercen637 = 10
                self.wave_change_laser.ligtopenbuttom637 = 0
                self.wave_change_laser.create()
                q.wave_flag = 0
                while True:
                    if q.wave_flag == 1:
                        break
                t = self.pool_wave.submit(self.wave_change_laser.sent_wave)
                # t.start()

    def on_update_637_click(self):
        print("尝试更新637")
        if (self.laser_control.serial_start_flag == True) and (self.button_637_flag == True):
            # self.laser_control.change_laser_power_4(self.widgets["laser_data"][7].text())
            # wave_change_laser = wave()
            self.wave_change_laser.powerpercen637 = int(self.widgets["laser_data"][7].text())
            print(self.wave_change_laser.powerpercen637)
            self.wave_change_laser.ligtopenbuttom637 = 1
            self.wave_change_laser.create()
            q.wave_flag = 0
            while True:
                if q.wave_flag == 1:
                    break
            t = self.pool_wave.submit(self.wave_change_laser.sent_wave)
            # t.start()

    def button_637_add_clicked(self):
        print("add 637")
        current = int(self.widgets["laser_data"][7].text())
        self.widgets["laser_data"][7].setText(str(current + self.unit_power))

    def button_637_cut_clicked(self):
        print("cut 637")
        current = int(self.widgets["laser_data"][7].text())
        if current > 10:
            self.widgets["laser_data"][7].setText(str(current - self.unit_power))

    # 关闭所有激光 按钮函数
    def close_all_laser(self):
        if self.button_405_flag == True:
            self.on_button_405_click()

        if self.button_488_flag == True:
            self.on_button_488_click()

        if self.button_561_flag == True:
            self.on_button_561_click()

        if self.button_637_flag == True:
            self.on_button_637_click()

    # 启动位移台函数。调用位移台类 的连接
    def start_displacement_system(self):
        self.displacement_control_system.connect()
        # self.displacement_get_position=threading.Thread(self.get_position_thread)
        print("zhunbei ")
        # self.displacement_get_position.start()
        self.displacement_control_system.set_axial_speed(1, 30)
        self.displacement_control_system.set_axial_speed(2, 30)
        self.displacement_control_system.set_axial_speed(3, 30)
        # #
        # self.displacement_control_system.hui_dao_yuangchanglingdian()
        # # # time.sleep(2)
        # # # self.chaxun_start()
        # # self.displacement_control_system.hui_dao_yuangchanglingdian()
        # self.displacement_control_system.chaxun_start_for_thread()
        # self.displacement_control_system.set_axial_speed(3, 20)
        # self.displacement_control_system.set_axis_movement(3, 200000)
        # self.displacement_control_system.chaxun_start_for_thread()
        # self.displacement_control_system.set_zero_point()

    # 信号函数，点击位移台 更新位置 的执行函数
    def on_update_button_click(self):
        try:
            if self.displacement_control_system.displacement_start_flag == True:
                self.break_get_position_thread = 0
                self.displacement_get_position.join()
                # self.get_position_thread

                current_x_distance = self.widgets["displacement_control"][6].text()
                current_y_distance = self.widgets["displacement_control"][7].text()
                current_z_distance = self.widgets["displacement_control"][8].text()

                try:
                    x_distance = float(current_x_distance) / 0.05
                    y_distance = float(current_y_distance) / 0.05
                    z_distance = float(current_z_distance) / 0.05
                except:
                    current_x_distance = float(
                        str(self.displacement_control_system.query_position("x_position"))[0:-2]) * 0.05
                    current_y_distance = float(
                        str(self.displacement_control_system.query_position("y_position"))[0:-2]) * 0.05
                    current_z_distance = float(
                        str(self.displacement_control_system.query_position("z_position"))[0:-2]) * 0.05
                    x_distance = float(current_x_distance) / 0.05
                    y_distance = float(current_y_distance) / 0.05
                    z_distance = float(current_z_distance) / 0.05
                    print("请输入正确的数值")

                self.displacement_control_system.set_axial_speed(1, self.x_speed)
                self.displacement_control_system.set_axial_speed(2, self.y_speed)
                self.displacement_control_system.set_axial_speed(3, self.z_speed)

                self.displacement_control_system.chuansong_1(x_distance)
                self.displacement_control_system.chuansong_2(y_distance)
                self.displacement_control_system.chuansong_3(z_distance)
                self.displacement_control_system.chuansong_start_flag(1)

                # self.displacement_control_system.update_move_and_query(1)

                # print('ka')
                # self.displacement_control_system.update_move_and_query(2)
                # self.displacement_control_system.update_move_and_query(3)
                # t= threading.Thread(target=self.chaxun_1)
                # t.start()

                # print('ka')

                # x_position = float(str(self.displacement_control_system.query_position("x_position"))[0:-2]) * 0.05
                # y_position = float(str(self.displacement_control_system.query_position("y_position"))[0:-2]) * 0.05
                # z_position = float(str(self.displacement_control_system.query_position("z_position"))[0:-2]) * 0.05
                #
                #
                # print("x_position = ", x_position)
                # print("y_position = ", y_position)
                # print("z_position = ", z_position)
                # x_position = round(x_position, 2)
                # y_position = round(y_position, 2)
                # z_position = round(z_position, 2)
                #
                # # 版本1
                # self.widgets["displacement_control"][3].setText(str(x_position))
                # self.widgets["displacement_control"][4].setText(str(y_position))
                # self.widgets["displacement_control"][5].setText(str(z_position))

                # 版本2
                # x
                # if abs(x_position - float(current_x_distance)) <= 0.05:
                #     self.widgets["displacement_control"][3].setText(self.widgets["displacement_control"][6].text())
                #     print("改变x")
                # else:
                #     self.widgets["displacement_control"][3].setText(str(x_position))
                #
                # # y
                # if abs(y_position - float(current_y_distance)) <= 0.05:
                #     self.widgets["displacement_control"][4].setText(self.widgets["displacement_control"][7].text())
                #     print("改变y")
                # else:
                #     self.widgets["displacement_control"][4].setText(str(y_position))
                #
                # # z
                # if abs(z_position - float(current_z_distance)) <= 0.05:
                #     self.widgets["displacement_control"][5].setText(self.widgets["displacement_control"][8].text())
                #     print("改变z")
                # else:
                #     self.widgets["displacement_control"][5].setText(str(z_position))
                # self.displacement_get_position.start()
                self.displacement_get_position = threading.Thread(target=self.get_position_thread)
                print("zhunbei ")
                self.displacement_get_position.start()


        except AttributeError:
            pass

    # def show(self):
    # while True:

    # self.widgets["displacement_control"][3].setText(str(q.x_position))
    # self.widgets["displacement_control"][4].setText(str(q.y_position))
    # self.widgets["displacement_control"][5].setText(str(q.z_position))
    #########定义一个函数用来做线程获取实时位置
    def get_position_thread(self):
        while True:

            x_position = float(str(self.displacement_control_system.query_position("x_position"))[0:-2]) * 0.05
            y_position = float(str(self.displacement_control_system.query_position("y_position"))[0:-2]) * 0.05
            z_position = float(str(self.displacement_control_system.query_position("z_position"))[0:-2]) * 0.05

            x_position = round(x_position, 2)
            y_position = round(y_position, 2)
            z_position = round(z_position, 2)
            # print("位移台查询位置")

            # 版本1
            self.widgets["displacement_control"][3].setText(str(x_position))
            self.widgets["displacement_control"][4].setText(str(y_position))
            self.widgets["displacement_control"][5].setText(str(z_position))
            # time.sleep(0.2)
            # print("更新位置")
            if self.break_get_position_thread == 0:
                self.break_get_position_thread = 1

                break

    # 保存采集中执行的 启动更新位移台的函数
    def on_update_button_click_start(self):

        if self.displacement_control_system.displacement_start_flag == True:
            # x_distance = float(self.widgets["displacement_control"][9].text()) / 0.05
            # y_distance = float(self.widgets["displacement_control"][10].text()) / 0.05
            try:
                self.x_distance_for_save = (float(
                    self.widgets["displacement_control"][9].text()) + self.xdistance_j * 320) / 0.05
                self.z_distance_for_save = (float(
                    self.widgets["displacement_control"][11].text()) + self.zdistance_i * 27) / 0.05
            except:
                pass

            y_distance = float(self.widgets["displacement_control"][10].text()) / 0.05

            self.displacement_control_system.set_axial_speed(1, 5)
            self.displacement_control_system.set_axial_speed(2, 5)
            self.displacement_control_system.set_axial_speed(3, 5)
            try:
                self.displacement_control_system.chuansong_1(self.x_distance_for_save)
                self.displacement_control_system.chuansong_3(self.z_distance_for_save)
            except:
                pass
            self.displacement_control_system.chuansong_2(y_distance)
            self.displacement_control_system.chuansong_start_flag(1)
            # self.displacement_control_system.update_move_and_query(1)

            print('ka_1')
            # self.displacement_control_system.update_move_and_query(2)
            # self.displacement_control_system.update_move_and_query(3)
            # t = threading.Thread(target=self.chaxun_start())
            # t.start()
            # t.join()
            self.find_displacement_system_start = MyThread_chaxun_start_thread(self.displacement_control_system)
            self.find_displacement_system_start.start()
            self.find_displacement_system_start.wait()
            # .self.displacement_control_system.chuansong_1(x_distance)
            # self.displacement_control_system.chuansong_2(y_distance)
            # self.displacement_control_system.set_axial_speed(1, 0.2)
            # self.displacement_control_system.set_axial_speed(2, 0.2)
            # self.displacement_control_system.set_axial_speed(3, 0.2)
            # try:
            #     self.displacement_control_system.chuansong_1(self.x_distance_for_save)
            #     self.displacement_control_system.chuansong_3(self.z_distance_for_save)
            # except:
            #     pass
            # self.displacement_control_system.chuansong_2(y_distance)
            # self.displacement_control_system.chuansong_start_flag(1)
            # self.displacement_control_system.chaxun()
            # t = threading.Thread(target=self.chaxun_start())
            # t.start()
            # t.join()
            # self.find_displacement_system_start = MyThread_chaxun_start_thread(self.displacement_control_system)
            # self.find_displacement_system_start.start()
            # self.find_displacement_system_start.wait()

            print('ka_!')

            # x_position = float(str(self.displacement_control_system.query_position("x_position"))[0:-2]) * 0.05
            # y_position = float(str(self.displacement_control_system.query_position("y_position"))[0:-2]) * 0.05
            # z_position = float(str(self.displacement_control_system.query_position("z_position"))[0:-2]) * 0.05

            '''print("x_position = ", x_position)
            print("y_position = ", y_position)
            print("z_position = ", z_position)
            x_position = round(x_position, 2)
            y_position = round(y_position, 2)
            z_position = round(z_position, 2)

            self.widgets["displacement_control"][3].setText(str(x_position))
            self.widgets["displacement_control"][4].setText(str(y_position))
            self.widgets["displacement_control"][5].setText(str(z_position))'''

    # 保存采集中执行的 关闭更新位移台的函数
    def on_update_button_click_end(self):

        if self.displacement_control_system.displacement_start_flag == True:
            # x_distance = float(self.widgets["displacement_control"][12].text()) / 0.05
            # y_distance = float(self.widgets["displacement_control"][13].text()) / 0.05
            # try:
            y_distance = float(self.widgets["displacement_control"][13].text()) / 0.05
            # y_distance=float(self.widgets["displacement_control"][10].text())+float(self.widgets["displacement_control"][14].text())-float(self.widgets["displacement_control"][11].text())
            # y_distance=float(y_distance)/0.05
            # except:
            # z_distance = float(str(self.displacement_control_system.query_position("z_position"))[0:-2]) * 0.05

            self.displacement_control_system.set_axial_speed(1, 0.24)
            self.displacement_control_system.set_axial_speed(2, 8)

            self.displacement_control_system.set_axial_speed(3, 0.5658)

            # self.displacement_control_system.chuansong_1(x_distance)
            # self.displacement_control_system.chuansong_2((0-y_distance))
            self.displacement_control_system.chuansong_2((y_distance))
            self.displacement_control_system.chuansong_start_flag(1)

            # self.displacement_control_system.update_move_and_query(1)

            print('ka')
            # self.displacement_control_system.update_move_and_query(2)
            # self.displacement_control_system.update_move_and_query(3)
            # t = threading.Thread(target=self.chaxun_end)
            # t.start()
            # # t.join()
            time_end = (int(self.widgets["displacement_control"][13].text()) - int(
                self.widgets["displacement_control"][10].text()))  / 400
            time.sleep(abs(time_end +3))
            self.find_displacement_system_end = MyThread_chaxun_end_thread(self.displacement_control_system)
            self.find_displacement_system_end.start()

            print('ka')

            # x_position = float(str(self.displacement_control_system.query_position("x_position"))[0:-2]) * 0.05
            # y_position = float(str(self.displacement_control_system.query_position("y_position"))[0:-2]) * 0.05
            # z_position = float(str(self.displacement_control_system.query_position("z_position"))[0:-2]) * 0.05

            '''print("x_position = ", x_position)
            print("y_position = ", y_position)
            print("z_position = ", z_position)
            x_position = round(x_position, 2)
            y_position = round(y_position, 2)
            z_position = round(z_position, 2)

            self.widgets["displacement_control"][3].setText(str(x_position))
            self.widgets["displacement_control"][4].setText(str(y_position))
            self.widgets["displacement_control"][5].setText(str(z_position))'''

    #######获取位置
    def get_position_for_once(self):
        try:
            x_position = float(str(self.displacement_control_system.query_position("x_position"))[0:-2]) * 0.05
            y_position = float(str(self.displacement_control_system.query_position("y_position"))[0:-2]) * 0.05
            z_position = float(str(self.displacement_control_system.query_position("z_position"))[0:-2]) * 0.05

            x_position = round(x_position, 2)
            y_position = round(y_position, 2)
            z_position = round(z_position, 2)

            # 版本1
            print("get once")
            self.widgets["displacement_control"][3].setText(str(x_position))
            self.widgets["displacement_control"][4].setText(str(y_position))
            self.widgets["displacement_control"][5].setText(str(z_position))
        except:
            pass

    # 设置位移台起点的按钮函数
    def on_start_point_button_click(self):
        print("设置起点")
        x_distance = self.widgets["displacement_control"][6].text()
        y_distance = self.widgets["displacement_control"][7].text()
        z_distance = self.widgets["displacement_control"][8].text()

        self.point_dict["start"] = [x_distance, y_distance, z_distance]
        self.widgets["displacement_control"][9].setText(x_distance)
        self.widgets["displacement_control"][10].setText(y_distance)
        self.widgets["displacement_control"][11].setText(z_distance)
        # print(self.widgets["displacement_control"][9].text())
        # print(self.widgets["displacement_control"][10].text())
        print(self.point_dict)

    # 设置位移台终点的按钮函数
    def on_end_point_button_click(self):
        print("设置终点")
        x_distance = self.widgets["displacement_control"][6].text()
        y_distance = self.widgets["displacement_control"][7].text()
        z_distance = self.widgets["displacement_control"][8].text()

        self.point_dict["end"] = [x_distance, y_distance, z_distance]
        self.widgets["displacement_control"][12].setText(x_distance)
        self.widgets["displacement_control"][13].setText(y_distance)
        self.widgets["displacement_control"][14].setText(z_distance)

    # 查询位移台的函数
    def chaxun(self):
        self.displacement_control_system.update_move_and_query(1)

        self.displacement_control_system.update_move_and_query(2)
        self.displacement_control_system.update_move_and_query(3)
        # q.start_save_weiyitai = 1
        # q.start_save_weiyitai = 1

    # 启动查询位移台的函数
    def chaxun_start(self):

        self.displacement_control_system.update_move_and_query(1)
        print("x停止")

        self.displacement_control_system.update_move_and_query(2)
        print("y停止")

        self.displacement_control_system.update_move_and_query(3)
        print("z停止")

    # 结束位移台查询的函数
    def chaxun_end(self):

        self.displacement_control_system.update_move_and_query(1)
        print("x停止")

        self.displacement_control_system.update_move_and_query(2)
        print("y停止")

        self.displacement_control_system.update_move_and_query(3)
        print("z停止")
        # self.lock_thread.acquire()
        q.start_save_weiyitai = 1
        # self.lock_thread.release()

        # q.start_save_buttom = 0
        # self.widgets["start_button"][1].setText("采集数据")

        print("到这里了")

    # 设置位移台速度 慢中快的速度定义
    def set_speed(self, current_text):
        speed = 0
        if current_text == "慢":
            speed = 0.240
            # speed = 0.1
        elif current_text == "中":
            speed = 1
        elif current_text == "快":
            speed = 10
        return speed

    # 设置位移台 x 的速度 的界面更新
    def set_x_speed(self):
        self.x_speed = self.set_speed(self.widgets["displacement_control"][0].currentText())

    # 设置位移台 y 的速度 的界面更新
    def set_y_speed(self):
        self.y_speed = self.set_speed(self.widgets["displacement_control"][1].currentText())

    # 设置位移台 z 的速度 的界面更新
    def set_z_speed(self):
        self.z_speed = self.set_speed(self.widgets["displacement_control"][2].currentText())

    # 启动位移台的函数
    def displacement_start(self):
        try:
            self.start_displacement_system()

            self.displacement_control_system.displacement_start_flag = True
        except Exception as e:
            return

        x_distance = float(self.widgets["displacement_control"][6].text()) / 0.05
        y_distance = float(self.widgets["displacement_control"][7].text()) / 0.05
        z_distance = float(self.widgets["displacement_control"][8].text()) / 0.05
        # print("z_distance=",z_distance)

        # self.displacement_control_system.set_axial_speed(1, self.x_speed)
        # self.displacement_control_system.set_axial_speed(2, self.y_speed)
        # self.displacement_control_system.set_axial_speed(3, self.z_speed)

        # self.displacement_control_system.set_axis_movement(1, str(x_distance))
        # self.displacement_control_system.set_axis_movement(2, str(y_distance))
        # self.displacement_control_system.set_axis_movement(3, str(z_distance))

        # self.displacement_control_system.update_move_and_query(1)
        # self.displacement_control_system.update_move_and_query(2)
        # self.displacement_control_system.update_move_and_query(3)

        # g=threading.Thread(target=self.chaxun)
        # g.start()

        # print(float(str(self.displacement_control_system.query_position("x_position"))[0:-2])*0.05)
        # print(self.displacement_control_system.query_position("y_position"))
        x_position = float(str(self.displacement_control_system.query_position("x_position"))[0:-2]) * 0.05
        y_position = float(str(self.displacement_control_system.query_position("y_position"))[0:-2]) * 0.05
        z_position = float(str(self.displacement_control_system.query_position("z_position"))[0:-2]) * 0.05

        print("x_position = ", x_position)
        print("y_position = ", y_position)
        print("z_position = ", z_position)
        x_position = round(x_position, 2)
        y_position = round(y_position, 2)
        z_position = round(z_position, 2)

        self.widgets["displacement_control"][3].setText(str(x_position))
        self.widgets["displacement_control"][4].setText(str(y_position))
        self.widgets["displacement_control"][5].setText(str(z_position))
        self.displacement_get_position = threading.Thread(target=self.get_position_thread)
        print("zhunbei ")
        self.displacement_get_position.start()

    # 创建 采集图片的界面 函数
    def create_image(self):
        # self.image_box = QGroupBox("采集相片显示")
        # self.image_box.setMinimumSize(1000, 800)

        canvas = Image2D()
        layout = QGridLayout()
        # self.label = QLabel()
        # self.label_1=QLabel()
        #
        # layout.addWidget(self.label,0,0,2,2,QtCore.Qt.AlignBottom)
        # layout.addWidget(self.label_1,0,3,2,2,QtCore.Qt.AlignBottom)

        # canvas.setMinimumSize(1000, 800)
        # layout = QGridLayout()
        # layout.addWidget(canvas)
        # print(canvas)

        # self.image_box.setLayout(layout)
        self.widgets["image"] = [canvas, layout]

    # 灰度值 滑块信号改变 执行的函数
    def gray_slider_Change(self, value):

        current_value = self.widgets["image_slider_setting"][4].text()

        self.widgets["image_slider_setting"][3].setText(current_value)
        # self.widgets["image_slider_setting"][1].setMaximum(int(current_value))
        # self.onChange()

        min = int(self.widgets["image_slider_setting"][2].text())
        max = int(self.widgets["image_slider_setting"][3].text())

        self.widgets["image"][0].max = max
        self.widgets["image"][0].min = min

    # 创建 文字标签的通用函数
    def createText(self, str, sizeList):
        font = PyQt5.QtGui.QFont()
        font.setPointSize(sizeList[0])
        text = QLineEdit()
        text.setEnabled(False)
        text.setStyleSheet('background:transparent;border-width:0;border-style:outset;')
        text.setText(str)
        text.setFont(font)
        text.setMaximumSize(sizeList[1], sizeList[2])

        return text

    # 创建按钮的通用函数
    def create_Button(self, text, sizeList, color_text="rgb(102,102,102)"):
        switch_button = QPushButton()
        switch_button.setFocusPolicy(Qt.NoFocus)
        switch_button.setText(text)
        switch_button.setStyleSheet(f"background-color:{color_text};")
        switch_button.setMaximumSize(sizeList[0], sizeList[1])
        return switch_button

    # 创建位移台复选框的函数
    def create_displacement_comboBox(self):
        combox = QComboBox()
        combox.addItem("快")
        combox.addItem("中")
        combox.addItem("慢")
        return combox

    # 关闭主界面的信号函数
    def closeEvent(self, event):
        try:
            self.close_collect_clicked_for_close_software()
            # self.laser_control.close_serial()
            q.wave_flag = 0
            q.f.close()
            self.displacement_control_system.close_connect()
            while True:
                if q.wave_flag == 1:
                    break
        except AttributeError:
            self.write_log("没有创建串口对象")

    # 判断是否存在 日志文件夹 的函数
    def judge_path(self):

        if not os.path.exists("log"):
            os.mkdir("log")

        current_time = self.GetTiem("%Y%m%d%H%M%S")
        self.log_name = f"./log/{current_time}.txt"
        f = open(self.log_name, "w", encoding="utf-8")
        f.close()

    # 写入 日志 的通用函数
    def write_log(self, log):
        log_time = self.GetTiem("%Y-%m-%d %H:%M:%S")

        log_mes = log_time + ": " + log
        f = open(self.log_name, "a", encoding="utf-8")
        f.write(log_mes + "\n")
        f.close()

    #####点击按钮后，确定存储的位置
    def insure_save_direction(self):
        root = tk.Tk()
        root.withdraw()
        # 获取文件夹路径
        self.f_path = filedialog.askdirectory()
        print(self.f_path)

    # 获取当前时间的函数
    def GetTiem(self, timeFormat):
        return time.strftime(timeFormat, time.localtime(time.time()))

    def update_painter(self, hist, photo):
        # hist = cv2.cvtColor(hist, cv2.COLOR_BGR2GRAY)
        height, width, depth = hist.shape

        depth = width * depth
        QImg = QImage(hist, width, height, depth, QImage.Format_RGB888)
        # QImg = QImage(self.imagedata.data, width, height, QImage.Format_Grayscale16*10)
        size = QSize(200, 200)
        pixmap_1 = QPixmap.fromImage(QImg.scaled(size, Qt.IgnoreAspectRatio))
        #################
        height, width = photo.shape
        QImg = QImage(photo.data, width, height, QImage.Format_Grayscale8)
        # QImg = QImage(self.imagedata.data, width, height, QImage.Format_Grayscale16*10)
        size = QSize(800, 80)
        pixmap = QPixmap.fromImage(QImg.scaled(size, Qt.IgnoreAspectRatio))
        self.label_for_paint[0].setPixmap(pixmap)
        self.label_for_paint[0].setCursor(Qt.CrossCursor)
        self.label_for_paint[1].setPixmap(pixmap_1)
        self.label_for_paint[1].setCursor(Qt.CrossCursor)
        self.update()


# 主函数，启动主程序
def start_app():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # 设置主题
    color_palette = color_setting
    app.setPalette(color_palette.set_dark())

    login = User_Manage()  # 创建自定义APP 界面对象
    gallery = App(login.login_user)  # 创建自定义APP 界面对象

    gallery.show()

    # if (login.exec() == QDialog.Accepted):
    #     gallery = App(login.login_user)  # 创建自定义APP 界面对象
    #     gallery.show()cl
    #
    #     return app.exec()
    # else:
    #     return

    return app.exec()


if __name__ == '__main__':
    PyQt5.QtCore.QCoreApplication.setAttribute(PyQt5.QtCore.Qt.AA_EnableHighDpiScaling)
    start_app()