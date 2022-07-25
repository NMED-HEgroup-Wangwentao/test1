import serial  # 导入模块
import time

import serial.tools.list_ports


class LaserControl:

    def __init__(self):
        self.portx = ''
        self.serial_start_flag = True
        self.port_list = []

    def check_serial(self):
        self.port_list = list(serial.tools.list_ports.comports())

        if len(self.port_list) == 0:
            return
        else:
            for i in range(0, len(self.port_list)):
                print("串口信息为：", self.port_list[i])

    def open_serial(self):
        self.check_serial()
        self.bps = 115200
        self.timex = 0.5
        #self.ser = serial.Serial(self.portx, self.bps, timeout=self.timex)
        self.serial_start_flag = True


    #####激光器1
    def open_laser_1(self):
        self.ser.write("SOURce1:AM:STATe ON\r".encode())

        self.ser.write("SOURce1:AM:STATe?\r".encode())
        time.sleep(0.1)
        self.a = self.ser.readall()
        self.a = str(self.a)
        print("激光器的状态" + self.a)

    def change_laser_power_1(self, power):
        self.ser.write(("SOURce1:POWer:LEVel:IMMediate:AMPLitude " + str(int(power)/1000) + "\r").encode())
        time.sleep(0.1)
        self.ser.write("SOURce1:POWer:LEVel:IMMediate:AMPLitude?\r".encode())
        time.sleep(0.1)
        self.a = self.ser.readall()
        self.a = str(self.a)
        print("激光器的功率" + self.a)

    def close_laser_1(self):
        self.ser.write("SOURce1:AM:STATe OFF\r".encode())

        self.ser.write("SOURce1:AM:STATe?\r".encode())
        time.sleep(0.1)
        self.a = self.ser.readall()
        self.a = str(self.a)
        print("激光器的状态" + self.a)

    ####激光器2
    def open_laser_2(self):
        self.ser.write("SOURce2:AM:STATe ON\r".encode())

        self.ser.write("SOURce2:AM:STATe?\r".encode())
        time.sleep(0.1)
        self.a = self.ser.readall()
        self.a = str(self.a)
        print("激光器的状态" + self.a)

    def change_laser_power_2(self, power):
        self.ser.write(("SOURce2:POWer:LEVel:IMMediate:AMPLitude " + str(int(power)/1000) + "\r").encode())
        time.sleep(0.1)
        self.ser.write("SOURce2:POWer:LEVel:IMMediate:AMPLitude?\r".encode())
        time.sleep(0.1)
        self.a = self.ser.readall()
        self.a = str(self.a)
        print("激光器的功率" + self.a)

    def close_laser_2(self):
        self.ser.write("SOURce2:AM:STATe OFF\r".encode())

        self.ser.write("SOURce2:AM:STATe?\r".encode())
        time.sleep(0.1)
        self.a = self.ser.readall()
        self.a = str(self.a)
        print("激光器的状态" + self.a)

    ####激光器3
    def open_laser_3(self):
        self.ser.write("SOURce3:AM:STATe ON\r".encode())

        self.ser.write("SOURce3:AM:STATe?\r".encode())
        time.sleep(0.1)
        self.a = self.ser.readall()
        self.a = str(self.a)
        print("激光器的状态" + self.a)

    def change_laser_power_3(self, power):
        self.ser.write(("SOURce3:POWer:LEVel:IMMediate:AMPLitude " + str(int(power)/1000) + "\r").encode())
        time.sleep(0.1)
        self.ser.write("SOURce3:POWer:LEVel:IMMediate:AMPLitude?\r".encode())
        time.sleep(0.1)
        self.a = self.ser.readall()
        self.a = str(self.a)
        print("激光器的功率" + self.a)

    def close_laser_3(self):
        self.ser.write("SOURce3:AM:STATe OFF\r".encode())

        self.ser.write("SOURce3:AM:STATe?\r".encode())
        time.sleep(0.1)
        self.a = self.ser.readall()
        self.a = str(self.a)
        print("激光器的状态" + self.a)

    ####激光器4
    def open_laser_4(self):
        self.ser.write("SOURce4:AM:STATe ON\r".encode())

        self.ser.write("SOURce4:AM:STATe?\r".encode())
        time.sleep(0.1)
        self.a = self.ser.readall()
        self.a = str(self.a)
        print("激光器的状态" + self.a)

    def change_laser_power_4(self, power):
        self.ser.write(("SOURce4:POWer:LEVel:IMMediate:AMPLitude " + str(int(power)/1000) + "\r").encode())
        time.sleep(0.1)
        self.ser.write("SOURce4:POWer:LEVel:IMMediate:AMPLitude?\r".encode())
        time.sleep(0.1)
        self.a = self.ser.readall()
        self.a = str(self.a)
        print("激光器的功率" + self.a)

    def close_laser_4(self):
        self.ser.write("SOURce4:AM:STATe OFF\r".encode())

        self.ser.write("SOURce4:AM:STATe?\r".encode())
        time.sleep(0.1)
        self.a = self.ser.readall()
        self.a = str(self.a)
        print("激光器的状态" + self.a)

    def close_serial(self):
        self.ser.close()
        print("串口关闭")



