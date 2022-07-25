import vtk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

from mpl_toolkits.mplot3d import Axes3D
import cv2
from PIL import Image
import time
import math
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor as QVTKWidget
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QGridLayout, QGroupBox, QSlider, QLineEdit, QPushButton
from PyQt5.QtGui import QPaintEvent
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QFont

import threading
from vtkmodules.vtkCommonCore import vtkCommand
from threading import Thread
import os
import datetime

os.environ["CUDA_VISIBLE_DEVICES"] = "0"


class View3D(QWidget, QThread):

    # 三维初始化,创建类的时候，执行这个初始化
    def __init__(self, parent=None):
        super().__init__(parent)
        self.file_path = ""
        self.resize(1100, 700)
        self.setWindowTitle("三维展示")
        self.Render_Flag = False
        self.plane_widget_Flag = False
        self.preview = False
        self.size_list = [0, 1499, 0, 1499, 0, 99]
        self.push_distance = 0
        self.widgets = {}
        self.diff = 5
        self.init_vtk()
        self.SampleRate = [3, 10, 20]

    # 创建vtk 变量
    def init_vtk(self):
        self.Reader = vtk.vtkTIFFReader()
        self.appendFilter = vtk.vtkImageAppendComponents()
        self.mapper = vtk.vtkDataSetMapper()
        self.actor = vtk.vtkActor()
        self.Render = vtk.vtkRenderer()
        self.volumemapper = vtk.vtkGPUVolumeRayCastMapper()
        self.volumeProperty = vtk.vtkVolumeProperty()

        self.axes_actor = vtk.vtkAxesActor()
        self.vtk_widget = QVTKWidget(self)
        self.renWin = self.vtk_widget.GetRenderWindow()
        self.iren = self.renWin.GetInteractor()
        # self.iren = vtk.vtkRenderWindowInteractor()
        self.style = vtk.vtkInteractorStyleTrackballCamera()
        self.iren.SetInteractorStyle(self.style)
        vtk.vtkOutputWindow.SetGlobalWarningDisplay(0)
        self.i=0

        self.extractVOI = vtk.vtkExtractVOI()
        self.extractVOI_red = vtk.vtkExtractVOI()
        self.extractVOI_green = vtk.vtkExtractVOI()
        self.extractVOI_blue = vtk.vtkExtractVOI()
        self.volume = vtk.vtkVolume()

        self.implicitPlaneWidget = vtk.vtkImplicitPlaneWidget()

    # 创建三维主界面
    def create_main_widget(self):
        self.create_3d_slider()
        self.create_view_button()
        self.create_plane_widget()

        self.vtk_widget.setMinimumSize(700, 500)
        self.view3d_angle.setMinimumSize(100, 100)

        layout = QGridLayout(self)
        layout.addWidget(self.view3d_angle, 0, 0, 1, 1)
        layout.addWidget(self.view3d_box, 1, 0, 1, 1)
        layout.addWidget(self.plane_widget, 2, 0, 1, 1)
        layout.addWidget(self.vtk_widget, 0, 1, 3, 1)

    # 创建三维 x,y,z 三轴的界面
    def create_3d_slider(self):
        self.view3d_box = QGroupBox("三维切面提取")

        x_slider = QSlider(Qt.Horizontal)
        y_slider = QSlider(Qt.Horizontal)
        z_slider = QSlider(Qt.Horizontal)

        x_slider.setMinimum(0)
        x_slider.setMaximum(1499)

        y_slider.setMinimum(0)
        y_slider.setMaximum(1499)

        z_slider.setMinimum(0)
        z_slider.setMaximum(self.size_list[5])

        x_slider.setValue(1499)
        y_slider.setValue(1499)
        z_slider.setValue(self.size_list[5])

        x_slider.setPageStep(1)
        y_slider.setPageStep(1)
        y_slider.setPageStep(1)

        x_slider.valueChanged.connect(self.x_3d_slider)
        y_slider.valueChanged.connect(self.y_3d_slider)
        z_slider.valueChanged.connect(self.z_3d_slider)

        x_text = self.createText("X", [10, 10, 12])
        y_text = self.createText("Y", [10, 10, 12])
        z_text = self.createText("Z", [10, 10, 12])

        x_current_text = self.createText("1499", [10, 40, 12])
        y_current_text = self.createText("1499", [10, 40, 12])
        z_current_text = self.createText(str(self.size_list[5]), [10, 40, 12])

        x_max_text = self.createText("1499", [10, 40, 12])
        y_max_text = self.createText("1499", [10, 40, 12])
        z_max_text = self.createText(str(self.size_list[5]), [10, 40, 12])

        current_text = self.createText("当前", [10, 40, 12])
        max_text = self.createText("最大", [10, 40, 12])

        # show_3d_button = QPushButton("显示三维")
        # show_3d_button.clicked.connect(self.show_3d_view)

        layout = QGridLayout()
        layout.addWidget(current_text, 0, 0, 1, 1)
        layout.addWidget(max_text, 0, 3, 1, 1)

        layout.addWidget(x_current_text, 1, 0, 1, 1)
        layout.addWidget(x_text, 1, 1, 1, 1)
        layout.addWidget(x_slider, 1, 2, 1, 1)
        layout.addWidget(x_max_text, 1, 3, 1, 1)

        layout.addWidget(y_current_text, 2, 0, 1, 1)
        layout.addWidget(y_text, 2, 1, 1, 1)
        layout.addWidget(y_slider, 2, 2, 1, 1)
        layout.addWidget(y_max_text, 2, 3, 1, 1)

        layout.addWidget(z_current_text, 3, 0, 1, 1)
        layout.addWidget(z_text, 3, 1, 1, 1)
        layout.addWidget(z_slider, 3, 2, 1, 1)
        layout.addWidget(z_max_text, 3, 3, 1, 1)

        # layout.addWidget(show_3d_button, 4, 2, 1, 1)
        self.view3d_box.setLayout(layout)

        self.widgets["3d_slider"] = [x_slider, y_slider, z_slider,
                                     x_current_text, y_current_text, z_current_text]

    # 创建视角界面
    def create_view_button(self):
        self.view3d_angle = QGroupBox("视角")

        x_button = QPushButton()
        y_button = QPushButton()
        z_button = QPushButton()

        x_button.setText("X")
        y_button.setText("Y")
        z_button.setText("Z")

        x_button.clicked.connect(self.view_x_angle)
        y_button.clicked.connect(self.view_y_angle)
        z_button.clicked.connect(self.view_z_angle)

        layout = QGridLayout()
        layout.addWidget(x_button, 0, 0, 1, 1)
        layout.addWidget(y_button, 0, 1, 1, 1)
        layout.addWidget(z_button, 0, 2, 1, 1)

        self.view3d_angle.setLayout(layout)

    # 创建斜切的界面
    def create_plane_widget(self):
        self.plane_widget = QGroupBox("斜切")

        plane_button = QPushButton()
        plane_button.setText("提取斜面")
        plane_button.clicked.connect(self.get_plane_widget)

        reset_button = QPushButton()
        reset_button.setText("恢复")
        reset_button.clicked.connect(self.reset_button_click)

        choose_plane_button = QPushButton()
        choose_plane_button.setText("确定切取")
        choose_plane_button.clicked.connect(self.on_plane_widget_run)

        # 斜切滑块
        plane_slider = QSlider(Qt.Horizontal)
        plane_slider.valueChanged[int].connect(self.plane_slider_change)
        plane_slider.setPageStep(1)
        plane_slider.setValue(0)
        plane_slider.setMinimum(0)
        plane_slider.setMaximum(1500)

        plane_current_value = self.createText("0/1500", [10, 70, 12])

        layout = QGridLayout()
        layout.addWidget(plane_button, 0, 0, 1, 1)
        layout.addWidget(choose_plane_button, 0, 1, 1, 1)
        layout.addWidget(reset_button, 0, 2, 1, 1)

        layout.addWidget(plane_current_value, 1, 0, 1, 1)
        layout.addWidget(plane_slider, 1, 1, 1, 2)

        self.plane_widget.setLayout(layout)
        self.widgets["plane_widget"] = [plane_slider, plane_current_value]

    # 显示之前的picker
    def on_plane_widget_preview_show(self, obj, event):

        if self.preview == True:
            self.set_SampleRate(2)
            self.extractVOI.Update()

            # 1. 更新位置
            self.clickPos = self.iren.GetEventPosition()
            self.picker = self.iren.GetPicker()
            self.picker.Pick(self.clickPos[0], self.clickPos[1], 0, self.Render)
            self.point_position = self.picker.GetPickPosition()

            # 2. 设置位置以及渲染
            self.sphereSource.SetCenter(self.point_position[0], self.point_position[1],
                                        self.point_position[2])
            self.sphereSource.SetRadius(10)
            self.sphereSource.Update()
            self.sphereMapper.SetInputConnection(self.sphereSource.GetOutputPort())

            self.sphereActor.SetMapper(self.sphereMapper)
            self.sphereActor.GetProperty().SetColor(1, 0, 0)
            self.sphereActor.SetScale(1, 1, 1)

            # 3.设置相机的位置
            self.Render.GetActiveCamera().SetPosition(self.point_position[0],
                                                      self.point_position[1],
                                                      self.point_position[2])
            self.Render.ResetCamera()

            # # 4. 创建Plane
            self.plane_preview = vtk.vtkPlane()
            self.plane_preview.SetNormal(self.Render.GetActiveCamera().GetDirectionOfProjection())
            self.plane_preview.SetOrigin(self.point_position[0],
                                         self.point_position[1],
                                         self.point_position[2])

            # 4. 恢复数据
            self.mapper.SetInputConnection(self.extractVOI.GetOutputPort())
            self.actor.SetMapper(self.mapper)
            self.renWin.Render()

    # 斜切 滑块执行的函数
    def plane_slider_change(self, value):
        try:
            self.volumemapper.RemoveClippingPlane(self.planeNew)
        except:
            pass

      #  1.重采样
        self.set_SampleRate(2)
        self.extractVOI.Update()

        # 2.获取当前数值
        current_value = int(self.widgets["plane_widget"][1].text().split("/")[0])
        max_value = int(self.widgets["plane_widget"][1].text().split("/")[1])
        slider_text = str(value) + "/" + str(max_value)
        self.widgets["plane_widget"][1].setText(slider_text)

        # 3.设置平面位置
        if current_value < value:
            self.planeNew.Push(value - current_value)

        elif value < current_value:
            self.planeNew.Push(-(current_value - value))

        # print("xieqie")
        print(datetime.datetime.now())
        m_plane = vtk.vtkPlane()
        m_plane.SetOrigin(self.planeNew.GetOrigin())
        print("self/plane")
        #print(self.planeNew)
        m_plane.SetNormal(self.planeNew.GetNormal())
        print("m_plane")
        #print(m_plane)

        # self.cliper_preview = vtk.vtkClipVolume()
        # self.cliper_preview.SetInputConnection(self.extractVOI.GetOutputPort())
        # self.cliper_preview.SetClipFunction(self.planeNew)
        # self.cliper_preview.GenerateClippedOutputOff()
        # self.cliper_preview.Mixed3DCellGenerationOff()
        print(datetime.datetime.now())
        #self.mapper.SetInputConnection(self.cliper_preview.GetOutputPort())
        #self.volumemapper.SetInputConnection(self.extractVOI.GetOutputPort())
        self.plane=vtk.vtkPlane()

        # self.plane.SetNormal(0.808277, -0.0644682, 0.585263)
        # self.plane.SetOrigin(78.4028, -6.2, 56.7705 )
        self.volumemapper.AddClippingPlane(self.planeNew)
        # print("self.volume")
        # print(self.volumemapper)
        self.volume.SetMapper(self.volumemapper)
        self.volume.SetProperty(self.volumeProperty)
        self.Render.AddVolume(self.volume)

        # self.actor.SetMapper(self.mapper)
        print(datetime.datetime.now())




        self.renWin.Render()



        print(datetime.datetime.now())


    # 更新 滑块平面
    def update_plane(self, Plane: vtk.vtkPlane, diff):

        Origin = list(Plane.GetOrigin())
        for i in range(3):
            Origin[i] += diff * Plane.GetNormal()[i]

        Plane.SetOrigin(tuple(Origin))

        return Plane

    # 设置重采样频率，根据图片多少，进行重采样。图片越多。重采样越大
    def set_SampleRate(self, index):

        if self.size_list[5] < 200:
            self.SampleRate = [1, 1, 1]

        elif self.size_list[5] >= 200 and self.size_list[5] < 500:
            self.SampleRate = [1, 1, 1]

        elif self.size_list[5] >= 500 and self.size_list[5] < 800:
            self.SampleRate = [1, 1, 1]

        elif self.size_list[5] >= 800:
            self.SampleRate = [1, 1, 1]

        self.extractVOI.SetSampleRate(self.SampleRate[index], self.SampleRate[index], self.SampleRate[index])

    # 创建 斜切平面裁剪工具
    def get_plane_widget(self):

        if self.plane_widget_Flag == False:
            self.implicitPlaneWidget.SetInteractor(self.iren)
            self.implicitPlaneWidget.SetInputData(self.extractVOI.GetOutput())
            # self.implicitPlaneWidget.SetResolution(1)
            self.implicitPlaneWidget.GetPlaneProperty().SetColor(.9, .4, .4)
            # self.implicitPlaneWidget.GetHandleProperty().SetColor(0, .4, .7)
            # self.implicitPlaneWidget.GetHandleProperty().SetLineWidth(0.2)
            self.implicitPlaneWidget.GetPlaneProperty().SetOpacity(0)  # 透明度
            # self.implicitPlaneWidget.NormalToYAxisOn()
            # self.implicitPlaneWidget.SetRepresentationToSurface()
            self.implicitPlaneWidget.SetPlaceFactor(1.1)
            # self.implicitPlaneWidget.SetCenter(0,0,0)

            self.implicitPlaneWidget.NormalToZAxisOff()
            self.implicitPlaneWidget.SetHandleSize(0.01)
            self.implicitPlaneWidget.PlaceWidget()

            self.plane_widget_Flag = True
            # self.implicitPlaneWidget.AddObserver(vtkCommand.EndInteractionEvent, self.on_plane_widget_preview)
            self.implicitPlaneWidget.AddObserver(vtkCommand.EndInteractionEvent, self.on_get_planeWidget_preview)
            self.implicitPlaneWidget.On()
            self.renWin.Render()

    # 信号函数，鼠标交互
    def on_get_planeWidget_preview(self, obj, event):
        print("移动")
        self.on_plane_widget_run()
        self.implicitPlaneWidget.On()
        self.plane_slider_change(0)

    # 当pWidget控件改变时，触发函数
    def on_plane_widget_run(self):
        # 表示当pWidget控件改变时，触发函数
        self.planeNew = vtk.vtkPlane()
        self.implicitPlaneWidget.GetPlane(self.planeNew)

        self.plane_widget_Flag = False
        self.implicitPlaneWidget.Off()

        plane_origin = self.planeNew.GetOrigin()
        print("queding tiqu")
        print(self.planeNew)
        # 移动相机视角
        self.Render.GetActiveCamera().SetPosition(plane_origin)
        self.Render.ResetCamera()

    # 恢复三维
    def reset_button_click(self):
        print("恢复")
        #self.extractVOI.SetInputConnection(self.appendFilter.GetOutputPort())
        #self.extractVOI.Update()
        # self.mapper.SetInputConnection(self.extractVOI.GetOutputPort())
        # self.actor.SetMapper(self.mapper)
        # self.Render.AddActor(self.actor)
        # self.renWin.Render()
        #####
        # self.volumemapper.SetInputConnection(self.appendFilter.GetOutputPort())
        # self.volume.SetMapper(self.volumemapper)
        #
        # self.volume.SetProperty(self.volumeProperty)
        #
        # self.Render.AddVolume(self.volume)
        # self.iren.Render()
        #self.renWin.Render()
        #####
        self.volumemapper.SetInputConnection(self.appendFilter.GetOutputPort())
        self.volumemapper.RemoveAllClippingPlanes()
        #self.volumemapper.AddClippingPlane(self.planeNew)

        self.volume.SetMapper(self.volumemapper)

        self.volume.SetProperty(self.volumeProperty)

        self.Render.AddVolume(self.volume)
        self.iren.Render()

    # 翻转，查看 x 轴的面
    def view_x_angle(self):
        print("x 视角")
        self.Render.GetActiveCamera().SetPosition(1, 0, 0)
        self.Render.GetActiveCamera().SetViewUp(0.0, 1.0, 0.0)
        self.Render.GetActiveCamera().SetFocalPoint(-1, 0, 0)
        self.Render.ResetCamera()
        self.renWin.Render()

    # 翻转，查看 y 轴的面
    def view_y_angle(self):
        print("y 视角")
        self.Render.GetActiveCamera().SetPosition(0, 1, 0)
        self.Render.GetActiveCamera().SetViewUp(0.0, 0, 1)
        self.Render.GetActiveCamera().SetFocalPoint(0, -1, 0)
        self.Render.ResetCamera()
        self.renWin.Render()

    # 翻转，查看 z 轴的面
    def view_z_angle(self):
        print("z 视角")
        self.Render.GetActiveCamera().SetPosition(0, 0, 1)
        self.Render.GetActiveCamera().SetViewUp(1, 0, 0)
        self.Render.GetActiveCamera().SetFocalPoint(0, 0, -1)
        self.Render.ResetCamera()
        self.renWin.Render()

    # x 滑块滑动执行
    def x_3d_slider(self):
        # print(self.widgets["3d_slider"][0].value())
        current = str(self.widgets["3d_slider"][0].value())
        self.widgets["3d_slider"][3].setText(current)
        self.size_list[1] = int(current)
        self.update_reslice()
        # print(self.Render.GetActiveCamera())
        self.update()

    # y 滑块滑动执行
    def y_3d_slider(self):
        # print(self.widgets["3d_slider"][1].value())
        current = str(self.widgets["3d_slider"][1].value())
        self.widgets["3d_slider"][4].setText(current)
        self.size_list[3] = int(current)
        self.update_reslice()
        # print(self.Render.GetActiveCamera())
        self.update()

    # z 滑块滑动执行
    def z_3d_slider(self):
        # print(self.widgets["3d_slider"][2].value())
        current = str(self.widgets["3d_slider"][2].value())
        self.widgets["3d_slider"][5].setText(current)
        self.size_list[5] = int(current)
        self.update_reslice()
        # print(self.Render.GetActiveCamera())
        self.update()

    # 读取数据
    def read_data(self):
        print("file_path = ", self.file_path)

        # 读取数据
        self.Reader.SetDataScalarTypeToUnsignedChar()
        self.Reader.SetFileDimensionality(4)
        self.Reader.SetFilePrefix(self.file_path)
        self.Reader.SetFileNameSliceSpacing(1)
        self.Reader.SetFilePattern("%s%d.tiff")
        self.Reader.SetDataExtent(0, 1500, 0, 1500, 0, self.size_list[5])
        self.Reader.SetDataSpacing(0.325, 0.325, 1)
        self.Reader.Update()

        # 设置间隔
        changer = vtk.vtkImageChangeInformation()
        changer.SetInputData(self.Reader.GetOutput())
        changer.SetOutputSpacing(0.325, 0.325, 1)
        changer.Update()

        # 翻转Z轴
        # flip = vtk.vtkImageFlip()
        # flip.SetInputConnection(changer.GetOutputPort())
        # flip.SetFilteredAxis(1)
        # flip.Update()

        # 提取三色合并三色。返回合并的

        self.appendFilter = self.color_extract(changer)

        self.appendFilter.Update()

        # self.print_info(self.appendFilter)

    # 提取 红绿蓝三色，合成颜色
    def color_extract(self, data):
        # 提取红
        self.extractRedFilter = vtk.vtkImageExtractComponents()
        self.extractRedFilter.SetInputConnection(data.GetOutputPort())
        self.extractRedFilter.SetComponents(0)
        self.extractRedFilter.Update()

        # 提取绿
        self.extractGreenFilter = vtk.vtkImageExtractComponents()
        self.extractGreenFilter.SetInputConnection(data.GetOutputPort())
        self.extractGreenFilter.SetComponents(1)
        self.extractGreenFilter.Update()

        # 提取蓝
        self.extractBlueFilter = vtk.vtkImageExtractComponents()
        self.extractBlueFilter.SetInputConnection(data.GetOutputPort())
        self.extractBlueFilter.SetComponents(2)
        self.extractBlueFilter.Update()
        ###
        self.extractAlaFilter = vtk.vtkImageExtractComponents()
        self.extractAlaFilter.SetInputConnection(data.GetOutputPort())
        self.extractAlaFilter.SetComponents(3)
        self.extractAlaFilter.Update()

        # 合并三色
        new_data = vtk.vtkImageAppendComponents()
        new_data.SetInputConnection(0, self.extractRedFilter.GetOutputPort())
        new_data.AddInputConnection(0, self.extractGreenFilter.GetOutputPort())
        new_data.AddInputConnection(0, self.extractBlueFilter.GetOutputPort())
        new_data.AddInputConnection(0, self.extractAlaFilter.GetOutputPort())
        new_data.Update()

        return new_data

    # 设置 三维坐标轴
    def set_axes(self):
        self.axes_actor.SetPosition(0, 0, 0)
        self.axes_actor.SetTotalLength(30, 30, 30)
        self.axes_actor.SetShaftType(0)
        self.axes_actor.SetCylinderRadius(0.02)
        self.axes_widget = vtk.vtkOrientationMarkerWidget()
        self.axes_widget.SetOrientationMarker(self.axes_actor)
        self.axes_widget.SetInteractor(self.iren)
        self.axes_widget.InteractiveOff()
        self.axes_widget.On()
        self.axes_widget.InteractiveOn()
        self.setEnabled(True)

    # 读取图像数据
    def reslice_widget(self):

        self.extractVOI.SetInputConnection(self.appendFilter.GetOutputPort())
        self.extractVOI.SetVOI(self.size_list[0], self.size_list[1],
                               self.size_list[2], self.size_list[3],
                               self.size_list[4], self.size_list[5])

        self.extractVOI.Update()

    # 更新滑块，提取图像的像素 （卡在这里）
    def update_reslice(self):
        print("huadong")
        print(datetime.datetime.now())
        # self.extractVOI.SetVOI(self.size_list[0], self.size_list[1],
        #                        self.size_list[2], self.size_list[3],
        #                        self.size_list[4], self.size_list[5])
        self.volumemapper.SetCropping(1)
        self.volumemapper.SetCroppingRegionPlanes(self.size_list[0], self.size_list[1],
                               self.size_list[2], self.size_list[3],
                               self.size_list[4], self.size_list[5])
        self.volumemapper.SetCroppingRegionFlags(0x0002000)
        self.volume.SetMapper(self.volumemapper)

        self.volume.SetProperty(self.volumeProperty)

        self.Render.AddVolume(self.volume)

        # self.set_SampleRate(0)
        #self.extractVOI.Update()
        print(datetime.datetime.now())
        self.iren.Render()
        self.update()
        print(datetime.datetime.now())

    def update_reslice_color_append(self):
        print(datetime.time())
        self.extractVOI_red.SetInputConnection(self.extractRedFilter.GetOutputPort())
        self.extractVOI_red.SetVOI(self.size_list[0], self.size_list[1],
                                   self.size_list[2], self.size_list[3],
                                   self.size_list[4], self.size_list[5])
        self.extractVOI_red.Update()
        self.extractVOI_blue.SetInputConnection(self.extractBlueFilterFilter.GetOutputPort())
        self.extractBlueFilter.SetVOI(self.size_list[0], self.size_list[1],
                                      self.size_list[2], self.size_list[3],
                                      self.size_list[4], self.size_list[5])
        self.extractBlueFilterFilterFilter.Update()

        self.extractGreenFilterFilterFilter.SetVOI(self.size_list[0], self.size_list[1],
                                                   self.size_list[2], self.size_list[3],
                                                   self.size_list[4], self.size_list[5])
        self.extractGreenFilterFilterFilterFilter.Update()
        self.extractVOI = vtk.vtkImageAppendComponents()
        self.extractVOI.SetInputConnection(0, self.extractRedFilter.GetOutputPort())
        self.extractVOI.AddInputConnection(0, self.extractGreenFilter.GetOutputPort())
        self.extractVOI.AddInputConnection(0, self.extractBlueFilter.GetOutputPort())
        self.extractVOI.Update()
        print(datetime.time())

        # self.set_SampleRate(0)
        # self.extractVOI.Update()
        self.iren.Render()
        self.update()

    def set_volume_Property(self):
        self.volumeProperty.ShadeOff()
        self.volumeProperty.SetInterpolationTypeToLinear()
        self.volumeProperty.SetAmbient(0.4)
        self.volumeProperty.SetDiffuse(0.6)
        self.volumeProperty.SetSpecular(0.2)
        # self.volumeProperty.SetIndependentComponents(0)
        self.volumeProperty.IndependentComponentsOff()

        print(self.volumeProperty.GetIndependentComponents())

        # # 设置颜色
        # colorTransformFunction = vtk.vtkColorTransferFunction()
        # colorTransformFunction.AddRGBPoint(0.0, 0.0, 0.0, 0.0)
        # colorTransformFunction.AddRGBPoint(64.0, 0.0, 0.0, 0.0)
        # colorTransformFunction.AddRGBPoint(128.0, 1.0, 0.0, 0.0)
        # colorTransformFunction.AddRGBPoint(192.0, 1.0, 0.0, 0.0)
        # colorTransformFunction.AddRGBPoint(255.0, 1.0, 0.0, 0.0)
        # self.volumeProperty.SetColor(colorTransformFunction)
        #
        # # 设置不透明度
        # opacityTransform = vtk.vtkPiecewiseFunction()
        # opacityTransform.AddPoint(0, 0.0)
        # opacityTransform.AddPoint(20, 0.0)
        # opacityTransform.AddPoint(200, 1.0)
        # opacityTransform.AddPoint(300, 1.0)
        # self.volumeProperty.SetScalarOpacity(opacityTransform)
        #
        # # 设置梯度不透明
        # gradientTransform = vtk.vtkPiecewiseFunction()
        # gradientTransform.AddPoint(0, 0.0)
        # gradientTransform.AddPoint(20, 2.0)
        # gradientTransform.AddPoint(200, 0.1)
        # gradientTransform.AddPoint(300, 0.1)
        # self.volumeProperty.SetGradientOpacity(gradientTransform)

    # 启动初始渲染
    def start_render(self):
        self.volumemapper.SetInputConnection(self.appendFilter.GetOutputPort())

        self.volumemapper.SetInputConnection(self.extractVOI.GetOutputPort())
        self.volume.SetMapper(self.volumemapper)

        self.volume.SetProperty(self.volumeProperty)

        self.Render.AddVolume(self.volume)
        self.Render.SetBackground(0, 0, 0)

        # Camera
        self.Render.GetActiveCamera().SetPosition(0, 0, 0)
        self.Render.GetActiveCamera().SetFocalPoint(0, 1, 0)
        self.Render.GetActiveCamera().SetViewUp(1, 1, 0)
        self.Render.GetActiveCamera().Azimuth(90)
        self.Render.GetActiveCamera().Elevation(0)
        self.Render.GetActiveCamera().ComputeViewPlaneNormal()
        self.Render.ResetCamera()
        self.renWin.AddRenderer(self.Render)

        self.pick = vtk.vtkVolumePicker()
        self.iren.SetPicker(self.pick)
        self.iren.AddObserver(vtkCommand.RightButtonPressEvent, self.on_plane_widget_preview_show)
        self.iren.Initialize()
        self.renWin.Render()

    # 启动函数，启动初始化，执行界面绘制，读取数据，渲染，设置坐标轴
    def run(self):
        # 创建主界面控件
        print("1")
        print(datetime.datetime.now())
        self.create_main_widget()
        print("2")
        print(datetime.datetime.now())
        self.read_data()
        self.set_volume_Property()
        print("3")
        print(datetime.datetime.now())
        self.reslice_widget()
        print("run")
        print(datetime.datetime.now())
        print("5")
        self.start_render()
        print(datetime.datetime.now())
        print("6")
        self.set_axes()
        print(datetime.datetime.now())
        print("7")
        self.show()
        print(datetime.datetime.now())

    # 创建文字 label 通用函数
    def createText(self, str, sizeList):
        font = QFont()
        font.setPointSize(sizeList[0])
        text = QLineEdit()
        text.setEnabled(False)
        text.setStyleSheet('background:transparent;border-width:0;border-style:outset;')
        text.setText(str)
        text.setFont(font)
        text.setMaximumSize(sizeList[1], sizeList[2])

        return text

    # 打印 imagedata 属性
    def print_info(self, data):
        dims = data.GetOutput().GetDimensions()
        origin = data.GetOutput().GetOrigin()
        spaceing = data.GetOutput().GetSpacing()

        print("维数：", dims)
        print("原图像原点：", origin)
        print("原像素间隔：", spaceing)


if __name__ == '__main__':
    view_3d = View3D()
    view_3d.read_data()
    view_3d.set_axes()
    view_3d.reslice_widget()
    view_3d.start()
