import threading

import PyQt5
import sys
import os
import time
from PyQt5.QtWidgets import (QApplication, QGroupBox, QDialog, QLineEdit, QLabel, QSlider,
                             QPushButton, QGridLayout, QMessageBox, QStatusBar, QComboBox, QProgressBar)
from PyQt5.QtCore import Qt, QBasicTimer
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtGui
import q
import math
from view3D import View3D

import color_setting
from image_canvas import Image2D
from user_manage import User_Manage
from pco_control import PCO_Control
from displacement_system import Displacement_Table_Control
from laser_control import LaserControl


class App(QDialog):

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
        self.x_speed = 0.044
        self.y_speed = 0.044
        self.z_speed = 0.044
        self.mylist_x_start = []
        self.mylist_y_start = []
        self.mylist_x_end = []
        self.mylist_y_end = []
        self.mylist_z_start = []
        self.mylist_z_end = 0

        # 初始启动位移台
        self.displacement_start()

        self.judge_path()

    def crete_main_widget(self):

        self.setWindowFlags(Qt.WindowMaximizeButtonHint | Qt.WindowMinimizeButtonHint |
                            Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)

        self.create_canvas()
        layout = QGridLayout(self)
        layout.addWidget(self.current_user_box, 0, 1, 2, 1)
        layout.addWidget(self.start_button_box, 2, 1, 1, 1)
        layout.addWidget(self.schedule_bar, 3, 1, 1, 1)
        layout.addWidget(self.laser_box, 4, 1, 4, 1)
        layout.addWidget(self.displacement_system_box, 8, 1, 4, 1)
        layout.addWidget(self.image_slider_box, 0, 2, 20, 2)
        layout.addWidget(self.image_box, 0, 4, 20, 2)
        layout.addWidget(self.view3d_box, 13, 1, 4, 1)
        layout.setAlignment(QtCore.Qt.AlignLeft)
    def create_3d_slider(self):
        self.view3d_box = QGroupBox("相机设置")

        show_3d_button = QComboBox(self)
        # show_3d_button.setFocusPolicy(Qt.NoFocus)
        #
        # show_3d_button.clicked.connect(self.show_3d_view)
        show_3d_button.addItem('Tnternal Trigal')
        show_3d_button.addItem('Edge Trigal')

        save_button = QLabel("触发模式选择")
        # save_button.clicked.connect(self.save_current_button_click)

        show_mode_select = QComboBox()
        show_mode_select.addItem("LineOutput")
        show_mode_select.addItem("Auto")

        save_button_mode = QLabel("模式选择")

        expouse_time = QLineEdit()
        expourse_label = QLabel("曝光时间（us)")
        voiX=QLineEdit()
        voiY = QLineEdit()
        VOI_label = QLabel("ROIXY")

        show_3d_button.setMinimumSize(100, 20)
        layout = QGridLayout()
        layout.addWidget(save_button, 0, 0, 1, 1)
        layout.addWidget(show_3d_button, 1, 0, 1, 1)

        layout.addWidget(save_button_mode, 0, 1, 1, 1)
        layout.addWidget(show_mode_select, 1, 1, 1, 1)
        #
        layout.addWidget(expourse_label, 2, 0, 1, 1)
        layout.addWidget(expouse_time, 2, 1, 1, 2)
        #
        layout.addWidget(VOI_label, 3, 0, 1, 1)
        layout.addWidget(voiX, 3, 1, 1, 1)
        layout.addWidget(voiY, 3, 2, 1, 1)


        self.view3d_box.setMaximumSize(500, 300)
        self.view3d_box.setLayout(layout)
        self.widgets["3d_slider"] = [show_3d_button]
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

        self.file_size -=1
        if self.file_size != 0:
            self.view3D_run()


    # 启动三维的函数
    def view3D_run(self):
        self.view3D = View3D()
        self.view3D.file_path = self.directory
        self.view3D.size_list[5] = self.file_size
        self.view3D.run()
    def save_current_button_click(self):
        print("保存")


        cv2.imwrite("C:\\xiangji\\" + str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))) + '.tiff', self.pco_control.np_image)


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

    def create_schedule_widget(self):
        self.schedule_bar = QGroupBox("进度")

        progress_bar = QProgressBar()
        progress_bar.setOrientation(Qt.Horizontal)

        file_name = self.createText("文件名: ", [10, 70, 12])
        file_edit = QLineEdit()

        layout = QGridLayout()
        layout.addWidget(progress_bar, 0, 0, 1, 2)
        layout.addWidget(file_name, 1, 0, 1, 1)
        layout.addWidget(file_edit, 1, 1, 1, 1)

        self.schedule_bar.setLayout(layout)
        self.widgets["schedule_bar"] = [progress_bar, file_edit]

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

    def create_slider(self):
        self.image_slider_box = QGroupBox("相片设置")
        # self.image_slider_box.setMaximumSize(300,1200)

        name_text = self.createText("灰度值", [10, 50, 50])
        gray_slider = QSlider(Qt.Vertical)

        gray_slider.setMinimum(0)
        gray_slider.setMaximum(256)

        auto_button = QPushButton("自动")
        auto_button.setFocusPolicy(Qt.NoFocus)
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

    def create_laser_setting(self):
        self.laser_box = QGroupBox("激光设置")
        # self.laser_box.setMaximumSize(500,500)

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
        layout.addWidget(power_label, 1, 4, 1, 1)
        layout.addWidget(filter_label, 1, 5, 1, 1)

        layout.addWidget(label_405, 2, 0, 1, 1)
        layout.addWidget(button_405, 2, 2, 1, 1)
        layout.addWidget(update_405, 2, 3, 1, 1)
        layout.addWidget(edit_405_power, 2, 4, 1, 1)
        layout.addWidget(edit_405_filter, 2, 5, 1, 1)

        layout.addWidget(label_488, 3, 0, 1, 1)
        layout.addWidget(button_488, 3, 2, 1, 1)
        layout.addWidget(update_488, 3, 3, 1, 1)
        layout.addWidget(edit_488_power, 3, 4, 1, 1)
        layout.addWidget(edit_488_filter, 3, 5, 1, 1)

        layout.addWidget(label_561, 4, 0, 1, 1)
        layout.addWidget(button_561, 4, 2, 1, 1)
        layout.addWidget(update_561, 4, 3, 1, 1)
        layout.addWidget(edit_561_power, 4, 4, 1, 1)
        layout.addWidget(edit_561_filter, 4, 5, 1, 1)

        layout.addWidget(label_637, 5, 0, 1, 1)
        layout.addWidget(button_637, 5, 2, 1, 1)
        layout.addWidget(update_637, 5, 3, 1, 1)
        layout.addWidget(edit_637_power, 5, 4, 1, 1)
        layout.addWidget(edit_637_filter, 5, 5, 1, 1)

        layout.addWidget(button_close_all, 2, 1, 4, 1)
        # layout.setAlignment(QtCore.Qt.AlignLeft)

        self.laser_box.setLayout(layout)
        self.widgets["laser_data"] = [button_405, button_488, button_561, button_637,
                                      edit_405_power, edit_488_power, edit_561_power, edit_637_power,
                                      edit_405_filter, edit_488_filter, edit_561_filter, edit_637_filter]

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
        distance_text = self.createText("目标位置", [10, 150, 20])
        start_text = self.createText("起点位置", [10, 150, 20])
        end_text = self.createText("终点位置", [10, 150, 20])

        location_tip = self.createText("μm", [10, 150, 20])
        distance_tip = self.createText("±12500μm", [10, 150, 20])
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

        update_button = QPushButton("更新位置")
        start_point_button = QPushButton("设置起点")
        end_point_button = QPushButton("设置终点")

        update_button.setFocusPolicy(Qt.NoFocus)
        start_point_button.setFocusPolicy(Qt.NoFocus)
        end_point_button.setFocusPolicy(Qt.NoFocus)

        # start_button.clicked.connect(self.displacement_start)
        update_button.clicked.connect(self.on_update_button_click)
        start_point_button.clicked.connect(self.on_start_point_button_click)
        end_point_button.clicked.connect(self.on_end_point_button_click)

        layout = QGridLayout(self)
        layout.addWidget(speed_text, 0, 1, 1, 1)
        layout.addWidget(location_text, 0, 2, 1, 1)
        layout.addWidget(distance_text, 0, 3, 1, 1)
        layout.addWidget(start_text, 0, 4, 1, 1)
        layout.addWidget(end_text, 0, 5, 1, 1)

        layout.addWidget(location_tip, 1, 2, 1, 1)
        layout.addWidget(distance_tip, 1, 3, 1, 1)
        layout.addWidget(start_tip, 1, 4, 1, 1)
        layout.addWidget(end_tip, 1, 5, 1, 1)

        layout.addWidget(x_text, 2, 0, 1, 1)
        layout.addWidget(y_text, 3, 0, 1, 1)
        layout.addWidget(z_text, 4, 0, 1, 1)

        layout.addWidget(x_speed_combox, 2, 1, 1, 1)
        layout.addWidget(y_speed_combox, 3, 1, 1, 1)
        layout.addWidget(z_speed_combox, 4, 1, 1, 1)

        layout.addWidget(x_location_edit, 2, 2, 1, 1)
        layout.addWidget(y_location_edit, 3, 2, 1, 1)
        layout.addWidget(z_location_edit, 4, 2, 1, 1)

        layout.addWidget(x_distance_edit, 2, 3, 1, 1)
        layout.addWidget(y_distance_edit, 3, 3, 1, 1)
        layout.addWidget(z_distance_edit, 4, 3, 1, 1)

        layout.addWidget(x_start_edit, 2, 4, 1, 1)
        layout.addWidget(y_start_edit, 3, 4, 1, 1)
        layout.addWidget(z_start_edit, 4, 4, 1, 1)

        layout.addWidget(x_end_edit, 2, 5, 1, 1)
        layout.addWidget(y_end_edit, 3, 5, 1, 1)
        layout.addWidget(z_end_edit, 4, 5, 1, 1)

        # layout.addWidget(start_button, 5,1,1,1)
        layout.addWidget(update_button, 5, 2, 1, 1)
        layout.addWidget(start_point_button, 5, 4, 1, 1)
        layout.addWidget(end_point_button, 5, 5, 1, 1)

        self.displacement_system_box.setLayout(layout)

        self.widgets["displacement_control"] = [x_speed_combox, y_speed_combox, z_speed_combox,
                                                x_location_edit, y_location_edit, z_location_edit,
                                                x_distance_edit, y_distance_edit, z_distance_edit,
                                                x_start_edit, y_start_edit, z_start_edit,
                                                x_end_edit, y_end_edit, z_end_edit, update_button]

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

    def create_start_button(self):
        self.start_button_box = QGroupBox("")
        # self.start_button_box.setMaximumSize(500, 500)

        start_button = QPushButton("打开相机")
        save_button = QPushButton("采集数据")

        start_button.setFocusPolicy(Qt.NoFocus)
        save_button.setFocusPolicy(Qt.NoFocus)

        start_button.clicked.connect(self.start_collect_clicked)
        save_button.clicked.connect(self.save_collect_clicked)

        # exposure_time
        layout = QGridLayout()
        layout.addWidget(start_button, 0, 0, 1, 1)
        layout.addWidget(save_button, 0, 1, 1, 1)

        self.start_button_box.setLayout(layout)
        self.widgets["start_button"] = [start_button, save_button, layout]

    def save_collect_clicked(self):
        print("调用了保存采集")
        print(self.pco_save_flag)
        self.create_list()
        self.displacement_control_system.shuju_shuru(1, self.mylist_x_start)
        self.displacement_control_system.shuju_shuru(2, self.mylist_y_start)
        self.displacement_control_system.shuju_shuru(3, self.mylist_z_start)
        q.filename = self.widgets["schedule_bar"][1].text()
        x_distance = float(self.widgets["displacement_control"][9].text()) / 0.05
        y_distance = float(self.widgets["displacement_control"][10].text()) / 0.05
        z_distance = float(self.widgets["displacement_control"][11].text()) / 0.05

        self.on_update_button_click_start(x_distance, y_distance, z_distance)  #

        if self.pco_save_flag == False:

            try:

                if self.pco_control.start_flag:
                    # self.pco_control.run_save_thread()

                    q.f = open("C:\\TEST\\" + str(q.filename) + "_" + str(q.i) + ".bin", 'ab')
                    self.widgets["schedule_bar"][0].setValue(self.step)
                    self.displacement_control_system.start_weiyitai()  ###开启位移台
                    t_weiyitai = threading.Thread(target=self.weiyitia)
                    t_weiyitai.start()
                    # if self.jiancep110_1() == 3
                    # break
                    # self.pco_save_flag = True
                    self.widgets["start_button"][1].setText("采集中...")
                    self.get_m_time()
                    self.schedule_run()
                    # self.pco_save_flag = False



            except AttributeError:
                QMessageBox.warning(self, '警告',
                                    '没有找到相机！请检查连接，并关闭其他相机使用的进程!')

    def weiyitia(self):
        while True:

            if self.displacement_control_system.chaxunp110() == 1:  # 开始存储
                if panduan == 0:
                    q.start_save_buttom = 1
                    panduan = 1
                    # time.sleep(0.1)
            if self.displacement_control_system.chaxunp110() == 2:  # 结束存储
                if panduan == 1:
                    q.start_save_weiyitai = 1
                    panduan = 0
            if self.displacement_control_system.chaxunp110() == 3:
                break
            # if self.jiancep110_1() == 3
            # break

    def get_m_time(self):
        try:
            x_distance_start = float(self.widgets["displacement_control"][9].text())
            y_distance_start = float(self.widgets["displacement_control"][10].text())
            z_distance_start = float(self.widgets["displacement_control"][11].text())

            x_distance_end = float(self.widgets["displacement_control"][12].text())
            y_distance_end = float(self.widgets["displacement_control"][13].text())
            z_distance_end = float(self.widgets["displacement_control"][14].text())

            t1 = math.ceil((z_distance_end - z_distance_start) / 2.2)
            t2 = math.ceil((x_distance_end - x_distance_start) / 500)
            t3 = math.ceil((y_distance_end - y_distance_start) / 500)

            self.m_time = (t1 * t2 * t3) * 10

        except ValueError:
            pass

    def start_collect_clicked(self):
        print("调用了开始收集")

        try:
            if self.Init == False:
                self.pco_control = PCO_Control()


        except ValueError:
            QMessageBox.warning(self, '警告', '没有找到相机！请检查连接，并关闭其他相机使用的进程!')
            return

        if self.pco_control.start_flag == False:
            self.pco_control.start_flag = True
            self.Init = True
            self.pco_control.start_pco()
            self.draw_thread = threading.Thread(target=self.draw_image)
            self.draw_thread.start()

            self.widgets["start_button"][0].setText("关闭相机")

        else:
            self.close_collect_clicked()
            self.widgets["start_button"][0].setText("打开相机")

    def schedule_run(self):
        self.timer.start(int(self.m_time), self)

    def timerEvent(self, e):
        if self.step >= 100:
            self.timer.stop()
            self.step = 0
            self.widgets["start_button"][1].setText("采集数据")
            return

        self.step = self.step + 1
        self.widgets["schedule_bar"][0].setValue(self.step)

    def draw_image(self):
        while self.pco_control.start_flag:
            self.pco_control.start_plot_thread()
            self.widgets["image"][0].imagedata = self.pco_control.np_image
            self.widgets["image"][0].draw()

    def close_collect_clicked(self):
        try:
            if self.pco_control.start_flag:
                self.pco_control.start_flag = False
                self.pco_control.stop_pco()
                self.draw_thread.join()


        except AttributeError:
            QMessageBox.warning(self, '警告',
                                '没有找到相机！请检查连接，并关闭其他相机使用的进程!')

            self.write_log("无相机连接")
            return

    def on_combox_changed(self):
        # self.laser_control.portx = self.Serial_box.currentText()
        try:
            self.laser_control.open_serial()

        except Exception as e:
            return

    def onChange(self):

        if ((not self.is_number(self.widgets["image_slider_setting"][2].text())) or
                (not self.is_number(self.widgets["image_slider_setting"][3].text()))):
            return

        try:
            # 设置lable最大最小
            self.widgets["image_slider_setting"][1].setMinimum(int(self.widgets["image_slider_setting"][2].text()))
            self.widgets["image_slider_setting"][1].setMaximum(int(self.widgets["image_slider_setting"][3].text()))

            min = int(self.widgets["image_slider_setting"][2].text())
            max = int(self.widgets["image_slider_setting"][3].text())

            self.widgets["image"][0].max = max
            self.widgets["image"][0].min = min

            self.widgets["image_slider_setting"][1].setValue(max)

        except Exception as e:
            pass

    def auto_button_click(self):

        if self.widgets["image"][0].auto_Flag == False:
            self.widgets["image"][0].auto_Flag = True
            self.widgets["image_slider_setting"][1].setEnabled(False)
            self.widgets["image_slider_setting"][2].setEnabled(False)
            self.widgets["image_slider_setting"][3].setEnabled(False)

        else:
            self.widgets["image"][0].auto_Flag = False
            self.widgets["image_slider_setting"][1].setEnabled(True)
            self.widgets["image_slider_setting"][2].setEnabled(True)
            self.widgets["image_slider_setting"][3].setEnabled(True)

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

    def on_update_405_click(self):
        print("尝试更新405")
        if (self.laser_control.serial_start_flag == True) and (self.button_405_flag == True):
            self.laser_control.change_laser_power_1(self.widgets["laser_data"][4].text())

    def on_button_488_click(self):

        if self.laser_control.serial_start_flag == True:
            if not self.button_488_flag:
                self.button_488_flag = True
                self.widgets["laser_data"][1].setText("启动")
                self.widgets["laser_data"][1].setStyleSheet("background-color: rgb(0, 170, 255);")
                self.laser_control.open_laser_2()
                # self.laser_control.change_laser_power_2(self.widgets["laser_data"][5].text())
            else:
                self.button_488_flag = False
                self.widgets["laser_data"][1].setText("关闭")
                self.widgets["laser_data"][1].setStyleSheet("background-color: rgb(102, 102, 102)")
                self.laser_control.close_laser_2()

    def on_update_488_click(self):
        print("尝试更新488")
        if (self.laser_control.serial_start_flag == True) and (self.button_488_flag == True):
            self.laser_control.change_laser_power_2(self.widgets["laser_data"][5].text())

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

    def on_button_637_click(self):
        if self.laser_control.serial_start_flag == True:
            if not self.button_637_flag:
                self.button_637_flag = True
                self.widgets["laser_data"][3].setText("启动")
                self.widgets["laser_data"][3].setStyleSheet("background-color: rgb(255, 0, 0);")
                self.laser_control.open_laser_4()
                # self.laser_control.change_laser_power_4(self.widgets["laser_data"][7].text())
            else:
                self.button_637_flag = False
                self.widgets["laser_data"][3].setText("关闭")
                self.widgets["laser_data"][3].setStyleSheet("background-color: rgb(102, 102, 102)")
                self.laser_control.close_laser_4()

    def on_update_637_click(self):
        print("尝试更新637")
        if (self.laser_control.serial_start_flag == True) and (self.button_637_flag == True):
            self.laser_control.change_laser_power_4(self.widgets["laser_data"][7].text())

    def close_all_laser(self):

        if ((self.button_405_flag == True) and (self.button_488_flag == True) and
                (self.button_561_flag == True) and (self.button_637_flag == True)):
            print("关闭全部激光")
            self.on_button_405_click()
            self.on_button_488_click()
            self.on_button_561_click()
            self.on_button_637_click()

    def start_displacement_system(self):
        self.displacement_control_system.connect()

    def on_update_button_click(self):
        try:
            if self.displacement_control_system.displacement_start_flag == True:
                x_distance = float(self.widgets["displacement_control"][6].text()) / 0.05
                y_distance = float(self.widgets["displacement_control"][7].text()) / 0.05
                z_distance = float(self.widgets["displacement_control"][8].text()) / 0.05

                self.displacement_control_system.set_axial_speed(1, self.x_speed)
                self.displacement_control_system.set_axial_speed(2, self.y_speed)
                self.displacement_control_system.set_axial_speed(3, self.z_speed)

                self.displacement_control_system.chuansong_1(x_distance)
                self.displacement_control_system.chuansong_2(y_distance)
                self.displacement_control_system.chuansong_3(z_distance)
                # self.displacement_control_system.update_move_and_query(1)

                # print('ka')
                # self.displacement_control_system.update_move_and_query(2)
                # self.displacement_control_system.update_move_and_query(3)
                # t= threading.Thread(target=self.chaxun_1)
                # t.start()

                # print('ka')

                x_position = float(str(self.displacement_control_system.query_position("x_position"))[0:-2]) * 0.05
                y_position = float(str(self.displacement_control_system.query_position("y_position"))[0:-2]) * 0.05
                z_position = float(str(self.displacement_control_system.query_position("z_position"))[0:-2]) * 0.05

                print("x_position = ", x_position)
                print("y_position = ", y_position)
                print("z_position = ", z_position)
                x_position = round(x_position, 2)
                y_position = round(y_position, 2)
                z_position = round(z_position, 2)

                # 版本1
                self.widgets["displacement_control"][3].setText(str(x_position))
                self.widgets["displacement_control"][4].setText(str(y_position))
                self.widgets["displacement_control"][5].setText(str(z_position))

        except AttributeError:
            pass

    # def show(self):
    # while True:

    # self.widgets["displacement_control"][3].setText(str(q.x_position))
    # self.widgets["displacement_control"][4].setText(str(q.y_position))
    # self.widgets["displacement_control"][5].setText(str(q.z_position))

    def create_list(self):
        x_distance_start = float(self.widgets["displacement_control"][9].text()) / 0.05
        y_distance_start = float(self.widgets["displacement_control"][10].text()) / 0.05
        z_distance_start = float(self.widgets["displacement_control"][11].text()) / 0.05
        x_distance_end = float(self.widgets["displacement_control"][12].text()) / 0.05
        y_distance_end = float(self.widgets["displacement_control"][13].text()) / 0.05
        z_distance_end = float(self.widgets["displacement_control"][14].text()) / 0.05
        y_number = (y_distance_end - y_distance_start) // 10000 + 2  ###确认y的数值
        x_number = (x_distance_end - x_distance_start) // 10000 + 2
        for i in range(0, int(y_number)):
            list_append_y_start = y_distance_start + i * 10000
            self.mylist_y_start.append(int(list_append_y_start))
        for j in range(0, int(x_number)):
            list_append_x_start = x_distance_start + j * 10000
            self.mylist_x_start.append(int(list_append_x_start))
        self.mylist_z_start.append(int(z_distance_end))
        self.mylist_z_start.append(int(z_distance_start))  # 获取数据



    def on_update_button_click_start(self, x_distance, y_distance, z_distance):

        if self.displacement_control_system.displacement_start_flag == True:
            # x_distance = float(self.widgets["displacement_control"][9].text()) / 0.05
            # y_distance = float(self.widgets["displacement_control"][10].text()) / 0.05
            # z_distance = float(self.widgets["displacement_control"][11].text()) / 0.05

            self.displacement_control_system.set_axial_speed(1, 5)
            self.displacement_control_system.set_axial_speed(2, 5)
            self.displacement_control_system.set_axial_speed(3, 5)

            self.displacement_control_system.set_axis_movement(1,x_distance)
            self.displacement_control_system.set_axis_movement(2,y_distance)
            self.displacement_control_system.set_axis_movement(3,z_distance)
            # self.displacement_control_system.update_move_and_query(1)

            print('ka')
            # self.displacement_control_system.update_move_and_query(2)
            # self.displacement_control_system.update_move_and_query(3)
            t = threading.Thread(target=self.chaxun_start)
            t.start()
            t.join()
            self.displacement_control_system.set_axis_movement(3,z_distance)
            time.sleep(0.1)

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

    def on_update_button_click_end(self, x_distance, y_distance, z_distance):

        if self.displacement_control_system.displacement_start_flag == True:
            # x_distance = float(self.widgets["displacement_control"][12].text()) / 0.05
            # y_distance = float(self.widgets["displacement_control"][13].text()) / 0.05
            # z_distance = float(self.widgets["displacement_control"][14].text()) / 0.05

            self.displacement_control_system.set_axial_speed(1, self.x_speed)
            self.displacement_control_system.set_axial_speed(2, self.y_speed)
            self.displacement_control_system.set_axial_speed(3, self.z_speed)

            self.displacement_control_system.chuansong_1(x_distance)
            self.displacement_control_system.chuansong_2(y_distance)
            self.displacement_control_system.chuansong_3(z_distance)

            # self.displacement_control_system.update_move_and_query(1)

            print('ka')
            # self.displacement_control_system.update_move_and_query(2)
            # self.displacement_control_system.update_move_and_query(3)
            t = threading.Thread(target=self.chaxun_end())
            t.start()
            # t.join()

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

    def on_start_point_button_click(self):
        print("设置起点")
        x_distance = self.widgets["displacement_control"][9].text()
        y_distance = self.widgets["displacement_control"][10].text()
        z_distance = self.widgets["displacement_control"][11].text()

        self.point_dict["start"] = [x_distance, y_distance, z_distance]
        print(self.point_dict)

    def on_end_point_button_click(self):
        print("设置终点")
        x_distance = self.widgets["displacement_control"][12].text()
        y_distance = self.widgets["displacement_control"][13].text()
        z_distance = self.widgets["displacement_control"][14].text()

        self.point_dict["end"] = [x_distance, y_distance, z_distance]
        print(self.point_dict)

    def chaxun(self):
        self.displacement_control_system.update_move_and_query(1)

        self.displacement_control_system.update_move_and_query(2)
        self.displacement_control_system.update_move_and_query(3)
        # q.start_save_weiyitai = 1
        # q.start_save_weiyitai = 1

    def chaxun_start(self):

        self.displacement_control_system.update_move_and_query(1)
        print("x停止")

        self.displacement_control_system.update_move_and_query(2)
        print("y停止")

        self.displacement_control_system.update_move_and_query(3)
        print("z停止")

    def chaxun_end(self):

        self.displacement_control_system.update_move_and_query(1)
        print("x停止")

        self.displacement_control_system.update_move_and_query(2)
        print("y停止")

        self.displacement_control_system.update_move_and_query(3)
        print("z停止")
        q.start_save_weiyitai = 1

        # q.start_save_buttom = 0
        # self.widgets["start_button"][1].setText("采集数据")

        print("到这里了")

    def set_speed(self, current_text):
        speed = 0
        if current_text == "慢":
            speed = 0.044
        elif current_text == "中":
            speed = 1
        elif current_text == "快":
            speed = 5
        return speed

    def set_x_speed(self):
        self.x_speed = self.set_speed(self.widgets["displacement_control"][0].currentText())

    def set_y_speed(self):
        self.y_speed = self.set_speed(self.widgets["displacement_control"][1].currentText())

    def set_z_speed(self):
        self.z_speed = self.set_speed(self.widgets["displacement_control"][2].currentText())

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

        self.displacement_control_system.set_axial_speed(1, self.x_speed)
        self.displacement_control_system.set_axial_speed(2, self.y_speed)
        self.displacement_control_system.set_axial_speed(3, self.z_speed)

        self.displacement_control_system.set_axis_movement(1, str(x_distance))
        self.displacement_control_system.set_axis_movement(2, str(y_distance))
        self.displacement_control_system.set_axis_movement(3, str(z_distance))

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

    def create_image(self):
        self.image_box = QGroupBox("采集相片显示")
        # self.image_box.setMinimumSize(1000, 720)

        canvas = Image2D()
        canvas.setMinimumSize(1000, 720)
        layout = QGridLayout()
        layout.addWidget(canvas)

        self.image_box.setLayout(layout)
        self.widgets["image"] = [canvas, layout]

    def gray_slider_Change(self, value):

        current_value = self.widgets["image_slider_setting"][4].text()

        self.widgets["image_slider_setting"][3].setText(current_value)
        # self.widgets["image_slider_setting"][1].setMaximum(int(current_value))
        # self.onChange()

        min = int(self.widgets["image_slider_setting"][2].text())
        max = int(self.widgets["image_slider_setting"][3].text())

        self.widgets["image"][0].max = max
        self.widgets["image"][0].min = min

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

    def create_Button(self, text, sizeList, color_text="rgb(102,102,102)"):
        switch_button = QPushButton()
        switch_button.setFocusPolicy(Qt.NoFocus)
        switch_button.setText(text)
        switch_button.setStyleSheet(f"background-color:{color_text};")
        switch_button.setMaximumSize(sizeList[0], sizeList[1])
        return switch_button

    def create_displacement_comboBox(self):
        combox = QComboBox()
        combox.addItem("慢")
        combox.addItem("中")
        combox.addItem("快")
        return combox

    def closeEvent(self, event):
        try:
            self.close_collect_clicked()
            self.laser_control.close_serial()
        except AttributeError:
            self.write_log("没有创建串口对象")

    def judge_path(self):

        if not os.path.exists("log"):
            os.mkdir("log")

        current_time = self.GetTiem("%Y%m%d%H%M%S")
        self.log_name = f"./log/{current_time}.txt"
        f = open(self.log_name, "w", encoding="utf-8")
        f.close()

    def write_log(self, log):
        log_time = self.GetTiem("%Y-%m-%d %H:%M:%S")

        log_mes = log_time + ": " + log
        f = open(self.log_name, "a", encoding="utf-8")
        f.write(log_mes + "\n")
        f.close()

    def GetTiem(self, timeFormat):
        return time.strftime(timeFormat, time.localtime(time.time()))


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
    #     gallery.show()
    #
    #     return app.exec()
    # else:
    #     return

    return app.exec()


if __name__ == '__main__':
    PyQt5.QtCore.QCoreApplication.setAttribute(PyQt5.QtCore.Qt.AA_EnableHighDpiScaling)
    start_app()