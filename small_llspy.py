
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import gc
import time
import os
import cv2
from datetime import datetime

#import  llspy
import numpy as np
import multiprocessing
from multiprocessing import shared_memory
from multiprocessing import Process
import matplotlib.pyplot as plt
import os
from skimage import io

def change(start,end,sharememory_array_data_name,sharememory_final_array_data_name,leng):
    sharememory_array_data = shared_memory.SharedMemory(name=sharememory_array_data_name)
    array_data = np.ndarray((int(leng), 180, 2048), dtype=np.uint16, buffer=sharememory_array_data.buf)
    sharememory_final_array_data = shared_memory.SharedMemory(name=sharememory_final_array_data_name)
    final_array_data = np.ndarray((int(leng+26), 180, 2896), dtype=np.uint16, buffer=sharememory_final_array_data.buf)
    array_for_interpolation = np.ones((int((leng) * 6.8) + 180, 2896), dtype=np.uint16, order='C')
    array_ones_2048 = np.ones((180, 2896), dtype=np.uint16)
    for i in range(start,end):
       # print(i)
        #print(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])

        #print(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
        cc=cv2.resize(array_data[:,i,:],None,fx=1.414,fy=6.8, interpolation=cv2.INTER_LINEAR)
       # print(cc.shape)
        #cc=np.ascontiguousarray(cc)
        #print(cc.dtype)
        #print(cc.shape)
        #cc=np.array(cc)
        #print(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
        array_for_interpolation[i:i+int(leng*6.8),:]=cc
        #print(array_for_interpolation.shape)
        #print(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
        ggg=cv2.resize(array_for_interpolation,None,fx=1,fy=1/6.8,interpolation=cv2.INTER_LINEAR)
       # print(ggg.shape)
        #print(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
        final_array_data[:,i,:]=ggg
        array_for_interpolation[0:180,:]=array_ones_2048
        #print(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    import os

    path = "Z:\\蔡小静\\前列腺\\全\\data_h_3\\"  # 文件夹目录

    files = os.listdir(path)  # 得到文件夹下的所有文件名称
    print(files[1])
    binry_data = np.fromfile(path + str(files[1]), dtype=np.uint16)
    array_length = len(binry_data) / 180 / 2048
    final_array_data = np.ones((int(array_length) + 27, 180, 2896), dtype=np.uint16)
    sharememory_final_array_data = shared_memory.SharedMemory(create=True, size=final_array_data.nbytes)
    array_data = binry_data.reshape(int(array_length), 180, 2048)

    array_data = array_data[0:(int(array_length)), :, :]
    sharememory_array_data = shared_memory.SharedMemory(create=True, size=array_data.nbytes)
    share_final_array_data = np.ndarray(final_array_data.shape, dtype=final_array_data.dtype,
                                        buffer=sharememory_final_array_data.buf)
    share_array_data = np.ndarray(array_data.shape, dtype=array_data.dtype, buffer=sharememory_array_data.buf)
    share_final_array_data[:] = final_array_data[:]
    #array_data = binry_data.reshape(int(array_length),180, 2048)
    s = []
    for file in files:  # 遍历文件夹
        if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
            print(file)
            #file="N肝Z_x_distance5680.0z_distance754.0.bin"
            binry_data = np.fromfile(path+str(file), dtype=np.uint16)
            array_length=len(binry_data )/180/2048
            print(array_length)

            array_data = binry_data.reshape(int(array_length), 180, 2048)
            array_length = array_length
            array_data =array_data[0:(int(array_length)),:,:]
            print(array_data[:,100,:].shape)
            # plt.imshow(array_data[1,:,:])
            # plt.show()
           # del binry_data
            #c=c[0:400,:,:]
            #d=np.zeros((1208,2048,2048))
            # for i in range(0,400):
            #     d[399-i,:,:]=c[i,:,:]
            # dd=500
            # g=llspy.deskew(d)
            # print(g.shape)

            #print(g.shape)



            #print(g[0,:,100].shape)
            a=0
            d=2048/2048
            print(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
            array_for_interpolation = np.ones((int(array_length * 6.8) + 180, 2896), dtype=np.uint16, order='C')
            array_ones_2048=np.ones((180,2896),dtype=np.uint16)




            #


            share_array_data[:] = array_data[:]
            # del final_array_data
            # del array_data
            gc.collect()
            pool = multiprocessing.Pool(5)
            print(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
            for i in range(0,5):
                    # p = Process(target=change, args=(i* 36, (i + 1) * 36,sharememory_array_data.name,sharememory_final_array_data.name,array_length))
                    # p.start()
                    # p.join()
                    pool.apply_async(change, (i * 36, (i + 1) * 36,sharememory_array_data.name,sharememory_final_array_data.name,array_length,))
            pool.close()
            pool.join()
            #change(0,2048,array_data,array_for_interpolation,final_array_data,array_ones_2048)
            print(time.time())
            print(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
            #f = open("Z:\\顾江涛\\small拼接测试"+"矫正"+str(file), 'wb+')
            os.mkdir("Z:\\蔡小静\\前列腺\\全\\data_h_3\\"+str(file)+"tiff")
            #g=llspy.deskew(c)
            for i in range(0,180):
                io.imsave("Z:\\蔡小静\\前列腺\\全\\data_h_3\\"+str(file)+"tiff\\" + str(i)+".tif", share_final_array_data[:,i,:])
            print(share_final_array_data.shape)
            #f.close()
            #del final_array_data
            #del array_data
            # sharememory_array_data.close()
            # sharememory_final_array_data.close()
            # sharememory_array_data.unlink()
            # sharememory_final_array_data.unlink()
            # del share_array_data
            # del share_final_array_data
            # gc.collect()

    #g=np.swapaxes(g,1,2)


    #print(c[100,:,:])
