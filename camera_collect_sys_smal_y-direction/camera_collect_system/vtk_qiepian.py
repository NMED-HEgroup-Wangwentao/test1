#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import vtk
reader = vtk.vtkMetaImageReader()     # 读取三维图像
reader.SetFileName("C://data//111.mha")
reader.Update()

extent = reader.GetOutput().GetExtent()  # 获取图像范围
spacing = reader.GetOutput().GetSpacing()    # 像素间隔
origin = reader.GetOutput().GetOrigin()   # 原点

center1 = origin[0] + spacing[0] * 0.5 *(extent[0] + extent[1])
center2 = origin[1] + spacing[1] * 0.5 *(extent[2] + extent[3])
center3 = origin[2] + spacing[2] * 0.5 *(extent[4] + extent[5])
# 切片的变换矩阵，钱三列表示XYZ方向矢量，第四列为切面坐标系原点。
axialElements = [1, 0, 0, 0,
                 0, 1, 0, 0,
                 0, 0, 1, 0,
                 0, 0, 0, 1]    # 表示切面坐标系与图像坐标系一致，且经过图像中心点center

'''coronalElements = [1, 0, 0, 0,
                   0, 0, 1, 0,
                   0, -1, 0, 0,
                   0, 0, 0, 1]     # 提取平行于XZ平面的切片

sagittalElements = [0, 0, -1, 0,
                    1, 0, 0, 0,
                    0, -1, 0, 0,
                    0, 0, 0, 1]     # 提取平行于YZ平面的切片

obliqueElements = [1, 0, 0, 0,
                   0, 0.866025, -0.5, 0,
                   0, 0.5, 0.866025, 0,
                   0, 0, 0, 1]      # 提取斜切切片
 注意使用这些变换矩阵时，需要将第四列替换为切片经过图像的一个点坐标
'''

resliceAxes = vtk.vtkMatrix4x4()
resliceAxes.DeepCopy(axialElements)
resliceAxes.SetElement(0, 3, center1*2)
resliceAxes.SetElement(1, 3, center2)
resliceAxes.SetElement(2, 3, center3*1.5)
print(center1)
print(center2)
print(center3)

reslice = vtk.vtkImageReslice()      # 图像切面的提取
reslice.SetInputConnection(reader.GetOutputPort())
reslice.SetOutputDimensionality(3)    # 指定输出的图像为一个二维图像
reslice.SetResliceAxes(resliceAxes)    # 设置变换矩阵
reslice.SetInterpolationModeToLinear()   # 线性插值

'''
reslice.SetInterpolationModeToNearestNeighbor()  最近邻插值
reslice.SetInterpolationModeToCubic()    三次线性插值
'''
colorTable = vtk.vtkLookupTable()
colorTable.SetRange(0, 1000)
colorTable.SetValueRange(0.0, 1.0)
colorTable.SetSaturationRange(0.0, 0.0)
colorTable.SetRampToLinear()
colorTable.Build()

colorMap = vtk.vtkImageMapToColors()
colorMap.SetLookupTable(colorTable)
colorMap.SetInputConnection(reslice.GetOutputPort())
colorMap.Update()   # 新版vtk需要添加

imageActor = vtk.vtkImageActor()
imageActor.SetInputData(colorMap.GetOutput())

renderer = vtk.vtkRenderer()
renderer.AddActor(imageActor)
renderer.SetBackground(1.0, 1.0, 1.0)

renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)
renderWindow.Render()
renderWindow.SetSize(640, 480)
renderWindow.SetWindowName('ImageResliceExample')

renderWindowInteractor = vtk.vtkRenderWindowInteractor()
style = vtk.vtkInteractorStyleImage()
renderWindowInteractor.SetInteractorStyle(style)
renderWindowInteractor.SetRenderWindow(renderWindow)
renderWindowInteractor.Initialize()
renderWindowInteractor.Start()

