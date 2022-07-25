import gc

import falsecolor.coloring as fc
import numpy as np
import os
from falsecolor.process import ViewImage
import h5py as h5
from skimage.measure import block_reduce
#Read data from Examples directory
import matplotlib.pyplot as plt
import matplotlib.image as mp
import gc
import time
import math
from multiprocessing import Process
import datetime
import scipy.signal as signal
import gpu
import cv2
import scipy.ndimage as nd
import multiprocessing
from multiprocessing import shared_memory
from concurrent.futures import ThreadPoolExecutor
from skimage.filters import (threshold_otsu, threshold_niblack,
                             threshold_sauvola)
import copy


import threading


def split(nuclei_numpy,cyto_numpy):

    # cytoplasm_background = fc.getBackgroundLevels(cyto_numpy[:,  j ],threshold=500)[1]
    # nuclear_background = fc.getBackgroundLevels(nuclei_numpy[:,j])[1]

    nuclei_32 = nuclei_numpy - 1
    #nuclei_32 = nuclei_32.astype(np.int32)
    #nuclei_8U = nuclei_numpy
    nuclei_max = np.max(nuclei_32)
    nuclei_min = np.min(nuclei_32)

    if nuclei_max==0:
        nuclei_max=1
    #nuclei_8U = cv2.convertScaleAbs(nuclei_8U, alpha=(255.0 / nuclei_max))


    retVal = cv2.threshold(nuclei_32, nuclei_min, nuclei_max, cv2.THRESH_OTSU)[0]
    # retVal=255-retVal

    #nuclear_background = 0.7 * (int(retVal * nuclei_max / 255))
    nuclear_background = 0.5 * retVal

    if nuclear_background <200:
        nuclear_background=200
        ###################
    cyto_8U = cyto_numpy
    cyto_max = np.max(cyto_8U)
    #cyto_8U = cv2.convertScaleAbs(cyto_8U, alpha=(255.0 / cyto_max))
    # print(nuclei[:,i])

    # print(nuclei_8U)

    retVal = cv2.threshold(cyto_8U, 0, 65536 ,cv2.THRESH_OTSU)[0]
    # retVal=255-retVal

    cyto_background = int(0.5 * retVal)
    if cyto_background<200:
        cyto_background=200


    #########################
    # print("qiege")
    # print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))##0.03
    # nuclear_map = fc.getIntensityMap_nuc_split(nuc_ds, tileSize=50, blockSize=5, bgThreshold=nuclear_background)
    # cytoplasm_map = fc.getIntensityMap_cyto(cyto_ds, tileSize=50, blockSize=5, bgThreshold=cyto_background)
    # print("cytoplasm_map.shape")
    # print(cytoplasm_map.shape)
    #
    # # print("qiege")
    # # print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))##0.03
    # # cv2.resize()
    #
    # C_nuc = fc.interpolateDS_1(nuclear_map, 0, tileSize=50, beta=0)
    # C_cyto = fc.interpolateDS_1(cytoplasm_map, 0, tileSize=5, beta=2.5)
    # print("C_cyto.shape")
    # print(C_cyto.shape)

    # print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
    # nuc_nobg = np.clip(nuclei_numpy[:,j]-0.5*nuclear_background, 0, 2**16)
    # nuclei_numpy[nuclei_numpy <= 0.5 * nuclear_background] = 0.5 * nuclear_background
    # nuc_nobg = nuclei_numpy - 0.5 * nuclear_background
    # cyto_numpy[cyto_numpy <= 0.7 * cyto_background] = 0.7 * cyto_background
    # cyto_nobg = cyto_numpy - 0.7 * cyto_background
    return nuclear_background,cyto_background


