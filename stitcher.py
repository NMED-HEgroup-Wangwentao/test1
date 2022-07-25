import numpy as np
import matplotlib.pyplot as plt
import cv2
import copy
import datetime
from skimage import io
import multiprocessing
from multiprocessing import Process


def calWeight(d, k):
    '''
    :param d: 融合重叠部分直径
    :param k: 融合计算权重参数
    :return:
    '''

    x = np.arange(-d / 2, d / 2)
    y = 1 / (1 + np.exp(-k * x))
    return y
def jisuan_chazhi(img_src,img_src_1,right_bottom_on,i):
    img_src = img_src.astype(np.float32)
    # img_src_1 = cv2.convertScaleAbs(img_src_1, alpha=(255.0 / (max_img_src - min_img_src)),
    # beta=-(255.0 / (max_img_src - min_img_src) * min_img_src))
    img_src_1 = img_src_1.astype(np.float32)
    # print(img_src.shape)

    img_templ = img_src[10:2000, 1800:2000].copy()
    b = np.max(img_templ)
    img_src_1 = img_src_1[0:2048, 0:500]
    img_src_1 = img_src_1 * b / np.max(img_src_1)
    # img_templ = img_src_1[195:795,22:162].copy()
    # if b<300:
    #     right_bottom=right_bottom_on[i]
    #else:

        # print('img_src.shape:',img_src.shape)
        # print('img_templ.shape:',img_templ.shape)

        # 模板匹配
    result = cv2.matchTemplate(img_src_1, img_templ, 0)

        # 计算匹配位置
    min_max = cv2.minMaxLoc(result)


    match_loc = min_max[2]

        # 注意计算右下角坐标时x坐标要加模板图像shape[1]表示的宽度，y坐标加高度
    right_bottom = (match_loc[0] + img_templ.shape[1], match_loc[1] + img_templ.shape[0])
    #if abs(right_bottom[0])-
    if right_bottom[0]<320:
        right_bottom=right_bottom_on[i]
    if right_bottom[0]>350:
        right_bottom=right_bottom_on[i]
    #print(right_bottom)


    return  right_bottom
def roll_for_photo(img_save_1,data_for_roll_updown):
    r = np.roll(img_save_1, int(data_for_roll_updown), axis=0)
    if int(data_for_roll_updown) < 0:
        r_roll_vstack = np.zeros((abs(int(data_for_roll_updown)), 2048))
        #print(r_roll_vstack.shape)
        r[2048 - abs(int(data_for_roll_updown)):2048, :] = r_roll_vstack
    if int(data_for_roll_updown) > 0:
        r_roll_vstack = np.zeros((abs(int(data_for_roll_updown)), 2048))
        #print(r_roll_vstack.shape)
        r[0:int(data_for_roll_updown), :] = r_roll_vstack
    return r
def find_best_num(num_for_len):
    right_bottom_x=[]
    right_bottom_y=[]
    num_for_len_1 = num_for_len + 350
    for i in range(0,800,10):
        numstr = str(i).zfill(4)
        a='041801Z'+str(num_for_len)
        print(a)
        img_src = cv2.imread('f:\\stitcher_by_self_data\\'+a+'\\'+ numstr + '.tif', -1)
        img_src = img_src.astype(np.float32)
        img_templ = img_src[10:2000, 1800:2000].copy()
        if np.mean(img_templ)>400:

            b='041801Z'+str(num_for_len_1)

            img_src_1 = cv2.imread('f:\\stitcher_by_self_data\\'+b+'\\'+ numstr + '.tif', -1)
            b = np.max(img_templ)
            img_src_1 = img_src_1[0:2048, 0:500]
            img_src_1 = img_src_1 * b / np.max(img_src_1)
            result = cv2.matchTemplate(img_src_1, img_templ, 0)

            # 计算匹配位置
            min_max = cv2.minMaxLoc(result)

            match_loc = min_max[2]

            # 注意计算右下角坐标时x坐标要加模板图像shape[1]表示的宽度，y坐标加高度
            right_bottom = (match_loc[0] + img_templ.shape[1], match_loc[1] + img_templ.shape[0])
            right_bottom_x.append(right_bottom[0])
            right_bottom_y.append(right_bottom[1])
            print(len(right_bottom_x))
            if len(right_bottom_x)==20:
                break
                #pass
        print(i)
    print(len(right_bottom_x))
    num_x=int(sum(right_bottom_x)/(len(right_bottom_x)))
    num_y=int(sum(right_bottom_y)/(len(right_bottom_y)))
    return num_x,num_y



