import numpy as np
import pco
#from pco import Camera
from pco.sdk import sdk
from pco.recorder import recorder as rec
from PyQt5.QtCore import *
from PyQt5.QtCore import QThread, pyqtSignal
from pyvcam import pvc
#from camera import Camera
import matplotlib.pyplot as plt
import time
import datetime
import threading
import cv2
import q
import cv2
from pyvcam import pvc
from camera import Camera
from pyvcam import pvc
import os
#from wave import Wave
#from pyvcam.camera import Camera


start_save_buttom = 0
AAA=0

class PCO_Control(Camera):

    def __init__(self):
        #super().__init__()
        self.start_flag = False
        self.delay_time = 0
        self.pixel_rate = 272250000
        self.dwline_time = 0.0000585
        self.exposure_line = 100
        self.delay_line = 12
        self.exposure_time = (self.dwline_time * self.exposure_line) + self.delay_line
        self.i = 0
        self.bbb = None
        self.AAA=0


    def save_pic(self, n):
        self.run_wait_image()
        print(time.asctime(time.localtime(time.time())))
        self.image(n,bbb=self.bbb)

    def plot_picture(self):
        #f = open("C:\\test\\filename1.bin", 'ab')
        #self.timer = QTimer()



        #print("kazhuke ")
        #print("kazhuke ")
        #while True:
        frame, fps, frame_count = self.cam.poll_frame_1(oldestFrame=False,copyData=False)
            #print("start pco control xunhuan")
            # if frame_count!=self.AAA:
            #     break
        #print(plot_roi)
        #time.sleep(0.05)
        #print('zhaopian')
        #print(time.asctime(time.localtime(time.time())))

        #frame, fps, frame_count = self.cam.poll_frame_1(oldestFrame=False)
        self.AAA=frame_count
        # print(fps)
        print(self.AAA)
        self.np_image = frame['pixel_data']
        # print("fps ")
        # print(fps)
        #print("Camera Data = ", self.np_image)
        #print("start_save_buttom",q.start_save_buttom)
        #print("start_save_weiytai",q.start_save_weiyitai)
        #print(self.np_image)
        #self.timer.start(100)
        #print("11111")
        # if q.start_save_buttom==1:
        #
        #     if q.start_save_weiyitai==0:
        #             #print("start_save_buttom",q.start_save_buttom)
        #             #q.i = q.i + 1
        #             #print(q.i)
        #             print('cunxhu')
        #             print(time.asctime(time.localtime(time.time())))
        #
        #             self.np_image.tofile(q.f)
        #
        #
        # if q.start_save_buttom == 1:
        #     if q.start_save_weiyitai==1:
        #         q.f.close()
        #         print("结束")
        #         q.start_save_buttom = 0
        #         q.start_save_weiyitai = 0
        #         q.i = q.i + 1
        #         q.f = open("C:\\TEST\\" + str(q.filename) + "_" + str(q.i) + ".bin", 'ab')


                #self.widgets["start_button"][1].setText("采集数据")
    # def wave(self):
    #     self.wave = Wave()
    #
    #     self.wave.sent_wave()


    def start_pco(self):
        # t=threading.Thread(target=self.wave)
        # t.start()


        pvc.init_pvcam()
        self.cam = next(Camera.detect_camera())
        self.cam.open()
        self.cam.clear_mode = 0
        self.cam.exp_mode = "Edge Trigger"
        # self.cam.exp_out_mode = 'Line Output'
        self.cam.exp_out_mode = 'First Row'
        # self.cam.set_roi(576, 576, 2048, 2048)
        self.cam.set_roi(576, 1500, 2048, 180)
        # cam.prog_scan_mode= "Scan Width"
        # cam.prog_scan_width=100
        self.cam._update_mode()
        self.cam.readout_port = 2
        self.cam.speed_table_index = 0
        # self.cam.prog_scan_mode = "Scan Width"
        # self.cam.prog_scan_width =100
        self.cam.exp_out_mode = 'First Row'
        print("exposure out mode: {}".format(self.cam.exp_out_modes[self.cam.exp_out_mode]))

        # cam.exp_out_mode = "First Row"
        self.cam.exp_res=0
        # self.cam.start_live(exp_time=4241, buffer_frame_count=200)

        # self.cam.start_live(exp_time=580, buffer_frame_count=100)#20FPS
        self.cam.start_live(exp_time=800, buffer_frame_count=100)#12FPS
        # self.cam.start_live(exp_time=846, buffer_frame_count=100)#10FPS
    def stop_pco(self):
        print("关闭相机")
        self.cam.finish()
        self.cam.close()
        pvc.uninit_pvcam()
        print('jieshu')




    def run_save_thread(self):
        print("开始保存线程")
        t_save = threading.Thread(target=self.save_pic, args=(1000,))  ####数字代表的意思是开始存储多少张照片
        t_save.start()
        print('chuchu')
        t_save.join()

    def run_wait_image(self):
        self.wait_for_first_image()


    def start_plot_thread(self):
        self.plot_picture()######确认一下是否正确
        # self.t_plot = threading.Thread(target=self.plot_picture)
        # self.t_plot.start()
        # #print("huatu")
        # self.t_plot.join()


    # def plot_picture(self):
    #     b = np.fromfile("./data/filename27.bin", dtype=np.uint16)
    #     c = np.fromfile("./data/filename52.bin", dtype=np.uint16)
    #     b = b.reshape(2048,2060)
    #     c = c.reshape(2048,2060)
    #
    #     if self.i % 2 ==0:
    #         self.np_image = b
    #     else:
    #         self.np_image = c
    #
    #     self.i+=1
