import numpy as np
import nidaqmx
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
from nidaqmx.constants import AcquisitionType, TaskMode
from scipy.interpolate import make_interp_spline
import scipy
import time
from PyQt5.QtCore import QTimer,QDateTime
import q


def smooth2nd(x,M): ##x 为一维数组
    K = round(M/2-0.1) ##M应
    # 为奇数，如果是偶数，则取大1的奇数
    lenX = len(x)
    if lenX<2*K+1:
        print('数据长度小于平滑点数')
    else:
        y = np.zeros(lenX)
        for NN in range(0,lenX,1):

            if NN<K+1 or lenX-NN<K+1:

                y[NN]=x[NN]
            else:

                startInd = NN-K
                endInd = NN+K
                y[NN] = np.mean(x[startInd:endInd])

##    y[0]=x[0]       #首部保持一致
##    y[-1]=x[-1]     #尾部也保持一致
    return(y)
class wave:
    def __init__(self):
        self.powerpercen405=0
        self.powerpercen488=0
        self.powerpercen561=0
        self.powerpercen637=0
        self.ligtopenbuttom405=0
        self.ligtopenbuttom488=0
        self.ligtopenbuttom561=0
        self.ligtopenbuttom637=0
        self.timer=QTimer()
        self.control_488_displacement_off_on=1########控制在移动的时候吧激光器给关掉
        self.control_637_displacement_off_on = 1  ########控制在移动的时候吧激光器给关掉

    def create(self):

        a=1
        self.samplerate=300000
        # freq = 12   #电压8.3

        # phase1 = int(10330)
        # phase2 = int(1000)
        amp = 0.09
        freq = 20
        pointnum=int(np.ceil(self.samplerate/freq))
        print(pointnum)

        #电压8.7
        phase1=7400              #坐标值
        phase2=1000             #坐标值
        periods=50
        duty=50

        duty=50
        #激振器波形
        w1=np.linspace(0,-amp,int(pointnum*duty/100/2))
        w2=np.linspace(-amp,amp,int(pointnum*(100-duty)/100))
        w3=np.linspace(amp,0,int(pointnum-len(w1)-len(w2)))
        out1=np.append(w1,w2)
        out1=np.append(out1,w3)
        # out1=smooth2nd(out1,3000)                              #激振器波形
        out1=np.array(out1)
        # plt.plot(y)
        # plt.plot(out1)
        # plt.show()
        #相机曝光同步
        plus1=np.ones(50)*5
        # expotimetime=2400  #20FPS设定相机曝光的时间。
        expotimetime = 4800
        expotime1=np.ones(expotimetime)

        a=1
        if a==1:
            plus2=np.zeros(50)
            expotime2=np.zeros(expotimetime)
        if a==2:
            plus2=np.ones(50)*5
            expotime2=np.ones(expotimetime)
        #脉冲触发信号

        if  phase2>phase1:
            zerors21=np.zeros(phase1)
            zerors22=np.zeros(phase2-phase1-50)
            zerors23=np.zeros(pointnum-phase2-50)
            out2=list(zerors21)+list(plus1)+list(zerors22)+list(plus2)+list(zerors23)   # phase1+plus2+phase2（将波形分为两段，各自一个phase）+plus2+尾巴
            out2=np.array(out2)
            zerose1= zerors21
            zerose2=np.zeros(phase2-phase1-expotimetime)
            zerose3=np.zeros(pointnum-phase2-expotimetime)
            exposyn=list(zerose1)+list(expotime1)+list(zerose2)+list(expotime2)+list(zerose3)
            print(len(exposyn))

        if  phase2<phase1:
            zerors21 = np.zeros(phase2)
            zerors22 = np.zeros(phase1 - phase2 - 50)
            zerors23 = np.zeros(pointnum - phase1 - 50)
            out2 = list(zerors21) + list(plus2) + list(zerors22) + list(plus1) + list(zerors23)
            zerose1= zerors21
            zerose2=np.zeros(phase1-phase2-expotimetime)
            zerose3=np.zeros(pointnum-phase1-expotimetime)
            exposyn=list(zerose1)+list(expotime2)+list(zerose2)+list(expotime1)+list(zerose3)
            out=np.array(out2)
            exposyn=np.array(exposyn)  #光源同步相机信号
        ###激光器波形 脉冲+常量
        o31=np.ones(2)
        o32=np.ones(4)*5
        o33=np.append(o31,o32)
        o33=np.append(o33,o31)
        # 300000

        lightpls=np.tile(o33, int(pointnum/8))                 #脉冲 数字信号，四通道共用
        out3=exposyn*5
        out3=np.ones(pointnum)*5
        exposyn=out3
        power405=exposyn*self.ligtopenbuttom405*self.powerpercen405/100*5
        power488=exposyn*self.ligtopenbuttom488*self.powerpercen488*self.control_488_displacement_off_on/100*5
        power561=exposyn*self.ligtopenbuttom561*self.powerpercen561/100*5
        power637=exposyn*self.ligtopenbuttom637*self.powerpercen637*self.control_637_displacement_off_on/100*5                  #模拟信号，控制功率大小


        print(len(out1))
        print(len(out2))
        print(len(out3))
        print(len(exposyn))
        print("power488")
        print(power637)
        p1 = np.ones(100) * 5
        p2 = np.ones(100) * 0
        out2 = np.append(p2, p1)
        out2 = np.append(out2, p1)
        out2 = np.tile(out2, 50)
        print(len(out2))


        ##相机脉冲相位设定光源
        #phase1 phase1





        #out1,out2,out3, power405, power488,power561,power637
        #out1  激振器波形
        #out2  相机同步
        #out3  光源数字信号


        plus405=out3*self.ligtopenbuttom405
        plus488=out3*self.ligtopenbuttom488
        plus561=out3*self.ligtopenbuttom561
        plus637=out3*self.ligtopenbuttom637




        c =np.vstack((out1,out2,out3,power405,power488,power561,power637))
        return c


    def sent_wave(self):
        attay_vstack=self.create()

        with nidaqmx.Task() as task:
            task.ao_channels.add_ao_voltage_chan('Dev1/ao0:6')
            task.timing.cfg_samp_clk_timing(self.samplerate,sample_mode=AcquisitionType.CONTINUOUS)
            print('Generation is started')
            task.write(attay_vstack)
            task.control(TaskMode.TASK_COMMIT)
            task.start()


            while True:
            # for i in range(5):
                #print("generating")
                #self.timer.start(10)
                time.sleep(1)
                if q.wave_flag==0:
                    q.wave_flag=1
                    print("ni办卡进程结束")
                    break