def fun(nuclei_name,cyto_name,start,end,leng):
    len=int(end-start)
    print(f'当前正在运行的进程是{os.getpid()}，它的主进程是{os.getppid()}')
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))

    settings_dict = fc.getColorSettings()
    nuclei_RGBsettings = settings_dict['nuclei']
    cyto_RGBsettings = settings_dict['cyto']
    nuclei_progress = shared_memory.SharedMemory(name=nuclei_name)
    nuclei_numpy = np.ndarray((1500,leng,1500), dtype=np.uint16, buffer=nuclei_progress.buf)
    cyto_progress = shared_memory.SharedMemory(name=cyto_name)
    cyto_numpy = np.ndarray((1500,leng,1500), dtype=np.uint16, buffer=cyto_progress.buf)
    jobs=[]
    pool = ThreadPoolExecutor(max_workers=60)
    #print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
    for j in range(start,end):
        numpy_split=nuclei_numpy[:,j][0:750,0:750]
        cyto_split = cyto_numpy[:, j][0:750, 0:750]
        nuclear_background_1,cyto_background_1=split(numpy_split,cyto_split)
        numpy_split=nuclei_numpy[:,j][0:750,750:1500]
        cyto_split = cyto_numpy[:, j][0:750, 750:1500]
        nuclear_background_2,cyto_background_2=split(numpy_split,cyto_split)
        numpy_split=nuclei_numpy[:,j][750:1500,0:750]
        cyto_split = cyto_numpy[:, j][750:1500, 0:750]
        nuclear_background_3,cyto_background_3=split(numpy_split,cyto_split)
        numpy_split=nuclei_numpy[:,j][750:1500,750:1500]
        cyto_split = cyto_numpy[:, j][750:1500, 750:1500]

        nuclear_background_4,cyto_background_4=split(numpy_split,cyto_split)
        nuclear_background_hstack_1=np.hstack((nuclear_background_1,nuclear_background_2))
        nuclear_background_hstack_2 = np.hstack((nuclear_background_3, nuclear_background_4))
        nuclear_background=np.vstack((nuclear_background_hstack_1,nuclear_background_hstack_2))


        cyto_background_hstack_1=np.hstack((cyto_background_1,cyto_background_2))
        cyto_background_hstack_2 = np.hstack((cyto_background_3, cyto_background_4))
        cyto_background=np.vstack((cyto_background_hstack_1,cyto_background_hstack_2))


        #nuclear_background_final=cv2.resize(nuclear_background,None,fx=750,fy=750,interpolation = cv2.INTER_NEAREST)

        nuclear_background_final = nd.interpolation.zoom(nuclear_background, 750, order=1, mode='constant')

        #cyto_background_final = cv2.resize(cyto_background, None, fx=750, fy=750,interpolation = cv2.INTER_NEAREST)
        cyto_background_final = nd.interpolation.zoom(cyto_background, 750, order=1,mode='constant')
        # print("cyto_background_final.type")
        # print(cyto_background_final.dtype)
        # print(cyto_background_final.shape)
        #cyto_background_final= cv2.resize(cyto_background, None, fx=750, fy=750, interpolation=cv2.INTER_LINEAR)

        nuc_ds = block_reduce(nuclei_numpy[:,j,:], block_size=(5, 5), func=np.mean)


        cyto_ds = block_reduce(cyto_numpy[:, j ,:], block_size=(5,5), func=np.mean)
        nuclear_background_midfit=np.average(nuclear_background)
        cyto_background_midfit= np.average(cyto_background)
        #print(j)
        #print(cyto_background_midfit)
        nuclear_map= fc.getIntensityMap_nuc_split(nuc_ds, tileSize=50 ,blockSize=5, bgThreshold=nuclear_background_midfit)
        cytoplasm_map = fc.getIntensityMap_cyto_split(cyto_ds, tileSize=50, blockSize=5, bgThreshold=cyto_background_midfit)
        print("cytoplasm_map")
        print(cytoplasm_map.shape)
        C_nuc = fc.interpolateDS_1(nuclear_map,0, tileSize=50,beta=1)
        C_cyto = fc.interpolateDS_1(cytoplasm_map, 0, tileSize=50,beta=1)


        #nuclei_numpy[nuclei_numpy <= 0.5 * nuclear_background] = 0.5 * nuclear_background

        nuc_nobg = nuclei_numpy[:, j] - 0.7*nuclear_background_final
        #nuc_nobg = fc.sharpenImage(nuc_nobg)
        #cyto_numpy[cyto_numpy <= 0.yto7 * cyto_background] = 0.7 * cyto_background
        cyto_numpy_1=cyto_numpy[:, j]-1
        cyto_numpy_1=cyto_numpy_1.astype(np.int32)

        cyto_nobg = cyto_numpy_1 - 0.5 * cyto_background_final
        cyto_numpy_1[cyto_numpy_1>0.7*cyto_background_final]=0
        cyto_numpy_1[cyto_numpy_1<100]=0

        cyto_nobg_for_soft =cyto_numpy_1



        # print("cyto_numpy_type")
        # print(cyto_numpy.dtype)
        # print(cyto_nobg)
        # print(cyto_numpy_1)
        # print("cyto_type")
        # print(cyto_nobg.dtype)
        nuc_nobg[nuc_nobg<0]=0
        cyto_nobg[cyto_nobg <0] =0
        cyto_nobg = cyto_nobg + cyto_nobg_for_soft * 0.1






        #(nuc_nobg, cyto_nobg, nuclei_RGBsettings, cyto_RGBsettings, C_cyto, C_nuc, j)
        level_virtualHE = fc.rapidFalseColor(nuc_nobg, cyto_nobg, nuclei_RGBsettings, cyto_RGBsettings,
                                             run_FlatField_cyto=True,
                                             run_FlatField_nuc=True, cyto_normfactor=C_cyto, nuc_normfactor=C_nuc)
        #plt.imsave("E:\\DATA\\DATA\\human_zang_nuc\\" + str(j) + ".tiff", nuc_nobg)

        plt.imsave("E:\\DATA\\DATA\\06270201\\" + str(j) + ".tiff", level_virtualHE)
        #fname = "f:\\数据\\20220412N肝01Z\\" + numstr + '.tif'

        #pool.submit(trhead_GPU,nuc_nobg, cyto_nobg, nuclei_RGBsettings, cyto_RGBsettings, C_cyto, C_nuc, j)
    # print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
    #pool.shutdown(wait=True)
    #print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
        #   trhead_GPU(nuc_nobg, cyto_nobg, nuclei_RGBsettings, cyto_RGBsettings, C_cyto, C_nuc, j)

        #nuc_nobg[nuc_nobg>60000]=0
        #cyto_nobg = np.clip(cyto_numpy[:,j]-0.7*cyto_background, 0, 2**16)

        ###0.07
        #print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))###0.07
        # p=threading.Thread(target=trhead_GPU,args=(nuc_nobg,cyto_nobg,nuclei_RGBsettings,cyto_RGBsettings,C_cyto,C_nuc,j))
        # jobs.append(p)
        # p.start()
        # level_virtualHE = fc.rapidFalseColor(nuc_nobg, cyto_nobg, nuclei_RGBsettings, cyto_RGBsettings,
        #                                      run_FlatField_cyto=True,
        #                                      run_FlatField_nuc=True, cyto_normfactor=C_cyto, nuc_normfactor=C_nuc)
        # plt.imsave("E:\\DATA\\DATA\\falsecolor_29\\" + str(j) + ".tiff", level_virtualHE)

    #
    #
    #     #print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
    #
    #
    #
    #
    #     #print(j + start)
    #     #print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))#0.08
    # for p in jobs:
    #     p.join()
