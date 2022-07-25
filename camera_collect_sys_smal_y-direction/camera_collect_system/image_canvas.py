import threading

import matplotlib as mpl
import cv2
from matplotlib.figure import Figure
import datetime
from PyQt5.QtWidgets import QWidget, QGridLayout,QLabel
from PyQt5.QtGui import QImage,QPixmap
from PyQt5.Qt import *
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtCore
from concurrent.futures import ThreadPoolExecutor
import q
from scipy import io
import scipy
mpl.use('Qt5Agg')
import time
class MyMplCanvas(FigureCanvas):  # 画布基类
    """这是一个窗口部件，即QWidget（当然也是FigureCanvasAgg）"""

    def __init__(self,imagedata, parent=None, width=2, height=2, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # 每次plot()调用的时候，我们希望原来的坐标轴被清除(所以False)
        # self.axes.hold(False)
        # fig.clf()
        print("father")

        #self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        self.axes.set_xlabel('x')
        self.axes.set_ylabel('y')
        FigureCanvas.updateGeometry(self)
        self.imagedata_class=imagedata

    def compute_initial_figure(self):
        pass


class MyStaticMplCanvas(MyMplCanvas):#单个画布
	"""静态画布：一条正弦线"""
	def compute_initial_figure(self):

		self.axes.plot(self.imagedata_class)



class Image2D(QWidget):

    def __init__(self, parent=None, width=8, height=8, dpi=100):
        super().__init__()
        self.setParent(parent)
        plt.style.use('dark_background')
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        self.figure = FigureCanvas(self.fig)
        self.layout = QGridLayout(self)
        self.label = QLabel()
        self.label_1=QLabel()

        self.layout.addWidget(self.label,0,0,2,2,QtCore.Qt.AlignBottom)
        self.layout.addWidget(self.label_1,0,3,2,2,QtCore.Qt.AlignBottom)
        #self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.duibidu = 20
        self.max = 65536
        self.min = 0
        self.auto_min = 0
        self.auto_max = 0
        self.auto_Flag = False
        self.auto_Flag_press = False
        self.i=500
        self.j=0
        self.pool=self.pool = ThreadPoolExecutor(max_workers=10)
        # self.slider_min = QSlider(Qt.Horizontal)
        # self.slider_max = QSlider(Qt.Horizontal)
        # self.slider_min.setMinimum(10)
        # self.slider_min.setMaximum(65510)
        # self.slider_max.setMinimum(20)
        # self.slider_max.setMaximum(65536)
        # self.slider_min.setValue(10)
        # self.slider_max.setValue(65536)
        # self.slider_max.setSingleStep(20)
        # self.slider_min.setSingleStep(20)
        # self.slider_min.sliderMoved.connect(self.value_change_min)
        # self.slider_max.sliderMoved.connect(self.value_change_min)


        #self.x_show = MyStaticMplCanvas()
        #self.layout.addWidget(self.y_show, 0, 1, 2, 1)

        # self.label.setText("hhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
        # self.draw()
    def mubu(self):
        cv2.namedWindow('PCO', 0)
        cv2.resizeWindow('PCO', 400, 480)

    # def draw(self):
    #     self.imagedata = cv2.convertScaleAbs(self.imagedata, alpha=(self.duibidu * 255.0 / 65535.0))
    #     cv2.imshow('PCO', self.imagedata)
    #     cv2.waitKey(20)
    def thread_save_100(self):
        self.i=self.i+1

        #mpl.image.imsave("C:\\xiangji\\"+str(self.i)+'.tiff', self.imagedata)
        cv2.imwrite("C:\\xiangji\\"+str(self.i)+'.tiff', self.imagedata)
        #scipy.misc.imsave("C:\\xiangji\\"+str(self.i)+'.tiff', self.imagedata)
        pass

    def calcAndDrawHist(self,image, min, max):
        # if max-min<255:
        #     hist_size=10
        #     print(hist_size)
        # else:
        #     hist_size=255
        hist = cv2.calcHist([image], [0], None, [255], [min, max])
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(hist)
        # print(hist)

        histImg = np.zeros([500, 500, 3], np.uint8)
        hpt = int(0.9 * 500);

        for h in range(255):
            intensity = int(hist[h] * hpt / maxVal)
            cv2.line(histImg, (h, 500), (h, 500 - intensity), [255, 0, 0])
        image_change = image.flatten()

        font = cv2.FONT_HERSHEY_SIMPLEX
        text = str(max)
        text = "max:" + text
        cv2.putText(histImg, text, (300, 30), font, 1, (255, 255, 0), 2)
        text = str(min)
        text = "min:" + text
        cv2.putText(histImg, text, (300, 60), font, 1, (255, 255, 0), 2)
        text = str(np.argmax(np.bincount(image_change)))
        text = "mode:" + text
        cv2.putText(histImg, text, (300, 90), font, 1, (255, 255, 0), 2)

        return histImg;
    def show_histogram(self):
            try:
                # cv2.namedWindow('histImgB', 0)
                # cv2.resizeWindow('histImgB', 480, 480)

                self.hist = self.calcAndDrawHist(self.imagedata,np.min(self.imagedata),np.max(self.imagedata))
                # cv2.imshow("histImgB", hist)
                #
                # cv2.waitKey(10)
                # #print("直方图")
                #return hist


            except:
                print(np.shape(self.imagedata))



    def value_change_min(self):
        print("changevalue")
        self.min = self.slider_min.value()
        self.max = self.slider_max.value()
        print(self.min)
        print(self.max)
        self.auto_Flag=False
        # print("gaibianzhi ")
        # print(self.min)
        # print(self.max)
    def value_change_max(self):
        pass



    def draw(self):
        if q.start_save_buttom==1:

            if q.start_save_weiyitai==0:
                self.imagedata=self.imagedata[::4, ::4]


        self.auto_min = np.min(self.imagedata)
        self.auto_max = np.max(self.imagedata)
        # if int(abs(self.auto_max-self.i))>1:
        #
        #     self.slider_min.setMinimum(self.auto_min)
        #     self.slider_min.setMaximum(2*self.auto_max)
        #     self.slider_max.setMinimum(self.auto_min)
        #     self.slider_max.setMaximum(2*self.auto_max)
        #
        #
        #
        #
        #     self.i = self.auto_max
        #     self.j = self.auto_min
        #     if self.auto_max < 500:
        #         self.slider_min.setMaximum(1000)
        #         self.slider_max.setMaximum(1000)
        #         self.i=500
        #     #print("change")
        # else:
        #     self.slider_min.setMinimum(self.j)
        #     self.slider_min.setMaximum(2*self.i)
        #     self.slider_max.setMinimum(self.j)
        #     self.slider_max.setMaximum(2*self.i)
            #print("unchange")


        #print("draw")
        #t_start_show_histogram=threading.Thread(target=self.show_histogram,args=(self.imagedata,))
        #t_start_show_histogram.start()
        #print(time.asctime(time.localtime(time.time())))
        self.t=self.pool.submit(self.show_histogram)
        #t.start()
        self.t.result()
        #print(hist.dtype)
        #print(time.asctime(time.localtime(time.time())))
       # self.x_show = MyStaticMplCanvas()
        #print("self.auto_Flag = ", self.auto_Flag)

        if self.auto_Flag == True:
            self.min = self.auto_min
            self.max = self.auto_max
            # self.slider_min.setValue(self.min)
            # self.slider_max.setValue(self.max)


            #print("self.auto_min = ", self.auto_min)
            #print("self.auto_max = ", self.auto_max)

        #print(self.slider_min.value())
        #print(self.slider_max.value())



        self.imagedata[self.imagedata>self.max]=self.max
        self.imagedata[self.imagedata<self.min]=self.min
        #print("huatu")
        # if self.auto_Flag==True:
        #     print("self.auto_Flag")
        #     print(self.auto_Flag)
        try:
            if (self.max-self.min)==0:
                self.max=self.min+1


            self.imagedata = cv2.convertScaleAbs(self.imagedata, alpha=(255.0 / (self.max - self.min)),
                                             beta=-(255.0 / (self.max - self.min) * self.min))
            #print(hist.shape)

            # height, width,depth = self.hist.shape
            #
            # depth=width*depth
            # QImg = QImage(self.hist, width, height,depth ,QImage.Format_BGR888)
            # # QImg = QImage(self.imagedata.data, width, height, QImage.Format_Grayscale16*10)
            # size = QSize(200, 200)
            # pixmap_1 = QPixmap.fromImage(QImg.scaled(size, Qt.IgnoreAspectRatio))
            # #################
            # height, width = self.imagedata.shape
            # QImg = QImage(self.imagedata.data, width, height, QImage.Format_Grayscale8)
            # # QImg = QImage(self.imagedata.data, width, height, QImage.Format_Grayscale16*10)
            # size = QSize(800, 800)
            # pixmap = QPixmap.fromImage(QImg.scaled(size, Qt.IgnoreAspectRatio))
            # print(self.hist.dtype)
            # print(self.imagedata.dtype)
            # self.label.setPixmap(pixmap)
            # self.label.setCursor(Qt.CrossCursor)
            # self.label_1.setPixmap(pixmap_1)
            # self.label_1.setCursor(Qt.CrossCursor)
            # self.update()
        except:
            print("chuwenti")










