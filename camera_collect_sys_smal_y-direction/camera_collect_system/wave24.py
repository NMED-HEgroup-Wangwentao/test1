import nidaqmx
import numpy as np
import time
from nidaqmx.constants import AcquisitionType, TaskMode


class Wave:
    def __init__(self):
        self.samplerate = 300000

        # freq = 2.4
        # phase = int(38000)
        # amp = 0.09

        freq = 24
        phase = int(30000)
        amp = 0.09
        self.pointmun = int(np.ceil(self.samplerate / freq))

        # phase=int(34000+self.pointmun/2+1000)

        periods = 50

        w1 = np.linspace(0, -amp, int(self.pointmun / 4))
        w2 = np.linspace(-amp, amp, int(self.pointmun / 2))
        w3 = np.linspace(amp, 0, int(self.pointmun / 4))
        out1 = np.append(w1, w2)
        out1 = np.append(out1, w3)
        o21 = np.ones(50) * 5
        o22 = np.zeros(phase)
        o23 = np.zeros(self.pointmun - phase - 50)
        out2 = np.append(o22, o21)
        out2 = np.append(out2, o23)
        x = np.array(out1)
        out1 = np.tile(x, periods)
        out2 = np.tile(out2, periods)
        self.c = np.vstack((out1, out2))

    def sent_wave(self):
        with nidaqmx.Task() as task:
            task.ao_channels.add_ao_voltage_chan('Dev1/ao0:1')
            task.timing.cfg_samp_clk_timing(self.samplerate, sample_mode=AcquisitionType.CONTINUOUS)
            # print("*" * 50)
            # print('Generation is started')
            task.write(self.c)
            task.control(TaskMode.TASK_COMMIT)
            task.start()

            while True:
                # for i in range(5):
                # print("generating")
                time.sleep(0.5)
                # print(self.pointmun)
            task.close()


if __name__ == '__main__':
    wave = Wave()
    wave.sent_wave()