def trhead_GPU(nuc_nobg,cyto_nobg,nuclei_RGBsettings,cyto_RGBsettings,C_cyto,C_nuc,j):

    level_virtualHE = fc.rapidFalseColor(nuc_nobg, cyto_nobg, nuclei_RGBsettings, cyto_RGBsettings,
                                         run_FlatField_cyto=True,
                                         run_FlatField_nuc=True, cyto_normfactor=C_cyto, nuc_normfactor=C_nuc)
    plt.imsave("E:\\DATA\\DATA\\human_shen_nuc\\" + str(j) + ".tiff", level_virtualHE)

def jiangzao(nuclei_name,cyto_name,mean_name,start,end,leng):
    d=[]
    nuclei_progress = shared_memory.SharedMemory(name=nuclei_name)
    nuclei_numpy = np.ndarray((1500, leng, 1500), dtype=np.uint16, buffer=nuclei_progress.buf)
    mean_progress = shared_memory.SharedMemory(name=mean_name)
    mean_numpy = np.ndarray((leng), dtype=np.float, buffer=mean_progress.buf)
    cyto_progress = shared_memory.SharedMemory(name=cyto_name)
    cyto_numpy = np.ndarray((1500, leng, 1500), dtype=np.uint16, buffer=cyto_progress.buf)
    for i in range(start,end):

        nuclei_jiangzao=nuclei_numpy[:,i]
        nuclei_jiangzao = fc.applyCLAHE(nuclei_jiangzao)
        window_size=25
        thresh_niblack = threshold_sauvola(nuclei_jiangzao, window_size=window_size, k=0.8)

        #nuclei_jiangzao=nuclei_jiangzao.astype(np.int32)
        #nuclei_8U = cv2.convertScaleAbs(nuclei_jiangzao, alpha=(255.0/nuclei_max))
        #print(nuclei[:,i])

        #print(nuclei_8U)

        #retVal= cv2.threshold(nuclei_jiangzao, nuclei_min, nuclei_max, cv2.THRESH_OTSU)[0]

        retVal=thresh_niblack
        #print(retVal)
        # retVal, a_img = cv2.threshold(nuclei_8U, 0, 255, cv2.THRESH_TRIANGLE)
        # print("retval_th")
        # print((retVal)*nuclei_max/255)
        retVal=0.1*retVal

        #io.imsave("E:\\数据\\数据\\falsecolor_jiangzao_mid_z\\" + str(i) + ".tiff", a_img)

        #nuclei_jiangzao[nuclei_jiangzao<=retVal]= 0
        #nuclei_jiangzao[nuclei_jiangzao ==retVal] = 0

        nuclei_jiangzao =nuclei_jiangzao-retVal
        nuclei_jiangzao[nuclei_jiangzao < 0] = 0########需要解决的问题
        nuclei_jiangzao = nuclei_jiangzao.astype(np.uint16)

        nuclei_numpy[:,i]=nuclei_jiangzao
        #io.imsave("E:\\DATA\\DATA\\falsecolor_jiangzao_mid_z\\" + str(i) + ".tiff", nuclei_numpy[:,i])
        #print(a)
        b=np.sum(nuclei_jiangzao>0)

        c=nuclei_jiangzao.sum()
        #print(c)
        if b==0:
            print("B")
        if c==0:
            print("c")

        c=c/b
        mean_numpy[i]=c
        if b==0:
            mean_numpy[i]=1




        cyto_numpy[:,i]=fc.sharpenImage(cyto_numpy[:,i])
        cyto_numpy[:,i]=fc.applyCLAHE(cyto_numpy[:,i])




