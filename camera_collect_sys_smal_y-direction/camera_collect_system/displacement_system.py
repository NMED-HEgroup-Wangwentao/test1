import json
import socket
import sys
import binascii
import time
import q

class Displacement_Table_Control:

    def __init__(self):
        self.server_ip = '192.6.94.5'
        self.server_sport = int(1025)

    def connect(self):
        socket.setdefaulttimeout(3)
        self.tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_client_socket.connect((self.server_ip, self.server_sport))

    def query_position(self, data_flag):
        send_x_position_order = b'\x40\xbf\x00\x00\x00\x00\x00\x03\x23\x31\x50'
        send_y_position_order = b'\x40\xbf\x00\x00\x00\x00\x00\x03\x23\x32\x50'
        send_z_position_order = b'\x40\xbf\x00\x00\x00\x00\x00\x03\x23\x33\x50'

        #send_order = b"\x40\xbf\x00\x00\x00\x00\x00\x03\x23\x31\x50"
        if data_flag == "x_position":
            send_order = send_x_position_order
        elif data_flag == "y_position":
            send_order = send_y_position_order
        elif data_flag == "z_position":
            send_order = send_z_position_order

        self.tcp_client_socket.send(send_order)
        self.recvData = self.tcp_client_socket.recv(1024)
        time.sleep(0.1)
        self.recvData = self.recvData.decode('utf-8')
        #print(self.recvData)



        return self.recvData

    def move_and_query(self, axis):
        aa = 'M' + str(axis) + '40'
        BB = len(aa)
        AA = chr(BB)
        DD = str(AA).encode('utf-8')
        cc = str(aa)
        dd = cc.encode("utf-8")
        ddd = b'\x40\xbf\x00\x00\x00\x00\x00' + DD
        send_data_1 = ddd + dd
        self.tcp_client_socket.send(send_data_1)  ###选择是否设置
        time.sleep(0.1)
        recvData = self.tcp_client_socket.recv(1024)
        #print(recvData.decode)

        return recvData.decode('utf-8')

    def update_move_and_query(self,axis):
        while True:
            time.sleep(0.1)

            try:
                a = self.move_and_query(axis)
                #print(a[0])
                if int(a[0]) == 1:
                    break
            except:
                pass
    def chaxun(self):
            send_data_x = b'\x40\xbf\x00\x00\x00\x00\x00\x03\x23\x31\x50'
            self.tcp_client_socket.send(send_data_x)
            recvData = self.tcp_client_socket.recv(1024)
            print('x轴位置为:', recvData.decode('utf-8'))
            send_data_y = b'\x40\xbf\x00\x00\x00\x00\x00\x03\x23\x32\x50'
            self.tcp_client_socket.send(send_data_y)
            recvData = self.tcp_client_socket.recv(1024)
            print('y轴位置为:', recvData.decode('utf-8'))
            send_data_z = b'\x40\xbf\x00\x00\x00\x00\x00\x03\x23\x33\x50'
            self.tcp_client_socket.send(send_data_z)
            recvData = self.tcp_client_socket.recv(1024)
            print('z轴位置为:', recvData.decode('utf-8'))

    def chuansong_1(self,shuju):

        aa = 'P' + str(1000) + '=' + str(shuju)
        BB = len(aa)
        AA = chr(BB)
        DD = str(AA).encode('utf-8')
        cc = str(aa)
        dd = cc.encode("utf-8")
        ddd = ddd = b'\x40\xbf\x00\x00\x00\x00\x00' + DD
        send_data_1 = ddd + dd
        print(send_data_1)
        self.tcp_client_socket.send(send_data_1)
        recvData = self.tcp_client_socket.recv(1024)

    def chuansong_2(self, shuju):

        aa = 'P' + str(2000) + '=' + str(shuju)
        BB = len(aa)
        AA = chr(BB)
        DD = str(AA).encode('utf-8')
        cc = str(aa)
        dd = cc.encode("utf-8")
        ddd = ddd = b'\x40\xbf\x00\x00\x00\x00\x00' + DD
        send_data_1 = ddd + dd
        print(send_data_1)
        self.tcp_client_socket.send(send_data_1)
        recvData = self.tcp_client_socket.recv(1024)

    def chuansong_3(self, shuju):

        aa = 'P' + str(3000) + '=' + str(shuju)
        BB = len(aa)
        AA = chr(BB)
        DD = str(AA).encode('utf-8')
        cc = str(aa)
        dd = cc.encode("utf-8")
        ddd = ddd = b'\x40\xbf\x00\x00\x00\x00\x00' + DD
        send_data_1 = ddd + dd
        print(send_data_1)
        self.tcp_client_socket.send(send_data_1)
        recvData = self.tcp_client_socket.recv(1024)
    def chuansong_start_flag(self,shuju):


        aa = 'P' + str(5000) + '=' + str(shuju)
        BB = len(aa)
        AA = chr(BB)
        DD = str(AA).encode('utf-8')
        cc = str(aa)
        dd = cc.encode("utf-8")
        ddd = ddd = b'\x40\xbf\x00\x00\x00\x00\x00' + DD
        send_data_1 = ddd + dd
        print(send_data_1)
        self.tcp_client_socket.send(send_data_1)
        recvData = self.tcp_client_socket.recv(1024)
    def chaxunp110(self):
        send_data = b'\x40\xbf\x00\x00\x00\x00\x00\x04\x70\x31\x31\x30'
        self.tcp_client_socket.send(send_data)
        recvData = self.tcp_client_socket.recv(1024)
        A=recvData.decode('utf-8')
        print(A)
        print("A[0]:"+A[0])
        return A[0]
    def start_weiyitai(self):
        send_data = b'\x40\xbf\x00\x00\x00\x00\x00\x06\x70\x31\x32\x30\x3D\x32'
        self.tcp_client_socket.send(send_data)
        recvData = self.tcp_client_socket.recv(1024)





    #设置轴速度
    def set_axial_speed(self, axis, speed):
        aa = 'I' + str(axis) + '22' + '=' + str(speed)
        BB = len(aa)
        AA = chr(BB)
        DD = str(AA).encode('utf-8')
        cc = str(aa)
        dd = cc.encode("utf-8")
        ddd = b'\x40\xbf\x00\x00\x00\x00\x00' + DD
        send_data_1 = ddd + dd
        self.tcp_client_socket.send(send_data_1)
        #time.sleep(0.1)
        recvData = self.tcp_client_socket.recv(1024)

    ###轴运动距离
    def set_axis_movement(self,axis, axis_position):
        axis_position = str(axis_position)
        axis = str(axis)
        a = '#' + axis + 'J=' + axis_position
        B = len(a)
        A = chr(B)
        print(B)
        c = a
        D = str(A).encode('utf-8')
        d = c.encode("utf-8")
        ddd = b'\x40\xbf\x00\x00\x00\x00\x00' + D
        send_data = ddd + d
        print("send_data = ", send_data)
        self.tcp_client_socket.send(send_data)  ###选择是否设置
        #time.sleep(0.1)
        recvData = self.tcp_client_socket.recv(1024)
        print('接收到的数据为:', recvData.decode('utf-8'))

    def close_connect(self):
        self.tcp_client_socket.close()

    def set_zero_point(self):
        send_data = b'\x40\xbf\x00\x00\x00\x00\x00\x05\x23\x31\x68\x6D\x7A'
        self.tcp_client_socket.send(send_data)
        recvData = self.tcp_client_socket.recv(1024)
        print('接收到的数据为:', recvData.decode('utf-8'))
        send_data = b'\x40\xbf\x00\x00\x00\x00\x00\x05\x23\x32\x68\x6D\x7A'
        self.tcp_client_socket.send(send_data)
        recvData = self.tcp_client_socket.recv(1024)
        print('接收到的数据为:', recvData.decode('utf-8'))
        send_data = b'\x40\xbf\x00\x00\x00\x00\x00\x05\x23\x33\x68\x6D\x7A'
        self.tcp_client_socket.send(send_data)
        recvData = self.tcp_client_socket.recv(1024)
        print('接收到的数据为:', recvData.decode('utf-8'))

    def hui_dao_yuangchanglingdian(self):
        send_data_2 = b'\x40\xbf\x00\x00\x00\x00\x00\x06\x50\x33\x34\x35\x3D\x31'
        self.tcp_client_socket.send(send_data_2)  ###选择是否设置
        recvData = self.tcp_client_socket.recv(1024)
        send_data_3 = b'\x40\xbf\x00\x00\x00\x00\x00\x06\x50\x32\x34\x35\x3D\x31'
        self.tcp_client_socket.send(send_data_3)  ###选择是否设置
        recvData = self.tcp_client_socket.recv(1024)
        send_data_4 = b'\x40\xbf\x00\x00\x00\x00\x00\x06\x50\x31\x34\x35\x3D\x31'
        self.tcp_client_socket.send(send_data_4)  ###选择是否设置
        recvData = self.tcp_client_socket.recv(1024)
    def shuju_shuru(self, zhou, shuju):
        if int(zhou == 1):
            aa = 'p102=' + str(len(shuju))
            BB = len(aa)
            AA = chr(BB)
            DD = str(AA).encode('utf-8')
            cc = str(aa)
            dd = cc.encode("utf-8")
            ddd = b'\x40\xbf\x00\x00\x00\x00\x00' + DD
            send_data_1 = ddd + dd
            print(send_data_1)
            self.tcp_client_socket.send(send_data_1)  ###选择是否设置

            recvData = self.tcp_client_socket.recv(1024)
            for i in range(len(shuju)):
                print(len(shuju))
                print(i)
                d = 1000 + i
                aa = 'P' + str(d) + '=' + str(shuju[i])
                print(shuju[i])
                BB = len(aa)
                AA = chr(BB)
                DD = str(AA).encode('utf-8')
                cc = str(aa)
                dd = cc.encode("utf-8")
                ddd = b'\x40\xbf\x00\x00\x00\x00\x00' + DD
                send_data_1 = ddd + dd
                print(send_data_1)
                self.tcp_client_socket.send(send_data_1)  ###选择是否设置

                recvData = self.tcp_client_socket.recv(1024)
        if int(zhou == 2):
            aa = 'p202=' + str(len(shuju))
            BB = len(aa)
            AA = chr(BB)
            DD = str(AA).encode('utf-8')
            cc = str(aa)
            dd = cc.encode("utf-8")
            ddd = b'\x40\xbf\x00\x00\x00\x00\x00' + DD
            send_data_1 = ddd + dd
            print(send_data_1)
            self.tcp_client_socket.send(send_data_1)  ###选择是否设置

            recvData = self.tcp_client_socket.recv(1024)
            for i in range(len(shuju)):
                d = 2000 + i
                aa = 'P' + str(d) + '=' + str(shuju[i])
                print(shuju[i])
                BB = len(aa)
                AA = chr(BB)
                DD = str(AA).encode('utf-8')
                cc = str(aa)
                dd = cc.encode("utf-8")
                ddd = b'\x40\xbf\x00\x00\x00\x00\x00' + DD
                send_data_1 = ddd + dd
                print(send_data_1)
                self.tcp_client_socket.send(send_data_1)  ###选择是否设置

                recvData = self.tcp_client_socket.recv(1024)
        if int(zhou == 3):
            for i in range(0,len(shuju)):
                d = 3000 + i + 1
                aa = 'P' + str(d) + '=' + str(shuju[i])
                print(shuju[i])
                BB = len(aa)
                AA = chr(BB)
                DD = str(AA).encode('utf-8')
                cc = str(aa)
                dd = cc.encode("utf-8")
                ddd = b'\x40\xbf\x00\x00\x00\x00\x00' + DD
                send_data_1 = ddd + dd
                print(send_data_1)
                self.tcp_client_socket.send(send_data_1)  ###选择是否设置

                recvData = self.tcp_client_socket.recv(1024)
    def chaxun_start_for_thread(self):

        self.update_move_and_query(1)
        print("x停止")

        self.update_move_and_query(2)
        print("y停止")

        self.update_move_and_query(3)
        print("z停止")
    def chaxun_end_for_thread(self):
        #def chaxun_end(self):
            self.update_move_and_query(1)
            print("x停止")

            self.update_move_and_query(2)
            print("y停止")

            self.update_move_and_query(3)
            print("z停止")
            q.start_save_weiyitai = 1

            # q.start_save_buttom = 0
            # self.widgets["start_button"][1].setText("采集数据")

            print("到这里了")


if __name__ == '__main__':
    control = Displacement_Table_Control()
    control.connect()