def start_ststcher_right_bottom(start,end):
    right_bottom_on=[(333,1990),(333,1990),(333,1990),(333,1990)]

    for i in range(start,end):
        a=[]
        right_bottom_x_array=[]
        right_bottom_y_array=[]
        numstr = str(i).zfill(4)
        #读入图像，截图部分作为模板图片
        img_src = cv2.imread('f:\\stitcher_by_self_data\\041801Z650\\'+numstr+'.tif',-1)
        a.append(img_src)
        img_src_1 = cv2.imread('f:\\stitcher_by_self_data\\041801Z1000\\'+numstr+'.tif',-1)
        a.append(img_src_1)

        img_src_2 = cv2.imread('f:\\stitcher_by_self_data\\041801Z1350\\'+numstr+'.tif',-1)

        a.append(img_src_2)
        img_src_3 = cv2.imread('f:\\stitcher_by_self_data\\041801Z1700\\'+numstr+'.tif',-1)
        a.append(img_src_3)

        img_src_4 = cv2.imread('f:\\stitcher_by_self_data\\041801Z2050\\'+numstr+'.tif',-1)
        a.append(img_src_4)
        #print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
        photo_np_array=np.array(a)
        #print()
        #plt.imshow(photo_np_array[2,:])
        #plt.show()
        img_save=copy.deepcopy(photo_np_array[0,:])

        for i in range(0,4):
            right_bottom_1=jisuan_chazhi(photo_np_array[i,:],photo_np_array[i+1,:],right_bottom_on,i)

            #right_bottom_x_1,right_bottom_y_1=jisuan_chazhi(photo_np_array[1,:],photo_np_array[2,:])
            right_bottom_on[i]=right_bottom_1
            right_bottom_x_array.append(right_bottom_1[0])
            right_bottom_y_array.append(right_bottom_1[1])
        right_bottom_x_array=np.array(right_bottom_x_array)
        right_bottom_y_array=np.array(right_bottom_y_array)

        data_for_roll_updown_array=[]
        for i in range(0,4):


            data_for_roll_updown=2000-right_bottom_y_array[i]
        #data_for_roll_updown_1=1400-right_bottom_y_1
            data_for_roll_updown_array.append(data_for_roll_updown)
            # img_src = cv2.imread('f:\\stitcher_by_self_data\\041801H650\\0100.tif', -1)
            # img_src_1 = cv2.imread('f:\\stitcher_by_self_data\\041801H1000\\0100.tif', -1)
        data_for_roll_updown_array=np.array(data_for_roll_updown_array)

        # r=r[:,(right_bottom_x+48):2048]
        #     #plt.imshow(r)
        #     # plt.show()
        # img=cv2.hconcat([img_save, r])
        d=0
        img_save_array=[]
        for i in range(1,5):
            d=d+data_for_roll_updown_array[i-1]
            photo_np_array[i,:]=roll_for_photo(photo_np_array[i,:],d)
            #img_save_2=roll_for_photo(img_save_2,data_for_roll_updown_array[0]+data_for_roll_updown_array[1])
            #img_save_array.append(img_save_1)
        #img_save_array=np.array(img_save_array)
        overlap_array=[]
        w_array=[]
        for i in range(0,4):

            overlap=right_bottom_x_array[i]+48
            w = calWeight(overlap, 0.05)
            #print(w.shape)
            #w_1 = calWeight(overlap_1, 0.05)
            overlap_array.append(overlap)
            w_array.append(w)

        overlap_array=np.array(overlap_array)
        #w_array=np.array(w_array)


        col, row = img_save.shape
        #img_new = np.zeros((row,5*col-np.sum(overlap_array)))
        img_new = np.zeros((row, 5 * col))

        img_new[:,:col] = photo_np_array[0,:]
        w_expand_array=[]
        for i in range(0,4):
            w_expand=np.tile(w_array[i],(col,1))
            #print(w_expand.shape)
            w_expand_array.append(w_expand)
        #print(w_expand_array_1[1])
        #w_expand_array=np.array(w_expand_array_1)


        # w_expand = np.tile(w_array[0],(col,1))  # 权重扩增
        # w_expand_1 = np.tile(w_array[1],(col,1))  # 权重扩增
        # img_new[:,col-overlap_array[0]:col] = (1-w_expand_array[0])*photo_np_array[0,:][:,col-overlap_array[0]:col]+w_expand_array[0]*photo_np_array[1,:][:,:overlap_array[0]]
        # img_new[:,2*col-overlap_array[0]-overlap_array[1]:2*col-overlap_array[0]] = (1-w_expand_array[1])*photo_np_array[1,:][:,col-overlap_array[1]:col]+w_expand_array[1]*photo_np_array[2,:][:,:overlap_array[1]]
        #
        # img_new[:,:col-overlap_array[0]]=photo_np_array[0,:][:,:col-overlap_array[0]]
        # img_new[:,col:2*col-overlap_array[0]-overlap_array[1]]=photo_np_array[1,:][:,overlap_array[0]:col-overlap_array[1]]
        # img_new[:,2*col-overlap_array[0]:3*col-overlap_array[0]-overlap_array[1]]=photo_np_array[2,:][:,overlap_array[1]:]
        # img_new=img_new.astype(np.uint16)
        dd=0
        cc=0
        for i in range(0,4):
            cc=dd
            dd=dd+overlap_array[i]
            img_new[:,(i+1)*col-dd:(i+1)*col-cc]=(1-w_expand_array[i])*photo_np_array[i,:][:,col-overlap_array[i]:col]+w_expand_array[i]*photo_np_array[i+1,:][:,:overlap_array[i]]
            img_new[:,(i+1)*col-cc:(i+2)*col-dd]=photo_np_array[i+1,:][:,overlap_array[i]:col]
        img_new=img_new.astype(np.uint16)




        io.imsave("E:\\DATA\\GJTpinjie_for_ppt_5\\" + numstr+".tif", img_new)
        print(numstr)

def start_stitcher():
    pass
if __name__ == '__main__':
    pool = multiprocessing.Pool(15)

    a=find_best_num(650)
    print(a)
    # for i in range(4):
    #
    #     pool.apply_async(start_ststcher_right_bottom, (i*40,(i+1)*40,))
    #     #p = Process(target=start_ststcher_right_bottom, args=(i*40,(i+1)*40))
    #     # p.start()
    #     # p.join()
    #
    pool.close()
    pool.join()
    #print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))