def z_leveing(nuclei_name,cyto_name,mean_name,start,end,leng):
    nuclei_progress = shared_memory.SharedMemory(name=nuclei_name)
    nuclei_numpy = np.ndarray((1500, leng, 1500), dtype=np.uint16, buffer=nuclei_progress.buf)
    mean_progress = shared_memory.SharedMemory(name=mean_name)
    mean_numpy = np.ndarray((leng), dtype=np.float, buffer=mean_progress.buf)
    e=np.mean(mean_numpy)
    for i in range(start,end):


        f = math.log(e, mean_numpy[i])
        nuc_max=np.max(nuclei_numpy[:, i])
        nuc_power_max=np.max(nuc_max )**f

        if nuc_power_max>60000:
            f=math.log(60000,nuc_max)

        nuclei_numpy[:, i] = np.power(nuclei_numpy[:, i], f)
        #print(nuclei_numpy[:, i].shape)
        nuclei_numpy[:, i] = np.round(nuclei_numpy[:, i])


        #nuclei_numpy[:,i] = cv2.medianBlur(nuclei_numpy[:,i],3)
        #plt.imsave("E:\\DATA\\DATA\\falsecolor_jiangzao_mid_z\\" + str(i) + ".tiff", nuclei_numpy[:,i])

if __name__ == '__main__':
    range_start = 600
    range_end =700
    range_all=int(range_end-range_start)

    array_nuclei =[]*range_all
    array_cyo = []*range_all

    arrays = []*range_all
    cyto_otu=[]*range_all

    for number in range(range_start, range_end):
        numstr = str(number).zfill(4)
        print(numstr)
        #fname = "F:\\对准\\20211229_Z_TIFF\\" + 'z' + numstr + '.tif'
        #fname = "E:\\数据\\数据\\2021121917_z\\" + '2021121702c1219z01' + numstr + '.tif'
        #fname = "E:\\数据\\数据\\20211218_z\\" + 'C1-Reslice of Reslice of Composite' + numstr + '.tif'
        #fname = "E:\\数据\\数据\\2021121918_z\\" + '2021121701c1219z01-1' + numstr + '.tif'
        #fname = "E:\\DATA\\DATA\\20211228_Z_TIFF_2\\" + '202112280102z01-1' + numstr + '.tif'
        #fname = "F:\\20220106肺01\\1\\" + '202112280501z01-1' + numstr + '.tif'
        #fname = "F:\\20220106肺01\\2\\" + '202112280501z02-1' + numstr + '.tif'
        #fname = "C:\\数据\\2022040203N肝Z01\\" + numstr + '.tif'
        #fname = "C:\\数据\\2022040203N肝Z05\\" + numstr + '.tif'
        #fname = "C:\\数据\\2022040203N肝Z01\\" + numstr + '.tif'
        fname = "Z:\\刘俐玮\\小视场大厚度\\N腺Z_x_distance0.0z_distance1000.0.bintiff\\" + str(number) + '.tif'
        #fname = "Z:\\GJT_Processing data\\服务器F盘对准后的TIFF图片---后期可以删除\\数据\\2022040101N肺Z02\\" + numstr + '.tif'

        a = mp.imread(fname)

        a = a[200:1700, 200:1700]
        #a = fc.applyCLAHE(a)

        arrays.append(a)


        print(a.shape)
    cyto = np.array(arrays)
    print(cyto.shape)

    arrays_1 = (int(range_end-range_start))*[]
    for number in range(range_start, range_end):
        numstr = str(number).zfill(4)
        print(numstr)
        #fname ="F:\\对准\\20211229_H_TIFF\\" + "h" + numstr + '.tif'
        #fname = "E:\\数据\\数据\\2021121917_h\\" + '2021121702c1219h01' + numstr + '.tif'
        #fname = "E:\\数据\\数据\\20211218_h\\" + 'C1-Reslice of Reslice of Composite' + numstr + '.tif'
        #fname = "E:\\数据\\数据\\2021121918_h\\" + '2021121701c1219h01' + numstr + '.tif'
        #fname = "E:\\DATA\\DATA\\20211228_H_TIFF_2\\" + '202112280102z01-4' + numstr + '.tif'
        #fname = "F:\\20220106肺01\\2\\" + '202112280501z02-1' + numstr + '.tif'
        #fname = "F:\\20220106肺01\\1\\" + '202112280501z01-1' + numstr + '.tif'
        #fname = "c:\\数据\\2022040203N肝H01\\" +numstr + '.tif'
        fname = "c:\\数据\\2022040203N肝H05\\" + numstr + '.tif'
        #fname = "c:\\数据\\2022040202N肝H01\\" + numstr + '.tif'
        fname = "Z:\\刘俐玮\\小视场大厚度\\N腺H_x_distance0.0z_distance1000.0.bintiff\\" + str(number) + '.tif'
        #fname = "Z:\\GJT_Processing data\\服务器F盘对准后的TIFF图片---后期可以删除\\数据\\2022040101N肺H\\" + numstr + '.tif'



        a = mp.imread(fname)
        a = a[200:1700, 200:1700]




        print(a.shape)

        arrays_1.append(a)


    nuclei = np.array(arrays_1)
    # print(data_1)
    print(nuclei.shape)

    nuclei = np.swapaxes(nuclei, 0, 1)
    # cyto=cyto.reshape(2048,50,2060,)
    cyto = np.swapaxes(cyto, 0, 1)


    del arrays_1
    del arrays

    leng = (range_end - range_start)
    leng = int(leng)


    mean=np.zeros(leng, dtype = float)
    sharememory_nuclei= shared_memory.SharedMemory(create=True, size=nuclei.nbytes)
    sharememory_cyto = shared_memory.SharedMemory(create=True, size=cyto.nbytes)
    share_nuclei = np.ndarray(nuclei.shape, dtype=nuclei.dtype, buffer=sharememory_nuclei.buf)
    share_cyto = np.ndarray(cyto.shape, dtype=cyto.dtype, buffer=sharememory_cyto.buf)
    sharememory_mean = shared_memory.SharedMemory(create=True, size=mean.nbytes)
    share_mean = np.ndarray(mean.shape, dtype=mean.dtype, buffer=sharememory_mean.buf)

    share_nuclei[:] = nuclei[:]
    share_cyto[:] = cyto[:]
    share_mean[:]=mean[:]
    jobs=[]
    pool = multiprocessing.Pool()
    print("start jiangzao")
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
    del nuclei
    del cyto
    gc.collect()
    time.sleep(1)
    for i in range(20):




          pool.apply_async(jiangzao, (
          sharememory_nuclei.name, sharememory_cyto.name, sharememory_mean.name, i * 5, (i + 1) *5, leng,))
        # p = Process(target=jiangzao, args=(sharememory_nuclei.name,sharememory_cyto.name,sharememory_mean.name,i*40,(i+1)*40,leng))
        # p.start()
        # p.join()

    pool.close()
    pool.join()

    jobs=[]
    pool = multiprocessing.Pool()
    print("start z")
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
    for i in range(20):
        pool.apply_async(z_leveing, (sharememory_nuclei.name, sharememory_cyto.name,sharememory_mean.name, i *5, (i + 1) * 5, leng,))

    pool.close()
    pool.join()
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))




    print("start")
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
    #
    pool = multiprocessing.Pool()
    for i in range(20):

        #pool.apply_async(fun, (sharememory_nuclei.name,sharememory_cyto.name,i*5,(i+1)*5,leng,))
        p = Process(target=fun, args=(sharememory_nuclei.name,sharememory_cyto.name,i*5,(i+1)*5,leng))
        p.start()
        p.join()

    pool.close()
    pool.join()
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
#



#
    # for p in jobs:
    #     p.join()
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
    print("end")
    print("Sub-process(es) done.")
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
